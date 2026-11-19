"""Rev B-kandidat (PRELIMINÄR, antagna elementimpedanser). Återanvänder modell och data från rl6000_mkii_sim.

Ändringar mot rev A (motivering: granskning_revA.md):
  S1  bas/vägg: W1-seriemotstånd 1,0 / 3,3 / 10 Ω (större omfång; 1,0 Ω minimum håller Zmin uppe).
  S2  närvaro 3–5 kHz: SHUNT-notch över diskanten (Ln–Cn–Rn, ~3,4 kHz). Shunt förstärks av högpasset
      i stället för att kompenseras som serieelement gör. Fram = notch bortkopplad.
  S3  diskantnivå: konstantimpedans-L-pad (Rs-kedja + omkopplade shuntar) -> jämn nivå från ~3 kHz.
  Fast trap ~13 kHz (Lh||Ch||Rh) mot diskantens topp (B&O använder −4,8 dB @ 12,3 kHz).
  W2-trapen utgår.  Polyfuse Rf före C3 (skydd mot C3-genomslag).  L1 kärnspole: DCR 0,5 Ω.
Kör:  python3 revB_candidate.py
"""
import itertools, os
import numpy as np
import rl6000_mkii_sim as s
from rl6000_mkii_sim import f, j, ZL, ZC, par, db, at
from review_revA import epdr

DCRB = lambda L: 0.5 if L > 2e-3 else s.DCR(L)  # L1 kärnspole ~0,5 Ω, övriga som rev A
OPEN = None

B = dict(
    L1=3.9e-3, C1=15e-6, R1=(1.0, 3.3, 10.0),                  # S1: Fri / Neutral / Vägg
    L2=0.82e-3, C2=8.2e-6, R_C2=1.0, Rz=6.8, Cz=8.2e-6,
    Rf=0.15,                                                     # polyfuse, kall resistans
    C3=4.7e-6, L3=0.22e-3, C4=22e-6,
    Lh=0.10e-3, Ch=1.5e-6, Rh=4.7,                               # fast trap ~13 kHz
    Rs=(0.68, 1.5, 2.7), Rsh=(OPEN, 33.0, 15.0),                 # S3: + / 0 / −  (konstant-Z L-pad)
    Ln=0.47e-3, Cn=4.7e-6, Rn=(OPEN, 10.0, 3.3),                 # S2: Fram / Neutral / Mjuk
)
# B2: B optimerad för fasföljd W2–diskant (RL60.2-elementdata, se imaging_analysis.py avsnitt 6).
# Delning ~2,1 kHz, stabil i alla S2-lägen. Pris: Zmin ~3,2 Ω (vid ~6 kHz), diskanten närmare sin fs (1,5 kHz).
B2 = dict(B, L2=1.8e-3, C2=8.2e-6, R_C2=0.22, C3=5.6e-6, L3=0.18e-3, C4=12e-6, Ln=0.82e-3, Cn=1.5e-6, Rs=(1.0, 2.2, 3.9))
S1B = {'Fri': 0, 'Neutral': 1, 'Vägg': 2}
S2B = {'Fram': 0, 'Neutral': 1, 'Mjuk': 2}
S3B = {'+': 0, '0': 1, '−': 2}
P_ = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'plots')


def networkB(v, s1, s2, s3):
    Zw, Zt = s.Zw, s.Zt
    Zsh1 = par(ZC(v['C1']), Zw); Zin1 = v['R1'][S1B[s1]] + ZL(v['L1'], DCRB(v['L1'])) + Zsh1; H1 = Zsh1 / Zin1
    Zl2 = par(par(Zw, v['Rz'] + ZC(v['Cz'])), v['R_C2'] + ZC(v['C2'])); Zin2 = ZL(v['L2'], DCRB(v['L2'])) + Zl2; H2 = Zl2 / Zin2
    Zend = Zt
    if v['Rsh'][S3B[s3]] is not OPEN: Zend = par(Zend, v['Rsh'][S3B[s3]])
    if v['Rn'][S2B[s2]] is not OPEN: Zend = par(Zend, v['Rn'][S2B[s2]] + ZL(v['Ln'], DCRB(v['Ln'])) + ZC(v['Cn']))
    Zh = 1 / (1 / ZL(v['Lh'], DCRB(v['Lh'])) + 1 / ZC(v['Ch']) + 1 / v['Rh'])
    Zpad = Zh + v['Rs'][S3B[s3]] + Zend
    Zb = ZC(v['C4']) + Zpad
    Za = par(ZL(v['L3'], DCRB(v['L3'])), Zb)
    Zin3 = v['Rf'] + ZC(v['C3']) + Za
    Ht = (Za / Zin3) * (Zpad / Zb) * (Zend / Zpad)
    Zin = 1 / (1 / Zin1 + 1 / Zin2 + 1 / Zin3)
    P = dict(W1=H1 * s.A_W, W2=H2 * s.A_W, T=Ht * s.A_T); P['sum'] = P['W1'] + P['W2'] + P['T']
    return P, Zin


if __name__ == '__main__':
    import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
    wall = 1 + (10 ** (5 / 20) - 1) / (1 + j * f / 250)   # antagen väggförstärkning (se review_revA)
    rows = [(st, np.abs(Z).min(), epdr(Z).min()) for st in itertools.product(S1B, S2B, S3B) for Z in [networkB(B, *st)[1]]]
    zmin = min(r[1] for r in rows)
    print(f"Zmin alla 27: {zmin:.2f} Ω   EPDR min {min(r[2] for r in rows):.2f} Ω")
    P0, _ = networkB(B, 'Neutral', 'Neutral', '0'); ref = db(P0['sum'])
    print('Neutral (fritt fält) rel 1 kHz:', ' '.join(f"{x}:{at(ref,x)-at(ref,1000):+.1f}" for x in (100, 200, 400, 1500, 2500, 3500, 5000, 6500, 8000, 10000, 12500, 16000)))
    for name, idx, S in (('S1', 0, S1B), ('S2', 1, S2B), ('S3', 2, S3B)):
        for pos in S:
            st = ['Neutral', 'Neutral', '0']; st[idx] = pos
            P, _ = networkB(B, *st); d_ = db(P['sum']) - ref
            print(f"  {name} {pos:8}: " + ' '.join(f"{x}:{at(d_,x):+.1f}" for x in (100, 200, 500, 1000, 2000, 3000, 4000, 5000, 6500, 10000, 15000)))
    for pos in ('Fri', 'Vägg'):
        Pw, _ = networkB(B, pos, 'Neutral', '0'); wl = db((Pw['W1'] + Pw['W2']) * wall + Pw['T'])
        print(f"Väggmonterad (modell), S1 {pos}: 150 Hz {at(wl,150)-at(wl,1500):+.1f}  400 Hz {at(wl,400)-at(wl,1500):+.1f} dB rel 1,5 kHz")
    h = db(P0['T']) - db(s.A_T); print(f"Diskantdämpning: 500 Hz {at(h,500):.1f}  1 kHz {at(h,1000):.1f} dB")
    _, Zc = networkB(dict(B, C3=1.0), 'Neutral', 'Neutral', '0'); print(f"C3 kortsluten -> Zmin {np.abs(Zc).min():.2f} Ω (polyfuse Rf ska lösa ut)")
    assert zmin > 3.3 and at(h, 1000) < -28, 'rev B-kandidat utanför krav'

    fig, ax = plt.subplots(3, 1, figsize=(9, 10), sharex=True)
    for i, (name, S) in enumerate((('S1 Bas/vägg', S1B), ('S2 Närvaro (3–5 kHz)', S2B), ('S3 Diskantnivå (konstant-Z, från ~3 kHz)', S3B))):
        for pos in S:
            st = ['Neutral', 'Neutral', '0']; st[i] = pos
            P, _ = networkB(B, *st); ax[i].semilogx(f, db(P['sum']), label=pos)
        ax[i].set_title(name + ' – rev B-kandidat, BERÄKNAD (fritt fält, antagen impedans)', fontsize=9)
        ax[i].set_ylim(-12, 6); ax[i].grid(which='both', alpha=.3); ax[i].legend(fontsize=8)
    ax[2].set_xlim(20, 20000); ax[2].set_xlabel('Hz')
    fig.tight_layout(); fig.savefig(os.path.join(P_, '07_revB_switches.png'), dpi=110); plt.close(fig)
    fig, ax = plt.subplots(figsize=(9, 4))
    for st in itertools.product(S1B, S2B, S3B):
        ax.semilogx(f, np.abs(networkB(B, *st)[1]), lw=.7)
    ax.axhline(3.5, color='r', ls=':'); ax.set_ylim(0, 25); ax.set_xlim(20, 20000); ax.grid(which='both', alpha=.3)
    ax.set_title('Rev B-kandidat: inimpedans, alla 27 lägen (antagen elementimpedans)'); ax.set_xlabel('Hz'); ax.set_ylabel('ohm')
    fig.tight_layout(); fig.savefig(os.path.join(P_, '08_revB_impedance_all.png'), dpi=110); plt.close(fig)
