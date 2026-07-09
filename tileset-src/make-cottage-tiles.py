#!/usr/bin/env python3
"""Procedurally re-skin the geometric terrain tiles of tileset-lexy.png in a
cozy-cottage style. Deterministic (seeded). Characters, monsters, items and
mechanisms are left for a hand-drawn pixel-art pass.

Run from repo root:  python3 tileset-src/make-cottage-tiles.py
Overwrites tileset-lexy.png in place (original preserved in git history).
NOTE: re-exporting the .aseprite source would overwrite these tiles — fold them
into the source art when the hand-drawn pass begins."""
import random, math
from PIL import Image

SHEET = "tileset-lexy.png"
T = 32

def clamp(v): return max(0, min(255, int(v)))
def mix(a, b, t): return tuple(clamp(a[i] * (1 - t) + b[i] * t) for i in range(3))
def jit(c, rng, amt): return tuple(clamp(ch + (rng.random() - 0.5) * amt) for ch in c)
def img(): return Image.new("RGBA", (T, T), (0, 0, 0, 255))

# ---------------------------------------------------------------- floor: wood
def make_floor(seed=11):
    rng = random.Random(seed); im = img(); px = im.load()
    ph = 8; planks = [(176,138,96),(168,130,88),(184,146,104),(172,134,92)]
    for y in range(T):
        row = y // ph; base = planks[row % 4]; seam = (y % ph == 0)
        for x in range(T):
            g = (rng.random()-0.5)*0.10
            if (x*7+row*13) % 32 < 2: g -= 0.08
            c = tuple(clamp(ch*(1+g)) for ch in base)
            if seam: c = mix(c,(120,92,60),0.65)
            elif y % ph == ph-1: c = mix(c,(150,116,78),0.3)
            px[x,y]=(c[0],c[1],c[2],255)
    return im

def make_cracked_floor():
    im = make_floor(seed=11); px = im.load(); rng = random.Random(99)
    # a couple of jagged cracks
    for _ in range(2):
        x = rng.randint(6,26); y = 0
        while y < T:
            px[max(0,min(31,x)),y] = (70,52,34,255)
            if 0<=x-1<32: px[x-1,y]=(96,72,48,255)
            x += rng.choice([-1,0,0,1,1]); y += 1
    return im

# ---------------------------------------------------------------- wall: brick
def make_wall(seed=22):
    rng = random.Random(seed); im = img(); px = im.load()
    mortar=(214,196,168); cols=[(176,104,72),(166,96,66),(186,114,80)]; rh=8; bw=16
    for y in range(T):
        row=y//rh; off=(row%2)*(bw//2)
        for x in range(T):
            bx=(x+off)%bw
            if (y%rh==0) or bx==0:
                c=jit(mortar,rng,12)
            else:
                c=cols[((x+off)//bw+row*3)%3]; c=jit(c,rng,16)
                yy=y%rh
                if yy==1: c=tuple(clamp(ch*1.08) for ch in c)
                if yy==rh-1: c=tuple(clamp(ch*0.9) for ch in c)
            px[x,y]=(c[0],c[1],c[2],255)
    return im

# ---------------------------------------------------------------- stone (steel)
def make_stone(seed=44):
    rng = random.Random(seed); im = img(); px = im.load()
    mortar=(74,72,78); cols=[(126,124,130),(112,110,118),(138,136,142)]; rh=16; bw=16
    for y in range(T):
        row=y//rh; off=(row%2)*(bw//2)
        for x in range(T):
            bx=(x+off)%bw
            if (y%rh==0) or bx==0:
                c=jit(mortar,rng,10)
            else:
                c=cols[((x+off)//bw+row)%3]; c=jit(c,rng,20)
                yy=y%rh
                if yy<=1: c=tuple(clamp(ch*1.1) for ch in c)
                if yy>=rh-2: c=tuple(clamp(ch*0.85) for ch in c)
            px[x,y]=(c[0],c[1],c[2],255)
    return im

# ---------------------------------------------------------------- dirt / soil
def make_dirt(seed=55):
    rng = random.Random(seed); im = img(); px = im.load()
    base=(138,102,68)
    for y in range(T):
        for x in range(T):
            c=jit(base,rng,22)
            if rng.random()<0.06: c=mix(c,(96,68,42),0.6)   # clumps
            elif rng.random()<0.05: c=mix(c,(170,134,96),0.5)  # bright fleck
            px[x,y]=(c[0],c[1],c[2],255)
    return im

# ---------------------------------------------------------------- gravel path
def make_gravel(seed=66):
    rng = random.Random(seed); im = img(); px = im.load()
    base=(120,110,96)
    for y in range(T):
        for x in range(T):
            px[x,y]=(*jit(base,rng,10),255)
    pebbles=[(190,180,160),(168,150,128),(200,192,176),(150,140,124)]
    for _ in range(26):
        cx=rng.randint(0,31); cy=rng.randint(0,31); r=rng.randint(2,4); col=rng.choice(pebbles)
        for dy in range(-r,r+1):
            for dx in range(-r,r+1):
                if dx*dx+dy*dy<=r*r:
                    x=(cx+dx)%T; y=(cy+dy)%T
                    sh=1-(dy+r)/(2*r)*0.3
                    px[x,y]=(*tuple(clamp(ch*(0.85+sh*0.3)) for ch in jit(col,rng,10)),255)
    return im

# ---------------------------------------------------------------- sand
def make_sand(seed=77):
    rng = random.Random(seed); im = img(); px = im.load()
    base=(216,198,152)
    for y in range(T):
        rip=math.sin(y/32*math.pi*3)*6
        for x in range(T):
            c=jit(base,rng,10)
            c=tuple(clamp(ch+rip) for ch in c)
            px[x,y]=(c[0],c[1],c[2],255)
    return im

# ---------------------------------------------------------------- grass
def make_grass(seed=88):
    rng = random.Random(seed); im = img(); px = im.load()
    base=(108,150,76)
    for y in range(T):
        for x in range(T):
            px[x,y]=(*jit(base,rng,14),255)
    blades=[(92,132,60),(130,168,92),(84,120,54)]
    for _ in range(70):
        x=rng.randint(0,31); y=rng.randint(2,31); h=rng.randint(2,4); col=rng.choice(blades)
        for k in range(h):
            yy=y-k
            if 0<=yy<32: px[x,yy]=(*col,255)
    return im

# ---------------------------------------------------------------- ice family
ICE_BASE=(202,224,234); ICE_HI=(236,246,250); ICE_CRK=(150,188,210)
def make_ice(seed=101, cracks=1, glint=None):
    rng=random.Random(seed); im=img(); px=im.load()
    for y in range(T):
        for x in range(T):
            c=jit(ICE_BASE,rng,6)
            # diagonal sheen streaks
            if (x+y)%9<2: c=mix(c,ICE_HI,0.5)
            px[x,y]=(c[0],c[1],c[2],255)
    for _ in range(cracks):
        x=rng.randint(4,28); y=rng.randint(2,10)
        for _ in range(rng.randint(10,20)):
            if 0<=x<32 and 0<=y<32: px[x,y]=(*ICE_CRK,255)
            x+=rng.choice([-1,0,1]); y+=rng.choice([0,1,1])
    if glint is not None:
        gx,gy=glint
        for dx,dy in [(0,0),(1,0),(-1,0),(0,1),(0,-1)]:
            x,y=(gx+dx)%T,(gy+dy)%T; px[x,y]=(*ICE_HI,255)
    return im

def make_ice_corner(which):
    im=make_ice(seed=hash(which)%9999, cracks=0); px=im.load()
    bank=(150,120,84)  # a wooden lip on the closed side (cozy 'shore')
    for y in range(T):
        for x in range(T):
            edge=False
            if which=='se' and (x>=30 or y>=30): edge=True
            if which=='sw' and (x<=1 or y>=30): edge=True
            if which=='ne' and (x>=30 or y<=1): edge=True
            if which=='nw' and (x<=1 or y<=1): edge=True
            if edge: px[x,y]=(*bank,255)
    return im

# ---------------------------------------------------------------- fire (4 fr)
def make_fire(frame, seed=201):
    rng=random.Random(seed+frame*17); im=img(); px=im.load()
    ember=(48,24,16)
    for y in range(T):
        for x in range(T):
            px[x,y]=(*jit(ember,rng,8),255)
    body=(226,108,38); core=(250,214,96); tip=(252,168,60)
    for x in range(T):
        # flame height varies by column and frame (flicker)
        h = 14+10*abs(math.sin((x/32)*math.pi*2 + frame*1.3)) + rng.random()*4
        for y in range(T):
            up = T-1-y  # height from bottom
            if up < h:
                f = up/max(1,h)
                if f<0.45: c=body
                elif f<0.75: c=tip
                else: c=core
                # narrow the flame near the tip
                width_ok = abs(x-16) < (16 - up*0.35)
                if width_ok or f<0.3:
                    px[x,y]=(*jit(c,rng,18),255)
    return im

# ---------------------------------------------------------------- custom rugs / walls
RUG_TINTS={'green':(120,168,108),'pink':(212,150,176),'yellow':(224,200,120),'blue':(120,160,204)}
def make_custom_floor(color):
    rng=random.Random(hash('rug'+color)%9999); im=img(); px=im.load()
    tint=RUG_TINTS[color]; base=mix(tint,(120,96,70),0.35); weave=mix(tint,(255,255,255),0.18)
    for y in range(T):
        for x in range(T):
            c=weave if ((x+y)%4<2) else base
            c=jit(c,rng,10)
            # border
            if x<2 or x>29 or y<2 or y>29: c=mix(tint,(60,44,30),0.4)
            px[x,y]=(c[0],c[1],c[2],255)
    return im

def make_custom_wall(color):
    rng=random.Random(hash('paint'+color)%9999); im=img(); px=im.load()
    tint=RUG_TINTS[color]; wall=mix(tint,(240,232,214),0.35); panel=mix(tint,(90,70,52),0.25)
    for y in range(T):
        for x in range(T):
            c=wall
            # wainscot panel in lower half with a frame
            if y>16:
                if 3<x<28 and 19<y<29: c=panel
                elif y>=17 and (x in (2,29) or y in (17,30)): c=mix(tint,(70,52,38),0.5)
            c=jit(c,rng,8)
            px[x,y]=(c[0],c[1],c[2],255)
    return im

# ---------------------------------------------------------------- spikes / hole
def make_spikes():
    im=make_dirt(seed=303); px=im.load()
    stake=(96,74,52); tipc=(150,128,100)
    for bx in range(0,T,8):
        for k in range(7):
            y=24-k
            for x in range(bx+3-k//2, bx+5+k//2):
                if 0<=x<32 and 0<=y<32: px[x,y]=(*stake,255)
        px[bx+4, 17]=(*tipc,255)
    return im

def make_hole(open_top=True):
    im=img(); px=im.load(); pit=(30,24,20); rim=(150,116,78)
    for y in range(T):
        for x in range(T):
            if x<3 or y<3 or x>28 or y>28:
                c=rim if not (open_top and y<3) else pit
            else:
                d=1-((x-16)**2+(y-16)**2)/512
                c=mix((44,34,26),pit,max(0,min(1,d)))
            px[x,y]=(c[0],c[1],c[2],255)
    return im

# ---------------------------------------------------------------- composite
def main():
    s = Image.open(SHEET).convert("RGBA")
    def put(im, col, row): s.paste(im, (col*T, row*T))

    put(make_floor(), 0, 2)
    put(make_wall(), 0, 3)
    put(make_stone(), 1, 3)
    put(make_dirt(), 8, 2)
    put(make_gravel(), 8, 3)
    put(make_sand(), 9, 2)
    put(make_grass(), 10, 2)
    put(make_cracked_floor(), 13, 2)
    put(make_spikes(), 9, 3)
    put(make_hole(open_top=True), 12, 2)   # north
    put(make_hole(open_top=False), 12, 3)  # open

    # water (4 frames) — kept from the first pass
    for i in range(4):
        put(make_water_frame(i), i, 6)
    # fire (4 frames)
    for i in range(4):
        put(make_fire(i), i, 7)
    # ice family
    put(make_ice(), 4, 7)
    put(make_ice(seed=102, cracks=4), 5, 7)  # cracked_ice
    put(make_ice_corner('se'), 6, 7)
    put(make_ice_corner('sw'), 7, 7)
    put(make_ice_corner('ne'), 6, 8)
    put(make_ice_corner('nw'), 7, 8)
    for i,(c,r) in enumerate([(4,9),(5,9),(6,9),(7,9)]):  # ice shine frames
        put(make_ice(seed=110+i, cracks=0, glint=(8+i*6, 8+i*4)), c, r)

    # custom colour rugs + walls
    for i,col in enumerate(['green','pink','yellow','blue']):
        put(make_custom_floor(col), 8+i, 4)
        put(make_custom_wall(col), 8+i, 5)

    s.save(SHEET)
    print("re-skinned cozy terrain in", SHEET)

# soft rippling water (kept from first pass)
def make_water_frame(frame, seed=33):
    rng=random.Random(seed); im=img(); px=im.load()
    deep=(58,104,140); midc=(74,134,176); lite=(128,186,214); phase=frame/4*2*math.pi
    for y in range(T):
        for x in range(T):
            w=(math.sin((x/32)*2*math.pi*2+phase)+math.sin((y/32)*2*math.pi-phase*0.7))*0.5
            t=(w+1)/2; c=mix(deep,midc,min(1,t*1.3))
            if t>0.72: c=mix(c,lite,(t-0.72)/0.28)
            c=jit(c,rng,6); px[x,y]=(c[0],c[1],c[2],255)
    return im

if __name__ == "__main__":
    main()
