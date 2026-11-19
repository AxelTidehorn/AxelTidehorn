"""Originalfiltren, båda VERIFIERADE mot B&O:s servicemanualer:
  RL60.2: Beovox RL60.2 service manual s. 1-15, filter 8039073.
  RL6000: Red Line service manual (RL1000/2000/6000/7000) s. 15-1, typ 6522, filter 8039097.

Akustik: B&O BeoCreate-elementdata (RL6000-element). Elementimpedans: RL60.2-data (imaging_analysis.W602/T602).
Kör:  python3 originals.py   -> tabeller, plots/12–13, spice/*.cir
"""
import itertools, os
import numpy as np
import rl6000_mkii_sim as s
import revB_candidate as rb
from rl6000_mkii_sim import f, j, ZL, ZC, par, db, at
from review_revA import epdr, with_drivers
from imaging_analysis import W602, T602

HERE = os.path.dirname(os.path.abspath(__file__))
# DCR (antaganden): 6,8 mH är separat spole (91L1), troligen kärnspole ~0,6 Ω; övriga luftspolar enligt s.DCR
DCR = lambda L: 0.6 if L > 5e-3 else s.DCR(L)

# RL60.2, filter 8039073 – avläst ur schemat (beteckningar som i manualen)
RL602 = dict(L1=6.8e-3, C1=22e-6, R6=6.8,                      # nedre bas: L1 serie, C1+R6 shunt
             L2=1.0e-3, C2=6.8e-6, L3=0.33e-3, R2=15.0, C3=10e-6,  # övre bas: L2–C2(shunt)–L3, R2+C3 över elementet
             C4=4.7e-6, L4=0.33e-3, C5=15e-6)                  # diskant: C4–L4(shunt)–C5, ingen nivåanpassning
# RL6000, filter 8039097 – avläst ur schemat s. 15-1 (egen topologi, se network_rl6000)
RL6000 = dict(L1=6.8e-3, C1=22e-6, R4=15.0,                    # nedre bas: L1 serie, C1+R4 shunt
              L2=0.68e-3, C5=5.6e-6, C2=15e-6, R3=15.0,         # övre bas: L2+C5 i serie (bandpass), C2+R3 shunt
              C3=5.6e-6, L4=0.33e-3, R2=3.9, C4=3.3e-6, R1=10.0)  # diskant: C3, L4 shunt, R2||C4 serie, R1 shunt


def network_rl6000(v, c5_shunt=True, tpol=-1):
    """c5_shunt=True: TOLKNING (C5 från L2/elementnoden till jord). False: som schemat är ritat (C5 i serie),
    vilket ger ett hål på ~13 dB vid 0,5–1,5 kHz och bedöms vara ett ritfel – verifieras på kortet.
    tpol=-1: diskanten inverterad (TROLIG: praxis för 2:a ordn. HP/LP; polaritet ej angiven i schemat)."""
    Zw, Zt = s.Zw, s.Zt
    Zsh1 = par(v['R4'] + ZC(v['C1']), Zw); Zin1 = ZL(v['L1'], DCR(v['L1'])) + Zsh1; H1 = Zsh1 / Zin1
    if c5_shunt:
        Zsh2 = par(par(Zw, v['R3'] + ZC(v['C2'])), ZC(v['C5'])); Zin2 = ZL(v['L2'], DCR(v['L2'])) + Zsh2
    else:
        Zsh2 = par(v['R3'] + ZC(v['C2']), Zw); Zin2 = ZL(v['L2'], DCR(v['L2'])) + ZC(v['C5']) + Zsh2
    H2 = Zsh2 / Zin2
    ZB = par(v['R1'], Zt); Zser = par(v['R2'], ZC(v['C4'])); Zb = Zser + ZB
    Za = par(ZL(v['L4'], DCR(v['L4'])), Zb); Zin3 = ZC(v['C3']) + Za
    Ht = tpol * (Za / Zin3) * (ZB / Zb)
    Zin = 1 / (1 / Zin1 + 1 / Zin2 + 1 / Zin3)
    P = dict(W1=H1 * s.A_W, W2=H2 * s.A_W, T=Ht * s.A_T); P['sum'] = P['W1'] + P['W2'] + P['T']
    return P, Zin


def network_orig(v):
    Zw, Zt = s.Zw, s.Zt
    Zsh1 = par(v['R6'] + ZC(v['C1']), Zw); Zin1 = ZL(v['L1'], DCR(v['L1'])) + Zsh1; H1 = Zsh1 / Zin1
    Zl2 = par(Zw, v['R2'] + ZC(v['C3']))
    Zb2 = ZL(v['L3'], DCR(v['L3'])) + Zl2
    Za2 = par(ZC(v['C2']), Zb2)
    Zin2 = ZL(v['L2'], DCR(v['L2'])) + Za2
    H2 = (Za2 / Zin2) * (Zl2 / Zb2)
    Zb3 = ZC(v['C5']) + Zt
    Za3 = par(ZL(v['L4'], DCR(v['L4'])), Zb3)
    Zin3 = ZC(v['C4']) + Za3
    Ht = (Za3 / Zin3) * (Zt / Zb3)
    Zin = 1 / (1 / Zin1 + 1 / Zin2 + 1 / Zin3)
    P = dict(W1=H1 * s.A_W, W2=H2 * s.A_W, T=Ht * s.A_T); P['sum'] = P['W1'] + P['W2'] + P['T']
    return P, Zin


def hybrid(v_orig, v_b, R1, s2='Neutral', s3='0'):
    """Hybrid: originalets nedre basgren (L1, C1+R6) + seriemotstånd R1 (S1), och B/B2:s övre bas + diskant."""
    Zw = s.Zw
    Zsh1 = par(v_orig.get('R4', v_orig.get('R6')) + ZC(v_orig['C1']), Zw); Zin1 = R1 + ZL(v_orig['L1'], DCR(v_orig['L1'])) + Zsh1; H1 = Zsh1 / Zin1
    P, Z23 = rb.networkB(dict(v_b, R1=(1e9, 1e9, 1e9)), 'Neutral', s2, s3)   # W1 bortkopplad i B-nätet
    P = dict(P, W1=H1 * s.A_W); P['sum'] = P['W1'] + P['W2'] + P['T']
    return P, 1 / (1 / Zin1 + 1 / Z23)


def spice_rl6000(v, path):
    L = ["* RL6000 filter 8039097 – genererad av originals.py. Element som Re+Le (förenklat, RL60.2-elementdata).",
         "Vin in 0 AC 2.83",
         f"L1 in n1 {v['L1']} Rser={DCR(v['L1']):.2f}", f"C1 n1 n1a {v['C1']}", f"R4 n1a 0 {v['R4']}", f"RW1 n1 n1w {W602['Re']}", f"LW1 n1w 0 {W602['Le']}",
         f"L2 in n2a {v['L2']} Rser={DCR(v['L2']):.2f}", f"C5 n2a n2 {v['C5']}", f"C2 n2 n2b {v['C2']}", f"R3 n2b 0 {v['R3']}", f"RW2 n2 n2w {W602['Re']}", f"LW2 n2w 0 {W602['Le']}",
         f"C3 in n3 {v['C3']}", f"L4 n3 0 {v['L4']} Rser={DCR(v['L4']):.2f}", f"R2 n3 n4 {v['R2']}", f"C4 n3 n4 {v['C4']}", f"R1 n4 0 {v['R1']}", f"RT n4 n4t {T602['Re']}", f"LT n4t 0 {T602['Le']}",
         ".ac dec 100 20 20k", ".end"]
    open(path, 'w').write('\n'.join(L) + '\n')


def spice(name, v, path):
    """SPICE-netlista (elementen som ideala Re+Le-laster; ersätt med egen elementmodell vid behov)."""
    L = [f"* {name} – genererad av originals.py. Noder: in, 0 (jord). Element som Re+Le (förenklat).",
         "Vin in 0 AC 2.83",
         f"L1 in n1 {v['L1']} Rser={DCR(v['L1']):.2f}", f"C1 n1 n1a {v['C1']}", f"R6 n1a 0 {v['R6']}",
         f"RW1 n1 n1w {W602['Re']}", f"LW1 n1w 0 {W602['Le']}",
         f"L2 in n2 {v['L2']} Rser={DCR(v['L2']):.2f}", f"C2 n2 0 {v['C2']}", f"L3 n2 n3 {v['L3']} Rser={DCR(v['L3']):.2f}",
         f"R2 n3 n3a {v['R2']}", f"C3 n3a 0 {v['C3']}", f"RW2 n3 n3w {W602['Re']}", f"LW2 n3w 0 {W602['Le']}",
         f"C4 in n4 {v['C4']}", f"L4 n4 0 {v['L4']} Rser={DCR(v['L4']):.2f}", f"C5 n4 n5 {v['C5']}",
         f"RT n5 n5t {T602['Re']}", f"LT n5t 0 {T602['Le']}",
         ".ac dec 100 20 20k", ".end"]
    open(path, 'w').write('\n'.join(L) + '\n')


if __name__ == '__main__':
    import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
    with_drivers(W602, T602)
    os.makedirs(os.path.join(HERE, 'spice'), exist_ok=True)
    spice('RL60.2 filter 8039073 (verifierat schema)', RL602, os.path.join(HERE, 'spice', 'rl602_8039073.cir'))
    spice_rl6000(RL6000, os.path.join(HERE, 'spice', 'rl6000_8039097.cir'))
    R = s.json.load(open(s.DATA))['results']['total']
    dsp = np.interp(np.log10(f), np.log10(R['f']), R['db'])
    band = (f > 1800) & (f < 3500); m = (f > 1000) & (f < 6000)
    cases = {'RL6000 original (C5 shunt, diskant inv.)': ('6000', RL6000), 'RL6000 som ritat (C5 serie)': ('6000s', RL6000), 'RL60.2 original (verifierat schema)': ('orig', RL602),
             'MkII rev B (neutral)': ('B', rb.B), 'MkII B2 (neutral)': ('B', rb.B2)}
    out = {}
    for name, (kind, v) in cases.items():
        P, Z = network_orig(v) if kind == 'orig' else network_rl6000(v) if kind == '6000' else network_rl6000(v, False) if kind == '6000s' else rb.networkB(v, 'Neutral', 'Neutral', '0')
        S = db(P['sum']); out[name] = (P, Z)
        lw = (f > 100) & (f < 3000); xo1 = f[lw][np.argmin(np.abs(db(P['W1']) - db(P['W2']) + 6)[lw])]  # W1 6 dB under W2
        xo2 = f[m][np.argmin(np.abs(db(P['W2']) - db(P['T']))[m])]
        dphi = np.degrees(np.angle(P['W2'] / P['T']))[band]
        h = db(P['T']) - db(s.A_T); lo = f < 1000
        print(f"\n{name}")
        print(f"  nedre bas −6 dB under övre vid {xo1:.0f} Hz, W2/diskant {xo2:.0f} Hz, fasskillnad W2–T 1,8–3,5 kHz {dphi.min():+.0f}…{dphi.max():+.0f}°")
        print("  summa rel 1 kHz: " + ' '.join(f"{x}:{at(S,x)-at(S,1000):+.1f}" for x in (100, 200, 400, 1500, 2000, 2500, 3000, 4000, 5000, 7000, 10000, 12500, 16000)))
        print(f"  diskant elektr. 500 Hz {at(h,500):.1f} / 1 kHz {at(h,1000):.1f} dB | Zmin <1k {np.abs(Z)[lo].min():.2f} Ω, >1k {np.abs(Z)[~lo].min():.2f} Ω | EPDR <1k {epdr(Z)[lo].min():.2f}, >1k {epdr(Z)[~lo].min():.2f} Ω")
    print("\nParmatchning L/R, RL6000-original (toleranser enligt komponentlistan) mot 5 % film:")
    rng = np.random.default_rng(7); bb = (f > 500) & (f < 10000)
    TOL = dict(C1=.10, C2=.05, C3=.05, C5=.05, C4=.025, R1=.025, R2=.05, R3=.05, R4=.05)  # 1σ = halva toleransen
    for lab, scale in (('original-toleranser', 1.0), ('5 % film / 5 % R', None)):
        d = []
        for _ in range(300):
            one = lambda: db(network_rl6000({k: x * (1 + rng.normal(0, (TOL.get(k, .025) if scale else .025))) for k, x in RL6000.items()})[0]['sum'])
            d.append(one() - one())
        p95 = np.percentile(np.abs(d), 95, axis=0)
        print(f"  {lab:20}: |L−R| 95-perc 0,5–10 kHz max {p95[bb].max():.2f} dB @ {f[bb][p95[bb].argmax()]:.0f} Hz, median {np.median(p95[bb]):.2f} dB")
    print("\nHybrid (originalets nedre basgren + B2): väggmodell, rel 1,5 kHz")
    wall = 1 + (10 ** (5 / 20) - 1) / (1 + j * f / 250)
    for R1 in (0.0, 2.2, 4.7, 10.0):
        P, Z = hybrid(RL6000, rb.B2, R1); wl = db((P['W1'] + P['W2']) * wall + P['T']); fr = db(P['sum'])
        zs = [hybrid(RL6000, rb.B2, R1, a, b)[1] for a in rb.S2B for b in rb.S3B]
        print(f"  R1 {R1:4.1f} Ω: fritt 150 Hz {at(fr,150)-at(fr,1500):+.1f} 400 Hz {at(fr,400)-at(fr,1500):+.1f} | vägg 150 Hz {at(wl,150)-at(wl,1500):+.1f} 400 Hz {at(wl,400)-at(wl,1500):+.1f} | Zmin {min(np.abs(z).min() for z in zs):.2f} Ω, EPDR<1k {min(epdr(z)[f<1000].min() for z in zs):.2f}")
    for R1 in (0.0, 2.2, 4.7, 10.0):   # jämför: B2 med egen W1 (3,9 mH)
        v = dict(rb.B2, R1=(R1, R1, R1)); P, Z = rb.networkB(v, 'Fri', 'Neutral', '0'); wl = db((P['W1'] + P['W2']) * wall + P['T'])
        print(f"  (B2 egen W1, R1 {R1:4.1f}): vägg 150 Hz {at(wl,150)-at(wl,1500):+.1f} 400 Hz {at(wl,400)-at(wl,1500):+.1f}")
    # Plots
    fig, ax = plt.subplots(2, 1, figsize=(9, 8), sharex=True)
    P, Z = out['RL6000 original (C5 shunt, diskant inv.)']
    for k, cl, lab in (('W1', 'tab:red', 'Nedre bas'), ('W2', 'tab:blue', 'Övre bas'), ('T', 'tab:green', 'Diskant'), ('sum', 'k', 'Summa')):
        ax[0].semilogx(f, db(P[k]), color=cl, label=lab)
    ax[0].semilogx(f, dsp, color='orange', ls='--', lw=1, label='B&O BeoCreate DSP (RL6000)')
    ax[0].set_ylim(-30, 12); ax[0].grid(which='both', alpha=.3); ax[0].legend(fontsize=8)
    ax[0].set_title('RL6000-original 8039097 (C5 som shunt, tolkning) – BERÄKNAD (B&O-elementdata, RL60.2-elementimpedans)', fontsize=9)
    ax[1].semilogx(f, np.abs(Z), 'k'); ax[1].set_ylim(0, 25); ax[1].grid(which='both', alpha=.3); ax[1].set_ylabel('|Z| [Ω]'); ax[1].set_xlabel('Hz'); ax[1].set_xlim(20, 20000)
    fig.tight_layout(); fig.savefig(os.path.join(HERE, '..', 'plots', '12_rl6000_original.png'), dpi=110); plt.close(fig)
    fig, ax = plt.subplots(figsize=(9, 4.5))
    for name, (P, Z) in out.items():
        ax.semilogx(f, db(P['sum']) - at(db(P['sum']), 1000), label=name)
    ax.semilogx(f, dsp - np.interp(3, np.log10(f), dsp), 'k:', lw=1, label='B&O DSP-mål')
    ax.set_xlim(50, 20000); ax.set_ylim(-12, 10); ax.grid(which='both', alpha=.3); ax.legend(fontsize=7)
    ax.set_title('Original mot MkII – summa på axeln, normerad vid 1 kHz – BERÄKNAD', fontsize=9); ax.set_xlabel('Hz')
    fig.tight_layout(); fig.savefig(os.path.join(HERE, '..', 'plots', '13_original_vs_mkii.png'), dpi=110); plt.close(fig)
    with_drivers()
