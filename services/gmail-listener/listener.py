#!/usr/bin/env python3
"""Composio Gmail trigger -> Grok Bot webhook forwarder (realtime/Pusher, no public URL).
Secrets come only from env (COMPOSIO_API_KEY, GMAIL_WEBHOOK_KEY); never logged."""
import json, logging, os, sys, threading, time, urllib.request, urllib.error

DIR = os.path.dirname(os.path.abspath(__file__))
def _load_webhook_url():
    u = os.environ.get("GMAIL_WEBHOOK_URL", "").strip()
    if not u:
        f = os.path.join(os.path.dirname(os.path.abspath(__file__)), "webhook_url.local")
        if os.path.exists(f):
            u = open(f).read().strip()
    return u

WEBHOOK_URL = _load_webhook_url()
ACCOUNTS = {"ca_ZnzYtlTeic0s": "ohulercxm8@gmail.com", "ca_5jGHEthCoWuD": "zhimeng63@gmail.com"}
USERS = {"pg-test-5be86c3e-d220-4538-ab6d-ae22d538dfde": "ca_ZnzYtlTeic0s", "zhimeng63": "ca_5jGHEthCoWuD"}
FORWARDED = os.path.join(DIR, "forwarded_ids.txt")  # listener-local dedupe (seen.txt belongs to the routine)
FAILED = os.path.join(DIR, "failed.jsonl")

logging.basicConfig(filename=os.path.join(DIR, "listener.log"), level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(name)s: %(message)s")
log = logging.getLogger("gmail-listener")

class _NoFrames(logging.Filter):
    """SDK error lines may include a raw-frame preview (email content); redact those."""
    def filter(self, rec):
        msg = rec.getMessage()
        if "frame" in msg.lower() or "payload" in msg.lower():
            rec.msg, rec.args = "[redacted SDK message mentioning frame/payload]", None
        return True
for name in ("httpx", "httpcore", "websocket", "urllib3"):
    logging.getLogger(name).setLevel(logging.WARNING)
for name in ("composio", "pysher"):
    lg = logging.getLogger(name); lg.setLevel(logging.ERROR); lg.addFilter(_NoFrames())
for h in logging.getLogger().handlers:
    h.addFilter(_NoFrames())

_lock = threading.Lock()
try:
    with open(FORWARDED) as f:
        _seen = set(l.strip() for l in f if l.strip())
except FileNotFoundError:
    _seen = set()

def post(body: dict) -> bool:
    key = os.environ.get("GMAIL_WEBHOOK_KEY", "")
    data = json.dumps(body).encode()
    req = urllib.request.Request(WEBHOOK_URL, data=data, method="POST", headers={
        "Content-Type": "application/json", "Authorization": f"Bearer {key}", "X-Automation-Key": key})
    try:
        with urllib.request.urlopen(req, timeout=8) as r:
            ok = 200 <= r.status < 300
            log.info("POST event=%s mid=%s -> HTTP %s", body.get("event"), body.get("message_id"), r.status)
    except urllib.error.HTTPError as e:
        ok = False; log.error("POST event=%s mid=%s -> HTTP %s", body.get("event"), body.get("message_id"), e.code)
    except Exception as e:
        ok = False; log.error("POST event=%s mid=%s failed: %s", body.get("event"), body.get("message_id"), type(e).__name__)
    if not ok:
        with _lock, open(FAILED, "a") as f:
            f.write(json.dumps(body) + "\n")
    return ok

def on_event(ev):
    try:
        slug = ev.get("trigger_slug", "")
        meta = ev.get("metadata") or {}
        if slug == "GMAIL_NEW_GMAIL_MESSAGE":
            p = ev.get("payload") or {}
            ca = (meta.get("connected_account") or {}).get("id") or USERS.get(ev.get("user_id", ""), "")
            mid = p.get("message_id") or p.get("id") or ""
            with _lock:
                if mid and mid in _seen:
                    log.info("dup mid=%s skipped", mid); return
                if mid:
                    _seen.add(mid)
                    with open(FORWARDED, "a") as f: f.write(mid + "\n")
            post({"event": "new_mail", "account": ACCOUNTS.get(ca, "unknown"), "connected_account_id": ca,
                  "message_id": mid, "thread_id": p.get("thread_id", ""), "subject": p.get("subject", ""),
                  "sender": p.get("sender", ""), "timestamp": p.get("message_timestamp", "")})
        elif slug in ("composio.trigger.disabled", "composio.connected_account.expired"):
            raw = ev.get("original_payload") or {}
            d = raw.get("data") or ev.get("payload") or {}
            md = raw.get("metadata") or {}
            ca = d.get("connected_account_id") or md.get("connected_account_id") or d.get("id") or ""
            post({"event": "trigger_disabled" if slug.endswith("trigger.disabled") else "account_expired",
                  "account": ACCOUNTS.get(ca, "unknown"), "connected_account_id": ca,
                  "trigger_id": d.get("trigger_id") or md.get("trigger_id") or "",
                  "timestamp": raw.get("timestamp", "")})
        else:
            log.info("ignored event slug=%s", slug)
    except Exception as e:
        log.error("handler error: %s", type(e).__name__)

def main():
    if not WEBHOOK_URL:
        log.error("missing GMAIL_WEBHOOK_URL (env or webhook_url.local)"); sys.exit(2)
    if not os.environ.get("COMPOSIO_API_KEY") or not os.environ.get("GMAIL_WEBHOOK_KEY"):
        log.error("missing COMPOSIO_API_KEY or GMAIL_WEBHOOK_KEY in env"); sys.exit(2)
    from composio import Composio
    backoff = 5
    while True:
        try:
            c = Composio(allow_tracking=False)
            sub = c.triggers.subscribe(timeout=30, on_subscription_error=lambda e: log.error("subscription error callback"))
            sub.handle()(on_event)  # no filters: all project events
            log.info("connected and subscribed to Composio realtime trigger channel")
            backoff = 5
            last_hb = time.time()
            while sub.is_alive() and not sub.has_errored():
                time.sleep(1)
                if time.time() - last_hb > 3600:
                    log.info("heartbeat: still connected"); last_hb = time.time()
            log.warning("subscription dropped; reconnecting")
            try: sub.stop()
            except Exception: pass
        except Exception as e:
            log.error("subscribe failed: %s: %s", type(e).__name__, str(e)[:200])
        time.sleep(backoff); backoff = min(backoff * 2, 300)

if __name__ == "__main__":
    main()
