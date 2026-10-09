import os
from composio import Composio
key = open("/home/box/.composio_pg_key").read().strip()
# Dedicated Composio user for zhimeng63@gmail.com; Gmail only.
s = Composio(api_key=key).create(
    user_id="zhimeng63",
    toolkits=["gmail"],
    auth_configs={"gmail": "ac_OusYuVoTaQMY"},
)
os.execvp("npx", ["npx", "-y", "mcp-remote", s.mcp.url, "--transport", "http-only", "--header", "x-api-key:" + key])
