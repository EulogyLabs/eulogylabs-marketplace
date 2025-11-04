import os, sys, json
from pathlib import Path
import requests
from requests.auth import HTTPBasicAuth

# Optional .env support
try:
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

title = os.getenv("WP_PAGE_TITLE", "Repo Test Page")
content_path = os.getenv("WP_CONTENT_FILE")
if content_path and Path(content_path).exists():
    content = Path(content_path).read_text(encoding="utf-8")
else:
    content = "<h1>Hello from EulogyLabs</h1><p>Deployed via repo sync.</p>"

payload = {"title": title, "content": content, "status": "draft"}  # or "publish"

api = f"{WP_BASE_URL}/wp-json/wp/v2/pages"
auth = HTTPBasicAuth(WP_USERNAME, WP_APP_PASSWORD)

# --- Important: set WAF-friendly headers & session ---
session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0 Safari/537.36 EulogyLabsPublisher/1.0",
    "Accept": "application/json",
    "Content-Type": "application/json",
})

try:
    resp = session.post(api, auth=auth, json=payload, timeout=30)
    if resp.status_code == 406:
        # Fallback: tweak headers again in case ModSecurity is picky
        session.headers.update({
            "X-Requested-With": "XMLHttpRequest",
        })
        resp = session.post(api, auth=auth, json=payload, timeout=30)

    resp.raise_for_status()
    print(json.dumps(resp.json(), indent=2))
except requests.HTTPError as e:
    print("ERROR:", resp.status_code, resp.text[:4000])
    raise
