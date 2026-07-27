#!/usr/bin/env python3
"""Generate a COMPLETE cozy-cottage tileset procedurally — every tile filled in,
so tileset-lexy.png is ready to import as-is (and every cell is a starting point
you can tweak). Terrain is textured; items/blocks/mechanisms are simple icons;
the player is a little butler; monsters are simple creatures; VFX are bursts.

Reads tileset-src/tile-cells.json (name -> [[col,row],...]) and paints each tile
into all of its cells. Run from repo root:  python3 tileset-src/make-tileset.py
Overwrites tileset-lexy.png (original preserved in git history)."""
import json, os, math, random
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SHEET = os.path.join(ROOT, "tileset-lexy.png")
CELLS = json.load(open(os.path.join(HERE, "tile-cells.json")))
T = 32
OUT = (46, 34, 26)   # dark outline

# ---- palette --------------------------------------------------------------
WOOD=(176,138,96); WOOD_D=(120,92,60); WOOD_L=(196,160,116)
BRICK=(176,104,72); MORT=(214,196,168)
STONE=(126,124,130); STONE_D=(74,72,78)
DIRTC=(138,102,68); GRAV=(150,140,124); SANDC=(216,198,152); GRASSC=(108,150,76)
ICEC=(202,224,234); ICE_HI=(236,246,250); ICE_CRK=(150,188,210)
WATERC=(74,134,176); WATER_D=(58,104,140); WATER_L=(128,186,214)
FIREC=(226,108,38); FIRE_HI=(250,214,96)
CREAM=(240,230,210)
KEY={'red':(210,74,62),'blue':(74,116,204),'yellow':(228,198,82),'green':(98,178,98)}
BTN={'blue':(74,116,204),'green':(98,178,98),'red':(210,74,62),'brown':(150,104,64),
     'pink':(224,140,176),'black':(70,64,72),'orange':(230,150,60),'gray':(150,148,150),
     'cyan':(96,190,200),'yellow':(228,198,82)}

def rng(seed): return random.Random(seed)
def clamp(v): return max(0,min(255,int(v)))
def jit(c,r,a): return tuple(clamp(x+(r.random()-0.5)*a) for x in c)
def TT(): return Image.new("RGBA",(T,T),(0,0,0,0))
def OO(c): return Image.new("RGBA",(T,T),(c[0],c[1],c[2],255))
def D(im): return ImageDraw.Draw(im,"RGBA")
def disc(d,cx,cy,r,fill,line=OUT,w=1):
    d.ellipse([cx-r,cy-r,cx+r,cy+r],fill=fill,outline=line,width=w)
def eyes(d,cx,cy,dx=4,r=2):
    for s in(-1,1):
        d.ellipse([cx+s*dx-r,cy-r,cx+s*dx+r,cy+r],fill=(250,250,250,255))
        d.ellipse([cx+s*dx-1,cy-1,cx+s*dx+1,cy+1],fill=(20,20,20,255))

# ---- terrain textures (opaque) -------------------------------------------
def floor(seed=11):
    r=rng(seed); im=OO(WOOD); px=im.load(); ph=8
    pl=[(176,138,96),(168,130,88),(184,146,104),(172,134,92)]
    for y in range(T):
        row=y//ph; b=pl[row%4]
        for x in range(T):
            c=jit(b,r,18)
            if y%ph==0: c=tuple(clamp(v*0.72) for v in c)
            elif y%ph==ph-1: c=tuple(clamp(v*0.9) for v in c)
            px[x,y]=(c[0],c[1],c[2],255)
    return im
def brickwall(seed=22):
    r=rng(seed); im=OO(BRICK); px=im.load(); rh=8; bw=16
    cols=[(176,104,72),(166,96,66),(186,114,80)]
    for y in range(T):
        row=y//rh; off=(row%2)*8
        for x in range(T):
            bx=(x+off)%bw
            c=jit(MORT,r,12) if (y%rh==0 or bx==0) else jit(cols[((x+off)//bw+row)%3],r,16)
            px[x,y]=(c[0],c[1],c[2],255)
    return im
def blocks(seed,base,mort,rh=16,bw=16):
    r=rng(seed); im=OO(base); px=im.load()
    for y in range(T):
        row=y//rh; off=(row%2)*(bw//2)
        for x in range(T):
            bx=(x+off)%bw
            c=jit(mort,r,10) if (y%rh==0 or bx==0) else jit(base,r,20)
            px[x,y]=(c[0],c[1],c[2],255)
    return im
def noise_tile(base,seed,amt=22,speck=None):
    r=rng(seed); im=OO(base); px=im.load()
    for y in range(T):
        for x in range(T):
            c=jit(base,r,amt)
            if speck and r.random()<0.06: c=speck
            px[x,y]=(c[0],c[1],c[2],255)
    return im
def gravel(seed=66):
    r=rng(seed); im=noise_tile(GRAV,seed,10); px=im.load()
    for _ in range(24):
        cx,cy,rad=r.randint(0,31),r.randint(0,31),r.randint(2,4)
        col=jit((186,176,158),r,20)
        for dy in range(-rad,rad+1):
            for dx in range(-rad,rad+1):
                if dx*dx+dy*dy<=rad*rad:
                    px[(cx+dx)%T,(cy+dy)%T]=(col[0],col[1],col[2],255)
    return im
def grass(seed=88):
    im=noise_tile(GRASSC,seed,14); px=im.load(); r=rng(seed+1)
    for _ in range(70):
        x,y=r.randint(0,31),r.randint(3,31); col=(90,132,60)
        for k in range(r.randint(2,4)):
            if 0<=y-k<32: px[x,y-k]=(col[0],col[1],col[2],255)
    return im
def cracked(base_fn):
    im=base_fn(); px=im.load(); r=rng(9)
    for _ in range(2):
        x,y=r.randint(6,26),0
        while y<T:
            px[max(0,min(31,x)),y]=(70,52,34,255); x+=r.choice([-1,0,0,1,1]); y+=1
    return im
def ice(seed=101,cr=1,glint=None):
    r=rng(seed); im=OO(ICEC); px=im.load()
    for y in range(T):
        for x in range(T):
            c=jit(ICEC,r,6)
            if (x+y)%9<2: c=ICE_HI
            px[x,y]=(c[0],c[1],c[2],255)
    for _ in range(cr):
        x,y=r.randint(4,28),r.randint(2,10)
        for _ in range(14):
            if 0<=x<32 and 0<=y<32: px[x,y]=(*ICE_CRK,255)
            x+=r.choice([-1,0,1]); y+=r.choice([0,1,1])
    if glint:
        for dx,dy in[(0,0),(1,0),(-1,0),(0,1),(0,-1)]: px[(glint[0]+dx)%T,(glint[1]+dy)%T]=(*ICE_HI,255)
    return im
def ice_corner(which):
    im=ice(seed=hash(which)%9999,cr=0); px=im.load(); bank=(150,120,84)
    for y in range(T):
        for x in range(T):
            e=(which=='se'and(x>=30 or y>=30))or(which=='sw'and(x<=1 or y>=30))or(which=='ne'and(x>=30 or y<=1))or(which=='nw'and(x<=1 or y<=1))
            if e: px[x,y]=(*bank,255)
    return im
def water(f):
    r=rng(33); im=OO(WATERC); px=im.load(); ph=f/4*2*math.pi
    for y in range(T):
        for x in range(T):
            w=(math.sin(x/32*2*math.pi*2+ph)+math.sin(y/32*2*math.pi-ph*0.7))*0.5; t=(w+1)/2
            c=tuple(clamp(WATER_D[i]*(1-min(1,t*1.3))+WATERC[i]*min(1,t*1.3)) for i in range(3))
            if t>0.72: c=tuple(clamp(c[i]*(1-(t-.72)/.28)+WATER_L[i]*((t-.72)/.28)) for i in range(3))
            px[x,y]=(*jit(c,r,6),255)
    return im
def fire(f):
    r=rng(201+f*17); im=OO((48,24,16)); px=im.load()
    for x in range(T):
        h=14+10*abs(math.sin(x/32*math.pi*2+f*1.3))+r.random()*4
        for y in range(T):
            up=T-1-y
            if up<h:
                fr=up/max(1,h); c=FIREC if fr<0.5 else (FIRE_HI if fr>0.75 else (250,168,60))
                if abs(x-16)<(16-up*0.35) or fr<0.3: px[x,y]=(*jit(c,r,18),255)
    return im
def custom_rug(color):
    r=rng(hash('rug'+color)%9999); im=TT(); px=im.load()
    tint=KEY.get(color,BTN.get(color,(150,150,150)))
    base=tuple(clamp(tint[i]*0.55+WOOD_D[i]*0.45) for i in range(3))
    weave=tuple(clamp(tint[i]*0.7+255*0.3) for i in range(3))
    for y in range(T):
        for x in range(T):
            c=weave if (x+y)%4<2 else base
            if x<2 or x>29 or y<2 or y>29: c=tuple(clamp(tint[i]*0.6+60*0.4) for i in range(3))
            px[x,y]=(*jit(c,r,10),255)
    return im
def custom_wall(color):
    r=rng(hash('pw'+color)%9999); tint=KEY.get(color,BTN.get(color,(150,150,150)))
    wall=tuple(clamp(tint[i]*0.4+236*0.6) for i in range(3)); im=OO(wall); px=im.load()
    panel=tuple(clamp(tint[i]*0.7+90*0.3) for i in range(3))
    for y in range(T):
        for x in range(T):
            c=wall
            if y>16 and 3<x<28 and 19<y<29: c=panel
            elif y>16 and (x in(2,29) or y in(17,30)): c=tuple(clamp(tint[i]*0.5+70*0.5) for i in range(3))
            px[x,y]=(*jit(c,r,8),255)
    return im
def toggle_floor(color,f=0):
    base=KEY.get(color,(120,170,110)); im=OO(tuple(clamp(base[i]*0.5+CREAM[i]*0.5) for i in range(3)))
    d=D(im); d.rectangle([0,0,31,31],outline=tuple(clamp(v*0.7) for v in base),width=2)
    d.line([8,16,24,16],fill=base,width=2); d.line([16,8,16,24],fill=base,width=2)
    return im
def toggle_wall(color):
    base=KEY.get(color,(120,170,110)); return blocks(hash(color)%999,tuple(clamp(v*0.7) for v in base),tuple(clamp(v*0.45) for v in base))
def arrow_floor(dirn,f=0,base=WOOD):
    im=floor(seed=hash(dirn)%99); d=D(im); c=(90,70,50,180)
    cx=16; ys=[6,14,22]
    for i,y in enumerate(ys):
        yy=(y+f*3)%28+2
        if dirn=='n': d.polygon([(cx,yy-3),(cx-5,yy+3),(cx+5,yy+3)],fill=c)
        elif dirn=='s': d.polygon([(cx,yy+3),(cx-5,yy-3),(cx+5,yy-3)],fill=c)
        elif dirn=='e': d.polygon([(yy+3,cx),(yy-3,cx-5),(yy-3,cx+5)],fill=c)
        else: d.polygon([(yy-3,cx),(yy+3,cx-5),(yy+3,cx+5)],fill=c)
    return im
def conveyor(dirn,f=0):
    im=blocks(hash('cv'+dirn)%999,(120,112,104),(88,82,76),rh=6,bw=32); d=D(im)
    for y in range(2,30,6):
        yy=(y+f*2)%28+2; d.line([2,yy,30,yy],fill=(60,56,52,200))
    return arrow_over(im,dirn,f)
def arrow_over(im,dirn,f):
    d=D(im); c=(240,232,214,220)
    yy=(8+f*4)%20+6
    if dirn=='n': d.polygon([(16,yy-3),(11,yy+3),(21,yy+3)],fill=c)
    elif dirn=='s': d.polygon([(16,yy+3),(11,yy-3),(21,yy-3)],fill=c)
    elif dirn=='e': d.polygon([(yy+3,16),(yy-3,11),(yy-3,21)],fill=c)
    else: d.polygon([(yy-3,16),(yy+3,11),(yy+3,21)],fill=c)
    return im
def slime(f):
    r=rng(303+f); im=OO((96,150,74)); px=im.load()
    for y in range(T):
        for x in range(T):
            w=math.sin((x+y+f*4)/5.0); c=(110,166,86) if w>0.3 else (86,138,66)
            px[x,y]=(*jit(c,r,12),255)
    return im
def dash_floor(f):
    im=floor(seed=44); d=D(im)
    for x in range(0,32,8):
        xx=(x+f*3)%32; d.line([xx,4,xx+4,4],fill=(230,200,120,200),width=2); d.line([xx,26,xx+4,26],fill=(230,200,120,200),width=2)
    return im
def rail():
    im=noise_tile((150,140,124),7,8); d=D(im)
    d.line([2,16,30,16],fill=(90,72,54),width=2); d.line([2,12,30,12],fill=(120,100,78),width=1); d.line([2,20,30,20],fill=(120,100,78),width=1)
    for x in range(4,30,6): d.line([x,10,x,22],fill=(96,74,52),width=2)
    return im
def teleport_pad(color,f=0):
    base=KEY.get(color,BTN.get(color,(150,150,150))); im=OO(tuple(clamp(v*0.3) for v in base)); d=D(im)
    for i in range(5):
        a=f*0.5+i*1.2; rr=4+i*2
        x=16+math.cos(a)*rr; y=16+math.sin(a)*rr
        d.ellipse([x-2,y-2,x+2,y+2],fill=(*tuple(clamp(v*1.2) for v in base),255))
    disc(d,16,16,3,tuple(clamp(v*1.4) for v in base))
    return im
def exit_tile(f=0):
    im=floor(seed=5); d=D(im)
    d.rectangle([8,4,24,30],fill=(120,80,50),outline=OUT,width=1)
    d.rectangle([10,6,22,28],fill=(150,104,64))
    d.ellipse([18,16,21,19],fill=(230,200,90))  # knob
    glow=(250,220,120,80+f*20); d.rectangle([10,6,22,28],outline=glow,width=1)
    return im
def socket():
    im=brickwall(); d=D(im); d.ellipse([10,10,22,22],fill=(60,50,44),outline=OUT); d.text((13,11),"?",fill=(230,210,160))
    return im
def cloner():
    im=blocks(3,(110,100,110),(70,64,72)); d=D(im); d.rectangle([8,8,24,24],outline=(200,200,210),width=1); d.line([16,8,16,24],fill=(200,200,210)); d.line([8,16,24,16],fill=(200,200,210))
    return im
def trap(open_=False):
    im=floor(seed=6); d=D(im); col=(60,50,44) if not open_ else (30,24,20)
    d.rectangle([6,6,26,26],fill=col,outline=OUT);
    if not open_: d.line([6,16,26,16],fill=(90,74,58),width=1)
    return im
def canopy():
    im=TT(); d=D(im)
    for _ in range(40):
        pass
    r=rng(7)
    for x in range(T):
        for y in range(T):
            if (x*y+x*3)%7<3: im.putpixel((x,y),(70,120,70,150))
    return im
def thin_wall_edges():
    im=TT(); d=D(im)
    d.rectangle([0,0,31,3],fill=(*BRICK,255)); d.rectangle([0,28,31,31],fill=(*BRICK,255))
    d.rectangle([0,0,3,31],fill=(*BRICK,255)); d.rectangle([28,0,31,31],fill=(*BRICK,255))
    return im

# ---- items / actors (transparent) ----------------------------------------
def chip(f=0):
    im=TT(); d=D(im); disc(d,16,16,9,(226,180,90)); disc(d,16,16,5,(240,206,120),line=None)
    d.text((12,9),"$",fill=(120,80,30)); return im
def nega(f=0):
    im=TT(); d=D(im); disc(d,16,16,9,(90,80,110)); disc(d,16,16,5,(120,110,150),line=None); return im
def keyspr(color):
    im=TT(); d=D(im); c=KEY[color]
    disc(d,12,11,5,c); d.ellipse([10,9,14,13],fill=None,outline=(255,255,255,120))
    d.rectangle([15,13,18,26],fill=c,outline=OUT); d.rectangle([18,22,22,25],fill=c); d.rectangle([18,17,21,19],fill=c)
    return im
def doorspr(color):
    im=TT(); d=D(im); c=KEY[color]
    d.rectangle([6,4,26,30],fill=c,outline=OUT); d.rectangle([9,7,23,27],outline=tuple(clamp(v*0.7) for v in c),width=1)
    disc(d,16,17,3,(250,240,210)); return im
def gatespr(color):
    im=TT(); d=D(im); c=KEY[color]
    for x in range(6,27,5): d.line([x,4,x,28],fill=c,width=2)
    d.line([6,10,26,10],fill=c,width=2); d.line([6,22,26,22],fill=c,width=2); return im
def boot(color=(140,100,66),accent=None):
    im=TT(); d=D(im)
    d.polygon([(10,8),(18,8),(18,22),(24,22),(24,26),(10,26)],fill=color,outline=OUT)
    if accent: d.rectangle([10,22,24,26],fill=accent)
    return im
def bombspr(lit=False):
    im=TT(); d=D(im); disc(d,15,19,8,(60,58,64)); d.rectangle([14,8,17,12],fill=(90,88,94))
    if lit: d.ellipse([13,4,19,10],fill=(250,200,80))
    else: d.line([15,12,18,7],fill=(180,140,60),width=1)
    return im
def token(text,col=(226,180,90)):
    im=TT(); d=D(im); disc(d,16,16,10,col); disc(d,16,16,6,tuple(clamp(v*1.15) for v in col),line=None)
    d.text((16-3*len(text),11),text,fill=(90,60,20)); return im
def clock(tint=(230,220,200)):
    im=TT(); d=D(im); disc(d,16,16,9,tint); d.line([16,16,16,9],fill=OUT,width=1); d.line([16,16,21,16],fill=OUT,width=1); return im
def button(color,down=False):
    im=floor(seed=hash(color)%99); d=D(im); c=BTN.get(color,(150,150,150))
    r=6 if not down else 5; disc(d,16,16,r,c);
    if not down: disc(d,16,14,3,tuple(clamp(v*1.25) for v in c),line=None)
    return im
def gem(col):
    im=TT(); d=D(im); d.polygon([(16,6),(24,14),(16,26),(8,14)],fill=col,outline=OUT); d.polygon([(16,6),(20,14),(16,16),(12,14)],fill=tuple(clamp(v*1.3) for v in col)); return im
# blocks
def crate(tint=(170,128,84)):
    im=TT(); d=D(im); d.rectangle([3,3,28,28],fill=tint,outline=OUT,width=1)
    d.rectangle([3,3,28,28],outline=tuple(clamp(v*0.7) for v in tint),width=1)
    d.line([3,3,28,28],fill=tuple(clamp(v*0.8) for v in tint)); d.line([28,3,3,28],fill=tuple(clamp(v*0.8) for v in tint))
    return im
def rockblk():
    im=TT(); d=D(im); disc(d,16,17,12,(140,132,120)); disc(d,13,13,4,(170,162,150),line=None); return im
def logblk():
    im=TT(); d=D(im); d.rounded_rectangle([2,8,30,24],5,fill=(150,110,68),outline=OUT)
    disc(d,8,16,4,(120,86,52)); d.arc([5,13,11,19],0,360,fill=(90,64,40)); return im
# player butler
def butler(shirt=(238,232,222)):
    im=TT(); d=D(im)
    d.ellipse([11,13,21,26],fill=(58,50,62),outline=OUT)      # suit body
    d.polygon([(16,14),(13,24),(19,24)],fill=shirt)            # shirt front
    d.ellipse([15,20,17,22],fill=(150,40,40))                 # bowtie center
    d.polygon([(13,20),(15,21),(13,22)],fill=(170,50,50)); d.polygon([(19,20),(17,21),(19,22)],fill=(170,50,50))
    disc(d,16,9,5,(232,196,164))                              # head
    d.chord([11,3,21,12],180,360,fill=(60,44,34))             # hair
    d.ellipse([14,8,15,10],fill=(30,20,16)); d.ellipse([17,8,18,10],fill=(30,20,16))  # eyes
    d.ellipse([11,25,15,29],fill=(40,34,40)); d.ellipse([17,25,21,29],fill=(40,34,40))# shoes
    return im
# monsters
def creature(body,eye=True,horns=False,ears=False,ghost=False):
    im=TT(); d=D(im)
    if ghost:
        d.pieslice([6,6,26,30],180,360,fill=(*body,200)); d.rectangle([6,18,26,28],fill=(*body,200))
        for x in range(6,27,5): d.ellipse([x,26,x+5,31],fill=(0,0,0,0))
    else:
        disc(d,16,17,11,body)
    if ears: d.polygon([(8,8),(12,4),(13,12)],fill=body,outline=OUT); d.polygon([(24,8),(20,4),(19,12)],fill=body,outline=OUT)
    if horns: d.polygon([(9,9),(6,3),(12,8)],fill=(240,230,210)); d.polygon([(23,9),(26,3),(20,8)],fill=(240,230,210))
    if eye: eyes(d,16,15,4,2)
    return im
def toothy(body):
    im=creature(body,eye=True,ears=True); d=D(im)
    d.polygon([(11,20),(13,25),(15,20)],fill=(255,255,255)); d.polygon([(17,20),(19,25),(21,20)],fill=(255,255,255))
    return im
def flameball():
    im=TT(); d=D(im); disc(d,16,17,10,(226,108,38)); disc(d,16,15,6,(250,200,90),line=None); disc(d,16,13,3,(255,240,180),line=None); return im
def rubberball(col=(90,150,210)):
    im=TT(); d=D(im); disc(d,16,16,10,col); d.ellipse([11,10,16,15],fill=(255,255,255,140)); return im
def tankbot(col):
    im=TT(); d=D(im); d.rounded_rectangle([5,8,27,26],3,fill=col,outline=OUT); d.rectangle([13,3,19,10],fill=tuple(clamp(v*0.8) for v in col),outline=OUT); eyes(d,16,17,4,2); return im
def robot():
    im=TT(); d=D(im); d.rounded_rectangle([5,6,27,28],3,fill=(150,150,160),outline=OUT); d.ellipse([12,12,20,20],fill=(90,160,200)); d.ellipse([14,14,17,17],fill=(20,30,40)); return im
# vfx
def burst(f,col,n=8):
    im=TT(); d=D(im); R=4+f*4
    for i in range(n):
        a=i/n*2*math.pi; x=16+math.cos(a)*R; y=16+math.sin(a)*R
        d.ellipse([x-2,y-2,x+2,y+2],fill=(*col,max(0,220-f*50)))
    return im
def ring(f,col):
    im=TT(); d=D(im); R=3+f*5; d.ellipse([16-R,16-R,16+R,16+R],outline=(*col,max(0,220-f*45)),width=2); return im

# ---- dispatch: name -> list of frame images ------------------------------
def frames_for(name):
    n=name; k=n.split('_')[-1]
    # terrain opaque
    if n=='floor': return [floor()]
    if n=='wall': return [brickwall()]
    if n=='steel': return [blocks(44,STONE,STONE_D)]
    if n=='dirt': return [noise_tile(DIRTC,55,22,(100,72,46))]
    if n=='gravel': return [gravel()]
    if n=='sand': return [noise_tile(SANDC,77,10)]
    if n=='grass': return [grass()]
    if n=='cracked_floor': return [cracked(floor)]
    if n=='spikes':
        im=noise_tile(DIRTC,303,18); d=D(im)
        for bx in range(2,30,7): d.polygon([(bx,26),(bx+3,14),(bx+6,26)],fill=(150,128,100),outline=OUT)
        return [im]
    if n=='hole': return [ (lambda:(lambda im:(D(im).ellipse([4,4,28,28],fill=(28,22,18),outline=OUT) or im))(floor(seed=8)))() ]
    if n=='water': return [water(i) for i in range(4)]
    if n=='fire': return [fire(i) for i in range(4)]
    if n=='ice': return [ice()]
    if n=='cracked_ice': return [ice(cr=4)]
    if n in('ice_se','ice_sw','ice_ne','ice_nw'): return [ice_corner(k)]
    if n in('green_floor','purple_floor'): return [toggle_floor('green' if 'green' in n else 'blue')]
    if n in('green_wall','purple_wall'): return [toggle_wall('green' if 'green' in n else 'blue')]
    if n.startswith('floor_custom_'): return [custom_rug(k)]
    if n.startswith('wall_custom_'): return [custom_wall(k)]
    if n.startswith('force_floor_'):
        dv={'n':'n','e':'e','s':'s','w':'w','all':'n'}[k]; return [arrow_floor(dv,i) for i in range(4)]
    if n.startswith('conveyor_'): return [conveyor(k,i) for i in range(4)]
    if n=='slime': return [slime(i) for i in range(4)]
    if n=='dash_floor': return [dash_floor(i) for i in range(4)]
    if n=='railroad' or n.startswith('swivel') or n.startswith('turntable'): return [rail()]
    if n.startswith('teleport'):
        col={'red':'red','blue':'blue','yellow':'yellow','green':'green','rainbow':'pink','exit':'blue'}.get(k,'blue')
        return [teleport_pad(col,i) for i in range(4)]
    if n=='exit': return [exit_tile(i) for i in range(4)]
    if n=='socket': return [socket()]
    if n=='cloner': return [cloner()]
    if n=='trap': return [trap(False),trap(True)]
    if n=='scanner': return [blocks(9,(120,120,140),(80,80,100))]
    if n=='turtle': return [ice(seed=60,cr=0)]
    if n in('flame_jet_off',): return [brickwall()]
    if n=='flame_jet_on': return [fire(i) for i in range(3)]
    if n=='electrified_floor': return [toggle_floor('yellow')]
    if n in('sokoban_floor',): return [toggle_floor('yellow')]
    if n in('sokoban_wall',): return [toggle_wall('yellow')]
    if n in('canopy',): return [canopy()]
    if n in('thin_walls','one_way_walls'): return [thin_wall_edges()]
    if n in('popwall','popwall2','fake_wall','popdown_wall','wall_invisible','wall_appearing'): return [brickwall()]
    if n in('fake_floor','popdown_floor','floor_mimic','floor_ankh'): return [floor()]
    if n=='hint':
        im=floor(); d=D(im); d.text((13,10),"?",fill=(90,70,50)); return [im]
    if n in('no_player1_sign','no_player2_sign'):
        im=floor(); d=D(im); d.ellipse([6,6,26,26],outline=(180,60,60),width=2); d.line([9,9,23,23],fill=(180,60,60),width=2); return [im]
    # items
    if n=='chip' or n=='chip_extra': return [chip()]
    if n=='green_chip': return [token("$",(120,180,110))]
    if n=='nega_chip': return [nega()]
    if n=='green_bomb': return [bombspr()]
    if n.startswith('key_'): return [keyspr(k)]
    if n.startswith('door_'): return [doorspr(k)]
    if n.startswith('gate_'): return [gatespr(k)]
    if n=='flippers': return [boot((80,150,170),(200,230,240))]
    if n=='fire_boots': return [boot((180,90,60),(240,180,80))]
    if n=='cleats': return [boot((140,140,150),(90,90,100))]
    if n=='suction_boots': return [boot((150,120,180))]
    if n=='hiking_boots': return [boot((150,110,70))]
    if n=='speed_boots': return [boot((110,170,120),(220,230,180))]
    if n in('bomb','dormant_bomb'): return [bombspr()]
    if n=='dynamite' or n=='dynamite_lit': return [ (lambda im:(D(im).rectangle([12,10,20,26],fill=(190,70,60),outline=OUT) or D(im).line([16,10,16,5],fill=(200,160,80),width=1) or im))(TT()) ]
    if n.startswith('score_'): return [token(k.replace('x','×'))]
    if n.startswith('stopwatch'): return [clock()]
    if n=='lightning_bolt': return [ (lambda im:(D(im).polygon([(18,4),(10,18),(15,18),(13,28),(22,12),(17,12)],fill=(240,210,90),outline=OUT) or im))(TT()) ]
    if n=='helmet': return [ (lambda im:(D(im).pieslice([8,8,24,26],180,360,fill=(150,160,170),outline=OUT) or im))(TT()) ]
    if n=='bowling_ball': return [rubberball((70,60,80))]
    if n=='bribe' or n=='gift_bow': return [token("★",(230,180,90))]
    if n=='xray_eye': return [ (lambda im:(D(im).ellipse([7,11,25,21],fill=(240,240,245),outline=OUT) or D(im).ellipse([13,12,19,20],fill=(90,140,180)) or im))(TT()) ]
    if n in('remote_gray','remote_green'): return [crate((110,110,120) if 'gray' in n else (110,160,110))]
    if n in('bucket_water','bucket_fire'): return [token("~",(90,140,180) if 'water' in n else (220,120,60))]
    if n in('feather',): return [gem((230,230,240))]
    if n in('dumbbell',): return [ (lambda im:(D(im).line([8,16,24,16],fill=(80,80,90),width=3) or D(im).ellipse([5,11,11,21],fill=(90,90,100)) or D(im).ellipse([21,11,27,21],fill=(90,90,100)) or im))(TT()) ]
    if n in('skeleton_key','hook','foil','ankh','phantom_ring','toll_gate','no_sign','railroad_sign','thief_tools','thief_keys','thief_lock'):
        return [gem((200,180,120))]
    # buttons / mechanisms
    if n.startswith('button_'): return [button(k,False),button(k,True)]
    if n.startswith('light_switch'): return [button('gray','on' in n)]
    if n=='transmogrifier': return [teleport_pad('pink',0)]
    if n=='sokoban_button': return [button('blue',False)]
    # blocks
    if n=='dirt_block': return [crate((150,108,68))]
    if n=='ice_block': return [crate((180,210,224))]
    if n=='frame_block': return [crate((160,150,130))]
    if n=='glass_block': return [ (lambda im:(D(im).rectangle([4,4,27,27],fill=(200,220,230,120),outline=(255,255,255,180)) or im))(TT()) ]
    if n=='green_block': return [crate((110,160,110))]
    if n=='circuit_block': return [crate((120,140,120))]
    if n=='sokoban_block': return [crate((170,120,80))]
    if n=='boulder': return [rockblk()]
    if n=='burr': return [rockblk()]
    if n=='log': return [logblk()]
    if n=='logic_gate': return [ (lambda im:(D(im).pieslice([6,8,26,24],270,90,fill=(120,130,140),outline=OUT) or im))(TT()) ]
    # player + doppel
    if n=='player': return [butler()]
    if n=='player2': return [butler((240,220,230))]
    if n.startswith('bogus_player'): return [butler()]
    # monsters
    if n=='fireball': return [flameball()]
    if n=='ball': return [rubberball((90,150,210))]
    if n=='rolling_ball': return [rubberball((120,110,100))]
    if n=='tank_blue': return [tankbot((80,110,190))]
    if n=='tank_yellow': return [tankbot((220,190,80))]
    if n=='bug': return [creature((110,160,80),ears=False)]
    if n=='paramecium': return [creature((200,150,170))]
    if n=='glider': return [ (lambda im:(D(im).polygon([(16,4),(28,26),(16,20),(4,26)],fill=(120,180,200),outline=OUT) or im))(TT()) ]
    if n=='ghost': return [creature((210,215,230),ghost=True)]
    if n=='blob': return [creature((120,180,110))]
    if n=='walker': return [creature((170,120,190),ears=True)]
    if n=='teeth': return [toothy((150,110,80))]
    if n=='teeth_timid': return [toothy((180,160,120))]
    if n=='bear': return [creature((150,110,80),ears=True)]
    if n=='bull': return [creature((120,100,90),horns=True)]
    if n=='shark': return [creature((110,130,150))]
    if n=='green_twister': return [creature((120,180,120))]
    if n=='glint': return [gem((240,240,250))]
    if n=='rover': return [robot()]
    if n=='floor_mimic': return [floor()]
    # vfx
    if n in('explosion',): return [burst(i,(250,180,80)) for i in range(4)]
    if n in('splash',): return [ring(i,(120,180,220)) for i in range(4)]
    if n in('splash_slime',): return [ring(i,(140,190,90)) for i in range(4)]
    if n in('fall',): return [burst(i,(120,100,80)) for i in range(4)]
    if n in('puff',): return [burst(i,(220,220,220)) for i in range(4)]
    if n in('transmogrify_flash',): return [ring(i,(210,150,200)) for i in range(7)]
    if n in('teleport_flash',): return [ring(i,(150,200,230)) for i in range(4)]
    if n in('player1_exit','player2_exit','resurrection'): return [ring(i,(240,220,140)) for i in range(4)]
    # fallback
    return [gem((170,150,120))]

def main():
    sheet=Image.open(SHEET).convert("RGBA")
    n_tiles=0; n_cells=0
    for name,cells in CELLS.items():
        fr=frames_for(name);
        if not fr: continue
        n_tiles+=1
        for i,(c,r) in enumerate(cells):
            sheet.paste(fr[i%len(fr)],(c*T,r*T)); n_cells+=1
    sheet.save(SHEET)
    print(f"filled {n_cells} cells across {n_tiles} tiles -> {SHEET}")

if __name__=="__main__":
    main()
