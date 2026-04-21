---
title: "CachyOS su ThinkPad T450: guida all'installazione e configurazione"
date: 2026-04-21
tags: [thinkpad, cachyos, linux, nvidia, optimus]
description: Guida completa e personalizzata per installare CachyOS su ThinkPad T450 con i7-5500U, 16GB DDR3, Intel HD 5500 + NVIDIA 940M e doppia batteria.
---

Questa guida è calibrata sull'hardware specifico di questo T450, rilevato con `lscpu`, `lspci`, `upower` e `lsblk`. Le specifiche di riferimento sono: Intel Core i7-5500U (Broadwell, 2 core / 4 thread, boost 3.0 GHz), 16 GB DDR3 1600 MT/s in dual channel, Intel HD Graphics 5500 + NVIDIA GeForce 940M (Optimus), SSD SATA da 238.5 GB, doppia batteria SANYO e Intel Wireless 7265.

## 1. Preparazione — USB bootable

Scarica la ISO di CachyOS da `https://cachyos.org/download`. Scegli la versione **x86_64**. Per creare la USB, Ventoy è il metodo consigliato perché permette di avere più ISO sullo stesso disco:

```bash
# Sostituisci /dev/sdX con il tuo USB
sudo bash Ventoy2Disk.sh -i /dev/sdX
# poi copia la ISO nella partizione Ventoy
```

In alternativa con `dd`:

```bash
sudo dd if=cachyos-*.iso of=/dev/sdX bs=4M status=progress oflag=sync
```

Attenzione: il disco interno rilevato è `/dev/sda` (238.5 GB). Il dispositivo `/dev/sdb` da 7.3 TB con array RAID software (`md127`) non va toccato — assicurati che l'installer punti solo a `/dev/sda`.

## 2. Configurazione BIOS

Accedi al BIOS con **F1** all'avvio. Il firmware rilevato è **JBET54WW v1.19 (2015)** — vale la pena verificare su `support.lenovo.com` se esiste un aggiornamento prima di procedere. Il T450 non ha un modulo TPM fisico separato, il che non crea problemi per l'installazione.

Le impostazioni da modificare sono:

* Security → Secure Boot → **Disabled**
* Startup → UEFI/Legacy Boot → **UEFI Only**
* Startup → Boot Order → USB FDD/USB HDD al primo posto
* Config → Power → Wake on LAN → **Disabled**
* Security → Anti-Theft → **Disabled** (se presente)

Questo T450 ha la NVIDIA 940M. Sotto Config → Display, se esiste l'opzione "Hybrid Graphics" / "Discrete Graphics", lasciarla su **Hybrid** per usare Optimus. Scegliere "Discrete only" solo se si vuole disabilitare permanentemente l'iGPU Intel.

## 3. Installazione con Calamares

CachyOS usa l'installer Calamares. Nella schermata "Partizioni" si può scegliere **"Cancella disco"** e lasciare che Calamares gestisca tutto automaticamente — creerà la partizione EFI in FAT32, root e swap. La cifratura LUKS è attivabile direttamente da quella schermata senza configurazione manuale.

In alternativa, uno schema manuale consigliato per l'SSD da 238 GB è:

```
/boot/efi  →  512 MB  → FAT32  → EFI System Partition
/boot      →    1 GB  → ext4   → utile con LUKS
/          →   60 GB+ → btrfs o ext4
swap       →    4 GB  → swap
/home      →  resto   → btrfs o ext4
```

Il filesystem consigliato è **btrfs con subvolumi** (`@`, `@home`, `@log`, `@cache`, `@tmp`): CachyOS supporta snapper nativamente, che permette rollback istantaneo in caso di aggiornamenti kernel problematici — rilevante su una distribuzione con kernel aggiornati frequentemente come questa.

Per il kernel, scegliere **`linux-cachyos`** (scheduler BORE/EEVDF). L'i7-5500U supporta AVX2 (x86-64-v3): se l'installer propone la selezione del profilo di ottimizzazione, scegliere **x86-64-v3** per un incremento di performance reale rispetto al profilo generico.

## 4. Post-installazione base

Dopo il primo avvio, aggiornare il sistema — se è presente CachyOS Hello, eseguirlo prima di qualsiasi altra cosa:

```bash
sudo pacman -Syu
```

I pacchetti essenziali per questo hardware sono:

```bash
sudo pacman -S linux-firmware intel-ucode \
  thermald tlp tlp-rdw acpi_call \
  mesa lib32-mesa vulkan-intel lib32-vulkan-intel \
  intel-media-driver libva-intel-driver libva-utils \
  xf86-video-intel \
  bluez bluez-utils networkmanager
```

Il WiFi Intel 7265 è supportato nativamente dal driver `iwlwifi` incluso in `linux-firmware` — non servono pacchetti aggiuntivi. Abilitare i servizi essenziali:

```bash
sudo systemctl enable --now thermald tlp NetworkManager bluetooth
```

**Microcode Intel.** Calamares sceglie il bootloader durante l'installazione. Verificare quale è stato installato prima di usare il comando corretto:

```bash
ls /boot/grub   2>/dev/null && echo "→ GRUB"
ls /boot/loader 2>/dev/null && echo "→ systemd-boot"

# Se GRUB:
sudo grub-mkconfig -o /boot/grub/grub.cfg

# Se systemd-boot:
sudo bootctl update

# Verifica che il microcode sia caricato:
grep -m1 "microcode" /proc/cpuinfo
```

## 5. Ottimizzazione CPU e risparmio energetico

L'i7-5500U ha un TDP di 15W e a riposo è stato rilevato a 57°C di package con la ventola a 3479 RPM — valori nella norma. Se sotto carico leggero si superano i 75°C, potrebbe valere la pena rinnovare il thermal paste.

Aggiungere o modificare in `/etc/tlp.conf`:

```
CPU_SCALING_GOVERNOR_ON_AC=performance
CPU_SCALING_GOVERNOR_ON_BAT=powersave
CPU_ENERGY_PERF_POLICY_ON_AC=performance
CPU_ENERGY_PERF_POLICY_ON_BAT=balance_power
CPU_MIN_PERF_ON_AC=0
CPU_MAX_PERF_ON_AC=100
CPU_MIN_PERF_ON_BAT=0
CPU_MAX_PERF_ON_BAT=60
SCHED_POWERSAVE_ON_BAT=1
NMI_WATCHDOG=0
PLATFORM_PROFILE_ON_AC=performance
PLATFORM_PROFILE_ON_BAT=low-power
DISK_APM_LEVEL_ON_AC=192
DISK_APM_LEVEL_ON_BAT=128
```

Aggiungere i seguenti parametri kernel in `/etc/default/grub` alla riga `GRUB_CMDLINE_LINUX_DEFAULT`, poi rigenerare con `sudo grub-mkconfig -o /boot/grub/grub.cfg`:

```
intel_idle.max_cstate=4 intel_pstate=active i915.enable_fbc=1
i915.enable_psr=1 i915.enable_rc6=1 nowatchdog nmi_watchdog=0
```

Il parametro `mitigations=off` è disponibile e offre circa 10–15% di performance in più, ma disabilita le patch Spectre/Meltdown. Non è consigliato se il laptop si connette a reti non fidate.

Per il monitoraggio in tempo reale:

```bash
sudo pacman -S s-tui stress lm_sensors
sudo sensors-detect --auto
s-tui
```

## 6. GPU: Intel HD 5500 + NVIDIA 940M (Optimus)

Questo T450 ha entrambe le GPU: Intel HD Graphics 5500 come iGPU e NVIDIA GeForce 940M (GM108M, architettura Maxwell) come dGPU. Serve configurare Optimus. Non installare `bumblebee`, che è deprecato e non funziona sui kernel recenti.

### Verifica del driver installato da CachyOS

Dall'ISO di maggio 2025, CachyOS rileva automaticamente la GPU e carica il modulo proprietario corretto. Tuttavia, per schede Maxwell in configurazione Optimus, è stato segnalato un bug per cui `chwd` installa `nvidia-open-dkms` (590xx, incompatibile con Maxwell) invece del corretto `nvidia-580xx-dkms`. Verificare subito al primo avvio:

```bash
pacman -Q | grep -i nvidia
```

Il risultato corretto contiene `nvidia-580xx-dkms`. Se invece compare `nvidia-open-dkms` o `nvidia-dkms` senza il suffisso `580xx`, il driver installato non supporta la 940M e il sistema potrebbe non avviare l'ambiente grafico.

**Se il driver è errato**, rimuoverlo e installare quello corretto:

```bash
# Rimuovi il driver incompatibile:
sudo pacman -Rns nvidia-open-dkms nvidia-utils lib32-nvidia-utils 2>/dev/null
sudo pacman -Rns nvidia-dkms nvidia-utils lib32-nvidia-utils 2>/dev/null

# Installa il driver Maxwell corretto:
sudo pacman -S nvidia-580xx-dkms nvidia-580xx-utils lib32-nvidia-580xx-utils

# Rigenera i moduli kernel e riavvia:
sudo mkinitcpio -P
sudo reboot
```

Se `nvidia-580xx-dkms` non è nei repo ufficiali, installarlo dall'AUR — il pacchetto è mantenuto da *ventureo* del team CachyOS ed è la fonte ufficiale di riferimento per Maxwell/Pascal su Arch:

```bash
yay -S nvidia-580xx-dkms nvidia-580xx-utils lib32-nvidia-580xx-utils
sudo mkinitcpio -P && sudo reboot
```

**Se l'ambiente grafico non si avvia (schermo nero / TTY)**, accedere con `Ctrl+Alt+F2` e usare una di queste opzioni:

```bash
# Opzione 1 — avvia senza DE, installa il driver corretto, poi ripristina:
sudo systemctl set-default multi-user.target
# ... installa driver come sopra ...
sudo systemctl set-default graphical.target

# Opzione 2 — da GRUB, premere 'e' e aggiungere "nomodeset" ai parametri kernel,
# poi installare il driver corretto e rimuovere nomodeset.
```

### Configurazione Optimus

**Opzione A — nvidia-prime (consigliata).** L'iGPU Intel gestisce sempre il display; la 940M viene attivata solo per le app che lo richiedono con il prefisso `prime-run`. È la scelta migliore per l'autonomia:

```bash
sudo pacman -S nvidia-580xx-dkms nvidia-580xx-utils lib32-nvidia-580xx-utils \
  nvidia-prime mesa lib32-mesa vulkan-intel lib32-vulkan-intel \
  intel-media-driver libva-intel-driver

# Uso della 940M per un'app specifica:
prime-run <nome-applicazione>
```

**Opzione B — optimus-manager.** Permette di switchare tra Intel, NVIDIA e modalità ibrida con un comando (richiede riavvio del display manager):

```bash
yay -S optimus-manager optimus-manager-qt
sudo systemctl enable --now optimus-manager

optimus-manager --switch intel    # solo iGPU
optimus-manager --switch nvidia   # solo dGPU
optimus-manager --switch hybrid   # Optimus automatico
```

Per spegnere la 940M quando non è in uso, aggiungere in `/etc/tlp.conf`:

```
RUNTIME_PM_ON_AC=auto
RUNTIME_PM_ON_BAT=auto
```

Con la 940M in `power/control=auto`, la GPU discreta si spegne automaticamente riducendo i consumi di 3–5W.

**Configurazione iGPU per X11** (non necessaria su Wayland):

```bash
sudo nano /etc/X11/xorg.conf.d/20-intel.conf
```

```
Section "Device"
  Identifier "Intel Graphics"
  Driver "intel"
  Option "TearFree" "true"
  Option "AccelMethod" "sna"
  Option "DRI" "3"
EndSection
```

Per verificare l'accelerazione hardware e quale GPU è attiva:

```bash
vainfo
glxinfo | grep "OpenGL renderer"
prime-run glxinfo | grep "OpenGL renderer"
```

## 7. Batteria (doppia)

Entrambe le batterie sono funzionanti. Stato rilevato: BAT0 (interna) a 18.21 Wh su 23.2 Wh di design, capacità residua 78.5%; BAT1 (esterna) a 19.88 Wh su 23.2 Wh, capacità residua 85.7%. Autonomia totale stimata intorno a 3–4 ore in uso misto con la 940M spenta. Al momento del rilevamento il drain era 18W a riposo — con TLP, powertop e 940M in auto-suspend si dovrebbe scendere a 8–12W.

Soglie di carica consigliate in `/etc/tlp.conf` per preservare le batterie già parzialmente degradate:

```
START_CHARGE_THRESH_BAT0=75
STOP_CHARGE_THRESH_BAT0=80
START_CHARGE_THRESH_BAT1=75
STOP_CHARGE_THRESH_BAT1=80
```

Per l'analisi e l'ottimizzazione dei consumi:

```bash
sudo pacman -S powertop
sudo powertop --auto-tune
sudo powertop   # analisi interattiva
```

Per eseguire l'auto-tune di powertop ad ogni avvio, creare `/etc/systemd/system/powertop.service`:

```
[Unit]
Description=Powertop auto-tune
After=multi-user.target

[Service]
Type=oneshot
ExecStart=/usr/bin/powertop --auto-tune

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable powertop
```

Per verificare lo stato delle batterie:

```bash
tlp-stat -b
upower -i /org/freedesktop/UPower/devices/battery_BAT0
upower -i /org/freedesktop/UPower/devices/battery_BAT1
```

## 8. SSD, filesystem e RAM

Il disco rilevato è un SSD SATA da 238.5 GB (ROTA=0 confermato), senza NVMe. Abilitare il TRIM schedulato:

```bash
sudo systemctl enable --now fstrim.timer
```

Aggiungere `noatime` in `/etc/fstab` per ridurre le scritture inutili:

```
# Per ext4:
UUID=xxxx  /  ext4   defaults,noatime,errors=remount-ro  0 1

# Per btrfs:
UUID=xxxx  /  btrfs  defaults,noatime,compress=zstd:1,subvol=@  0 0
```

CachyOS installa `zram-generator` di default. Con 16 GB di RAM, la configurazione ottimale in `/etc/systemd/zram-generator.conf` è:

```
[zram0]
zram-size = ram / 2
compression-algorithm = zstd
```

Parametri sysctl in `/etc/sysctl.d/99-performance.conf`:

```
vm.swappiness=10
vm.vfs_cache_pressure=50
vm.dirty_ratio=10
vm.dirty_background_ratio=5
kernel.nmi_watchdog=0
```

```bash
sudo sysctl --system
sudo pacman -S irqbalance
sudo systemctl enable --now irqbalance
```

Il disco esterno `/dev/sdb` (7.3 TB, con array `md127`) non viene toccato dall'installer se si installa solo su `/dev/sda`. Se lo si vuole rimontare su CachyOS, verificare la configurazione `/etc/fstab` e `/etc/mdadm.conf` dopo l'installazione.
