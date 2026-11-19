"""Ritar MkII rev A-kopplingsschemat (plots/04_schema_revA.png/.svg). Värden = BASE i rl6000_mkii_sim.py."""
import os, schemdraw, schemdraw.elements as elm
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'plots', '04_schema_revA')

def bracket(d, x0, x1, y, text):
    # streckad markering av element som omkopplaren kortsluter
    d += elm.Line().at((x0, y)).to((x0, y + .6)).linestyle('--').color('#b3001b')
    d += elm.Line().at((x0, y + .6)).to((x1, y + .6)).linestyle('--').color('#b3001b').label(text, 'top', fontsize=9, color='#b3001b')
    d += elm.Line().at((x1, y + .6)).to((x1, y)).linestyle('--').color('#b3001b')

with schemdraw.Drawing(show=False) as d:
    d.config(unit=2.2, fontsize=10)
    d += elm.Dot(open=True).at((0, 0)).label('AMP +', 'left')
    d += elm.Line().at((0, 0)).to((0, -16))
    # --- W1 nedre bas ---
    d += elm.Line().at((0, 0)).right(.6)
    r1a = elm.Resistor().right().label('R1a\n2,2 Ω'); d += r1a
    r1b = elm.Resistor().right().label('R1b\n3,3 Ω'); d += r1b
    d += elm.Inductor2(loops=3).right().label('L1 3,9 mH\n(kärnspole)')
    d += (n1 := elm.Dot())
    d += elm.Capacitor().down().at(n1.center).label('C1\n15 µF', 'bottom', ofst=.2); d += elm.Ground()
    d += elm.Line().at(n1.center).right(3.2)
    d += elm.Dot(open=True).label('W1 + (nedre bas)', 'right')
    bracket(d, r1a.start[0], r1a.end[0] - .05, .9, 'S1: R1a'); bracket(d, r1b.start[0] + .05, r1b.end[0], .9, 'S1: R1b')
    # --- W2 övre bas ---
    y = -5.5
    d += elm.Line().at((0, y)).right(.6)
    xa = 0.6
    d += elm.Line().at((xa, y)).to((xa, y + 1.2)); d += elm.Line().at((xa, y)).to((xa, y - 1.2))
    d += elm.Inductor2(loops=2).at((xa, y + 1.2)).right(3).label('Lt 0,47 mH', fontsize=9)
    d += elm.Capacitor().at((xa, y)).right(3).label('Ct 10 µF', fontsize=9)
    d += elm.Resistor().at((xa, y - 1.2)).right(1.5).label('Rta 2,2', 'bottom', fontsize=9)
    rtb = elm.Resistor().right(1.5).label('Rtb 3,3', 'bottom', fontsize=9); d += rtb
    xb = xa + 3
    d += elm.Line().at((xb, y + 1.2)).to((xb, y - 1.2))
    bracket(d, xa - .15, xb + .15, y + 1.7, 'S2: förbikoppla hela trapen')
    d += elm.Line().at((xa + 1.5, y - 1.2)).to((xa + 1.5, y - 2.4)).linestyle('--').color('#b3001b')
    d += elm.Line().at((xa + 1.5, y - 2.4)).to((xb, y - 2.4)).linestyle('--').color('#b3001b').label('S2: Rtb', 'bottom', fontsize=9, color='#b3001b')
    d += elm.Line().at((xb, y - 2.4)).to((xb, y - 1.2)).linestyle('--').color('#b3001b')
    d += elm.Line().at((xb, y)).right(.6)
    d += elm.Inductor2(loops=3).right().label('L2 0,82 mH')
    d += (n2 := elm.Dot())
    d += elm.Capacitor().down(1.6).at(n2.center).label('C2\n8,2 µF', 'top', fontsize=9, ofst=.2)
    d += elm.Resistor().down(1.6).label('RC2\n1,0 Ω', 'top', fontsize=9, ofst=.2); d += elm.Ground()
    d += elm.Line().at(n2.center).right(1.6); d += (n3 := elm.Dot())
    d += elm.Resistor().down(1.6).at(n3.center).label('Rz\n6,8 Ω', 'bottom', fontsize=9, ofst=.2)
    d += elm.Capacitor().down(1.6).label('Cz\n8,2 µF', 'bottom', fontsize=9, ofst=.2); d += elm.Ground()
    d += elm.Line().at(n3.center).right(1.6)
    d += elm.Dot(open=True).label('W2 + (övre bas)', 'right')
    # --- Diskant ---
    y = -13
    d += elm.Line().at((0, y)).right(.6)
    d += elm.Capacitor().right().label('C3 4,7 µF\nMKP 250 V')
    d += (n4 := elm.Dot())
    d += elm.Inductor2(loops=2).down().at(n4.center).label('L3\n0,22 mH', 'bottom', ofst=.2); d += elm.Ground()
    d += elm.Capacitor().at(n4.center).right().label('C4 22 µF')
    d += elm.Resistor().right(1.8).label('Rs1\n2,7 Ω', fontsize=9)
    rs2 = elm.Resistor().right(1.8).label('Rs2\n1,8 Ω', fontsize=9); d += rs2
    rs3 = elm.Resistor().right(1.8).label('Rs3\n2,7 Ω', fontsize=9); d += rs3
    d += (n5 := elm.Dot())
    d += elm.Resistor().down().at(n5.center).label('Rp\n15 Ω', 'bottom', ofst=.2); d += elm.Ground()
    d += elm.Line().at(n5.center).right(1.5)
    d += elm.Dot(open=True).label('T + (diskant)', 'right')
    bracket(d, rs2.start[0], rs2.end[0] - .05, y + 1.0, 'S3: Rs2'); bracket(d, rs3.start[0] + .05, rs3.end[0], y + 1.0, 'S3: Rs3')
    d += elm.Label().at((6, y - 3.4)).label('HÖGPASS C3–L3–C4 ALLTID I KRETS – ingen omkopplare här', fontsize=9, color='#555')
    # retur
    d += elm.Dot(open=True).at((0, -17)).label('AMP −', 'left')
    d += elm.Line().at((0, -17)).right(1); d += elm.Ground()
    d += elm.Label().at((10, -17)).label('Jordsymbol = gemensam retur: AMP− och W1−, W2−, T−.   Streckat rött = element som omkopplaren kortsluter (se lägestabell D5).', fontsize=9, color='#333')
    d.save(OUT + '.svg'); d.save(OUT + '.png', dpi=160)
print('ok', OUT)
