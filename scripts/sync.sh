#!/usr/bin/env bash
# 每日同步的“机械部分”：收集 bot 文件 → 更新清单 → 密钥扫描 → 有变化才 commit + push。
# “理解对话、写 CONTEXT.md”那部分由主 bot 在运行本脚本之前完成（见 scripts/sync.md）。
# 用法：bash scripts/sync.sh [--dry-run]
set -uo pipefail
DRY=0; [[ "${1:-}" == "--dry-run" ]] && DRY=1
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
AGENTS=/home/box/agent-data/agents
WORKFLOWS=/home/box/agent-data/workflows
cd "$REPO" || exit 2

echo "== git pull"
git pull --rebase --autostash -q || { echo "!! git pull 失败"; exit 3; }

# 1) 原始设定快照：profile.json / settings.json（不含密钥）。按 index.json 里的 slug ↔ 当前 agent id 映射。
#    新号上 agent id 会变：BOOTSTRAP 第 6 步建完 bot 后要更新 bots/agent-map.json（不含密钥，可以提交），
#    格式：{"grok-bot": "<当前 id>", "xiaozhi": "<当前 id>", ...}。没有映射的 bot 跳过快照。
MAP=bots/agent-map.json
if [[ -f "$MAP" ]]; then
  for slug in $(jq -r 'keys[]' "$MAP"); do
    id=$(jq -r --arg s "$slug" '.[$s]' "$MAP")
    src="$AGENTS/$id"; dst="bots/$slug/raw"
    [[ -d "$src" ]] || { echo "   跳过 $slug（$src 不存在）"; continue; }
    mkdir -p "$dst"
    for f in profile.json settings.json; do
      [[ -f "$src/$f" ]] && jq 'del(.serverId)' "$src/$f" > "$dst/$f" 2>/dev/null
    done
    # 自定义头像（若有）
    for a in "$src"/avatar.{png,jpg,jpeg,webp,gif,svg}; do [[ -f "$a" ]] && cp "$a" "bots/$slug/"; done
    # bot 自己的记忆文件（memory/profile.md、memory/log/），原样备份
    if [[ -d "$src/memory" ]]; then
      mkdir -p "$dst/memory"; cp -r "$src/memory/." "$dst/memory/"
    fi
  done
else
  echo "   没有 $MAP，跳过原始设定快照"
fi

# 2) 用户自建技能
if [[ -d "$WORKFLOWS" ]] && [[ -n "$(ls -A "$WORKFLOWS" 2>/dev/null)" ]]; then
  for d in "$WORKFLOWS"/*/; do
    slug=$(basename "$d"); mkdir -p "skills/$slug"; cp -r "$d." "skills/$slug/"
  done
  echo "   已同步 $(ls -d "$WORKFLOWS"/*/ | wc -l) 个技能"
fi

# 3) 工具环境清单（帮助发现 setup.sh 漏了什么）
{
  echo "# 工具环境快照（自动生成，$(date '+%F %T %Z')）"
  for c in kicad-cli pio node npm npx pnpm bun gh git git-lfs java uv cargo go prusa-slicer gitleaks; do
    p=$(command -v "$c" 2>/dev/null); echo "- $c: ${p:-MISSING}"
  done
  echo; echo "## pip --user"; python3 -m pip list --user --format=freeze 2>/dev/null | sed 's/^/- /'
} > scripts/env-snapshot.md

# 4) 密钥扫描（不干净就停）
bash scripts/secret-scan.sh "$REPO" || { echo "!! 密钥扫描未通过，中止，不提交"; exit 4; }

# 5) 有变化才提交
git add -A
if git diff --cached --quiet; then
  echo "== 没有变化"; exit 0
fi
git diff --cached --stat
if [[ $DRY -eq 1 ]]; then echo "== dry-run：不提交"; git reset -q; exit 0; fi
git commit -q -m "sync: $(date '+%F %H:%M') Asia/Shanghai" && git push -q && echo "== 已推送"
