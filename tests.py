import numpy as np
import matplotlib.pyplot as plt
from  fractional_delay import FractionalDelayWithCircularBuffer
from lfo import LFO

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

    print("Input Samples:", input_samples)
    print("Output Samples:", output_samples)

    assert len(output_samples) == num_samples_to_read, "Mismatch in the number of output samples."
    print("Test passed.")

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

    time = np.linspace(0, duration, num_samples, endpoint=False)
    plt.plot(time, output)
    plt.title("LFO Output (Debug)")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.grid()
    plt.show()

    print("Debug: Peak value (expected ~1):", peak_value)
    print("Debug: Negative peak value (expected ~-1):", negative_peak_value)
    print("Debug: Zero crossing (expected ~0):", zero_crossing_value)

    assert np.isclose(peak_value, 1, atol=1e-2), "LFO does not reach peak amplitude."
    assert np.isclose(negative_peak_value, -1, atol=1e-2), "LFO does not reach negative peak."
    assert np.isclose(zero_crossing_value, 0, atol=1e-2), "LFO does not cross zero correctly."

    print("LFO test passed!")    


test_fractional_delay()
test_lfo()

