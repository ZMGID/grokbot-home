#!/usr/bin/env bash
# 密钥扫描：gitleaks + rg 模式 + 实际密钥/口令比对。干净返回 0，发现可疑内容返回 1。
# 用法：bash scripts/secret-scan.sh [仓库目录]
# 扫描范围 = git 会提交的所有文件（git ls-files -co --exclude-standard，含隐藏文件和未跟踪文件）
#            + 还没推送的提交（@{u}..HEAD；没有上游时扫全部历史）。
# 任何情况下都只输出文件名/行号/计数，绝不打印匹配到的内容。
set -uo pipefail
REPO="${1:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
cd "$REPO" || exit 2
export PATH="$HOME/.local/bin:$PATH"
STATUS=0
TMPD=$(mktemp -d "${TMPDIR:-/tmp}/secret-scan.XXXXXX"); chmod 700 "$TMPD"
cleanup() { find "$TMPD" -type f -exec shred -u {} + 2>/dev/null; rm -rf "$TMPD"; }
trap cleanup EXIT

# 要提交的文件清单（NUL 分隔）；只保留实际存在的普通文件
git ls-files -co --exclude-standard -z 2>/dev/null \
  | while IFS= read -r -d '' f; do [[ -f "$f" ]] && printf '%s\0' "$f"; done > "$TMPD/files"
NFILES=$(tr -cd '\0' < "$TMPD/files" | wc -c)
echo "== 将被提交的文件：$NFILES 个"

# 在“将提交的文件”里找固定字符串（-F），只返回命中文件数。$1=模式文件 $2=额外 rg 参数
count_hits() { xargs -0 -r rg -l -F --no-messages $2 -f "$1" -- < "$TMPD/files" 2>/dev/null | wc -l; }
list_hits()  { xargs -0 -r rg -l -F --no-messages $2 -f "$1" -- < "$TMPD/files" 2>/dev/null | sed 's/^/     /'; }
# 未推送提交里的补丁（包括已删除文件、提交说明）
if git rev-parse --verify -q '@{u}' >/dev/null 2>&1; then RANGE='@{u}..HEAD'; else RANGE='--all'; fi
hist_hits() { git rev-parse --verify -q HEAD >/dev/null || { echo 0; return; }
  git log $RANGE -p --no-color --no-ext-diff --format='%B' 2>/dev/null | rg -c -F $2 -f "$1" 2>/dev/null || echo 0; }

if command -v gitleaks >/dev/null 2>&1; then
  echo "== gitleaks（工作区，含未提交文件）"
  gitleaks dir . --redact --no-banner --exit-code 1 || STATUS=1
  if git rev-parse --verify HEAD >/dev/null 2>&1; then
    echo "== gitleaks（git 历史）"
    gitleaks git . --redact --no-banner --exit-code 1 || STATUS=1
  fi
else
  echo "!! 没有 gitleaks，只用 rg 兜底（建议先跑 setup.sh 安装）"
fi

echo "== rg 模式扫描"
PATTERNS='(ak_[A-Za-z0-9]{12,}|ghp_[A-Za-z0-9]{20,}|gho_[A-Za-z0-9]{20,}|ghu_[A-Za-z0-9]{20,}|ghs_[A-Za-z0-9]{20,}|ghr_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|sk-[A-Za-z0-9_-]{20,}|xox[abeprs]-[A-Za-z0-9-]{10,}|-----BEGIN [A-Z ]*PRIVATE KEY-----|AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z_-]{35}|ya29\.[A-Za-z0-9_-]{20,}|(api[_-]?key|secret|token|password|passphrase)["'\'' ]*[:=]["'\'' ]*[A-Za-z0-9_\-]{16,})'
HITS=$(xargs -0 -r rg -n -i -o --no-heading --no-messages -g '!scripts/secret-scan.sh' -g '!*.kicad_pcb' -g '!*.step' -g '!*.stl' -g '!*.3mf' -g '!*.bin' -g '!*.enc' -e "$PATTERNS" -- < "$TMPD/files" 2>/dev/null | cut -d: -f1,2 | sort -u)
if [[ -n "$HITS" ]]; then
  echo "!! 可疑位置（只列文件:行号）："; echo "$HITS"; STATUS=1
fi

# 实际密钥内容比对：~/.composio_pg_key，以及（有口令时）secrets/*.enc 解密出的明文
KEYS=()
[[ -s "$HOME/.composio_pg_key" ]] && KEYS+=("$HOME/.composio_pg_key")
if [[ -n "${GROKBOT_HOME_PASSPHRASE:-}" && -f scripts/secret-crypt.py ]]; then
  for e in secrets/*.enc; do
    [[ -f "$e" ]] || continue
    out="$TMPD/dec.$(basename "$e")"
    if python3 scripts/secret-crypt.py dec "$e" "$out" >/dev/null 2>&1; then KEYS+=("$out:$e")
    else echo "   （$e 用当前口令解不开，跳过该明文比对）"; fi
  done
fi
for entry in "${KEYS[@]}"; do
  kf="${entry%%:*}"; label="${entry#*:}"; [[ "$label" == "$entry" ]] && label="$kf" || label="$label 的明文"
  # 去掉换行/空白，避免空行模式匹配一切
  tr -d '\r\n\t ' < "$kf" > "$TMPD/pat"; [[ -s "$TMPD/pat" ]] || continue
  n=$(count_hits "$TMPD/pat" ""); h=$(hist_hits "$TMPD/pat" "")
  if [[ "$n" -gt 0 || "$h" -gt 0 ]]; then
    echo "!! $label 出现在仓库里（文件 $n 个，未推送提交 $h 处）："; list_hits "$TMPD/pat" ""; STATUS=1
  else
    echo "   $label 没有出现在仓库中"
  fi
done

# 口令本身（GROKBOT_HOME_PASSPHRASE）：短口令只按“整词”匹配，避免 STEP/Gerber 里的数字串误报
if [[ -n "${GROKBOT_HOME_PASSPHRASE:-}" ]]; then
  printf '%s\n' "$GROKBOT_HOME_PASSPHRASE" > "$TMPD/pp"
  if [[ ${#GROKBOT_HOME_PASSPHRASE} -ge 10 ]]; then PPOPT=""; else PPOPT="-w"; fi
  n=$(count_hits "$TMPD/pp" "$PPOPT"); h=$(hist_hits "$TMPD/pp" "$PPOPT")
  if [[ "$n" -gt 0 || "$h" -gt 0 ]]; then
    echo "!! 口令 GROKBOT_HOME_PASSPHRASE 出现在仓库里（文件 $n 个，未推送提交 $h 处）："; list_hits "$TMPD/pp" "$PPOPT"; STATUS=1
  else
    echo "   口令 GROKBOT_HOME_PASSPHRASE 没有出现在仓库中"
  fi
else
  echo "   （未设置 GROKBOT_HOME_PASSPHRASE，跳过口令比对）"
fi

# secrets/ 下只允许 README.md 和真正加密过的 *.enc（GBH1 文件头）
while IFS= read -r -d '' f; do
  case "$f" in
    secrets/README.md) ;;
    secrets/*.enc) [[ "$(head -c 4 "$f")" == "GBH1" ]] || { echo "!! $f 不是 secret-crypt.py 加密格式（可能是明文）"; STATUS=1; } ;;
    secrets/*) echo "!! secrets/ 下不该提交的文件：$f"; STATUS=1 ;;
  esac
done < "$TMPD/files"

# 禁止入库的路径与账本类文件名（收紧，无白名单例外）
# /workspace/finance/ 账本、/workspace/assistant/daily/ 日记，以及任何看起来像 ledger/流水 的已跟踪路径
FORBIDDEN_PATHS=$(tr '\0' '\n' < "$TMPD/files" | rg -i '(^|/)(finance(/|$)|assistant/daily(/|$))' || true)
LEDGER_NAMES=$(tr '\0' '\n' < "$TMPD/files" | rg -i '(^|/)([^/]*(ledger|账本|流水|对账|报销)[^/]*\.(csv|tsv|xlsx|xls|ods|json|md|txt)|[^/]*(ledger|账本|流水)\.[^/]+)$' || true)
if [[ -n "$FORBIDDEN_PATHS" || -n "$LEDGER_NAMES" ]]; then
  echo "!! 禁止入库的财务/日记路径或账本类文件："
  [[ -n "$FORBIDDEN_PATHS" ]] && echo "$FORBIDDEN_PATHS"
  [[ -n "$LEDGER_NAMES" ]] && echo "$LEDGER_NAMES"
  STATUS=1
fi

# 禁止提交的文件名
BAD=$(tr '\0' '\n' < "$TMPD/files" | rg -i '(^|/)(\.env(\..*)?|.*\.pem|.*\.key|id_rsa.*|id_ed25519.*|\.?composio_pg_key|box-secrets\.json|host-secrets\.json|gateway\.json|hosts\.yml|cpg\.err|.*mcp-remote.*\.log|search-index\.db.*|store\.db|conversation-blobs\.db)$' | rg -v '\.env\.example$' || true)
if [[ -n "$BAD" ]]; then echo "!! 不该提交的文件："; echo "$BAD"; STATUS=1; fi

if [[ $STATUS -eq 0 ]]; then echo "== 密钥扫描：干净"; else echo "== 密钥扫描：发现问题，禁止推送"; fi
exit $STATUS
