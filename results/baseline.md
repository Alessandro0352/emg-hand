# Baseline NinaPro DB2 (fase 1)

Esercizio B (E1), soggetti 1-10. MOVES = [0, 6, 5, 13], CHANNELS_4 = [8, 3, 9, 7].
LDA, validazione leave-one-repetition-out, finestre 200 ms / passo 50 ms, accumulo alpha = 0,3, soglia 0,7.
Colonne "12 can." e "4 can. finestra": filtro a fase zero. Tempo: 4 canali, causale.

| Soggetto | 12 can. finestra | 4 can. finestra | 4 can. causale finestra | 4 can. causale comando | tempo [s] |
|----------|------------------|-----------------|-------------------------|------------------------|-----------|
| S1       | 0.985 | 0.971 | 0.970 | 0.885 | 0.16 |
| S2       | 0.944 | 0.932 | 0.932 | 0.909 | 0.18 |
| S3       | 0.970 | 0.964 | 0.963 | 0.884 | 0.17 |
| S4       | 0.880 | 0.857 | 0.857 | 0.876 | 0.20 |
| S5       | 0.989 | 0.975 | 0.972 | 0.892 | 0.16 |
| S6       | 0.965 | 0.952 | 0.952 | 0.893 | 0.16 |
| S7       | 0.847 | 0.786 | 0.781 | 0.825 | 0.39 |
| S8       | 0.982 | 0.968 | 0.966 | 0.942 | 0.16 |
| S9       | 0.994 | 0.991 | 0.992 | 0.967 | 0.15 |
| S10      | 0.990 | 0.985 | 0.986 | 0.925 | 0.16 |
| **Media ± dev. std** | **0.955 ± 0.048** | **0.938 ± 0.062** | **0.937 ± 0.063** | **0.900 ± 0.037** | **0.19 ± 0.07** |