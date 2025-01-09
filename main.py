import argparse
import numpy as np
import soundfile as sf

from lfo import LFO
from fractional_delay import FractionalDelayWithCircularBuffer
from fractional_delay import next_power_of_2

def flanger_effect(input_audio, sample_rate, depth, rate, delay_ms, wet, dry):
    buffer_size = next_power_of_2(int(sample_rate * (delay_ms / 1000 + depth)))
    delay = FractionalDelayWithCircularBuffer(buffer_size, delay_ms * sample_rate / 1000.0)
    lfo = LFO(rate, sample_rate)

    output_audio = np.zeros_like(input_audio)
    for i, sample in enumerate(input_audio):
        current_delay = delay_ms + lfo.out() * depth
        delay.read_pointer = (delay.write_pointer - current_delay * sample_rate / 1000) % buffer_size
        output_audio[i] = (sample * dry) + (wet * delay.read_sample())
        delay.write_sample(sample)

    return output_audio


def main():
    parser = argparse.ArgumentParser(description="Apply a flanger effect to an audio file.")
    parser.add_argument("input_file", help="Path to the input audio file (mandatory)")
    parser.add_argument("--output_file", default="output_flanger.wav", help="Path to save the output file (default: output_flanger.wav)")
    parser.add_argument("--wet", type=float, default=0.5, help="Wet mix (default: 0.5)")
    parser.add_argument("--dry", type=float, default=0.5, help="Dry mix (default: 0.5)")
    parser.add_argument("--depth", type=float, default=5.0, help="Depth of modulation in milliseconds (default: 5.0)")
    parser.add_argument("--rate", type=float, default=0.25, help="LFO rate in Hz (default: 0.25)")
    parser.add_argument("--delay_ms", type=float, default=10.0, help="Base delay in milliseconds (default: 10.0)")

    args = parser.parse_args()

    input_audio, sample_rate = sf.read(args.input_file)

    # converting to mono... for now
    if input_audio.ndim > 1:
        input_audio = np.mean(input_audio, axis=1)

    output_audio = flanger_effect(input_audio, sample_rate, args.depth, args.rate,
                                  args.delay_ms, args.wet, args.dry)

    sf.write(args.output_file, output_audio, sample_rate)

    import matplotlib.pyplot as plt
    plt.figure(figsize=(10, 6))
    plt.plot(input_audio[:1000], label="Original")
    plt.plot(output_audio[:1000], label="Flanger Effect")
    plt.legend()
    plt.title("Waveform Comparison")
    plt.xlabel("Sample Index")
    plt.ylabel("Amplitude")
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()
