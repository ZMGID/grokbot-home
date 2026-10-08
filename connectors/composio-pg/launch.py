import os, sys
from composio import Composio
key = open("/home/box/.composio_pg_key").read().strip()
s = Composio(api_key=key).create(user_id="pg-test-5be86c3e-d220-4538-ab6d-ae22d538dfde")
os.execvp("npx", ["npx", "-y", "mcp-remote", s.mcp.url, "--transport", "http-only", "--header", "x-api-key:" + key])
