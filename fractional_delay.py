import numpy as np
from numpy import ceil, log2, zeros

def next_power_of_2(x):
    return int(2 ** (ceil(log2(x))))

class FractionalDelayWithCircularBuffer:
    def __init__(self, size, delay: float):
        size = next_power_of_2(size)
        self.wrap_mask = size - 1
        self.buffer = zeros((size,))
        self.write_pointer = 0
        self.read_pointer = (self.write_pointer - delay) % self.buffer.shape[0]

    def interpolate(self, values, index):
        low = int(index) & self.wrap_mask
        high = int(np.ceil(index)) & self.wrap_mask

        if low == high:
            return values[low]

        return (index - low) * values[high %
                                      values.shape[0]] + (high - index) * values[low]

    def write_sample(self, sample: float):
        if self.write_pointer == self.read_pointer:
            raise Exception("Overrun: the write pointer passed the read pointer")
        
        self.buffer[self.write_pointer] = sample
        self.write_pointer = (self.write_pointer + 1) & self.wrap_mask

    def read_sample(self):
        if self.read_pointer == self.write_pointer:
            raise Exception("Underrun: the read pointer passed the write pointer")

        sample = self.interpolate(self.buffer, self.read_pointer)

        self.read_pointer = (self.read_pointer + 1.0) % self.buffer.shape[0]
        return sample
