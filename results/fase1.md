# Fase 1: baseline su NinaPro DB2

Dati: DB2, esercizio B, soggetti 1-10. Classi: riposo (0), apri (5), pugno (6), flessione del polso (13).
Canali: 12, oppure 4 = [8, 3, 9, 7]. LDA, leave-one-repetition-out, finestre 200 ms / passo 50 ms,
accumulo alpha = 0,3, soglia 0,7. Tabella per soggetto in baseline.md, output completi in baseline_raw.txt
(senza priors) e baseline_priors_raw.txt (priors uguali).

## 12 contro 4 canali
Per finestra: 0,955 ± 0,048 con 12 canali, 0,938 ± 0,062 con 4 (fase zero).
[cosa ne pensi: quanto perdi, e cosa vuol dire per un sistema economico]

## Costo del filtro causale
4 canali: 0,938 a fase zero, 0,937 causale.
[conclusione per il tempo reale]

## Accumulo dell'evidenza
4 canali causale: per comando 0,900 ± 0,037, tempo medio 0,19 ± 0,07 s (S7: 0,39 s).
L'accuratezza per comando e' piu' bassa di quella per finestra perche' [la tua spiegazione: quando decide l'accumulo?]

## Attenzione: l'accuratezza per finestra e' gonfiata dal riposo
Il riposo e' circa il 91% delle finestre (S1: 532.300 campioni di riposo contro 52.497 dei tre movimenti).
Un classificatore che dice sempre "riposo" farebbe il 91%. Accuratezza bilanciata (media della diagonale): 0,721.

Matrice di confusione, 4 canali, causale, somma sui 10 soggetti [%] (righe = vero, colonne = previsto):

|        | riposo | apri | pugno | polso |
|--------|--------|------|-------|-------|
| riposo | 98,9 | 0,4 | 0,5 | 0,1 |
| apri   | 37,4 | 55,2 | 4,8 | 2,6 |
| pugno  | 30,5 | 6,3 | 61,3 | 2,0 |
| polso  | 14,7 | 9,3 | 3,2 | 72,9 |

Con priors uguali nella LDA: bilanciata 0,749, ma il tempo medio sale a 0,26 s (S7: 0,84 s) e
calano i soggetti difficili. L'errore principale resta movimento scambiato per riposo.

## Perche' queste confusioni (anatomia)
[polso il migliore: perche'? apri il peggiore: chi fa l'abduzione delle dita, e dove sta?
perche' i movimenti finiscono nel riposo e non si confondono tra loro?]

## Cosa mi aspetto sul mio hardware
[4 canali come qui, ma: tuoi elettrodi, un solo soggetto (tu), meno ripetizioni, rumore...
quale numero ti aspetti, e quale soggetto di NinaPro potresti somigliare?]