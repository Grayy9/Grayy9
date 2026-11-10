"""Render the original orbital profile header. Requires Pillow."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math
ROOT=Path(__file__).resolve().parents[1]
W,H=1000,250
small=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',20)
large=ImageFont.truetype('C:/Windows/Fonts/consolab.ttf',70)
base=Image.new('RGB',(W,H));d=ImageDraw.Draw(base)
for y in range(H):
 t=y/(H-1);d.line((0,y,W,y),fill=tuple(round(a+(b-a)*t) for a,b in zip((8,14,27),(20,36,61))))
for x in range(0,W,32):d.line((x,0,x,H),fill=(19,42,59))
for y in range(0,H,32):d.line((0,y,W,y),fill=(19,42,59))
for y in (22,228):d.line((0,y,W,y),fill=(35,78,96))
for x in (30,970):d.line((x,22,x,228),fill=(35,78,96))
d.line((700,125,920,125),fill=(35,72,89));d.line((810,16,810,234),fill=(35,72,89))
d.ellipse((722,37,898,213),outline=(76,162,188),width=2)
d.ellipse((753,68,867,182),outline=(43,104,124),width=1)
d.text((68,45),'SYSTEM PROFILE // ONLINE',font=small,fill=(142,231,237))
d.text((65,91),'GRAYY9',font=large,fill=(244,251,255))
d.line((625,183,730,183),fill=(65,142,165),width=2);d.line((690,195,760,195),fill=(65,142,165),width=2)
frames=[]
for i in range(48):
 im=base.copy();p=ImageDraw.Draw(im);angle=2*math.pi*i/48
 pulse=(1+math.sin(angle*2))/2
 for r in (22,17):p.ellipse((810-r,125-r,810+r,125+r),outline=(23,round(58+20*pulse),round(73+20*pulse)),width=2)
 p.ellipse((800,115,820,135),fill=(80,round(175+35*pulse),round(190+35*pulse)))
 for offset,r,col in ((0,88,(164,169,255)),(math.pi,57,(101,233,238))):
  x=810+r*math.cos(angle+offset);y=125+r*math.sin(angle+offset)
  for j in range(7,0,-1):
   a=angle+offset-j*.045;xx=810+r*math.cos(a);yy=125+r*math.sin(a)
   p.ellipse((xx-2,yy-2,xx+2,yy+2),fill=tuple(round(c*(1-j/9)) for c in col))
  p.ellipse((x-4,y-4,x+4,y+4),fill=col)
 if i%12<7:p.text((325,91),'_',font=large,fill=(101,233,238))
 frames.append(im)
# One shared palette avoids color flicker between frames.
palette=base.quantize(colors=128)
frames=[f.quantize(palette=palette,dither=Image.Dither.NONE) for f in frames]
path=ROOT/'assets/orbit-header.gif'
frames[0].save(path,save_all=True,append_images=frames[1:],duration=125,loop=0,disposal=2,optimize=True)
with Image.open(path) as gif:
 assert gif.n_frames==48 and gif.size==(1000,250)
 assert gif.info['loop']==0
print(f'Validated GIF: 48 frames, 6-second loop, {path.stat().st_size} bytes')
