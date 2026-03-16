# Come aggiungere un nuovo post

I post sono file Markdown nella cartella `posts/`.

---

## Passi

### 1. Prima installazione (una volta sola)

Se usi Node.js:
```bash
npm install
```

Se usi Python (già disponibile su questo PC):
```bash
pip install markdown
```

### 2. Crea il file `.md`

Crea un nuovo file in `posts/`. Il nome del file diventa l'URL del post.
Usa solo lettere minuscole e trattini:

```
posts/thinkpad-x220.md   →   retrothink.click/thinkpad-x220/
```

### 3. Aggiungi il frontmatter

Ogni file inizia con un blocco tra `---`:

```markdown
---
title: Titolo del post
date: 2024-06-01
tags: [thinkpad, linux]
description: Breve descrizione che appare nei risultati di ricerca (1-2 righe).
---

Qui inizia il testo del post in Markdown.

## Sezione

Puoi usare **grassetto**, *corsivo*, `codice`, [link](https://esempio.com),
elenchi puntati, blocchi di codice, tabelle — tutto il Markdown standard.

```bash
# Esempio di blocco di codice
pacman -S vim
```
```

#### Campi del frontmatter

| Campo | Obbligatorio | Note |
|-------|-------------|------|
| `title` | Sì | Titolo del post |
| `date` | Sì | Formato `YYYY-MM-DD` |
| `tags` | Consigliato | Array: `[arch, linux]` oppure singolo: `arch` |
| `description` | Consigliato | Usato nel meta description e nei social |

I tag disponibili (con icona Font Awesome) sono:
`arch`, `linux`, `mobile`, `pdf`, `server`, `software`, `sync`,
`thinkpad`, `retro`, `terminal`, `typing`, `fountainpen`, `markdown`, `writingtools`

Puoi usare tag liberi — appariranno senza icona.

### 4. Genera le pagine HTML e aggiorna l'indice

```bash
python scripts/update-posts.py
```

oppure, se hai Node.js:

```bash
node scripts/update-posts.js
# oppure: npm run build
```

Lo script fa tutto in automatico:
- Genera `<slug>/index.html` per ogni nuovo post
- Aggiorna la lista articoli in `index.html`
- Aggiorna il tag cloud in `index.html`

### 5. Pubblica

Fai commit e push su GitHub.

---

## Esempio completo

**`posts/thinkpad-x220.md`**

```markdown
---
title: ThinkPad X220: il laptop perfetto per Linux
date: 2024-06-01
tags: [thinkpad, linux]
description: Perché il ThinkPad X220 rimane una delle scelte migliori per chi usa Linux nel 2024.
---

Il ThinkPad X220 è uscito nel 2011, eppure continua a essere uno dei laptop
più apprezzati dalla comunità Linux.

## Compatibilità hardware

Tutto funziona out-of-the-box su qualsiasi distribuzione moderna:
Wi-Fi, Bluetooth, sospensione, gestione batteria.

## Perché ancora oggi

- Tastiera eccellente
- Riparabilità totale
- Prezzo contenuto sul mercato dell'usato
```

Dopo aver eseguito lo script, il post sarà accessibile all'indirizzo:

```
https://retrothink.click/thinkpad-x220/
```

---

## Struttura URL

| Tipo | URL |
|------|-----|
| Homepage | `retrothink.click/` |
| Nuovo post | `retrothink.click/<slug>/` |
| Tag | `retrothink.click/tags/<tag>/` |

---

## Articoli esistenti

I file `posts/*.md` con `existing: true` nel frontmatter sono gli articoli
originali generati da Hugo. Lo script li include nell'indice ma non sovrascrive
il loro HTML (già presente nella rispettiva cartella).
