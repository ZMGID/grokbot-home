#!/usr/bin/env bash
# 每日同步的“机械部分”：收集 bot 文件 → 更新清单 → 暂存 → 密钥扫描 → 有变化才 commit + push。
# “理解对话、写 CONTEXT.md”那部分由仓库管家在运行本脚本之前完成（见 scripts/sync.md）。
# 用法：bash scripts/sync.sh [--dry-run]
#   --dry-run：照常收集文件、跑密钥扫描、显示会提交什么，但不 commit、不 push（收集到的文件会留在工作区）。
# 推送目标固定为 origin（https://github.com/ZMGID/grokbot-home）的 main 分支；推送需要 gh 已登录（ZMGID）。
set -uo pipefail
DRY=0; [[ "${1:-}" == "--dry-run" ]] && DRY=1
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
AGENTS=/home/box/agent-data/agents
WORKFLOWS=/home/box/agent-data/workflows
REMOTE=origin; BRANCH=main
cd "$REPO" || exit 2
export PATH="$HOME/.local/bin:$PATH"

# 0) 确认是正确的仓库和分支
URL=$(git remote get-url "$REMOTE" 2>/dev/null || true)
[[ "$URL" =~ github\.com[:/]ZMGID/grokbot-home(\.git)?$ ]] || { echo "!! $REMOTE 不是 ZMGID/grokbot-home（$URL），中止"; exit 2; }
CUR=$(git rev-parse --abbrev-ref HEAD 2>/dev/null)
[[ "$CUR" == "$BRANCH" ]] || { echo "!! 当前分支是 $CUR，不是 $BRANCH，中止"; exit 2; }
git config user.name  >/dev/null || git config user.name ZMGID
git config user.email >/dev/null || git config user.email 214914950+ZMGID@users.noreply.github.com

echo "== git pull"
gh auth setup-git >/dev/null 2>&1 || true
git pull --rebase --autostash -q "$REMOTE" "$BRANCH" || { echo "!! git pull 失败"; exit 3; }

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
    # bot 自己的记忆文件（memory/profile.md、memory/log/），原样备份（只要 .md，不要数据库/其他文件）
    if [[ -d "$src/memory" ]]; then
      mkdir -p "$dst/memory"
      (cd "$src/memory" && find . -type f -name '*.md' -print0) | while IFS= read -r -d '' m; do
        mkdir -p "$dst/memory/$(dirname "$m")"; cp "$src/memory/$m" "$dst/memory/$m"
      done
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

# 4) 暂存后做密钥扫描（扫描范围就是将要提交的文件 + 未推送提交；不干净就撤销暂存并停）
git add -A
if ! bash scripts/secret-scan.sh "$REPO"; then
  git reset -q; echo "!! 密钥扫描未通过，中止，不提交（已撤销暂存）"; exit 4
fi

# 5) 有变化才提交
if git diff --cached --quiet; then
  echo "== 没有变化"
  # 仍可能有之前没推上去的提交
  if [[ $DRY -eq 0 ]] && [[ -n "$(git log "$REMOTE/$BRANCH..HEAD" --oneline 2>/dev/null)" ]]; then
    git push -q "$REMOTE" "HEAD:$BRANCH" && echo "== 已推送之前未推送的提交" || { echo "!! 推送失败"; exit 5; }
  fi
  exit 0
fi
git diff --cached --stat
if [[ $DRY -eq 1 ]]; then echo "== dry-run：不提交"; git reset -q; exit 0; fi
git commit -q -m "sync: $(date '+%F %H:%M') Asia/Shanghai" || { echo "!! commit 失败"; exit 5; }
for try in 1 2; do
  if git push -q "$REMOTE" "HEAD:$BRANCH"; then echo "== 已推送 $(git rev-parse --short HEAD) → $REMOTE/$BRANCH"; exit 0; fi
  echo "   推送被拒，pull --rebase 后重试"
  git pull --rebase -q "$REMOTE" "$BRANCH" || break
  bash scripts/secret-scan.sh "$REPO" >/dev/null || { echo "!! 合并后的密钥扫描未通过，不推送"; exit 4; }
done
echo "!! 推送失败（检查 gh auth status 是否为 ZMGID）"; exit 5
