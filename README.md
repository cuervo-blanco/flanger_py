## Flanger_py

This script lets you add a flanger effect to your audio files. It uses techniques 
like a Circular Buffer and Fractional Delay to achieve the sweeping modulation of a flanger. 
At its core, the flanger effect is powered by an LFO (Low-Frequency Oscillator) 
that modulates the delay time, creating that iconic swirling sound.

A big shoutout to **Jan Wilzcek** from [thewolfsound](https://thewolfsound.com/) 
for sharing insights on Circular Buffers and Fractional Delays—they were instrumental in building this effect.

### How to Use
Let’s say you’ve got an audio file called `input_audio.wav`, and you want to 
give it some flanger magic. Here’s how you can do it:

```bash
python flanger_script.py input_audio.wav --output_file output_flanger.wav --wet 0.7 --dry 0.3 --depth 7.0 --rate 0.5 --delay_ms 12.0
```

### What the Parameters Mean:
- **`input_audio.wav`**: Your original audio file.
- **`--output_file output_flanger.wav`**: The name of the processed file (default: `output_flanger.wav`).
- **`--wet 0.7`**: The amount of the effect in the mix (higher = more flanger).
- **`--dry 0.3`**: The amount of the original sound in the mix.
- **`--depth 7.0`**: How deep the modulation goes (measured in milliseconds, default: `5.0` ms).
- **`--rate 0.5`**: Speed of the modulation in Hz (default: `0.25` Hz).
- **`--delay_ms 12.0`**: The base delay time before modulation (default: `10.0` ms).

After running the command, you’ll end up with a new file called `output_flanger.wav`, 
complete with the flanger effect. Feel free to tweak the parameters to create your own unique sound!

