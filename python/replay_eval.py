"""Phase 2 (no hardware): runs the online decoder on a recording, feeding it in blocks of
random size as a real serial port would, and measures how it behaves over time.
Usage: python replay_eval.py ../models/sim.joblib ../data/sim/S1_test.npz"""
import sys
import numpy as np
import joblib
from decoder import Decoder
import emg


def run(model, x, block_sizes):
    dec, states, i = Decoder(model), [], 0
    for n in block_sizes:
        if i >= len(x):
            break
        for cls, speed, D in dec.update(x[i:i + n]):
            states.append(cls)
        i += n
    ends = np.arange(len(states)) * emg.STEP + emg.WIN - 1    # last sample of each decision
    return np.array(states), ends


model = joblib.load(sys.argv[1])
d = np.load(sys.argv[2])
x, lab = d["emg"].astype(float), d["label"]

rng = np.random.default_rng(0)
states, ends = run(model, x, rng.integers(1, 40, size=len(x)))   # irregular blocks
states_big, _ = run(model, x, [len(x)])                          # everything at once
print(f"Decisioni identiche con blocchi irregolari e con un blocco unico: "
      f"{np.mean(states == states_big[:len(states)]) * 100:.1f}%")

truth = lab[ends]
valid = truth >= 0
print(f"Decisioni valutate: {valid.sum()} | stato del decoder corretto: "
      f"{np.mean(states[valid] == truth[valid]) * 100:.1f}%")

per_class = [np.mean(states[valid & (truth == c)] == c) * 100 for c in range(4)]
print(f"Per classe (riposo, chiudi, apri, polso): {np.round(per_class, 1)} | bilanciata {np.mean(per_class):.1f}%")

# reaction time: from the start of a labelled segment to the first decision of that class
onsets = np.flatnonzero((np.diff(lab) != 0) & (lab[1:] >= 0)) + 1
delays, kinds, missed = [], [], 0
for s in onsets:
    c, e = lab[s], s
    while e < len(lab) and lab[e] == c:
        e += 1
    hit = np.flatnonzero((ends >= s) & (ends < e) & (states == c))
    if len(hit):
        delays.append((ends[hit[0]] - s) / emg.FS)
        kinds.append(c)
    else:
        missed += 1
if delays:
    print(f"Tempo di reazione del decoder: mediana {np.median(delays) * 1000:.0f} ms "
          f"su {len(delays)} segmenti, {missed} segmenti mai riconosciuti")

d_arr, k_arr = np.array(delays), np.array(kinds)
print(f"Solo inizio dei movimenti: mediana {np.median(d_arr[k_arr > 0]) * 1000:.0f} ms | "
      f"ritorno a riposo: mediana {np.median(d_arr[k_arr == 0]) * 1000:.0f} ms")