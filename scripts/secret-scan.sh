#!/usr/bin/env bash
# 密钥扫描：gitleaks 优先，rg 兜底。干净返回 0，发现可疑内容返回 1。
# 用法：bash scripts/secret-scan.sh [仓库目录]
set -uo pipefail
REPO="${1:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
cd "$REPO" || exit 2
export PATH="$HOME/.local/bin:$PATH"
STATUS=0

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
# 只报文件名和行号，不打印匹配内容，避免把密钥带进日志
PATTERNS='(ak_[A-Za-z0-9]{12,}|ghp_[A-Za-z0-9]{20,}|gho_[A-Za-z0-9]{20,}|ghu_[A-Za-z0-9]{20,}|ghs_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|sk-[A-Za-z0-9_-]{20,}|xox[abprs]-[A-Za-z0-9-]{10,}|-----BEGIN [A-Z ]*PRIVATE KEY-----|AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z_-]{35}|(api[_-]?key|secret|token|password)["'\'' ]*[:=]["'\'' ]*[A-Za-z0-9_\-]{16,})'
HITS=$(rg -n -i -o --no-heading -g '!.git' -g '!scripts/secret-scan.sh' -g '!*.kicad_pcb' -g '!*.step' -g '!*.stl' -g '!*.3mf' -g '!*.bin' -e "$PATTERNS" . 2>/dev/null | cut -d: -f1,2 | sort -u)
if [[ -n "$HITS" ]]; then
  echo "!! 可疑位置（只列文件:行号）："
  echo "$HITS"
  STATUS=1
fi
# 实际 key 文件内容比对（只输出是否命中，不打印内容）
for KF in "$HOME/.composio_pg_key"; do
  if [[ -s "$KF" ]]; then
    if rg -l -F -f "$KF" -g '!.git' . >/dev/null 2>&1; then
      echo "!! 仓库里出现了 $KF 的内容！"; STATUS=1
    else
      echo "   $KF 的内容没有出现在仓库中"
    fi
  fi
done
# 禁止提交的文件名
BAD=$(git ls-files -co --exclude-standard 2>/dev/null | rg -i '(^|/)(\.env(\..*)?|.*\.pem|.*\.key|id_rsa.*|id_ed25519.*|\.composio_pg_key|box-secrets\.json|host-secrets\.json|hosts\.yml)$' | rg -v '\.env\.example$' || true)
if [[ -n "$BAD" ]]; then echo "!! 不该提交的文件："; echo "$BAD"; STATUS=1; fi

if [[ $STATUS -eq 0 ]]; then echo "== 密钥扫描：干净"; else echo "== 密钥扫描：发现问题，禁止推送"; fi
exit $STATUS
