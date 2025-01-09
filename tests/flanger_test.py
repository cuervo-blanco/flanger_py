import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np
import matplotlib.pyplot as plt

from  fractional_delay import FractionalDelayWithCircularBuffer
from lfo import LFO
from main import flanger_effect

def test_fractional_delay_streaming():
    buffer_size = 16
    delay = 4.5
    frac_delay = FractionalDelayWithCircularBuffer(buffer_size, delay)

    input_samples = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 
                              7.0, 8.0, 9.0, 10.0, 11.0, 12.0])
    
    output_samples = []
    
    for sample in input_samples:
        frac_delay.write_sample(sample)
        out = frac_delay.read_sample()
        output_samples.append(out)

    assert len(output_samples) == len(input_samples)
    
    # print("Output:", output_samples)


def test_fractional_delay_with_warmup():
    buffer_size = 16
    delay = 4.5
    frac_delay = FractionalDelayWithCircularBuffer(buffer_size, delay)

    input_samples = np.arange(1, 13, dtype=np.float64)  # [1.0, 2.0, ..., 12.0]
    
    for sample in input_samples:
        frac_delay.write_sample(sample)

    warmup_count = int(np.ceil(delay))
    for _ in range(warmup_count):
        frac_delay.read_sample()
    
    output_samples = []
    for _ in range(len(input_samples) - warmup_count):
        output_samples.append(frac_delay.read_sample())

    assert len(output_samples) == len(input_samples) - warmup_count

    assert not np.allclose(output_samples, 0), "Output is all zeros after warm-up!"


def test_lfo():
    freq = 1
    sample_rate = 100
    duration = 2

    lfo = LFO(freq=freq, sample_rate=sample_rate)

    num_samples = int(sample_rate * duration)
    output = np.array([lfo.out() for _ in range(num_samples)])

    peak_value = np.max(output)
    negative_peak_value = np.min(output)
    zero_crossing_value = output[num_samples // 4]

    assert np.isclose(peak_value, 1, atol=1e-2), "LFO does not reach peak amplitude."
    assert np.isclose(negative_peak_value, -1, atol=1e-2), "LFO does not reach negative peak."
    assert np.isclose(zero_crossing_value, 0, atol=1e-2), "LFO does not cross zero correctly."


def test_flanger_effect():
    sample_rate = 44100
    duration = 1.0  # 1 second
    input_audio = np.sin(2 * np.pi * 440 * np.arange(int(sample_rate * duration)) / sample_rate)
    depth = 5.0
    rate = 0.25
    delay_ms = 10.0
    wet = 0.5
    dry = 0.5

    output_audio = flanger_effect(input_audio, sample_rate, depth, rate, delay_ms, wet, dry)
    assert len(output_audio) == len(input_audio), "Output audio length mismatch."
    assert not np.allclose(output_audio, input_audio), "Effect not applied."


test_fractional_delay_streaming()
test_fractional_delay_with_warmup()
test_lfo()
test_flanger_effect()

