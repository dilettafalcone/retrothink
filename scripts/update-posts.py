"""
update-posts.py

Scansiona posts/*.md, legge frontmatter, genera l'HTML per i nuovi post
e aggiorna la lista articoli e il tag cloud in index.html.

Uso:
    python scripts/update-posts.py

Dipendenze:
    pip install markdown
"""

import os
import re
import sys
import json
from pathlib import Path

try:
    import markdown as md_lib
except ImportError:
    sys.exit("Installa il modulo markdown:  pip install markdown")

ROOT     = Path(__file__).parent.parent
SITE_URL = "https://retrothink.click"


# ── Frontmatter parser ─────────────────────────────────────────────────────

def parse_frontmatter(filepath):
    text  = Path(filepath).read_text(encoding="utf-8")
    match = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n?(.*)", text, re.DOTALL)
    if not match:
        return {}, text

    meta = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        key = key.strip()
        val = val.strip().strip("\"'")
        # array: [arch, linux]
        if val.startswith("[") and val.endswith("]"):
            val = [t.strip().strip("\"'") for t in val[1:-1].split(",") if t.strip()]
        meta[key] = val

    return meta, match.group(2).strip()


# ── Helpers ────────────────────────────────────────────────────────────────

def to_list(val):
    if not val:
        return []
    return val if isinstance(val, list) else [val]

def capitalize(s):
    return s[0].upper() + s[1:] if s else s


# ── HTML template per un nuovo post ────────────────────────────────────────

def generate_post_html(meta, html_content, all_posts):
    slug        = meta["slug"]
    title       = meta.get("title", "")
    description = meta.get("description", "").replace('"', "&quot;")
    tags        = to_list(meta.get("tags"))

    # Prev/next
    idx      = next((i for i, p in enumerate(all_posts) if p["meta"]["slug"] == slug), -1)
    prev_next = ""
    if idx > 0:
        newer      = all_posts[idx - 1]
        prev_next += f'<a href="/{newer["meta"]["slug"]}/"><div id="nextart">Prossimo:<br>{newer["meta"]["title"]}</div></a>'
    if idx < len(all_posts) - 1:
        older      = all_posts[idx + 1]
        prev_next += f'<a href="/{older["meta"]["slug"]}/"><div id="prevart">Precedente:<br>{older["meta"]["title"]}</div></a>'

    tag_links = " ".join(
        f'<a id="tag_{t}" href="{SITE_URL}/tags/{t}">{capitalize(t)}</a>' for t in tags
    )
    tag_list_html  = f'\n<div style="clear:both" class="taglist">Tag correlati<br>{tag_links}</div>' if tags else ""
    prev_next_html = f'\n<div id="nextprev">{prev_next}</div>' if prev_next else ""

    return f"""<!DOCTYPE html>
<html lang="it">
<head>
\t<meta charset="utf-8">
\t<meta name="viewport" content="width=device-width, initial-scale=1">
\t<title>{title} | Retro Think</title>
\t<meta name="description" content="{description}">
\t<meta name="keywords" content="{', '.join(tags)}">
\t<meta name="robots" content="index, follow">
\t<link rel="canonical" href="{SITE_URL}/{slug}/">
\t<link rel='alternate' type='application/rss+xml' title="Retro Think RSS" href='/index.xml'>
\t<link rel="icon" href="/favicon.ico">
\t<meta property="og:type" content="article">
\t<meta property="og:url" content="{SITE_URL}/{slug}/">
\t<meta property="og:title" content="{title}">
\t<meta property="og:description" content="{description}">
\t<link rel='stylesheet' type='text/css' href='/style.css'>
\t<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css" crossorigin="anonymous" referrerpolicy="no-referrer" />
\t<link rel="preconnect" href="https://fonts.googleapis.com">
\t<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
\t<link href="https://fonts.googleapis.com/css2?family=Source+Serif+4:ital,opsz,wght@0,8..60,300..900;1,8..60,300..900&display=swap" rel="stylesheet">
</head>
<body>

<nav class="site-nav">
\t<div class="nav-inner">
\t\t<a href="/" class="nav-brand">Retro Think</a>
\t\t<a href="/index.xml" class="nav-rss" title="Feed RSS">
\t\t\t<img src="/rss.svg" alt="RSS">
\t\t</a>
\t</div>
</nav>

<main>
<a href="/" class="back-link">&#8592; tutti gli articoli</a>

<h1>{title}</h1>
<div class="article-meta">
  <span>{meta.get("date", "")}</span>{(" &middot; " + tag_links) if tags else ""}
</div>

<article>
{html_content}{prev_next_html}
</article>
</main>

<footer>
\t<a href="/" class="footer-brand">retrothink.click</a>
\t<div class="footer-icons">
\t\t<a href="/index.xml" title="Iscriviti via RSS">
\t\t\t<img src="/rss.svg" alt="RSS Feed">
\t\t</a>
\t\t<a href="https://www.youtube.com/@Retro_Think" title="Visita il mio canale YouTube">
\t\t\t<img src="/youtube.png" alt="YouTube Channel">
\t\t</a>
\t</div>
</footer>

<script src="https://unpkg.com/feather-icons" defer></script>
<script defer>
  document.addEventListener("DOMContentLoaded", () => feather.replace());
</script>
</body>
</html>
"""


# ── Aggiorna index.html ────────────────────────────────────────────────────

def rebuild_index_html(all_posts):
    index_path = ROOT / "index.html"
    content    = index_path.read_text(encoding="utf-8")

    # Artlist
    items = "".join(
        (lambda m, tags, first_tag: (
            f'<li data-tags="[{", ".join(tags)}]">\n'
            f'    <a href="{SITE_URL}/{m["slug"]}/">\n'
            f'      <span class="art-date">{m["date"]}</span>\n'
            f'      <span class="art-title">{m["title"]}</span>\n'
            + (f'      <span class="art-tag">{first_tag}</span>\n' if first_tag else '')
            + f'    </a>\n  </li>'
        ))(p["meta"], to_list(p["meta"].get("tags")), to_list(p["meta"].get("tags"))[0] if to_list(p["meta"].get("tags")) else "")
        for p in all_posts
    )
    content = re.sub(
        r'<ul id="artlist">[\s\S]*?</ul>',
        f'<ul id="artlist">{items}</ul>',
        content,
    )

    # Tagcloud
    all_tags = sorted(set(t for p in all_posts for t in to_list(p["meta"].get("tags"))))
    tag_items = "\n".join(
        f'    <li><a href="{SITE_URL}/tags/{t}" id="tag_{t}">{capitalize(t)}</a></li>'
        for t in all_tags
    )
    content = re.sub(
        r'<ul id="tagcloud">[\s\S]*?</ul>',
        f'<ul id="tagcloud">\n{tag_items}\n    </ul>',
        content,
    )

    index_path.write_text(content, encoding="utf-8")
    print("OK index.html aggiornato")


# ── Main ───────────────────────────────────────────────────────────────────

def main():
    posts_dir = ROOT / "posts"
    if not posts_dir.exists():
        sys.exit("Cartella posts/ non trovata.")

    files = sorted(posts_dir.glob("*.md"))
    if not files:
        print("Nessun post trovato in posts/")
        return

    all_posts = []
    for f in files:
        meta, body = parse_frontmatter(f)
        if "slug" not in meta:
            meta["slug"] = f.stem
        if "date" not in meta:
            meta["date"] = "1970-01-01"
        all_posts.append({"meta": meta, "body": body})

    # Ordine: più recente prima
    all_posts.sort(key=lambda p: p["meta"]["date"], reverse=True)

    print(f"\nTrovati {len(all_posts)} post.\n")

    md = md_lib.Markdown(extensions=["tables", "fenced_code", "codehilite"])

    for post in all_posts:
        meta      = post["meta"]
        is_existing = str(meta.get("existing", "false")).lower() == "true"
        if is_existing:
            print(f"~  {meta['slug']}  (esistente, skip HTML)")
            continue

        md.reset()
        html_content = md.convert(post["body"])
        html         = generate_post_html(meta, html_content, all_posts)

        out_dir = ROOT / meta["slug"]
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "index.html").write_text(html, encoding="utf-8")
        print(f"✓  {meta['slug']}/index.html")

    rebuild_index_html(all_posts)
    print("\nFatto. Puoi fare commit e push.")


if __name__ == "__main__":
    main()
