"""Hybrid MkII (rev B-kandidat H): B&O:s RL6000-topologi (filter 8039097, C5 tolkad som shunt) + justeringar.
  W1: original (L1 6,8 mH, C1 22 µF + R4 15 Ω) + S1 seriemotstånd (Fri/Neutral/Vägg).
  W2: original topologi (L2, C5 shunt, C2+R3 över elementet) – värden får optimeras för fasföljd.
  T : original topologi (C3, L4 shunt, R2||C4 i serie, R1 shunt) + polyfuse + fast trap ~13 kHz
      + S2 närvaronotch (shunt Ln–Cn–Rn) + S3 nivå (R2/R1 parvis, ungefär konstant impedans).
Kör: python3 hybrid_candidate.py [--opt]   (--opt kör optimeringen igen, annars används lagrade värden)
Allt BERÄKNAT med B&O-elementdata och RL60.2-elementimpedans (RL6000-elementens impedans okänd).
"""
import itertools, os, sys
import numpy as np
import rl6000_mkii_sim as s
from rl6000_mkii_sim import f, w, j, ZL, ZC, par, db, at
from review_revA import epdr, with_drivers
from imaging_analysis import W602, T602
import originals as o

DCR = o.DCR
H = dict(o.RL6000, R1s=(0.0, 3.3, 10.0),                     # S1: W1-seriemotstånd
         Rf=0.15, Lh=0.10e-3, Ch=1.5e-6, Rh=4.7,              # polyfuse + fast trap ~13 kHz
         Ln=0.47e-3, Cn=4.7e-6, Rn=(None, 10.0, 3.3),         # S2: Fram / Neutral / Mjuk
         R2s=(2.7, 3.9, 5.6), R1s_t=(15.0, 10.0, 6.8))        # S3: + / 0 / − (R2 serie, R1 shunt)
S1H = {'Fri': 0, 'Neutral': 1, 'Vägg': 2}; S2H = {'Fram': 0, 'Neutral': 1, 'Mjuk': 2}; S3H = {'+': 0, '0': 1, '−': 2}
TPOL = 1  # diskantens polaritet: OKÄND i RL6000-schemat; +1 = i fas


def network_h(v, s1='Neutral', s2='Neutral', s3='0', tpol=None):
    Zw, Zt = s.Zw, s.Zt
    Zsh1 = par(v['R4'] + ZC(v['C1']), Zw); Zin1 = v['R1s'][S1H[s1]] + ZL(v['L1'], DCR(v['L1'])) + Zsh1; H1 = Zsh1 / Zin1
    Zsh2 = par(par(Zw, v['R3'] + ZC(v['C2'])), ZC(v['C5'])); Zin2 = ZL(v['L2'], DCR(v['L2'])) + Zsh2; H2 = Zsh2 / Zin2
    ZB = par(v['R1s_t'][S3H[s3]], Zt)
    if v['Rn'][S2H[s2]] is not None: ZB = par(ZB, v['Rn'][S2H[s2]] + ZL(v['Ln'], DCR(v['Ln'])) + ZC(v['Cn']))
    Zh = 1 / (1 / ZL(v['Lh'], DCR(v['Lh'])) + 1 / ZC(v['Ch']) + 1 / v['Rh'])
    Zb = Zh + par(v['R2s'][S3H[s3]], ZC(v['C4'])) + ZB
    Za = par(ZL(v['L4'], DCR(v['L4'])), Zb); Zin3 = v['Rf'] + ZC(v['C3']) + Za
    Ht = (Za / Zin3) * (ZB / Zb)
    P = dict(W1=H1 * s.A_W, W2=H2 * s.A_W, T=(tpol or TPOL) * Ht * s.A_T); P['sum'] = P['W1'] + P['W2'] + P['T']
    return P, 1 / (1 / Zin1 + 1 / Zin2 + 1 / Zin3)


# Optimerade värden (python3 hybrid_candidate.py --opt), avrundade till E12 – PRELIMINÄRA.
# Ger fasföljd ca −15…+27° (original ca −94…−50° med inverterad diskant). Neutralläget ligger ~3–5 dB lågt
# vid 2,5–5 kHz och Zmin >1 kHz ~3,05 Ω: diskantdämpningen måste räknas om när RL6000-diskantens (8480209) impedans är mätt.
H_OPT = dict(H, L2=1.0e-3, C5=22e-6, C3=6.8e-6, L4=0.18e-3, C4=12e-6, Ln=0.18e-3, Cn=4.7e-6)

K = ['L2', 'C5', 'C3', 'L4', 'C4', 'Ln', 'Cn']
band = (f > 1800) & (f < 3500); flat = ((f > 300) & (f < 5800)) | ((f > 8500) & (f < 15000))


def cost(x, v0):
    v = dict(v0); v.update(dict(zip(K, np.exp(x)))); c = 0
    for s2 in S2H:
        P, Z = network_h(v, 'Neutral', s2, '0'); S = db(P['sum']); e = S[flat] - np.mean(S[flat]); wt = 1 if s2 == 'Neutral' else .3
        c += wt * (np.mean(e ** 2) + np.mean(np.degrees(np.angle(P['W2'] / P['T']))[band] ** 2) / 400)
        c += 30 * max(0, 3.4 - np.abs(Z).min()) ** 2
        h = db(P['T']) - db(s.A_T); c += .5 * max(0, at(h, 1000) + 28) ** 2 + .5 * max(0, at(h, 500) + 42) ** 2
    Pf, _ = network_h(v, 'Neutral', 'Fram', '0'); Pm, _ = network_h(v, 'Neutral', 'Mjuk', '0')
    c += 2 * max(0, 3 - (at(db(Pf['sum']), 4000) - at(db(Pm['sum']), 4000))) ** 2
    return c


def report(v, name):
    print(f"\n== {name}")
    for s2 in S2H:
        P, _ = network_h(v, 'Neutral', s2, '0'); S = db(P['sum']); m = (f > 1000) & (f < 6000)
        xo = f[m][np.argmin(np.abs(db(P['W2']) - db(P['T']))[m])]; d = np.degrees(np.angle(P['W2'] / P['T']))[band]
        print(f"  S2 {s2:7}: delning {xo:5.0f} Hz, fas {d.min():+4.0f}…{d.max():+4.0f}° | rel 1k: " + ' '.join(f"{x}:{at(S,x)-at(S,1000):+.1f}" for x in (200, 1500, 2500, 3000, 4000, 5000, 7000, 10000, 12500, 16000)))
    for s3 in ('+', '−'):
        P, _ = network_h(v, 'Neutral', 'Neutral', s3); P0, _ = network_h(v); d = db(P['sum']) - db(P0['sum'])
        print(f"  S3 {s3}: " + ' '.join(f"{x}:{at(d,x):+.1f}" for x in (2000, 3000, 5000, 10000, 15000)))
    zs = [network_h(v, a, b, c)[1] for a, b, c in itertools.product(S1H, S2H, S3H)]; lo = f < 1000
    P, _ = network_h(v); h = db(P['T']) - db(s.A_T)
    print(f"  Zmin <1k {min(np.abs(z)[lo].min() for z in zs):.2f} / >1k {min(np.abs(z)[~lo].min() for z in zs):.2f} Ω | EPDR <1k {min(epdr(z)[lo].min() for z in zs):.2f} / >1k {min(epdr(z)[~lo].min() for z in zs):.2f} Ω | diskant 500 Hz {at(h,500):.1f}, 1 kHz {at(h,1000):.1f} dB")


if __name__ == '__main__':
    from scipy.optimize import minimize
    with_drivers(W602, T602)
    report(H, 'Hybrid med originalvärden (bara tillägg)')
    if '--opt' in sys.argv:
        x0 = np.log([H[k] for k in K]); best = None
        for seed in range(3):
            xs = x0 + (np.random.default_rng(seed).normal(0, .2, len(K)) if seed else 0)
            r = minimize(cost, xs, args=(H,), method='Powell', options=dict(maxiter=3000, xtol=1e-3, ftol=1e-4))
            if best is None or r.fun < best.fun: best = r
        print('optimerat:', {k: float(np.exp(x)) for k, x in zip(K, best.x)})
    report(H_OPT, 'Hybrid optimerad (H_OPT)')
    with_drivers()
