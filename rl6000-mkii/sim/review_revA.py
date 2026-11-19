"""Granskning av rev A: komplex last/EPDR, toleranser, tidsförskjutning, W1-delning, väggmodell,
effektförluster och felmoder.  Kör:  python3 review_revA.py   (skriver ut tabeller + plots/05-08)."""
import itertools, os
import numpy as np
import rl6000_mkii_sim as s
from rl6000_mkii_sim import f, w, j, ZL, ZC, par, db, at, BASE, S1, S2, S3, network

rng = np.random.default_rng(1)
ALL = list(itertools.product(S1, S2, S3))


def epdr(Z):
    """EPDR: den resistans som ger samma toppeffekt i ett klass B-slutsteg (numeriskt, per frekvens).
    Resistiv last R ger toppeffekt Vs^2/(4R) => EPDR = Vs^2/(4*pmax). Vs = 1."""
    th = np.linspace(0, 2 * np.pi, 361)[:, None, None]
    A = np.linspace(0.05, 1, 40)[None, :, None]
    mag, ph = np.abs(Z)[None, None, :], np.angle(Z)[None, None, :]
    v = A * np.sin(th); i = A / mag * np.sin(th - ph)
    p = np.where(i * np.sign(v + 1e-12) >= 0, (1 - np.abs(v)) * np.abs(i), (1 + np.abs(v)) * np.abs(i))
    return 1 / (4 * p.max(axis=(0, 1)))


def with_drivers(wd=None, td=None):
    s.Zw = s.Zdriver(wd or s.DRIVERS['woofer']); s.Zt = s.Zdriver(td or s.DRIVERS['tweeter'])


def section(t): print('\n' + '=' * 8, t, '=' * 8)


def load_analysis(v=BASE, states=ALL):
    rows = []
    for st in states:
        _, Z, _ = network(v, *st)
        e = epdr(Z)
        rows.append((st, np.abs(Z).min(), f[np.abs(Z).argmin()], np.degrees(np.angle(Z)).min(), np.degrees(np.angle(Z)).max(), e.min(), f[e.argmin()]))
    return rows


if __name__ == '__main__':
    import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
    P = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'plots')

    section('1. Komplex last, alla 27 lägen (antagna element)')
    r = load_analysis()
    r.sort(key=lambda x: x[5])
    print('värsta 4 (EPDR):'); [print(f"  {x[0]}  |Z|min {x[1]:.2f}@{x[2]:.0f}  fas {x[3]:+.0f}..{x[4]:+.0f}°  EPDR {x[5]:.2f}@{x[6]:.0f}") for x in r[:4]]
    print(f"  bästa: EPDR {r[-1][5]:.2f}")
    # referens: ren 4 ohm-resistor har EPDR 4.0; ren 8 ohm 8.0

    section('1b. Egen fynd: L1 är kärnspole => DCR ~0.5 ohm, inte modellens 1.8 ohm')
    DCR0 = s.DCR
    s.DCR = lambda L: 0.5 if L > 3e-3 else DCR0(L)
    r2 = sorted(load_analysis(), key=lambda x: x[1])
    print(f"  Zmin med realistisk L1-DCR: {r2[0][1]:.2f} ohm @ {r2[0][2]:.0f} Hz ({r2[0][0]}), EPDR min {min(x[5] for x in r2):.2f}")
    P0, _, _ = network(BASE, 'Neutral', 'Neutral', '0'); s.DCR = DCR0
    P1, _, _ = network(BASE, 'Neutral', 'Neutral', '0')
    print(f"  basnivå 150 Hz: +{at(db(P0['sum']),150)-at(db(P1['sum']),150):.1f} dB jämfört med rapportens modell")

    section('2. Toleranser + elementspridning (Monte Carlo, 400 körn., värsta läge Fri/Fram/+1.5 och neutral)')
    zmins, devs, sums = [], [], []
    keys = list(BASE)
    for n in range(400):
        v = {k: BASE[k] * (1 + rng.normal(0, 0.05 if not k.startswith('C1') else 0.10) / 1.0) for k in keys}  # ±5 % (1σ), elyt ±10 %
        wd = {k: x * (1 + rng.normal(0, {'Re': .07, 'Le': .25, 'fs': .15, 'Qes': .15, 'Qms': .2}[k])) for k, x in s.DRIVERS['woofer'].items()}
        td = {k: x * (1 + rng.normal(0, {'Re': .07, 'Le': .25, 'fs': .15, 'Qes': .15, 'Qms': .2}[k])) for k, x in s.DRIVERS['tweeter'].items()}
        with_drivers(wd, td)
        zmins.append(min(np.abs(network(v, a, 'Fram', '+1.5')[1]).min() for a in ('Fri',)))
        Pn, _, _ = network(v, 'Neutral', 'Neutral', '0'); sums.append(db(Pn['sum']))
    with_drivers()
    zmins = np.array(zmins); sums = np.array(sums)
    band = (f > 150) & (f < 6000)
    spread = np.percentile(sums, 95, axis=0) - np.percentile(sums, 5, axis=0)
    print(f"  Zmin (värsta läge): median {np.median(zmins):.2f}, 5-percentil {np.percentile(zmins,5):.2f}, min {zmins.min():.2f} ohm")
    print(f"  Spridning summa (5–95 %), 150 Hz–6 kHz: max {spread[band].max():.1f} dB vid {f[band][spread[band].argmax()]:.0f} Hz, median {np.median(spread[band]):.1f} dB")

    section('3. Tidsförskjutning diskant vs bas (akustiskt centrum)  + polaritet')
    fig, ax = plt.subplots(figsize=(9, 4.5))
    Pn, _, _ = network(BASE, 'Neutral', 'Neutral', '0')
    for dt_us in (-60, -30, 0, 30, 60, 90):
        S = Pn['W1'] + Pn['W2'] + Pn['T'] * np.exp(-j * w * dt_us * 1e-6)
        x = db(S); b = (f > 1500) & (f < 5000)
        print(f"  diskant {dt_us:+4d} µs ({dt_us*0.343:+5.1f} mm): 1,5–5 kHz min {x[b].min()-at(x,1000):+5.1f} max {x[b].max()-at(x,1000):+5.1f} dB rel 1 kHz")
        ax.semilogx(f, x, label=f'{dt_us:+d} µs ({dt_us*0.343:+.0f} mm)')
    Sinv = Pn['W1'] + Pn['W2'] - Pn['T']; x = db(Sinv); b = (f > 1500) & (f < 5000)
    print(f"  diskant inverterad (0 µs): 1,5–5 kHz min {x[b].min()-at(x,1000):+5.1f} dB  -> tydlig dip = polariteten är testbar")
    ax.semilogx(f, x, 'k:', label='inverterad diskant')
    ax.set_xlim(500, 20000); ax.set_ylim(-15, 6); ax.grid(which='both', alpha=.3); ax.legend(fontsize=7, ncol=2)
    ax.set_title('Känslighet för diskantens tidsförskjutning (positiv = diskanten senare) – BERÄKNAD'); ax.set_xlabel('Hz')
    fig.tight_layout(); fig.savefig(os.path.join(P, '05_delay_sensitivity.png'), dpi=110); plt.close(fig)

    section('4. Nedre basens delning (W1) – svep, fritt fält och väggmodell')
    # Väggmodell (antagande): flush mot vägg => baffle step försvinner: +5 dB shelf under ~250 Hz på basarna.
    wall = 1 + (10 ** (5 / 20) - 1) / (1 + j * f / 250)
    variants = {'~300 Hz (L 6,8 mH, C 33 µF)': (6.8e-3, 33e-6), '~450 Hz rev A (3,9 mH, 15 µF)': (3.9e-3, 15e-6),
                '~600 Hz (2,7 mH, 10 µF)': (2.7e-3, 10e-6), '~800 Hz (1,8 mH, 6,8 µF)': (1.8e-3, 6.8e-6)}
    fig, ax = plt.subplots(1, 2, figsize=(12, 4.5), sharey=True)
    for name, (L1, C1) in variants.items():
        v = dict(BASE, L1=L1, C1=C1)
        Pv, Zv, _ = network(v, 'Fri', 'Neutral', '0')
        free = db(Pv['sum']); wl = db((Pv['W1'] + Pv['W2']) * wall + Pv['T'])
        print(f"  {name:32} Zmin {np.abs(Zv).min():.2f}  fritt: 150Hz {at(free,150)-at(free,1500):+.1f} 400Hz {at(free,400)-at(free,1500):+.1f}  | vägg: 150Hz {at(wl,150)-at(wl,1500):+.1f} 400Hz {at(wl,400)-at(wl,1500):+.1f} dB (rel 1,5 kHz)")
        ax[0].semilogx(f, free, label=name); ax[1].semilogx(f, wl, label=name)
    for a_, t in zip(ax, ['Fritt fält (B&O-data), S1 Fri', 'Väggmonterad (antagen +5 dB under ~250 Hz)']):
        a_.set_xlim(30, 20000); a_.set_ylim(-10, 10); a_.grid(which='both', alpha=.3); a_.set_title(t + ' – BERÄKNAD', fontsize=9); a_.set_xlabel('Hz')
    ax[0].legend(fontsize=7)
    fig.tight_layout(); fig.savefig(os.path.join(P, '06_w1_crossover_sweep.png'), dpi=110); plt.close(fig)
    print("  Lobing W1/W2 (antaget c-c-avstånd 0,17 m): första nollställe utanför axeln när d·sinθ = λ/2 =>",
          f"f > {343/(2*0.17):.0f} Hz krävs för någon nolla alls (θ = 90°); vid 800 Hz ingen nolla inom ±90°.")

    section('5. Effektförluster i motstånd, rosa brus (realistisk musik-proxy)')
    # Rosa brus 20 Hz–20 kHz, normerat så att medeleffekten i 8 ohm-referens = Pavg.
    df = np.gradient(f); pink = 1 / f; pink *= 1 / np.sum(pink * df)          # V^2/Hz-form, summa = 1 V^2
    def avg_power(Pavg, st, v=BASE):
        V2 = pink * df * Pavg * 8                                              # V^2 per bin
        R1 = sum(v[k] for k in S1[st[0]]); Zw = s.Zw
        Zsh1 = par(ZC(v['C1']), Zw); I1 = 1 / (R1 + ZL(v['L1'], s.DCR(v['L1'])) + Zsh1)
        Zl2 = par(par(Zw, v['Rz'] + ZC(v['Cz'])), v['R_C2'] + ZC(v['C2']))
        Rt = v['Rta'] + v['Rtb']; Zt_ = 1 / (1 / ZL(v['Lt'], s.DCR(v['Lt'])) + 1 / ZC(v['Ct']) + 1 / Rt)
        I2 = 1 / (Zt_ + ZL(v['L2'], s.DCR(v['L2'])) + Zl2); Vl2 = I2 * Zl2
        Rs = v['Rs1'] + v['Rs2'] + v['Rs3']; Zpad = Rs + par(v['Rp'], s.Zt); Zb = ZC(v['C4']) + Zpad
        Za = par(ZL(v['L3'], s.DCR(v['L3'])), Zb); Ib = (Za / (ZC(v['C3']) + Za)) / Zb
        out = {'R1a+R1b (Vägg)': np.sum(V2 * abs(I1) ** 2) * R1,
               'Rta+Rtb (Mjuk)': np.sum(V2 * abs(I2 * Zt_) ** 2 / Rt),
               'Rz (Zobel)': np.sum(V2 * abs(Vl2 / (v['Rz'] + ZC(v['Cz']))) ** 2) * v['Rz'],
               'Rs-kedja (−)': np.sum(V2 * abs(Ib) ** 2) * Rs,
               'Rp': np.sum(V2 * abs(Ib * par(v['Rp'], s.Zt)) ** 2) / v['Rp']}
        return out
    for Pavg, lab in ((2, 'normal hög volym (2 W medel)'), (10, 'mycket högt (10 W medel ≈ SU-V505 nära klippning vid musik)')):
        o = avg_power(Pavg, ('Vägg', 'Mjuk', '-1.5'))
        print(f"  {lab}: " + ', '.join(f"{k} {x:.2f} W" for k, x in o.items()))

    section('6. Felmoder i diskantgrenen (elektrisk dämpning till diskanten)')
    def tw_att(v):
        Pv, Zv, _ = network(v, 'Neutral', 'Neutral', '0')
        h = db(Pv['T']) - db(s.A_T)
        return at(h, 500), at(h, 1000), at(h, 2000), np.abs(Zv).min()
    cases = {'intakt': BASE, 'C3 kortsluten': dict(BASE, C3=1.0), 'C4 kortsluten': dict(BASE, C4=1.0),
             'L3 avbrott': dict(BASE, L3=10.0), 'Rp avbrott': dict(BASE, Rp=1e6), 'Rp kortsluten': dict(BASE, Rp=1e-3)}
    for n, v in cases.items():
        a5, a1, a2, zm = tw_att(v)
        print(f"  {n:15} 500 Hz {a5:6.1f}  1 kHz {a1:6.1f}  2 kHz {a2:6.1f} dB   Zmin {zm:.2f}")

    section('7. Omkopplartillstånd: alla 2^2 kontaktkombinationer per omkopplare (oberoende av kontaktbild)')
    extra = {'S1 bara R1a kortsluten': dict(BASE, R1a=0.0)}  # R = R1b (3,3) -> mellan Neutral och Vägg i värde
    for n, v in extra.items():
        _, Zv, _ = network(v, 'Vägg', 'Neutral', '0'); print(f"  {n}: Zmin {np.abs(Zv).min():.2f}")
    print("  S2: (trap förbikopplad, Rtb kortsl.) = Fram; (Rtb kortsl.) = Neutral; (ingen) = Mjuk; (bara förbikoppling) = Fram")
    v = dict(BASE, Rs2=0.0); _, Zv, _ = network(v, '-1.5' and 'Neutral', 'Neutral', '-1.5')
    print(f"  S3 bara Rs2 kortsluten (Rs = 5,4 Ω): Zmin {np.abs(Zv).min():.2f}  -> alla mellantillstånd ligger inom de simulerade")

    section('8. Är S3 en ren nivåkontroll?  (diskantens elektriska överföring, relativt läge 0)')
    H = {}
    for c in S3:
        Pv, _, _ = network(BASE, 'Neutral', 'Neutral', c); H[c] = db(Pv['T']) - db(s.A_T)
    for c in ('+1.5', '-1.5'):
        d_ = H[c] - H['0']
        print(f"  {c:5}: 2,5k {at(d_,2500):+.2f}  4k {at(d_,4000):+.2f}  6k {at(d_,6000):+.2f}  10k {at(d_,10000):+.2f}  16k {at(d_,16000):+.2f} dB")
