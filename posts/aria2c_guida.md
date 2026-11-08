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

Se invece `brew` non esiste, installalo con il comando ufficiale (lo stesso mostrato su `https://brew.sh`; ti chiede la password e di premere Invio per confermare):

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Alla fine dell'installazione rendi `brew` disponibile nel terminale, adesso e ai prossimi accessi (questi sono i comandi della documentazione ufficiale per bash; con zsh sostituisci `~/.bashrc` con `~/.zshrc`):

```bash
echo 'eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"' >> ~/.bashrc
eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"
```

Poi installa aria2 e verifica:

```bash
brew install aria2
aria2c --version
```

> **Alternative, da sapere ma non consigliate:** `rpm-ostree install aria2` lo integra nel sistema ma obbliga al riavvio; con Distrobox si installa dentro un contenitore Fedora o Arch, ma i download e la configurazione restano legati al contenitore. Per questo uso Homebrew.

La configurazione di aria2 (sezione 5) si mette nella tua cartella personale, quindi funziona uguale con tutti e tre i metodi.

### 2.6 Windows

Su Windows 10 e 11 il modo più semplice è `winget`, già incluso nel sistema. Apri **PowerShell** (non serve come amministratore):

```powershell
winget install aria2.aria2
```

Il terminale già aperto non conosce ancora il nuovo programma. Puoi chiuderlo e riaprirlo, oppure aggiornare il PATH della sessione corrente con questo comando:

```powershell
$env:Path = [Environment]::GetEnvironmentVariable("Path","User") + ";" + [Environment]::GetEnvironmentVariable("Path","Machine")
```

Poi verifica:

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

**Installazione manuale (senza gestori pacchetti):** tre comandi PowerShell. Il primo scarica lo zip ufficiale dalla pagina delle release del progetto (`https://github.com/aria2/aria2/releases`), il secondo lo estrae in `%LOCALAPPDATA%\Programs` (non servono i permessi di amministratore), il terzo aggiunge la cartella al PATH del tuo utente:

```powershell
Invoke-WebRequest -Uri "https://github.com/aria2/aria2/releases/download/release-1.37.0/aria2-1.37.0-win-64bit-build1.zip" -OutFile "$env:TEMP\aria2.zip"
```

```powershell
Expand-Archive -Path "$env:TEMP\aria2.zip" -DestinationPath "$env:LOCALAPPDATA\Programs" -Force
```

```powershell
[Environment]::SetEnvironmentVariable("Path", [Environment]::GetEnvironmentVariable("Path","User") + ";$env:LOCALAPPDATA\Programs\aria2-1.37.0-win-64bit-build1", "User")
```

Poi aggiorna il PATH della sessione e verifica, con i due comandi mostrati sopra (`$env:Path = ...` e `aria2c --version`). Si usa `SetEnvironmentVariable` e non `setx`, perché `setx` taglia il PATH oltre i 1024 caratteri e può rovinarlo.

> **Aggiornamenti:** con l'installazione manuale non si aggiorna da solo. Quando esce una versione nuova, ripeti i primi due comandi con il nuovo numero di versione e correggi il percorso nel PATH.

---

## 3. I primi comandi

Tutti gli esempi di questa guida si possono incollare così come sono: usano i **file di prova pubblici di OVH** (`https://proof.ovh.net/files/`), che esistono apposta per misurare la velocità. Hanno nome `1Mb.dat`, `10Mb.dat`, `100Mb.dat` e `1Gb.dat` e, nonostante la sigla, pesano rispettivamente 1, 10, 100 e 1024 MiB. Non contengono nulla di utile: servono solo a provare.

> **Se il server di prova non risponde:** sono server pubblici e limitano chi scarica troppo spesso. Dopo molte prove di seguito può comparire un timeout o l'errore `status=429`. Aspetta qualche minuto, oppure sostituisci `proof.ovh.net` con `proof.ovh.ca` o `proof.ovh.us` nello stesso comando: sono lo stesso file su altri server.

Scaricare un file (da 10 MiB) nella cartella corrente:

```bash
aria2c https://proof.ovh.net/files/10Mb.dat
```

Con connessioni multiple, scelte a mano (file da 100 MiB):

```bash
aria2c -x 8 -s 8 -k 5M https://proof.ovh.net/files/100Mb.dat
```

Scegliere cartella e nome del file. Il flag `-d` indica la cartella di destinazione, `-o` il nome con cui salvare il file.

```bash
# Linux e Bazzite
aria2c -d ~/Downloads -o prova.dat https://proof.ovh.net/files/10Mb.dat
```

```powershell
# Windows (PowerShell)
aria2c -d "$env:USERPROFILE\Downloads" -o prova.dat https://proof.ovh.net/files/10Mb.dat
```

Riprendere un download interrotto: lancia il download da 100 MiB, premi `Ctrl+C` dopo qualche secondo e rilancia lo stesso comando con `-c`. Riparte da dove si era fermato:

```bash
aria2c -c -x 8 -s 8 -k 5M https://proof.ovh.net/files/100Mb.dat
```

> **Virgolette sulle URL:** se l'indirizzo contiene `&`, `?` o `;` mettilo **tra virgolette singole**. Senza, la shell lo interpreta come comando e lo spezza. Vale per bash, zsh e PowerShell. Nel vecchio prompt dei comandi di Windows (`cmd`) usa le virgolette doppie. Esempio di sintassi (l'indirizzo è inventato, sostituiscilo con il tuo):
>
> ```bash
> aria2c 'https://example.org/scarica?id=15&formato=iso'
> ```

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

Scarica lo stesso file da 100 MiB prima con una connessione sola e poi con otto, e confronta il tempo totale. `--no-conf` serve a ignorare l'eventuale `aria2.conf` della sezione 5, così le due prove dipendono solo dai flag scritti qui.

```bash
# Linux e Bazzite
aria2c --no-conf -x 1 -s 1 -d /tmp -o prova-x1.dat https://proof.ovh.net/files/100Mb.dat
aria2c --no-conf -x 8 -s 8 -k 5M -d /tmp -o prova-x8.dat https://proof.ovh.net/files/100Mb.dat
rm /tmp/prova-x1.dat /tmp/prova-x8.dat
```

```powershell
# Windows (PowerShell)
aria2c --no-conf -x 1 -s 1 -d "$env:TEMP" -o prova-x1.dat https://proof.ovh.net/files/100Mb.dat
aria2c --no-conf -x 8 -s 8 -k 5M -d "$env:TEMP" -o prova-x8.dat https://proof.ovh.net/files/100Mb.dat
Remove-Item "$env:TEMP\prova-x1.dat", "$env:TEMP\prova-x8.dat"
```

Guarda la velocità media (`avg speed`) nella tabella finale. Se le due prove sono simili, quel server ti dà già tutta la banda e le connessioni multiple non servono. Se la seconda è nettamente più veloce, il server limita ogni connessione.

Come esempio, sul PC con cui ho scritto questa guida (8 novembre 2026, verso il server OVH) lo stesso file da 100 MiB ha impiegato circa **120 secondi con una connessione** e circa **61 secondi con otto**. Il risultato dipende da linea, ora del giorno e server, quindi il tuo sarà diverso. Se otto connessioni migliorano molto, prova anche con 12 o 16 (`-x 16 -s 16`): se non guadagni altro, resta su 8.

---

## 5. Il file di configurazione per una linea FTTC/VDSL

Invece di scrivere ogni volta tutti i flag, si mettono le impostazioni in un file `aria2.conf` che aria2c legge da solo a ogni avvio. I flag scritti sulla riga di comando hanno comunque la precedenza.

### Creare il file con un solo comando

Il file va in questo percorso, che aria2c 1.37.0 legge da solo a ogni avvio (verificato con `aria2c --help=--conf-path`):

- **Linux e Bazzite:** `~/.config/aria2/aria2.conf`
- **Windows:** `C:\Users\NOMEUTENTE\.config\aria2\aria2.conf`

Non devi modificare nulla a mano: i comandi qui sotto creano la cartella, scrivono il file e inseriscono da soli la tua cartella dei download.

**Linux e Bazzite** (un unico blocco da incollare nel terminale). La cartella dei download viene letta dal sistema con `xdg-user-dir`, quindi funziona anche se la tua si chiama `Scaricati` invece di `Downloads`:

```bash
mkdir -p ~/.config/aria2
DL="$(xdg-user-dir DOWNLOAD 2>/dev/null || echo "$HOME/Downloads")"
cat > ~/.config/aria2/aria2.conf <<EOF
# aria2.conf - FTTC/VDSL (30-200 Mbit)

# Cartella di destinazione
dir=$DL

# Connessioni
max-connection-per-server=8
split=8
min-split-size=5M
max-concurrent-downloads=3

# Ripresa e tentativi
continue=true
max-tries=10
retry-wait=5
connect-timeout=10
timeout=30

# Disco: falloc riserva lo spazio subito (ext4, btrfs, xfs, NTFS). Su FAT32 o exFAT usa none
file-allocation=falloc
disk-cache=32M

# Banda: 0 = nessun limite. 100 Mbit = 12,5 MB/s: per lasciare banda libera usa circa 10M
max-overall-download-limit=0

# Varie
remote-time=true
console-log-level=warn
EOF
```

**Windows** (un unico blocco da incollare in PowerShell). Scrive il file in UTF-8 senza BOM, che è il formato che aria2c legge senza errori, e usa le barre normali nel percorso, accettate da aria2c:

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.config\aria2" | Out-Null
$dir = "$env:USERPROFILE\Downloads" -replace '\\','/'
$conf = @"
# aria2.conf - FTTC/VDSL (30-200 Mbit)

# Cartella di destinazione
dir=$dir

# Connessioni
max-connection-per-server=8
split=8
min-split-size=5M
max-concurrent-downloads=3

# Ripresa e tentativi
continue=true
max-tries=10
retry-wait=5
connect-timeout=10
timeout=30

# Disco: falloc riserva lo spazio subito (ext4, btrfs, xfs, NTFS). Su FAT32 o exFAT usa none
file-allocation=falloc
disk-cache=32M

# Banda: 0 = nessun limite. 100 Mbit = 12,5 MB/s: per lasciare banda libera usa circa 10M
max-overall-download-limit=0

# Varie
remote-time=true
console-log-level=warn
"@
[System.IO.File]::WriteAllText("$env:USERPROFILE\.config\aria2\aria2.conf", $conf, (New-Object System.Text.UTF8Encoding $false))
```

### Controllare che funzioni

Mostra il file appena creato e controlla che la riga `dir=` contenga la tua cartella dei download:

```bash
# Linux e Bazzite
cat ~/.config/aria2/aria2.conf
```

```powershell
# Windows (PowerShell)
Get-Content "$env:USERPROFILE\.config\aria2\aria2.conf"
```

Poi scarica un file di prova senza scrivere nessun flag: deve comparire nella cartella indicata in `dir=`, scaricato con 8 connessioni (`CN:8` nella riga di stato):

```bash
aria2c https://proof.ovh.net/files/10Mb.dat
```

### Modificarlo in seguito

Quando vorrai cambiare un valore (per esempio passare a `file-allocation=none`), apri il file con un editor:

```bash
# Linux e Bazzite
nano ~/.config/aria2/aria2.conf
```

```powershell
# Windows (PowerShell)
notepad "$env:USERPROFILE\.config\aria2\aria2.conf"
```

Se vuoi tenere il file altrove, aria2c si avvia con `--conf-path` seguito dal percorso. Per ignorare del tutto il file in un singolo comando c'è `--no-conf`.

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

L'elenco è un file di testo con **un indirizzo per riga**. Questi comandi creano `lista.txt` con tre file di prova e li scaricano (se hai creato l'`aria2.conf` della sezione 5, finiscono nella tua cartella dei download; altrimenti nella cartella corrente).

```bash
# Linux e Bazzite
cat > lista.txt <<'EOF'
https://proof.ovh.net/files/1Mb.dat
https://proof.ovh.net/files/10Mb.dat
https://proof.ovh.net/files/100Mb.dat
EOF
aria2c -i lista.txt
```

```powershell
# Windows (PowerShell)
@"
https://proof.ovh.net/files/1Mb.dat
https://proof.ovh.net/files/10Mb.dat
https://proof.ovh.net/files/100Mb.dat
"@ | Set-Content lista.txt -Encoding ascii
aria2c -i lista.txt
```

I file vengono scaricati `max-concurrent-downloads` alla volta (3 con la nostra configurazione), ciascuno con le sue connessioni.

### Cartella e nome diversi per ogni file

Nello stesso file puoi scegliere cartella e nome per ogni indirizzo, indentando le opzioni sotto l'indirizzo con uno o più spazi. Qui i due file vanno in una sottocartella `prove` dei download, il primo con un nome scelto da te:

```bash
# Linux e Bazzite
cat > lista2.txt <<EOF
https://proof.ovh.net/files/10Mb.dat
  dir=$HOME/Downloads/prove
  out=prova-10.dat
https://proof.ovh.net/files/1Mb.dat
  dir=$HOME/Downloads/prove
EOF
aria2c -i lista2.txt
```

```powershell
# Windows (PowerShell)
$d = "$env:USERPROFILE\Downloads\prove" -replace '\\','/'
@"
https://proof.ovh.net/files/10Mb.dat
  dir=$d
  out=prova-10.dat
https://proof.ovh.net/files/1Mb.dat
  dir=$d
"@ | Set-Content lista2.txt -Encoding ascii
aria2c -i lista2.txt
```

### Lo stesso file da più mirror insieme

Per scaricare **lo stesso file da più server contemporaneamente**, scrivi gli indirizzi sulla stessa riga, separati da una tabulazione. OVH mette a disposizione lo stesso file di prova su tre server (`.net`, `.ca`, `.us`); ho calcolato l'hash dei tre e coincide:

```bash
# Linux e Bazzite
printf 'https://proof.ovh.net/files/10Mb.dat\thttps://proof.ovh.ca/files/10Mb.dat\thttps://proof.ovh.us/files/10Mb.dat\n' > mirror.txt
aria2c -x 8 -s 8 -k 1M -i mirror.txt
```

```powershell
# Windows (PowerShell)
"https://proof.ovh.net/files/10Mb.dat`thttps://proof.ovh.ca/files/10Mb.dat`thttps://proof.ovh.us/files/10Mb.dat" | Set-Content mirror.txt -Encoding ascii
aria2c -x 8 -s 8 -k 1M -i mirror.txt
```

aria2c usa tutti i mirror contemporaneamente e, se uno cade, continua con gli altri. Verifica sempre che siano davvero lo stesso file (vedi sezione 7).

### Come funziona la ripresa

Mentre scarica, aria2c crea accanto al file un secondo file con lo stesso nome più `.aria2` (per esempio `100Mb.dat.aria2`), che contiene la mappa dei segmenti già completati. Se il download si interrompe per un errore, per `Ctrl+C` o per uno spegnimento, basta rilanciare lo stesso comando: aria2c legge quel file e riparte dai segmenti mancanti.

Per vederlo, lancia il download, interrompilo con `Ctrl+C` dopo qualche secondo ed elenca i file:

```bash
# Linux e Bazzite
aria2c --no-conf -x 8 -s 8 -k 5M https://proof.ovh.net/files/100Mb.dat
ls -l 100Mb.dat*
```

```powershell
# Windows (PowerShell)
aria2c --no-conf -x 8 -s 8 -k 5M https://proof.ovh.net/files/100Mb.dat
Get-ChildItem 100Mb.dat*
```

Compaiono `100Mb.dat` e `100Mb.dat.aria2`. Per riprendere basta aggiungere `-c`:

```bash
aria2c --no-conf -c -x 8 -s 8 -k 5M https://proof.ovh.net/files/100Mb.dat
```

Quando il download finisce, il file `.aria2` sparisce da solo.

Tre cose da ricordare:

1. **Non cancellare il file `.aria2`** finché il download non è finito: senza di esso aria2c non sa quali segmenti sono completi.
2. Il server deve supportare le richieste parziali (header `Range`). Quasi tutti lo fanno; se non lo fa, aria2c lo segnala e scarica con una connessione sola, senza possibilità di ripresa. Per controllare un server prima di scaricare: `curl -sI https://proof.ovh.net/files/100Mb.dat | grep -i accept-ranges` (Linux e Bazzite) oppure `(Invoke-WebRequest -Method Head https://proof.ovh.net/files/100Mb.dat).Headers["Accept-Ranges"]` (Windows). Se risponde `bytes`, va bene.
3. Con un elenco, per riprendere **tutto l'elenco dopo una chiusura** chiedi ad aria2c di salvare i download non finiti, e al riavvio rilancia il file di sessione (che contiene solo ciò che era rimasto indietro):

```bash
aria2c -i lista.txt --save-session=sessione.txt
aria2c -i sessione.txt --save-session=sessione.txt
```

Il primo comando è quello da usare la prima volta; il secondo, dopo un'interruzione.

Se il link è scaduto (capita con i link temporanei), puoi riprendere lo stesso file con un nuovo indirizzo che punta allo stesso contenuto, indicando lo stesso nome e la stessa cartella. Sostituisci `NUOVO_INDIRIZZO` con l'indirizzo che hai ottenuto (non posso scriverlo io: lo conosci solo tu):

```bash
aria2c -c -d ~/Downloads -o file.iso 'NUOVO_INDIRIZZO'
```

aria2c dovrebbe ripartire dal `.aria2` esistente, purché il file abbia la stessa dimensione.

---

## 7. Verificare che il file sia integro

Un download multi-sorgente va sempre verificato quando il file è importante, come un'ISO. aria2c lo fa da solo se gli dai l'hash, che di solito è pubblicato accanto al file sul sito ufficiale. Nell'esempio uso il file di prova da 10 MiB; l'hash SHA-256 l'ho calcolato io l'8 novembre 2026 e coincide sui tre server OVH. Per i tuoi file copia sempre l'hash dal sito ufficiale.

```bash
aria2c --checksum=sha-256=e5b844cc57f57094ea4585e235f36c78c1cd222262bb89d53c94dcb4d6b3e55d https://proof.ovh.net/files/10Mb.dat
```

Con l'hash giusto il download termina con `(OK):download completed`. Per vedere cosa succede con un hash sbagliato, prova questo (sono 64 zeri) e leggi il codice di uscita:

```bash
# Linux e Bazzite
aria2c -d /tmp --checksum=sha-256=0000000000000000000000000000000000000000000000000000000000000000 https://proof.ovh.net/files/1Mb.dat; echo $?
```

```powershell
# Windows (PowerShell)
aria2c -d "$env:TEMP" --checksum=sha-256=0000000000000000000000000000000000000000000000000000000000000000 https://proof.ovh.net/files/1Mb.dat; $LASTEXITCODE
```

aria2c segnala `Checksum error detected`, mostra `(ERR):error occurred` e restituisce il codice **32**. Se hai già il file, puoi controllarlo anche dopo:

```bash
# Linux e Bazzite (nella cartella del file)
sha256sum 10Mb.dat
```

```powershell
# Windows (PowerShell, nella cartella del file)
Get-FileHash 10Mb.dat -Algorithm SHA256
```

Confronta il risultato con quello pubblicato (PowerShell lo scrive in maiuscolo, ma le lettere maiuscole e minuscole non cambiano il valore). Se non coincide, il file va riscaricato.

---

## 8. Problemi comuni

**Il terminale dice che `aria2c` non esiste.**
Prima controlla dove lo cerca il sistema:

```bash
# Linux e Bazzite
command -v aria2c
```

```powershell
# Windows (PowerShell)
Get-Command aria2c
```

Se non risponde nulla, su Windows aggiorna il PATH della sessione (oppure riapri il terminale):

```powershell
$env:Path = [Environment]::GetEnvironmentVariable("Path","User") + ";" + [Environment]::GetEnvironmentVariable("Path","Machine")
```

Su Bazzite rendi `brew` disponibile nella sessione e riprova:

```bash
eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"
```

**Errore con `status=403` o `429`, oppure `errorCode=22`.**
Il server rifiuta le troppe connessioni o il tuo user agent. Abbassa il numero di connessioni a 2 e riprova:

```bash
aria2c -x 2 -s 2 https://proof.ovh.net/files/10Mb.dat
```

Se il problema resta, prova a presentarti come un browser:

```bash
aria2c --user-agent="Mozilla/5.0" https://proof.ovh.net/files/10Mb.dat
```

**`errorCode=29` o 503.**
Il server è sovraccarico o ti ha limitato per un po'. Aspetta qualche minuto e rilancia lo stesso comando con `-c` (nell'esempio, il download da 100 MiB):

```bash
aria2c -c https://proof.ovh.net/files/100Mb.dat
```

oppure usa un altro mirror.

**La velocità non cresce con più connessioni.**
Il server o la tua linea sono già al massimo. Rifai il confronto della sezione 4: in quel caso `-x 1` è sufficiente.

**Il file scaricato si chiama `10Mb.1.dat`.**
Esisteva già un file con quel nome e aria2c lo ha rinominato per non sovrascriverlo. Per riprendere quello vecchio aggiungi `-c`, per sostituirlo aggiungi `--allow-overwrite=true`:

```bash
aria2c -c https://proof.ovh.net/files/10Mb.dat
aria2c --allow-overwrite=true https://proof.ovh.net/files/10Mb.dat
```

**Download da Google Drive, Mega, Dropbox o siti con login.**
aria2c funziona con link **diretti** al file. Le pagine di condivisione di quei servizi non lo sono. Per i siti che richiedono il login puoi passare i cookie esportati dal browser in un file `cookies.txt` (formato Netscape). L'indirizzo qui sotto è inventato, sostituiscilo con il tuo:

```bash
aria2c --load-cookies=cookies.txt 'https://example.org/area-riservata/file.zip'
```

Per quei servizi è spesso più semplice usare il loro strumento ufficiale.

**Spazio su disco insufficiente (`errorCode=9`).**
Con `falloc` lo spazio viene riservato subito, quindi l'errore compare all'inizio e non dopo ore. Controlla lo spazio libero, liberane e rilancia con `-c`:

```bash
# Linux e Bazzite
df -h .
```

```powershell
# Windows (PowerShell)
Get-PSDrive -PSProvider FileSystem
```

### Leggere il codice di uscita

Dopo ogni comando aria2c lascia un codice di uscita. Subito dopo il comando, in bash `echo $?`; in PowerShell `$LASTEXITCODE`:

```bash
# Linux e Bazzite
echo $?
```

```powershell
# Windows (PowerShell)
$LASTEXITCODE
```

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

Installazione (un comando per sistema):

```bash
sudo apt update && sudo apt install aria2          # Debian, Ubuntu, Mint
sudo dnf install aria2                             # Fedora
sudo pacman -S aria2                               # Arch, CachyOS, EndeavourOS, Manjaro
sudo zypper install aria2                          # openSUSE
brew install aria2                                 # Bazzite
```

```powershell
winget install aria2.aria2                         # Windows
```

Uso (gli stessi comandi valgono su tutti i sistemi):

```bash
aria2c URL                                         # download semplice
aria2c -x 8 -s 8 -k 5M URL                         # 8 connessioni
aria2c -c URL                                      # riprendere un download interrotto
aria2c -i lista.txt                                # elenco di URL
aria2c --checksum=sha-256=HASH URL                 # con verifica dell'hash
aria2c --no-conf URL                               # ignora aria2.conf
```

Con l'`aria2.conf` della sezione 5 bastano `aria2c URL` e `aria2c -i lista.txt`: tutto il resto è già impostato. Qui `URL` e `HASH` sono gli unici segnaposto: li conosci solo tu.

### Cosa non è coperto

Per tenere la guida concentrata su ciò che serve ogni giorno, restano fuori l'uso come client BitTorrent (`aria2c file.torrent` o un magnet link), i file Metalink e la modalità demone con RPC e interfacce web come AriaNg o Motrix. Sono argomenti per un secondo articolo.
