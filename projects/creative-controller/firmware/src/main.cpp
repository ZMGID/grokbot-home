// CreativeDial firmware (ESP32-S3) - USB HID keyboard+consumer, BLE HID keyboard,
// 9 keys + 2 EC11 encoders, single/double/long press, "hold-modifier" combos,
// JSON config over USB CDC stored in NVS.
#include <Arduino.h>
#include <USB.h>
#include <USBHIDKeyboard.h>
#include <USBHIDConsumerControl.h>
#include <Preferences.h>
#include <ArduinoJson.h>
#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEHIDDevice.h>
#include <HIDTypes.h>
#include <BLESecurity.h>
#include "driver/gpio.h"
#include "driver/rtc_io.h"
#include "esp_sleep.h"

#define FW_VERSION "1.1.0"
// ---------------- Pin map (must match pcb/netlist) ----------------
enum { K_TOP, K_SIDE, K_TR1, K_TR2, K_TALL1, K_TALL2, K_BR, K_KNOB, K_WHEEL, NKEYS };
static const uint8_t KEY_PINS[NKEYS] = {4, 5, 6, 7, 15, 16, 17, 18, 8};
static const char *KEY_NAMES[NKEYS] = {"top","side","tr1","tr2","tall1","tall2","br","knob_press","wheel_press"};
#define ENC_KNOB_A 9
#define ENC_KNOB_B 10
#define ENC_WHEEL_A 11
#define ENC_WHEEL_B 12
// EC11E18244A5: 36 detents / 18 pulses -> 2 quadrature transitions per detent (rest at AB=00 and AB=11).
// Mouse-wheel encoder: default also 2; override with config key "wheel_steps" (2 or 4).
#ifndef ENC_STEPS
#define ENC_STEPS 2
#endif
#define LED_PIN 48       // GPIO48 -> U5 SN74LV1T34 (VSYS level) -> WS2812B DIN
#define VBAT_ADC 1       // GPIO1: battery (after power switch) via 100k/100k divider
#define CHG_STAT 2       // GPIO2: MCP73831 STAT via 15k/22k divider: LOW = charging (or no battery), HIGH = charge complete
#define VBUS_SENSE 13    // GPIO13: VBUS via 22k/39k divider, HIGH = USB power present

USBHIDKeyboard Keyboard;
USBHIDConsumerControl Consumer;
Preferences prefs;

// ---------------- Actions ----------------
// action string syntax: "ctrl+z", "ctrl+shift+z", "[", "space", "consumer:volup", "hold:space", "" (none)
struct Action { uint8_t mods; uint8_t key; uint16_t consumer; bool hold; };
static Action parseAction(const char *s) {
  Action a{0,0,0,false};
  String str(s); str.toLowerCase();
  if (str.startsWith("hold:")) { a.hold = true; str = str.substring(5); }
  if (str.startsWith("consumer:")) {
    String c = str.substring(9);
    if (c=="volup") a.consumer=0xE9; else if (c=="voldown") a.consumer=0xEA;
    else if (c=="mute") a.consumer=0xE2; else if (c=="play") a.consumer=0xCD;
    else a.consumer = strtol(c.c_str(), nullptr, 0);
    return a;
  }
  int start = 0;
  while (start <= (int)str.length()) {
    int p = str.indexOf('+', start); if (p == start && p >= 0 && p == (int)str.length()-1) p = -1;
    String t = (p < 0) ? str.substring(start) : str.substring(start, p);
    if (t=="ctrl") a.mods |= 0x01; else if (t=="shift") a.mods |= 0x02;
    else if (t=="alt") a.mods |= 0x04; else if (t=="cmd"||t=="win"||t=="gui") a.mods |= 0x08;
    else if (t.length()==1) { char ch=t[0];
      if (ch>='a'&&ch<='z') a.key=0x04 + (ch-'a'); else if (ch>='1'&&ch<='9') a.key=0x1E + (ch-'1');
      else if (ch=='0') a.key=0x27; else if (ch=='[') a.key=0x2F; else if (ch==']') a.key=0x30;
      else if (ch=='-') a.key=0x2D; else if (ch=='=') a.key=0x2E; else if (ch=='+') a.key=0x2E;
      else if (ch==',') a.key=0x36; else if (ch==';') a.key=0x33; else if (ch=='\'') a.key=0x34; else if (ch=='`') a.key=0x35; else if (ch=='\\') a.key=0x31; else if (ch=='.') a.key=0x37; else if (ch=='/') a.key=0x38; }
    else if (t=="space") a.key=0x2C; else if (t=="enter") a.key=0x28; else if (t=="esc") a.key=0x29;
    else if (t=="tab") a.key=0x2B; else if (t=="del") a.key=0x4C; else if (t=="backspace") a.key=0x2A;
    else if (t=="ins") a.key=0x49; else if (t=="home") a.key=0x4A; else if (t=="end") a.key=0x4D; else if (t=="pgup") a.key=0x4B; else if (t=="pgdn") a.key=0x4E;
    else if (t=="up") a.key=0x52; else if (t=="down") a.key=0x51; else if (t=="left") a.key=0x50; else if (t=="right") a.key=0x4F;
    else if (t.length()>1 && t[0]=='f') { int n=t.substring(1).toInt(); if(n>=1&&n<=12) a.key=0x3A + n - 1; }
    if (p < 0) break; start = p + 1;
  }
  return a;
}

// ---------------- Config ----------------
// events: <key>.single / <key>.double / <key>.long, knob.cw/ccw, wheel.up/down,
// combos: "<holdkey>+knob.cw" etc. (encoder turned while holding a key)
JsonDocument cfg;
static const char *DEFAULT_CFG = R"JSON({"name":"Photoshop","map":{
"top.single":"e","top.double":"ctrl+z","top.long":"hold:space",
"side.single":"ctrl+z","side.double":"ctrl+shift+z",
"tr1.single":"i","tr2.single":"b","tall1.single":"hold:space","tall2.single":"hold:alt",
"br.single":"ctrl+0","br.double":"ctrl+shift+n",
"knob_press.single":"0","wheel_press.single":"u",
"knob.cw":"]","knob.ccw":"[",
"wheel.up":"ctrl+=","wheel.down":"ctrl+-",
"side+knob.cw":"r","side+knob.ccw":"shift+r",
"tr1+knob.cw":".","tr1+knob.ccw":",",
"top+wheel.up":"shift+]","top+wheel.down":"shift+["}})JSON";

void loadCfg() {
  prefs.begin("cdial", true);
  String s = prefs.getString("cfg", DEFAULT_CFG);
  prefs.end();
  if (deserializeJson(cfg, s)) deserializeJson(cfg, DEFAULT_CFG);
}
bool saveCfg(const String &s) {
  JsonDocument tmp; if (deserializeJson(tmp, s)) return false;
  if (!tmp["map"].is<JsonObject>()) return false;
  prefs.begin("cdial", false); prefs.putString("cfg", s); prefs.end();
  cfg = tmp; return true;
}
const char *lookup(const String &ev) { const char *v = cfg["map"][ev] | ""; return v; }

// ---------------- BLE HID ----------------
static const uint8_t REPORT_MAP[] = {
  0x05,0x01,0x09,0x06,0xA1,0x01,0x85,0x01,0x05,0x07,0x19,0xE0,0x29,0xE7,0x15,0x00,0x25,0x01,
  0x75,0x01,0x95,0x08,0x81,0x02,0x95,0x01,0x75,0x08,0x81,0x01,0x95,0x06,0x75,0x08,0x15,0x00,
  0x25,0x65,0x05,0x07,0x19,0x00,0x29,0x65,0x81,0x00,0xC0 };
BLEHIDDevice *hid = nullptr; BLECharacteristic *bleIn = nullptr; volatile bool bleConn = false;
class SrvCB : public BLEServerCallbacks {
  void onConnect(BLEServer *) override { bleConn = true; }
  void onDisconnect(BLEServer *s) override { bleConn = false; s->getAdvertising()->start(); }
};
void bleBegin() {
  BLEDevice::init("CreativeDial");
  BLESecurity *sec = new BLESecurity();            // must be configured BEFORE advertising starts
  sec->setAuthenticationMode(ESP_LE_AUTH_REQ_SC_BOND); sec->setCapability(ESP_IO_CAP_NONE);
  sec->setInitEncryptionKey(ESP_BLE_ENC_KEY_MASK | ESP_BLE_ID_KEY_MASK);
  BLEServer *srv = BLEDevice::createServer(); srv->setCallbacks(new SrvCB());
  hid = new BLEHIDDevice(srv);
  bleIn = hid->inputReport(1);
  hid->manufacturer()->setValue("OpenMaker");
  hid->pnp(0x02, 0x303A, 0x8001, 0x0100);
  hid->hidInfo(0x00, 0x01);
  hid->reportMap((uint8_t *)REPORT_MAP, sizeof(REPORT_MAP));
  hid->startServices();
  hid->setBatteryLevel(100);
  BLEAdvertising *adv = srv->getAdvertising();
  adv->setAppearance(0x03C1); adv->addServiceUUID(hid->hidService()->getUUID()); adv->setScanResponse(true); adv->start();
}
void bleReport(uint8_t mods, uint8_t key) {
  if (!bleConn) return; uint8_t r[8] = {mods,0,key,0,0,0,0,0};
  bleIn->setValue(r, 8); bleIn->notify();
}

// ---------------- Output ----------------
bool usbMounted() { return (bool)USB; }
bool selftest = false;            // hardware bring-up mode: no HID output, print raw events
uint32_t lastActivity = 0;
void sendDown(const Action &a) {
  lastActivity = millis();
  if (selftest) return;
  bool usb = usbMounted();            // don't call TinyUSB when not enumerated (avoids report timeouts on battery)
  if (a.consumer) { if (usb) Consumer.press(a.consumer); return; }   // consumer keys: USB only (BLE map is keyboard-only)
  KeyReport r{}; r.modifiers = a.mods; r.keys[0] = a.key;
  if (usb) Keyboard.sendReport(&r);
  if (!usb || (cfg["ble_when_usb"] | false)) bleReport(a.mods, a.key);   // avoid double keystrokes when both links go to one PC
}
void sendUp(const Action &a) {
  if (selftest) return;
  bool usb = usbMounted();
  if (a.consumer) { if (usb) Consumer.release(); return; }
  if (usb) Keyboard.releaseAll();
  bleReport(0, 0);
}
void tap(const char *s) { if (!*s) return; Action a = parseAction(s); sendDown(a); delay(8); sendUp(a); }

// ---------------- Keys: debounce + single/double/long ----------------
const uint32_t DEBOUNCE=5, DOUBLE_MS=250, LONG_MS=450;
struct KeyState { bool down=false, raw=false; uint32_t tChange=0, tDown=0, tUp=0; uint8_t clicks=0;
  bool usedAsMod=false, longFired=false, holding=false; Action holdAct{}; } ks[NKEYS];

void keyEvent(int k, const char *type) {
  String ev = String(KEY_NAMES[k]) + "." + type; tap(lookup(ev));
  Serial.printf("{\"ev\":\"%s\"}\n", ev.c_str());
}
void scanKeys() {
  uint32_t now = millis();
  for (int k = 0; k < NKEYS; k++) {
    KeyState &s = ks[k]; bool raw = !digitalRead(KEY_PINS[k]);
    if (raw != s.raw) { s.raw = raw; s.tChange = now; }
    if (now - s.tChange >= DEBOUNCE && raw != s.down) {
      s.down = raw; lastActivity = now;
      if (selftest) { Serial.printf("[selftest] key %-11s GPIO%-2d %s\n", KEY_NAMES[k], KEY_PINS[k], raw ? "DOWN" : "up"); continue; }
      if (raw) { // press
        s.tDown = now; s.usedAsMod = false; s.longFired = false;
        String ev = String(KEY_NAMES[k]) + ".single"; const char *m = lookup(ev);
        if (!strncmp(m, "hold:", 5) && s.clicks == 0) { s.holdAct = parseAction(m); sendDown(s.holdAct); s.holding = true; }
      } else { // release
        if (s.holding) { sendUp(s.holdAct); s.holding = false; s.clicks = 0; continue; }
        if (s.usedAsMod || s.longFired) { s.clicks = 0; continue; }
        s.clicks++; s.tUp = now;
        if (s.clicks >= 2) { keyEvent(k, "double"); s.clicks = 0; }
        else if (!*lookup(String(KEY_NAMES[k]) + ".double")) { keyEvent(k, "single"); s.clicks = 0; }
      }
    }
    if (selftest) continue;
    if (s.down && !s.holding && !s.usedAsMod && !s.longFired && now - s.tDown > LONG_MS
        && *lookup(String(KEY_NAMES[k]) + ".long")) {
      String ev = String(KEY_NAMES[k]) + ".long"; const char *m = lookup(ev);
      if (!strncmp(m, "hold:", 5)) { s.holdAct = parseAction(m); sendDown(s.holdAct); s.holding = true; }
      else keyEvent(k, "long");
      s.longFired = true;
    }
    if (!s.down && s.clicks == 1 && now - s.tUp > DOUBLE_MS) { keyEvent(k, "single"); s.clicks = 0; }
  }
}

// ---------------- Encoders (quadrature state machine, ISR) ----------------
static const int8_t QDEC[16] = {0,-1,1,0,1,0,0,-1,-1,0,0,1,0,1,-1,0};
// Table-driven decoder: index = (prev AB << 2) | new AB; invalid (double) transitions = 0 (ignored, bounce-proof).
// A detent is counted only when the encoder arrives in a REST state with |acc| >= steps; acc is cleared at
// every rest state, so contact bounce and missed edges can never accumulate into a phantom step.
struct Enc { uint8_t a,b; volatile uint8_t st; volatile int8_t acc; volatile int32_t det; volatile uint8_t steps; volatile uint32_t edges; } encs[2] =
  {{ENC_KNOB_A,ENC_KNOB_B,0,0,0,ENC_STEPS,0},{ENC_WHEEL_A,ENC_WHEEL_B,0,0,0,ENC_STEPS,0}};
void IRAM_ATTR encIsr(void *arg) {
  Enc *e = (Enc *)arg;
  uint8_t ab = (gpio_get_level((gpio_num_t)e->a) << 1) | gpio_get_level((gpio_num_t)e->b);
  if (ab == (e->st & 3)) return;                       // no change (bounce on the other pin)
  e->st = ((e->st << 2) | ab) & 0x0F; e->edges++;
  e->acc += QDEC[e->st];
  bool rest = (ab == 3) || (e->steps == 2 && ab == 0);
  if (rest) {
    if (e->acc >= (int8_t)e->steps) e->det++; else if (e->acc <= -(int8_t)e->steps) e->det--;
    e->acc = 0;
  } else if (e->acc > 4 || e->acc < -4) e->acc = 0;
}
void handleEnc(int i, const char *name, const char *pos, const char *neg) {
  noInterrupts(); int32_t d = encs[i].det; encs[i].det = 0; interrupts();
  if (d) lastActivity = millis();
  if (selftest) { if (d) Serial.printf("[selftest] enc %s %+d detent(s)  AB=%d%d edges=%u\n", name, (int)d,
                    digitalRead(encs[i].a), digitalRead(encs[i].b), (unsigned)encs[i].edges); return; }
  while (d != 0) {
    const char *dir = d > 0 ? pos : neg; d += d > 0 ? -1 : 1;
    String base = String(name) + "." + dir; String used = base;
    const char *m = "";
    for (int k = 0; k < NKEYS; k++) if (ks[k].down) {           // combo with held key
      String c = String(KEY_NAMES[k]) + "+" + base; const char *mm = lookup(c);
      if (*mm) { m = mm; used = c; ks[k].usedAsMod = true; ks[k].clicks = 0; break; }
    }
    if (!*m) m = lookup(base);
    tap(m); Serial.printf("{\"ev\":\"%s\"}\n", used.c_str());
  }
}

// ---------------- Serial config protocol (JSON lines) ----------------
// {"cmd":"hello"} {"cmd":"get"} {"cmd":"set","config":{...}} {"cmd":"reset"}
// ---------------- Power: battery, USB detect, charge state, deep sleep ----------------
bool usbPower() { return digitalRead(VBUS_SENSE); }
bool charging() { return usbPower() && !digitalRead(CHG_STAT); }
int batteryMv() {                       // 1:2 divider, ADC1 (BLE-safe), 11 dB attenuation, averaged
  uint32_t s = 0; for (int i = 0; i < 16; i++) s += analogReadMilliVolts(VBAT_ADC);
  return (int)(s / 16) * 2;
}
int batteryPct(int mv) {                // simple LiPo curve (resting voltage)
  static const int T[][2] = {{4150,100},{4000,85},{3900,72},{3800,55},{3700,35},{3600,15},{3500,5},{3300,0}};
  if (mv >= T[0][0]) return 100;
  for (int i = 1; i < 8; i++) if (mv >= T[i][0]) return T[i][1] + (mv - T[i][0]) * (T[i-1][1] - T[i][1]) / (T[i-1][0] - T[i][0]);
  return 0;
}
void goToSleep() {                      // wake on ANY key press (all key GPIOs are RTC GPIOs 4..18)
  Serial.println("{\"ev\":\"sleep\"}"); Serial.flush();
  neopixelWrite(LED_PIN, 0, 0, 0);
  uint64_t mask = 0;
  for (int k = 0; k < NKEYS; k++) { gpio_num_t g = (gpio_num_t)KEY_PINS[k]; mask |= 1ULL << g;
    rtc_gpio_init(g); rtc_gpio_set_direction(g, RTC_GPIO_MODE_INPUT_ONLY); rtc_gpio_pullup_en(g); rtc_gpio_pulldown_dis(g); }
  esp_sleep_pd_config(ESP_PD_DOMAIN_RTC_PERIPH, ESP_PD_OPTION_ON);   // keep RTC pull-ups alive
  esp_sleep_enable_ext1_wakeup(mask, ESP_EXT1_WAKEUP_ANY_LOW);
  esp_deep_sleep_start();
}

String line;
void handleLine(const String &l) {
  JsonDocument req; if (deserializeJson(req, l)) { Serial.println("{\"ok\":false,\"err\":\"json\"}"); return; }
  String cmd = req["cmd"] | "";
  if (cmd == "hello") Serial.printf("{\"ok\":true,\"device\":\"CreativeDial\",\"fw\":\"%s\",\"keys\":%d}\n", FW_VERSION, NKEYS);
  else if (cmd == "get") { Serial.print("{\"ok\":true,\"config\":"); serializeJson(cfg, Serial); Serial.println("}"); }
  else if (cmd == "set") { String s; serializeJson(req["config"], s); Serial.println(saveCfg(s) ? "{\"ok\":true}" : "{\"ok\":false,\"err\":\"bad config\"}"); }
  else if (cmd == "reset") { prefs.begin("cdial", false); prefs.clear(); prefs.end(); loadCfg(); Serial.println("{\"ok\":true}"); }
  else if (cmd == "battery") { Serial.printf("{\"ok\":true,\"mv\":%d,\"pct\":%d,\"usb\":%s,\"charging\":%s,\"full\":%s}\n", batteryMv(), batteryPct(batteryMv()),
      usbPower()?"true":"false", charging()?"true":"false", (usbPower() && digitalRead(CHG_STAT))?"true":"false"); }
  else if (cmd == "selftest") { selftest = req["on"] | !selftest; Serial.printf("{\"ok\":true,\"selftest\":%s}\n", selftest?"true":"false"); }
  else if (cmd == "sleep") { goToSleep(); }
  else Serial.println("{\"ok\":false,\"err\":\"unknown cmd\"}");
}

void setup() {
  for (int k = 0; k < NKEYS; k++) { if (rtc_gpio_is_valid_gpio((gpio_num_t)KEY_PINS[k])) rtc_gpio_deinit((gpio_num_t)KEY_PINS[k]);
    pinMode(KEY_PINS[k], INPUT_PULLUP); }
  pinMode(CHG_STAT, INPUT);            // external 15k/22k divider, no pull
  pinMode(VBUS_SENSE, INPUT);          // external 22k/39k divider
  analogSetPinAttenuation(VBAT_ADC, ADC_11db);
  for (auto &e : encs) { pinMode(e.a, INPUT_PULLUP); pinMode(e.b, INPUT_PULLUP);
    e.st = (digitalRead(e.a) << 1) | digitalRead(e.b);
    attachInterruptArg(e.a, encIsr, &e, CHANGE); attachInterruptArg(e.b, encIsr, &e, CHANGE); }
  loadCfg();
  { int ws = cfg["wheel_steps"] | ENC_STEPS; encs[1].steps = (ws == 4) ? 4 : 2; int ks_ = cfg["knob_steps"] | ENC_STEPS; encs[0].steps = (ks_ == 4) ? 4 : 2; }
  delay(20); selftest = !digitalRead(KEY_PINS[K_TOP]);   // hold TOP key while powering on -> self-test mode
  Keyboard.begin(); Consumer.begin();
  USB.productName("CreativeDial"); USB.manufacturerName("OpenMaker"); USB.begin();
  Serial.begin(115200);
  bleBegin();
  lastActivity = millis();
  if (selftest) {                      // LED test: R, G, B, white
    uint32_t t0 = millis(); while (!Serial && millis() - t0 < 3000) delay(10);
    Serial.printf("[selftest] CreativeDial fw %s - press every key / turn encoders; LED R,G,B,W\n", FW_VERSION);
    const uint8_t c[4][3] = {{40,0,0},{0,40,0},{0,0,40},{30,30,30}};
    for (auto &x : c) { neopixelWrite(LED_PIN, x[0], x[1], x[2]); delay(300); }
  }
  neopixelWrite(LED_PIN, 0, 20, 0);
}

void loop() {
  scanKeys();
  handleEnc(0, "knob", "cw", "ccw");
  handleEnc(1, "wheel", "up", "down");
  while (Serial.available()) { char c = Serial.read();
    if (c == '\n') { handleLine(line); line = ""; } else if (line.length() < 4096) line += c; }
  static uint32_t tl = 0, tb = 0; static int lastPct = -1;
  if (millis() - tl > 1000) { tl = millis();
    bool usb = usbPower(), chg = charging(); int mv = batteryMv();
    // LED: orange = charging, green = charged, blue = BLE connected, dim cyan = USB HID only, off on low battery
    if (chg) neopixelWrite(LED_PIN, 30, 8, 0);
    else if (usb && digitalRead(CHG_STAT)) neopixelWrite(LED_PIN, 0, 25, 0);
    else if (mv < 3450 && !usb) neopixelWrite(LED_PIN, 0, 0, 0);
    else if (bleConn) neopixelWrite(LED_PIN, 0, 0, 25);
    else neopixelWrite(LED_PIN, 0, usbMounted() ? 8 : 0, usbMounted() ? 8 : 4);
    if (selftest && millis() - tb > 2000) { tb = millis();
      Serial.printf("[selftest] vbat=%dmV (%d%%) usb=%d chg_stat=%d charging=%d ble=%d usb_hid=%d\n", mv, batteryPct(mv), usb, digitalRead(CHG_STAT), chg, (int)bleConn, (int)usbMounted()); }
    int pct = batteryPct(mv); if (hid && abs(pct - lastPct) >= 2) { hid->setBatteryLevel(pct); lastPct = pct; }
    uint32_t idle = (uint32_t)((cfg["sleep_min"] | 10)) * 60000UL;
    if (!usb && !selftest && idle && millis() - lastActivity > idle) goToSleep();
    static uint8_t lowCnt = 0;           // unprotected-cell safety net: sleep below 3.30 V (5 consecutive readings)
    lowCnt = (!usb && mv > 1000 && mv < 3300) ? lowCnt + 1 : 0;
    if (lowCnt >= 5) { Serial.println("{\"ev\":\"low_battery\"}"); goToSleep(); }
  }
  delay(1);
}
