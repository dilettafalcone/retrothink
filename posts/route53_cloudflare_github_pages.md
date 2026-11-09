---
title: "Dominio .xyz (gen.xyz, Spaceship, Porkbun, Dynadot) + Cloudflare + GitHub Pages: guida completa con privacy avanzata"
date: 2026-11-07
tags: [dns, cloudflare, registrar, github, privacy, guida]
description: Dalla registrazione di un dominio su gen.xyz, Spaceship, Porkbun o Dynadot alla gestione DNS gratuita su Cloudflare e al collegamento a GitHub Pages, con sezioni facoltative di hardening e privacy (proxy, ECH, header HTTP, email anti-spoofing, DNSSEC, CAA, zero tracking).
---

Procedura passo passo per registrare un dominio su uno di questi quattro registrar (**gen.xyz**, **Spaceship**, **Porkbun**, **Dynadot**), gestire i DNS gratis su **Cloudflare** (piano Free, 0 €/mese) e collegarlo a una pagina su **GitHub Pages** (hosting e SSL gratuiti), con sezioni facoltative di hardening e privacy avanzata.

Il registrar ti serve solo per **comprare e rinnovare** il nome. I DNS li gestisce Cloudflare: al registrar si cambiano soltanto i Name Server (Fase 6). Scegli un registrar e segui solo la sua sottosezione nelle Fasi 1, 6 e nell'Opzionale E.

Negli esempi uso **`tuodominio.xyz`** come nome del dominio e **`tuonome.github.io`** come indirizzo della pagina GitHub Pages, dove `tuonome` è il tuo nome utente GitHub. Sostituiscili con i tuoi in ogni comando, record e link.

**In questa guida**

*Percorso base (configurazione e zero costi)*

- Fase 0: [Prerequisito: creare il sito su GitHub Pages](#fase-0)
- Fase 1: [Registrazione del dominio (gen.xyz, Spaceship, Porkbun o Dynadot)](#fase-1)
- Fase 2: [Aggiunta del dominio su Cloudflare (piano Free)](#fase-2)
- Fase 3: [Configurazione privacy e blocco dei bot AI](#fase-3)
- Fase 4: [Inserimento dei record DNS per GitHub Pages](#fase-4)
- Fase 5: [Controllo DNSSEC e recupero dei Name Server](#fase-5)
- Fase 6: [Cambio dei Name Server dal registrar](#fase-6)
- Fase 7: [Collegamento del Custom Domain su GitHub Pages](#fase-7)
- Fase 8: [Verifica finale e pulizia](#fase-8)

*Sezioni facoltative (privacy avanzata)*

- [A. Proxy arancione, SSL Strict ed ECH](#opzionale-a)
- [B. Header HTTP di privacy (zero referrer e permessi)](#opzionale-b)
- [C. Blindatura email (SPF, DMARC, Null MX o alias)](#opzionale-c)
- [D. Privacy su GitHub (email noreply ed EXIF)](#opzionale-d)
- [E. DNSSEC completo e record CAA](#opzionale-e)
- [F. Zero tracking e isolamento delle risorse esterne](#opzionale-f)

**Prima di iniziare: i comandi di verifica.** In tutta la guida controllo i DNS con questi comandi. Su Linux/Bazzite/macOS usa `dig` (se manca: `sudo apt install dnsutils` su Debian/Ubuntu, `sudo dnf install bind-utils` su Fedora/Bazzite, già presente su macOS). Su Windows usa PowerShell, dove `Resolve-DnsName` è già installato. Non serve installare nulla.

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

<h2 id="fase-1">Fase 1. Registrazione del dominio</h2>

Registra `tuodominio.xyz` su **uno solo** dei quattro registrar qui sotto. Paghi il nome a dominio (primo anno e rinnovi: controlla il prezzo del **rinnovo**, non solo quello della promozione del primo anno). Ogni registrar mette di default i propri DNS e spesso crea record "di parcheggio": li sostituiremo con Cloudflare nella Fase 6.

Prima di pagare, in tutti e quattro i casi verifica queste due cose nel carrello:

- **Privacy WHOIS** attiva, per oscurare nome, indirizzo, email e telefono nei database pubblici.
- **Rinnovo automatico** attivo (o un promemoria ben visibile): se il dominio scade, il sito sparisce e qualcun altro può registrarlo.

<h3 id="fase-1-genxyz">1A. gen.xyz</h3>

[gen.xyz](https://gen.xyz/) è il registrar ufficiale del registro del `.xyz`: vende solo domini `.xyz` e, per i `.xyz` a 4 o più cifre, sfrutta le promozioni del registro.

1. Apri [gen.xyz](https://gen.xyz/), scrivi `tuodominio` nella casella di ricerca e premi **Search**.
2. Accanto a `tuodominio.xyz` clicca su **Add to cart** e poi su **Checkout**.
3. Scegli il periodo di registrazione (1 anno) e, nella sezione dei componenti aggiuntivi, **aggiungi la protezione WHOIS** (*WHOIS Privacy Protection*): su gen.xyz è un'opzione a pagamento, non è inclusa di default.
4. Crea l'account (email e password) o accedi, completa i dati di contatto del registrante e paga.
5. Conferma l'email di verifica ICANN che arriva all'indirizzo del registrante: senza conferma, il dominio viene sospeso dopo qualche giorno.

> **Verifica:** accedi a [gen.xyz/account/clientarea.php](https://gen.xyz/account/clientarea.php) > **Domains** > **My Domains**: `tuodominio.xyz` compare con stato *Active*.

<h3 id="fase-1-spaceship">1B. Spaceship</h3>

1. Apri [spaceship.com](https://www.spaceship.com/), scrivi `tuodominio.xyz` nella ricerca e clicca su **Search**.
2. Clicca su **Add to cart** accanto al dominio e poi su **Checkout**.
3. Registra l'account (o accedi). Nel riepilogo ordine verifica che **Domain Privacy** (*Spaceship Privacy*) sia incluso a 0 €: su Spaceship la protezione WHOIS è gratuita.
4. Disattiva (se presenti) i componenti aggiuntivi non richiesti, come hosting, email e *Spaceship Domain Protection*, e paga.
5. Conferma l'email di verifica ICANN che arriva all'indirizzo del registrante.

> **Verifica:** nel pannello [Domain List](https://www.spaceship.com/application/domain-list-application/) il dominio `tuodominio.xyz` compare con stato attivo.

<h3 id="fase-1-porkbun">1C. Porkbun</h3>

1. Apri [porkbun.com](https://porkbun.com/), scrivi `tuodominio.xyz` nella casella di ricerca e premi invio.
2. Clicca sul pulsante **+** (aggiungi al carrello) accanto a `tuodominio.xyz` e poi su **Go to Cart**.
3. Nel carrello controlla che **WHOIS Privacy** sia incluso e gratuito (lo è di default per i domini che lo supportano). Se Porkbun ti propone un bundle di hosting o email, togli la spunta.
4. Crea l'account (o accedi), imposta i dati di contatto del registrante e paga.
5. Conferma l'email di verifica ICANN che arriva all'indirizzo del registrante.

> **Verifica:** da **ACCOUNT** > **Domain Management** il dominio `tuodominio.xyz` compare nell'elenco con la scritta *WHOIS Privacy* attiva.

<h3 id="fase-1-dynadot">1D. Dynadot</h3>

1. Apri [dynadot.com](https://www.dynadot.com/), scrivi `tuodominio.xyz` nella casella di ricerca e clicca su **Search**.
2. Clicca su **Add to Cart** accanto al dominio e poi sull'icona del carrello > **Checkout**.
3. Nel carrello verifica che **Whois Privacy** sia impostato su **Free** (Dynadot lo include senza costi). Se compaiono proposte di hosting, sito web o email, togli la spunta.
4. Crea l'account (o accedi), controlla i dati del registrante e paga.
5. Conferma l'email di verifica ICANN che arriva all'indirizzo del registrante.

> **Verifica:** da **My Domains** > **Manage Domains** il dominio `tuodominio.xyz` compare con *Whois Privacy* attiva.

---

<h2 id="fase-2">Fase 2. Aggiunta del dominio su Cloudflare (piano Free)</h2>

Ora configuriamo Cloudflare per gestire gratuitamente i record DNS senza trasferire la proprietà del dominio: il registrar resta quello che hai scelto nella Fase 1.

1. Accedi alla [dashboard di Cloudflare](https://dash.cloudflare.com/) e clicca su **Aggiungi un sito** (*Add a site*).
2. Tra le tre opzioni proposte (*Connetti un dominio*, *Trasferisci un dominio*, *Acquista un dominio*), scegli **Connetti un dominio**.
3. Nel campo **Nome dominio**, inserisci esattamente `tuodominio.xyz` (senza `www` né `https://`).
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

Nella schermata **Rivedi i record DNS** clicca sul pulsante **+ Aggiungi record** per inserire i 4 indirizzi IP ufficiali di GitHub Pages e il sottodominio `www`.

**Prima controlla cosa ha importato Cloudflare.** Se il registrar ha già messo record di parcheggio sul dominio (succede spesso su Porkbun, Spaceship e Dynadot: un `A`, un `ALIAS`/`CNAME` o un `URL forwarding` verso la loro pagina "domain parked"), la scansione li mostra tra i record trovati. **Eliminali tutti** con l'icona del cestino: se restano, si mescolano ai record di GitHub Pages e il sito risponde a volte con la pagina del registrar. Se la scansione dice `Record trovati: 0`, non c'è niente da togliere.

Poi inserisci questi 5 record:

| Tipo | Nome | Contenuto / Destinazione | Stato Proxy | TTL |
|---|---|---|---|---|
| `A` | `@` (tuodominio.xyz) | `185.199.108.153` | Solo DNS (grigio) | `1` (Auto) |
| `A` | `@` (tuodominio.xyz) | `185.199.109.153` | Solo DNS (grigio) | `1` (Auto) |
| `A` | `@` (tuodominio.xyz) | `185.199.110.153` | Solo DNS (grigio) | `1` (Auto) |
| `A` | `@` (tuodominio.xyz) | `185.199.111.153` | Solo DNS (grigio) | `1` (Auto) |
| `CNAME` | `www` | `tuonome.github.io` | Solo DNS (grigio) | `1` (Auto) |

1. Una volta inseriti i 5 record nella tabella, clicca sul pulsante blu **Continua** in fondo alla pagina.
2. Compare il popup di avviso *"tuodominio.xyz non è completamente protetto (Tutti i record DNS sono impostati sullo stato proxy Solo DNS)"*: clicca su **Lo farò più tardi**.

---

<h2 id="fase-5">Fase 5. Controllo DNSSEC e recupero dei Name Server Cloudflare</h2>

**1. Controlla se sul dominio c'è già un record DS.** Il DS è l'"impronta" DNSSEC che il registrar pubblica nel registro del `.xyz`. Se resta lì mentre cambi i Name Server, i resolver che validano DNSSEC (Google 8.8.8.8, Cloudflare 1.1.1.1, la maggior parte degli ISP) non risolvono più il dominio e il sito risulta irraggiungibile (errore `SERVFAIL`). Alcuni registrar lo attivano da soli quando usi i loro DNS (Spaceship per esempio assegna DNSSEC di default), altri no.

Linux/Bazzite/macOS:

```bash
dig DS tuodominio.xyz +short
```

Windows (PowerShell):

```powershell
Resolve-DnsName tuodominio.xyz -Type DS -Server 8.8.8.8
```

- **Nessun risultato** (su `dig` risposta vuota; su PowerShell l'errore *DNS name does not exist* oppure nessuna riga di tipo `DS`): non c'è DNSSEC, vai avanti.
- **Compare una riga** del tipo `12345 13 2 ABCD...`: c'è un DS attivo. Prima di cambiare i Name Server **cancellalo dal pannello del registrar** (nella Fase 6, passo 0, trovi dove) e aspetta che il TTL scada (di solito da 1 a 24 ore). Controlla di nuovo con il comando qui sopra finché non risulta vuoto.

**2. Recupera i Name Server di Cloudflare.** Nella stessa pagina di Cloudflare, individua i **2 Name Server** assegnati al tuo account (per esempio `xxx.ns.cloudflare.com` e `yyy.ns.cloudflare.com`) e copiali: ti servono nella Fase 6.

---

<h2 id="fase-6">Fase 6. Cambio dei Name Server dal registrar</h2>

Qui dici al registro del `.xyz` di usare i DNS di Cloudflare al posto di quelli del registrar. Segui la sottosezione del tuo registrar. In ognuna, al **passo 0** rimuovi eventuali DS trovati nella Fase 5.

<h3 id="fase-6-genxyz">6A. gen.xyz</h3>

0. **Se la Fase 5 ha trovato un DS:** su gen.xyz i record DNSSEC si gestiscono **solo tramite il supporto**. Apri un ticket su [gen.xyz/account/submitticket.php](https://gen.xyz/account/submitticket.php) chiedendo di **rimuovere il record DS** da `tuodominio.xyz`, e aspetta la conferma prima di continuare.
1. Accedi a [gen.xyz/account/clientarea.php](https://gen.xyz/account/clientarea.php) > **Domains** > **My Domains**.
2. Sulla riga di `tuodominio.xyz` clicca su **Manage Domain** (icona a ingranaggio) e poi su **Nameservers** nel menu a sinistra.
3. Seleziona **Use custom nameservers** (*Usa nameserver personalizzati*).
4. Nei campi **Nameserver 1** e **Nameserver 2** incolla i due Name Server di Cloudflare. Lascia vuoti i campi 3, 4 e 5.
5. Clicca su **Change Nameservers** e conferma.

> I nomi esatti dei pulsanti di gen.xyz (area clienti basata su WHMCS) possono differire leggermente da quelli scritti qui. Se non trovi una voce, cerca nel menu del dominio quella che parla di *Nameservers* o *Name Servers* e, in caso di dubbio, consulta l'articolo [How do I set custom nameservers for a domain name?](https://gen.xyz/account/knowledgebase/14/How-do-I-set-custom-nameservers-for-a-domain-name.html) della loro guida.

> Se il pulsante **Manage DNS** del dominio è grigio, è normale: è attivo solo con i nameserver di default di gen.xyz. Da ora i record si gestiscono su Cloudflare.

<h3 id="fase-6-spaceship">6B. Spaceship</h3>

0. **Se la Fase 5 ha trovato un DS:** su Spaceship il DNSSEC si attiva e si disattiva da **Advanced DNS** del dominio. Apri [spaceship.com](https://www.spaceship.com/) > **Domain List** > **Manage** accanto a `tuodominio.xyz` > **Advanced DNS** e disattiva **DNSSEC**. Se non trovi l'interruttore, apri un ticket dal [Support Center](https://www.spaceship.com/support/) chiedendo di rimuovere il DS. Aspetta che il TTL scada.
1. Accedi a Spaceship e vai su **Domain List**; clicca su **Manage** accanto a `tuodominio.xyz`.
2. Apri la scheda **Advanced DNS** (o *DNS*) del dominio.
3. Nella sezione **Nameservers** clicca su **Change**.
4. Nella finestra che si apre scegli **Custom nameservers**.
5. Incolla i due Name Server di Cloudflare (uno per riga o uno per campo), poi clicca su **Save**. Spaceship avvisa che hosting ed email collegati a Spaceship smetteranno di funzionare: conferma (non ne hai).

<h3 id="fase-6-porkbun">6C. Porkbun</h3>

0. **Se la Fase 5 ha trovato un DS:** accedi a Porkbun > **ACCOUNT** > **Domain Management**, clicca su **Details** a destra di `tuodominio.xyz` e, accanto a **Registry DNSSEC**, clicca sull'icona di modifica; elimina il record (voce di cancellazione/*Delete* accanto alla riga) e salva. Aspetta che il TTL scada.
1. Accedi a [porkbun.com](https://porkbun.com/) e clicca su **ACCOUNT** > **Domain Management**.
2. Sulla riga di `tuodominio.xyz` clicca su **Details** (freccia a destra).
3. Nella sezione **Authoritative Nameservers** clicca sull'icona **Edit** (matita).
4. Cancella tutti i nameserver di Porkbun (`curitiba.ns.porkbun.com`, `fortaleza.ns.porkbun.com`, `maceio.ns.porkbun.com`, `salvador.ns.porkbun.com`) e inserisci i due di Cloudflare, uno per riga.
5. Clicca su **Submit**. Se compare un messaggio che chiede di confermare il cambio, clicca su **Submit** una seconda volta: senza la seconda conferma la modifica non viene salvata.

> Non aggiungere i Name Server come record `NS` nella sezione *DNS Records* di Porkbun: quei record non cambiano i nameserver autoritativi del dominio.

<h3 id="fase-6-dynadot">6D. Dynadot</h3>

0. **Se la Fase 5 ha trovato un DS:** accedi a Dynadot > **My Domains** > **Manage Domains**, clicca sul nome `tuodominio.xyz`, scorri fino alla sezione **DNSSEC** e clicca su **Clear DNSSEC**. Ha effetto subito sul registro, ma aspetta comunque che il TTL scada.
1. Accedi a [dynadot.com](https://www.dynadot.com/) > **My Domains** > **Manage Domains**.
2. Spunta la casella accanto a `tuodominio.xyz`, clicca sul pulsante **Action** e scegli **DNS Settings**.
3. Nel menu a tendina in alto della pagina DNS scegli **Name Servers**.
4. Seleziona l'opzione dei nameserver personalizzati (*Use Custom Name Servers*) e incolla i due Name Server di Cloudflare nei campi **Name Server 1** e **Name Server 2**.
5. Clicca su **Save Name Servers**.

**Verifica comune a tutti i registrar** (dopo qualche minuto; la propagazione completa può richiedere fino a 24-48 ore):

Linux/Bazzite/macOS:

```bash
dig NS tuodominio.xyz +short
```

Windows (PowerShell):

```powershell
Resolve-DnsName tuodominio.xyz -Type NS -Server 8.8.8.8
```

Devi vedere i due Name Server di Cloudflare (`xxx.ns.cloudflare.com` e `yyy.ns.cloudflare.com`). Poi torna su Cloudflare e premi **Fine, controlla i server dei nomi** (*Done, check nameservers*): quando lo stato del dominio diventa **Attivo** (*Active*), Cloudflare ti manda una email di conferma.

---

<h2 id="fase-7">Fase 7. Collegamento del Custom Domain su GitHub Pages</h2>

1. Su GitHub entra nel repository `tuonome.github.io` > **Settings** > **Pages**.
2. Sotto **Custom domain**, inserisci `tuodominio.xyz` (senza `www`) e clicca su **Save**.
3. GitHub aggiunge da solo al repository un file chiamato `CNAME` con il tuo dominio: **non eliminarlo**. Se lavori con Git in locale, esegui `git pull` prima del prossimo `git push`.
4. Attendi la scritta verde *DNS check successful*. Può richiedere da pochi minuti a qualche ora, finché i Name Server della Fase 6 non si sono propagati.
5. Spunta la casella **Enforce HTTPS**. Se è grigia e non selezionabile, GitHub sta ancora emettendo il certificato: riprova dopo 15-60 minuti.
6. Apri `https://tuodominio.xyz` e `https://www.tuodominio.xyz`: entrambi devono mostrare il tuo sito (`www` viene reindirizzato in automatico al dominio principale).

> **Importante: tieni la nuvola grigia fino alla fine.** Finché il *DNS check* non è riuscito e *Enforce HTTPS* non è attivo, lascia i record su Cloudflare in modalità **Solo DNS** (nuvola grigia). Il proxy arancione (Opzionale A) va attivato solo dopo, altrimenti GitHub non riesce a verificare il dominio.

> **Consigliato: verifica il dominio su GitHub.** Da [Settings > Pages > Add a domain](https://github.com/settings/pages_verified_domains) del tuo profilo puoi verificare `tuodominio.xyz` con un record `TXT` su Cloudflare. Impedisce ad altri utenti GitHub di rivendicare il tuo dominio (domain takeover) se un giorno i record DNS restassero orfani.

> **Verifica:** `https://tuodominio.xyz` si apre con il lucchetto e *Settings > Pages* mostra *"Your site is published at https://tuodominio.xyz/"*.

---

<h2 id="fase-8">Fase 8. Verifica finale e pulizia</h2>

Con il registrar non c'è nessuna "zona" da eliminare e non ci sono costi mensili: pagherai solo il rinnovo annuale del nome. Resta da controllare che i vecchi DNS del registrar non vengano più usati e che tutto risolva come previsto.

1. **Controlla gli indirizzi del sito.**

    Linux/Bazzite/macOS:

    ```bash
    dig A tuodominio.xyz +short
    dig CNAME www.tuodominio.xyz +short
    ```

    Windows (PowerShell):

    ```powershell
    Resolve-DnsName tuodominio.xyz -Type A -Server 8.8.8.8
    Resolve-DnsName www.tuodominio.xyz -Type CNAME -Server 8.8.8.8
    ```

    Devono comparire i quattro IP `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153` e `tuonome.github.io`. Se vedi altri indirizzi, sono record di parcheggio del registrar rimasti su Cloudflare (torna alla Fase 4).

2. **Controlla il certificato e la risposta HTTP.**

    Linux/Bazzite/macOS e Windows 10/11 (PowerShell, usa `curl.exe`):

    ```bash
    curl -I https://tuodominio.xyz
    ```

    La prima riga deve essere `HTTP/2 200` (o `301` se stai chiedendo `http://`).

3. **Spegni ogni servizio di parcheggio, inoltro o email del registrar** nel pannello del dominio (*URL forwarding*, *Domain Parking*, *Email forwarding*): con i Name Server di Cloudflare non hanno più effetto, ma meglio non lasciarli configurati. Gli inoltri email si rifanno con Cloudflare Email Routing (Opzionale C).
4. **Attiva il rinnovo automatico** (*Auto-Renew*) nel pannello del registrar, se non l'hai già fatto, e usa un metodo di pagamento che non scade a breve.
5. **Attiva il blocco di trasferimento** (*Registrar Lock*, *Transfer Lock*): di solito è già attivo di default. Impedisce che il dominio venga trasferito a un altro registrar senza il tuo consenso.

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

4. Verifica gli header dal terminale:

    ```bash
    curl -sI https://tuodominio.xyz | grep -iE "referrer-policy|permissions-policy|x-content-type-options|x-frame-options"
    ```

    Su Windows (PowerShell):

    ```powershell
    curl.exe -sI https://tuodominio.xyz | Select-String -Pattern "referrer-policy|permissions-policy|x-content-type-options|x-frame-options"
    ```

<h3 id="opzionale-c">Opzionale C. Blindatura email del dominio (anti-spoofing o Email Routing anonimo)</h3>

Un dominio senza record di posta permette a chiunque di inviare email di phishing fingendo di scrivere da `@tuodominio.xyz`. Hai due scenari possibili.

**Scenario 1: non usi l'email sul dominio (blocco totale anti-spoofing).** Aggiungi questi 3 record su Cloudflare > DNS > Record, per dichiarare a tutti i server del mondo che nessuna email legittima parte o arriva su `tuodominio.xyz`:

| Tipo | Nome | Contenuto | Note |
|---|---|---|---|
| `TXT` | `@` | `"v=spf1 -all"` | SPF rigoroso: nessun server è autorizzato a inviare email. |
| `TXT` | `_dmarc` | `"v=DMARC1; p=reject; sp=reject; adkim=s; aspf=s;"` | DMARC: ordina di cestinare subito qualsiasi email contraffatta. |
| `MX` | `@` | Server: `.` · Priorità: `0` | Record Null MX (RFC 7505): indica che il dominio non accetta posta. |

Se il registrar aveva attivato l'inoltro email o un `MX` suo (per esempio quelli di Spaceship, Porkbun o Dynadot), controlla che su Cloudflare non sia stato importato nessun altro record `MX` o `TXT` di tipo SPF, altrimenti i record qui sopra si sommano a quelli vecchi.

Verifica dal terminale:

```bash
dig TXT tuodominio.xyz +short
dig TXT _dmarc.tuodominio.xyz +short
dig MX tuodominio.xyz +short
```

Su Windows (PowerShell):

```powershell
Resolve-DnsName tuodominio.xyz -Type TXT -Server 8.8.8.8
Resolve-DnsName _dmarc.tuodominio.xyz -Type TXT -Server 8.8.8.8
Resolve-DnsName tuodominio.xyz -Type MX -Server 8.8.8.8
```

**Scenario 2: vuoi ricevere email senza esporre il tuo indirizzo personale.** Se vuoi pubblicare un contatto sul sito (per esempio `info@tuodominio.xyz`) senza rivelare la tua casella personale, vai su Cloudflare in **Email** > **Email Routing**: Cloudflare inoltra gratuitamente i messaggi ricevuti su `info@tuodominio.xyz` alla tua casella privata, mantenendola nascosta. In questo scenario **non** aggiungere i tre record dello Scenario 1: Email Routing crea da sé i record `MX` e `TXT` necessari.

<h3 id="opzionale-d">Opzionale D. Privacy del proprietario su GitHub (email nei commit e metadati EXIF)</h3>

> **Attenzione: i repository GitHub Pages gratuiti sono pubblici.** Chiunque può ispezionare la cronologia dei commit di `tuonome.github.io`. Se fai commit con la tua email personale, questa resta visibile pubblicamente nel log di Git (`git log`).

1. **Attiva l'email privata su GitHub.** Vai su GitHub > **Settings** (del tuo profilo) > **Emails**.
2. Spunta la casella **Keep my email addresses private** e spunta anche **Block command line pushes that expose my personal email**.
3. Copia l'indirizzo generato da GitHub nelle [impostazioni email](https://github.com/settings/emails) (formato `12345678+tuonome@users.noreply.github.com`) e configuralo nel tuo terminale locale con `git config --global user.email "12345678+tuonome@users.noreply.github.com"`.

4. **Rimozione dei metadati EXIF dalle immagini.** Prima di caricare foto JPG/PNG nel repository del sito, rimuovi sempre i metadati EXIF (che possono contenere le coordinate GPS esatte di casa o ufficio e il modello del telefono) usando strumenti come [exiftool](https://exiftool.org/): `exiftool -all= immagine.jpg`.

<h3 id="opzionale-e">Opzionale E. DNSSEC completo (Cloudflare + registrar) e record CAA</h3>

Per impedire attacchi di *DNS Spoofing / Cache Poisoning* e limitare chi può generare certificati SSL per il tuo dominio. Ordine obbligato: prima si firma la zona su Cloudflare, poi si pubblica il DS dal registrar. Se fai il contrario, il dominio diventa irraggiungibile per i resolver che validano DNSSEC.

1. **Attiva DNSSEC su Cloudflare.** Vai su **DNS** > **Impostazioni (Settings)** e clicca su **Abilita DNSSEC (Enable DNSSEC)**. Cloudflare ti mostra i parametri del record `DS`: **Key Tag**, **Algorithm** (di solito `13`, *ECDSA Curve P-256 with SHA-256*), **Digest Type** (di solito `2`, *SHA-256*) e **Digest**. Cloudflare mostra anche il record DS già composto in una riga, pronto da copiare: tienilo aperto.
2. **Registra il DS dal registrar.** Segui la sottosezione del tuo registrar.

    <h4 id="opzionale-e-genxyz">E-1. gen.xyz</h4>

    Su gen.xyz il DS non si inserisce da pannello: va chiesto al supporto. Apri un ticket su [gen.xyz/account/submitticket.php](https://gen.xyz/account/submitticket.php) e scrivi il DS in questo formato, con tutti i campi presi dalla schermata di Cloudflare (esempio con valori finti: sostituiscili con i tuoi):

    ```text
    tuodominio.xyz. 86400 IN DS 2371 13 2 ( A1B2C3D4E5F60718293A4B5C6D7E8F90A1B2C3D4E5F60718293A4B5C6D7E8F90 )
    ```

    I campi sono, nell'ordine: nome del dominio, TTL (`86400`), classe `IN`, tipo `DS`, **Key Tag**, **Algorithm**, **Digest Type**, **Digest**. gen.xyz non accetta i record `DNSKEY`: solo il DS.

    <h4 id="opzionale-e-spaceship">E-2. Spaceship</h4>

    1. Accedi a Spaceship > **Domain List** > **Manage** accanto a `tuodominio.xyz`.
    2. Cerca la sezione **DNSSEC** della pagina del dominio (se è su una scheda separata, di solito è dentro **Advanced DNS**).
    3. Aggiungi un nuovo record DS e inserisci **Key Tag**, **Algorithm**, **Digest Type** e **Digest** copiati da Cloudflare. Salva.
    4. Se la sezione DNSSEC non permette di inserire un DS con Name Server esterni, apri un ticket dal [Support Center](https://www.spaceship.com/support/) con gli stessi quattro valori.

    <h4 id="opzionale-e-porkbun">E-3. Porkbun</h4>

    1. Accedi a Porkbun > **ACCOUNT** > **Domain Management**.
    2. Sulla riga di `tuodominio.xyz` clicca su **Details** e poi sull'icona di modifica accanto a **Registry DNSSEC**.
    3. Nella schermata **Create DNSSEC Record** compila **Key Tag**, **Algorithm** (`13`), **Digest Type** (`2`) e **Digest** con i valori di Cloudflare. Lascia vuoti i campi del tipo `keyData` (il `.xyz` accetta solo `dsData`).
    4. Clicca su **Create** in basso a sinistra.

    <h4 id="opzionale-e-dynadot">E-4. Dynadot</h4>

    1. Accedi a Dynadot > **My Domains** > **Manage Domains** e clicca sul nome `tuodominio.xyz`.
    2. Scorri fino alla sezione **DNSSEC** (mostra *Not Set*) e clicca su **Change**.
    3. Scegli **Set a DNSSEC Record** e compila **Key Tag**, **Algorithm** (`13`, se la lista non lo mostra così cerca *ECDSA Curve P-256 with SHA-256*), **Digest Type** (`2`, *SHA-256*) e **Digest**.
    4. Clicca su **Set DNSSEC Record**.

3. **Verifica.** Dopo qualche minuto (fino a qualche ora per il DS) controlla che il DS sia pubblicato nel registro e che la catena di fiducia sia valida:

    ```bash
    dig DS tuodominio.xyz +short
    dig A tuodominio.xyz +dnssec @8.8.8.8
    ```

    Su Windows (PowerShell):

    ```powershell
    Resolve-DnsName tuodominio.xyz -Type DS -Server 8.8.8.8
    Resolve-DnsName tuodominio.xyz -Type A -DnssecOk -Server 8.8.8.8
    ```

    Nel risultato di `dig` cerca il flag `ad` (*Authenticated Data*) nella riga `flags:`. In più puoi usare il [DNSSEC Analyzer di Verisign](https://dnssec-analyzer.verisignlabs.com/) inserendo `tuodominio.xyz`. Su Cloudflare lo stato diventa **Attivo** (*DNSSEC is active*).

4. **Aggiungi i record CAA su Cloudflare.** In **DNS > Record**, aggiungi due record di tipo `CAA` su `@` con flag `0` e tag `issue`: uno per [`letsencrypt.org`](https://letsencrypt.org/) (usato da GitHub Pages) e uno per `pki.goog` / `ssl.com` (usati da Cloudflare Universal SSL). In questo modo nessun'altra Certification Authority al mondo potrà emettere certificati per `tuodominio.xyz`.

    Verifica:

    ```bash
    dig CAA tuodominio.xyz +short
    ```

    Su Windows (PowerShell):

    ```powershell
    Resolve-DnsName tuodominio.xyz -Type CAA -Server 8.8.8.8
    ```

> **Se in futuro cambi Name Server o lasci Cloudflare:** prima **togli il DS dal registrar**, aspetta che il TTL scada, e solo dopo cambia i Name Server. Altrimenti il dominio sparisce per i resolver che validano DNSSEC.

<h3 id="opzionale-f">Opzionale F. Zero tracking sul sito e isolamento delle risorse di terze parti (niente cookie banner)</h3>

Per rendere `tuodominio.xyz` conforme al GDPR senza banner dei cookie e senza cedere a terzi i dati dei visitatori:

- **Niente Google Fonts da CDN esterno.** Non caricare mai font da `fonts.googleapis.com` o `fonts.gstatic.com` (trasmettono l'indirizzo IP di ogni visitatore a Google). Scarica i file `.woff2` e ospitali direttamente in una cartella `/fonts` dentro il tuo repository GitHub.
- **Niente librerie JS da CDN esterni.** Evita link a `cdnjs`, `unpkg` o `jsdelivr`; salva gli script localmente nel repository.
- **Statistiche senza tracciamento.** Se vuoi sapere quante visite riceve il sito senza usare Google Analytics, ti basta consultare le statistiche aggregate lato rete già incluse gratuitamente nella dashboard di Cloudflare (sezione **Analytics & Logs > Traffic**), che non installano alcun cookie né script nel browser dell'utente.

---

*Guida tecnica (edizione privacy avanzata): gen.xyz / Spaceship / Porkbun / Dynadot + Cloudflare + GitHub Pages.*
