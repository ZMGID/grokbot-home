#!/usr/bin/env bash
# 每日同步的“机械部分”：收集 bot 文件 → 更新清单 → 暂存 → 密钥扫描 → 有变化才 commit + push。
# “理解对话、写 CONTEXT.md”那部分由仓库管家在运行本脚本之前完成（见 scripts/sync.md）。
# 用法：bash scripts/sync.sh [--dry-run]
#   --dry-run：照常收集文件、跑密钥扫描、显示会提交什么，但不 commit、不 push（收集到的文件会留在工作区）。
# 推送目标固定为 origin（https://github.com/ZMGID/grokbot-home）的 main 分支。
# 2026-10-11 起不用 gh：git push 失败（退出码 5）属预期，之后改用 Composio GitHub（composio-pg, ZMGID）推送，见 scripts/sync.md。
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
# （2026-10-11 起不用 gh，已移除 gh auth setup-git）
git pull --rebase --autostash -q "$REMOTE" "$BRANCH" || { echo "!! git pull 失败"; exit 3; }

# 1) 原始设定快照：profile.json / settings.json（不含密钥）。
#    agent-map.json format 2：{"format":2,"accounts":{<小萌id>:{...}},"bots":{<slug>:{"ids":{<小萌id>:<agentId>,...}}}}
#    format 1（旧）：{"<slug>":"<agentId>",...} 仍可读。
#    解析：优先用本 box 上存在的 id；都没有再按 index.json 名字匹配。多账号并存时不要把 map 压回单 id。
MAP=bots/agent-map.json
if [[ -f "$MAP" ]]; then
  MAP_FMT=$(jq -r '.format // 1' "$MAP")
  if [[ "$MAP_FMT" == "2" ]]; then
    SLUGS=$(jq -r '.bots | keys[]' "$MAP")
  else
    SLUGS=$(jq -r 'keys[]' "$MAP")
  fi
  for slug in $SLUGS; do
    id=""
    if [[ "$MAP_FMT" == "2" ]]; then
      # 在本 bot 的 ids 里找第一个本 box 存在的目录
      while IFS= read -r cand; do
        [[ -z "$cand" || "$cand" == "null" ]] && continue
        if [[ -d "$AGENTS/$cand" ]]; then id="$cand"; break; fi
      done < <(jq -r --arg s "$slug" '.bots[$s].ids // {} | .[]' "$MAP")
    else
      id=$(jq -r --arg s "$slug" '.[$s] // empty' "$MAP")
    fi
    src="${id:+$AGENTS/$id}"; dst="bots/$slug/raw"
    if [[ -z "$id" || ! -d "$src" ]]; then
      # 映射 id 不在本 box（他号专有 bot，或尚未写入本号 id）：按名字找
      nm=$(jq -r --arg s "$slug" '.bots[]? | select(.slug==$s) | .name' bots/index.json 2>/dev/null)
      alt=""
      if [[ -n "$nm" ]]; then
        for pj in "$AGENTS"/*/profile.json; do
          [[ "$(jq -r '.name // empty' "$pj" 2>/dev/null)" == "$nm" ]] && { [[ -z "$alt" ]] && alt=$(dirname "$pj") || alt="MULTI"; }
        done
      fi
      if [[ -n "$alt" && "$alt" != "MULTI" ]]; then
        echo "   $slug：本 box 无映射 id，按名字「$nm」用 $(basename "$alt")"
        src="$alt"
      else
        note=$(jq -r --arg s "$slug" 'if .format==2 then (.bots[$s].note // empty) else empty end' "$MAP" 2>/dev/null)
        echo "   跳过 $slug（本 box 无此 bot${note:+；$note}）"
        continue
      fi
    fi
    mkdir -p "$dst"
    for f in profile.json settings.json; do
      [[ -f "$src/$f" ]] && jq 'del(.serverId)' "$src/$f" > "$dst/$f" 2>/dev/null
    done
    # 自定义头像（若有）
    for a in "$src"/avatar.{png,jpg,jpeg,webp,gif,svg}; do [[ -f "$a" ]] && cp "$a" "bots/$slug/"; done
    # bot 自己的记忆文件（memory/profile.md、memory/log/），原样备份（只要 .md，不要数据库/其他文件）
    # 财务管家：明文 memory 永不拷进 raw/；有内容则加密进 secrets/
    if [[ "$slug" == "财务管家" ]]; then
      echo "   跳过 $slug 的明文 memory/（改为加密备份，若有内容）"
      if [[ -d "$src/memory" ]] && [[ -n "$(find "$src/memory" -type f 2>/dev/null | head -1)" ]]; then
        if [[ -z "${GROKBOT_HOME_PASSPHRASE:-}" ]]; then
          echo "   !! GROKBOT_HOME_PASSPHRASE 未设置，无法加密 财务管家 memory，跳过"
        else
          _mtmp=$(mktemp /tmp/cw-mem.XXXXXX.tgz)
          tar -C "$src" -czf "$_mtmp" memory
          if [[ -s "$_mtmp" ]]; then
            python3 scripts/secret-crypt.py enc-bin "$_mtmp" "secrets/财务管家-memory.tgz.enc" \
              && echo "   已更新 secrets/财务管家-memory.tgz.enc" \
              || echo "   !! 加密 财务管家 memory 失败"
          fi
          shred -u "$_mtmp" 2>/dev/null || rm -f "$_mtmp"
        fi
      else
        echo "   财务管家 memory 为空或不存在，跳过加密包"
      fi
    elif [[ -d "$src/memory" ]]; then
      mkdir -p "$dst/memory"
      (cd "$src/memory" && find . -type f -name '*.md' -print0) | while IFS= read -r -d '' m; do
        mkdir -p "$dst/memory/$(dirname "$m")"; cp "$src/memory/$m" "$dst/memory/$m"
      done
    fi
  done
else
  echo "   没有 $MAP，跳过原始设定快照"
fi

# 1b) 加密包：box-secrets / daily / feishu-cli / finance（见 scripts/pack-bundles.sh）
#     只在设置了 GROKBOT_HOME_PASSPHRASE 时打包；内容没变不会重新加密。明文只在 /tmp，结束后 shred。
bash scripts/pack-bundles.sh || { echo "!! 加密包更新失败，中止"; exit 6; }

# 1c) 明文（无密钥）的 box 文件：服务脚本、连接器启动器、assistant 笔记、小项目
copy_if() { [[ -f "$1" ]] && { mkdir -p "$(dirname "$2")"; cmp -s "$1" "$2" || cp "$1" "$2"; }; }
for f in listener.py run_loop.sh start.sh stop.sh; do copy_if "/workspace/gmail-listener/$f" "services/gmail-listener/$f"; done
for c in composio-pg composio-zhimeng; do for f in launch.py launch.sh; do copy_if "/workspace/$c/$f" "connectors/$c/$f"; done; done
if [[ -d /workspace/assistant ]]; then
  for f in README.md big-picture.md routines.md; do copy_if "/workspace/assistant/$f" "workspace/assistant/$f"; done
  if [[ -d /workspace/assistant/ideas ]]; then
    rm -rf workspace/assistant/ideas; mkdir -p workspace/assistant; cp -r /workspace/assistant/ideas workspace/assistant/ideas
  fi
fi
# daily/ 只以 secrets/daily.tgz.enc 形式备份（明文由 .gitignore 和 secret-scan 拦截）
if [[ -d /workspace/brake-game ]]; then
  mkdir -p projects/brake-game
  (cd /workspace/brake-game && find . -type f -print0) | while IFS= read -r -d '' f; do copy_if "/workspace/brake-game/$f" "projects/brake-game/$f"; done
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
echo "!! git push 失败：本地已 commit，请按 scripts/sync.md 用 Composio GitHub（composio-pg）推送"; exit 5
