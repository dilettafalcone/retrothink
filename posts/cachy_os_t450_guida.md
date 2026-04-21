---

title: "CachyOS su ThinkPad T450: guida completa all'installazione e configurazione"
date: 2026-04-21
tags: [thinkpad, cachyos, linux, nvidia, optimus]
description: Guida dettagliata e personalizzata per installare CachyOS su ThinkPad T450 con i7-5500U, 16GB DDR3, Intel HD 5500 + NVIDIA 940M e doppia batteria.

---



Questa guida è scritta per questo specifico T450, con le seguenti specifiche rilevate dal sistema: Intel Core i7-5500U (Broadwell, 2 core / 4 thread, frequenza base 2.4 GHz, boost fino a 3.0 GHz), 16 GB DDR3 1600 MT/s in configurazione dual channel (2× 8 GB), Intel HD Graphics 5500 come GPU integrata più NVIDIA GeForce 940M (architettura Maxwell, chip GM108M) come GPU dedicata in configurazione Optimus, SSD SATA da 238.5 GB, doppia batteria SANYO (BAT0 interna + BAT1 esterna), e scheda WiFi/Bluetooth Intel Wireless 7265.



Ogni passaggio è spiegato nel dettaglio per evitare errori. I comandi vanno eseguiti esattamente come scritti, salvo dove indicato diversamente.



---



## 1. Preparazione — creare la USB bootable



Prima di fare qualsiasi cosa sul T450, bisogna creare una USB avviabile con la ISO di CachyOS da un altro computer o dallo stesso T450 con il sistema attuale ancora funzionante.



### Scaricare la ISO



Aprire il browser e andare su `https://cachyos.org/download`. Scaricare la versione **x86_64** — l'unica disponibile per desktop/laptop moderni. Il T450 con i7-5500U è a 64 bit. Il file si chiamerà qualcosa come `cachyos-x86\_64-YYYYMMDD.iso`. Salvarlo in una posizione nota, ad esempio `\~/Downloads`.



### Creare la USB con Ventoy (metodo consigliato)



Ventoy è uno strumento che formatta la USB in modo da poter copiare le ISO direttamente come file, senza doverla riscrivere ogni volta che se ne cambia una. Scaricare Ventoy da `https://ventoy.net/en/download.html`, estrarre l'archivio e aprire un terminale nella cartella estratta.



Prima identificare quale dispositivo è la USB:



```bash

lsblk

```



Nell'output, trovare il dispositivo che corrisponde alla USB in base alla dimensione. Non confonderlo con `/dev/sda` (SSD interno del T450) né con dischi esterni. Installare Ventoy sulla USB — sostituire `/dev/sdX` con il dispositivo corretto:



```bash

sudo bash Ventoy2Disk.sh -i /dev/sdX

```



Ventoy crea due partizioni sulla USB. Montare la partizione grande (chiamata "Ventoy") e copiarci dentro il file ISO scaricato. Nessun altro passaggio necessario: Ventoy mostrerà un menu all'avvio con tutte le ISO presenti.



### Creare la USB con dd (metodo alternativo)



Se non si vuole usare Ventoy, `dd` scrive la ISO direttamente sulla USB sovrascrivendo tutto ciò che c'è senza chiedere conferma. Sostituire `/dev/sdX` con il dispositivo USB corretto:



```bash

sudo dd if=\~/Downloads/cachyos-x86\_64-\*.iso of=/dev/sdX bs=4M status=progress oflag=sync

```



Il parametro `status=progress` mostra l'avanzamento. Quando il comando termina e restituisce il prompt, la USB è pronta.



> **Attenzione dischi:** il disco interno è `/dev/sda` (238.5 GB, SSD) e il disco esterno è `/dev/sdb` (7.3 TB con array RAID `md127`). Nessuno dei due va toccato durante la creazione della USB. Il target di installazione di CachyOS sarà `/dev/sda`.



---



## 2. Configurazione BIOS



Prima di avviare dalla USB, il BIOS del T450 va configurato correttamente. Il firmware rilevato è **Lenovo JBET54WW v1.19 del 2015**. Prima di procedere, è consigliabile verificare su `https://support.lenovo.com` se esiste una versione più recente: cercare "ThinkPad T450 BIOS update" e seguire le istruzioni Lenovo.



### Accedere al BIOS



Spegnere completamente il T450 — non ibernazione, non sospensione, spegnimento completo. Premere il tasto di accensione e immediatamente, in modo ripetuto, premere **F1** fino a quando appare la schermata del BIOS. Se il sistema avvia normalmente senza mostrare il BIOS, riprovare: la finestra temporale è breve. Navigare con i tasti freccia.



### Modifiche da applicare



**Security → Secure Boot → Disabled.** Secure Boot impedisce l'avvio di sistemi operativi non firmati da Microsoft. CachyOS non ha la firma richiesta, quindi va disabilitato. Senza questa modifica la USB non si avvierà.



**Startup → UEFI/Legacy Boot → UEFI Only.** Il T450 supporta sia UEFI che il vecchio BIOS legacy. CachyOS va installato in modalità UEFI, che è lo standard moderno e permette il partizionamento GPT. "UEFI Only" elimina l'ambiguità.



**Startup → Boot Order.** Spostare "USB FDD" o "USB HDD" in prima posizione, prima del disco interno. Questo permette al T450 di avviare dalla USB quando è inserita.



**Config → Power → Wake on LAN → Disabled.** Funzione non necessaria che consuma energia in standby.



**Security → Anti-Theft → Disabled** (se presente). Va disabilitata per evitare conflitti durante l'installazione.



**Config → Display → Graphics Device.** Il T450 ha la NVIDIA 940M: se l'opzione è presente, lasciarla su **Hybrid Graphics** (o "Switchable") per mantenere la configurazione Optimus. Scegliere "Discrete only" solo se si vuole usare solo la NVIDIA, disabilitando permanentemente l'Intel — sconsigliato per l'autonomia.



Salvare ed uscire con **F10** → confermare con "Yes".



---



## 3. Avvio dalla USB e installazione con Calamares



### Avviare dalla USB



Inserire la USB. All'accensione del T450 apparirà il menu Ventoy (o l'avvio diretto se si è usato `dd`). Selezionare la ISO di CachyOS e attendere il caricamento del live environment. Se il sistema avvia dal disco interno, spegnere e riprovare, oppure premere **F12** appena acceso per il menu di avvio temporaneo.



### Scegliere il profilo al boot



All'avvio della ISO, CachyOS mostra un menu con voci come "CachyOS (open drivers)" e "CachyOS (proprietary NVIDIA)". Selezionare **la voce con i driver proprietari NVIDIA**: carica il modulo corretto per la 940M già nel live environment e riduce il rischio di schermo nero durante l'installazione.



### Partizioni



Una volta nel live environment, avviare Calamares dall'icona sul desktop. Seguire le schermate per lingua, fuso orario e tastiera, poi arrivare alla schermata **Partizioni**.



Scegliere **"Cancella disco"** e lasciare che Calamares gestisca tutto automaticamente: creerà la partizione EFI in FAT32, root e swap. Su questa schermata è possibile attivare la **cifratura LUKS** spuntando l'apposita opzione e inserendo una passphrase. Equivale alla configurazione LUKS+ext4 del sistema precedente, ma gestita interamente dall'installer senza configurazione manuale.



In alternativa, con il partizionamento manuale, lo schema consigliato per il disco da 238 GB è:



```

/dev/sda1  →  512 MB  → FAT32  → flag: esp  → mount: /boot/efi

/dev/sda2  →    1 GB  → ext4               → mount: /boot

/dev/sda3  →   60 GB+ → btrfs              → mount: /

/dev/sda4  →    4 GB  → swap

/dev/sda5  →  resto   → btrfs              → mount: /home

```



La partizione `/boot` separata da 1 GB è utile con LUKS: il kernel e GRUB devono essere leggibili prima che la cifratura venga sbloccata, quindi `/boot` rimane non cifrato mentre il resto è cifrato.



### Filesystem



Il filesystem consigliato è **btrfs**. CachyOS integra snapper per gli snapshot automatici, che permettono di tornare indietro in pochi secondi se un aggiornamento del kernel dovesse rompere qualcosa — su una distribuzione con aggiornamenti frequenti come CachyOS è una funzionalità concreta. I subvolumi standard sono `@` per `/`, `@home` per `/home`, `@log` per `/var/log`, `@cache` per `/var/cache` e `@tmp` per `/tmp`. Calamares li crea automaticamente se si sceglie btrfs con l'opzione subvolumi.



### Kernel



Nell'apposita schermata, scegliere **`linux-cachyos`**: include lo scheduler BORE/EEVDF ottimizzato per la reattività. L'i7-5500U supporta AVX2 (x86-64-v3): se l'installer propone la selezione del profilo di ottimizzazione, scegliere **x86-64-v3** per un miglioramento concreto rispetto al profilo generico.



Avviare l'installazione, attendere il completamento, rimuovere la USB quando richiesto e riavviare.



---



## 4. Post-installazione base



Al primo avvio, se è presente **CachyOS Hello**, eseguirlo: guida la configurazione iniziale e l'installazione di pacchetti comuni. È il punto di partenza ufficiale.



### Aggiornare il sistema



```bash

sudo pacman -Syu

```



`pacman` è il gestore pacchetti. Il flag `-S` installa o aggiorna, `-y` sincronizza il database dai mirror, `-u` aggiorna tutti i pacchetti installati. Va sempre eseguito per primo, prima di installare qualsiasi altra cosa, per evitare conflitti di dipendenze.



### Installare driver e firmware essenziali



```bash

sudo pacman -S linux-firmware intel-ucode \\

&#x20; thermald tlp tlp-rdw acpi\_call \\

&#x20; mesa lib32-mesa vulkan-intel lib32-vulkan-intel \\

&#x20; intel-media-driver libva-intel-driver libva-utils \\

&#x20; xf86-video-intel \\

&#x20; bluez bluez-utils networkmanager

```



- `linux-firmware`: firmware binari per l'hardware, incluso il firmware per il WiFi Intel 7265 (`iwlwifi`). Supportato nativamente, senza pacchetti aggiuntivi.

- `intel-ucode`: aggiornamenti microcode per la CPU Intel. Corregge bug della CPU caricati all'avvio. Per un i7-5500U (Broadwell) rilevante per sicurezza e stabilità.

- `thermald`: demone per il controllo termico. Usa i sensori per prevenire il throttling prima che il kernel debba intervenire d'urgenza.

- `tlp` + `tlp-rdw` + `acpi\_call`: gestione avanzata del risparmio energetico. TLP è il pacchetto principale. `tlp-rdw` gestisce i dispositivi radio in base alla fonte di alimentazione. `acpi\_call` è necessario per le soglie di carica delle batterie ThinkPad — senza di esso le soglie in `/etc/tlp.conf` non avranno effetto.

- `mesa` + `lib32-mesa`: driver OpenGL open-source per Intel.

- `vulkan-intel` + `lib32-vulkan-intel`: supporto Vulkan per l'Intel HD 5500. I pacchetti `lib32-\*` sono necessari per le applicazioni a 32 bit (ad esempio Steam).

- `intel-media-driver` + `libva-intel-driver` + `libva-utils`: accelerazione hardware per la decodifica video (VA-API). `intel-media-driver` è il driver moderno per Broadwell e successivi. `libva-utils` fornisce `vainfo` per verificare che funzioni.

- `xf86-video-intel`: driver X11 per la GPU Intel. Non necessario con Wayland, utile come fallback su X11.

- `bluez` + `bluez-utils`: stack Bluetooth. Il modulo Intel 8087:0a2a è supportato nativamente.

- `networkmanager`: gestione connessioni di rete. Probabilmente già installato da Calamares.



### Abilitare i servizi



Il flag `--now` avvia il servizio immediatamente, oltre ad abilitarlo per i boot futuri:



```bash

sudo systemctl enable --now thermald

sudo systemctl enable --now tlp

sudo systemctl enable --now NetworkManager

sudo systemctl enable --now bluetooth

```



### Aggiornare il microcode Intel



Il microcode viene caricato dal bootloader all'avvio. Dopo aver installato `intel-ucode`, il bootloader va informato. Prima verificare quale bootloader ha installato Calamares:



```bash

ls /boot/grub   2>/dev/null \&\& echo "→ GRUB installato"

ls /boot/loader 2>/dev/null \&\& echo "→ systemd-boot installato"

```



Se GRUB:



```bash

sudo grub-mkconfig -o /boot/grub/grub.cfg

```



Se systemd-boot:



```bash

sudo bootctl update

```



Riavviare, poi verificare che il microcode sia stato caricato:



```bash

grep -m1 "microcode" /proc/cpuinfo

```



L'output deve contenere un numero di revisione del microcode dopo la parola "microcode". Se la riga è vuota, il bootloader non è stato configurato correttamente — ripetere il comando corretto e riavviare.



---



## 5. Ottimizzazione CPU e risparmio energetico



### Configurare TLP



Il file di configurazione di TLP è `/etc/tlp.conf`. Aprirlo con `nano`:



```bash

sudo nano /etc/tlp.conf

```



In `nano`: navigare con le frecce, salvare con `Ctrl+O` poi `Invio`, uscire con `Ctrl+X`. Cercare le righe esistenti (alcune saranno commentate con `#`) o aggiungere in fondo al file:



```

CPU\_SCALING\_GOVERNOR\_ON\_AC=performance

CPU\_SCALING\_GOVERNOR\_ON\_BAT=powersave

CPU\_ENERGY\_PERF\_POLICY\_ON\_AC=performance

CPU\_ENERGY\_PERF\_POLICY\_ON\_BAT=balance\_power

CPU\_MIN\_PERF\_ON\_AC=0

CPU\_MAX\_PERF\_ON\_AC=100

CPU\_MIN\_PERF\_ON\_BAT=0

CPU\_MAX\_PERF\_ON\_BAT=60

SCHED\_POWERSAVE\_ON\_BAT=1

NMI\_WATCHDOG=0

PLATFORM\_PROFILE\_ON\_AC=performance

PLATFORM\_PROFILE\_ON\_BAT=low-power

DISK\_APM\_LEVEL\_ON\_AC=192

DISK\_APM\_LEVEL\_ON\_BAT=128

```



- `CPU\_SCALING\_GOVERNOR`: controlla come il kernel gestisce la frequenza della CPU. `performance` mantiene frequenza alta su corrente, `powersave` la abbassa su batteria.

- `CPU\_ENERGY\_PERF\_POLICY`: affina la preferenza tramite l'interfaccia EPP del processore, disponibile su Broadwell.

- `CPU\_MAX\_PERF\_ON\_BAT=60`: limita il turbo boost al 60% su batteria. Riduce consumi e calore senza impatto sulla fluidità quotidiana.

- `SCHED\_POWERSAVE\_ON\_BAT=1`: suggerisce al kernel di concentrare i task su meno core quando possibile su batteria.

- `NMI\_WATCHDOG=0`: disabilita il watchdog NMI, un meccanismo di controllo del kernel che consuma cicli CPU inutilmente su un laptop personale.

- `DISK\_APM\_LEVEL`: livello di risparmio energetico dell'SSD. 192 è conservativo su corrente, 128 più aggressivo su batteria.



Dopo aver salvato, applicare le modifiche senza riavviare:



```bash

sudo tlp start

```



### Parametri kernel per l'i7-5500U



Aprire il file di configurazione di GRUB:



```bash

sudo nano /etc/default/grub

```



Trovare la riga `GRUB\_CMDLINE\_LINUX\_DEFAULT`. Avrà un contenuto simile a `"quiet splash"`. Aggiungere i parametri all'interno delle virgolette, separati da spazi, senza andare a capo:



```

GRUB\_CMDLINE\_LINUX\_DEFAULT="quiet splash intel\_idle.max\_cstate=4 intel\_pstate=active i915.enable\_fbc=1 i915.enable\_psr=1 i915.enable\_rc6=1 nowatchdog nmi\_watchdog=0"

```



- `intel\_idle.max\_cstate=4`: limita gli stati di idle della CPU al C4, evitando stati profondi che su Broadwell possono causare latenze di risveglio elevate.

- `intel\_pstate=active`: attiva la gestione della frequenza tramite il driver Intel P-state, più efficiente del driver generico `acpi-cpufreq` su Broadwell.

- `i915.enable\_fbc=1`: abilita la Framebuffer Compression dell'iGPU. Riduce i consumi quando il contenuto dello schermo non cambia.

- `i915.enable\_psr=1`: Panel Self Refresh — il display si aggiorna autonomamente senza coinvolgere la GPU quando il frame non cambia.

- `i915.enable\_rc6=1`: mette la GPU in stati di basso consumo quando non è utilizzata.

- `nowatchdog` + `nmi\_watchdog=0`: disabilita i watchdog del kernel, applicato prima che TLP parta.



Dopo aver salvato, rigenerare la configurazione GRUB:



```bash

sudo grub-mkconfig -o /boot/grub/grub.cfg

```



Questo comando legge `/etc/default/grub` e scrive la configurazione finale in `/boot/grub/grub.cfg`. Le modifiche saranno attive al prossimo riavvio.



> **Nota su `mitigations=off`:** aggiungere questo parametro disabilita le patch software per Spectre e Meltdown, vulnerabilità che affliggono l'i7-5500U. Il guadagno in performance è reale (circa 10–15%) ma aumenta il rischio di sicurezza. Sconsigliato se il laptop si connette a reti WiFi pubbliche o non fidate.



### Monitoraggio temperature



Il sistema espone già i sensori `thinkpad-isa-0000` e `coretemp`. Installare gli strumenti:



```bash

sudo pacman -S s-tui stress lm\_sensors

sudo sensors-detect --auto

```



`sensors-detect` rileva i sensori hardware e li configura. Il flag `--auto` risponde "sì" a tutte le domande senza input manuale. Dopo l'esecuzione, `sensors` mostra le temperature. `s-tui` è un'interfaccia interattiva che mostra frequenze, temperature e utilizzo CPU in tempo reale in un unico pannello.



---



## 6. GPU: Intel HD 5500 + NVIDIA 940M (Optimus)



Questo è il passaggio più delicato. Il T450 ha due GPU: Intel HD Graphics 5500 (iGPU, integrata nella CPU) e NVIDIA GeForce 940M — chip GM108M, architettura Maxwell — (dGPU). Questa configurazione si chiama NVIDIA Optimus: l'iGPU gestisce il display e il rendering quotidiano, la dGPU viene attivata per i carichi grafici intensi.



Non installare `bumblebee`: è un progetto abbandonato, incompatibile con i kernel recenti e con Wayland.



### Passo obbligatorio: verificare quale driver ha installato CachyOS



Dal maggio 2025, CachyOS tenta di rilevare automaticamente la GPU e installare il driver corretto. Tuttavia, per le schede Maxwell in configurazione Optimus è documentato un bug per cui lo strumento `chwd` installa `nvidia-open-dkms` (driver 590xx, per GPU Turing e successive) invece del corretto `nvidia-580xx-dkms`. Il 590xx non supporta Maxwell: se viene installato, il sistema può avviarsi con schermo nero.



Verificare subito dopo il primo avvio, **prima di qualsiasi altra configurazione GPU**:



```bash

pacman -Q | grep -i nvidia

```



Leggere l'output:



- Compare `nvidia-580xx-dkms`: corretto, CachyOS ha rilevato correttamente la Maxwell. Passare direttamente alla sezione "Configurazione Optimus".

- Compare `nvidia-open-dkms` oppure `nvidia-dkms` senza il suffisso `580xx`: sbagliato, va sostituito.

- Non compare nulla: nessun driver installato, va installato manualmente.



### Correggere il driver sbagliato



Rimuovere il driver incompatibile. I comandi usano `2>/dev/null` per sopprimere i messaggi di errore se qualche pacchetto non è presente:



```bash

sudo pacman -Rns nvidia-open-dkms 2>/dev/null

sudo pacman -Rns nvidia-dkms 2>/dev/null

sudo pacman -Rns nvidia-utils lib32-nvidia-utils 2>/dev/null

```



Installare il driver Maxwell corretto dai repository CachyOS:



```bash

sudo pacman -S nvidia-580xx-dkms nvidia-580xx-utils lib32-nvidia-580xx-utils

```



Se `pacman` risponde "target not found", il pacchetto non è nei repo ufficiali in quel momento. Installarlo dall'AUR. Prima installare `yay` se non è già presente:



```bash

sudo pacman -S --needed base-devel git

git clone https://aur.archlinux.org/yay.git

cd yay

makepkg -si

```



Poi installare il driver:



```bash

yay -S nvidia-580xx-dkms nvidia-580xx-utils lib32-nvidia-580xx-utils

```



Il pacchetto AUR è mantenuto da *ventureo* del team CachyOS — è la fonte di riferimento ufficiale per Maxwell e Pascal su Arch.



Rigenerare gli initramfs e riavviare:



```bash

sudo mkinitcpio -P

sudo reboot

```



`mkinitcpio -P` rigenera tutte le immagini di avvio iniziale del kernel, includendo il nuovo modulo NVIDIA. Senza questo passaggio il modulo potrebbe non caricarsi correttamente al boot.



### Recupero da schermo nero o TTY



Se all'avvio il sistema non mostra l'ambiente grafico, accedere alla TTY con `Ctrl+Alt+F2` (o F3, F4). Inserire nome utente e password. Da lì si opera normalmente da riga di comando.



Opzione 1 — disabilitare l'avvio grafico temporaneamente, installare il driver corretto, poi ripristinare:



```bash

sudo systemctl set-default multi-user.target

\# installare il driver corretto come sopra

sudo systemctl set-default graphical.target

sudo reboot

```



Opzione 2 — usare `nomodeset` da GRUB. Al menu GRUB, premere **`e`** sulla voce di avvio. Trovare la riga che inizia con `linux` e aggiungere `nomodeset` alla fine prima di `--`. Premere `Ctrl+X` per avviare. Una volta nel sistema, installare il driver corretto, poi aprire `/etc/default/grub`, rimuovere `nomodeset` e rigenerare GRUB.



### Configurazione Optimus: Opzione A — nvidia-prime (consigliata)



Con nvidia-prime, l'iGPU Intel gestisce sempre il display. La 940M si attiva solo esplicitamente tramite il prefisso `prime-run`. È la configurazione con il miglior equilibrio tra prestazioni e autonomia.



```bash

sudo pacman -S nvidia-580xx-dkms nvidia-580xx-utils lib32-nvidia-580xx-utils \\

&#x20; nvidia-prime mesa lib32-mesa \\

&#x20; vulkan-intel lib32-vulkan-intel \\

&#x20; intel-media-driver libva-intel-driver

```



Verificare che il modulo sia caricato:



```bash

lsmod | grep nvidia

```



L'output deve mostrare `nvidia`, `nvidia\_drm`, `nvidia\_modeset`. Per usare la 940M su un'applicazione specifica:



```bash

prime-run nome-applicazione

\# esempi concreti:

prime-run glxgears

prime-run blender

prime-run steam

```



### Configurazione Optimus: Opzione B — optimus-manager



Permette di cambiare la GPU attiva in modo persistente, senza `prime-run` per ogni applicazione. Richiede il riavvio del display manager a ogni switch — salvare il lavoro prima di usarlo.



```bash

yay -S optimus-manager optimus-manager-qt

sudo systemctl enable --now optimus-manager

```



`optimus-manager-qt` aggiunge un'icona nel system tray per cambiare GPU graficamente. Da terminale:



```bash

optimus-manager --switch intel    # usa solo l'iGPU Intel (massima autonomia)

optimus-manager --switch nvidia   # usa solo la dGPU 940M (massima performance)

optimus-manager --switch hybrid   # Optimus automatico

```



### Risparmio energetico: spegnere la 940M quando non è in uso



Anche con nvidia-prime, la 940M può rimanere alimentata in idle consumando 3–5W. Per abilitare il runtime power management, aggiungere in `/etc/tlp.conf`:



```

RUNTIME\_PM\_ON\_AC=auto

RUNTIME\_PM\_ON\_BAT=auto

```



Con questa impostazione TLP istruisce il kernel a spegnere i dispositivi PCI inattivi, inclusa la 940M. Si riaccenderà automaticamente quando si usa `prime-run`.



### Configurazione iGPU Intel per X11



Su X11 (non Wayland), creare il file di configurazione:



```bash

sudo nano /etc/X11/xorg.conf.d/20-intel.conf

```



Inserire:



```

Section "Device"

&#x20; Identifier "Intel Graphics"

&#x20; Driver "intel"

&#x20; Option "TearFree" "true"

&#x20; Option "AccelMethod" "sna"

&#x20; Option "DRI" "3"

EndSection

```



`TearFree` elimina il tearing video. `AccelMethod sna` è il metodo più stabile per HD 5500. Su Wayland questo file non è necessario.



### Verificare che tutto funzioni



```bash

\# Accelerazione hardware video Intel:

vainfo

\# Deve mostrare VAEntrypointVLD (decodifica) e VAEntrypointEncSlice (codifica)



\# GPU attiva di default:

glxinfo | grep "OpenGL renderer"

\# Deve mostrare "Intel HD Graphics 5500"



\# GPU con prime-run:

prime-run glxinfo | grep "OpenGL renderer"

\# Deve mostrare "GeForce 940M"

```



---



## 7. Batteria (doppia)



Il T450 supporta due batterie contemporaneamente: BAT0 (interna) e BAT1 (esterna nella bay anteriore). Entrambe rilevate e funzionanti. Stato misurato: BAT0 a 18.21 Wh su 23.2 Wh di design (78.5% di capacità residua), BAT1 a 19.88 Wh su 23.2 Wh (85.7%). TLP gestisce automaticamente l'ordine di scarica. Al momento del rilevamento il drain era 18W a riposo — con le ottimizzazioni descritte dovrebbe scendere a 8–12W, per un'autonomia stimata di 3–4 ore.



### Soglie di carica



Tenere le batterie costantemente al 100% accelera la degradazione chimica. Le soglie di carica limitano il range di carica per preservare la durata nel tempo. Aprire `/etc/tlp.conf` e aggiungere o modificare:



```

START\_CHARGE\_THRESH\_BAT0=75

STOP\_CHARGE\_THRESH\_BAT0=80

START\_CHARGE\_THRESH\_BAT1=75

STOP\_CHARGE\_THRESH\_BAT1=80

```



Con questa configurazione TLP avvia la carica solo quando la batteria scende sotto il 75% e la interrompe all'80%. Funziona perché `acpi\_call` permette a TLP di comunicare direttamente con il firmware ThinkPad per controllare il circuito di carica — senza `acpi\_call` installato queste righe non avrebbero effetto.



Applicare le modifiche:



```bash

sudo tlp start

```



### Powertop — analisi e ottimizzazione dei consumi



```bash

sudo pacman -S powertop



\# Ottimizzazione automatica una tantum:

sudo powertop --auto-tune



\# Analisi interattiva in tempo reale:

sudo powertop

```



Nell'interfaccia interattiva, la scheda "Tunables" mostra le impostazioni con stato "Bad" o "Good". Premere `Tab` per navigare tra le schede, `Invio` per attivare una voce "Bad". Per rendere l'auto-tune permanente ad ogni avvio, creare un servizio systemd:



```bash

sudo nano /etc/systemd/system/powertop.service

```



Inserire:



```

\[Unit]

Description=Powertop auto-tune

After=multi-user.target



\[Service]

Type=oneshot

ExecStart=/usr/bin/powertop --auto-tune



\[Install]

WantedBy=multi-user.target

```



```bash

sudo systemctl enable powertop

```



### Verificare lo stato delle batterie



```bash

\# Riepilogo completo con soglie di carica attive:

tlp-stat -b



\# Dettagli singola batteria (energia, capacità, tasso di scarica):

upower -i /org/freedesktop/UPower/devices/battery\_BAT0

upower -i /org/freedesktop/UPower/devices/battery\_BAT1

```



---



## 8. SSD, filesystem e RAM



### TRIM



Il TRIM segnala all'SSD quali blocchi non sono più in uso, permettendo al controller di gestirli internamente. Senza TRIM le performance degradano nel tempo. `fstrim.timer` esegue un TRIM sull'intero filesystem settimanalmente:



```bash

sudo systemctl enable --now fstrim.timer

```



Per verificare che il timer sia attivo e quando verrà eseguito:



```bash

systemctl status fstrim.timer

```



### noatime nel filesystem



Ogni volta che un file viene letto, Linux per default aggiorna il campo "atime" (access time) dei metadati. Su un SSD queste scritture continue consumano cicli di scrittura inutilmente. `noatime` le disabilita.



Aprire `/etc/fstab`:



```bash

sudo nano /etc/fstab

```



Trovare la riga che monta la partizione root (`/`) e aggiungere `noatime` alle opzioni. Non modificare il valore `UUID=xxxx`, che è già corretto. Il risultato dipende dal filesystem scelto:



```

\# Per ext4:

UUID=xxxx  /  ext4   defaults,noatime,errors=remount-ro  0 1



\# Per btrfs (con compressione zstd):

UUID=xxxx  /  btrfs  defaults,noatime,compress=zstd:1,subvol=@  0 0

```



Con btrfs, `compress=zstd:1` attiva la compressione trasparente al livello più veloce. Su file di testo, codice e documenti riduce l'occupazione su disco del 20–40% senza impatto percettibile sulle prestazioni.



### zRAM



CachyOS installa `zram-generator` di default. zRAM crea un dispositivo di swap in RAM compressa: invece di scrivere su disco, usa RAM compressa che è ordini di grandezza più veloce. Verificare la configurazione:



```bash

cat /etc/systemd/zram-generator.conf

```



La configurazione ottimale per 16 GB di RAM è:



```

\[zram0]

zram-size = ram / 2

compression-algorithm = zstd

```



Se il file non esiste o ha valori diversi, crearlo o modificarlo, poi ricaricare:



```bash

sudo systemctl daemon-reload

sudo systemctl restart systemd-zram-setup@zram0.service

```



### Parametri sysctl



Creare un file di configurazione dedicato:



```bash

sudo nano /etc/sysctl.d/99-performance.conf

```



Inserire:



```

vm.swappiness=10

vm.vfs\_cache\_pressure=50

vm.dirty\_ratio=10

vm.dirty\_background\_ratio=5

kernel.nmi\_watchdog=0

```



- `vm.swappiness=10`: usa la swap solo quando la RAM libera scende sotto il 10%. Il valore default è 60, che causa swap prematura. Con 16 GB un valore basso è corretto.

- `vm.vfs\_cache\_pressure=50`: riduce la tendenza del kernel a liberare la cache del filesystem dalla memoria, migliorando le performance di I/O per file acceduti frequentemente.

- `vm.dirty\_ratio=10` e `vm.dirty\_background\_ratio=5`: controllano la soglia di dati "sporchi" (modificati ma non ancora scritti su disco). Valori bassi significano flush più frequenti e prevedibili, riducendo i picchi di latenza.

- `kernel.nmi\_watchdog=0`: già presente nei parametri kernel di GRUB, qui come garanzia aggiuntiva.



Applicare immediatamente senza riavviare:



```bash

sudo sysctl --system

```



### IRQ balance



`irqbalance` distribuisce le interruzioni hardware tra i core della CPU. Senza di esso, tutte le interruzioni vengono gestite dal core 0, creando un collo di bottiglia. Con i 4 thread dell'i7-5500U il beneficio è modesto ma misurabile in scenari di I/O intensivo:



```bash

sudo pacman -S irqbalance

sudo systemctl enable --now irqbalance

```





