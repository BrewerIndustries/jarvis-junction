#!/usr/bin/env python3
"""Synthesize the wall-bump effort grunts ("unh") via simple formant synthesis.
Pure stdlib (wave + math). Run from the repo root: `python3 sfx/make-grunt.py`.
Writes grunt1.wav / grunt2.wav into sfx/."""
import wave, struct, math, random

SR = 44100
OUT_DIR = "sfx"

def synth_grunt(path, dur=0.24, f0_start=150.0, f0_end=98.0,
                formants=((640, 90), (1080, 110), (2400, 160)), seed=1,
                breath=0.06):
    rng = random.Random(seed)
    n = int(SR * dur)
    samples = []
    phase = 0.0
    for i in range(n):
        t = i / n
        # pitch falls over the grunt (effort releasing)
        f0 = f0_start * (1 - t) + f0_end * t
        f0 *= 1.0 + 0.01 * math.sin(2 * math.pi * 18 * (i / SR))  # subtle jitter
        phase += 2 * math.pi * f0 / SR

        # voiced source: harmonics shaped by formant resonances
        s = 0.0
        for h in range(1, 26):
            fh = f0 * h
            if fh > 4200:
                break
            amp = 1.0 / h  # glottal rolloff
            w = 0.0
            for (ff, bw) in formants:
                w += 1.0 / (1.0 + ((fh - ff) / bw) ** 2)
            s += amp * w * math.sin(phase * h)

        # breath noise, strongest at the onset
        s += breath * math.exp(-t * 6.0) * (rng.random() * 2 - 1)

        # amplitude envelope: fast attack, short plateau, decay
        attack = min(1.0, (i / SR) / 0.012)
        decay = math.exp(-max(0.0, (i / SR) - 0.05) * 9.0)
        samples.append(s * attack * decay)

    peak = max(1e-6, max(abs(x) for x in samples))
    scale = 0.85 / peak
    frames = b''.join(struct.pack('<h', int(max(-1, min(1, x * scale)) * 32767)) for x in samples)
    with wave.open(path, 'w') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(frames)
    print("wrote", path, f"({n} samples, {dur}s)")

synth_grunt(f"{OUT_DIR}/grunt1.wav", f0_start=152, f0_end=100,
            formants=((640, 90), (1080, 110), (2400, 160)), seed=3)
synth_grunt(f"{OUT_DIR}/grunt2.wav", dur=0.20, f0_start=138, f0_end=92,
            formants=((600, 85), (1000, 105), (2200, 150)), seed=7)
