"""Analys inför rev B med fokus på ljudbild: elementdata från RL60.2 (troligen samma element i RL6000),
fasföljd vid delningen, lobing W2–diskant, spridning (kolvmodell), parmatchning L/R.
Kör:  python3 imaging_analysis.py   (skriver ut tabeller + plots/09–11).  Allt är BERÄKNAT."""
import itertools, os
import numpy as np
from scipy.special import j1
import rl6000_mkii_sim as s
import revB_candidate as rb
from rl6000_mkii_sim import f, w, j, db, at
from review_revA import epdr, with_drivers

P_ = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'plots')
c = 343.0

# Elementdata, RL60.2 (källor i rev B-PM). Qes ur datablad: 2π·fs·Mms·Re/Bl² = 1,07. Qms, Le: antagna.
W602 = dict(Re=7.2, Le=0.5e-3, fs=60.0, Qes=0.60, Qms=4.0)     # LPT 130/25/120 FG: Re uppmätt av säljare, övrigt antaget
T602 = dict(Re=4.6, Le=0.05e-3, fs=1500.0, Qes=1.07, Qms=1.5)  # Vifa D26TG-05-06 datablad (Qms, Le antagna)


def piston(a, theta):
    """Kolv i oändlig baffel: normerad tryckriktverkan."""
    x = 2 * np.pi * f / c * a * np.sin(theta)
    return np.where(x < 1e-6, 1.0, 2 * j1(x) / np.where(x < 1e-6, 1, x))


def section(t): print('\n' + '=' * 8, t, '=' * 8)


if __name__ == '__main__':
    import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
    ST = list(itertools.product(rb.S1B, rb.S2B, rb.S3B))

    section('1. Rev B med RL60.2-elementdata (i stället för antagna)')
    for name, (wd, td) in {'antagna (rev A/B-PM)': (None, None), 'RL60.2-data': (W602, T602)}.items():
        with_drivers(wd, td)
        zs = [rb.networkB(rb.B, *st)[1] for st in ST]
        P0, _ = rb.networkB(rb.B, 'Neutral', 'Neutral', '0'); x = db(P0['sum'])
        h = db(P0['T']) - db(s.A_T)
        print(f"  {name:22} Zmin {min(np.abs(z).min() for z in zs):.2f} Ω  EPDR {min(epdr(z).min() for z in zs):.2f} Ω  "
              f"diskant@1k {at(h,1000):.1f} dB  | neutral rel 1k: 3k {at(x,3000)-at(x,1000):+.1f} 5k {at(x,5000)-at(x,1000):+.1f} 10k {at(x,10000)-at(x,1000):+.1f}")
    # Fortsätt med RL60.2-data (bästa tillgängliga underlag)
    with_drivers(W602, T602)

    section('2. Fasföljd W2–diskant vid delningen (akustisk fasskillnad, 0° = perfekt följning)')
    band = (f > 1800) & (f < 3500)
    for st in [('Neutral', 'Neutral', '0'), ('Neutral', 'Fram', '0'), ('Neutral', 'Mjuk', '0'), ('Neutral', 'Neutral', '+'), ('Neutral', 'Neutral', '−')]:
        P, _ = rb.networkB(rb.B, *st)
        dphi = np.degrees(np.angle(P['W2'] / P['T']))[band]
        xo = f[np.argmin(np.abs(db(P['W2']) - db(P['T'])))]
        print(f"  {st[1]:7} {st[2]:2}: korsning {xo:5.0f} Hz, fasskillnad 1,8–3,5 kHz: {dphi.min():+5.0f}…{dphi.max():+5.0f}°")

    section('3. Lobing W2–diskant (antaget c-c-avstånd), summa i ±15°/±30° i planet där de sitter bredvid varandra')
    fig, ax = plt.subplots(figsize=(9, 4.5))
    P, _ = rb.networkB(rb.B, 'Neutral', 'Neutral', '0')
    for d in (0.10, 0.15):
        for ang in (-30, -15, 0, 15, 30):
            dt = d * np.sin(np.radians(ang)) / c
            S = P['W1'] + P['W2'] * np.exp(-j * w * dt) + P['T']  # W1 ignoreras i fasled (spelar under 500 Hz)
            x = db(S); b = (f > 1500) & (f < 5000)
            if d == 0.15: ax.semilogx(f, x, label=f'{ang:+d}°')
            print(f"  d={d:.2f} m {ang:+3d}°: 1,5–5 kHz min {x[b].min()-at(db(P['sum']),1000):+5.1f} dB")
    ax.set_xlim(500, 20000); ax.set_ylim(-15, 6); ax.grid(which='both', alpha=.3); ax.legend(fontsize=8)
    ax.set_title('Lobing W2–diskant, d = 0,15 m (antaget) – BERÄKNAD, RL60.2-elementdata'); ax.set_xlabel('Hz')
    fig.tight_layout(); fig.savefig(os.path.join(P_, '09_lobing.png'), dpi=110); plt.close(fig)

    section('4. Spridning (kolvmodell): bas a=52 mm, kalott a=13 mm. Respons utanför axeln rel. axeln')
    fig, ax = plt.subplots(figsize=(9, 4.5))
    on = db(P['sum'])
    for ang in (30, 45, 60):
        th = np.radians(ang)
        S = (P['W1'] + P['W2']) * piston(0.052, th) + P['T'] * piston(0.013, th)
        x = db(S) - on
        print(f"  {ang:2d}°: 1 kHz {at(x,1000):+5.1f}  2 kHz {at(x,2000):+5.1f}  2,5 kHz {at(x,2500):+5.1f}  3,5 kHz {at(x,3500):+5.1f}  6 kHz {at(x,6000):+5.1f}  10 kHz {at(x,10000):+5.1f}")
        ax.semilogx(f, x, label=f'{ang}° (rel. axeln)')
    ax.set_xlim(200, 20000); ax.set_ylim(-15, 5); ax.grid(which='both', alpha=.3); ax.legend(fontsize=8)
    ax.set_title('Spridning, kolvmodell (förenklad; vinklade fronter ej modellerade) – BERÄKNAD'); ax.set_xlabel('Hz')
    fig.tight_layout(); fig.savefig(os.path.join(P_, '10_directivity.png'), dpi=110); plt.close(fig)
    for fxo, a in ((2000, .052), (2500, .052), (3000, .052)):
        print(f"  bas vid {fxo} Hz: ka = {2*np.pi*fxo/c*a:.2f}  ({'riktverkan börjar' if 2*np.pi*fxo/c*a > 1 else 'nästan rundstrålande'})")

    section('5. Parmatchning: nivåskillnad vänster–höger (Monte Carlo 400 par), neutral')
    rng = np.random.default_rng(3)
    def one(tol):
        v = {k: (tuple(x * (1 + rng.normal(0, tol)) if x is not None else None for x in val) if isinstance(val, tuple)
                 else val * (1 + rng.normal(0, tol))) for k, val in rb.B.items()}
        return db(rb.networkB(v, 'Neutral', 'Neutral', '0')[0]['sum'])
    fig, ax = plt.subplots(figsize=(9, 4))
    for tol, lab in ((0.05 / 2, '±5 % (2σ) komponenter'), (0.02 / 2, '±2 % (2σ) – matchade'), (0.01 / 2, '±1 % (2σ) – uppmätta och parade')):
        diffs = np.array([one(tol) - one(tol) for _ in range(400)])
        p95 = np.percentile(np.abs(diffs), 95, axis=0); b = (f > 1000) & (f < 10000)
        print(f"  {lab:32}: 95-percentil |L−R| 1–10 kHz: max {p95[b].max():.2f} dB vid {f[b][p95[b].argmax()]:.0f} Hz, median {np.median(p95[b]):.2f} dB")
        ax.semilogx(f, p95, label=lab)
    ax.axhline(1.0, color='r', ls=':', lw=1); ax.set_xlim(100, 20000); ax.set_ylim(0, 2.5); ax.grid(which='both', alpha=.3); ax.legend(fontsize=8)
    ax.set_title('Nivåskillnad L/R från komponenttoleranser (95-percentil) – BERÄKNAD, element identiska'); ax.set_xlabel('Hz'); ax.set_ylabel('dB')
    fig.tight_layout(); fig.savefig(os.path.join(P_, '11_pair_matching.png'), dpi=110); plt.close(fig)

    section('6. Rev B mot B2 (fasoptimerad): fasföljd, delning, lobing d=0,15 m, Zmin')
    for name, v in (('B', rb.B), ('B2', rb.B2)):
        for s2 in rb.S2B:
            P, _ = rb.networkB(v, 'Neutral', s2, '0'); m = (f > 1000) & (f < 6000)
            dphi = np.degrees(np.angle(P['W2'] / P['T']))[band]; xo = f[m][np.argmin(np.abs(db(P['W2']) - db(P['T']))[m])]
            print(f"  {name:2} S2 {s2:7}: delning {xo:5.0f} Hz, fasskillnad {dphi.min():+4.0f}…{dphi.max():+4.0f}°")
        P, _ = rb.networkB(v, 'Neutral', 'Neutral', '0'); on = at(db(P['sum']), 1000); lob = []
        for ang in (-15, 15, -30, 30):
            x = db(P['W1'] + P['W2'] * np.exp(-j * w * 0.15 * np.sin(np.radians(ang)) / c) + P['T']); b = (f > 1500) & (f < 5000)
            lob.append(f"{ang:+d}°: {x[b].min()-on:+.1f}")
        zs = [rb.networkB(v, *st)[1] for st in ST]; h = db(P['T']) - db(s.A_T)
        print(f"  {name:2} lobing (min 1,5–5 kHz): {'  '.join(lob)} | Zmin {min(np.abs(z).min() for z in zs):.2f} Ω, EPDR {min(epdr(z).min() for z in zs):.2f} Ω, diskant@500 Hz {at(h,500):.1f} dB")
    with_drivers()
