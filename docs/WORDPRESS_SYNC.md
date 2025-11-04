# WordPress Sync (Pages)

## 1) Create an Application Password
- WordPress Admin → Users → (zapier_webops) → Application Passwords → Add New → copy it once.

## 2) Local use
```bash
cp .env.example .env
# Fill WP_BASE_URL, WP_USERNAME, WP_APP_PASSWORD
python3 -m venv .venv && source .venv/bin/activate
pip install requests python-dotenv
# Optional: create an HTML file to post
echo "<h1>Repo Draft</h1><p>Posted from the repo.</p>" > docs/sample_page.html
WP_CONTENT_FILE=docs/sample_page.html WP_PAGE_TITLE="Repo Draft from CLI" \
python scripts/wordpress_sync/push_page.py

