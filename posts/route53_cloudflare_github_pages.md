---
title: "Dominio Route 53 + Cloudflare + GitHub Pages: guida completa con privacy avanzata"
date: 2026-11-07
tags: [dns, cloudflare, aws, github, privacy, guida]
description: Dalla registrazione di un dominio su AWS Route 53 alla gestione DNS gratuita su Cloudflare e al collegamento a GitHub Pages, con sezioni facoltative di hardening e privacy (proxy, ECH, header HTTP, email anti-spoofing, DNSSEC, CAA, zero tracking).
---

Procedura passo passo per registrare un dominio su **AWS Route 53**, gestire i DNS gratis su **Cloudflare** (piano Free, 0 €/mese) e collegarlo a una pagina su **GitHub Pages** (hosting e SSL gratuiti), con sezioni facoltative di hardening e privacy avanzata.

Negli esempi uso **`tuodominio.click`** come nome del dominio e **`tuonome.github.io`** come indirizzo della pagina GitHub Pages, dove `tuonome` è il tuo nome utente GitHub. Sostituiscili con i tuoi in ogni comando, record e link.

**In questa guida**

*Percorso base (configurazione e zero costi)*

- Fase 0: [Prerequisito: creare il sito su GitHub Pages](#fase-0)
- Fase 1: [Registrazione del dominio su AWS Route 53](#fase-1)
- Fase 2: [Aggiunta del dominio su Cloudflare (piano Free)](#fase-2)
- Fase 3: [Configurazione privacy e blocco dei bot AI](#fase-3)
- Fase 4: [Inserimento dei record DNS per GitHub Pages](#fase-4)
- Fase 5: [Verifica DNSSEC e recupero dei Name Server](#fase-5)
- Fase 6: [Cambio dei Name Server su AWS Route 53](#fase-6)
- Fase 7: [Collegamento del Custom Domain su GitHub Pages](#fase-7)
- Fase 8: [Eliminazione della Hosted Zone AWS (zero costi)](#fase-8)

*Sezioni facoltative (privacy avanzata)*

- [A. Proxy arancione, SSL Strict ed ECH](#opzionale-a)
- [B. Header HTTP di privacy (zero referrer e permessi)](#opzionale-b)
- [C. Blindatura email (SPF, DMARC, Null MX o alias)](#opzionale-c)
- [D. Privacy su GitHub (email noreply ed EXIF)](#opzionale-d)
- [E. DNSSEC completo e record CAA](#opzionale-e)
- [F. Zero tracking e isolamento delle risorse esterne](#opzionale-f)

---

<h2 id="fase-0">Fase 0. Prerequisito: creare e pubblicare il sito su GitHub Pages</h2>

Prima di collegare il dominio serve un sito funzionante su GitHub Pages, raggiungibile all'indirizzo gratuito `tuonome.github.io`. Se lo hai già online, salta alla Fase 1.

1. Accedi al tuo account [GitHub](https://github.com/login) (o [creane uno](https://github.com/signup)). Il nome utente determina l'indirizzo del sito: l'utente `tuonome` ottiene `tuonome.github.io`.
2. Vai su [New repository](https://github.com/new) e imposta:
    - **Repository name:** esattamente `tuonome.github.io` (nome utente + `.github.io`).
    - **Visibilità:** **Public** (GitHub Pages gratuito richiede un repository pubblico).
    - Spunta **Add a README file** e clicca su **Create repository**.
3. Nel repository clicca su **Add file** > **Create new file**, chiamalo `index.html`, incolla il contenuto della tua pagina (o una pagina di prova) e premi **Commit changes**.
4. Vai su **Settings** > **Pages** del repository. Sotto **Build and deployment** imposta **Source: Deploy from a branch**, **Branch: main**, cartella **/ (root)** e clicca su **Save**.
5. Attendi 1-2 minuti (puoi seguire l'avanzamento nella scheda **Actions**, workflow *pages build and deployment*) e poi apri `https://tuonome.github.io`.

> **Verifica:** in *Settings > Pages* compare la scritta *"Your site is live at https://tuonome.github.io/"* e la pagina si apre correttamente nel browser.

---

<h2 id="fase-1">Fase 1. Registrazione del dominio su AWS Route 53</h2>

Quando acquisti un dominio su AWS Route 53, paghi solo il costo annuale del nome a dominio (TLD, per esempio `.click`). Tuttavia, AWS crea in automatico anche una **Hosted Zone** che costa **0,50 $/mese**. L'obiettivo della guida è mantenere la registrazione su AWS ma spostare i DNS gratis su Cloudflare.

1. Accedi alla [AWS Management Console](https://console.aws.amazon.com/) e apri il servizio [Route 53](https://console.aws.amazon.com/route53/home).
2. Nel menu laterale sinistro, sotto la voce **Domains**, clicca su [Registered domains](https://console.aws.amazon.com/route53/domains/home) e premi il pulsante **Register domains**.
3. Cerca il dominio desiderato (per esempio `tuodominio.click`), verifica la disponibilità e procedi al checkout.
4. Nella schermata dei dati di contatto del registrante, assicurati di **attivare la Privacy Protection** (*Enable privacy protection*) per oscurare gratuitamente i tuoi dati personali (nome, indirizzo, email, telefono) nei database pubblici WHOIS.
5. Completa l'ordine e attendi l'email di verifica ICANN per confermare l'indirizzo email del proprietario.

> **Verifica:** il dominio `tuodominio.click` compare nell'elenco [Route 53 > Registered domains](https://console.aws.amazon.com/route53/domains/home) con *Privacy protection: Enabled*.

---

<h2 id="fase-2">Fase 2. Aggiunta del dominio su Cloudflare (piano Free)</h2>

Ora configuriamo Cloudflare per gestire gratuitamente i record DNS senza trasferire la proprietà del dominio.

1. Accedi alla [dashboard di Cloudflare](https://dash.cloudflare.com/) e clicca su **Aggiungi un sito** (*Add a site*).
2. Tra le tre opzioni proposte (*Connetti un dominio*, *Trasferisci un dominio*, *Acquista un dominio*), scegli **Connetti un dominio**.
3. Nel campo **Nome dominio**, inserisci esattamente `tuodominio.click` (senza `www` né `https://`).
4. Sotto la sezione **Importa record DNS**, lascia selezionata l'opzione **Automatico** (*Importa i record DNS automaticamente*).

---

<h2 id="fase-3">Fase 3. Configurazione privacy stringente e blocco dei bot AI</h2>

Nella stessa schermata di inserimento del dominio su Cloudflare (sotto *Configurazione aggiuntiva*), applica le impostazioni di privacy più restrittive prima di continuare:

- **Monetizzo le pagine con annunci:** lascia **Disattivato**.
- **Ricerca (motori di ricerca):** imposta su **Consenti** se vuoi che il sito sia trovabile su Google/Bing, oppure su **Blocca** se desideri che il sito non venga indicizzato.
- **Addestramento (crawler AI):** imposta su **Blocca** (impedisce lo scraping del tuo sito per l'addestramento di modelli LLM).
- **Agenti e agenti personali:** imposta su **Blocca** sia la policy generale sia i singoli agenti (*Claude Duet*, *dots*, *Gemini Spark*, *Muse*, *Instinct*).
- **Enable Bot Preference Sync:** lascia **Disattivato** per evitare che Cloudflare modifichi automaticamente il file `robots.txt`.

Poi:

1. Clicca su **Continua** in fondo alla pagina.
2. Nella schermata di selezione del piano tariffario, scorri fino in fondo, seleziona il piano **Free (0 $/mese)** e clicca su **Continua**.

---

<h2 id="fase-4">Fase 4. Inserimento dei record DNS per GitHub Pages</h2>

Nella schermata **Rivedi i record DNS** (dove la scansione iniziale mostra `Record trovati: 0`), clicca sul pulsante **+ Aggiungi record** per inserire i 4 indirizzi IP ufficiali di GitHub Pages e il sottodominio `www`.

| Tipo | Nome | Contenuto / Destinazione | Stato Proxy | TTL |
|---|---|---|---|---|
| `A` | `@` (tuodominio.click) | `185.199.108.153` | Solo DNS (grigio) | `1` (Auto) |
| `A` | `@` (tuodominio.click) | `185.199.109.153` | Solo DNS (grigio) | `1` (Auto) |
| `A` | `@` (tuodominio.click) | `185.199.110.153` | Solo DNS (grigio) | `1` (Auto) |
| `A` | `@` (tuodominio.click) | `185.199.111.153` | Solo DNS (grigio) | `1` (Auto) |
| `CNAME` | `www` | `tuonome.github.io` | Solo DNS (grigio) | `1` (Auto) |

1. Una volta inseriti i 5 record nella tabella, clicca sul pulsante blu **Continua** in fondo alla pagina.
2. Compare il popup di avviso *"tuodominio.click non è completamente protetto (Tutti i record DNS sono impostati sullo stato proxy Solo DNS)"*: clicca su **Lo farò più tardi**.

---

<h2 id="fase-5">Fase 5. Verifica DNSSEC e recupero dei Name Server Cloudflare</h2>

1. **Avviso DNSSEC:** su AWS Route 53 il DNSSEC per i nuovi domini è **disattivato di default**.
2. Nella stessa pagina di Cloudflare, individua i **2 Name Server** assegnati al tuo account (per esempio `xxx.ns.cloudflare.com` e `yyy.ns.cloudflare.com`) e copiali.

---

<h2 id="fase-6">Fase 6. Aggiornamento dei Name Server su AWS Route 53</h2>

1. Nella console di [AWS Route 53](https://console.aws.amazon.com/route53/home), vai su [Registered domains](https://console.aws.amazon.com/route53/domains/home) > `tuodominio.click`.
2. Clicca su **Actions** > **Edit name servers**.
3. Cancella i 4 server di AWS e incolla i **2 Name Server di Cloudflare**.
4. Clicca su **Save** e poi su Cloudflare premi **Fine, controlla i server dei nomi**.

---

<h2 id="fase-7">Fase 7. Collegamento del Custom Domain su GitHub Pages</h2>

1. Su GitHub entra nel repository `tuonome.github.io` > **Settings** > **Pages**.
2. Sotto **Custom domain**, inserisci `tuodominio.click` (senza `www`) e clicca su **Save**.
3. GitHub aggiunge da solo al repository un file chiamato `CNAME` con il tuo dominio: **non eliminarlo**. Se lavori con Git in locale, esegui `git pull` prima del prossimo `git push`.
4. Attendi la scritta verde *DNS check successful*. Può richiedere da pochi minuti a qualche ora, finché i Name Server della Fase 6 non si sono propagati.
5. Spunta la casella **Enforce HTTPS**. Se è grigia e non selezionabile, GitHub sta ancora emettendo il certificato: riprova dopo 15-60 minuti.
6. Apri `https://tuodominio.click` e `https://www.tuodominio.click`: entrambi devono mostrare il tuo sito (`www` viene reindirizzato in automatico al dominio principale).

> **Importante: tieni la nuvola grigia fino alla fine.** Finché il *DNS check* non è riuscito e *Enforce HTTPS* non è attivo, lascia i record su Cloudflare in modalità **Solo DNS** (nuvola grigia). Il proxy arancione (Opzionale A) va attivato solo dopo, altrimenti GitHub non riesce a verificare il dominio.

> **Consigliato: verifica il dominio su GitHub.** Da [Settings > Pages > Add a domain](https://github.com/settings/pages_verified_domains) del tuo profilo puoi verificare `tuodominio.click` con un record `TXT` su Cloudflare. Impedisce ad altri utenti GitHub di rivendicare il tuo dominio (domain takeover) se un giorno i record DNS restassero orfani.

> **Verifica:** `https://tuodominio.click` si apre con il lucchetto e *Settings > Pages* mostra *"Your site is published at https://tuodominio.click/"*.

---

<h2 id="fase-8">Fase 8. Eliminazione della Hosted Zone su AWS (azzeramento costi)</h2>

1. Solo dopo che il sito è attivo su Cloudflare, apri [AWS Route 53](https://console.aws.amazon.com/route53/home) > [Hosted zones](https://console.aws.amazon.com/route53/v2/hostedzones).
2. Elimina eventuali record personalizzati interni a `tuodominio.click` (eccetto NS e SOA).
3. Seleziona la zona `tuodominio.click`, clicca su **Delete zone** e conferma digitando `delete`.

---

## Sezioni facoltative: hardening e privacy avanzata

Le sei sezioni che seguono sono indipendenti tra loro. Si fanno **dopo** la Fase 8, a sito funzionante.

<h3 id="opzionale-a">Opzionale A. Proxy Cloudflare, SSL Full (Strict) ed ECH (Encrypted Client Hello)</h3>

Una volta che GitHub Pages ha emesso il certificato HTTPS e il sito funziona, puoi attivare il proxy di Cloudflare (**Con proxy / nuvola arancione**) per sbloccare le funzioni di crittografia avanzata e proteggere la privacy dei visitatori dagli ISP.

1. **Prima imposta SSL/TLS su Full (Strict).** Nel menu di Cloudflare vai su **SSL/TLS** > **Panoramica (Overview)** e seleziona **Completa (rigida) / Full (Strict)**. *Importante: se lasci "Flessibile", si crea un loop di reindirizzamento infinito con GitHub Pages.*
2. **Attiva la nuvola arancione.** Vai su **DNS** > **Record** e commuta lo switch da *Solo DNS* a **Con proxy** su tutti i 4 record `A` e sul record `CNAME`.
3. **Attiva HSTS e TLS 1.3.** Vai su **SSL/TLS** > **Certificati Edge (Edge Certificates)**:
    - Attiva **Usa sempre HTTPS (Always Use HTTPS)**.
    - Imposta **Versione TLS minima** su `TLS 1.2`.
    - Attiva **TLS 1.3**.
4. **Encrypted Client Hello (ECH).** Sempre in *Certificati Edge* (o nella sezione *Rete / Network*), assicurati che **Encrypted Client Hello (ECH)** sia attivo. Questa funzione cifra il campo SNI durante la connessione TLS, impedendo al provider Internet (ISP) del visitatore di leggere il nome specifico del dominio visitato dietro la rete Cloudflare.

<h3 id="opzionale-b">Opzionale B. HTTP Response Headers per la privacy (zero referrer e blocco API del browser)</h3>

Anche su un sito statico su GitHub Pages (che non permette di configurare file `.htaccess`), il piano gratuito di Cloudflare permette di iniettare header HTTP di sicurezza e privacy tramite le **Transform Rules**. Richiede la nuvola arancione attiva.

1. Su Cloudflare, apri il tuo dominio e vai su **Regole (Rules)** > **Impostazioni / Transform Rules** > scheda **Modifica intestazione di risposta (Modify Response Header)**.
2. Clicca su **Crea regola**, chiamala `Privacy Hardening Headers` e seleziona **Tutte le richieste in arrivo (All incoming requests)**.
3. Aggiungi le seguenti operazioni di tipo **Set static** (Imposta statico):

| Nome intestazione (Header Name) | Valore (Value) | Scopo per la privacy |
|---|---|---|
| `Referrer-Policy` | `no-referrer` | Impedisce al browser di comunicare ai siti esterni che l'utente proviene dal tuo dominio. |
| `Permissions-Policy` | `geolocation=(), camera=(), microphone=(), interest-cohort=(), browsing-topics=()` | Disattiva geolocalizzazione, sensori e blocca il tracciamento pubblicitario (Google Topics API / FLoC). |
| `X-Content-Type-Options` | `nosniff` | Impedisce il MIME-sniffing dei file scaricati o visualizzati. |
| `X-Frame-Options` | `DENY` | Impedisce a siti terzi di incorporare il tuo sito dentro un `<iframe>` (anti-clickjacking). |

<h3 id="opzionale-c">Opzionale C. Blindatura email del dominio (anti-spoofing o Email Routing anonimo)</h3>

Un dominio senza record di posta permette a chiunque di inviare email di phishing fingendo di scrivere da `@tuodominio.click`. Hai due scenari possibili.

**Scenario 1: non usi l'email sul dominio (blocco totale anti-spoofing).** Aggiungi questi 3 record su Cloudflare > DNS > Record, per dichiarare a tutti i server del mondo che nessuna email legittima parte o arriva su `tuodominio.click`:

| Tipo | Nome | Contenuto | Note |
|---|---|---|---|
| `TXT` | `@` | `"v=spf1 -all"` | SPF rigoroso: nessun server è autorizzato a inviare email. |
| `TXT` | `_dmarc` | `"v=DMARC1; p=reject; sp=reject; adkim=s; aspf=s;"` | DMARC: ordina di cestinare subito qualsiasi email contraffatta. |
| `MX` | `@` | Server: `.` · Priorità: `0` | Record Null MX (RFC 7505): indica che il dominio non accetta posta. |

**Scenario 2: vuoi ricevere email senza esporre il tuo indirizzo personale.** Se vuoi pubblicare un contatto sul sito (per esempio `info@tuodominio.click`) senza rivelare la tua casella personale, vai su Cloudflare in **Email** > **Email Routing**: Cloudflare inoltra gratuitamente i messaggi ricevuti su `info@tuodominio.click` alla tua casella privata, mantenendola nascosta.

<h3 id="opzionale-d">Opzionale D. Privacy del proprietario su GitHub (email nei commit e metadati EXIF)</h3>

> **Attenzione: i repository GitHub Pages gratuiti sono pubblici.** Chiunque può ispezionare la cronologia dei commit di `tuonome.github.io`. Se fai commit con la tua email personale, questa resta visibile pubblicamente nel log di Git (`git log`).

1. **Attiva l'email privata su GitHub.** Vai su GitHub > **Settings** (del tuo profilo) > **Emails**.
2. Spunta la casella **Keep my email addresses private** e spunta anche **Block command line pushes that expose my personal email**.
3. Copia l'indirizzo generato da GitHub nelle [impostazioni email](https://github.com/settings/emails) (formato `12345678+tuonome@users.noreply.github.com`) e configuralo nel tuo terminale locale con `git config --global user.email "12345678+tuonome@users.noreply.github.com"`.

4. **Rimozione dei metadati EXIF dalle immagini.** Prima di caricare foto JPG/PNG nel repository del sito, rimuovi sempre i metadati EXIF (che possono contenere le coordinate GPS esatte di casa o ufficio e il modello del telefono) usando strumenti come [exiftool](https://exiftool.org/): `exiftool -all= immagine.jpg`.

<h3 id="opzionale-e">Opzionale E. Riattivazione DNSSEC (Cloudflare + Route 53) e record CAA</h3>

Per impedire attacchi di *DNS Spoofing / Cache Poisoning* e limitare chi può generare certificati SSL per il tuo dominio:

1. **Attiva DNSSEC su Cloudflare.** Vai su **DNS** > **Impostazioni (Settings)** e clicca su **Abilita DNSSEC (Enable DNSSEC)**. Cloudflare ti mostra i parametri del record `DS` (Key Tag, Algorithm, Digest Type, Digest).
2. **Registra la chiave DS su AWS Route 53.** Vai su [Route 53](https://console.aws.amazon.com/route53/home) > [Registered domains](https://console.aws.amazon.com/route53/domains/home) > `tuodominio.click` > sezione **DNSSEC status** > **Manage keys** e inserisci i dati mostrati da Cloudflare.
3. **Aggiungi i record CAA su Cloudflare.** In **DNS > Record**, aggiungi due record di tipo `CAA` su `@` con flag `0` e tag `issue`: uno per [`letsencrypt.org`](https://letsencrypt.org/) (usato da GitHub Pages) e uno per `pki.goog` / `ssl.com` (usati da Cloudflare Universal SSL). In questo modo nessun'altra Certification Authority al mondo potrà emettere certificati per `tuodominio.click`.

<h3 id="opzionale-f">Opzionale F. Zero tracking sul sito e isolamento delle risorse di terze parti (niente cookie banner)</h3>

Per rendere `tuodominio.click` conforme al GDPR senza banner dei cookie e senza cedere a terzi i dati dei visitatori:

- **Niente Google Fonts da CDN esterno.** Non caricare mai font da `fonts.googleapis.com` o `fonts.gstatic.com` (trasmettono l'indirizzo IP di ogni visitatore a Google). Scarica i file `.woff2` e ospitali direttamente in una cartella `/fonts` dentro il tuo repository GitHub.
- **Niente librerie JS da CDN esterni.** Evita link a `cdnjs`, `unpkg` o `jsdelivr`; salva gli script localmente nel repository.
- **Statistiche senza tracciamento.** Se vuoi sapere quante visite riceve il sito senza usare Google Analytics, ti basta consultare le statistiche aggregate lato rete già incluse gratuitamente nella dashboard di Cloudflare (sezione **Analytics & Logs > Traffic**), che non installano alcun cookie né script nel browser dell'utente.

---

*Guida tecnica (edizione privacy avanzata): AWS Route 53 + Cloudflare + GitHub Pages.*
