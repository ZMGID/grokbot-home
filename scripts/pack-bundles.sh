#!/usr/bin/env bash
# 把 box 上恢复所需的密钥/私密文件打成加密包（GBH1，secret-crypt.py enc-bin）放进 secrets/。
# 只在设置了 GROKBOT_HOME_PASSPHRASE 时运行；明文只在 /tmp 临时存在，结束后 shred。
# tar 用固定排序/属主/mtime + gzip -n，内容没变就不重新加密（避免每次同步都产生新密文、新提交）。
# 用法：bash scripts/pack-bundles.sh        （sync.sh 每次会调用）
# 包清单（box-secrets 包内路径相对于 /，恢复 tar -C / -xzpf；其余相对于 /workspace，恢复 tar -C /workspace -xzpf）：
#   secrets/box-secrets.tgz.enc  ~/.composio_pg_key、~/.lark-cli/config.json、~/.local/share/lark-cli/、
#                                ~/.config/gh/、~/.gitconfig、~/.ssh/、~/servers/、
#                                /workspace/gmail-listener/webhook_url.local、
#                                ~/.grokbot-home/secrets.env（COMPOSIO_API_KEY、GMAIL_WEBHOOK_KEY 的值；不含口令本身）
#   secrets/daily.tgz.enc        /workspace/assistant/daily/
#   secrets/feishu-cli.tgz.enc   /workspace/feishu-cli/（含 survey/、approvals/、chats/、日志）
#   secrets/finance.tgz.enc      /workspace/finance/
# 绝不打印任何密钥内容。
set -uo pipefail
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO" || exit 2
if [[ -z "${GROKBOT_HOME_PASSPHRASE:-}" ]]; then
  echo "!! GROKBOT_HOME_PASSPHRASE 未设置，跳过所有加密包（secrets/*.tgz.enc 保持旧版本）"; exit 0
fi
umask 077
STAGE=$(mktemp -d /tmp/gbh-pack.XXXXXX)
cleanup() { find "$STAGE" -type f -exec shred -u {} + 2>/dev/null; rm -rf "$STAGE"; }
trap cleanup EXIT
FAIL=0
TAROPTS=(--sort=name --owner=0 --group=0 --numeric-owner --mtime=@0)

# pack_enc <out.enc> <base_dir> <rel_path>...   不存在的路径自动跳过；全都不存在则不动旧包
pack_enc() {
  local out=$1 base=$2; shift 2
  local paths=() p
  for p in "$@"; do [[ -e "$base/$p" ]] && paths+=("$p"); done
  if [[ ${#paths[@]} -eq 0 ]]; then echo "   $out：源文件都不存在，跳过"; return 0; fi
  local new="$STAGE/new.tgz" old="$STAGE/old.tgz"
  tar "${TAROPTS[@]}" -C "$base" -cf - "${paths[@]}" | gzip -n > "$new"
  if [[ ! -s "$new" ]]; then echo "!! $out：打包失败"; FAIL=1; return 0; fi
  if [[ -f "$out" ]] && python3 scripts/secret-crypt.py dec-bin "$out" "$old" >/dev/null 2>&1 && cmp -s "$new" "$old"; then
    echo "   $out 内容未变化"
  elif python3 scripts/secret-crypt.py enc-bin "$new" "$out" && [[ "$(head -c 4 "$out")" == "GBH1" ]]; then
    echo "   已更新 $out"
  else
    echo "!! 加密 $out 失败"; FAIL=1
  fi
  shred -u "$new" "$old" 2>/dev/null; rm -f "$new" "$old"
}

# --- box-secrets：先把需要的文件拷到 STAGE/root（保持相对 / 的路径），再加上环境变量密钥文件 ---
ROOT="$STAGE/root"; mkdir -p "$ROOT"
H="${HOME#/}"   # home/box
for p in \
  "$H/.composio_pg_key" \
  "$H/.lark-cli/config.json" \
  "$H/.local/share/lark-cli" \
  "$H/.config/gh/hosts.yml" "$H/.config/gh/config.yml" \
  "$H/.gitconfig" \
  "$H/.ssh/config" "$H/.ssh/known_hosts" \
  "$H/servers" \
  "workspace/gmail-listener/webhook_url.local"; do
  if [[ -e "/$p" ]]; then mkdir -p "$ROOT/$(dirname "$p")"; cp -a "/$p" "$ROOT/$p"; fi
done
# 新增 ssh 私钥（若以后放进 ~/.ssh）也一起带上
for k in "$HOME"/.ssh/id_*; do [[ -f "$k" ]] && { mkdir -p "$ROOT/$H/.ssh"; cp -a "$k" "$ROOT/$H/.ssh/"; }; done
ENVF="$ROOT/$H/.grokbot-home/secrets.env"
for v in COMPOSIO_API_KEY GMAIL_WEBHOOK_KEY GMAIL_WEBHOOK_URL; do
  if [[ -n "${!v:-}" ]]; then mkdir -p "$(dirname "$ENVF")"; printf 'export %s=%q\n' "$v" "${!v}" >> "$ENVF"; fi
done
[[ -f "$ENVF" ]] && chmod 600 "$ENVF"
mapfile -t BOXPATHS < <(cd "$ROOT" && find . -mindepth 1 \( -type f -o -type l \) -printf '%P\n' | sort)
pack_enc secrets/box-secrets.tgz.enc "$ROOT" "${BOXPATHS[@]}"

pack_enc secrets/daily.tgz.enc      /workspace assistant/daily
pack_enc secrets/feishu-cli.tgz.enc /workspace feishu-cli
pack_enc secrets/finance.tgz.enc    /workspace finance

exit $FAIL
