# /// script
# dependencies = ["pillow"]
# ///
# Usage: uv run build.py cuts.txt out.mp4
# cuts.txt: one caption line per row -> "Caption text | clip,start,end ; clip,start,end". Lines starting with # are ignored.
# Each part becomes one hard-cut segment with the caption burned in and a small "parody" tag.
import subprocess, os, sys, textwrap
from PIL import Image, ImageDraw, ImageFont
W,H=1280,720; TAG=os.environ.get('TAG','parody')
FONTS=['/System/Library/Fonts/Supplemental/Arial Bold.ttf','/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf']
def font(n):
    for p in FONTS:
        if os.path.exists(p): return ImageFont.truetype(p,n)
    return ImageFont.load_default(n)
ENC=['-r','30','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-ar','48000','-ac','2','-b:a','192k']
os.makedirs('build/seg',exist_ok=True); os.makedirs('build/cap',exist_ok=True)
def run(a): subprocess.run(a,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)

def cap_png(text,i):
    im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im); f=font(40)
    lines=textwrap.wrap(text,44); y=H-60-len(lines)*50
    bw=max(d.textlength(l,font=f) for l in lines)
    d.rounded_rectangle(((W-bw)/2-18,y-8,(W+bw)/2+18,y+len(lines)*50+8),12,fill=(0,0,0,150))
    for l in lines:
        d.text(((W-d.textlength(l,font=f))/2,y),l,font=f,fill='white',stroke_width=4,stroke_fill='black'); y+=50
    d.text((W-120,20),TAG,font=font(20),fill=(255,255,255,140))
    p=f'build/cap/{i:03d}.png'; im.save(p); return p

segs=[]
for row in open(sys.argv[1]):
    row=row.strip()
    if not row or row.startswith('#'): continue
    text,parts=[x.strip() for x in row.split('|',1)]
    for part in parts.split(';'):
        f,s,e=[x.strip() for x in part.split(',')]; s,e=float(s),float(e)
        i=len(segs); d=e-s; o=f'build/seg/{i:03d}.mp4'
        # 15 ms fade-in / 25 ms fade-out removes clicks at hard cuts without sounding like an effect.
        fc=f"[0:v]scale={W}:{H},fps=30[v0];[v0][1:v]overlay=0:0,format=yuv420p[v];[0:a]aresample=48000,afade=t=in:d=0.015,afade=t=out:st={max(0,d-0.025):.3f}:d=0.025[a]"
        run(['ffmpeg','-y','-ss',str(s),'-t',f'{d:.3f}','-i',f'raw/{f}.mp4','-i',cap_png(text,i),'-filter_complex',fc,'-map','[v]','-map','[a]',*ENC,o])
        segs.append(o)
open('build/list.txt','w').write(''.join(f"file '{os.path.abspath(s)}'\n" for s in segs))
run(['ffmpeg','-y','-f','concat','-safe','0','-i','build/list.txt','-c','copy',sys.argv[2]])
print('ok',len(segs),'segments ->',sys.argv[2])
