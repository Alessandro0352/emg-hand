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

## 2026-11-21 (1 h)
Fatto:
- Letti i Passi 1.4-1.8 del piano. Sono solo teoria (filtri, finestre e feature, LDA, validazione, accumulo dell'evidenza): non si scrive codice.
- Passo 1.9: scritto python/emg.py, il modulo comune con filtri, finestre, feature e accumulo. Controllo: `python -c "import emg; print(emg.design_filters().shape)"` stampa (5, 6).
- Passo 1.10: scritto python/ninapro_baseline.py e lanciato su S1-S10. Tabella per soggetto in results/baseline.md, output completo in results/baseline_raw.txt.
- Passo 1.11: aggiunte allo script la stampa della matrice di confusione (4 canali, causale, somma sui 10 soggetti) e l'accuratezza bilanciata. Provata la LDA con priors uguali (output in results/baseline_priors_raw.txt), poi rimessa la versione senza priors come baseline ufficiale. Scritta la nota results/fase1.md.
- Commit e12442e (Passi 1.9-1.10) e 698335a (Passo 1.11). **Fase 1 finita.**

Non ha funzionato:
- `AttributeError: module 'emg' has no attribute 'design_filters'`. Perche': emg.py su disco era vuoto (0 byte), il codice era nell'editor ma non salvato. Soluzione: Ctrl+S. E' la seconda volta (era gia' successo con explore.py): conviene attivare File -> Auto Save.
- `IndentationError: unexpected indent` sulle due righe dell'accuratezza bilanciata. Perche': incollando, VS Code ha aggiunto i suoi spazi a quelli gia' presenti nel testo, e le righe avevano 8 spazi invece di 4. Spostandole tutte a sinistra l'errore spariva, ma le righe uscivano dal blocco `if __name__ == "__main__":`. Soluzione: esattamente 4 spazi. Per controllarlo, cliccare subito prima della prima lettera della riga: nella barra blu in basso deve comparire "Col 5", come per le righe sopra.
- Il comando lungo e' partito due volte, una volta senza Tee-Object. Nessun danno: i numeri sono identici.
- Da sistemare: i .txt salvati con Tee-Object sono in UTF-16, che e' la codifica di default di Windows PowerShell 5.1. Per questo nel commit Git li mostra come "Bin" (file binari) e GitHub non li visualizza come testo. Per convertire quelli che ci sono gia' (dalla cartella python/):
  `(Get-Content ../results/baseline_raw.txt) | Out-File -Encoding utf8 ../results/baseline_raw.txt`
  e lo stesso per baseline_priors_raw.txt. Le parentesi tonde servono a leggere tutto il file prima di riscriverlo. Per i prossimi output, al posto di `| Tee-Object file` usare:
  `python script.py ... | Tee-Object -Variable out; $out | Out-File -Encoding utf8 ../results/file.txt`

Numeri (10 soggetti, 4 canali = [8, 3, 9, 7], media +- dev. std):

| | 12 can. fase zero | 4 can. fase zero | 4 can. causale |
|---|---|---|---|
| finestra | 0,955 +- 0,048 | 0,938 +- 0,062 | 0,937 +- 0,063 |
| comando | | | 0,900 +- 0,037 |
| tempo | | | 0,19 +- 0,07 s |

- Soggetti peggiori: S7 (4 can. causale: finestra 0,781, tempo 0,39 s) e S4 (0,857). Il migliore e' S9 (0,992).
- Il riposo e' circa il 91% delle finestre (S1: 10.237 finestre di riposo, contro 375 di apri, 234 di pugno e 368 di polso).
- Matrice di confusione, 4 canali, causale, somma sui 10 soggetti, in %. Diagonale: riposo 98,9, apri 55,2, pugno 61,3, polso 72,9. **Accuratezza bilanciata 0,721**, contro 0,937 per finestra.
- Con priors uguali: bilanciata 0,749, riposo 97,1, apri 62,4, pugno 66,1, polso 74,2. Pero' il tempo medio sale a 0,26 s (S7: 0,84 s) e S4 e S7 peggiorano. Tenuta la versione senza priors.

Prossimo passo: convertire i due .txt in UTF-8 (vedi sopra) e fare il commit. Poi leggere l'inizio della fase 2 nel piano. Prima del Passo 2.23: installare Python 3.12 e ricreare .venv (h5py).

### Spiegazioni per ripassare (fase 1, Passi 1.4-1.11)

Questa parte spiega da zero tutto quello che abbiamo usato oggi: prima l'idea, poi come diventa codice. Segue l'ordine in cui i dati passano nello script: segnale -> filtri -> 1 kHz -> etichette -> finestre -> feature -> LDA -> validazione -> accumulo -> misure.

#### 1. Il segnale EMG, in parole povere

- Quando un muscolo si contrae, le sue fibre producono piccolissimi segnali elettrici. Un elettrodo sulla pelle raccoglie la somma di tutti questi segnali.
- Il risultato e' un segnale che oscilla velocemente intorno allo zero, a volte positivo e a volte negativo, e sembra rumore. Quando il muscolo e' a riposo le oscillazioni sono piccolissime. Piu' il muscolo lavora, piu' diventano grandi.
- Tutta l'informazione sta in due cose: **quanto sono grandi** le oscillazioni e **quanto sono veloci**. Le quattro feature (punto 6) misurano proprio questo.

**Campionamento.** Il computer non vede un segnale continuo: misura la tensione tante volte al secondo, e ogni misura e' un **campione**. NinaPro misura 2000 volte al secondo (2 kHz), il tuo hardware 1000 volte (1 kHz). Quindi 1 secondo a 1 kHz sono 1000 numeri per ogni canale.

**Come sono messi i dati.** Una matrice (una tabella): ogni riga e' un istante di tempo, ogni colonna e' un canale. Il file S1 ha 1.808.331 righe e 12 colonne. Per questo nel codice c'e' sempre `axis=0`: vuol dire "lavora lungo il tempo (le righe), separatamente per ogni canale (colonna)". Il risultato e' un numero per canale.

**Frequenza.** Ogni segnale si puo' pensare come una somma di oscillazioni, alcune lente e alcune veloci. La frequenza dice quante oscillazioni complete ci sono in un secondo e si misura in Hz: 50 Hz = 50 oscillazioni al secondo. Il "contenuto in frequenza" dice quanta parte del segnale e' fatta di oscillazioni lente e quanta di oscillazioni veloci. L'EMG utile sta piu' o meno tra 20 e 450 Hz.

**Regola di Nyquist (semplice).** Con N campioni al secondo si possono rappresentare oscillazioni solo fino a N/2. A 1 kHz il massimo e' 500 Hz. Le oscillazioni piu' veloci non spariscono: si "travestono" da oscillazioni piu' lente, e questo si chiama **aliasing**. E' lo stesso effetto delle ruote delle auto nei film, che sembrano girare all'indietro perche' la cinepresa fa troppo poche foto al secondo.

#### 2. I filtri (Passo 1.4)

Un filtro e' come un setaccio per le frequenze: alcune le fa passare, altre le blocca.

**Passa-banda 20-450 Hz.** Fa passare solo le frequenze tra 20 e 450 Hz.
- Sotto i 20 Hz ci sono soprattutto disturbi lenti: il cavo che si muove, la pelle che si sposta sotto l'elettrodo. Non sono attivita' muscolare.
- Sopra i 450 Hz l'EMG non ha quasi piu' niente di utile, resta solo rumore. In piu', a 1 kHz sopra i 500 Hz non si puo' andare comunque (Nyquist).

**Butterworth del 4 ordine.**
- "Butterworth" e' un tipo di filtro con la banda passante piatta: le frequenze che lascia passare non vengono ne' amplificate ne' attenuate. Quindi il segnale utile resta com'e'.
- L'"ordine" dice quanto e' ripido il passaggio tra "passa" e "bloccato". Un ordine alto taglia piu' netto, ma introduce piu' ritardo e diventa piu' delicato da calcolare. 4 e' il compromesso standard.

**Notch a 50 Hz.** La rete elettrica in Italia oscilla a 50 Hz, e i cavi la captano come un ronzio. Il notch toglie una fettina strettissima intorno ai 50 Hz. `Q=30` dice quanto e' stretta la fettina: circa 50/30, cioe' meno di 2 Hz. Toglie anche un pochino di EMG a 50 Hz, ma il ronzio di solito e' molto piu' forte, quindi conviene.

**SOS (second-order sections).** Il filtro non viene calcolato come un unico filtro grande, ma come una catena di filtrini piccoli messi in fila, le "sezioni del secondo ordine". Il motivo: un unico filtro grande, nei calcoli al computer, accumula errori di arrotondamento e puo' dare risultati sbagliati. Tanti pezzi piccoli invece sono stabili. Ogni sezione e' descritta da 6 numeri.

**Fase zero o causale: la differenza piu' importante.**
- Il **filtro causale** e' come una persona che riassume quello che dici mentre ti ascolta: puo' usare solo le parole gia' dette, quindi resta sempre un po' indietro. Questo e' il **ritardo**. E' l'unico filtro possibile in tempo reale, perche' il futuro non lo hai ancora.
- Il **filtro a fase zero** (`filtfilt`) e' come una persona che legge tutto il testo prima di riassumerlo. Filtra il segnale in avanti e poi all'indietro, e il ritardo della prima passata viene annullato da quello, opposto, della seconda. Risultato: zero ritardo, pero' ha bisogno dei campioni "futuri", quindi funziona solo offline, su una registrazione gia' finita.
- Perche' li proviamo tutti e due: il classificatore deve vedere, in uso, lo stesso tipo di segnale su cui ha imparato. Se lo addestri con il fase zero e poi lo usi con il causale, vede segnali leggermente diversi. Oggi abbiamo misurato la differenza: 0,938 contro 0,937, praticamente niente. Buona notizia: il causale non ti costa nulla.

**Il codice (emg.py).**
- `design_filters()`:
  - `signal.butter(4, band, btype="bandpass", fs=fs, output="sos")` progetta il passa-banda. Un passa-banda ha due "bordi" (20 e 450 Hz), quindi un ordine 4 diventa in tutto 8, cioe' 4 sezioni.
  - `signal.iirnotch(50, Q=30, fs=fs)` progetta il notch, e `tf2sos` lo trasforma nello stesso formato a sezioni: 1 sezione.
  - `np.vstack([...])` mette le sezioni una sotto l'altra: 4 + 1 = 5 righe da 6 numeri. Per questo il controllo stampava **(5, 6)**.
- `filter_offline(x, sos)` usa `sosfiltfilt`, cioe' il filtro a fase zero.
- `filter_causal(x, sos)` usa `sosfilt`, cioe' il filtro causale. La riga con `zi` serve a evitare un difetto all'inizio:
  - Un filtro causale ha una "memoria" dei campioni passati (lo **stato**). All'inizio la memoria e' vuota, come se prima il segnale fosse sempre stato 0.
  - Se il primo campione vale, per esempio, 50, il filtro vede un salto da 0 a 50 e produce una grossa oscillazione finta all'inizio (il **transitorio**).
  - `zi = sosfilt_zi(sos) * x[0]` fa partire il filtro come se il segnale fosse sempre stato uguale al primo campione: niente salto, niente transitorio.
  - I vari `[:, :, None]` e `[None, None, :]` servono solo a far combaciare le dimensioni: uno stato per ogni sezione e per ogni canale.
- `class OnlineFilter` serve per il tempo reale (fasi successive):
  - Dal tuo hardware i dati arriveranno a pezzi (blocchi), per esempio 50 campioni alla volta. Se filtrassi ogni blocco da zero, ogni blocco avrebbe il suo transitorio all'inizio.
  - La classe si ricorda lo stato del filtro (`self.zi`) tra un blocco e l'altro, cosi' il filtro riprende esattamente da dove era rimasto.
  - `__init__` viene eseguito una volta sola, quando crei il filtro: `f = OnlineFilter(sos)`.
  - `__call__` viene eseguito ogni volta che usi l'oggetto come una funzione: `y = f(blocco)`.
  - Il risultato e' identico a filtrare tutta la registrazione in una volta con `filter_causal`.

#### 3. Da 2 kHz a 1 kHz (`decimate`, in ninapro_baseline.py)

- **Perche':** in emg.py una finestra e' di 200 campioni e il passo di 50. Questo vuol dire 200 ms e 50 ms solo se i campioni sono 1000 al secondo. Portando NinaPro a 1 kHz, tutto funziona con gli stessi numeri del tuo hardware.
- **Perche' non basta prendere un campione si' e uno no:** i dati a 2 kHz contengono anche oscillazioni tra 500 e 1000 Hz, che a 1 kHz si travestirebbero da frequenze piu' basse (aliasing, punto 1). `decimate` prima applica un filtro che toglie tutto quello che sta sopra circa 500 Hz, e poi tiene un campione ogni due. `zero_phase=True` lo fa a fase zero: siamo offline, quindi il ritardo lo possiamo evitare.
- `lab[::2]` e `rep[::2]`: per le etichette basta tenere un valore ogni due. `[::2]` vuol dire "dall'inizio alla fine, a passi di 2". Le etichette non si filtrano: sono numeri interi (0, 5, 6, 13), non un segnale.

#### 4. Etichette e ripetizioni (`load_subject`)

- `restimulus`: per ogni campione dice quale movimento sta facendo il soggetto (0 = riposo). Il "re" sta per *relabeled*: NinaPro ha corretto le etichette dopo la registrazione, perche' seguissero il movimento vero e non l'istruzione sullo schermo (quella e' `stimulus`). Usare `stimulus` e' uno degli errori tipici citati nel piano.
- `rerepetition`: dice a quale ripetizione (da 1 a 6) appartiene ogni campione. Il riposo ha 0, cioe' "nessuna ripetizione".
- Il ciclo `for` con `last`:
  - `last` si ricorda l'ultimo numero di ripetizione visto.
  - Quando incontra un campione di riposo (`lab[i] == 0`, con ripetizione 0), gli assegna `last`.
  - Cosi' il riposo che segue la ripetizione 3 di un movimento diventa "ripetizione 3".
  - Serve per la validazione (punto 8): ogni finestra deve appartenere a una ripetizione per poter finire nel training o nel test.
- `keep = np.isin(lab, MOVES)` da' True per i campioni il cui movimento e' uno dei tuoi 4, False per gli altri.
- `lab = np.where(keep, lab, -1)`: dove `keep` e' True lascia l'etichetta com'e', altrimenti mette -1. **-1 vuol dire "ignora"**: sono i 14 movimenti che non usi.

#### 5. Le finestre (Passo 1.5, `make_windows`)

- Il classificatore non guarda un campione alla volta. Un singolo numero non dice niente, perche' l'EMG oscilla sempre intorno allo zero. Guarda invece pezzi di segnale da **200 ms** (le **finestre**).
- Ogni **50 ms** parte una finestra nuova, quindi due finestre vicine si sovrappongono per 150 ms. Il risultato sono 20 decisioni al secondo.
- E' un compromesso: finestre piu' lunghe danno numeri piu' stabili, ma la mano risponde piu' tardi.
- `for end in range(win, x.shape[0] + 1, step)`: `end` vale 200, 250, 300, ..., quindi le finestre sono i campioni 0-199, 50-249, 100-299, e cosi' via.
- Si tengono solo le finestre **"pure"**: stessa etichetta dall'inizio alla fine, stessa ripetizione, ed etichetta diversa da -1. Una finestra a cavallo tra riposo e pugno viene scartata, perche' non sapremmo quale etichetta darle.
- La funzione restituisce quattro cose:
  - `X`: la tabella delle feature, una riga per finestra e 16 colonne;
  - `y`: l'etichetta di ogni finestra;
  - `r`: la ripetizione di ogni finestra;
  - `idx`: l'indice dell'ultimo campione della finestra, cioe' l'istante in cui la decisione sarebbe presa. Serve per ricostruire l'ordine nel tempo (punto 9).
- Nel soggetto 1 (4 canali, causale) le finestre sono 10.237 di riposo, 375 di apri, 234 di pugno e 368 di polso.

#### 6. Le feature (Passo 1.5, `td_features`)

Una finestra a 4 canali e' fatta di 200 x 4 = 800 numeri: troppi, e troppo "grezzi". Allora ogni canale si riassume in 4 numeri, e in tutto restano 4 x 4 = **16 feature**.

Esempio con una mini-finestra di 5 campioni: `[2, -1, 3, -2, 1]`.

- **MAV** (valore medio assoluto): si tolgono i segni e si fa la media. (2 + 1 + 3 + 2 + 1) / 5 = **1,8**. Dice quanto e' attivo il muscolo.
- **WL** (lunghezza d'onda): si sommano i salti tra un campione e il successivo, senza segno. I salti sono -3, +4, -5, +3, quindi 3 + 4 + 5 + 3 = **15**. E' la lunghezza della linea se stendessi il disegno dell'onda. Cresce sia se le oscillazioni sono grandi sia se sono veloci.
- **ZC** (passaggi per lo zero): quante volte il segnale cambia segno. 2 -> -1 si', -1 -> 3 si', 3 -> -2 si', -2 -> 1 si': **4**. E' una stima grossolana della frequenza: piu' il segnale e' veloce, piu' passa per lo zero.
- **SSC** (cambi di pendenza): quanti picchi e valli ci sono. -1 e' una valle, 3 e' un picco, -2 e' una valle: **3**. Anche questa e' legata alla frequenza.

**La soglia.** A riposo il segnale e' un rumorino intorno allo zero, che passa per lo zero di continuo. Senza soglia, ZC e SSC conterebbero il rumore. Per questo un passaggio conta solo se il salto e' abbastanza grande:
- la soglia e' `thr = 2 x deviazione standard del segnale a riposo`;
- la deviazione standard e' "quanto oscilla di solito" il segnale, quindi qui misura quanto e' grande il rumore a riposo;
- la soglia e' calcolata canale per canale, perche' ogni elettrodo ha il suo livello di rumore;
- `rest_threshold(xf[lab == 0])` la calcola prendendo solo i campioni di riposo.

**Il codice, riga per riga.**
- `d = np.diff(win, axis=0)`: i salti tra un campione e il successivo.
- `mav = np.mean(np.abs(win), axis=0)`: media dei valori senza segno.
- `wl = np.sum(np.abs(d), axis=0)`: somma dei salti senza segno.
- `zc`:
  - `win[:-1] * win[1:] < 0` moltiplica ogni campione per il successivo. Se hanno segno opposto il prodotto e' negativo, quindi c'e' stato un passaggio per lo zero.
  - `& (np.abs(d) >= thr)` aggiunge "e il salto e' abbastanza grande".
  - `np.sum` conta quanti True ci sono.
- `ssc`: `(x[i] - x[i-1]) * (x[i] - x[i+1])` e' positivo quando `x[i]` e' piu' alto di tutti e due i vicini (un picco) o piu' basso di tutti e due (una valle). `>= thr ** 2` chiede che lo sia abbastanza. La soglia e' al quadrato perche' si moltiplicano due differenze.
- `np.concatenate([mav, wl, zc, ssc])` mette in fila i 16 numeri: prima i 4 MAV, poi i 4 WL, i 4 ZC e i 4 SSC.

#### 7. Standardizzazione e LDA (Passo 1.6)

**Standardizzazione (`StandardScaler`).**
- Le feature hanno scale molto diverse: un MAV puo' valere 0,00001 (sono volt), uno ZC 30.
- Lo scaler prende ogni colonna, toglie la media e divide per la deviazione standard. Dopo, ogni feature sta intorno a 0 con una grandezza tipica di 1.
- Media e deviazione standard le impara **solo dal training**.
- Per la LDA non cambia le decisioni, ma evita problemi numerici e rende confrontabili i pesi.

**LDA, l'idea.**
- Ogni finestra e' un punto in uno spazio a 16 dimensioni. Per immaginarlo bastano 2 feature: un foglio, con il MAV del flessore sull'asse orizzontale e il MAV dell'estensore su quello verticale.
- Le finestre della stessa classe formano una **nuvola** di punti:
  - pugno: dove il flessore e' alto;
  - apri: dove l'estensore e' alto;
  - riposo: vicino all'origine, perche' tutto e' basso.
- **Addestramento** (`fit`): la LDA calcola il centro di ogni nuvola e quanto le nuvole sono "sparpagliate". Assume che abbiano tutte la stessa forma. Poi traccia delle **linee dritte** che le separano (in 16 dimensioni sono piani, ma l'idea e' la stessa).
- **Uso**: per una finestra nuova guarda da che parte delle linee cade e la assegna a quella classe.

**Probabilita'.**
- La LDA non dice solo "pugno": dice anche quanto e' sicura, con una probabilita' per classe. Per esempio [0,05; 0,10; 0,80; 0,05].
- E' quello che restituisce `predict_proba`, ed e' il `p(t)` che usa l'accumulo (punto 9).

**Perche' la LDA:** si addestra in un istante, le bastano pochi dati, e per usarla servono poche moltiplicazioni, quindi gira anche su un microcontrollore (fase 7).

**Il codice.**
- `make_pipeline(StandardScaler(), LinearDiscriminantAnalysis())` mette in fila scaler e LDA. `fit` li addestra tutti e due, `predict_proba` li applica tutti e due.
- `clf.classes_` e' l'ordine delle colonne di P, in ordine crescente: [0, 5, 6, 13].
- `P.argmax(1)` dice, per ogni finestra, la colonna con la probabilita' piu' alta.
- `clf.classes_[P.argmax(1)]` trasforma quella colonna nell'etichetta: colonna 2 -> movimento 6.

#### 8. Validazione (Passo 1.7)

- **Scopo:** misurare quanto funziona il classificatore su dati che **non ha mai visto**. Quindi si addestra su una parte dei dati (training) e si misura sul resto (test).
- **La trappola:** due finestre consecutive hanno in comune 150 ms su 200, sono quasi gemelle. Se mescoli le finestre a caso, ogni finestra di test ha la sua gemella nel training. E' come un esame con domande che hai gia' visto: il voto esce gonfiato.
- **La soluzione: leave-one-repetition-out.** Si fanno 6 giri:
  - addestri sulle ripetizioni 1-5 e testi sulla 6;
  - poi addestri su 1-4 e 6, e testi sulla 5;
  - e cosi' via, finche' ogni ripetizione e' stata il test una volta;
  - alla fine si fa la media dei 6 risultati.
- Le gemelle stanno sempre nella stessa ripetizione, quindi non finiscono mai una nel training e una nel test.
- **Il codice:**
  - `for test_rep in np.unique(r[r > 0])` gira su 1, 2, ..., 6.
  - `tr, te = r != test_rep, r == test_rep` sono due **maschere**, liste di True e False.
  - `X[tr]` prende solo le righe dove la maschera e' True, cioe' le finestre di training.
  - Il riposo prima del primo movimento ha ripetizione 0: non e' mai nel test e sta sempre nel training. Va bene cosi'.

#### 9. Accumulo dell'evidenza (Passo 1.8)

- **Il problema:** se la mano si muovesse a ogni finestra, una sola finestra sbagliata (un disturbo) la farebbe muovere a caso. Meglio aspettare di essere abbastanza sicuri.
- **L'idea:** ogni classe ha una "barra di evidenza" D. All'inizio tutte valgono 0,25, cioe' 1/4: non sappiamo niente. A ogni finestra nuova:

  `D = 0,7 x D + 0,3 x p`

  Si tiene il 70% di quello che si pensava prima e si aggiunge il 30% di quello che dice la finestra nuova. E' una media che dimentica il passato poco alla volta.
- **Decisione:** quando una barra arriva a **0,7** (la soglia), si decide quella classe.

**Esempio con i numeri.** Supponiamo che la LDA dia sempre probabilita' 1 alla classe giusta:
- finestra 1: 0,7 x 0,25 + 0,3 x 1 = 0,175 + 0,3 = **0,475**
- finestra 2: 0,7 x 0,475 + 0,3 = 0,3325 + 0,3 = **0,633**
- finestra 3: 0,7 x 0,633 + 0,3 = 0,443 + 0,3 = **0,743**, che supera 0,7: si decide.

3 finestre x 50 ms = **150 ms**. E' il tempo minimo possibile, e infatti la media misurata e' 0,19 s. Se a meta' arriva una finestra sbagliata, la barra giusta scende un po', ma non crolla: e' questo che rende la decisione robusta.

**Cosa fa alpha (0,3).**
- Alpha grande: ci si fida molto della finestra nuova, quindi la decisione e' veloce ma "nervosa".
- Alpha piccolo: ci si fida del passato, quindi la decisione e' calma ma lenta.
- Nel BCI si usava alpha = 0,05, e servirebbero 18 finestre, cioe' 0,9 s: troppo per una mano, che deve rispondere in circa 100-125 ms. Per questo qui si usa 0,3. Stesso metodo, parametri diversi, perche' l'applicazione ha vincoli diversi.

**Il codice (`trial_metrics`).**
- Una **prova** (trial) e' una sequenza di finestre consecutive con la stessa etichetta e senza buchi nel tempo. Un buco c'e' quando `idx` salta di piu' di 50, cioe' quando delle finestre sono state scartate.
- `bounds` trova i punti dove cambia l'etichetta o c'e' un buco, e `np.split` taglia li'.
- Per ogni prova:
  - la barra riparte da 0,25 per tutte le classi;
  - si scorrono le finestre e si accumula;
  - appena il massimo supera 0,7 si decide, e il tempo e' (numero di finestre) x 0,05 s;
  - se la soglia non viene mai raggiunta, alla fine della prova si decide comunque la classe con la barra piu' alta (**decisione forzata**).
- Alla fine la funzione restituisce la frazione di prove decise giuste e il tempo medio.

#### 10. Le tre misure che stampa lo script

- **finestra**: la frazione di finestre in cui la classe con la probabilita' piu' alta e' quella giusta. Non c'e' accumulo, ogni finestra conta da sola.
- **comando**: la frazione di prove in cui l'accumulo prende la decisione giusta.
- **tempo**: il tempo medio, in secondi, per arrivare alla decisione.

**Perche' "comando" e' piu' bassa di "finestra".** L'accumulo decide nei primi 150-200 ms di ogni prova, cioe' proprio nella fase di transizione, quando il muscolo ha appena cominciato o appena smesso di contrarsi. Li' le finestre sono le piu' ambigue. L'accuratezza per finestra invece fa la media su tutta la prova, compresa la lunga parte centrale, stabile e facile.

**Attenzione: anche "comando" pesa soprattutto il riposo.** Controllato su S1: in ogni ripetizione di test ci sono **20 prove**, 17 di riposo (una dopo ciascuno dei 17 movimenti dell'esercizio, anche quelli che non usi) e solo 3 di movimento. Quindi anche lo 0,900 dice soprattutto quanto bene si riconosce il riposo.

#### 11. La matrice di confusione (Passo 1.11)

- E' una tabella:
  - le righe sono il movimento **vero**, le colonne quello che ha detto il classificatore;
  - in percentuale, ogni riga somma a 100;
  - la **diagonale** (riposo->riposo, apri->apri, ...) sono le risposte giuste, il resto della riga dice con cosa e' stato scambiato.
- Esempio, la riga "apri": 37,4 riposo, 55,2 apri, 4,8 pugno, 2,6 polso. Vuol dire che le finestre di "apri" sono state riconosciute giuste il 55% delle volte, e scambiate per riposo il 37% delle volte.
- **Il codice:**
  - `confusion_matrix(vero, previsto, labels=classes)` conta i casi.
  - `sum(cms)` somma le 6 ripetizioni, e `cm_total = cm_total + cm` somma i 10 soggetti (solo il caso 4 canali, causale).
  - `cm_total.sum(axis=1, keepdims=True)` calcola il totale di ogni riga. `keepdims=True` lo tiene "in colonna", cosi' la divisione avviene riga per riga.
  - `100 * ... / ...` trasforma in percentuali, e `np.round(..., 1)` arrotonda a un decimale.
- **L'ordine delle classi e' 0, 5, 6, 13** (crescente): riposo, apri, pugno, polso. Non e' l'ordine di MOVES.

#### 12. Il risultato piu' importante di oggi: l'accuratezza gonfiata dal riposo

- In S1 il riposo e' il **91%** delle finestre. Il motivo: il file contiene il riposo dopo ognuno dei 17 movimenti x 6 ripetizioni, ma dei movimenti ne tieni solo 3. Il riposo invece lo tieni tutto.
- Quindi un classificatore "pigro", che rispondesse sempre "riposo", prenderebbe gia' il 91% per finestra. Il nostro 93,7% e' appena sopra.
- Il numero onesto e' l'**accuratezza bilanciata**: la media della diagonale, in cui ogni classe pesa uguale, indipendentemente da quante finestre ha. (98,9 + 55,2 + 61,3 + 72,9) / 4 = **72,1%**. Le due righe in fondo allo script la calcolano: `np.diag` prende la diagonale e `np.mean` fa la media.
- **Cosa dice la matrice:**
  - i 3 movimenti si confondono poco tra loro (sempre sotto il 10%);
  - l'errore principale e' un altro: il classificatore **non si accorge che c'e' un movimento** e dice "riposo";
  - la causa sono le finestre a inizio e fine movimento, e le contrazioni deboli, che somigliano al riposo.
- **Lettura anatomica (da approfondire nella nota):**
  - il polso e' il movimento riconosciuto meglio: i flessori del polso sono muscoli grandi, proprio sotto gli elettrodi dell'avambraccio;
  - "apri" e' il peggiore: l'abduzione delle dita la fanno soprattutto gli interossei dorsali, che stanno nella mano e non nell'avambraccio, quindi gli elettrodi vedono solo la parte fatta dall'estensore delle dita.

#### 13. I priors della LDA (la prova di oggi)

- La LDA, per decidere, mette insieme due cose:
  1. quanto la finestra somiglia a ogni nuvola;
  2. quanto e' frequente ogni classe nel training, cioe' il **prior**.
- E' come un medico davanti a sintomi che potrebbero essere un raffreddore o una malattia rarissima: nel dubbio dice raffreddore, perche' e' molto piu' comune.
- Di default i priors sono le frequenze del training: il riposo pesa il 91%, quindi nei casi dubbi la LDA dice "riposo".
- `LinearDiscriminantAnalysis(priors=np.ones(4) / 4)` mette i priors a [0,25; 0,25; 0,25; 0,25], cioe' tutte le classi ugualmente probabili.
- **Risultato:**
  - la bilanciata sale solo da 0,721 a 0,749 (+3 punti);
  - il riposo scende da 98,9 a 97,1;
  - il tempo medio sale da 0,19 a 0,26 s, e S7 arriva a 0,84 s;
  - S4 e S7 peggiorano.
- **Conclusione:** la confusione movimento -> riposo viene soprattutto dal segnale, non dallo sbilanciamento. In piu', i priors uguali fanno "vedere" movimenti anche durante il riposo, e in una protesi questo e' l'errore peggiore: la mano che si muove da sola. Per questo la baseline ufficiale resta **senza priors**, e i priors uguali sono un'analisi in piu' riportata nella nota.

#### 14. Le cose di Python incontrate oggi

- **`import emg`**: Python cerca un file `emg.py` nella cartella da cui lanci il comando. Per questo si lavora da `python/`. Se il file e' vuoto (non salvato), il modulo e' vuoto e compare `AttributeError: module 'emg' has no attribute ...`.
- **`python -c "..."`**: esegue un pezzetto di codice al volo, senza creare un file. Utile per i controlli rapidi.
- **Indentazione.** In Python gli spazi a inizio riga non sono estetica: decidono a quale blocco appartiene una riga.
  - Tutto quello che sta sotto `if ...:` o `for ...:` con 4 spazi in piu' fa parte di quel blocco.
  - Troppi spazi danno `unexpected indent`.
  - Troppo pochi fanno uscire la riga dal blocco, senza errore ma con un comportamento diverso.
  - Trucco: la colonna ("Col") nella barra in basso di VS Code.
- **`if __name__ == "__main__":`**: il blocco sotto parte solo quando lanci il file direttamente (`python ninapro_baseline.py ...`), non quando un altro script fa `import ninapro_baseline`. Nella fase 2 riuserai `load_subject` importandolo da qui, ed e' per questo che le righe finali devono stare dentro il blocco.
- **`sys.argv`**: la lista delle parole scritte dopo `python` nel comando. `sys.argv[0]` e' il nome dello script, `sys.argv[1:]` sono i file. Per questo puoi passare 1 file o 10.
- **Fette (slicing):**
  - `x[:, cols]`: tutte le righe, solo le colonne scelte. `slice(None)` equivale a `:`, cioe' tutte e 12.
  - `[::2]`: un elemento ogni due.
  - `win[:-1]` e `win[1:]`: tutti tranne l'ultimo, e tutti tranne il primo. Messi uno accanto all'altro confrontano ogni campione con il successivo.
- **Maschere:** `lab == 0` da' una lista di True e False. `xf[lab == 0]` prende solo le righe dove c'e' True, cioe' i campioni di riposo.
- **`axis=0` e `axis=1`:** `axis=0` lavora lungo le righe (il tempo) e da' un numero per colonna (canale). `axis=1` lavora lungo le colonne e da' un numero per riga, come i totali di riga della matrice di confusione.
- **f-string:** in `f"finestra {wa:.3f}"` il valore di `wa` viene inserito nel testo con 3 decimali.
- **`| Tee-Object file`** (PowerShell): mostra l'output a schermo e intanto lo salva nel file. Attenzione alla codifica UTF-16, vedi "Non ha funzionato".

#### 15. Git

- `git add file...` sceglie quali file mettere nella prossima "fotografia" del progetto.
- `git commit -m "messaggio"` scatta la fotografia, con un messaggio che dice cosa e' cambiato.
- Si puo' sempre tornare a una fotografia precedente: per questo conviene fare un commit a ogni passo finito. Oggi: e12442e (Passi 1.9-1.10) e 698335a (Passo 1.11).
