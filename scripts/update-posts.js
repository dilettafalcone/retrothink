/**
 * update-posts.js
 *
 * Scansiona posts/*.md, legge frontmatter, genera l'HTML per i nuovi post
 * e aggiorna la lista articoli e il tag cloud in index.html.
 *
 * Uso:
 *   node scripts/update-posts.js
 */

const fs   = require('fs');
const path = require('path');
const { marked } = require('marked');

const root     = path.join(__dirname, '..');
const SITE_URL = 'https://retrothink.click';

// ── Frontmatter parser ─────────────────────────────────────────────────────

function parseFrontmatter(filepath) {
  const text  = fs.readFileSync(filepath, 'utf8');
  const match = text.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n?([\s\S]*)$/m);
  if (!match) return { meta: {}, body: text };

  const meta = {};
  match[1].split('\n').forEach(line => {
    const i = line.indexOf(':');
    if (i === -1) return;
    const key = line.slice(0, i).trim();
    let val   = line.slice(i + 1).trim().replace(/^["']|["']$/g, '');
    // array: [arch, linux] o ["arch", "linux"]
    if (val.startsWith('[') && val.endsWith(']')) {
      val = val.slice(1, -1)
               .split(',')
               .map(t => t.trim().replace(/^["']|["']$/g, ''))
               .filter(Boolean);
    }
    meta[key] = val;
  });

  return { meta, body: (match[2] || '').trim() };
}

// ── Helpers ────────────────────────────────────────────────────────────────

function capitalize(s) {
  return s.charAt(0).toUpperCase() + s.slice(1);
}

function toArray(val) {
  if (!val) return [];
  return Array.isArray(val) ? val : [val];
}

// ── HTML template per un nuovo post ────────────────────────────────────────

function generatePostHtml(meta, htmlContent, allPosts) {
  const slug        = meta.slug;
  const title       = meta.title || '';
  const description = (meta.description || '').replace(/"/g, '&quot;');
  const tags        = toArray(meta.tags);

  // Prev/next (array ordinato: [0] = più recente)
  const idx  = allPosts.findIndex(p => p.meta.slug === slug);
  let prevNext = '';
  if (idx > 0) {
    const newer = allPosts[idx - 1];
    prevNext += `<a href="/${newer.meta.slug}/"><div id="nextart">Prossimo:<br>${newer.meta.title}</div></a>`;
  }
  if (idx < allPosts.length - 1) {
    const older = allPosts[idx + 1];
    prevNext += `<a href="/${older.meta.slug}/"><div id="prevart">Precedente:<br>${older.meta.title}</div></a>`;
  }

  const tagLinks = tags.map(t =>
    `<a id="tag_${t}" href="${SITE_URL}/tags/${t}">${capitalize(t)}</a>`
  ).join(' ');

  const tagListHtml  = tags.length ? `\n<div style="clear:both" class="taglist">Tag correlati<br>${tagLinks}</div>` : '';
  const prevNextHtml = prevNext    ? `\n<div id="nextprev">${prevNext}</div>` : '';

  return `<!DOCTYPE html>
<html lang="it">
<head>
\t<meta charset="utf-8">
\t<meta name="viewport" content="width=device-width, initial-scale=1">
\t<title>${title} | Retro Think</title>
\t<meta name="description" content="${description}">
\t<meta name="keywords" content="${tags.join(', ')}">
\t<meta name="robots" content="index, follow">
\t<link rel="canonical" href="${SITE_URL}/${slug}/">
\t<link rel='alternate' type='application/rss+xml' title="Retro Think RSS" href='/index.xml'>
\t<link rel="icon" href="/favicon.ico">
\t<meta property="og:type" content="article">
\t<meta property="og:url" content="${SITE_URL}/${slug}/">
\t<meta property="og:title" content="${title}">
\t<meta property="og:description" content="${description}">
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
<article>

<a href="/" class="back-link">&#8592; tutti gli articoli</a>

<h1>${title}</h1>
<div class="article-meta">
  <span>${date}</span>${tags.length ? ' · ' + tagLinks : ''}
</div>

<article>
${htmlContent}${prevNextHtml}
</article>
</article>
</main>

<footer>
\t<a href="${SITE_URL}/" class="footer-brand">retrothink.click</a>
\t<div class="footer-icons">
\t\t<a href="/index.xml" title="Iscriviti via RSS">
\t\t\t<img src="/rss.svg" alt="RSS Feed">
\t\t</a>
\t\t<a href="https://www.youtube.com/@Retro_Think" title="Visita il canale YouTube">
\t\t\t<img src="/youtube.png" alt="YouTube">
\t\t</a>
\t</div>
</footer>

<script src="https://unpkg.com/feather-icons" defer></script>
<script defer>
  document.addEventListener("DOMContentLoaded", () => feather.replace());
</script>
</body>
</html>
`;
}

// ── Aggiorna index.html ────────────────────────────────────────────────────

function rebuildIndexHtml(allPosts) {
  const indexPath = path.join(root, 'index.html');
  let content = fs.readFileSync(indexPath, 'utf8');

  // Artlist
  const artlistItems = allPosts.map(({ meta }) => {
    const tags    = toArray(meta.tags);
    const tagsStr = '[' + tags.join(', ') + ']';
    const firstTag = tags[0] || '';
    return `<li data-tags="${tagsStr}">\n    <a href="${SITE_URL}/${meta.slug}/">\n      <span class="art-date">${meta.date}</span>\n      <span class="art-title">${meta.title}</span>\n      ${firstTag ? `<span class="art-tag">${firstTag}</span>` : ''}\n    </a>\n  </li>`;
  }).join('');

  content = content.replace(
    /<ul id="artlist">[\s\S]*?<\/ul>/,
    `<ul id="artlist">${artlistItems}</ul>`
  );

  // Tagcloud
  const allTags = [...new Set(allPosts.flatMap(({ meta }) => toArray(meta.tags)))].sort();
  const tagcloudItems = allTags.map(t =>
    `    <li><a href="${SITE_URL}/tags/${t}" id="tag_${t}">${capitalize(t)}</a></li>`
  ).join('\n');

  content = content.replace(
    /<ul id="tagcloud">[\s\S]*?<\/ul>/,
    `<ul id="tagcloud">\n${tagcloudItems}\n    </ul>`
  );

  fs.writeFileSync(indexPath, content, 'utf8');
  console.log('✓  index.html aggiornato');
}

// ── Main ───────────────────────────────────────────────────────────────────

function main() {
  const postsDir = path.join(root, 'posts');

  if (!fs.existsSync(postsDir)) {
    console.error('Cartella posts/ non trovata.');
    process.exit(1);
  }

  const files = fs.readdirSync(postsDir).filter(f => f.endsWith('.md'));
  if (files.length === 0) {
    console.log('Nessun post trovato in posts/');
    return;
  }

  // Leggi e ordina tutti i post (più recente prima)
  const allPosts = files
    .map(f => {
      const { meta, body } = parseFrontmatter(path.join(postsDir, f));
      if (!meta.slug) meta.slug = f.replace('.md', '');
      if (!meta.date) meta.date = '1970-01-01';
      return { meta, body };
    })
    .sort((a, b) => (a.meta.date < b.meta.date ? 1 : -1));

  console.log(`\nTrovati ${allPosts.length} post.\n`);

  // Genera HTML per i post nuovi (non `existing: true`)
  for (const post of allPosts) {
    const isExisting = post.meta.existing === 'true' || post.meta.existing === true;
    if (isExisting) {
      console.log(`⟳  ${post.meta.slug}  (esistente, skip HTML)`);
      continue;
    }

    const htmlContent = marked(post.body);
    const html        = generatePostHtml(post.meta, htmlContent, allPosts);
    const dir         = path.join(root, post.meta.slug);

    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
    fs.writeFileSync(path.join(dir, 'index.html'), html, 'utf8');
    console.log(`✓  ${post.meta.slug}/index.html`);
  }

  // Aggiorna index.html
  rebuildIndexHtml(allPosts);

  console.log('\nFatto. Puoi fare commit e push.');
}

main();
