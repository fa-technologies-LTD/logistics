#!/usr/bin/env python3
"""
Generate per-product link-preview pages under /p/<PROD-ID>/index.html.

WhatsApp/Facebook/iMessage crawlers do NOT run JavaScript, so a static SPA
can only show per-product previews via a real pre-built page per product.
Each generated page carries that product's Open Graph tags, then instantly
forwards real visitors to /?product=<ID> (the normal in-app product view).

Re-run whenever products.json changes:  python3 scripts/gen-og-pages.py
"""
import json, os, re, shutil, html
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PRODUCTS = ROOT / "products.json"
OUT = ROOT / "p"
SITE = "https://gifting.fastaccs.com"

def og_image(img_url: str) -> str:
    """Render a 1200x630 preview via the weserv proxy (whole product on a warm bg)."""
    if not img_url:
        return f"{SITE}/assets/og-image.png"
    bare = re.sub(r"^https?://", "", img_url.strip())
    return ("https://images.weserv.nl/?url=" + bare +
            "&w=1200&h=630&fit=contain&bg=FCFAF6&output=jpg&q=82")

def clean(text: str, limit: int) -> str:
    text = re.sub(r"\s+", " ", (text or "").strip())
    if len(text) > limit:
        text = text[:limit].rsplit(" ", 1)[0] + "…"
    return text

def main():
    data = json.loads(PRODUCTS.read_text())
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)

    count = 0
    for row in data:
        pid = (row[0] or "").strip()
        if not pid:
            continue
        name = clean(row[1] if len(row) > 1 else "", 90) or "Gift"
        desc = clean(row[2] if len(row) > 2 else "", 150)
        price = (row[3] if len(row) > 3 else "").strip()
        img = (row[5] if len(row) > 5 else "").strip()

        price_part = price if price else "Price on request"
        description = f"{price_part} · {desc}".strip(" ·") if desc else price_part
        ogimg = og_image(img)

        # escape for HTML attribute context
        n = html.escape(name, quote=True)
        d = html.escape(description, quote=True)
        target = f"/?product={pid}"

        page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{n} — FA Logistics</title>
<meta name="description" content="{d}">
<meta property="og:type" content="product">
<meta property="og:site_name" content="FA Logistics">
<meta property="og:title" content="{n}">
<meta property="og:description" content="{d}">
<meta property="og:image" content="{ogimg}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:url" content="{SITE}/p/{pid}/">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{n}">
<meta name="twitter:description" content="{d}">
<meta name="twitter:image" content="{ogimg}">
<link rel="canonical" href="{SITE}{target}">
<meta http-equiv="refresh" content="0; url={target}">
<script>location.replace({json.dumps(target)});</script>
</head>
<body style="font-family:system-ui,sans-serif;background:#FCFAF6;color:#211B14;text-align:center;padding:40px">
<p>Taking you to <a href="{target}">{n}</a>…</p>
</body>
</html>
"""
        d_out = OUT / pid
        d_out.mkdir(parents=True, exist_ok=True)
        (d_out / "index.html").write_text(page)
        count += 1

    print(f"generated {count} product preview pages in {OUT}")

if __name__ == "__main__":
    main()
