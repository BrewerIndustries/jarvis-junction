#!/usr/bin/env python3
"""Procedurally re-skin the high-coverage terrain tiles (floor, wall, water) of
tileset-lexy.png in a cozy-cottage style: warm wood-plank floor, honey-brick
wall, and soft rippling water. Deterministic (seeded). Characters/monsters are
left untouched for a later art pass.

Run from repo root:  python3 tileset-src/make-cottage-tiles.py
Overwrites tileset-lexy.png in place (original preserved in git history)."""
import random
from PIL import Image

SHEET = "tileset-lexy.png"
T = 32  # tile size

def clamp(v): return max(0, min(255, int(v)))
def mix(a, b, t): return tuple(clamp(a[i] * (1 - t) + b[i] * t) for i in range(3))

# ---- cozy-cottage floor: warm wood planks ----------------------------------
def make_floor(seed=11):
    rng = random.Random(seed)
    img = Image.new("RGBA", (T, T), (0, 0, 0, 255))
    px = img.load()
    plank_h = 8
    planks = [
        (176, 138, 96), (168, 130, 88), (184, 146, 104), (172, 134, 92),
    ]
    for y in range(T):
        row = y // plank_h
        base = planks[row % len(planks)]
        seam = (y % plank_h == 0)  # dark groove between planks
        for x in range(T):
            c = base
            # long horizontal grain streaks
            g = (rng.random() - 0.5) * 0.10
            # a few darker grain lines per plank
            if (x * 7 + row * 13) % 32 < 2:
                g -= 0.08
            c = tuple(clamp(ch * (1 + g)) for ch in c)
            if seam:
                c = mix(c, (120, 92, 60), 0.65)
            elif y % plank_h == plank_h - 1:
                c = mix(c, (150, 116, 78), 0.3)  # soft shadow above the groove
            px[x, y] = (c[0], c[1], c[2], 255)
    return img

# ---- cozy-cottage wall: warm honey brick -----------------------------------
def make_wall(seed=22):
    rng = random.Random(seed)
    img = Image.new("RGBA", (T, T), (0, 0, 0, 255))
    px = img.load()
    mortar = (214, 196, 168)
    brick_cols = [(176, 104, 72), (166, 96, 66), (186, 114, 80)]
    row_h = 8
    brick_w = 16
    for y in range(T):
        row = y // row_h
        offset = (row % 2) * (brick_w // 2)
        for x in range(T):
            bx = (x + offset) % brick_w
            is_mortar = (y % row_h == 0) or (bx == 0)
            if is_mortar:
                c = mortar
                c = tuple(clamp(ch + (rng.random() - 0.5) * 12) for ch in c)
            else:
                bi = ((x + offset) // brick_w + row * 3) % len(brick_cols)
                c = brick_cols[bi]
                c = tuple(clamp(ch + (rng.random() - 0.5) * 16) for ch in c)
                # subtle top highlight / bottom shadow within each brick
                yy = y % row_h
                if yy == 1: c = tuple(clamp(ch * 1.08) for ch in c)
                if yy == row_h - 1: c = tuple(clamp(ch * 0.9) for ch in c)
            px[x, y] = (c[0], c[1], c[2], 255)
    return img

# ---- soft rippling water (4 animation frames) ------------------------------
import math
def make_water_frame(frame, seed=33):
    rng = random.Random(seed)
    img = Image.new("RGBA", (T, T), (0, 0, 0, 255))
    px = img.load()
    deep = (58, 104, 140)
    mid = (74, 134, 176)
    lite = (128, 186, 214)
    phase = frame / 4.0 * 2 * math.pi
    for y in range(T):
        for x in range(T):
            # two overlapping sine ripples that scroll with the frame
            w = (math.sin((x / 32) * 2 * math.pi * 2 + phase) +
                 math.sin((y / 32) * 2 * math.pi * 1 - phase * 0.7)) * 0.5
            t = (w + 1) / 2  # 0..1
            c = mix(deep, mid, min(1, t * 1.3))
            if t > 0.72:
                c = mix(c, lite, (t - 0.72) / 0.28)
            c = tuple(clamp(ch + (rng.random() - 0.5) * 6) for ch in c)
            px[x, y] = (c[0], c[1], c[2], 255)
    return img

def main():
    sheet = Image.open(SHEET).convert("RGBA")
    def paste(img, col, row):
        sheet.paste(img, (col * T, row * T))
    paste(make_floor(), 0, 2)   # floor.base  [0,2]
    paste(make_wall(), 0, 3)    # wall        [0,3]
    for i in range(4):          # water anim  [0..3, 6]
        paste(make_water_frame(i), i, 6)
    sheet.save(SHEET)
    print("re-skinned floor, wall, water in", SHEET)

if __name__ == "__main__":
    main()
