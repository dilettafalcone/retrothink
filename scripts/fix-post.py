"""
fix-post.py
Corregge il frontmatter e rimuove gli escape markdown superflui
da un file .md generato con caratteri escaped.
Uso: python scripts/fix-post.py posts/nomefile.md
"""

import re
import sys
from pathlib import Path

SPECIAL_CHARS = r'\\([\\*_{}\[\]()#+\-.!>|~`])'

def fix_frontmatter(text):
    # Correggi \--- -> ---
    text = re.sub(r'^\\---', '---', text, flags=re.MULTILINE)
    # Rimuovi righe vuote all'interno del frontmatter
    def compact(m):
        inner = re.sub(r'\n{2,}', '\n', m.group(1))
        return '---\n' + inner + '\n---'
    text = re.sub(r'^---\n([\s\S]*?)\n---', compact, text, count=1, flags=re.MULTILINE)
    # Correggi \[ nei tags
    text = re.sub(r'^(tags:\s*)\\(\[)', lambda m: m.group(1) + m.group(2), text, flags=re.MULTILINE)
    return text

def unescape_body(text):
    """Rimuove backslash-escape fuori dai blocchi di codice."""
    # Dividi su fenced code blocks (```...```) e inline code (`...`)
    fence_re = re.compile(r'(```[\s\S]*?```|`[^`\n]+`)', re.DOTALL)
    parts = fence_re.split(text)
    result = []
    for i, part in enumerate(parts):
        if i % 2 == 1:
            result.append(part)  # codice: non toccare
        else:
            result.append(re.sub(SPECIAL_CHARS, r'\1', part))
    return ''.join(result)

def main():
    if len(sys.argv) < 2:
        print("Uso: python scripts/fix-post.py posts/nomefile.md")
        sys.exit(1)

    filepath = Path(sys.argv[1])
    if not filepath.exists():
        print(f"File non trovato: {filepath}")
        sys.exit(1)

    text = filepath.read_text(encoding='utf-8')
    text = fix_frontmatter(text)

    # Separa frontmatter dal corpo
    fm_match = re.match(r'^(---\n[\s\S]*?\n---\n?)', text)
    if fm_match:
        frontmatter = fm_match.group(1)
        body = text[len(frontmatter):]
        body = unescape_body(body)
        text = frontmatter + body
    else:
        text = unescape_body(text)

    filepath.write_text(text, encoding='utf-8')
    print(f"OK  {filepath} corretto.")

if __name__ == '__main__':
    main()
