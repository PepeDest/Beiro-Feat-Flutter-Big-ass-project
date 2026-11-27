# Calcoli lunghi delle nicchie D, F e G: cosa fare sulle macchine Xeon

Lo zip contiene tutto il codice. Il programma usa tutti i core della macchina. Ogni compito finito viene salvato
subito. Se la macchina si spegne, fai ripartire lo stesso comando: il programma salta i compiti già fatti.

## Cosa serve
- Python 3.11 o più recente (su Linux di solito c'è già, su Windows lo installi da python.org).
- La connessione a internet solo all'inizio, per scaricare numpy, scipy e numba.
- Circa 1 GB di spazio libero.

## Con una sola macchina

### Linux
1. Copia lo zip sulla macchina ed estrailo in una cartella nuova.
2. Apri un terminale in quella cartella.
3. Scrivi questo comando e premi Invio:
   ```
   nohup bash cluster/run_linux.sh > run.log 2>&1 &
   ```
4. Puoi chiudere il terminale. Il calcolo continua da solo.
5. Per vedere a che punto è, scrivi: `tail cluster_out/progress.log`

### Windows
1. Estrai lo zip in una cartella nuova.
2. Nelle impostazioni di risparmio energia, metti "Sospensione: mai".
3. Apri la cartella `cluster` e fai doppio clic su `run_windows.bat`.
4. Lascia aperta la finestra nera. Alla fine scrive "FINISHED".

## Con due o più macchine
Su ogni macchina estrai lo stesso zip. Poi aggiungi `--part N/M` al comando, dove M è il numero di macchine e N il
numero della macchina:
- Linux, macchina 1 di 2: `nohup bash cluster/run_linux.sh --part 1/2 > run.log 2>&1 &`
- Linux, macchina 2 di 2: `nohup bash cluster/run_linux.sh --part 2/2 > run.log 2>&1 &`
- Windows: apri un terminale nella cartella e scrivi `cluster\run_windows.bat --part 1/2` (oppure `2/2`).

Le macchine si dividono i compiti senza parlarsi. Non serve una rete tra loro.

## Cosa succede, in ordine
1. Installa le librerie (pochi minuti).
2. Fa un test breve (circa 1 minuto). Se il test dà un errore, si ferma.
3. Fa il calcolo vero. All'inizio scrive una stima delle ore. La stima è fatta sul PC di casa, che ha 4 core.
4. Alla fine crea il file `results_cluster_out_NOMEMACCHINA.zip` nella cartella principale.

## Quanto dura
Il lavoro totale è circa 370 ore di un core del PC di casa:

| Lavoro | Compiti | Ore di un core |
|---|---|---|
| d1: l'agente che raccoglie cibo | 1606 | 42 |
| d2: l'agente nella rete di oscillatori | 6528 | 44 |
| f: le scelte di CLD | 840 | 57 |
| g3: S_TE e D_T* a tempi lunghi | 1200 | 228 |

Con 40 core sono circa 9-10 ore. Con 2 macchine da 40 core sono circa 5 ore. Un core Xeon di qualche anno fa può
essere più lento o più veloce di un core del PC di casa: la stima nel file `progress.log` si aggiorna durante il calcolo.

## Cosa mi devi rimandare
Solo il file `results_cluster_out_NOMEMACCHINA.zip` di ogni macchina. Lo metti nella cartella
`Desktop\frazbaro\variational_life` del PC di casa e mi dici "fatto".

Come deve essere il risultato:
- Dentro lo zip c'è la cartella `cluster_out` con le sottocartelle `d1`, `d2`, `f`, `g3`.
- Con tutte le macchine insieme: 1606 file in `d1`, 6528 in `d2`, 840 in `f`, 1200 in `g3`.
- Ogni file è un piccolo file di testo `.json`. Lo zip pesa circa 50-100 MB.
- Nel file `progress.log` l'ultima riga dice `finished: ... tasks done, 0 errors`.

## Se qualcosa va storto
- **La macchina si spegne o il calcolo si ferma:** fai ripartire lo stesso comando. Riparte da dove era.
- **L'ultima riga di `progress.log` dice "errors" con un numero più grande di 0:** mandami il file
  `cluster_out/progress.log`.
- **Il comando non parte:** mandami una foto della finestra o il file `run.log`.
