---
title: Synctrain - Automazione iOS
date: 2026-04-14
tags: \[iOS]
description: Come mantenere sincronizzati i file su iOS con Synctrain e Comandi Rapidi

---

# 

# Synctrain su iPhone: Automazione Completa con Tailscale

Guida per configurare un Comando Rapido su iPhone che sincronizza file grandi (1–2 GB) tramite Synctrain e Tailscale, con avvio automatico all'apertura dell'app e quando l'iPhone è collegato all'alimentazione.

\
---

## Requisiti

Prima di iniziare, verifica di avere installato e configurato:

* **Synctrain** — app per Syncthing su iOS, con almeno una cartella già condivisa
* **Tailscale** — VPN mesh, già connessa e funzionante
* **Comandi Rapidi** — app nativa Apple (preinstallata da iOS 13+)
* iPhone connesso al Wi-Fi durante la sincronizzazione
* iOS 16 o successivo per le automazioni senza richiesta di conferma

\---

## Struttura del Comando Rapido

Il flusso è costruito attorno a un blocco **Ripeti 200 volte**, che mantiene Synctrain attivo abbastanza a lungo da completare trasferimenti da 1–2 GB.

```
Ripeti 200 volte
    Connect to your Tailscale network
    Attendi 5 secondi
    Riscansiona cartella          ← azione Synctrain
    Sincronizza per un po'        ← azione Synctrain (15 secondi)
Fine Ripeti
```

### Calcolo del tempo totale

| Azione per ciclo       | Durata stimata     |
| ---------------------- | ------------------ |
| Connect to Tailscale   | \~1–2 s            |
| Attendi                | 5 s                |
| Riscansiona cartella   | \~1–2 s            |
| Sincronizza per un po' | 15 s               |
| **Totale per ciclo**   | **\~23–24 s**      |
| **200 cicli**          | **\~75–80 minuti** |

Per file più piccoli puoi ridurre il numero di ripetizioni (es. 60–80 per file da 200–500 MB).

\---

## Come Creare il Comando Rapido

### 1\. Crea un nuovo comando

Apri **Comandi Rapidi** → tocca **+** in alto a destra → tocca **Aggiungi azione**.

### 2\. Aggiungi il blocco Ripeti

* Cerca `Ripeti` nel campo di ricerca azioni
* Seleziona **Ripeti**
* Imposta il numero di ripetizioni su **200**

### 3\. Dentro Ripeti — aggiungi Tailscale

* Tocca **+** dentro il blocco Ripeti
* Cerca `Tailscale` → seleziona **Connect to your Tailscale network**

### 4\. Aggiungi l'attesa

* Tocca **+** sotto Tailscale
* Cerca `Attendi` → seleziona **Attendi**
* Imposta su **5 secondi**

### 5\. Aggiungi la scansione Synctrain

* Tocca **+** → cerca `Synctrain` o `Riscansiona`
* Seleziona **Riscansiona cartella**
* Se richiesto, scegli la cartella desiderata

### 6\. Aggiungi la sincronizzazione Synctrain

* Tocca **+** → cerca `Sincronizza per un po'`
* Seleziona l'azione **Sincronizza per un po'** di Synctrain
* Imposta la durata su **15 secondi**

### 7\. Verifica l'ordine e salva

Controlla che l'ordine dentro il blocco Ripeti sia esattamente:

```
Ripeti 200 volte
    ① Connect to your Tailscale network
    ② Attendi — 5 secondi
    ③ Riscansiona cartella
    ④ Sincronizza per un po' — 15 secondi
Fine Ripeti
```

Tocca **Fine** in alto a destra e assegna un nome al comando, ad esempio:

> `Synctrain — File Grandi`

\---

## Configurare le Automazioni

Le automazioni consentono di avviare il comando **senza toccare nulla**. Devi creare **due automazioni separate**: una per l'apertura dell'app, una per il collegamento all'alimentazione.

\---

### Automazione 1 — Apertura e Riapertura di Synctrain

Questa automazione si attiva ogni volta che apri Synctrain (prima apertura o ritorno in foreground).

#### Passaggi

1. Apri **Comandi Rapidi** → scheda **Automazione** (icona orologio in basso)

2. Tocca **+** in alto a destra

3. Seleziona **App** come tipo di trigger

4. Tocca **Scegli** accanto ad App → cerca e seleziona **Synctrain**

5. Spunta entrambe le opzioni:
   
   * ✅ **L'app è aperta**
   * ✅ **L'app è chiusa** *(opzionale — utile per avviare un ciclo anche dopo aver usato l'app)*

6. Tocca **Avanti**

7. Tocca **Nuova azione vuota** → cerca il comando `Synctrain — File Grandi` che hai appena creato → selezionalo

8. Tocca **Avanti** → disattiva **"Chiedi prima di eseguire"** se disponibile

9. Tocca **Fine**

> \*\*Nota:\*\* Su iOS 16 e successivi le automazioni personali possono essere eseguite automaticamente senza conferma. Se il toggle non è disponibile, significa che iOS richiede sempre una notifica di conferma (la puoi eseguire con un tap sulla notifica).

\---

### Automazione 2 — iPhone Collegato all'Alimentazione

Questa automazione si attiva non appena colleghi il cavo o il caricabatterie, avviando la sincronizzazione in background.

#### Passaggi

1. Apri **Comandi Rapidi** → scheda **Automazione** → tocca **+**

2. Seleziona **Caricabatterie** come tipo di trigger

3. Spunta:
   
   * ✅ **È collegato**

4. Tocca **Avanti**

5. Tocca **Nuova azione vuota** → seleziona il comando `Synctrain — File Grandi`

6. Tocca **Avanti** → disattiva **"Chiedi prima di eseguire"** se disponibile

7. Tocca **Fine**

> Puoi anche spuntare \*\*"Non è collegato"\*\* se vuoi interrompere o gestire qualcosa alla disconnessione, ma per questo caso d'uso è sufficiente il trigger di collegamento.

\---

## Riepilogo delle Automazioni

| Automazione                 | Trigger                            | Azione                           |
| --------------------------- | ---------------------------------- | -------------------------------- |
| **App aperta**              | Synctrain viene aperta o riaperta  | Esegui `Synctrain — File Grandi` |
| **Alimentazione collegata** | iPhone collegato al caricabatterie | Esegui `Synctrain — File Grandi` |

\---

## Consigli per File da 1–2 GB

* **Tieni iPhone collegato alla corrente** per tutta la durata della sincronizzazione: iOS sospende più facilmente i processi in background a batteria scarica
* **Usa il Wi-Fi**, non la rete cellulare, per trasferimenti così grandi
* **Non bloccare lo schermo subito**: lascia qualche secondo affinché Tailscale completi la connessione prima che iOS inizi a limitare l'attività
* In Synctrain, verifica che la cartella abbia **"Watch for changes"** attivo nelle impostazioni avanzate della cartella, così le modifiche vengono rilevate in tempo reale
* Se la sincronizzazione è già completa prima della fine dei 200 cicli, puoi interrompere manualmente il comando senza conseguenze

\---

## Struttura Completa — Schema Finale

```
\[AUTOMAZIONE 1]
Trigger: Synctrain aperta o riaperta
↓
Esegui: Synctrain — File Grandi
    └─ Ripeti 200 volte
           ① Connect to your Tailscale network
           ② Attendi 5 secondi
           ③ Riscansiona cartella
           ④ Sincronizza per un po' — 15 secondi

\[AUTOMAZIONE 2]
Trigger: iPhone collegato all'alimentazione
↓
Esegui: Synctrain — File Grandi
    └─ (stesso flusso sopra)
```
