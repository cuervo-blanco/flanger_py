import numpy as np
import matplotlib.pyplot as plt
from  fractional_delay import FractionalDelayWithCircularBuffer
from lfo import LFO
from main import flanger_effect

def test_fractional_delay():
    buffer_size = 16
    delay = 4.5
    
    fractional_delay = FractionalDelayWithCircularBuffer(buffer_size, delay)

    num_samples_to_write = 12
    input_samples = np.linspace(1, num_samples_to_write, num_samples_to_write)

    for sample in input_samples:
        fractional_delay.write_sample(sample)

    num_samples_to_read = 8
    output_samples = []

    for _ in range(num_samples_to_read):
        try:
            output_sample = fractional_delay.read_sample()
            output_samples.append(output_sample)
        except Exception as e:
            print("Error reading sample:", e)
            break

    assert len(output_samples) == num_samples_to_read, "Mismatch in the number of output samples."
    assert np.allclose(output_samples, input_samples[:num_samples_to_read]), "Output samples mismatch input samples."

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


test_fractional_delay()
test_lfo()
test_flanger_effect()

