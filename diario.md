# Diario del progetto emg-hand

## 2026-11-12 (3 h)
Fatto: installati Python, VS Code, Git, Arduino IDE, Onshape. Creato repository, ambiente virtuale, struttura cartelle.
Non ha funzionato: primo tentativo di repository in OneDrive, cartella rimasta vuota. Activate falliva. Perche: terminale aperto sul Desktop invece che nella cartella del progetto.
Numeri: -
Prossimo passo: ...

## 2026-11-20 (3 h)
Fatto:
- Scaricati da ninapro.hevs.ch i primi 10 soggetti del DB2 (Passo 1.1). Ogni archivio si estraeva in due cartelle annidate (DB2_s1\DB2_s1\...): spostati i file S1-S10_E1_A1.mat direttamente in data/raw/ninapro, come si aspettano gli script. Cancellati gli esercizi 2 e 3, che non servono (circa 3 GB liberati).
- Scritto e lanciato python/explore.py (Passo 1.2). Aggiunti i tick da 0 a 17 sull'asse dei movimenti (set_yticks + grid) per leggere i codici nel grafico.
- Letto Atzori et al. 2014 (Scientific Data): il file E1 del DB2 e' l'esercizio B (17 movimenti), emg colonne 1-8 = anello equidistante sotto il gomito, 9 = flessore superficiale delle dita, 10 = estensore delle dita, 11-12 = bicipite e tricipite. 2 kHz, 6 ripetizioni da 5 s con 3 s di riposo.
- Scelti movimenti e canali (Passo 1.3).
  MOVES = [0, 6, 5, 13] (riposo, pugno, abduzione di tutte le dita come "apri", flessione del polso). L'esercizio B non ha un "apri la mano" puro, il 5 e' il piu' vicino (dita estese e aperte).
  CHANNELS_4 = [8, 3, 9, 7]: 8 = flessore delle dita, 9 = estensore delle dita (colonne 9 e 10 del paper). 3 e 7 = elettrodi dell'anello. Il paper non dice come e' orientato l'anello, quindi l'ho ricavato dai dati: confrontando flessione (13) ed estensione (14) del polso sul soggetto 1, gli indici 1-4 sono piu' attivi in flessione (lato flessori) e 5, 6, 7, 0 in estensione (lato estensori). Presi 3 e 7, interni ai due archi e opposti sull'anello. Limite: guardato un solo soggetto, e a occhio.

Non ha funzionato:
- Il progetto era finito di nuovo in OneDrive: avevo spostato emg-hand sul Desktop, che su questo PC e' dentro OneDrive. Perche: non sapevo che il Desktop fosse sincronizzato. Soluzione: rimesso in C:\Users\andrea\progetti\emg-hand.
- Dopo lo spostamento pip non funzionava piu'. Perche: l'ambiente .venv contiene il percorso in cui e' stato creato, quindi non si puo' spostare. Si e' sistemato rimettendo la cartella al suo posto. Lezione: non spostare mai la cartella del progetto, al massimo creare un collegamento.
- Non sapevo quale interprete scegliere in VS Code. Soluzione: sempre .venv (Workspace), mai quello Global.
- h5py non si installa. Perche: ho Python 3.15 e h5py non ha ancora una versione pronta per il 3.15 (il piano chiede 3.11 o 3.12). Per ora non blocca, serve solo nella fase 2 (Passo 2.23). Da fare prima della fase 2: installare Python 3.12 e ricreare .venv.
- python explore.py non faceva niente e tornava subito al prompt. Perche: il codice era nell'editor ma non salvato, il file su disco era vuoto (0 byte). Soluzione: Ctrl+S, e controllare sempre che sparisca il pallino bianco sulla linguetta.
- Il prompt PS non ricompariva dopo aver lanciato lo script. Perche: plt.show() aspetta che si chiuda la finestra del grafico. Soluzione: chiudere la finestra (o Ctrl+C nel terminale).
- Nel grafico era difficile distinguere il movimento 13 dal 14, perche' l'asse aveva tick ogni 5. Soluzione: ax[1].set_yticks(range(18)) e griglia.

Numeri: S1 = 1.808.331 campioni x 12 canali (circa 15 min a 2 kHz), movimenti 0-17, ripetizioni 0-6.

Prossimo passo: leggere i Passi 1.4-1.8 del piano (filtri, finestre, feature, LDA, validazione, accumulo), poi scrivere python/emg.py (Passo 1.9).