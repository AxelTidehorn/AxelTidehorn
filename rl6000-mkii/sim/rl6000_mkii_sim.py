"""RL6000 MkII – simuleringsmodell för passivt delningsfilter.

Akustik: B&O:s egna elementmätningar (BeoCreate, MIT), magnitud extraherad ur vektor-PDF,
fas rekonstruerad som minimumfas. Akustiska centrumförskjutningar ignoreras (B&O:s DSP-
preset använder ingen fördröjning, vilket tyder på att felet är litet – men det är ett antagande).

Elektrik: elementens IMPEDANS är ANTAGEN (ingen publicerad data). Värdena i DRIVERS ska
ersättas med uppmätta värden innan komponenter köps. Kör:  python3 rl6000_mkii_sim.py
"""
import json, os, itertools
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, '..', 'data', 'beocreate_rl6000_curves.json')
PLOTS = os.path.join(HERE, '..', 'plots')

f = np.logspace(np.log10(20), np.log10(20000), 600)
w = 2 * np.pi * f
j = 1j

# ---------- ANTAGNA elementparametrar (ersätt med mätdata) ----------
DRIVERS = {
    # 13 cm bas/mellan, antaget 8 ohm nominellt (Re 6.0). Box/port-resonans förenklad till en topp.
    'woofer':  dict(Re=6.0, Le=0.45e-3, fs=60.0, Qes=0.60, Qms=4.0),
    # 25 mm dome, antaget 8 ohm nominellt (Re 5.8), fs 1.3 kHz.
    'tweeter': dict(Re=5.8, Le=0.04e-3, fs=1300.0, Qes=1.2, Qms=1.6),
}


def Zdriver(p):
    # Re + jwLe + parallell RLC-motsvarighet för resonansen
    Rmot = p['Re'] * p['Qms'] / p['Qes']
    ws = 2 * np.pi * p['fs']
    Lmot = p['Re'] / (p['Qes'] * ws)
    Cmot = p['Qes'] / (p['Re'] * ws)
    Ymot = 1 / Rmot + 1 / (j * w * Lmot) + j * w * Cmot
    return p['Re'] + j * w * p['Le'] + 1 / Ymot


ZL = lambda L, R=0.0: R + j * w * L          # spole med DCR
ZC = lambda C: 1 / (j * w * C)
par = lambda a, b: a * b / (a + b)


def minphase(fd, db):
    """Minimumfas ur magnitud via kepstrum."""
    N = 1 << 16; fs = 96000
    fl = np.linspace(0, fs / 2, N // 2 + 1)
    lf = np.log10(np.maximum(fl, 1))
    x = np.log10(fd)
    m = np.interp(lf, x, db)
    # extrapolering: under data -40 dB/dek, över data konstant
    lo = lf < x[0]
    m[lo] = db[0] - 40 * (x[0] - lf[lo])
    mag = 10 ** (np.maximum(m, -160) / 20)
    c = np.fft.irfft(np.log(mag), N)
    c[1:N // 2] *= 2; c[N // 2 + 1:] = 0
    H = np.exp(np.fft.rfft(c, N))
    return np.interp(f, fl, H.real) + j * np.interp(f, fl, H.imag)


d = json.load(open(DATA))['drivers']
A_W = minphase(np.array(d['upper_woofer']['f']), np.array(d['upper_woofer']['db']))
A_T = minphase(np.array(d['tweeter']['f']), np.array(d['tweeter']['db']))
Zw = Zdriver(DRIVERS['woofer'])
Zt = Zdriver(DRIVERS['tweeter'])

# ---------- MkII-nät (preliminära värden) ----------
# Spolar: DCR enligt grov modell nedan. Alla värden PRELIMINÄRA tills elementimpedansen är uppmätt.
BASE = dict(
    # Nedre bas W1: 2:a ordn. LP (fast) + seriemotståndskedja R1a+R1b (S1 kortsluter steg)
    L1=3.9e-3, C1=15e-6, R1a=2.2, R1b=3.3,
    # Övre bas W2: 2:a ordn. LP + Zobel
    L2=0.82e-3, C2=8.2e-6, R_C2=1.0, Rz=6.8, Cz=8.2e-6,
    # Närvaro-trap i serie med W2: Lt || Ct || (Rta + Rtb)
    Lt=0.47e-3, Ct=10e-6, Rta=2.2, Rtb=3.3,
    # Diskant: 3:e ordn. HP C3 - L3 - C4, L-pad Rs-kedja (Rs1+Rs2+Rs3) + Rp
    C3=4.7e-6, L3=0.22e-3, C4=22e-6, Rs1=2.7, Rs2=1.8, Rs3=2.7, Rp=15.0,
)
DCR = lambda L: 0.25 + 400 * L   # grov DCR-modell [ohm] för 1.0 mm luftspole

# Omkopplarlägen: kortslutande stegkopplingar (öppnar aldrig en signalväg)
S1 = {'Fri': (), 'Neutral': ('R1a',), 'Vägg': ('R1a', 'R1b')}   # seriemotstånd före W1
S2 = {'Fram': 'bypass', 'Neutral': 'Rta', 'Mjuk': 'Rta+Rtb'}
S3 = {'+1.5': 1, '0': 2, '-1.5': 3}   # antal seriemotstånd i Rs-kedjan


def network(v, s1, s2, s3, invert_tweeter=False):
    # W1
    R1 = sum(v[k] for k in S1[s1])
    Zsh1 = par(ZC(v['C1']), Zw)
    Zin1 = R1 + ZL(v['L1'], DCR(v['L1'])) + Zsh1
    H1 = Zsh1 / Zin1
    # W2
    Zload2 = par(par(Zw, v['Rz'] + ZC(v['Cz'])), v['R_C2'] + ZC(v['C2']))
    if S2[s2] == 'bypass':
        Ztrap = 0
    else:
        R = v['Rta'] + (v['Rtb'] if S2[s2] == 'Rta+Rtb' else 0)
        Ztrap = 1 / (1 / ZL(v['Lt'], DCR(v['Lt'])) + 1 / ZC(v['Ct']) + 1 / R)
    Zin2 = Ztrap + ZL(v['L2'], DCR(v['L2'])) + Zload2
    H2 = Zload2 / Zin2
    # Tweeter
    Rs = sum([v['Rs1'], v['Rs2'], v['Rs3']][:S3[s3]])
    Zpad = Rs + par(v['Rp'], Zt)
    Zb = ZC(v['C4']) + Zpad
    Za = par(ZL(v['L3'], DCR(v['L3'])), Zb)
    Zin3 = ZC(v['C3']) + Za
    Ht = (Za / Zin3) * (Zpad / Zb) * (par(v['Rp'], Zt) / Zpad)
    Zin = 1 / (1 / Zin1 + 1 / Zin2 + 1 / Zin3)
    sign = -1 if invert_tweeter else 1
    P = dict(W1=H1 * A_W, W2=H2 * A_W, T=sign * Ht * A_T)
    P['sum'] = P['W1'] + P['W2'] + P['T']
    # Effekt i diskanten relativt 1 W vid ingången (8 ohm-ref, dvs 2.83 V)
    It = 2.83 * Ht / Zt  # ström genom tweetern vid 2.83 V in
    return P, Zin, It


def db(x): return 20 * np.log10(np.abs(x) + 1e-12)


def at(arr, ff): return float(np.interp(np.log10(ff), np.log10(f), arr))


def report(v=BASE):
    rows = []
    for a, b, c in itertools.product(S1, S2, S3):
        P, Zin, It = network(v, a, b, c)
        s = db(P['sum'])
        band = (f > 200) & (f < 10000)
        ref = at(s, 1000)
        rows.append(dict(S1=a, S2=b, S3=c, Zmin=float(np.abs(Zin).min()), fZmin=float(f[np.abs(Zin).argmin()]),
                         lowmid=at(s, 250) - ref, pres=at(s, 2000) - ref, treb=np.mean([at(s, x) for x in (4000, 6000, 10000)]) - ref,
                         dev=float(s[band].max() - s[band].min()),
                         Pt_1k=float((np.abs(It) ** 2 * DRIVERS['tweeter']['Re'])[np.argmin(abs(f - 1000))]),
                         Pt_500=float((np.abs(It) ** 2 * DRIVERS['tweeter']['Re'])[np.argmin(abs(f - 500))])))
    return rows


def plots(v=BASE):
    import matplotlib; matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    os.makedirs(PLOTS, exist_ok=True)
    # 1: neutral, alla grenar + impedans
    P, Zin, _ = network(v, 'Neutral', 'Neutral', '0')
    fig, ax = plt.subplots(2, 1, figsize=(9, 8), sharex=True)
    for k, cl in [('W1', 'tab:red'), ('W2', 'tab:blue'), ('T', 'tab:green'), ('sum', 'k')]:
        ax[0].semilogx(f, db(P[k]), color=cl, label={'W1': 'Nedre bas (W1)', 'W2': 'Övre bas (W2)', 'T': 'Diskant', 'sum': 'Summa'}[k])
    R = json.load(open(DATA))['results']['total']
    ax[0].semilogx(R['f'], R['db'], color='orange', ls='--', lw=1, label='B&O BeoCreate DSP (referens)')
    ax[0].set_ylim(-30, 10); ax[0].set_ylabel('dB (rel. B&O-mätning)'); ax[0].grid(which='both', alpha=.3); ax[0].legend(fontsize=8)
    ax[0].set_title('MkII neutralläge – BERÄKNAD (elementdata B&O, impedans antagen)')
    ax[1].semilogx(f, np.abs(Zin), 'k'); ax[1].set_ylabel('|Z| [ohm]'); ax[1].set_ylim(0, 20); ax[1].grid(which='both', alpha=.3)
    ax[1].axhline(3.5, color='r', ls=':', lw=1); ax[1].set_xlabel('Hz'); ax[1].set_xlim(20, 20000)
    fig.tight_layout(); fig.savefig(os.path.join(PLOTS, '01_neutral.png'), dpi=110); plt.close(fig)
    # 2: varje omkopplare för sig
    fig, ax = plt.subplots(3, 1, figsize=(9, 10), sharex=True)
    for i, (S, name, key) in enumerate([(S1, 'S1 Bas/väggbalans', 0), (S2, 'S2 Närvaro', 1), (S3, 'S3 Diskantnivå', 2)]):
        for pos in S:
            args = ['Neutral', 'Neutral', '0']; args[key] = pos
            P, _, _ = network(v, *args)
            ax[i].semilogx(f, db(P['sum']), label=pos)
        ax[i].set_title(name + ' (övriga i neutralläge) – BERÄKNAD'); ax[i].set_ylim(-12, 6); ax[i].grid(which='both', alpha=.3); ax[i].legend(fontsize=8)
    ax[2].set_xlabel('Hz'); ax[2].set_xlim(20, 20000)
    fig.tight_layout(); fig.savefig(os.path.join(PLOTS, '02_switches.png'), dpi=110); plt.close(fig)
    # 3: impedans, värsta fall
    fig, ax = plt.subplots(figsize=(9, 4))
    for a, b, c in itertools.product(S1, S2, S3):
        _, Zin, _ = network(v, a, b, c)
        ax.semilogx(f, np.abs(Zin), lw=.7)
    ax.axhline(3.5, color='r', ls=':'); ax.set_ylim(0, 25); ax.grid(which='both', alpha=.3)
    ax.set_title('Inimpedans, alla 27 kombinationer (antagen elementimpedans)'); ax.set_xlabel('Hz'); ax.set_ylabel('ohm')
    fig.tight_layout(); fig.savefig(os.path.join(PLOTS, '03_impedance_all.png'), dpi=110); plt.close(fig)


if __name__ == '__main__':
    rows = report()
    print(f"{'S1':8}{'S2':8}{'S3':6}{'Zmin':>6}{'@Hz':>7}{'250Hz':>7}{'2kHz':>7}{'4-10k':>7}{'dev':>6}{'Pt@1k':>8}{'Pt@500':>8}")
    for r in rows:
        print(f"{r['S1']:8}{r['S2']:8}{r['S3']:6}{r['Zmin']:6.2f}{r['fZmin']:7.0f}{r['lowmid']:7.1f}{r['pres']:7.1f}{r['treb']:7.1f}{r['dev']:6.1f}{r['Pt_1k']*1000:7.1f}m{r['Pt_500']*1000:7.2f}m")
    zmin = min(r['Zmin'] for r in rows)
    assert zmin > 3.2, f'Zmin {zmin:.2f} ohm för lågt'
    plots()
    print('Zmin över alla lägen: %.2f ohm. Plottar i plots/.' % zmin)
