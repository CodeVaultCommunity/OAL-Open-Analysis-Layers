"""Render the editable bilingual OAL illustrations. This is an asset renderer.

Run: python -m pip install cairosvg==2.9.1
     python assets/sources/render_images.py

The art background and original OAL mark are embedded into self-contained SVGs.
Labels, grouping, connectors and icons remain editable SVG elements. The PNGs
have the same canvas sizes as the illustrations they replace.
"""
from __future__ import annotations

import base64
import html
import json
from pathlib import Path

import cairosvg
from PIL import ImageFont

HERE = Path(__file__).resolve().parent
ASSETS = HERE.parent
LABELS = json.loads((HERE / "labels.json").read_text(encoding="utf-8"))
NAVY = "#06134f"
BLUE = "#0051dc"
CYAN = "#00c9ed"
MUTED = "#3c51a3"
FONT = "Arial, Helvetica, Nimbus Sans, sans-serif"


def font_file(bold=False):
    name = "NimbusSans-Bold.otf" if bold else "NimbusSans-Regular.otf"
    candidates = [Path("/usr/share/fonts/opentype/urw-base35") / name,
                  Path("C:/Windows/Fonts") / ("arialbd.ttf" if bold else "arial.ttf"),
                  Path("/usr/share/fonts/truetype/liberation2") / ("LiberationSans-Bold.ttf" if bold else "LiberationSans-Regular.ttf")]
    return next((p for p in candidates if p.exists()), None)


def text(x, y, value, size=28, bold=False, anchor="start", fill=BLUE, width=None):
    size = float(size)
    path = font_file(bold)
    if width is not None and path is not None:
        face = ImageFont.truetype(str(path), round(size * 4))
        measured = face.getlength(value) / 4
        if measured > width:
            size *= width / measured
    value = html.escape(value)
    return f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size:.2f}" font-weight="{700 if bold else 400}" text-anchor="{anchor}" fill="{fill}">{value}</text>'


def rect(x, y, w, h, rx=24, fill="url(#panel)", stroke=CYAN, sw=4):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def card(x, y, w, h, rx=32):
    return rect(x, y, w, h, rx, sw=6) + rect(x+3, y+3, w-6, h-6, rx-3, fill="none", stroke="#6ed2ff", sw=1)


def pill(x, y, w, h, label, size=28, strong=True):
    return card(x, y, w, h, h/2) + text(x+w/2, y+h/2+size*.34, label, size, strong, "middle", NAVY, w-28)


def badge(x, y, value, w=90, h=50):
    return rect(x, y, w, h, 19, "#c5edfc", "none", 0) + text(x+w/2, y+h/2+11, value, 31, True, "middle", NAVY)


def up_arrow(x, start, end, double=False):
    # start is the lower endpoint and end is the upper endpoint.
    p = f'M {x-9},{start} L {x+9},{start} L {x+9},{end+26} L {x+23},{end+26} L {x},{end} L {x-23},{end+26} L {x-9},{end+26} Z'
    out = f'<path d="{p}" fill="url(#arrow)" stroke="#77dcff" stroke-width="2"/>'
    if double:
        out += f'<path d="M{x-23},{start-26} L{x+23},{start-26} L{x},{start} Z" fill="url(#arrow)" stroke="#77dcff" stroke-width="2"/>'
    return out


def right_arrow(x, y):
    return f'<path d="M{x},{y-8} H{x+20} V{y-20} L{x+39},{y} L{x+20},{y+20} V{y+8} H{x} Z" fill="url(#arrow)" stroke="#4ccfff" stroke-width="1.5"/>'


def icon(kind, cx, cy, diameter=138):
    s = diameter/100
    parts = [f'<g transform="translate({cx-diameter/2} {cy-diameter/2}) scale({s})">', '<circle cx="50" cy="50" r="49" fill="url(#iconbg)"/>', '<g fill="white" stroke="#0054e8" stroke-width="5" stroke-linecap="round" stroke-linejoin="round">']
    if kind == "ucs":
        parts += ['<rect x="27" y="19" width="49" height="65" rx="6"/>', '<path d="M38 34H60 M38 45H65 M38 56H65 M38 67H58" fill="none" stroke-width="4"/>']
    elif kind == "model":
        parts += ['<path d="M50 41V50 M50 50L28 68 M50 50L72 68" fill="none"/>', '<rect x="38" y="22" width="25" height="18" rx="3"/>', '<rect x="17" y="66" width="24" height="18" rx="3"/>', '<rect x="60" y="66" width="24" height="18" rx="3"/>']
    elif kind == "test":
        parts += ['<rect x="26" y="22" width="49" height="60" rx="5"/>', '<path d="M38 54L48 64L66 39" fill="none" stroke="#008f83" stroke-width="6"/>']
    elif kind == "code":
        parts += ['<rect x="21" y="26" width="59" height="50" rx="6"/>', '<path d="M43 42L33 51L43 60 M59 42L69 51L59 60" fill="none"/>']
    elif kind == "browser":
        parts += ['<rect x="20" y="24" width="62" height="55" rx="6"/>', '<path d="M21 41H81" fill="none" stroke-width="4"/>', '<circle cx="29" cy="33" r="2.5" fill="#0054e8" stroke="none"/><circle cx="38" cy="33" r="2.5" fill="#0054e8" stroke="none"/><circle cx="47" cy="33" r="2.5" fill="#0054e8" stroke="none"/>', '<rect x="31" y="51" width="22" height="18" rx="4" fill="url(#teal)" stroke="none"/><path d="M62 55H71 M62 65H71" fill="none" stroke-width="4"/>']
    elif kind == "external":
        parts += ['<path d="M53 30H29V73H69V52 M50 27H77V54 M77 27L48 56" fill="none"/>']
    elif kind == "target":
        parts += ['<circle cx="48" cy="54" r="23" fill="none"/><circle cx="48" cy="54" r="12" fill="none"/><path d="M48 54L76 26 M67 26H76V35" fill="none"/>']
    elif kind == "shield":
        parts += ['<path d="M50 22L72 31V52Q72 69 50 81Q28 69 28 52V31Z" fill="none"/>', '<path d="M40 49L48 57L62 41" fill="none"/>']
    elif kind == "people":
        parts += ['<circle cx="39" cy="38" r="9" fill="none"/><circle cx="66" cy="39" r="8" fill="none"/>', '<path d="M21 74V62Q21 50 39 50Q56 50 56 62V74Z M59 55Q79 52 79 66V74H65" fill="none"/>']
    parts += ['</g></g>']
    return ''.join(parts)


def defs():
    return '''<defs>
      <linearGradient id="panel" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#fbfdff"/><stop offset=".55" stop-color="#f1faff"/><stop offset="1" stop-color="#e9f6ff"/></linearGradient>
      <linearGradient id="arrow" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#0079ff"/><stop offset="1" stop-color="#00c9ee"/></linearGradient>
      <radialGradient id="iconbg"><stop stop-color="#e1f4ff"/><stop offset="1" stop-color="#bfebfc"/></radialGradient>
      <linearGradient id="teal"><stop stop-color="#00c6b2"/><stop offset="1" stop-color="#007f78"/></linearGradient>
      <marker id="queryhead" viewBox="0 0 12 12" refX="10" refY="6" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M1 1L11 6L1 11Z" fill="#008aff"/></marker>
    </defs>'''


def embedded_image(path, x, y, w, h, aspect="xMidYMid meet"):
    data = base64.b64encode(path.read_bytes()).decode("ascii")
    return f'<image x="{x}" y="{y}" width="{w}" height="{h}" preserveAspectRatio="{aspect}" href="data:image/png;base64,{data}"/>'


def layer_group(y, width, height):
    return rect(7, y, width-14, height, 32, "#f2fbff", CYAN, 3)


def large_layer(x,y,w,h,name,level,description,kind, caption_size=30):
    return (card(x,y,w,h) + icon(kind,x+112,y+h/2,138) +
            text(x+210,y+76,name,56,True,fill=NAVY) + badge(x+211,y+96,level) +
            text(x+320,y+129,description,caption_size,width=w-345))


def layers(lang):
    l = LABELS[lang]
    parts = [layer_group(568,1284,215)]
    parts += [up_arrow(642,304,175), up_arrow(642,568,471), up_arrow(642,860,783)]
    parts += [large_layer(243,4,798,168,"ADIB","L4",l["layer"]["adib"],"browser",28),
              large_layer(243,305,798,166,"ADI","L3",l["layer"]["adi"],"code",29),
              large_layer(243,861,798,155,"UCS","L1",l["layer"]["ucs"],"ucs",29)]
    parts += [pill(520,213,244,58,l["engine"]+" L3–L4",27),
              pill(510,494,264,55,l["engine"]+" L2–L3",27),
              pill(510,801,264,55,l["engine"]+" L1–L2",27)]
    parts += [text(642,600,"ADMV · L2",30,True,"middle",NAVY)]
    for x,name,kind,label in [(22,"ADPM","model",l["layer"]["adpm"]),(656,"ADVS","test",l["layer"]["advs"])]:
        parts += [card(x,617,606,148,28),icon(kind,x+90,691,130),
                  text(x+179,677,name,48,True,fill=NAVY),text(x+179,728,label,29,width=405)]
    return 1284,1020,''.join(parts)


def chips(values, start, y, widths, gap=14):
    s=[]; centers=[]; x=start
    for val,w in zip(values,widths):
        s += [rect(x,y,w,44,13,"#d9f2ff","#7ccfff",1.5),text(x+w/2,y+29,val,20,True,"middle",BLUE,w-17)]
        centers.append(x+w/2); x+=w+gap
    s += [f'<path d="M{centers[0]},{y+50}V{y+61}H{centers[-1]}V{y+50} M{centers[1]},{y+50}V{y+61}" fill="none" stroke="#75caff" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>']
    for c in centers:
        s += [f'<circle cx="{c}" cy="{y+48}" r="5" fill="#0078ff" stroke="#92dfff" stroke-width="1.5"/>']
    return ''.join(s)


def case_map(lang):
    l=LABELS[lang]["map"]
    parts=[layer_group(597,1427,218)]
    parts += [up_arrow(714,292,176,True),up_arrow(714,597,468),up_arrow(360,898,792),up_arrow(1066,898,792)]
    parts += [large_layer(265,4,897,172,"ADIB","L4",l["adib"],"browser",29),
              large_layer(265,294,897,172,"ADI","L3",l["adi"],"code",29),
              large_layer(282,900,866,154,"UCS","L1",l["ucs"],"ucs",29)]
    parts += [chips(l["boundaries"],725,35,[130,119,128]),chips(l["implementations"],785,329,[112,112,112])]
    parts += [pill(574,212,280,56,l["many"],29),rect(870,212,548,56,27,"url(#panel)","#7bd5ff",2)]
    for i,line in enumerate(l["many_note"]):
        parts += [text(1144,235+i*22,line,20,anchor="middle",width=524)]
    parts += [pill(574,492,280,56,l["pair"],28), pill(417,550,594,48,l["pair_note"],21,False)]
    parts += [text(714,628,"ADMV · L2",30,True,"middle",NAVY)]
    for x,name,kind,desc,small in [(21,"ADPM","model",l["adpm"],l["model_uc"]),(730,"ADVS","test",l["advs"],l["behavioral_test"])]:
        parts += [card(x,645,675,147,29),icon(kind,x+90,718,130),text(x+174,700,name,49,True,fill=NAVY),text(x+174,753,desc,29,width=480),rect(x+449,662,210,40,13,"#d2efff","#79ccff",1.5),text(x+554,689,small,20,True,"middle",BLUE,194)]
    parts += [pill(251,831,218,55,l["bijection"],28),pill(957,831,218,55,l["bijection"],28),rect(960,955,153,45,14,"#cef0ff","#75cdff",1.5),text(1036.5,986,l["uc"],25,True,"middle",BLUE)]
    return 1427,1058,''.join(parts)


def banner(lang):
    b=LABELS[lang]["banner"]
    parts=['<clipPath id="bannerclip"><rect width="1766" height="776" rx="58"/></clipPath><g clip-path="url(#bannerclip)">',
           embedded_image(HERE/"banner-background.png",0,0,1766,776,"none"),
           embedded_image(ASSETS/"oal-mark.png",112,99,354,324),
           text(284,523,"OAL",130,True,"middle",NAVY),text(284,574,"Open Analysis Layers",40,anchor="middle",fill="#5c6c9f",width=442),
           '<path d="M62 600H506" stroke="#33a7ff" stroke-width="1.5"/>',text(282,647,b["tagline"],24,anchor="middle",fill="#5b6fa6",width=480)]
    for i,line in enumerate(b["reference"]):
        parts += [text(1140,94+i*25,line,22,anchor="middle",fill="#006eff",width=900)]
    parts += ['<path d="M1593 195V170Q1593 136 1559 136H720Q686 136 686 170V191" fill="none" stroke="#087bff" stroke-width="2.5" stroke-dasharray="14 9" marker-end="url(#queryhead)"/>']
    cards=[(550,"UCS · L1","ucs","ucs"),(852,"ADMV · L2","model","admv"),(1155,"ADI · L3","code","adi"),(1459,"ADIB · L4","external","adib")]
    for x,title,kind,key in cards:
        parts += [rect(x,198,266,290,23,"url(#panel)","#50c8ef" if key in ("admv","adib") else "#68b9ff",1.4),icon(kind,x+133,284,133),text(x+133,383,title,31,True,"middle",NAVY,width=243)]
        lines=b[key]
        if key=="admv":
            for i,line in enumerate(lines):
                parts += [text(x+133,418+i*25,line,23 if i==0 else 22,i==0,"middle",MUTED,width=244)]
        else:
            for i,line in enumerate(lines):
                parts += [text(x+133,432+i*29,line,24,anchor="middle",fill=MUTED,width=244)]
    for x in (815,1118,1421): parts += [right_arrow(x,343)]
    parts += ['<path d="M786 507V522H1188V507" fill="none" stroke="#5268b3" stroke-width="1.4"/>']
    for i,line in enumerate(b["parallel"]):
        parts += [text(987,548+i*25,line,21,anchor="middle",fill=MUTED,width=650)]
    widths=[269,265,321,297]; starts=[545,827,1105,1438]
    for x,w,label,kind in zip(starts,widths,b["benefits"],["target","ucs","shield","people"]):
        parts += [rect(x,608,w,81,40,"#f4fbff","none",0),icon(kind,x+43,648,70),text(x+85,657,label,20,True,fill=NAVY,width=w-99)]
    parts += ['</g>']
    return 1766,776,''.join(parts)


def write_asset(kind,lang,builder):
    w,h,body=builder(lang)
    title=f'OAL Alpha-v0.2.0-Alkimim — {kind} — {LABELS[lang]["language"]}'
    svg=(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title">'
         f'<title id="title">{html.escape(title)}</title>'+defs()+body+'</svg>')
    name=f'oal-{kind}-{lang}'
    (HERE/f'{name}.svg').write_text(svg,encoding="utf-8")
    cairosvg.svg2png(bytestring=svg.encode("utf-8"),write_to=str(ASSETS/f'{name}.png'),output_width=w,output_height=h)
    print(f'{name}: {w}×{h}')


if __name__ == "__main__":
    for language in LABELS:
        for kind,draw in [("banner",banner),("layers",layers),("map",case_map)]:
            write_asset(kind,language,draw)
