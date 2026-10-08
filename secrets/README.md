# secrets/

这里只放**加密后**的密钥，明文永远不进仓库（`.gitignore` 已拦截）。

- `COMPOSIO_API_KEY.enc`：Composio 项目 API Key，用 `scripts/secret-crypt.py` 加密（scrypt + AES-256）。
- 解密需要用户的口令，放在环境变量 `GROKBOT_HOME_PASSPHRASE`（用 secret-request 向用户要，不要让用户贴在聊天里）：
  `python3 scripts/secret-crypt.py dec secrets/COMPOSIO_API_KEY.enc /home/box/.composio_pg_key`
- 密钥轮换后：把新值写进 `~/.composio_pg_key`，再
  `python3 scripts/secret-crypt.py enc /home/box/.composio_pg_key secrets/COMPOSIO_API_KEY.enc`
