---
title: "aria2c: scaricare file da terminale in modo veloce e affidabile (Linux, Bazzite e Windows)"
date: 2026-11-08
tags: [aria2, aria2c, download, linux, windows, bazzite, terminale, guida]
description: Guida a aria2c, il downloader da riga di comando a più connessioni. Installazione su Debian/Ubuntu, Fedora, Arch/CachyOS, openSUSE, Bazzite e Windows, e configurazione ottimale per una normale connessione FTTC/VDSL.
---

`aria2c` è un downloader da riga di comando, leggero e senza interfaccia grafica, che scarica un file aprendo **più connessioni in parallelo** e ricomponendolo mentre arriva. Supporta HTTP, HTTPS, FTP, SFTP, BitTorrent e Metalink. Questa guida copre quello che serve nella maggior parte dei casi: scaricare un file o un elenco di file, riprenderli se si interrompono e farlo con impostazioni sensate per una connessione di casa normale.

La versione usata e verificata per scrivere la guida è la **1.37.0**, l'ultima rilasciata dal progetto. Le opzioni descritte sono state controllate con `aria2c --help` su quella versione.

---

## 1. Come funziona (e quando serve davvero)

Un browser o `curl` scaricano un file con **una sola connessione**. aria2c divide il file in segmenti e li scarica insieme, anche da più server (mirror) se glieli dai. Questo aiuta in tre casi:

- il server limita la velocità **per singola connessione** (molto comune sui mirror pubblici): con 8 connessioni si sommano gli 8 limiti;
- la tua linea ha una latenza alta verso il server e una sola connessione TCP non riesce a riempire la banda;
- vuoi **riprendere** un download interrotto senza ricominciare da capo, anche dopo ore o dopo un riavvio.

Non serve, anzi è inutile, quando il server ti dà già tutta la banda con una connessione sola: aria2c non può superare la velocità della tua linea. L'unico modo per saperlo è provare (vedi la sezione 4).

### I tre parametri da capire

Tutta l'ottimizzazione ruota attorno a tre opzioni, che si confondono facilmente:

- `-x` / `--max-connection-per-server`: quante connessioni apre **verso lo stesso server**. Valori da 1 a 16, **default 1**.
- `-s` / `--split`: in quante parti dividere il file, cioè quante connessioni totali usare. **Default 5**.
- `-k` / `--min-split-size`: dimensione minima di un segmento. **Default 20M**. aria2 non divide un intervallo più piccolo di `2 × SIZE`.

Con una sola URL il numero reale di connessioni è il **minore tra `-x` e `-s`**. Per questo i due valori vanno alzati insieme: con `-s 16` e `-x` lasciato a 1 si scarica comunque con una connessione sola. E con il `-k` di default da 20M un file sotto i 40 MiB non viene diviso affatto, quindi conviene abbassarlo.

> **Attenzione ai server:** molti siti limitano le connessioni per indirizzo IP. Se esageri puoi ricevere errori 403 o 429, oppure un blocco temporaneo. È il motivo per cui nella guida si arriva a 8 connessioni e non a 16 sulla linea di esempio.

---

## 2. Installazione

aria2 è nei repository di tutte le distribuzioni principali, quindi si installa con il gestore pacchetti della distro. Dopo l'installazione verifica sempre con:

```bash
aria2c --version
```

### 2.1 Debian, Ubuntu, Linux Mint, Pop!_OS

```bash
sudo apt update
sudo apt install aria2
```

### 2.2 Fedora

```bash
sudo dnf install aria2
```

### 2.3 Arch Linux, CachyOS, EndeavourOS, Manjaro

```bash
sudo pacman -S aria2
```

### 2.4 openSUSE

```bash
sudo zypper install aria2
```

### 2.5 Bazzite (e le altre distro immutabili)

Bazzite è un sistema **immutabile**: `/usr` è di sola lettura e i pacchetti di sistema si aggiungono con `rpm-ostree`, che richiede un riavvio e può dare noie negli aggiornamenti. Per uno strumento da terminale come aria2 il metodo più pulito è **Homebrew**, che installa tutto nella tua cartella senza toccare il sistema e sopravvive agli aggiornamenti di Bazzite.

Homebrew è in genere già presente su Bazzite. Controlla:

```bash
brew --version
```

Se risponde con una versione, installa aria2:

```bash
brew install aria2
aria2c --version
```

Se invece `brew` non esiste, installalo seguendo le istruzioni ufficiali su `https://brew.sh` e riapri il terminale.

> **Alternative, da sapere ma non consigliate:** `rpm-ostree install aria2` lo integra nel sistema ma obbliga al riavvio; con Distrobox si installa dentro un contenitore Fedora o Arch, ma i download e la configurazione restano legati al contenitore. Per questo uso Homebrew.

La configurazione di aria2 (sezione 5) si mette nella tua cartella personale, quindi funziona uguale con tutti e tre i metodi.

### 2.6 Windows

Su Windows 10 e 11 il modo più semplice è `winget`, già incluso nel sistema. Apri **PowerShell** (non serve come amministratore):

```powershell
winget install aria2.aria2
```

Chiudi e riapri il terminale, poi verifica:

```powershell
aria2c --version
```

Il pacchetto è quello ufficiale del progetto e viene installato come programma portatile, con `aria2c` già raggiungibile dal PATH. Se preferisci un altro gestore pacchetti:

```powershell
# Scoop
scoop install aria2

# Chocolatey (PowerShell come amministratore)
choco install aria2
```

**Installazione manuale:** scarica lo zip `aria2-1.37.0-win-64bit-build1.zip` dalla pagina delle release su `https://github.com/aria2/aria2/releases`, estrailo in una cartella fissa (per esempio `C:\Tools\aria2`) e aggiungi quella cartella al PATH di Windows. Se `aria2c` non viene riconosciuto dopo l'installazione, quasi sempre basta riaprire il terminale.

---

## 3. I primi comandi

Scaricare un file nella cartella corrente:

```bash
aria2c https://example.org/file.iso
```

Con connessioni multiple, scelte a mano:

```bash
aria2c -x 8 -s 8 -k 5M https://example.org/file.iso
```

Scegliere cartella e nome del file:

```bash
aria2c -d ~/Downloads -o ubuntu.iso https://example.org/file.iso
```

Il flag `-d` indica la cartella di destinazione, `-o` il nome con cui salvare il file.

Riprendere un download interrotto (basta rilanciare lo stesso comando con `-c`):

```bash
aria2c -c https://example.org/file.iso
```

> **Virgolette sulle URL:** se l'indirizzo contiene `&`, `?` o `;` mettilo **tra virgolette singole** (`'https://...'`). Senza, la shell lo interpreta come comando e lo spezza. Vale per bash, zsh e PowerShell. Nel vecchio prompt dei comandi di Windows (`cmd`) usa le virgolette doppie.

Durante il download aria2c mostra una riga di stato con la percentuale, la velocità, il tempo stimato e il numero di connessioni (`CN:8`). Con `Ctrl+C` si interrompe in modo pulito: il download resta riprendibile.

---

## 4. Quali valori usare in base alla connessione

Non esiste un valore universale: dipende dalla banda e dal numero di connessioni che i server accettano. La tabella dà un punto di partenza per tre fasce comuni. La riga **FTTC/VDSL** è quella usata nell'esempio completo della sezione 5.

| Parametro | ADSL, sotto 30 Mbit | FTTC/VDSL, 30-200 Mbit | FTTH, 100-1000 Mbit |
|---|---|---|---|
| `max-connection-per-server` (`-x`) | 4 | **8** | 16 |
| `split` (`-s`) | 4 | **8** | 16 |
| `min-split-size` (`-k`) | 10M | **5M** | 1M |
| `max-concurrent-downloads` (`-j`) | 2 | **3** | 5 |
| `disk-cache` | 16M | **32M** | 64M |
| `max-tries` / `retry-wait` | 10 / 10 | **10 / 5** | 5 / 3 |
| Limite globale di banda | circa 80% della linea | circa 80% della linea | nessuno |

Come leggere i valori:

- **Connessioni totali.** Il massimo di connessioni aperte è circa `-j × -x`. Con i valori FTTC sono fino a 24, un numero che la maggior parte dei router di casa gestisce senza problemi. Alzare tutto al massimo su una linea lenta non fa scaricare più veloce: affolla solo il router e lo rende lento anche per navigare.
- **Megabit contro megabyte.** Le linee si misurano in **Mbit/s**, aria2 mostra e accetta **byte al secondo**. Dividi per 8: una linea da 100 Mbit/s fa al massimo circa 12,5 MB/s. Per lasciare un 20% libero per il resto della rete, il limite sarebbe `--max-overall-download-limit=10M`.
- **`-k` più basso su linee più veloci.** Un segmento minimo piccolo permette di usare tutte le connessioni anche su file medi. Su una linea lenta segmenti più grandi riducono il lavoro inutile.
- **`-j` conta i file, non le connessioni.** Serve solo quando scarichi un elenco (sezione 6).
- **Nessun valore oltre 16** per `-x`: è il massimo consentito da aria2.

### Come provare quali valori funzionano meglio con il tuo provider

Scegli un file grande (almeno qualche centinaio di MB) da un server che usi spesso e confronta:

```bash
aria2c -x 1 -s 1 -d /tmp --allow-overwrite=true https://example.org/file.iso
aria2c -x 8 -s 8 -k 5M -d /tmp --allow-overwrite=true https://example.org/file.iso
```

Guarda la velocità media a fine download. Se le due prove sono simili, quel server ti dà già tutta la banda e le connessioni multiple non servono. Se la seconda è nettamente più veloce, il server limita ogni connessione. In quel caso prova anche 12 o 16: se non guadagni altro, resta su 8. Sui due comandi, `--allow-overwrite=true` evita che il secondo rinomini il file in `file.1.iso`.

---

## 5. Il file di configurazione per una linea FTTC/VDSL

Invece di scrivere ogni volta tutti i flag, si mettono le impostazioni in un file `aria2.conf` che aria2c legge da solo a ogni avvio. I flag scritti sulla riga di comando hanno comunque la precedenza.

### Dove va il file

Sulla versione 1.37.0 il percorso di default è questo (verificato con `aria2c --help=--conf-path`):

- **Linux e Bazzite:** `~/.config/aria2/aria2.conf`
- **Windows:** `C:\Users\NOMEUTENTE\.config\aria2\aria2.conf`

Su Linux e Bazzite crea cartella e file così:

```bash
mkdir -p ~/.config/aria2
nano ~/.config/aria2/aria2.conf
```

Su Windows, da PowerShell:

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.config\aria2"
notepad "$env:USERPROFILE\.config\aria2\aria2.conf"
```

Notepad chiede se creare il file: conferma. Se preferisci un'altra posizione, aria2c si può far partire con `--conf-path="percorso\del\file"`.

### Il file completo

```
# aria2.conf - configurazione per FTTC/VDSL (30-200 Mbit)

# --- Cartella di destinazione ---
# Metti un percorso assoluto: nel file di configurazione non c'è la shell
# a espandere la tilde (~) o le variabili d'ambiente.
# Linux/Bazzite:
dir=/home/NOMEUTENTE/Downloads
# Windows (barre normali, non rovesciate):
# dir=C:/Users/NOMEUTENTE/Downloads

# --- Connessioni ---
max-connection-per-server=8
split=8
min-split-size=5M
max-concurrent-downloads=3

# --- Ripresa e tentativi ---
continue=true
max-tries=10
retry-wait=5
connect-timeout=10
timeout=30

# --- Disco ---
# falloc riserva lo spazio all'inizio in modo quasi istantaneo.
# Va bene su ext4, btrfs, xfs e NTFS. NON usarlo su FAT32/exFAT: metti none.
file-allocation=falloc
disk-cache=32M

# --- Banda ---
# 0 = nessun limite. Per lasciare banda libera alla rete di casa,
# usa circa l'80% della linea in byte al secondo (100 Mbit = 12,5 MB/s -> 10M).
max-overall-download-limit=0

# --- Varie ---
# Applica al file la data di modifica che ha sul server (se la comunica)
remote-time=true
# Meno rumore nel terminale: mostra solo avvisi ed errori
console-log-level=warn
```

> **I commenti vanno su righe a parte.** Nel file di configurazione di aria2 un `#` a fine riga non è un commento: viene considerato parte del valore e l'opzione si rompe. Scrivi sempre `chiave=valore` da solo sulla riga.

### Cosa fa ogni gruppo

- `dir`: dove salvare i file se non indichi `-d`. Se non lo imposti, aria2c scarica nella cartella da cui lo lanci.
- `continue=true`: equivale a `-c` sempre attivo. Se il file esiste in parte, riprende da lì invece di ricominciare.
- `max-tries` e `retry-wait`: in caso di errore riprova fino a 10 volte, aspettando 5 secondi tra un tentativo e l'altro. Il default è 5 tentativi senza pausa, troppo poco per un server momentaneamente carico.
- `connect-timeout` e `timeout`: i default sono 60 secondi per entrambi. Abbassarli a 10 e 30 fa abbandonare prima una connessione bloccata e riprovare, invece di restare fermi un minuto.
- `file-allocation=falloc`: il default è `prealloc`, che scrive materialmente l'intero file a zeri prima di cominciare e su file di qualche GB può richiedere tempo. `falloc` è quasi istantaneo. Sulle chiavette USB formattate FAT32 o exFAT metti `none`. Su Windows con NTFS il manuale lo indica come supportato dalle build MinGW, che sono quelle ufficiali; se dovessi avere errori di allocazione, passa a `none`.
- `disk-cache=32M`: accumula i dati in memoria e li scrive in blocchi più grandi, riducendo gli accessi al disco. È particolarmente utile su hard disk meccanici. Il default è 16M.
- `remote-time=true`: il file scaricato riporta la data originale del server, comoda per riconoscere le versioni.

### Opzioni che sconsiglio

- **`--check-certificate=false`**: disattiva il controllo del certificato HTTPS. Risolve un errore nascondendolo e ti espone ad attacchi. Se compare un errore di certificato, la causa va cercata (data del PC sbagliata, certificato scaduto sul server).
- **`--optimize-concurrent-downloads`**: con i valori predefiniti adatta il numero di download paralleli alla banda e su una linea da 100 Mbit arriva a oltre 50 contemporanei. È pensata per altri scenari e su una linea domestica è controproducente.
- **`--lowest-speed-limit`**: chiude le connessioni sotto una certa velocità. Può servire con mirror instabili, ma se tutte le sorgenti sono lente il download termina con errore. Lasciala disattivata finché non hai un problema concreto.

---

## 6. Elenchi di URL e ripresa dei download

### Scaricare più file da un elenco

Crea un file di testo, per esempio `lista.txt`, con **un indirizzo per riga**:

```
https://example.org/file1.iso
https://example.org/file2.iso
https://example.org/file3.iso
```

e lancialo con `-i`:

```bash
aria2c -i lista.txt
```

I file vengono scaricati `max-concurrent-downloads` alla volta (3 con la nostra configurazione), ciascuno con le sue connessioni.

Nello stesso file puoi anche scegliere cartella e nome per ogni URL, indentando le opzioni sotto l'indirizzo con uno o più spazi:

```
https://example.org/file1.iso
  dir=/home/NOMEUTENTE/Downloads/iso
  out=distro-1.iso
https://example.org/file2.iso
  dir=/home/NOMEUTENTE/Downloads/iso
```

Per scaricare **lo stesso file da più mirror insieme**, scrivi le URL sulla stessa riga, separate da una tabulazione (TAB):

```
https://mirror-a.example.org/file.iso<TAB>https://mirror-b.example.org/file.iso
```

aria2c usa tutti i mirror contemporaneamente e, se uno cade, continua con gli altri. Verifica comunque che siano davvero lo stesso file (vedi sezione 7).

### Come funziona la ripresa

Mentre scarica, aria2c crea accanto al file un secondo file con lo stesso nome più `.aria2` (per esempio `file.iso.aria2`), che contiene la mappa dei segmenti già completati. Se il download si interrompe per un errore, per `Ctrl+C` o per uno spegnimento, basta rilanciare lo stesso comando: aria2c legge quel file e riparte dai segmenti mancanti.

Tre cose da ricordare:

1. **Non cancellare il file `.aria2`** finché il download non è finito. Quando termina, aria2c lo elimina da solo.
2. Il server deve supportare le richieste parziali (header `Range`). Quasi tutti lo fanno; se non lo fa, aria2c lo segnala e scarica con una connessione sola, senza possibilità di ripresa.
3. Con un elenco, per riprendere **tutto l'elenco dopo una chiusura** puoi chiedere ad aria2c di salvare i download non finiti:

```bash
aria2c -i lista.txt --save-session=sessione.txt
```

Al riavvio si rilancia con `aria2c -i sessione.txt`, che contiene solo ciò che era rimasto indietro.

Se il link è scaduto (capita con i link temporanei), puoi riprendere lo stesso file con un nuovo indirizzo che punta allo stesso contenuto: indica lo stesso nome con `-o` e la stessa cartella, e aria2c dovrebbe ripartire dal `.aria2` esistente (purché il file abbia la stessa dimensione).

---

## 7. Verificare che il file sia integro

Un download multi-sorgente va sempre verificato quando il file è importante, come un'ISO. aria2c può farlo da solo se conosci l'hash, pubblicato di solito accanto al file sul sito:

```bash
aria2c --checksum=sha-256=HASH_COPIATO_DAL_SITO https://example.org/file.iso
```

Se l'hash non coincide, aria2c lo segnala come errore (codice di uscita 32). In alternativa lo si controlla dopo:

```bash
# Linux e Bazzite
sha256sum file.iso
```

```powershell
# Windows
Get-FileHash file.iso -Algorithm SHA256
```

Confronta il risultato con quello pubblicato dal sito ufficiale. Se non coincide, il file va riscaricato.

---

## 8. Problemi comuni

**Il terminale dice che `aria2c` non esiste.**
Su Windows riapri il terminale dopo l'installazione. Su Bazzite controlla che `brew` sia nel PATH (`brew --version`) e riapri la sessione se l'hai appena installato.

**Errore con `status=403` o `429`, oppure `errorCode=22`.**
Il server rifiuta le troppe connessioni o il tuo user agent. Abbassa `-x` (prova 4 o 2) e riprova. Se il problema resta, prova a presentarti come un browser:

```bash
aria2c --user-agent="Mozilla/5.0" https://example.org/file.iso
```

**`errorCode=29` o 503.**
Il server è sovraccarico o ti ha limitato per un po': aspetta e rilancia con `-c`, oppure usa un altro mirror.

**La velocità non cresce con più connessioni.**
Il server o la tua linea sono già al massimo. Torna al confronto della sezione 4: in quel caso `-x 1` è sufficiente.

**Il file scaricato si chiama `file.1.iso`.**
Esisteva già un file con quel nome e aria2c lo ha rinominato per non sovrascriverlo. Se vuoi riprendere quello vecchio, aggiungi `-c`. Se vuoi sostituirlo, aggiungi `--allow-overwrite=true`.

**Download da Google Drive, Mega, Dropbox o siti con login.**
aria2c funziona con link **diretti** al file. Le pagine di condivisione di quei servizi non lo sono. Con i siti che richiedono il login puoi passare i cookie del browser con `--load-cookies=cookies.txt` o un header con `--header="Cookie: ..."`, ma per quei servizi è spesso più semplice usare il loro strumento ufficiale.

**Spazio su disco insufficiente (`errorCode=9`).**
Con `falloc` lo spazio viene riservato subito, quindi l'errore compare all'inizio e non dopo ore. È un vantaggio: libera spazio e rilancia con `-c`.

### Codici di uscita utili

| Codice | Significato |
|---|---|
| 0 | Tutti i download completati |
| 1 | Errore sconosciuto |
| 3 | Risorsa non trovata (404) |
| 8 | Il server non supporta la ripresa |
| 9 | Spazio su disco insufficiente |
| 19 | Risoluzione del nome (DNS) fallita |
| 22 | Risposta HTTP non valida, tipica di 403 e 429 |
| 29 | Server non disponibile o sovraccarico |
| 32 | Verifica dell'hash fallita |

---

## 9. Riepilogo rapido

```bash
# installare
sudo apt install aria2      # Debian, Ubuntu
sudo dnf install aria2      # Fedora
sudo pacman -S aria2        # Arch, CachyOS
sudo zypper install aria2   # openSUSE
brew install aria2          # Bazzite
winget install aria2.aria2  # Windows (PowerShell)

# usare
aria2c URL                          # download semplice
aria2c -x 8 -s 8 -k 5M URL          # 8 connessioni
aria2c -c URL                       # riprendere
aria2c -i lista.txt                 # elenco di URL
aria2c --checksum=sha-256=HASH URL  # con verifica
```

Con `~/.config/aria2/aria2.conf` configurato come nella sezione 5 bastano `aria2c URL` e `aria2c -i lista.txt`: tutto il resto è già impostato.

### Cosa non è coperto

Per tenere la guida concentrata su ciò che serve ogni giorno, restano fuori l'uso come client BitTorrent (`aria2c file.torrent` o un magnet link), i file Metalink e la modalità demone con RPC e interfacce web come AriaNg o Motrix. Sono argomenti per un secondo articolo.
