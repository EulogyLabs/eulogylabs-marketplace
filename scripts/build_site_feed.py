import json, yaml
from pathlib import Path

OUT_DIR = Path('marketplaces/site/dist'); OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_PATH = OUT_DIR / 'products.json'

items = []
for prod in Path('products').iterdir():
    if not prod.is_dir(): continue
    yml = prod / 'product.yml'
    if not yml.exists(): continue
    data = yaml.safe_load(yml.read_text(encoding='utf-8')) or {}

    slug = data.get('slug', prod.name)
    items.append({
        'sku': data.get('sku', prod.name),
        'slug': slug,
        'title': data.get('title',''),
        'description_md': data.get('description_md',''),
        'price_usd': data.get('price_usd',''),
        'keywords': data.get('keywords', []),
        'assets': {
            'thumbnail': f'products/{slug}/assets/thumbnail.png',
            'banner':    f'products/{slug}/assets/banner.png',
        }
    })

OUT_PATH.write_text(json.dumps({'products': items}, ensure_ascii=False, indent=2), encoding='utf-8')
print(f"Wrote site feed with {len(items)} products to {OUT_PATH}")
