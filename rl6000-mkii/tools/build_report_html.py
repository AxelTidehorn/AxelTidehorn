# Användning: python3 tools/build_report_html.py [README.md | granskning_revA.md]  -> _report.html
import markdown, pathlib, sys
R=pathlib.Path(__file__).resolve().parent.parent
SRC=sys.argv[1] if len(sys.argv)>1 else 'README.md'
md=(R/SRC).read_text()
import re
md=re.sub(r'(?m)^  (?=\S)', '    ', md)  # python-markdown kräver 4 blanksteg för nästling
md=re.sub(r'(?m)^(?!\s*(?:- |\d+\. |\|))(.+)\n(?=\s*(?:- |\d+\. ))', r'\1\n\n', md)
P=R/'plots'
fig=lambda n,c: f'\n<figure><img src="file://{P/n}"><figcaption>{c}</figcaption></figure>\n'
REVIEW_FIGS={'## Punkt 5':('05_delay_sensitivity.png','Figur R1. Känslighet för diskantens tidsförskjutning, rev A (BERÄKNAD).'),
 '## Punkt 7':('06_w1_crossover_sweep.png','Figur R2. Svep av nedre basens delning, fritt fält och väggmodell (BERÄKNAD).'),
 '## Punkt 9':('07_revB_switches.png','Figur R3. Rev B-kandidat: verkan av S1–S3 (BERÄKNAD, antagen impedans).'),
 '## Punkt 10':('08_revB_impedance_all.png','Figur R4. Rev B-kandidat: inimpedans i alla 27 lägen (antagen impedans).')}
SOUND_FIGS={'## 3. Svar på dina sex frågor':[('09_lobing.png','Figur L1. Lobing W2–diskant, rev B, d = 0,15 m antaget (BERÄKNAD).'),
   ('10_directivity.png','Figur L2. Spridning, kolvmodell (BERÄKNAD, vinklade fronter ej modellerade).'),
   ('11_pair_matching.png','Figur L3. Nivåskillnad vänster/höger från komponenttoleranser (BERÄKNAD).')]}
FIGS={'granskning_revA.md':{h:[x] for h,x in REVIEW_FIGS.items()}, 'ljudmal_revB.md':SOUND_FIGS}.get(SRC,{})
for h,lst in FIGS.items(): md=md.replace(h, ''.join(fig(n,c) for n,c in lst)+'\n'+h,1)
md=md.replace('### D6.', fig('01_neutral.png','Figur 1. MkII neutralläge – grenar, summa och impedans (BERÄKNAD; elementdata B&O, impedans antagen). Orange streckad: B&O BeoCreate DSP-resultat.')+fig('02_switches.png','Figur 2. Verkan av respektive omkopplare, övriga i neutralläge (BERÄKNAD).')+fig('03_impedance_all.png','Figur 3. Inimpedans i alla 27 lägeskombinationer (antagen elementimpedans). Röd linje 3,5 Ω.')+'\n### D6.',1)
body=markdown.markdown(md,extensions=['tables','fenced_code','sane_lists']).replace('src="plots/','src="file://'+str(P)+'/').replace('<p><img','<p style="text-align:center"><img style="width:100%"')
css='''@page{size:A4;margin:16mm 15mm 16mm 15mm}
body{font-family:"DejaVu Sans","Noto Color Emoji",sans-serif;font-size:9.6pt;line-height:1.42;color:#1d1d1f}
h1{font-size:20pt;margin:0 0 4px;border-bottom:3px solid #b3001b;padding-bottom:6px}
h2{font-size:14pt;margin:20px 0 6px;color:#b3001b;border-bottom:1px solid #ddd;padding-bottom:3px;break-after:avoid}
h3{font-size:11pt;margin:14px 0 4px;break-after:avoid}
table{border-collapse:collapse;width:100%;margin:6px 0 10px;font-size:8.4pt;break-inside:auto}
th,td{border:1px solid #ccc;padding:3px 5px;vertical-align:top;text-align:left}
th{background:#f2f2f4} tr{break-inside:avoid}
pre{background:#f7f7f9;border:1px solid #e3e3e6;padding:7px;font-size:7.1pt;line-height:1.25;white-space:pre;overflow:hidden;break-inside:avoid}
code{font-family:"DejaVu Sans Mono",monospace;font-size:0.92em}
figure{margin:10px 0;break-inside:avoid;text-align:center} figure img{width:88%} figcaption{font-size:8pt;color:#555}
a{color:#0b57d0;text-decoration:none} hr{border:0;border-top:1px solid #ddd;margin:14px 0}
blockquote{border-left:3px solid #ccc;margin:0;padding-left:10px;color:#444}'''
(R/'_report.html').write_text(f'<!doctype html><html lang="sv"><head><meta charset="utf-8"><title>RL6000 MkII</title><style>{css}</style></head><body>{body}</body></html>')
