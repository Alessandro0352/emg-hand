"""Online decoder. Receives raw samples, returns one decision every 50 ms."""
import numpy as np
import emg


class Decoder:
    def __init__(self, model, alpha=0.3, threshold=0.7):
        self.clf, self.thr, self.mvc = model["clf"], model["thr"], model["mvc"]
        self.deadzone = model["deadzone"]
        self.filter = emg.OnlineFilter(model["sos"])
        self.classes = self.clf.classes_
        self.n_ch = len(self.mvc)
        self.buf = np.zeros((emg.WIN, self.n_ch))   # last 200 ms, already filtered
        self.pending = 0                             # new samples since the last decision
        self.filled = 0                              # samples in the buffer (max 200)
        self.D = np.ones(len(self.classes)) / len(self.classes)
        self.state = 0                               # current class (starts at rest)
        self.alpha, self.threshold = alpha, threshold

    def update(self, raw):
        """raw: (m, n_ch) ADC samples. Returns a list of decisions (class, speed, D)."""
        out = []
        y = self.filter(raw)
        for sample in y:                             # push sample by sample into the buffer
            self.buf[:-1] = self.buf[1:]
            self.buf[-1] = sample
            self.pending += 1
            self.filled = min(self.filled + 1, emg.WIN)
            if self.pending >= emg.STEP and self.filled == emg.WIN:   # decide only on a full window
                self.pending = 0
                out.append(self.decide())
            elif self.pending >= emg.STEP:
                self.pending = 0
        return out

    def decide(self):
        f = emg.td_features(self.buf, self.thr)
        p = self.clf.predict_proba(f[None, :])[0]
        self.D = emg.accumulate(self.D, p, self.alpha)
        if self.D.max() >= self.threshold:           # change class only with enough evidence
            self.state = self.classes[np.argmax(self.D)]
        level = np.mean(f[:self.n_ch] / self.mvc)    # normalised MAV, 0 = rest, 1 = strong
        speed = float(np.clip((level - self.deadzone) / (1 - self.deadzone), 0, 1))
        return self.state, speed, self.D.copy()