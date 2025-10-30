import os
import json
import yaml
import pathlib

OUT_DIR = pathlib.Path("marketplaces/etsy/dist")
OUT_DIR.mkdir(parents=True, exist_ok=True)

for prod_dir in pathlib.Path("products").iterdir():
    if not prod_dir.is_dir():
        continue

    yml = prod_dir / "product.yml"
    if not yml.exists():
        continue

    with open(yml, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    sku = data.get("sku", prod_dir.name)
    etsy_payload = {
        "title": data.get("title", ""),
        "description": data.get("description_md", ""),
        "price": data.get("price_usd", ""),
        "who_made": "i_did",
        "is_supply": False,
        "when_made": "made_to_order",
        "tags": data.get("keywords", []),
    }

    output_file = OUT_DIR / f"{sku}.etsy.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(etsy_payload, f, ensure_ascii=False, indent=2)

    print(f"✅ Wrote {output_file}")

print("🎉 Etsy listings JSON generation complete!")
