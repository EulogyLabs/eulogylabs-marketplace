# Eulogy Labs – Marketplace Monorepo
**Where Your Light Lives On.**

This repository houses product source files, marketplace listings (Gumroad & Etsy),
and website-ready assets for Eulogy Labs.

## Contents
- `products/` — One folder per SKU with metadata, instructions, and asset pointers
- `marketplaces/` — Listing data (JSON/YAML) and export artifacts
- `assets/` — Centralized brand kit, thumbnails, banners
- `website/` — HTML/MD snippets for product cards and landing pages
- `scripts/` — Utilities to build listings from product metadata
- `.github/workflows/` — CI to validate metadata and produce exports

## SKU scheme
`EL-<NNN>-<short-name>` (e.g., `EL-001-printable-8.5x11`)

## How to work
1. Create or update `products/EL-XXX.../product.yml`.
2. Run `python3 scripts/build_listings.py` to generate Gumroad/Etsy payloads and website snippets.
3. Commit and push. CI validates and publishes artifacts to `marketplaces/*/dist/`.
