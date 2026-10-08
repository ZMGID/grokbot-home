# secrets/

这里只放**加密后**的密钥，明文永远不进仓库（`.gitignore` 已拦截）。

- `COMPOSIO_API_KEY.enc`：用户贴给 bot 的 Composio 项目 API Key，用 `scripts/secret-crypt.py` 加密（scrypt N=2^20 + AES-256-CBC，文件头 `GBH1`）。
- `COMPOSIO_API_KEY.box-current.enc`：旧号 box 上 `~/.composio_pg_key` 里实际在用的 key（和上面那份不同）。BOOTSTRAP 先用 `.enc`，composio-pg 连不上再用这份。
- **仓库是公开的**：任何人都能下载这些 `.enc` 文件离线猜口令，所以口令要足够长（建议 4 个以上随机词或 16+ 位随机字符）。
- 解密需要用户的口令，放在环境变量 `GROKBOT_HOME_PASSPHRASE`（用 secret-request 向用户要，不要让用户贴在聊天里）：
  `python3 scripts/secret-crypt.py dec secrets/COMPOSIO_API_KEY.enc /home/box/.composio_pg_key`
  （口令错误时只报一行错误，不会写文件，也不会打印任何密钥材料。）
- 密钥轮换后：把新值写进 `~/.composio_pg_key`，再
  `python3 scripts/secret-crypt.py enc /home/box/.composio_pg_key secrets/COMPOSIO_API_KEY.enc`
  再 `bash scripts/secret-scan.sh`（会确认明文 key、两份 `.enc` 的明文和口令都没出现在仓库里，且 `secrets/*.enc` 都是 `GBH1` 加密格式）后提交推送。
- 换口令：先用旧口令把两份都解密到 `/tmp`（`umask 077`），换成新口令的环境变量后重新 `enc`，删掉 `/tmp` 里的明文。
