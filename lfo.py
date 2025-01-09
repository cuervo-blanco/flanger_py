# create an LFO that modifies the delay in the FractionalDelayWithCircularBuffer
import matplotlib.pyplot as plt
import numpy as np

class LFO:
    def __init__(self, freq, sample_rate):
        self.freq = freq
        self.sample_rate = sample_rate
        self.phase = 0
        self.phase_increment = (2 * np.pi * self.freq) / self.sample_rate

    def out(self):
        value = np.sin(self.phase)
        self.phase += self.phase_increment

        self.phase %= 2 * np.pi

        return value
