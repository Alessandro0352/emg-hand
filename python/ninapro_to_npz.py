"""Phase 2 (no hardware): turns a NinaPro file into a recording with the same format
as your board (4 channels, 14-bit ADC counts, classes 0-3), split into a training
file and a test file. Usage:
    python ninapro_to_npz.py ../data/raw/ninapro/S1_E1_A1.mat ../data/sim/S1
writes ../data/sim/S1_train.npz and ../data/sim/S1_test.npz"""
import sys, os, json
import numpy as np
from scipy.io import loadmat
from ninapro_baseline import load_subject, MOVES, CHANNELS_4

TEST_REPS = [5, 6]  # repetitions kept for the test file, never seen in training


def previous_move(path):
    """For every sample at 1 kHz, the NinaPro code of the last movement before it."""
    lab = loadmat(path)["restimulus"].ravel().astype(int)
    prev, last = np.zeros_like(lab), 0
    for i, v in enumerate(lab):
        if v > 0:
            last = v
        prev[i] = last
    return prev[::2]


src, out = sys.argv[1], sys.argv[2]
x, lab, rep = load_subject(src)               # 1 kHz, NinaPro codes, -1 = ignored
prev = previous_move(src)[:len(lab)]

# keep chosen movements, and the rest that follows them (drops the other movements)
keep = (lab > 0) | ((lab == 0) & np.isin(prev, MOVES))
x, lab, rep = x[keep][:, CHANNELS_4], lab[keep], rep[keep]

# NinaPro codes -> 0 rest, 1 close, 2 open, 3 wrist (same order you put in MOVES)
cls = np.full(len(lab), -1)
for i, code in enumerate(MOVES):
    cls[lab == code] = i

# volts -> counts of a 14-bit ADC centred at 8192, like the BioAmp on the Arduino
x = x - np.median(x, axis=0)
scale = 3000.0 / np.percentile(np.abs(x), 99.5)
counts = np.clip(np.round(8192 + x * scale), 0, 16383)

test = np.isin(rep, TEST_REPS)
os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
for name, use in [("train", ~test), ("test", test)]:
    label = np.where(use, cls, -1)            # windows of the other split are ignored
    n = len(label)
    np.savez_compressed(f"{out}_{name}.npz", counter=np.arange(n) % 16384, emg=counts,
                        acc=np.full((n, 3), 8192.0), label=label, rep=rep, true_class=cls,
                        t_host=np.arange(n) / 1000.0,
                        meta=json.dumps({"source": src, "moves": MOVES, "channels": CHANNELS_4,
                                         "split": name, "test_reps": TEST_REPS}))
    print(f"Scritto {out}_{name}.npz: {n} campioni ({n / 1000:.0f} s), "
          f"ripetizioni valutate {sorted(int(v) for v in set(rep[use & (cls >= 0)]))}")