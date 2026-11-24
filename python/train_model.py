"""Train the online decoder on one or more calibration recordings.
Usage: python train_model.py ../models/model.joblib ../data/raw/file1.npz [file2.npz ...]"""
import sys
import numpy as np
import joblib
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
import emg

sos = emg.design_filters()
Xs, ys, rests = [], [], []
files = sys.argv[2:]

for f in files:                                   # first pass: rest signal for the thresholds
    d = np.load(f)
    xf = emg.filter_causal(d["emg"], sos)         # causal, exactly as online
    rests.append(xf[d["label"] == 0])
thr = emg.rest_threshold(np.vstack(rests))

for f in files:                                   # second pass: windows and features
    d = np.load(f)
    xf = emg.filter_causal(d["emg"], sos)
    X, y, r, idx = emg.make_windows(xf, d["label"], d["rep"], thr)
    Xs.append(X)
    ys.append(y)
X, y = np.vstack(Xs), np.concatenate(ys)

clf = make_pipeline(StandardScaler(), LinearDiscriminantAnalysis()).fit(X, y)

n_ch = d["emg"].shape[1]
mav = X[:, :n_ch]                                 # the first n_ch features are the MAV
mvc = np.percentile(mav[y != 0], 95, axis=0)      # reference "strong" contraction per channel
rest_level = np.percentile(mav[y == 0], 95, axis=0) / mvc

joblib.dump({"clf": clf, "thr": thr, "mvc": mvc, "sos": sos,
             "deadzone": float(np.clip(rest_level.mean() * 1.2, 0.05, 0.5))}, sys.argv[1])
print(f"Modello salvato. Accuratezza sul training (ottimistica): {clf.score(X, y):.3f}")