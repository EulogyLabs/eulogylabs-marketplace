import os, sys, json
from pathlib import Path

try:
    # Optional dependency; only used if .env exists
    from dotenv import load_dotenv  # type: ignore
    if Path(".env").exists():
        load_dotenv(".env")
except Exception:
    pass

WP_BASE_URL = os.getenv("WP_BASE_URL", "").rstrip("/")
WP_USERNAME = os.getenv("WP_USERNAME")
WP_APP_PASSWORD = os.getenv("WP_APP_PASSWORD")

if not WP_BASE_URL or not WP_USERNAME or not WP_APP_PASSWORD:
    sys.exit("Missing WP creds. Create .env from .env.example and set WP_* values.")

# Inputs (env overrides are handy for CI)
title = os.getenv("WP_PAGE_TITLE", "Repo Test Page")
content_path = os.getenv("WP_CONTENT_FILE")

if content_path and Path(content_path).exists():
    content = Path(content_path).read_text(encoding="utf-8")
else:
    content = "<h1>Hello from EulogyLabs</h1><p>Deployed via repo sync.</p>"

payload = {"title": title, "content": content, "status": "draft"}  # change to "publish" if desired

import requests
from requests.auth import HTTPBasicAuth
api = f"{WP_BASE_URL}/wp-json/wp/v2/pages"
resp = requests.post(api, auth=HTTPBasicAuth(WP_USERNAME, WP_APP_PASSWORD), json=payload, timeout=30)

try:
    resp.raise_for_status()
except Exception:
    print("ERROR:", resp.status_code, resp.text[:4000])
    raise

print(json.dumps(resp.json(), indent=2))
