import csv, yaml
from pathlib import Path

OUT_DIR = Path('marketplaces/gumroad/dist'); OUT_DIR.mkdir(parents=True, exist_ok=True)
CSV_PATH = OUT_DIR / 'products.csv'

FIELDS = [
  'Name','Description','Price','Tags','External ID','Custom URL','Is Published'
]

rows = []
for prod in Path('products').iterdir():
    if not prod.is_dir(): continue
    yml = prod / 'product.yml'
    if not yml.exists(): continue
    data = yaml.safe_load(yml.read_text(encoding='utf-8')) or {}

    rows.append({
      'Name': data.get('title',''),
      'Description': data.get('description_md',''),
      'Price': data.get('price_usd',''),
      'Tags': ','.join(data.get('keywords', [])),
      'External ID': data.get('sku', prod.name),
      'Custom URL': data.get('slug', prod.name),
      'Is Published': 'false',
    })

with CSV_PATH.open('w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=FIELDS)
    w.writeheader()
    for r in rows: w.writerow(r)

print(f"Wrote {len(rows)} Gumroad rows to {CSV_PATH}")
