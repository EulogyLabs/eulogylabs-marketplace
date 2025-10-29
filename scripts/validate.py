import os, yaml, sys

def validate_product(folder):
    path = os.path.join(folder, "product.yml")
    with open(path, "r") as f:
        data = yaml.safe_load(f)
    required = ["sku","title","description_md","canva_template_link","price_usd","thumbnail"]
    missing = [k for k in required if k not in data or data[k] in (None, "")]
    if missing:
        raise ValueError(f"{folder}: missing fields: {', '.join(missing)}")

def main():
    base = "products"
    for name in os.listdir(base):
        folder = os.path.join(base, name)
        if os.path.isdir(folder):
            try:
                validate_product(folder)
                print(f"OK: {name}")
            except Exception as e:
                print(f"ERROR: {name}: {e}")
                sys.exit(1)
    print("Validation complete.")

if __name__ == "__main__":
    main()
