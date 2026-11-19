"""Ritar B&O RL60.2-filtret 8039073 enligt servicemanualen s. 1-15 (plots/14_schema_rl602.png/.svg)."""
import os, schemdraw, schemdraw.elements as elm
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'plots', '14_schema_rl602')

with schemdraw.Drawing(show=False) as d:
    d.config(unit=2.2, fontsize=10)
    d += elm.Dot(open=True).at((0, 0)).label('IN +', 'left')
    d += elm.Line().at((0, 0)).to((0, -11))
    # Nedre bas: L1 6,8 mH (separat spole 91L1), C1 22 µF + R6 6,8 Ω shunt
    d += elm.Inductor2(loops=3).at((0, 0)).right(3).label('L1 6,8 mH\n(separat spole 91L1)')
    d += (n1 := elm.Dot())
    d += elm.Capacitor().down(1.8).at(n1.center).label('C1\n22 µF', 'bottom', ofst=.2)
    d += elm.Resistor().down(1.8).label('R6\n6,8 Ω', 'bottom', ofst=.2); d += elm.Ground()
    d += elm.Line().at(n1.center).right(3); d += elm.Dot(open=True).label('Nedre bas 8480177', 'right')
    # Övre bas: L2 1 mH – C2 6,8 µF shunt – L3 0,33 mH, R2 15 Ω + C3 10 µF över elementet
    y = -5
    d += elm.Inductor2(loops=3).at((0, y)).right(3).label('L2 1 mH')
    d += (n2 := elm.Dot())
    d += elm.Capacitor().down(1.8).at(n2.center).label('C2\n6,8 µF', 'bottom', ofst=.2); d += elm.Ground()
    d += elm.Inductor2(loops=2).at(n2.center).right(2.6).label('L3 0,33 mH')
    d += (n3 := elm.Dot())
    d += elm.Resistor().down(1.8).at(n3.center).label('R2\n15 Ω', 'bottom', ofst=.2)
    d += elm.Capacitor().down(1.8).label('C3\n10 µF', 'bottom', ofst=.2); d += elm.Ground()
    d += elm.Line().at(n3.center).right(2); d += elm.Dot(open=True).label('Övre bas 8480177', 'right')
    # Diskant: C4 4,7 µF – L4 0,33 mH shunt – C5 15 µF
    y = -11
    d += elm.Capacitor().at((0, y)).right(3).label('C4 4,7 µF')
    d += (n4 := elm.Dot())
    d += elm.Inductor2(loops=2).down(2.2).at(n4.center).label('L4\n0,33 mH', 'bottom', ofst=.2); d += elm.Ground()
    d += elm.Capacitor().at(n4.center).right(3).label('C5 15 µF')
    d += elm.Dot(open=True).label('Diskant 8480200', 'right')
    d += elm.Label().at((5, -15)).label('Servicemanual Beovox RL60.2, s. 1-15, filter 8039073. Kondensatorer: bipolära elektrolyter 20 %, 23 V.\n'
                                        'Jordsymbol = gemensam retur (IN −). Alla element + mot filtret. Exemplar kan avvika (filterrevisioner).', fontsize=9, color='#333')
    d.save(OUT + '.svg'); d.save(OUT + '.png', dpi=150)

OUT2 = OUT.replace('14_schema_rl602', '15_schema_rl6000')
with schemdraw.Drawing(show=False) as d:
    d.config(unit=2.2, fontsize=10)
    d += elm.Dot(open=True).at((0, 0)).label('IN +', 'left')
    d += elm.Line().at((0, 0)).to((0, -11))
    d += elm.Inductor2(loops=3).at((0, 0)).right(3).label('L1 6,8 mH\n(separat spole 91L1)')
    d += (n1 := elm.Dot())
    d += elm.Capacitor().down(1.8).at(n1.center).label('C1\n22 µF', 'bottom', ofst=.2)
    d += elm.Resistor().down(1.8).label('R4\n15 Ω', 'bottom', ofst=.2); d += elm.Ground()
    d += elm.Line().at(n1.center).right(3); d += elm.Dot(open=True).label('Bas 8480211 (nedre)', 'right')
    y = -5
    d += elm.Inductor2(loops=3).at((0, y)).right(3).label('L2 0,68 mH')
    d += (n2 := elm.Dot())
    d += elm.Capacitor().down(1.8).at(n2.center).label('C5 5,6 µF\nSHUNT (tolkning;\nritad i serie)', 'bottom', ofst=.2, color='#b3001b'); d += elm.Ground()
    d += elm.Line().at(n2.center).right(3.6); d += (n3 := elm.Dot())
    d += elm.Capacitor().down(1.8).at(n3.center).label('C2\n15 µF', 'bottom', ofst=.2)
    d += elm.Resistor().down(1.8).label('R3\n15 Ω', 'bottom', ofst=.2); d += elm.Ground()
    d += elm.Line().at(n3.center).right(2.4); d += elm.Dot(open=True).label('Bas 8480211 (övre)', 'right')
    y = -11
    d += elm.Capacitor().at((0, y)).right(3).label('C3 5,6 µF')
    d += (n4 := elm.Dot())
    d += elm.Inductor2(loops=2).down(2.2).at(n4.center).label('L4\n0,33 mH', 'bottom', ofst=.2); d += elm.Ground()
    d += elm.Line().at(n4.center).right(.5)
    xa = n4.center[0] + .5
    d += elm.Line().at((xa, y)).to((xa, y + 1.1)); d += elm.Line().at((xa, y)).to((xa, y - 0.0))
    d += elm.Capacitor().at((xa, y + 1.1)).right(2.6).label('C4 3,3 µF (film 5 %)', fontsize=9)
    d += elm.Resistor().at((xa, y)).right(2.6).label('R2 3,9 Ω', 'bottom', fontsize=9)
    xb = xa + 2.6
    d += elm.Line().at((xb, y + 1.1)).to((xb, y)); d += (n5 := elm.Dot().at((xb, y)))
    d += elm.Resistor().down(2.2).at(n5.center).label('R1\n10 Ω', 'bottom', ofst=.2); d += elm.Ground()
    d += elm.Line().at(n5.center).right(2); d += elm.Dot(open=True).label('Diskant 8480209\n(polaritet ej angiven)', 'right')
    d += elm.Label().at((6, -15.2)).label('Red Line service manual, RL 6000 typ 6522, s. 15-1, filter 8039097. Elektrolyter: C1 20 % 23 V; C2, C3, C5 10 % 35 V. C4 5 % 100 V.\n'
                                         'Rött: C5 är i manualen ritad i serie med L2; som shunt (mot jord) ger kretsen en rimlig respons – verifieras på kortet.', fontsize=9, color='#333')
    d.save(OUT2 + '.svg'); d.save(OUT2 + '.png', dpi=150)
print('ok')
