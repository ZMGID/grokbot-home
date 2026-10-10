#!/usr/bin/env bash
# grokbot-home 工具环境安装脚本（可重复运行 / idempotent）
# 目标环境：Grok Bot 的 box（Debian 13 trixie, x86_64, 用户 box, 有 sudo）。
# 用法：  bash setup.sh            # 全装
#         bash setup.sh --light    # 跳过重型包（KiCad、LibreOffice、PrusaSlicer、cadquery、PlatformIO 工具链）
# 每一步都会先检查是否已安装，已装就跳过。重型安装可能要 10–20 分钟，建议后台运行并看日志。
# 本脚本不包含、也不会写入任何密钥。

set -uo pipefail

LIGHT=0
[[ "${1:-}" == "--light" ]] && LIGHT=1

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOCAL_BIN="$HOME/.local/bin"
mkdir -p "$LOCAL_BIN"
export PATH="$LOCAL_BIN:$HOME/.cargo/bin:$PATH"

FAILED=()
log()  { printf '\n\033[1;34m==> %s\033[0m\n' "$*"; }
ok()   { printf '    \033[32m✓ %s\033[0m\n' "$*"; }
warn() { printf '    \033[33m! %s\033[0m\n' "$*"; FAILED+=("$*"); }
have() { command -v "$1" >/dev/null 2>&1; }

SUDO=""
if [[ $EUID -ne 0 ]] && have sudo; then SUDO="sudo"; fi

# ---------------------------------------------------------------------------
# 0. PATH：让 ~/.local/bin（pio、gitleaks 等）在新 shell 里也可用
# ---------------------------------------------------------------------------
log "PATH"
if ! grep -q 'HOME/.local/bin' "$HOME/.bashrc" 2>/dev/null; then
  echo 'export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$PATH"' >> "$HOME/.bashrc"
  ok "已把 ~/.local/bin 加进 ~/.bashrc"
else
  ok "~/.bashrc 已包含 ~/.local/bin"
fi

# ---------------------------------------------------------------------------
# 1. apt 包（上一个号 box 上手动装过的）
# ---------------------------------------------------------------------------
log "apt packages"
APT_LIGHT=(git gh jq ripgrep curl wget unzip zip tmux poppler-utils ffmpeg
           python3 python3-pip python3-venv python3-tk nodejs npm
           default-jre-headless openjdk-21-jre golang-go rustc cargo
           fonts-noto-cjk fonts-noto-color-emoji xvfb git-lfs)
APT_HEAVY=(kicad prusa-slicer libreoffice-calc libreoffice-writer libreoffice-impress)
APT_WANT=("${APT_LIGHT[@]}")
[[ $LIGHT -eq 0 ]] && APT_WANT+=("${APT_HEAVY[@]}")

APT_MISSING=()
for p in "${APT_WANT[@]}"; do
  dpkg -s "$p" >/dev/null 2>&1 || APT_MISSING+=("$p")
done
if [[ ${#APT_MISSING[@]} -eq 0 ]]; then
  ok "全部已安装"
else
  echo "    缺少: ${APT_MISSING[*]}"
  if $SUDO apt-get update -qq && \
     DEBIAN_FRONTEND=noninteractive $SUDO apt-get install -y -qq --no-install-recommends "${APT_MISSING[@]}"; then
    ok "apt 安装完成"
  else
    warn "apt 安装部分失败: ${APT_MISSING[*]}"
  fi
fi
# KiCad 9（kicad-cli 9.0.x）：Debian 13 自带 kicad 9.0.2。若 apt 版本低于 9，需要换源。
if have kicad-cli; then
  ok "kicad-cli $(kicad-cli --version 2>/dev/null | head -1)"
elif [[ $LIGHT -eq 0 ]]; then
  warn "kicad-cli 不可用（控制器项目需要 KiCad 9）"
fi
have git-lfs && git lfs install --skip-repo >/dev/null 2>&1 && ok "git-lfs 已初始化"

# ---------------------------------------------------------------------------
# 2. Node 工具：pnpm（corepack）、npx mcp-remote 预热
# ---------------------------------------------------------------------------
log "node / npx"
if have node; then ok "node $(node --version)"; else warn "node 缺失"; fi
if ! have pnpm; then
  ($SUDO corepack enable >/dev/null 2>&1 || $SUDO npm i -g pnpm >/dev/null 2>&1) && ok "pnpm 已启用" || warn "pnpm 安装失败"
else
  ok "pnpm $(pnpm --version 2>/dev/null)"
fi
# composio-pg 启动器用 npx -y mcp-remote，这里预先缓存一份，首次连接更快
if have npx; then
  timeout 120 npx -y mcp-remote --help >/dev/null 2>&1 && ok "mcp-remote 已缓存" || ok "mcp-remote 预热跳过（首次连接时会自动下载）"
fi
# bun（上一个号有，非必需）
if ! have bun; then
  (curl -fsSL https://bun.sh/install | bash >/dev/null 2>&1 && ok "bun 已安装") || warn "bun 安装失败（可选）"
else
  ok "bun $(bun --version)"
fi

# ---------------------------------------------------------------------------
# 3. uv（Python 包管理，composio-pg venv 用）
# ---------------------------------------------------------------------------
log "uv"
if ! have uv; then
  curl -LsSf https://astral.sh/uv/install.sh | env UV_INSTALL_DIR="$LOCAL_BIN" sh >/dev/null 2>&1 \
    && ok "uv 已安装" || warn "uv 安装失败"
else
  ok "$(uv --version)"
fi

# ---------------------------------------------------------------------------
# 4. Python 用户级包（PlatformIO、cadquery 等；上一个号是 pip --user 装的）
# ---------------------------------------------------------------------------
log "python user packages"
PY_LIGHT=(platformio pyserial trimesh ezdxf shapely matplotlib scipy networkx PyYAML tabulate)
PY_HEAVY=(cadquery)        # cadquery 2.8 + OCP 7.9，约 1GB，较慢
PY_WANT=("${PY_LIGHT[@]}")
[[ $LIGHT -eq 0 ]] && PY_WANT+=("${PY_HEAVY[@]}")
PY_MISSING=()
for p in "${PY_WANT[@]}"; do
  python3 -m pip show "$p" >/dev/null 2>&1 || PY_MISSING+=("$p")
done
if [[ ${#PY_MISSING[@]} -eq 0 ]]; then
  ok "全部已安装"
else
  echo "    缺少: ${PY_MISSING[*]}"
  python3 -m pip install --user --break-system-packages -q "${PY_MISSING[@]}" \
    && ok "pip 安装完成" || warn "pip 安装部分失败: ${PY_MISSING[*]}"
fi

# ---------------------------------------------------------------------------
# 5. PlatformIO：ESP32-S3 平台（控制器固件用 espressif32@6.9.0）
# ---------------------------------------------------------------------------
log "PlatformIO espressif32"
if have pio; then
  ok "$(pio --version)"
  if [[ $LIGHT -eq 0 ]]; then
    if pio pkg list -g --only-platforms 2>/dev/null | grep -q espressif32; then
      ok "espressif32 平台已安装"
    else
      pio pkg install -g --platform "espressif32@6.9.0" >/dev/null 2>&1 \
        && ok "espressif32@6.9.0 已安装（工具链首次编译时补全）" || warn "espressif32 平台安装失败"
    fi
  fi
else
  warn "pio 不可用"
fi

# ---------------------------------------------------------------------------
# 6. Freerouting（PCB 自动布线，route.sh 默认读 /workspace/freerouting.jar）
# ---------------------------------------------------------------------------
log "freerouting"
FR_JAR=/workspace/freerouting.jar
if [[ -s "$FR_JAR" ]]; then
  ok "$FR_JAR 已存在"
else
  # 上一个号用的是 2023-10-30 构建的版本（v1.9.0）
  curl -fsSL -o "$FR_JAR" https://github.com/freerouting/freerouting/releases/download/v1.9.0/freerouting-1.9.0.jar \
    && ok "已下载 freerouting v1.9.0 → $FR_JAR" || { rm -f "$FR_JAR"; warn "freerouting 下载失败"; }
fi

# ---------------------------------------------------------------------------
# 7. gitleaks（同步任务推送前的密钥扫描）
# ---------------------------------------------------------------------------
log "gitleaks"
if have gitleaks; then
  ok "gitleaks $(gitleaks version)"
else
  V=$(curl -fsSL https://api.github.com/repos/gitleaks/gitleaks/releases/latest | jq -r .tag_name 2>/dev/null)
  if [[ -n "$V" && "$V" != null ]]; then
    TMP=$(mktemp -d)
    curl -fsSL -o "$TMP/gl.tgz" "https://github.com/gitleaks/gitleaks/releases/download/${V}/gitleaks_${V#v}_linux_x64.tar.gz" \
      && tar -xzf "$TMP/gl.tgz" -C "$TMP" gitleaks && mv "$TMP/gitleaks" "$LOCAL_BIN/" && ok "gitleaks $V" \
      || warn "gitleaks 安装失败"
    rm -rf "$TMP"
  else
    warn "无法获取 gitleaks 最新版本号"
  fi
fi

# ---------------------------------------------------------------------------
# 8. composio-pg：启动器 + venv（密钥不在这里，由 bot 通过密码框写入 ~/.composio_pg_key）
# ---------------------------------------------------------------------------
log "composio-pg launcher"
CPG=/workspace/composio-pg
mkdir -p "$CPG"
install -m 700 "$REPO_DIR/connectors/composio-pg/launch.sh" "$CPG/launch.sh"
install -m 600 "$REPO_DIR/connectors/composio-pg/launch.py" "$CPG/launch.py"
ok "launch.sh / launch.py 已放到 $CPG"
if [[ -x "$CPG/.venv/bin/python" ]] && "$CPG/.venv/bin/python" -c "import composio" 2>/dev/null; then
  ok "venv 已就绪（composio $("$CPG/.venv/bin/python" -c 'import composio;print(composio.__version__)' 2>/dev/null)）"
elif have uv; then
  (cd "$CPG" && uv venv -q --prompt composio-pg .venv && uv pip install -q --python .venv/bin/python "composio==0.25.0") \
    && ok "venv 已创建并安装 composio 0.25.0" \
    || { (cd "$CPG" && uv pip install -q --python .venv/bin/python composio) && ok "venv 已安装最新 composio" || warn "composio venv 创建失败"; }
else
  warn "没有 uv，无法创建 composio venv"
fi
if [[ -s "$HOME/.composio_pg_key" ]]; then
  chmod 600 "$HOME/.composio_pg_key"; ok "~/.composio_pg_key 已存在（权限 600）"
else
  echo "    · ~/.composio_pg_key 还不存在：按 BOOTSTRAP.md Step 0 (b) 用口令 GROKBOT_HOME_PASSPHRASE 解密 secrets/COMPOSIO_API_KEY.enc"
fi


# ---------------------------------------------------------------------------
# 8b. composio-zhimeng：zhimeng63 Gmail 专用启动器（共用 ~/.composio_pg_key 与 composio-pg 的 venv）
# ---------------------------------------------------------------------------
log "composio-zhimeng launcher"
CZM=/workspace/composio-zhimeng
mkdir -p "$CZM"
install -m 700 "$REPO_DIR/connectors/composio-zhimeng/launch.sh" "$CZM/launch.sh"
install -m 600 "$REPO_DIR/connectors/composio-zhimeng/launch.py" "$CZM/launch.py"
ok "launch.sh / launch.py 已放到 $CZM（python 用 composio-pg/.venv；密钥同 ~/.composio_pg_key）"
if [[ -x "$CPG/.venv/bin/python" ]]; then
  ok "复用 $CPG/.venv"
else
  warn "composio-pg venv 尚未就绪；先完成上一节再 AddMcpServer composio-zhimeng"
fi
if [[ -s "$HOME/.composio_pg_key" ]]; then
  chmod 600 "$HOME/.composio_pg_key"; ok "~/.composio_pg_key 供 composio-pg 与 composio-zhimeng 共用"
fi


# ---------------------------------------------------------------------------
# 8c. lark-cli（飞书官方 CLI；Composio 无飞书，属例外）+ gmail-listener 脚本
# ---------------------------------------------------------------------------
log "lark-cli (Feishu)"
export PATH="$HOME/.local/bin:$PATH"
if command -v lark-cli >/dev/null 2>&1; then
  ok "lark-cli 已安装：$($(command -v lark-cli) --version 2>/dev/null | head -1 || echo present)"
else
  if have npm || command -v npm >/dev/null 2>&1; then
    npm install -g @larksuite/cli --prefix "$HOME/.local" \
      && ok "已安装 @larksuite/cli → ~/.local" \
      || warn "lark-cli npm 安装失败"
  else
    warn "没有 npm，跳过 lark-cli（见 BOOTSTRAP：换号后手动安装并 QR 登录）"
  fi
fi
# 确保非登录 shell 也能找到
grep -q '\.local/bin' "$HOME/.bashrc" 2>/dev/null || echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
export PATH="$HOME/.local/bin:$PATH"

log "gmail-listener scripts"
GL=/workspace/gmail-listener
mkdir -p "$GL"
if [[ -d "$REPO_DIR/services/gmail-listener" ]]; then
  install -m 755 "$REPO_DIR/services/gmail-listener/start.sh" "$GL/start.sh"
  install -m 755 "$REPO_DIR/services/gmail-listener/stop.sh" "$GL/stop.sh"
  install -m 755 "$REPO_DIR/services/gmail-listener/run_loop.sh" "$GL/run_loop.sh"
  install -m 755 "$REPO_DIR/services/gmail-listener/listener.py" "$GL/listener.py"
  install -m 644 "$REPO_DIR/services/gmail-listener/README.md" "$GL/README.md" 2>/dev/null || true
  ok "listener 脚本已放到 $GL（不含 webhook_url.local / venv / 密钥；盒子重启后需手动 start.sh）"
else
  warn "仓库缺少 services/gmail-listener/"
fi

# ---------------------------------------------------------------------------
# 9. gh 登录状态（只检查，不登录）。仓库公开，克隆不需要登录；只有推送（写回/每日同步）需要，见 BOOTSTRAP Step 1
# ---------------------------------------------------------------------------
log "gh auth"
if gh auth status >/dev/null 2>&1; then
  ok "gh 已登录"
  gh auth setup-git >/dev/null 2>&1 || true
else
  echo "    · gh 未登录：只影响推送。按 BOOTSTRAP Step 1 用 Composio 的 GitHub token 登录（失败再用设备码）"
fi

# ---------------------------------------------------------------------------
log "汇总"
if [[ ${#FAILED[@]} -eq 0 ]]; then
  ok "全部完成"
else
  printf '    \033[33m以下步骤需要关注：\033[0m\n'
  for f in "${FAILED[@]}"; do echo "      - $f"; done
fi
exit 0
