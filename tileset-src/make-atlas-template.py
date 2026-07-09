#!/usr/bin/env python3
"""Build a fill-in TEMPLATE for the tileset: a coordinate-labelled map of
tileset-lexy.png so you can draw each sprite into the right 32x32 cell.

Outputs:
  atlas-template.png  — the sheet at 2x with a numbered col/row ruler, a cell
                        grid, every tile named at its slot, and a green mark on
                        the tiles already re-skinned procedurally.
  tile-index.md       — a plain-text key: tile -> [col,row] and cell count.

Run from repo root:  python3 tileset-src/make-atlas-template.py"""
import json, os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHEET = os.path.join(ROOT, "tileset-lexy.png")
INDEX = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tile-index.json")
OUT_PNG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "atlas-template.png")
OUT_MD = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tile-index.md")

SCALE = 2
T = 32
CELL = T * SCALE          # 64
GRID = 32                 # tiles per side
MARGIN = 40               # ruler margin

# tiles already re-skinned by make-cottage-tiles.py
DONE = {(0,2),(0,3),(1,3),(8,2),(8,3),(9,2),(10,2),(13,2),(9,3),(12,2),(12,3),
        (0,6),(1,6),(2,6),(3,6),(0,7),(1,7),(2,7),(3,7),
        (4,7),(4,9),(5,9),(6,9),(7,9),(5,7),(6,7),(7,7),(6,8),(7,8),
        (8,4),(9,4),(10,4),(11,4),(8,5),(9,5),(10,5),(11,5)}

CATS = [
    ("terrain", (150,116,78), ("floor","wall","steel","dirt","gravel","sand","grass","spikes","hole","cracked_floor","ice","force_floor","slime","railroad","swivel","dash_floor","conveyor","green_floor","green_wall","purple_floor","purple_wall","custom","thin_walls","one_way","canopy","popwall","popdown","fake_","wall_invisible","wall_appearing","hint","floor_letter","electrified","turtle")),
    ("hazard", (196,90,44), ("water","fire","flame_jet")),
    ("key/door", (176,140,40), ("key_","door_","gate_")),
    ("item", (70,120,90), ("chip","green_bomb","score","stopwatch","flippers","boots","lightning","bribe","hook","foil","xray","helmet","bowling","dynamite","bomb","no_sign","gift","toll","dormant","skeleton","ankh","phantom","feather","dumbbell","remote","bucket","railroad_sign","cleats")),
    ("mechanism", (90,110,170), ("exit","socket","button","cloner","trap","scanner","light_switch","teleport","transmogrifier","turntable","thief","logic_gate","sokoban","no_player","doppelganger","nega_chip")),
    ("block", (120,90,60), ("dirt_block","ice_block","frame_block","boulder","burr","circuit_block","glass_block","green_block","log")),
    ("player", (170,70,120), ("player","bogus_player")),
    ("monster", (150,60,60), ("tank_","bug","paramecium","glider","ghost","blob","walker","teeth","bear","bull","green_twister","glint","shark","rover","fireball","floor_mimic","ball","rolling_ball","dynamite_lit")),
    ("effect", (110,110,120), ("explosion","splash","fall","transmogrify_flash","teleport_flash","puff","_exit","resurrection")),
]

def categorize(name):
    for cat, col, keys in CATS:
        for k in keys:
            if name.startswith(k) or ("_"+k in name) or name == k or k in name:
                return cat, col
    return "misc", (120,120,120)

def load_font(size):
    for p in ["/System/Library/Fonts/Menlo.ttc",
              "/System/Library/Fonts/Monaco.ttf",
              "/System/Library/Fonts/Supplemental/Arial.ttf",
              "/Library/Fonts/Arial.ttf"]:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, size)
            except Exception: pass
    return ImageFont.load_default()

def main():
    data = json.load(open(INDEX))["tiles"]
    sheet = Image.open(SHEET).convert("RGBA").resize((T*GRID*SCALE, T*GRID*SCALE), Image.NEAREST)

    W = MARGIN + T*GRID*SCALE
    H = MARGIN + T*GRID*SCALE
    im = Image.new("RGBA", (W, H), (244,238,226,255))
    im.paste(sheet, (MARGIN, MARGIN))
    d = ImageDraw.Draw(im, "RGBA")
    fnum = load_font(20)
    flabel = load_font(12)

    # (No dimming wash — ImageDraw fills *replace* pixels rather than compositing,
    # which would erase the art. The opaque label pills keep names legible.)

    # grid
    for i in range(GRID+1):
        x = MARGIN + i*CELL; y = MARGIN + i*CELL
        heavy = (i % 4 == 0)
        col = (60,48,36,150) if heavy else (60,48,36,60)
        w = 2 if heavy else 1
        d.line([(x, MARGIN), (x, H)], fill=col, width=w)
        d.line([(MARGIN, y), (W, y)], fill=col, width=w)

    # rulers
    for i in range(GRID):
        cx = MARGIN + i*CELL + CELL//2
        d.text((cx, MARGIN//2), str(i), fill=(90,72,52,255), font=fnum, anchor="mm")
        d.text((MARGIN//2, MARGIN + i*CELL + CELL//2), str(i), fill=(90,72,52,255), font=fnum, anchor="mm")

    # (every cell is now filled procedurally, so no per-cell "done" marks)

    # tile name labels at each primary cell
    for name, (c, r, cnt) in sorted(data.items(), key=lambda kv: (kv[1][1], kv[1][0])):
        cat, col = categorize(name)
        x0 = MARGIN + c*CELL; y0 = MARGIN + r*CELL
        label = name if cnt == 1 else f"{name} ({cnt})"
        tw = d.textlength(label, font=flabel)
        d.rectangle([x0+1, y0+1, x0+1+tw+6, y0+15], fill=(*col, 205))
        d.text((x0+4, y0+2), label, fill=(255,255,255,255), font=flabel)

    im.convert("RGB").save(OUT_PNG)
    print("wrote", OUT_PNG, im.size)

    # markdown key, grouped by category
    groups = {}
    for name, (c, r, cnt) in data.items():
        cat, _ = categorize(name)
        groups.setdefault(cat, []).append((name, c, r, cnt))
    order = [c[0] for c in CATS] + ["misc"]
    lines = ["# Tileset coordinate key",
             "",
             "`[col, row]` on the 32x32 grid of `tileset-lexy.png` (pixel = col*32, row*32). "
             "`×N` = cells in that tile's animation / direction set. ✅ = already re-skinned.", ""]
    done_primary = {(0,2),(0,3),(1,3),(8,2),(8,3),(9,2),(10,2),(13,2),(9,3),(12,2),
                    (0,6),(0,7),(4,7),(5,7),(6,7),(7,7),(6,8),(8,4),(9,4),(10,4),(11,4),
                    (8,5),(9,5),(10,5),(11,5)}
    for cat in order:
        if cat not in groups: continue
        lines.append(f"## {cat}")
        lines.append("")
        lines.append("| tile | col,row | cells |")
        lines.append("|---|---|---|")
        for name, c, r, cnt in sorted(groups[cat], key=lambda t: (t[2], t[1])):
            mark = " ✅" if (c, r) in done_primary else ""
            lines.append(f"| `{name}`{mark} | {c}, {r} | {cnt} |")
        lines.append("")
    open(OUT_MD, "w").write("\n".join(lines))
    print("wrote", OUT_MD)

if __name__ == "__main__":
    main()
