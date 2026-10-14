#!/usr/bin/env bash
# 用法: unpack.sh <文件.zip|.rar|.pdf> <输出目录>
# 依赖: unzip, unrar-free (RAR5 用 7z 会失败), poppler-utils (pdftoppm)
set -euo pipefail
IN="$1"; OUT="${2:-./imgs}"; mkdir -p "$OUT"
case "${IN,,}" in
  *.zip) unzip -o -q -O UTF-8 "$IN" -d "$OUT" 2>/dev/null || unzip -o -q "$IN" -d "$OUT" ;;
  *.rar) (cd "$OUT" && unrar-free -x "$(realpath "$IN")" >/dev/null) || unrar x -o+ "$IN" "$OUT/" ;;
  *.pdf) pdftoppm -r 110 -png "$IN" "$OUT/page" ;;
  *) echo "不支持的格式: $IN" >&2; exit 1 ;;
esac
# 把子目录里的图片平铺出来
find "$OUT" -mindepth 2 -type f \( -iname '*.jpg' -o -iname '*.jpeg' -o -iname '*.png' -o -iname '*.webp' \) -exec mv -n {} "$OUT/" \;
echo "图片数: $(find "$OUT" -maxdepth 1 -type f \( -iname '*.jpg' -o -iname '*.jpeg' -o -iname '*.png' -o -iname '*.webp' \) | wc -l)  -> $OUT"
