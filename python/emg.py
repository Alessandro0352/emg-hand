"""Shared EMG processing: filters, windows, features, evidence accumulation."""
import numpy as np
from scipy import signal

FS = 1000   # sampling rate of your hardware [Hz]
WIN = 200   # window length [samples] = 200 ms at 1 kHz
STEP = 50   # window step [samples] = 50 ms at 1 kHz


def design_filters(fs=FS, band=(20.0, 450.0), notch=50.0):
    """Band-pass (Butterworth, order 4) + 50 Hz notch, as second-order sections."""
    sos_bp = signal.butter(4, band, btype="bandpass", fs=fs, output="sos")
    b, a = signal.iirnotch(notch, Q=30.0, fs=fs)
    return np.vstack([sos_bp, signal.tf2sos(b, a)])


def filter_offline(x, sos):
    """Zero-phase filtering. Only for offline analysis, never in real time."""
    return signal.sosfiltfilt(sos, x, axis=0)


def filter_causal(x, sos):
    """Causal filtering of a whole recording, identical to what runs online."""
    zi = signal.sosfilt_zi(sos)[:, :, None] * x[0][None, None, :]
    y, _ = signal.sosfilt(sos, x, axis=0, zi=zi)
    return y


class OnlineFilter:
    """Causal filter that keeps its internal state between blocks."""

    def __init__(self, sos):
        self.sos = sos
        self.zi = None

    def __call__(self, block):  # block: (n_samples, n_channels)
        if self.zi is None:     # start from steady state on the first sample
            self.zi = signal.sosfilt_zi(self.sos)[:, :, None] * block[0][None, None, :]
        y, self.zi = signal.sosfilt(self.sos, block, axis=0, zi=self.zi)
        return y


def td_features(win, thr):
    """Hudgins features for one window. win: (n, n_ch), thr: (n_ch,). Returns 4*n_ch values."""
    d = np.diff(win, axis=0)
    mav = np.mean(np.abs(win), axis=0)
    wl = np.sum(np.abs(d), axis=0)
    zc = np.sum((win[:-1] * win[1:] < 0) & (np.abs(d) >= thr), axis=0)
    ssc = np.sum((win[1:-1] - win[:-2]) * (win[1:-1] - win[2:]) >= thr ** 2, axis=0)
    return np.concatenate([mav, wl, zc, ssc]).astype(float)


def make_windows(x, labels, reps, thr, win=WIN, step=STEP):
    """Cut a recording into windows. Keeps only 'pure' windows (one label, one repetition).
    Returns features X, label y, repetition r, index of the last sample of each window."""
    X, y, r, idx = [], [], [], []
    for end in range(win, x.shape[0] + 1, step):
        lab = labels[end - win:end]
        rep = reps[end - win:end]
        if lab[0] != lab[-1] or np.any(lab != lab[0]) or np.any(rep != rep[0]) or lab[0] < 0:
            continue
        X.append(td_features(x[end - win:end], thr))
        y.append(lab[0])
        r.append(rep[0])
        idx.append(end - 1)
    return np.array(X), np.array(y), np.array(r), np.array(idx)


def rest_threshold(x_rest, k=2.0):
    """ZC/SSC threshold per channel: k times the standard deviation of the filtered rest signal."""
    return k * np.std(x_rest, axis=0)


def accumulate(D, p, alpha=0.3):
    """Evidence accumulation, same rule as the BCI project: D <- (1-alpha) D + alpha p."""
    return (1.0 - alpha) * D + alpha * p


def trial_metrics(P, y, idx, classes, alpha=0.3, threshold=0.7, step=STEP, fs=FS):
    """Command-level accuracy and time-to-command, like the BCI project.
    P: posteriors of the test windows in time order, y: true labels,
    idx: last-sample index of each window. A trial is a run of consecutive windows
    with the same label and no gap in time."""
    step_s = step / fs
    correct, times = [], []
    bounds = np.flatnonzero((np.diff(y) != 0) | (np.diff(idx) != step)) + 1
    for seg in np.split(np.arange(len(y)), bounds):
        D = np.ones(len(classes)) / len(classes)
        decided = None
        for k, i in enumerate(seg):
            D = accumulate(D, P[i], alpha)
            if D.max() >= threshold:
                decided, t = classes[np.argmax(D)], (k + 1) * step_s
                break
        if decided is None:  # forced decision at the end of the trial
            decided, t = classes[np.argmax(D)], len(seg) * step_s
        correct.append(decided == y[seg[0]])
        times.append(t)
    return float(np.mean(correct)), float(np.mean(times))
