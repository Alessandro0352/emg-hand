"""Phase 1: baseline on NinaPro DB2 with leave-one-repetition-out validation."""
import sys
import numpy as np
from scipy.io import loadmat
from scipy.signal import decimate
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix
import emg

MOVES = [0, 6, 5, 13]       # rest, fist, open (abduction of all fingers), wrist flexion
CHANNELS_4 = [8, 3, 9, 7]   # finger flexor, ring flexor side, finger extensor, ring extensor side


def load_subject(path):
    m = loadmat(path)
    x = m["emg"].astype(float)                     # (n, 12), 2 kHz
    lab = m["restimulus"].ravel().astype(int)
    rep = m["rerepetition"].ravel().astype(int)
    # rest has repetition 0: give it the repetition of the movement that precedes it
    last = 0
    for i in range(len(rep)):
        if rep[i] > 0:
            last = rep[i]
        elif lab[i] == 0:
            rep[i] = last
    # bring 2 kHz to 1 kHz so that windows are in the same samples as your hardware
    x = decimate(x, 2, axis=0, zero_phase=True)
    lab, rep = lab[::2], rep[::2]
    keep = np.isin(lab, MOVES)
    lab = np.where(keep, lab, -1)                  # -1 = ignored
    return x, lab, rep


def evaluate(x, lab, rep, causal):
    sos = emg.design_filters()
    xf = emg.filter_causal(x, sos) if causal else emg.filter_offline(x, sos)
    thr = emg.rest_threshold(xf[lab == 0])
    X, y, r, idx = emg.make_windows(xf, lab, rep, thr)
    classes = np.unique(y)
    win_acc, tr_acc, tr_time, cms = [], [], [], []
    for test_rep in np.unique(r[r > 0]):           # leave one repetition out
        tr, te = r != test_rep, r == test_rep
        clf = make_pipeline(StandardScaler(), LinearDiscriminantAnalysis())
        clf.fit(X[tr], y[tr])
        P = clf.predict_proba(X[te])
        win_acc.append(np.mean(clf.classes_[P.argmax(1)] == y[te]))
        a, t = emg.trial_metrics(P, y[te], idx[te], clf.classes_)
        tr_acc.append(a)
        tr_time.append(t)
        cms.append(confusion_matrix(y[te], clf.classes_[P.argmax(1)], labels=classes))
    return np.mean(win_acc), np.mean(tr_acc), np.mean(tr_time), sum(cms)


if __name__ == "__main__":
    for path in sys.argv[1:]:   # e.g. python ninapro_baseline.py ../data/raw/ninapro/S1_E1_A1.mat
        x, lab, rep = load_subject(path)
        for name, cols in [("12 canali", slice(None)), ("4 canali", CHANNELS_4)]:
            for causal in (False, True):
                wa, ta, tt, cm = evaluate(x[:, cols], lab, rep, causal)
                kind = "causale" if causal else "fase zero"
                print(f"{path} | {name} | {kind} | finestra {wa:.3f} | comando {ta:.3f} | tempo {tt:.2f} s")