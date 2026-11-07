---
title: "Installare Bazzite sul OneXPlayer 1S: guida passo passo"
date: 2026-11-07
tags: [bazzite, linux, handheld, onexplayer, gaming, installazione, guida]
description: Guida passo passo per installare Bazzite sul OneXPlayer 1S (8.4", i7-1195G7, Iris Xe), con la correzione dello schermo nero, il passaggio al desktop, i giochi Epic con Heroic e i rollback.
---

Guida passo passo, aggiornata al 7 novembre 2026 dopo un'installazione reale: dalla preparazione di Windows fino ai giochi Epic nella Steam Gaming Mode.

**In questa guida**

1. [Verifica i requisiti](#requisiti) (1.1)
2. [Prepara Windows e il materiale](#preparazione) (2.1–2.5)
3. [Scarica l'immagine e crea la chiavetta](#chiavetta) (3.1–3.3)
4. [BIOS e avvio da USB](#bios) (4.1–4.3)
5. [Installa Bazzite](#installazione) (5.1–5.5)
6. [Primo avvio](#primo-avvio) (6.1–6.7, compresa la correzione dello schermo nero)
7. [Configura l'handheld](#handheld) (7.1–7.7, compresa la sincronizzazione di Google Drive)
8. [Giochi nella Gaming Mode: Epic e visual novel](#epic) (8.1–8.6)
9. [Previeni i problemi futuri](#prevenzione) (9.1–9.7)
10. [Problemi noti e rollback](#problemi-noti-e-rollback)
11. [Cosa non è verificato](#non-verificato)
12. [Fonti principali](#fonti)

| Modello | CPU / GPU | RAM | Disco |
|---|---|---|---|
| OneXPlayer 1S, 8.4" IPS | i7-1195G7 / Iris Xe | 16 GB | 1 TB NVMe |

> **Da sapere prima.** Bazzite si installa su questo dispositivo, ma **senza supporto ufficiale**.
>
> - La pagina ufficiale sui OneXPlayer documenta solo il modello X1.
> - La grafica Iris Xe non è tra le GPU indicate per la Steam Gaming Mode (sono indicate GPU AMD moderne e Intel Arc).
> - Al primo avvio la Gaming Mode parte con lo schermo nero. Si risolve con una correzione manuale dalla console, descritta ai passaggi 6.2 e 6.3, verificata su questo dispositivo.
> - Anche il passaggio al desktop dal menu di Steam non funziona subito: la soluzione è al passaggio 6.6.
>
> Fonti: [OneXPlayer Handhelds](https://docs.bazzite.gg/Handheld_and_HTPC_edition/Handheld_Wiki/OneXPlayer_Handhelds/), [Hardware Compatibility for Gaming](https://docs.bazzite.gg/Gaming/Hardware_compatibility_for_gaming/), [issue #6240](https://github.com/ublue-os/bazzite/issues/6240).

Accanto a ogni passaggio trovi l'indicazione di quanto è affidabile: **Verificato** (provato su questo dispositivo o confermato dalla documentazione ufficiale), **Non verificato** o **Facoltativo**.

---

<h2 id="requisiti">1. Verifica i requisiti</h2>

Prima di toccare il dispositivo, controlla che l'hardware soddisfi i requisiti ufficiali.

### 1.1 Confronta l'hardware con i requisiti minimi

*Verificato.*

Requisiti ufficiali di Bazzite e situazione del tuo dispositivo:

- **Firmware UEFI.** Il boot CSM/Legacy non è supportato.
- **CPU quad-core da 2 GHz e 8 GB di RAM.** Il i7-1195G7 e i 16 GB li superano.
- **GPU con Vulkan 1.3 o superiore.** Intel indica Vulkan 1.3 per la Iris Xe, ma con i driver Windows. Su Linux lo controllerai al passaggio 6.4.
- **Almeno 50 GB liberi su SSD interno** (consigliati 120 GB).
- **Disco in formato GPT.** L'installazione su un disco MBR fallisce.

Fonti: [Hardware Compatibility for Gaming](https://docs.bazzite.gg/Gaming/Hardware_compatibility_for_gaming/), Intel, articolo di supporto 000005524 "Supported APIs for Intel Graphics", [specifiche OneXPlayer 1S](https://onexplayer.bg/en/onexplayer_1s_spec).

---

<h2 id="preparazione">2. Prepara Windows e il materiale</h2>

Questi passaggi si fanno ancora in Windows. Anche se poi sostituisci Windows, servono a non perdere dati e licenza.

### 2.1 Fai il backup dei dati

*Verificato.*

Copia su un disco esterno o nel cloud tutto ciò che vuoi tenere: documenti, salvataggi dei giochi non sincronizzati, foto. La guida ufficiale lo chiede prima di procedere.

Fonte: [Installation Guide](https://docs.bazzite.gg/General/Installation_Guide/install-guide/).

### 2.2 Metti al sicuro licenza Windows e driver

*Non documentato da Bazzite.*

- Collega la licenza Windows al tuo account Microsoft e annota il product key. Di solito su questi dispositivi la licenza è legata all'hardware, ma per il tuo modello non l'ho verificato.
- Se un giorno vorrai tornare a Windows, DROIX distribuisce i driver del OneXPlayer 1S estratti da un'unità di serie.
- In Bazzite non servono driver aggiuntivi: sono integrati nel kernel che arriva con l'immagine.

Fonti: [DROIX, driver OneXPlayer](https://droix.net/blogs/onexplayer-downloads-drivers-faq/), [FAQ Bazzite](https://docs.bazzite.gg/General/FAQ/).

### 2.3 Disattiva BitLocker

*Verificato.*

In Windows apri *Impostazioni → Privacy e sicurezza → Crittografia dispositivo* (o *Gestione BitLocker* dal Pannello di controllo) e disattiva la crittografia. Prima annota la chiave di ripristino.

Fonte: [guida handheld ufficiale](https://docs.bazzite.gg/General/Installation_Guide/Installing_Bazzite_for_Handheld_PCs/).

### 2.4 Disattiva l'Avvio rapido di Windows

*Verificato.*

1. Apri *Pannello di controllo → Opzioni risparmio energia → Specifica comportamento pulsanti di alimentazione*.
2. Clicca *Modifica le impostazioni attualmente non disponibili* e togli la spunta da *Attiva avvio rapido*.
3. Spegni il dispositivo con un normale arresto, non con l'ibernazione.

Bazzite avverte che l'Avvio rapido può bloccare alcuni componenti, come il Wi-Fi.

Fonte: [Common Issues & Resolutions](https://docs.bazzite.gg/General/issues_and_resolutions/).

### 2.5 Procura il materiale

*Verificato.*

- **Chiavetta USB da almeno 16 GB**, meglio USB 3.0 per evitare che si surriscaldi.
- **Tastiera USB fisica.** Serve per digitare la password della chiave Secure Boot e, se attivi la cifratura, a ogni avvio.
- **Hub o adattatore USB-C**, per collegare insieme chiavetta e tastiera.

Fonti: [Installation Guide](https://docs.bazzite.gg/General/Installation_Guide/install-guide/), [Troubleshooting Guide](https://docs.bazzite.gg/General/Installation_Guide/troubleshoot_guide/).

---

<h2 id="chiavetta">3. Scarica l'immagine e crea la chiavetta</h2>

### 3.1 Scegli l'immagine giusta

*Scelta consigliata.*

Sul sito ufficiale scegli **Device: Handheld** e poi **Desktop: GNOME**. Per gli handheld il sito non chiede la GPU: la scelta "Handheld" porta già a un'immagine con Steam Gaming Mode. Nella scheda *New Users* compare il pulsante **Download bazzite-deck-gnome**: è quello da usare.

> **Usa l'installer normale.** Sotto il pulsante principale c'è anche il "Legacy installer". Il sito avverte che verrà dismesso presto e consiglia l'installer normale.

Per riferimento, le immagini disponibili:

| Immagine | Cosa offre | Per te |
|---|---|---|
| `bazzite-deck-gnome` | Steam Gaming Mode + desktop GNOME | **Consigliata.** È l'unica con Gaming Mode funzionante documentata su un OneXPlayer Intel Tiger Lake. |
| `bazzite-deck` | Steam Gaming Mode + desktop KDE | Plausibile con la stessa correzione, non verificata. |
| `bazzite` | Solo desktop KDE | Ripiego se la Gaming Mode non funziona: Steam si avvia in Big Picture. |
| `bazzite-gnome` | Solo desktop GNOME | Ripiego alternativo. |

Puoi cambiare immagine anche dopo, con un rebase (vedi [Problemi noti e rollback](#problemi-noti-e-rollback)).

Fonti: [bazzite.gg](https://bazzite.gg/), [FAQ Bazzite](https://docs.bazzite.gg/General/FAQ/), [issue #6240](https://github.com/ublue-os/bazzite/issues/6240).

### 3.2 Scarica la ISO e verifica il checksum

*Verificato.*

Scarica la ISO con il pulsante **Download bazzite-deck-gnome**. Accanto al pulsante ci sono le icone per la verifica del file: da lì ottieni lo SHA256 pubblicato. Poi confrontalo con quello del file scaricato, da PowerShell (sostituisci il nome con quello del file scaricato):

```powershell
Get-FileHash .\nome-del-file.iso -Algorithm SHA256
```

Fonte: [Installation Guide](https://docs.bazzite.gg/General/Installation_Guide/install-guide/).

### 3.3 Scrivi la chiavetta con Rufus

*Strumento ufficiale.*

Rufus è tra gli strumenti indicati dalla guida ufficiale di Bazzite, ma la documentazione non dice quali impostazioni usare. Quelle qui sotto derivano dai requisiti di Bazzite e dalle indicazioni dell'autore di Rufus. Tra parentesi trovi l'etichetta inglese, se Rufus è in inglese.

1. Scarica Rufus dal sito ufficiale [rufus.ie](https://rufus.ie/) e avvialo. Collega la chiavetta: il suo contenuto verrà cancellato.
2. **Dispositivo** (*Device*): seleziona la chiavetta. Controlla bene di non scegliere un disco esterno con dati.
3. **Selezione boot** (*Boot selection*): "Disco o immagine ISO", poi **SELEZIONA** e scegli il file `bazzite-deck-gnome` scaricato.
4. **Schema partizione e sistema destinazione**: se sono modificabili, scegli **GPT** e **UEFI (non CSM)**, perché Bazzite non supporta l'avvio Legacy/CSM. Se sono grigi, lasciali così (vedi la nota qui sotto).
5. **Etichetta volume, file system e dimensione cluster**: lascia i valori proposti da Rufus.
6. Premi **AVVIA** (*START*). Se Rufus chiede in che modalità scrivere l'immagine, scegli la **modalità immagine ISO** (*ISO Image mode*), quella consigliata da Rufus.
7. Conferma l'avviso di cancellazione e attendi la fine. Poi espelli la chiavetta in modo sicuro.

> **Opzioni grigie? È normale.** Con la ISO di Bazzite Rufus 4.15 blocca schema partizione, sistema destinazione, file system ed etichetta (mostrando MBR, BIOS o UEFI CSM, FAT32). Significa che scriverà l'immagine in modalità DD, come copia esatta della ISO: la chiavetta riceve la partizione di avvio UEFI già presente nella ISO e i valori mostrati non vengono applicati. Lascia tutto così e premi AVVIA. Dopo la scrittura Windows potrebbe proporti di formattare la chiavetta: non farlo.

> **Se la chiavetta non si avvia.** Riscrivila scegliendo la **modalità immagine DD** (*DD Image mode*), che copia la ISO byte per byte. L'autore di Rufus consiglia di provare prima la modalità ISO e passare alla DD solo in caso di problemi. Un utente Bazzite riporta di aver installato con la modalità DD. In modalità DD le opzioni di schema partizione vengono ignorate, ed è normale.

> **Evita Ventoy.** La guida attuale lo ammette con passaggi extra per il Secure Boot, mentre le guide precedenti lo sconsigliavano del tutto. L'alternativa consigliata dalla guida ufficiale è Fedora Media Writer.

Fonti: [Installation Guide](https://docs.bazzite.gg/General/Installation_Guide/install-guide/), [autore di Rufus su ISO e DD mode](https://github.com/pbatard/rufus/issues/843), [utente Bazzite con DD mode](https://www.answeroverflow.com/m/1427413230900351016).

---

<h2 id="bios">4. BIOS e avvio da USB</h2>

Collega hub, chiavetta e tastiera al OneXPlayer prima di accenderlo.

### 4.1 Entra nel BIOS

*Non ufficiale per l'8.4".*

Nessun manuale ufficiale copre l'8.4" 1S. Prova queste combinazioni, con la tastiera USB collegata:

- Premi ripetutamente <kbd>ESC</kbd> sulla tastiera all'accensione (FAQ ufficiale OneXPlayer, scritta per il Mini Intel 1195G7).
- Tieni premuti il **pulsante arancione sinistro** e <kbd>Volume +</kbd> mentre accendi (wiki della community).

Fonti: [FAQ OneXPlayer](https://onexplayerstore.com/pages/faqs), [OneXPlayer wiki](https://onexplayer.fandom.com/wiki/Linux).

### 4.2 Controlla le impostazioni del BIOS

*Da controllare.*

- **CSM / Legacy:** deve restare disattivato. Il nuovo installer potrebbe non avviarsi in modalità Legacy.
- **Secure Boot:** puoi lasciarlo attivo. Registrerai la chiave di Bazzite al passaggio 6.1.
- **Intel VMD / RST:** non ho trovato fonti che dicano se il 1S lo ha attivo di fabbrica. Se all'installazione l'SSD da 1 TB non compare, cerca qui un'opzione VMD o RST e disattivala.
- **Fast Boot del BIOS:** la documentazione Bazzite non ne parla. Disattivarlo rende più facile entrare nei menu, ma non è un requisito.

> **Attenzione al dual boot.** Se Windows è installato con VMD attivo, disattivare VMD può impedire a Windows di avviarsi.

Fonti: [Troubleshooting Guide](https://docs.bazzite.gg/General/Installation_Guide/troubleshoot_guide/), [Secure Boot](https://docs.bazzite.gg/General/Installation_Guide/secure_boot/), [Intel, VMD](https://www.intel.com/content/www/us/en/support/articles/000088580/memory-and-storage/client-ssds.html).

### 4.3 Avvia dalla chiavetta

*Fonte DROIX.*

1. Accendi il dispositivo.
2. Quando compare il logo, premi insieme <kbd>DESKTOP</kbd> + <kbd>Volume +</kbd>.
3. Nel menu di avvio scegli la chiavetta con il D-Pad e conferma con <kbd>START</kbd>. L'SSD interno compare come "UEFI OS (One-netbook PCI-E 1TB SSD)": non è quello.

Fonte: [DROIX, guida OneXPlayer 1165G7/1185G7/1195G7](https://droix.net/blogs/onexplayer-downloads-drivers-faq/).

---

<h2 id="installazione">5. Installa Bazzite</h2>

Non serve la connessione a Internet per installare.

### 5.1 Prova la sessione live

*Facoltativo.*

La sessione live permette di vedere se schermo, touch e Wi-Fi rispondono prima di installare. Non usarla per giocare: usa un kernel diverso da quello installato.

Già da qui puoi leggere il nome del modello, utile più avanti:

```bash
cat /sys/class/dmi/id/product_name
```

Fonte: [Installation Guide](https://docs.bazzite.gg/General/Installation_Guide/install-guide/).

### 5.2 Imposta lingua, regione e tastiera

Apri l'installer e scegli italiano per lingua, fuso orario e layout di tastiera.

### 5.3 Scegli il disco e il partizionamento

*Verificato.*

**Solo Bazzite.** Seleziona l'SSD interno da 1 TB e usa il **partizionamento automatico**.

> **Cancella tutto.** Questa scelta cancella tutti i dati sul disco selezionato, Windows compreso.

**Dual boot con Windows.**

1. Prima, in Windows, riduci la partizione di Windows con *Gestione disco* per liberare almeno 50 GB (consigliati 120 GB o più).
2. Nell'installer seleziona l'SSD e usa il **partizionamento automatico**, l'unica opzione disponibile nella ISO live: userà lo spazio libero.
3. Dopo l'installazione aggiungerai Windows al menu di avvio (passaggio 6.7).

> **Bug noto dell'installer.** Il pulsante "format as efi" dice che formatterà la partizione EFI di Windows, ma in realtà vi si aggiunge.

> **Alternativa più isolata.** La vecchia guida raccomandava una partizione EFI separata, così gli aggiornamenti di Windows non toccano Bazzite. Oggi richiede la [ISO legacy](https://docs.bazzite.gg/General/Installation_Guide/legacy-install/) con partizionamento manuale, che il sito dichiara in via di dismissione. Il OneXPlayer ha un solo slot M.2: un'altra strada è Windows-to-Go su disco esterno, creato con Rufus.

Non condividere la libreria giochi su una partizione NTFS o exFAT: Bazzite non le supporta per giocare.

Fonti: [Installation Guide](https://docs.bazzite.gg/General/Installation_Guide/install-guide/), [Dual boot](https://deepwiki.com/bazzite-org/docs.bazzite.gg/4.3-dual-boot-and-advanced-partitioning), [Hardware Compatibility](https://docs.bazzite.gg/Gaming/Hardware_compatibility_for_gaming/).

### 5.4 Crea l'utente e decidi sulla cifratura

- Crea utente e password. La guida sconsiglia di attivare l'account root.
- **Cifratura (facoltativa):** richiede la tastiera fisica a ogni avvio, e se perdi la password i dati non si recuperano.

Fonte: [Installation Guide](https://docs.bazzite.gg/General/Installation_Guide/install-guide/).

### 5.5 Avvia l'installazione e riavvia

Avvia l'installazione. Al termine riavvia e rimuovi la chiavetta. Tieni collegata la tastiera: servirà per la chiave Secure Boot e per la console del passaggio 6.2.

---

<h2 id="primo-avvio">6. Primo avvio</h2>

### 6.1 Registra la chiave Secure Boot (MOK)

*Verificato.*

Al riavvio compare una schermata blu, MokManager:

1. Scegli **Enroll MOK**, poi **Continue**.
2. Inserisci la password `universalblue`.
3. Conferma e riavvia.

> **Due trappole.** La schermata usa sempre il layout inglese QWERTY, e i caratteri digitati non vengono mostrati.

**Se la schermata non compare** o vedi l'errore "bad shim signature", segui il metodo alternativo:

1. Disattiva Secure Boot nel BIOS e avvia Bazzite.
2. Apri un terminale ed esegui il comando qui sotto, inserendo `universalblue`.
3. Riavvia nel BIOS con `ujust bios`, riattiva Secure Boot.
4. Al riavvio completa **Enroll MOK** con la stessa password.

```bash
ujust enroll-secure-boot-key
```

Un aggiornamento del BIOS può riattivare Secure Boot: in quel caso ripeti il metodo alternativo.

Fonte: [Secure Boot](https://docs.bazzite.gg/General/Installation_Guide/secure_boot/).

### 6.2 Se lo schermo resta nero, apri la console

*Verificato su questo dispositivo.*

Dopo il logo di Bazzite parte la Gaming Mode. Su questo modello lo schermo interno resta nero, anche se si sentono i suoni dell'interfaccia di Steam. Su questo dispositivo anche uno schermo esterno via USB-C è rimasto nero. Per applicare la correzione serve quindi la console testuale:

1. Con la tastiera USB collegata, premi <kbd>Ctrl</kbd> + <kbd>Alt</kbd> + <kbd>F3</kbd>. Se non succede nulla, prova <kbd>F2</kbd> o <kbd>F4</kbd>. Su una tastiera compatta può servire anche <kbd>Fn</kbd>.
2. Accedi con il nome utente e la password creati durante l'installazione. Mentre digiti la password non compare nulla: è normale.

> **Com'è fatta la console.**
>
> - Il testo appare ruotato, perché il pannello è montato in verticale: tieni il dispositivo in verticale per leggerlo. I comandi di rotazione della console non hanno effetto.
> - Non si può scorrere all'indietro. Per leggere un output lungo aggiungi `| less` in fondo al comando: scorri con le frecce ed esci con <kbd>q</kbd>.
> - Per uscire scrivi `exit`. Per tornare alla schermata grafica premi <kbd>Ctrl</kbd> + <kbd>Alt</kbd> + <kbd>F1</kbd> (o <kbd>F2</kbd>).

Fonti: [issue #6240](https://github.com/ublue-os/bazzite/issues/6240), [forum Universal Blue](https://universal-blue.discourse.group/t/gaming-mode-black-screen/1963), [Phoronix, scorrimento console](https://www.phoronix.com/news/Linux-5.9-Drops-Soft-Scrollback).

### 6.3 Applica la correzione dello schermo nero

*Verificato su questo dispositivo.*

Su Tiger Lake il display engine non riesce a ruotare di 90° le immagini compresse, e il pannello del OneXPlayer è montato in verticale. Nella console esegui, premendo Invio dopo ogni riga:

```bash
mkdir -p ~/.config/environment.d
echo "INTEL_DEBUG=norbc" >> ~/.config/environment.d/10-gamescope-session.conf
cat ~/.config/environment.d/10-gamescope-session.conf
```

L'ultimo comando deve mostrare la riga `INTEL_DEBUG=norbc`. Poi riavvia:

```bash
systemctl reboot
```

Al riavvio la Gaming Mode compare sullo schermo interno, nel verso giusto.

> **Se non basta.** Su un altro Tiger Lake (GPD Win 3) ha funzionato aggiungere `--force-composition-rotation` al comando di gamescope ([issue #6156](https://github.com/ublue-os/bazzite/issues/6156)). Non è verificato sul OneXPlayer.

Fonte: [issue #6240](https://github.com/ublue-os/bazzite/issues/6240).

### 6.4 Controlla nome del modello e versione Vulkan

*Facoltativo.*

Puoi farlo nella stessa console, prima di riavviare.

```bash
cat /sys/class/dmi/id/product_name
```

Su questo dispositivo risponde `ONE XPLAYER`: lo stesso nome del modello dell'issue #6240.

```bash
vulkaninfo | grep 'Instance Version'
```

Su questo dispositivo risponde `1.4.350`, sopra il requisito di 1.3. Le righe WARNING che compaiono prima si possono ignorare.

Fonti: [device-quirks](https://github.com/hhd-dev/bazzite-dc/blob/master/device-quirks), [Hardware Compatibility](https://docs.bazzite.gg/Gaming/Hardware_compatibility_for_gaming/).

### 6.5 Accedi a Steam

Con lo schermo funzionante, accedi con il tuo account Steam e riavvia dal menu di accensione di Steam.

Fonte: [guida handheld ufficiale](https://docs.bazzite.gg/General/Installation_Guide/Installing_Bazzite_for_Handheld_PCs/).

### 6.6 Fai funzionare il passaggio al desktop

*Verificato su questo dispositivo.*

Su questo dispositivo *Passa al desktop* dal menu di Steam fa diventare nero lo schermo e riporta alla Gaming Mode. È un problema noto, segnalato su altri handheld con la stessa sessione di gioco (`gamescope-session-ogui-steam`). Si risolve dalla console (<kbd>Ctrl</kbd> + <kbd>Alt</kbd> + <kbd>F3</kbd>):

1. Indica a Steam quale desktop avviare. Se non sei sicuro del nome, controllalo con `ls /usr/share/wayland-sessions/`.

        steamosctl set-default-desktop-session gnome.desktop

2. Imposta il desktop come modalità di avvio e riavvia:

        steamosctl set-default-login-mode desktop
        systemctl reboot

> **Non riavviare solo SDDM.** Un workaround segnalato online suggerisce `sudo systemctl restart sddm` al posto del riavvio. Su questo dispositivo ha bloccato la console. Se succede, tieni premuto il pulsante di accensione per circa 10 secondi e riaccendi: al riavvio parte il desktop.

**Per tornare alla Gaming Mode** (le modalità ammesse sono solo `game` e `desktop`):

```bash
steamosctl switch-to-game-mode
```

Passa subito alla Gaming Mode, senza cambiare la modalità di avvio.

```bash
steamosctl set-default-login-mode game
```

Rimette la Gaming Mode come modalità di avvio. Si applica al riavvio successivo.

Con `steamosctl get-default-login-mode` vedi quale modalità è impostata. Attento a scrivere bene `steamosctl`: un errore di battitura dà "command not found".

Fonti: [issue #6199](https://github.com/ublue-os/bazzite/issues/6199), [issue #6039](https://github.com/ublue-os/bazzite/issues/6039), [DeepWiki, selezione sessione](https://deepwiki.com/ublue-os/bazzite/9.2-audio-configuration-and-virtual-channels).

### 6.7 Aggiungi Windows al menu di avvio (solo dual boot)

*Solo dual boot.*

```bash
ujust regenerate-grub
```

Aggiunge Windows al menu GRUB.

```bash
ujust setup-boot-windows-steam
```

Facoltativo: crea in Steam una voce che riavvia in Windows.

Fonte: [comandi ujust](https://docs.bazzite.gg/Installing_and_Managing_Software/ujust/).

---

<h2 id="handheld">7. Configura l'handheld</h2>

### 7.1 Sistema orientamento e scala nel desktop

Se al primo avvio il desktop GNOME ha orientamento o scala sbagliati, correggili in *Impostazioni → Schermi*. Su un OneXPlayer Intel GNOME risulta già nel verso giusto. In alternativa, dal Terminale:

```bash
gdctl show
```

Mostra il nome dello schermo interno, di solito `eDP-1`.

```bash
gdctl set --logical-monitor --primary --monitor eDP-1 --transform 90
```

Se l'immagine è capovolta usa `270`. Aggiungi `--persistent` dopo `set` per mantenerla. Scollega prima gli schermi esterni.

Per duplicare lo schermo su un monitor esterno premi <kbd>Super</kbd> + <kbd>P</kbd> più volte finché compare il mirror.

Fonti: [guida handheld](https://docs.bazzite.gg/General/Installation_Guide/Installing_Bazzite_for_Handheld_PCs/), [gdctl](https://www.mankier.com/1/gdctl), [GNOME, Super+P](https://gitlab.gnome.org/GNOME/gnome-control-center/-/issues/1748).

### 7.2 Prova i controlli integrati

*Da provare.*

Bazzite gestisce i controlli degli handheld con InputPlumber, che ha un profilo per i OneXPlayer Intel. Le sue regole riconoscono il nome "ONE XPLAYER", che è quello riportato da questo dispositivo, quindi i controlli dovrebbero essere riconosciuti. Che funzionino tutti non è ancora verificato.

- **Menu rapido (QAM):** pulsante <kbd>Turbo</kbd>. Sui modelli più vecchi potrebbe non funzionare: usa <kbd>Guide</kbd> + <kbd>B</kbd>, che funziona sempre. Da tastiera: <kbd>Ctrl</kbd> + <kbd>2</kbd>.
- **Overlay di OpenGamepadUI:** tieni premuto <kbd>Guide</kbd> e premi QAM.
- **Giroscopio:** se non va, in OpenGamepadUI imposta l'emulazione `deck-uhid`.
- **Desktop Mode:** il controller si usa come mouse da *Steam → Impostazioni → Controller → Layout desktop*.

Se i controlli non vanno, apri una segnalazione su [GitHub](https://github.com/ublue-os/bazzite/issues) citando l'issue #6240.

Fonti: [Handheld Wiki](https://docs.bazzite.gg/Handheld_and_HTPC_edition/Handheld_Wiki/), [InputPlumber](https://shadowblip.github.io/InputPlumber/usage/), [note ChimeraOS](https://github.com/ChimeraOS/chimeraos/wiki/Release-Notes).

### 7.3 Scegli un solo metodo per il TDP

*Non verificato sul 1S.*

Le strade possibili sono tre. Usane una sola alla volta, come raccomanda la documentazione:

1. menu rapido di Steam, icona fulmine, sezione TDP (solo se il dispositivo è gestito da SteamOS Manager);
2. OpenGamepadUI / PowerStation;
3. un plugin Decky, come SimpleDeckyTDP.

Non ho trovato conferme che il TDP del 1S Intel sia regolabile in Bazzite.

Fonte: [Handheld Wiki](https://docs.bazzite.gg/Handheld_and_HTPC_edition/Handheld_Wiki/).

### 7.4 Installa Decky Loader

*Facoltativo.*

```bash
ujust setup-decky
```

Decky si apre dal menu rapido. Può rompersi o disinstallarsi dopo un aggiornamento: in quel caso ripeti il comando.

Fonte: [Handheld Wiki](https://docs.bazzite.gg/Handheld_and_HTPC_edition/Handheld_Wiki/).

### 7.5 Aggiorna e blocca la versione funzionante

*Verificato.*

Sulle immagini Deck gli aggiornamenti automatici sono spenti. Aggiorna con l'app Bazzite Updater (usabile col controller) oppure:

```bash
ujust update
```

Aggiorna sistema, app Flatpak e container. Serve almeno il 3% di spazio libero.

Quando tutto funziona, blocca questa versione: la trovi al passaggio 9.2. Le app si installano da **Bazaar**. Con `ujust --choose` vedi tutti i comandi di configurazione. Evita `rpm-ostree install`: può bloccare gli aggiornamenti.

Fonti: [Update Guide](https://docs.bazzite.gg/Installing_and_Managing_Software/Updates_Rollbacks_and_Rebasing/updating_guide/), [rpm-ostree](https://docs.bazzite.gg/Installing_and_Managing_Software/rpm-ostree/).

### 7.6 Installa Mullvad VPN

*Facoltativo.*

Mullvad non ha una versione Flatpak ufficiale, quindi va aggiunto al sistema con `rpm-ostree`. La documentazione di Bazzite sconsiglia questo metodo perché può bloccare gli aggiornamenti: per questo il primo passo è bloccare la versione attuale. Esegui i comandi dal Terminale del desktop.

1. Blocca la versione del sistema in uso, così puoi tornare indietro (vedi 9.2):

        sudo ostree admin pin 0

2. Aggiungi il repository ufficiale di Mullvad. Prima controlla che l'indirizzo corrisponda a quello indicato per Fedora nelle istruzioni ufficiali di Mullvad sul sito mullvad.net:

        curl -fsSL https://repository.mullvad.net/rpm/stable/mullvad.repo | sudo tee /etc/yum.repos.d/mullvad.repo

3. Installa l'app e riavvia:

        rpm-ostree install mullvad-vpn
        systemctl reboot

4. Attiva il servizio di Mullvad, che dopo l'installazione resta spento:

        sudo systemctl enable --now mullvad-daemon.service

5. Apri l'app **Mullvad VPN** dal menu delle applicazioni e inserisci il numero di account. Se vuoi che si connetta da sola, attiva la connessione automatica nelle impostazioni dell'app.

> **Da sapere.** La VPN gira come servizio di sistema, quindi dovrebbe restare attiva anche in Gaming Mode. L'app grafica si apre solo dal desktop. Se un aggiornamento di Bazzite fallisce per colpa del pacchetto aggiunto, disinstallalo con `rpm-ostree uninstall mullvad-vpn` e riavvia.

Fonti: [Adding Mullvad to Bazzite](https://zegnat.bearblog.dev/adding-mullvad-to-bazzite/), [Fedora Discussion](https://discussion.fedoraproject.org/t/howto-install-mullvadvpn-browser-on-fedora-atomic-desktops/125749), [Mullvad issue #5639](https://github.com/mullvad/mullvadvpn-app/issues/5639), [rpm-ostree](https://docs.bazzite.gg/Installing_and_Managing_Software/rpm-ostree/).

### 7.7 Sincronizza Google Drive con rclone

*Facoltativo. Non verificato su questo dispositivo.*

Per avere una copia locale di Google Drive (tutto «Il mio Drive» e, se vuoi, anche cartelle condivise con te), modificabile in entrambe le direzioni, la soluzione adatta è **rclone** con la funzione **bisync**: tiene allineata una cartella locale con una cartella di Drive in entrambi i sensi e può girare in automatico a intervalli regolari. Va bene per quantità di dati contenute (qui meno di 10 GB) e con un account Google gratuito.

> **Due avvertenze.**
>
> - **bisync è ancora in beta.** La documentazione la definisce una funzione avanzata da usare con cautela. Per questo il primo giro si fa in prova, con `--dry-run`.
> - **I documenti nativi di Google** (Documenti, Fogli, Presentazioni) **non si sincronizzano bene:** hanno dimensione −1 e nessun checksum, quindi si escludono con `--drive-skip-gdocs`. I file normali (PDF, Word, immagini e simili) si sincronizzano senza problemi.

> **Perché non l'account Google di GNOME.** Gli *Account online* di GNOME mostrano Drive solo online, senza una copia locale, quindi non servono a questo scopo.

**1. Solo per le cartelle condivise con te: prepara gli ID.** Tutto «Il mio Drive» si sincronizza senza ID. Servono solo per le cartelle che altri hanno condiviso con te, perché non fanno parte di «Il mio Drive». Per poter rimandare su Drive le tue modifiche devi essere **Editor** di queste cartelle. Se non ne hai, salta questo passo. Apri ogni cartella condivisa nel browser su `drive.google.com` (se è condivisa con te, la trovi in *Condivisi con me*: entraci con un doppio clic). L'ID è la parte dell'indirizzo dopo `/folders/`, senza eventuali code come `?usp=sharing`. Per esempio, in questo indirizzo:

```
https://drive.google.com/drive/folders/1AbCdEfGhIjKlMnOpQrStUvWxYz012345
```

l'ID è `1AbCdEfGhIjKlMnOpQrStUvWxYz012345`. Annotali.

**2. Installa rclone.** Dal Terminale controlla se c'è già:

```bash
rclone version
```

Se risponde "command not found", installalo con Homebrew, che su Bazzite è disponibile (meglio di `rpm-ostree install`, che può bloccare gli aggiornamenti):

```bash
brew install rclone
```

**3. Crea il tuo client id Google.** Il client id condiviso di rclone sta per essere ritirato: Google farà pagare le richieste fatte con quello integrato e rclone lo disattiverà nel corso del 2026 (l'annuncio parla di 90 giorni di preavviso, senza una data certa). Perciò conviene crearne uno proprio fin dall'inizio; è gratuito. I passaggi sotto sono quelli della documentazione rclone: i nomi dei menu nella console Google possono differire un po'.

1. Accedi alla [Google API Console](https://console.cloud.google.com/) con il tuo account Google e crea un progetto (*Select a project* > *New project*).
2. In *Enable APIs and services* cerca "Drive" e abilita **Google Drive API**.
3. Apri *Credentials* dal pannello a sinistra. Non usare "Create credentials": apre una procedura guidata. Clicca invece su **Configure consent screen** > **Get started**.
4. Inserisci un nome per l'applicazione (va bene "rclone") e la tua email di assistenza. In *Audience* scegli **External**, inserisci l'email di contatto, accetta i termini e clicca su **Create**.
5. In *Data Access* scegli *Add or remove scopes* (o *Manually add scopes*), aggiungi questi scope e salva: `https://www.googleapis.com/auth/docs`, `https://www.googleapis.com/auth/drive` e, facoltativo, `https://www.googleapis.com/auth/drive.metadata.readonly`.
6. In *Audience* clicca su **+ Add users**, aggiungi il tuo account Google e salva (utente di prova).
7. In *Overview* clicca su **Create OAuth client**, scegli il tipo di applicazione **Desktop app** e clicca su **Create**. Annota **client ID** e **client secret**.
8. In *Audience* clicca su **Publish app** e conferma. Se il pulsante è grigio, compila prima *Branding* (pagina iniziale, informativa sulla privacy, dominio autorizzato), salva e torna in *Audience*.

Se lasci l'app in stato "Testing" funziona, ma l'autorizzazione scade dopo circa una settimana e la sincronizzazione automatica si ferma: per questo si pubblica l'app.

**4. Collega il tuo account Google.**

```bash
rclone config
```

Rispondi così:

- `n` (nuovo remote);
- nome: `gdrive`;
- `Storage` (il tipo di servizio): scrivi `drive` (Google Drive) oppure il numero accanto a «Google Drive» nell'elenco;
- `client_id` e `client_secret`: incolla quelli creati al passo 3;
- scope: `1` (accesso completo);
- `service_account_file`: lascia vuoto e premi Invio (serve solo per gli account di servizio);
- impostazioni avanzate (*Edit advanced config*): `n`. In questo caso non ti verrà chiesto il `root_folder_id`: lo passi più avanti a ogni comando con `--drive-root-folder-id`;
- auto config: `y`. Si apre il browser: accedi e autorizza rclone;
- shared drive / team drive: `n`;
- conferma con `y`, poi esci con `q`.

Se avevi già creato il remote `gdrive` lasciando vuoti `client_id` e `client_secret`, aggiornalo con i tuoi (sostituisci i due valori) e ricollegalo, rispondendo `y` alla richiesta di aggiornare il token: senza questo passo rclone continua a usare il client id condiviso.

```bash
rclone config update gdrive client_id TUO_CLIENT_ID client_secret TUO_CLIENT_SECRET
rclone config reconnect gdrive:
```

**5. Primo allineamento.** Prima controlla quanto pesa il tuo Drive (esclusi i documenti nativi di Google) e che sul disco ci sia abbastanza spazio:

```bash
rclone size gdrive: --drive-skip-gdocs
```

Poi, per tutto «Il mio Drive»:

```bash
mkdir -p ~/GoogleDrive
rclone bisync ~/GoogleDrive gdrive: --drive-skip-gdocs --create-empty-src-dirs --resilient --recover --conflict-resolve newer --resync --dry-run -v
```

- Leggi il risultato: deve elencare i file da copiare **verso** la cartella locale.
- Se va bene, ripeti lo stesso comando **senza** `--dry-run`.
- `--resync` serve **solo** per questo primo giro. Se lo usi sempre, i file cancellati ricompaiono.

**Cartelle condivise con te (facoltativo).** Non stanno in «Il mio Drive», quindi si sincronizzano a parte, con l'ID del passo 1 e con una cartella locale **fuori** da `~/GoogleDrive`, per non far sovrapporre le due sincronizzazioni (qui `Progetto` è un nome di esempio e `ID_CARTELLA` va sostituito con l'ID vero):

```bash
mkdir -p ~/GoogleDrive-condivise/Progetto
rclone bisync ~/GoogleDrive-condivise/Progetto gdrive: --drive-root-folder-id ID_CARTELLA --drive-skip-gdocs --create-empty-src-dirs --resilient --recover --conflict-resolve newer --resync --dry-run -v
```

Anche qui: leggi il risultato, poi ripeti il comando senza `--dry-run`.

> **Cosa non viene sincronizzato.** Con `--drive-skip-gdocs` restano fuori i documenti nativi di Google (Documenti, Fogli, Presentazioni): se nel tuo Drive sono tanti, non li avrai in locale. I file normali (PDF, Word, immagini e simili) sì.

**6. Sincronizzazione automatica ogni 15 minuti.** Crea lo script `~/.local/bin/drive-sync.sh`, con una riga `rclone bisync` per «Il mio Drive» e, se le usi, una per ogni cartella condivisa:

```bash
#!/bin/bash
export PATH="/home/linuxbrew/.linuxbrew/bin:$PATH"
OPTS="--drive-skip-gdocs --create-empty-src-dirs --resilient --recover --conflict-resolve newer --max-lock 2m --log-file $HOME/.cache/drive-sync.log -v"
rclone bisync "$HOME/GoogleDrive" gdrive: $OPTS
# Facoltativo, una riga per ogni cartella condivisa con te (togli il # all'inizio):
# rclone bisync "$HOME/GoogleDrive-condivise/Progetto" gdrive: --drive-root-folder-id ID_CARTELLA $OPTS
```

Crea il file `~/.config/systemd/user/drive-sync.service`:

```ini
[Unit]
Description=Sincronizza Google Drive

[Service]
Type=oneshot
ExecStart=%h/.local/bin/drive-sync.sh
```

E il file `~/.config/systemd/user/drive-sync.timer`:

```ini
[Unit]
Description=Sincronizza Google Drive ogni 15 minuti

[Timer]
OnBootSec=2min
OnUnitActiveSec=15min

[Install]
WantedBy=timers.target
```

Poi rendi eseguibile lo script e attiva il timer:

```bash
chmod +x ~/.local/bin/drive-sync.sh
systemctl --user daemon-reload
systemctl --user enable --now drive-sync.timer
```

Se qualcosa non va, il registro si trova in `~/.cache/drive-sync.log`.

**Sicurezze già incluse**

- Se in un giro risulta cancellato più del 50% dei file, bisync si ferma senza toccare nulla: è il comportamento predefinito.
- `--resilient` e `--recover` evitano di dover rifare `--resync` dopo errori minori o dopo uno spegnimento improvviso.
- Se lo stesso file viene modificato da entrambe le parti, vince la versione più recente (`--conflict-resolve newer`).

Fonti: [rclone bisync, documentazione](https://git.frostfs.info/satyamisme/rclone/raw/branch/master/docs/content/bisync.md), [rclone Google Drive, documentazione](https://git.frostfs.info/KurlesHS/rclone/raw/commit/cf6d522d2f20bfe0e34f1635e21a1ecaa326a480/docs/content/drive.md), [Bisync of Googledocs on googledrive, forum rclone](https://forum.rclone.org/t/bisync-of-googledocs-on-googledrive/29961), [Syncing all Google Drive folders, owned and shared, forum rclone](https://forum.rclone.org/t/syncing-all-google-drive-folders-owned-and-shared/22661), [annuncio sul ritiro del client id condiviso, forum rclone](https://forum.rclone.org/t/google-drive-and-google-photos-users-action-required/54005).

---

<h2 id="epic">8. Giochi nella Gaming Mode: Epic e visual novel</h2>

Bazzite non integra Epic direttamente. La documentazione consiglia Heroic Games Launcher per i giochi Epic, GOG e Amazon. Tutto questo richiede che la Gaming Mode funzioni (passaggio 6.3).

### 8.1 Installa Heroic da Bazaar

*Verificato.*

Heroic non è preinstallato. Passa al Desktop Mode, apri Bazaar, cerca **Heroic Games Launcher** e installalo. È lo stesso pacchetto pubblicato su [Flathub](https://flathub.org/apps/com.heroicgameslauncher.hgl).

Fonti: [Introduction to Gaming](https://docs.bazzite.gg/Gaming/gaming-intro/), [Installing Software](https://docs.bazzite.gg/Installing_and_Managing_Software/software-intro/), [forum Universal Blue](https://universal-blue.discourse.group/t/is-bazzite-good-for-epic-games/4132).

### 8.2 Accedi a Epic e scarica un gioco

In Heroic scegli *Login → Epic Games*, accedi con il tuo account e installa un gioco dalla libreria.

Fonte: [Heroic Games Launcher](https://github.com/Heroic-Games-Launcher/HeroicGamesLauncher).

### 8.3 Avvialo una prima volta nel Desktop Mode

Molti giochi Epic installano dei prerequisiti al primo avvio, di solito un Visual C++ redistributable o un launcher proprio. Lascia che finiscano prima di tornare alla Gaming Mode.

Fonte: [heldgames](https://heldgames.com/guides/epic-games-steam-deck-heroic).

### 8.4 Porta i giochi nella Gaming Mode

Hai due possibilità, anche combinabili:

- **Un gioco alla volta.** In Heroic apri la pagina del gioco e usa *Add to Steam*.
- **Heroic intero.** In Steam (Desktop Mode) scegli *Aggiungi un gioco → Aggiungi un gioco non di Steam* e seleziona Heroic. Alcuni giochi partono solo da Heroic e non dalle scorciatoie, quindi conviene averlo comunque. Dalla versione 2.21 Heroic ha una modalità console a schermo intero, comoda col controller.

Torna alla Gaming Mode: trovi tutto in *Libreria → Non di Steam*.

Fonti: [guida Epic su Steam Deck](https://colematoyicu.s3.amazonaws.com/how-to-install-and-play-epic-games-on-a-steam-deck.html), [GamingOnLinux](https://www.gamingonlinux.com/2026/04/heroic-games-launcher-gets-a-slick-full-screen-console-like-mode/comment_id=293287).

### 8.5 Imposta i controlli e controlla l'anti-cheat

- I giochi non di Steam non hanno un layout ufficiale: nelle impostazioni controller di Steam scegline uno tra quelli della community.
- I giochi con anti-cheat possono non avviarsi su Linux. Controlla prima su [ProtonDB](https://www.protondb.com/) e [areweanticheatyet.com](https://areweanticheatyet.com/).
- Con la Iris Xe i titoli più pesanti potrebbero girare male: non ho trovato test con questo hardware.

### 8.6 Gioca a una visual novel Ren'Py

*Facoltativo. Non verificato su questo dispositivo.*

Per un gioco fatto con Ren'Py, il modo più semplice è usare la **versione Linux nativa**, aggiunta a Steam come gioco non Steam. Se lo sviluppatore offre solo la versione Windows, si può usare Proton, ma è un ripiego.

1. **Scarica la build Linux** del gioco, di solito un archivio `.tar.bz2` che contiene un file `NomeGioco.sh` e la cartella `lib/`. Estrailo con il gestore file o da terminale:

        tar xjf NomeGioco-linux.tar.bz2

2. **Controlla che sia eseguibile.** Estrarre da un `.zip` con alcuni programmi grafici può far perdere il permesso di esecuzione. In quel caso:

        chmod +x NomeGioco.sh

3. **Aggiungilo a Steam.** Passa al Desktop Mode e in Steam scegli *Giochi → Aggiungi un gioco non di Steam alla mia libreria → Sfoglia*. Cambia il filtro in «Tutti i file» e seleziona `NomeGioco.sh`.
4. **Torna alla Gaming Mode.** Il gioco compare in *Libreria → Non di Steam* e parte a schermo intero.

**Controlli.** Ren'Py supporta già i controller: croce direzionale per muoversi, A per confermare, B per tornare indietro. Il touch nella Gaming Mode funziona come un mouse, quindi puoi anche toccare lo schermo per avanzare. Se un gioco non risponde bene al controller, in Steam scegli un layout della community, per esempio quello con il trackpad come mouse.

**Da tenere d'occhio**

- **Schermo.** Il pannello del OneXPlayer è montato in verticale, ma gamescope lo ruota (passaggio 6.3). Un gioco in 16:9 occupa solo una fascia dello schermo, senza deformarsi.
- **Giochi vecchi.** I Ren'Py 7 più datati possono avere librerie a 32 bit che non partono. In quel caso usa la build Windows: in Steam, *Proprietà → Compatibilità → Forza l'uso di uno specifico strumento di compatibilità Steam Play*, e scegli Proton.
- **Salvataggi.** Con la build nativa stanno in `~/.renpy/NomeGioco/`: ci puoi copiare dentro i salvataggi di un altro computer. Con Proton finiscono invece nel prefisso Proton del gioco.

---

<h2 id="prevenzione">9. Previeni i problemi futuri</h2>

Gli aggiornamenti di Bazzite, del BIOS e di Windows sono i momenti in cui qualcosa può rompersi. Questi passaggi ti lasciano sempre una strada per tornare indietro.

### 9.1 Prepara un kit di emergenza

*Consiglio.*

- **Tieni la chiavetta di installazione** e non riusarla per altro. Se Bazzite non si avvia più, puoi avviare la sessione live da lì. Un utente del forum Universal Blue riporta che la ISO live include anche uno strumento per ripristinare il bootloader.
- **Copia su un disco esterno o nel cloud** il file con la correzione dello schermo. Il file sta nella tua cartella personale, che aggiornamenti e rollback non toccano:

```bash
cat ~/.config/environment.d/10-gamescope-session.conf
```

- **Annota** il nome del modello letto al passaggio 6.4, l'immagine installata e la combinazione di tasti che funziona per BIOS e menu di avvio.

Fonti: [forum Universal Blue](https://universal-blue.discourse.group/t/dual-boot-broken-after-bios-update/12193), [Rollbacks](https://docs.bazzite.gg/Installing_and_Managing_Software/Updates_Rollbacks_and_Rebasing/rolling_back_system_updates/).

### 9.2 Blocca la versione che funziona

*Verificato.*

Bazzite conserva solo 2 versioni del sistema: a ogni aggiornamento cancella la più vecchia. Se ne blocchi una con il pin, non viene mai cancellata.

1. Controlla l'indice della versione in uso (gli indici cambiano dopo ogni aggiornamento):

        rpm-ostree status -v

2. Blocca la versione corrente (indice 0):

        sudo ostree admin pin 0

Quando una versione più nuova ha funzionato bene per un po', puoi sbloccare quella vecchia con `sudo ostree admin pin -u` seguito dal suo indice, così liberi spazio.

Fonte: [Rolling back system updates](https://docs.bazzite.gg/Installing_and_Managing_Software/Updates_Rollbacks_and_Rebasing/rolling_back_system_updates/).

### 9.3 Segui una routine per ogni aggiornamento

*Verificato.*

Sulle immagini Deck gli aggiornamenti automatici sono spenti, quindi decidi tu quando aggiornare. Ogni volta:

1. Controlla di avere almeno il 3% di spazio libero sul disco.
2. Aggiorna da Steam (*Impostazioni → Sistema → Controlla aggiornamenti*), da Bazzite Updater o con `ujust update`.
3. Prima di riavviare, guarda cosa cambia. Il comando mostra le differenze di pacchetti tra la versione attuale e quella in attesa:

        rpm-ostree db diff

4. Riavvia: l'aggiornamento di sistema si applica solo al riavvio.
5. Prova subito Gaming Mode, controlli e un gioco. Se qualcosa non va, torna indietro (vedi [Problemi noti e rollback](#problemi-noti-e-rollback)).
6. Se tutto va bene per qualche giorno, blocca la nuova versione (passaggio 9.2).

Fonte: [Update Guide](https://docs.bazzite.gg/Installing_and_Managing_Software/Updates_Rollbacks_and_Rebasing/updating_guide/).

### 9.4 Tieni il sistema pulito

*Verificato.*

- Installa le app solo da Bazaar. Evita `rpm-ostree install`, salvo i casi senza alternativa come Mullvad (7.6): la documentazione avverte che può bloccare gli aggiornamenti.
- Usa un solo strumento per il TDP alla volta.
- Dopo un aggiornamento, se Decky sparisce, reinstallalo con `ujust setup-decky`.
- Non tenere la libreria giochi su partizioni NTFS o exFAT.

Fonti: [rpm-ostree](https://docs.bazzite.gg/Installing_and_Managing_Software/rpm-ostree/), [Handheld Wiki](https://docs.bazzite.gg/Handheld_and_HTPC_edition/Handheld_Wiki/), [Hardware Compatibility](https://docs.bazzite.gg/Gaming/Hardware_compatibility_for_gaming/).

### 9.5 Dopo un aggiornamento del BIOS, controlla Secure Boot

*Da ricordare.*

Un aggiornamento del BIOS può riattivare Secure Boot o ripristinare le impostazioni, e Bazzite può non avviarsi più. Per controllare che la chiave di Bazzite sia ancora registrata (elenca le chiavi MOK registrate):

```bash
sudo mokutil -l
```

Se Bazzite non parte più, disattiva Secure Boot nel BIOS, avvia Bazzite e registra di nuovo la chiave con il metodo alternativo del passaggio 6.1. Un utente del forum ha risolto proprio così un blocco dopo un aggiornamento del BIOS.

Fonti: [Secure Boot](https://docs.bazzite.gg/General/Installation_Guide/secure_boot/), [guida dual boot del forum](https://universal-blue.discourse.group/t/dual-boot-preliminary-setup-and-post-setup-guide/2743), [segnalazione sul forum](https://universal-blue.discourse.group/t/dual-boot-broken-after-bios-update/12193).

### 9.6 Dopo un aggiornamento di Windows, controlla l'avvio (solo dual boot)

*Solo dual boot.*

- Se il dispositivo avvia direttamente Windows, nel BIOS rimetti Bazzite davanti a Windows Boot Manager nell'ordine di avvio.
- Se la voce di Windows sparisce dal menu GRUB, rigenerala:

```bash
ujust regenerate-grub
```

Un utente del forum segnala che un aggiornamento di Windows con Secure Boot attivo può impedire l'avvio di versioni vecchie di GRUB. Tenere Bazzite aggiornato riduce il rischio.

Fonte: [guida dual boot del forum Universal Blue](https://universal-blue.discourse.group/t/dual-boot-preliminary-setup-and-post-setup-guide/2743).

### 9.7 Segui la segnalazione sullo schermo nero

*Consiglio.*

Apri l'[issue #6240](https://github.com/ublue-os/bazzite/issues/6240) e, con un account GitHub, usa *Subscribe* per ricevere notifiche. Saprai quando la correzione viene integrata nell'immagine o se gli sviluppatori propongono un'altra soluzione.

---

<h2 id="problemi-noti-e-rollback">Problemi noti e rollback</h2>

### Problemi noti

- **Gaming Mode nera su Tiger Lake:** correzione al passaggio 6.3. L'issue è ancora aperta e la correzione non è integrata nell'immagine.
- **"Passa al desktop" riporta alla Gaming Mode:** soluzione al passaggio 6.6. Le segnalazioni sono ancora aperte.
- **Crash della Iris Xe in alcuni giochi** (`VK_ERROR_DEVICE_LOST`, segnalato in CS2): prova l'opzione di avvio Steam `INTEL_DEBUG=stall %command%`. La causa non è confermata ([issue #6110](https://github.com/ublue-os/bazzite/issues/6110)).
- **Ventola:** il driver del kernel non supporta le schede OneXPlayer Intel. Aspettati la gestione automatica, senza curve personalizzate ([oxp-sensors](https://www.kernel.org/doc/html//v6.11/hwmon/oxp-sensors.html), [Quirks](https://docs.bazzite.gg/Handheld_and_HTPC_edition/quirks/)).

### Tornare alla versione precedente

- Sugli handheld il menu GRUB è nascosto: premi <kbd>Esc</kbd> all'avvio per mostrarlo, poi scegli la voce `ostree:1`.
- Avviare la versione precedente da GRUB vale solo per quell'avvio. Per renderla quella predefinita, una volta dentro esegui uno dei comandi qui sotto.
- Dopo 3 avvii falliti, sugli handheld Bazzite torna da solo alla versione precedente.
- Il rollback non tocca i tuoi file personali.

```bash
rpm-ostree rollback
```

```bash
brh rollback
```

Il secondo comando usa Bazzite Rollback Helper: `brh list` mostra le immagini degli ultimi 90 giorni.

**Cambiare immagine** (per esempio da Deck a Desktop): usa `brh rebase` o il Bazzite Portal. Non passare a un ambiente desktop diverso da quello in uso.

Fonti: [Rollbacks](https://docs.bazzite.gg/Installing_and_Managing_Software/Updates_Rollbacks_and_Rebasing/rolling_back_system_updates/), [Rollback Helper](https://docs.bazzite.gg/Installing_and_Managing_Software/Updates_Rollbacks_and_Rebasing/bazzite_rollback_helper/), [SteamOS Comparison](https://docs.bazzite.gg/General/SteamOS_Comparison/).

---

<h2 id="non-verificato">Cosa non è verificato</h2>

- Il supporto ufficiale per il OneXPlayer 1S / 8.4" Intel: non compare in nessuna pagina ufficiale.
- Il funzionamento completo dei controlli integrati.
- TDP, giroscopio, audio, Wi-Fi, sospensione, sensore di luminosità e tasti funzione: nessuna segnalazione trovata.
- Combinazioni per BIOS e menu di avvio, impostazione di fabbrica di Secure Boot e presenza di VMD sul 1S.
- Prestazioni reali della Iris Xe in Gaming Mode e con i giochi Epic.
- La documentazione Bazzite si contraddice su Ventoy, sul partizionamento per il dual boot e sulla dimensione minima della chiavetta. Questa guida segue la versione più recente.

---

<h2 id="fonti">Fonti principali</h2>

- [bazzite.gg, sito e configuratore](https://bazzite.gg/)
- [Installation Guide](https://docs.bazzite.gg/General/Installation_Guide/install-guide/)
- [Guida handheld](https://docs.bazzite.gg/General/Installation_Guide/Installing_Bazzite_for_Handheld_PCs/)
- [Secure Boot](https://docs.bazzite.gg/General/Installation_Guide/secure_boot/)
- [Troubleshooting Guide](https://docs.bazzite.gg/General/Installation_Guide/troubleshoot_guide/)
- [Legacy ISO](https://docs.bazzite.gg/General/Installation_Guide/legacy-install/)
- [FAQ](https://docs.bazzite.gg/General/FAQ/)
- [Common Issues & Resolutions](https://docs.bazzite.gg/General/issues_and_resolutions/)
- [Hardware Compatibility for Gaming](https://docs.bazzite.gg/Gaming/Hardware_compatibility_for_gaming/)
- [Introduction to Gaming](https://docs.bazzite.gg/Gaming/gaming-intro/)
- [Handheld Wiki](https://docs.bazzite.gg/Handheld_and_HTPC_edition/Handheld_Wiki/)
- [OneXPlayer Handhelds](https://docs.bazzite.gg/Handheld_and_HTPC_edition/Handheld_Wiki/OneXPlayer_Handhelds/)
- [Comandi ujust](https://docs.bazzite.gg/Installing_and_Managing_Software/ujust/)
- [Update Guide](https://docs.bazzite.gg/Installing_and_Managing_Software/Updates_Rollbacks_and_Rebasing/updating_guide/)
- [Rolling back system updates](https://docs.bazzite.gg/Installing_and_Managing_Software/Updates_Rollbacks_and_Rebasing/rolling_back_system_updates/)
- [Forum Universal Blue, guida dual boot](https://universal-blue.discourse.group/t/dual-boot-preliminary-setup-and-post-setup-guide/2743)
- [Forum Universal Blue, avvio dopo aggiornamento BIOS](https://universal-blue.discourse.group/t/dual-boot-broken-after-bios-update/12193)
- [Rufus, sito ufficiale](https://rufus.ie/)
- [Rufus, ISO mode e DD mode](https://github.com/pbatard/rufus/issues/843)
- [GitHub issue #6240](https://github.com/ublue-os/bazzite/issues/6240)
- [GitHub issue #6199](https://github.com/ublue-os/bazzite/issues/6199)
- [GitHub issue #6110](https://github.com/ublue-os/bazzite/issues/6110)
- [GitHub issue #6156](https://github.com/ublue-os/bazzite/issues/6156)
- [InputPlumber](https://shadowblip.github.io/InputPlumber/usage/)
- [Driver oxp-sensors](https://www.kernel.org/doc/html//v6.11/hwmon/oxp-sensors.html)
- [DROIX, driver e FAQ OneXPlayer](https://droix.net/blogs/onexplayer-downloads-drivers-faq/)
- [FAQ OneXPlayer](https://onexplayerstore.com/pages/faqs)
- [Heroic Games Launcher](https://github.com/Heroic-Games-Launcher/HeroicGamesLauncher)
- [Forum Universal Blue, Epic su Bazzite](https://universal-blue.discourse.group/t/is-bazzite-good-for-epic-games/4132)

*Guida basata sulla documentazione disponibile al 7 novembre 2026: verifica sempre le pagine ufficiali prima di procedere.*
