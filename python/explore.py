"""Phase 1: first look at a NinaPro file. Run it from the python/ folder."""
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat

m = loadmat("../data/raw/ninapro/S1_E1_A1.mat")
print([k for k in m if not k.startswith("__")])          # which variables are in the file
emg, lab, rep = m["emg"], m["restimulus"].ravel(), m["rerepetition"].ravel()
print(emg.shape, np.unique(lab), np.unique(rep))          # samples x channels, labels, repetitions

t = np.arange(len(emg)) / 2000
fig, ax = plt.subplots(2, 1, sharex=True)
ax[0].plot(t, emg[:, 6]); ax[0].set_ylabel("EMG canale 1")
ax[1].plot(t, lab); ax[1].set_ylabel("movimento")
plt.show()