# RL6000 MkII – justerbart passivt delningsfilter

**Förstudie och första konstruktionsförslag · rev A · 2026-11-19**

Status: preliminär konstruktion. Komponentvärdena är **beräknade**, inte verifierade. De får inte byggas in förrän elementens impedans är uppmätt (se avsnitt I).

| Symbol | Betydelse |
|---|---|
| ✅ | Verifierat ur primärkälla eller egen analys av primärdata |
| 🟡 | Rimlig slutsats eller tolkning, inte bekräftad |
| ❓ | Okänt, måste mätas eller kontrolleras |
| 🧮 | Beräknat eller simulerat i modell (`sim/rl6000_mkii_sim.py`) |

---

## Sammanfattning (läs detta först)

1. **Det bästa underlaget finns redan.** I B&O:s eget BeoCreate-repo (MIT-licens) finns **uppmätta frekvensgångar för RL6000:s tre element** och **B&O:s egen DSP-delning** för högtalaren. Jag har extraherat kurvorna numeriskt ur vektor-PDF:erna (`data/beocreate_rl6000_curves.json`). Med dem kan vi simulera den akustiska summan av ett passivt filter med rimlig träffsäkerhet. Det är betydligt bättre än att gissa.
2. **B&O:s egen "moderna" tolkning av RL6000 är en 2,5-vägare.** Nedre basen delas vid cirka 800 Hz, övre basen och diskanten vid cirka 2,5 kHz (LR4). Diskanten dämpas 4–6 dB och får en dip vid 12,3 kHz. Det säger mycket om vad elementen behöver ✅.
3. **Diskanten är elementets svaga punkt.** Den ligger 6–7 dB över basen, har en dip vid 6,5–7 kHz och en topp vid 12,5 kHz ✅. Det är sannolikt huvudorsaken till att högtalaren upplevs som både "lite tillbakadragen" och "lite oprecis" i toppen. Delningsfiltret kan forma nivå och övergång, men det kan inte laga dippen vid 6,5 kHz.
4. **Rekommendation: ny passiv 2,5-vägare med tre omkopplare** (bas/väggbalans, närvaro och diskantnivå). Varje omkopplare har tre lägen och verkar i ett eget frekvensband. Omkopplarna kortsluter bara seriekomponenter, så **ingen signalväg kan brytas och diskantens högpassfilter kan aldrig förbikopplas**. Simulerat neutralläge ligger inom ±2 dB mellan 100 Hz och 6 kHz och följer B&O:s DSP-mål mycket nära 🧮.
5. **Den kritiska okända faktorn är basdelarnas impedans.** Är de 8 Ω fungerar 2,5-vägaren (Zmin ≈ 3,6 Ω). Är de 4 Ω ger den cirka 2,5 Ω, och då väljer vi arkitektur B med baselementen i serie. **En multimetermätning av likströmsresistansen (Re) avgör det på fem minuter.**
6. **Rimlighet:** elektriskt mycket genomförbart. Komponenter för paret kostar cirka 1 500 kr i budgetutförande och cirka 2 200 kr i standardutförande. Det är över målet på 1 000 kr, se E för var pengarna går och vad som kan strykas. En akustisk förbättring jämfört med ett renoverat original är **sannolik men inte garanterad**, och den blir troligen måttlig snarare än dramatisk. Det största enskilda värdet ligger i att kunna anpassa bas och närvaro till väggmonteringen, vilket originalet inte kan.

---

## A. Teknisk nulägesanalys

### A1. Verifierat om RL6000

| Uppgift | Värde | Källa | Status |
|---|---|---|---|
| Typ | B&O Beovox RL 6000, typnr 6522, tillverkad 1991–1997 | [Beoworld](https://archived.beoworld.org/prod_details.asp?pid=652), [Beocentral](https://beocentral.com/beovoxrl6000) | ✅ |
| Element | 2 × 13 cm bas/mellan + 1 × 25 mm diskant | [beo.zone](https://beo.zone/en/beovox-rl-6000-passive-loudspeakers) | ✅ |
| Låda | Basreflex, cirka 19 liter netto | beo.zone | ✅ |
| Nominell impedans | 8 Ω (B&O-specifikation) | Beoworld | ✅ som spec. Verkligt minimum ❓ |
| Effekttålighet | 103 W "long-term max" | Beoworld | ✅ som spec. |
| Känslighet | 86 dB ±2 dB, 42 Hz–20 kHz | Andrahandsuppgift i annons (finn.no) | 🟡 |
| Elementen har separata ledare till filtret | Övre bas, nedre bas och diskant kopplas var för sig till förstärkaren | [BeoCreate RL6000-guide](https://github.com/bang-olufsen/create/tree/master/Guides) (= [HiFiBerry-PDF](https://www.hifiberry.com/wp-content/uploads/2018/05/rl6000-guide.pdf)), s. 16–18 | ✅ |
| Filterkortet sitter på skruvposter innanför bakstycket. Diskantens ledare är kort och behöver förlängas | – | samma guide, s. 9 och 16 | ✅ |
| Elementmätningar och DSP-delning | Se A3 | [bang-olufsen/create › Speakers/Beovox RL 6000](https://github.com/bang-olufsen/create/tree/master/Speakers/Beovox%20RL%206000) | ✅ |

### A2. Originalfiltret – vad vi vet och inte vet

**Inget originalschema hittades.** Varken B&O:s servicebibliotek, Beoworld eller Beocentral har ett publicerat schema för RL6000 (en Beoworld-tråd efterfrågar just det utan svar). Webbsidorna hos Beoworld, DK Soundparts och Hi-Fi News gick inte att hämta från den här miljön på grund av nätverkspolicyn, så den informationen bygger på sökresultat.

Vad som går att se på fotot av originalkortet i BeoCreate-guiden (s. 9) 🟡:
- två synliga luftspolar
- fem gula axiella kondensatorer (bipolära elektrolyter, B&O-typiskt)
- en rosa filmkondensator (MKT-typ)
- en grön komponent
- 3–4 keramiska eller trådlindade motstånd
- en liten glaskomponent i hörnet, möjligen en glödlampa eller PTC som diskantskydd (vanligt hos B&O, men inte bekräftat).

Tolkning 🟡: fem elektrolyter stämmer med de preliminära värdena 22 / 15 / 2 × 5,6 / 3,3 µF. Två spolar räcker inte för en "äkta" 2,5-vägare med separata lågpassfilter. Originalet är därför **troligen en tvåvägare där de två baselementen delar filter** (parallell- eller seriekopplade), möjligen med enkel BSC-kompensation. **Detta måste verifieras på kortet.**

DK Soundparts kit (CK-059, cirka 24 €, för ett par) består enligt sökresultatet av 100 V / 105 °C-kondensatorer, alltså elektrolyter som ersätter elektrolyter. Exakta värden listas inte på sidan ❓. Det räcker för referenstillstånd B. Det finns ingen anledning att uppgradera till dyra filmkondensatorer i originalet om syftet är en trogen referens.

### A3. B&O:s egna mätningar och DSP-delning (den viktigaste källan)

Repot innehåller `BeoVoxRL_DriverMeasurements.pdf`, `BeoVoxRL_Filters.pdf` och `BeoVoxRL_ResultingResponses.pdf`, plus filterkoefficienterna i `beovox-rl6000.json`. Jag har dekomponerat biquad-koefficienterna (Fs = 48 kHz) och extraherat kurvorna.

**Rå elementrespons (B&O-mätning, samma drivnivå, normerad):**

| Frekvens | Bas (per element) | Diskant | Kommentar |
|---|---|---|---|
| 100 Hz | −5,0 dB | – | baffle step och basreflex |
| 300–1000 Hz | −0,7…+1,6 | – | jämnt |
| 1,8 kHz | **+3,3** | +6,5 | topp hos basen |
| 2–4 kHz | +0,7…+1,4 | **+6…+7,4** | diskanten 6 dB "het" |
| 6,5 kHz | −2,6 | **−0,2** | **dip i diskanten**, cirka 7 dB under dess egen nivå |
| 12,5 kHz | −27 (brytning) | **+8,3** | **topp i diskanten** |

Observera: kurvorna för övre och nedre bas är identiska i datat. B&O har alltså använt samma mätning för båda ✅.

**B&O:s DSP-delning, dekomponerad ✅:**

| Kanal | Funktion |
|---|---|
| Nedre bas | −6 dB, LR4-lågpass **801 Hz** |
| Övre bas | Hyllfilter −6 dB under 801 Hz (bassumman blir rätt), LR4-lågpass **2 522 Hz** |
| Båda baselementen | +2,3 dB peak vid 193–209 Hz (Q 2,6), svag dip −1,1 dB vid 1,4 kHz, basförlängning cirka 28–34 Hz (Linkwitz-liknande) |
| Diskant | Högpass 2 522 Hz (2:a ordningen) + 2 × 2:a ordningen vid 801 Hz (skydd) + högpass-hylla. Total nivå −2 dB, **dip −4 dB vid 1,9 kHz**, **+3 dB vid 8,3 kHz** (fyller dippen), **notch −4,8 dB vid 12,3 kHz** (Q 2,3) |
| Fördröjning | 0 på alla kanaler, alltså ingen tidskorrigering mellan elementen |

Resultatet (B&O:s "Resulting responses") är rakt inom cirka ±2 dB från 80 Hz till 20 kHz.

**Slutsatser för passiv konstruktion ✅/🟡:**
- B&O valde **2,5-vägstopologi** när de var fria att välja. Elementen klarar alltså det.
- Delning vid cirka **2,5 kHz** med branta slänter (cirka 4:e ordningen akustiskt) är B&O:s val. Det ligger i nedre delen av området 3,5 kHz som nämnts tidigare 🟡. Det tidigare värdet kan gälla originalfiltrets elektriska brytfrekvens och behöver inte motsäga detta.
- Diskanten behöver **4–6 dB nivådämpning**. Den uppgiften löser ett L-pad passivt utan problem.
- Fördröjning noll i DSP:n tyder på att elementens akustiska centrum ligger tillräckligt nära varandra. Det förenklar passiv konstruktion 🟡.

### A4. Närliggande modell: RL60.2 (Hi-Fi News) – inte RL6000-data

Från [Hi-Fi News labbrapport](https://www.hifinews.com/content/bang-olufsen-beovox-red-line-602-loudspeaker-lab-report), via sökutdrag eftersom sidan inte gick att hämta härifrån:
- minimum 4,75–4,8 Ω vid 172 Hz trots 8 Ω-specifikation
- EPDR 2,3 Ω vid 124 Hz
- känslighet 90,4 dB (1 kHz) / 88,3 dB (IEC)
- axiell respons i stort sett rak **utom en notch på cirka 6 dB vid 7 kHz** (±3,8 dB totalt)
- recensionen nämner en dip i närvaroområdet som "drar tillbaka röster".

**Relevans 🟡:** dippen vid 7 kHz hos RL60.2 sammanfaller med diskantdippen vid 6,5–7 kHz i B&O:s RL6000-data. Det tyder på att diskanttypen eller monteringen (vågledare och front) är besläktad. Det är ett indicium, inte ett bevis. Att RL60.2 går ner till cirka 4,8 Ω trots 8 Ω-märkning tyder också på att B&O:s impedansangivelser var optimistiska.

### A5. Saknad information (❓)

| Saknas | Konsekvens | Hur vi får fram den |
|---|---|---|
| Basdelarnas impedans (Re, Le) | **Avgör topologin** (2,5-väg eller serie) och alla värden i basgrenarna | Multimeter (Re) + REW-impedansmätning |
| Diskantens impedans (Re, fs) | Påverkar mest nivån och högpassets Q. L-padet tar upp avvikelser | Samma |
| Originalfiltrets schema och värden | Behövs för referens och för att förstå B&O:s avvägningar | Foton av kortets båda sidor + kopparbanor |
| Mätförhållanden för B&O-kurvorna (avstånd, baffle, fritt fält eller halvrum) | Påverkar framför allt basbalansen | Okänt. Därför finns S1 |
| Elementens fasrespons | Modellen använder minimumfas, vilket är rimligt men approximativt | Egen akustisk mätning (valfritt) |
| Diskantens effekttålighet | Påverkar skyddsbedömningen | Eventuellt märkning på elementet |
| SU-V505:s exakta lastspecifikation | 60 W / 8 Ω, last 4–16 Ω enligt [HiFi Vintage](https://hifivintage.co.uk/portfolio/technics-su-v505-amplifier/). A+B-regeln är okänd | Bruksanvisningen. **Använd inte A+B med MkII** |

### A6. Gjorda antaganden

1. Basdelarna antas vara 8 Ω nominellt (Re 6,0 Ω, Le 0,45 mH). Diskanten antas vara 8 Ω nominellt (Re 5,8 Ω, fs 1,3 kHz).
2. B&O:s elementkurvor antas vara representativa för dina exemplar och mätta vid samma spänning.
3. Elementens akustiska centrumförskjutning ignoreras (stöds av B&O:s nollfördröjning).
4. Neutralläget optimeras mot rak summa i B&O:s mätvillkor. Väggmonteringen hanteras med S1.

---

## B. Projektets rimlighet

**Ja, det är realistiskt.** Med tre förbehåll.

- **Elektrisk funktion: hög sannolikhet.** Topologin är standard, de simulerade värdena är rimliga och vanliga, och lasten är hanterbar för SU-V505 om Zmin ≥ cirka 3,5 Ω. Arbetsinsatsen ryms i 8–15 timmar. Komponentkostnaden hamnar i övre delen av det accepterade spannet, eller något över (avsnitt E).
- **Akustisk förbättring: sannolik men måttlig.** Originalet är en professionell B&O-konstruktion med begränsningar från 1990-talets kostnadsramar (elektrolyter och få komponenter). Vår fördel är B&O:s egen DSP-trimning som facit, och den visar vad elementen behöver. Ett passivt filter som approximerar den kurvan bör ge en jämnare övergång kring 2–3 kHz och en mer genomtänkt diskantnivå. Mer realistiskt än "dramatiskt bättre" är **"jämnare, tydligare och anpassningsbar"**.
- **Det filtret inte kan göra:** dippen vid 6,5–7 kHz och toppen vid 12,5 kHz är elementets egenskaper. Spridning och djupbas begränsas av låda och element. "Luft" i bemärkelsen jämn energi över 10 kHz kan bara justeras i nivå.
- **Viktigaste osäkerheten** är impedansen hos basdelarna (se A5). Om de är 4 Ω faller 2,5-vägaren och vi går till arkitektur B, som fortfarande är fullt användbar.

Varför jag tror att "närvaro" går att påverka: B&O:s DSP har en lätt sänkning kring 1,4–1,9 kHz. Den råa basen har en topp vid 1,8 kHz. Dessutom ger väggmontering mer lägre bas och lägre mellanregister, vilket relativt sett "drar tillbaka" mellanregistret. Två av de tre omkopplarna angriper just dessa mekanismer.

---

## C. Alternativa arkitekturer

| | **A. Originalbaserad + tillsatsnät** | **B. Ny 2-vägare, bas i serie** | **C. Ny 2,5-vägare (rekommenderas)** |
|---|---|---|---|
| Princip | Renoverat original + omkopplingsbart L-pad och notch | Baselementen i serie (bara om de är 4 Ω), 2:a ordningens LP, 3:e ordningens HP, BSC-nät | Separat LP för nedre bas (cirka 400–600 Hz) och övre bas (cirka 2,5 kHz), 3:e ordningens HP |
| Krav på impedans | Inga nya | Bas 4 Ω vardera | Bas ≥ cirka 6 Ω vardera |
| Ljudpotential | Låg–medel. Ärver originalets övergång | Medel. BSC kostar känslighet | **Hög**. Följer B&O:s egen 2,5-vägsmålkurva, naturlig BSC utan förlust i bas |
| Justerbarhet | Diskantnivå, eventuellt notch | Diskant, närvaro, BSC | Diskant, närvaro, bas/väggbalans |
| Komponenter per sida | cirka 6–8 | cirka 14–16 | cirka 22 |
| Kostnad (par) | cirka 300–500 kr | cirka 1 100–1 700 kr | cirka 1 500–2 200 kr |
| Risk | Måste ändra i originalkortet (krockar med kravet att hålla det intakt) | Lägre känslighet (cirka −3 dB), större BSC-spole | Lägre Zmin (~3,6 Ω). Förutsätter 8 Ω-bas |
| Reversibilitet | Sämre | Bra | Bra |

**Val: C**, med B som förberedd reserv. A förkastas: den bryter kravet på intakt original och ger minst förbättringspotential.

---

## D. Rekommenderad första konstruktion – MkII rev A (arkitektur C)

### D1. Funktionsbeskrivning

- **Nedre bas (W1)** spelar bas och lägre mellanregister upp till cirka 400–600 Hz. Övre bas och nedre bas summeras i basen, vilket ger naturlig baffle step-kompensation utan att ett effektslösande motstånd behövs i huvudvägen.
- **Övre bas (W2)** spelar upp till cirka 2,5 kHz med ett 2:a ordningens lågpass. Ett Zobel-nät linjäriserar impedansen. En parallell-trap i serie formar området 1–2,5 kHz (närvaro).
- **Diskant (T)** har ett 3:e ordningens högpass (C-L-C) som alltid är i kretsen, följt av ett L-pad med omkopplingsbar seriedel.
- **Tre omkopplare** med tre lägen var, en per frekvensband. De påverkar varandra minimalt (se D5).

### D2. Blockschema

```
                ┌──────────────────────── MkII-filter (per högtalare) ─────────────────────────┐
 Förstärkare ──►│                                                                              │
   + / −        │  ├─► [S1-motstånd] ─► [LP 2:a ordn. ~450 Hz] ──────────────────────► W1 nedre bas
                │  │                                                                          │
                │  ├─► [S2 närvaro-trap] ─► [LP 2:a ordn. ~2,5 kHz] ─► [Zobel] ───────► W2 övre bas
                │  │                                                                          │
                │  └─► [HP 3:e ordn. ~2,5 kHz, ALLTID I KRETS] ─► [L-pad, S3] ────────► T diskant
                └──────────────────────────────────────────────────────────────────────────────┘
```

### D3. Preliminärt kopplingsschema (🧮, värden gäller antagen impedans)

```
 AMP+ ──┬─────────────────────────────────────────────────────────────────────────────────────
        │
        │  GREN W1 – nedre bas
        ├──[R1a 2,2Ω]──[R1b 3,3Ω]──[L1 3,9 mH]──┬────────────────────────────────── W1+
        │   S1 kortsluter R1a och/eller R1b      │
        │                                       [C1 15µF]
        │                                        │
        │  GREN W2 – övre bas                    │
        ├──[TRAP]──[L2 0,82 mH]──┬───────┬───────┼────────────────────────────────── W2+
        │                        │       │       │
        │   TRAP =               [C2]    [Rz]    │
        │   Lt 0,47 mH           8,2µF   6,8Ω    │
        │   ∥ Ct 10 µF           │       │       │
        │   ∥ (Rta 2,2Ω + Rtb 3,3Ω)     [Cz]    │
        │   S2 kortsluter hela   [RC2]   8,2µF   │
        │   trapen eller Rtb      1,0Ω   │       │
        │                        │       │       │
        │  GREN T – diskant      │       │       │
        └──[C3 4,7µF]──┬──[C4 22µF]──[Rs1 2,7Ω]──[Rs2 1,8Ω]──[Rs3 2,7Ω]──┬──────────── T+
                       │                 S3 kortsluter Rs2+Rs3 eller Rs3  │
                     [L3 0,22 mH]                                       [Rp 15Ω]
                       │                 │       │       │                │
 AMP− ─────────────────┴─────────────────┴───────┴───────┴────────────────┴── W1− W2− T−
```

**Polaritet:** alla element kopplas i fas (+ till +) i simuleringen. Den passiva fasvridningen gav bäst summa med diskanten i fas 🧮. Det kontrolleras vid första lyssning och mätning (se G4).

### D4. Filtergrenarna i detalj

**W1 – nedre bas.** 2:a ordningens lågpass L1/C1 (cirka 450 Hz i kombination med elementets Le). L1 kan vara en kärnspole eftersom den bara bär bas och lägre mellanregister. S1 lägger 0, 2,2 eller 5,5 Ω i serie. Det sänker W1:s bidrag och därmed bassumman med upp till cirka 1,5–2 dB, utan att påverka något över cirka 700 Hz 🧮. Seriemotståndet höjer också Zmin, vilket är bra för förstärkaren.

**W2 – övre bas.** 2:a ordningens lågpass L2/C2 med RC2 = 1 Ω för att dämpa filterkvaliteten. Zobel (Rz/Cz ≈ 1,1 × Re och Le/Re²) linjäriserar elementets stigande impedans så att lågpasset beter sig förutsägbart. Trapen (Lt ∥ Ct ∥ R, resonans cirka 2,3 kHz men bred) ligger i serie och ger en bred sänkning i området 1–2,5 kHz vars djup bestäms av R.

**T – diskant.** C3 + L3 + C4 bildar ett 3:e ordningens högpass. Tillsammans med elementets egen roll-off blir det cirka 4:e ordningen akustiskt. Elektrisk dämpning 🧮: **−32,5 dB vid 1 kHz** och **−49 dB vid 500 Hz** i alla lägen. Rp = 15 Ω parallellt med diskanten dämpar dess fs-topp och stabiliserar lasten för högpasset. Seriekedjan Rs (2,7 + 1,8 + 2,7 Ω) ger tillsammans med Rp cirka 5–8 dB nivådämpning. Det är just vad B&O:s DSP visar att diskanten behöver.

### D5. Omkopplarna

Samtliga omkopplare **kortsluter seriekomponenter**. De öppnar aldrig en signalväg och sitter aldrig i högpassets C3/L3/C4. Konsekvenser:
- Ett **avbrott** i en omkopplare (glapp, sliten kontakt) ger det läge som har mest seriemotstånd. Det läget ingår i de simulerade, tillåtna lägena.
- En **fastnad kortslutning** ger läget med minst seriemotstånd, som också är simulerat och tillåtet.
- Övergången mellan lägen passerar bara tillstånd med *mer* seriemotstånd. Ingen spik, ingen kortslutning över förstärkaren.
- **Diskantens högpass kan inte förbikopplas** av någon omkopplare, varken genom fel eller genom läge.

| Omkopplare | Läge ▲ | Läge ● (mitten) | Läge ▼ | Verkan (🧮, relativt neutral) |
|---|---|---|---|---|
| **S1 Bas/vägg** | **Fri** (R = 0) | **Neutral** (R = 2,2 Ω) | **Vägg** (R = 5,5 Ω) | 100–200 Hz: +0,8 / 0 / −0,9 dB. Ingen verkan över 700 Hz |
| **S2 Närvaro** | **Fram** (trap förbikopplad) | **Neutral** (R = 2,2 Ω) | **Mjuk** (R = 5,5 Ω) | 0,7–2 kHz: +1,2…+1,5 / 0 / −1,0…−1,3 dB |
| **S3 Diskant** | **+** (Rs = 2,7 Ω) | **0** (Rs = 4,5 Ω) | **−** (Rs = 7,2 Ω) | 8–16 kHz: +1,2…+2 / 0 / −1,4…−2 dB. Vid 4 kHz ±0,5 dB |

Samtliga 27 kombinationer är simulerade. **Zmin = 3,64 Ω** i värsta fallet (S1 Fri, cirka 200 Hz). Diskantskyddet är identiskt i alla lägen. Se `plots/03_impedance_all.png`.

**Omkopplartyp:** en **DPDT-vippomkopplare ON-ON-ON** (6 A eller mer) per funktion och högtalare. Kopplingsmönster, som är generiskt för alla tre omkopplarna:
- Pol 1 kortsluter element "A" och är sluten i läge ▲.
- Pol 2 kortsluter element "B" och är sluten i lägena ▲ och ●.
- S1: A = R1a, B = R1b. S2: A = hela trapen, B = Rtb. S3: A = Rs2, B = Rs3.

Det ger monotona lägen (▲ minst R, ● mellan, ▼ mest R) och mittläget blir neutralt. **Kontaktschemat för ON-ON-ON varierar mellan tillverkare. Mät upp varje omkopplare med multimeter innan den löds in.** Vippomkopplare valdes före vridomkopplare eftersom billiga vridomkopplare oftast bara klarar 0,15–0,5 A. S1 och S2 bär upp till cirka 3–3,7 A (sinus, full effekt 🧮).

**Säkerhetsregel:** ändra lägen vid låg volym eller med förstärkaren dämpad. Det är inte farligt att växla under spel, men kontaktnötningen blir mindre och man undviker knäppar.

### D6. Fasta skyddskomponenter

- C3, L3 och C4 (diskantens högpass): fasta, ingen omkopplare i den vägen.
- Rp: fast. Om den brister blir diskanten cirka 1 dB starkare, vilket är ofarligt.
- **Säkring eller PTC: ingen i rev A.** Motivering: med 60 W förstärkare och −32 dB vid 1 kHz får diskanten under 0,3 mW per 1 W insignal vid 1 kHz 🧮. Det verkliga hotet är klippning i förstärkaren vid hög volym, där hela högfrekvenseffekten hamnar i diskanten. En polyfuse (t.ex. 0,5–1 A, kall resistans cirka 0,3–1 Ω) kan läggas in som *del av Rs* när diskantens tålighet är känd. Den påverkar då nivån förutsägbart. Är originalets glaskomponent en skyddslampa tar vi samma ställning till den då.

### D7. Anslutning och återställning

1. **Ny kabelhärva i högtalaren:** varje element får ett eget ledarpar till en 6-polig kontakt (W1±, W2±, T±). Diskantledaren förlängs (det behövdes även i BeoCreate-guiden).
2. **Ny terminalplatta** (3D-printad, passar i originalurtaget) med 6-polig chassikontakt, t.ex. 2 × Speakon NL4 eller en 8-polig Speakon NL8. Originalets terminalkopp sparas.
3. **Både originalfiltret (renoverat) och MkII placeras i separata externa lådor** under utvärderingen. Varje låda har förstärkaringång och 6-polig utgång. A/B-byte = flytta en kontakt.
4. **Återställning:** originalkortet skruvas tillbaka på sina poster. Härvan kopplas till kortet via kabelskor eller lödning, och originalterminalen monteras. Inga hål eller ingrepp i originalkortet behövs.

---

## E. Komponentlista och kostnad (BOM)

Priser är **uppskattningar** utifrån typiska europeiska nätbutikspriser (soundimports.eu, lautsprechershop.de, Elfa Distrelec, Kjell & Co), utom där det anges. **Verifierat prisunderlag:** Intertechnik LU55/082/100 (0,82 mH luft, 0,52 Ω) 16,25 €, HQR32/082/71 (0,82 mH rörkärna) 6,45 € ([soundimports](https://www.soundimports.eu/en/it-intertechnik-hqr32-082-71.html)).

| Ref | Komponent | Specifikation | Antal (par) | Uppsk. kr/st | Summa |
|---|---|---|---|---|---|
| L1 | 3,9 mH kärnspole (ferrit/rörkärna) | DCR ≤ 0,5 Ω, Isat ≥ 4 A | 2 | 90 | 180 |
| L2 | 0,82 mH spole | **Luft** 1,0 mm (rek.) eller kärnspole med Isat ≥ 5 A | 2 | 180 / 75 | 360 / 150 |
| Lt | 0,47 mH spole | Luft 0,8 mm eller kärnspole | 2 | 110 / 65 | 220 / 130 |
| L3 | 0,22 mH luftspole | 0,8 mm | 2 | 70 | 140 |
| C1 | 15 µF | Bipolär elektrolyt 100 V (räcker i basgren) | 2 | 15 | 30 |
| C2 | 8,2 µF | MKT/MKP 100 V+ | 2 | 25 | 50 |
| Cz | 8,2 µF | MKT 100 V+ | 2 | 25 | 50 |
| Ct | 10 µF | MKT/MKP 100 V+ | 2 | 30 | 60 |
| C3 | 4,7 µF | **MKP** 250 V (diskantens seriekond.) | 2 | 30 | 60 |
| C4 | 22 µF | MKT 100 V+ (eller bipolär elyt) | 2 | 45 | 90 |
| R1a, R1b | 2,2 Ω / 3,3 Ω | 10 W cement/MOX (sinus max 6–10 W 🧮) | 2+2 | 12 | 48 |
| Rta, Rtb | 2,2 Ω / 3,3 Ω | 10 W | 2+2 | 12 | 48 |
| Rs1–Rs3 | 2,7 / 1,8 / 2,7 Ω | 10 W | 6 | 12 | 72 |
| Rp | 15 Ω | 10 W | 2 | 12 | 24 |
| Rz, RC2 | 6,8 Ω / 1,0 Ω | 10 W / 5 W | 2+2 | 12 | 48 |
| S1–S3 | DPDT ON-ON-ON vippomkopplare | ≥ 6 A, skruv- eller lödanslutning | 6 | 50 | 300 |
| – | Montageplatta, plint, buntband | Hålkortsplatta/MDF + skruvplintar | – | – | 100 |
| – | 6-poliga kontakter + kabel | Speakon NL4 ×2 per sida eller motsv., 4-ledare 1,5 mm² | – | – | 250 |
| – | Diskantförlängning, kabelskor, krympslang | – | – | – | 50 |
| | **Summa standard (luft på L2/Lt)** | | | | **≈ 2 180 kr** |
| | **Summa budget (kärnspolar L2/Lt, skruvplintar i stället för Speakon, enklare vippor)** | | | | **≈ 1 500 kr** |

**Kostnadsbedömning:** kontaktsystem och omkopplare utgör cirka 25 % av kostnaden. Rimligt sparupplägg för en första prototyp:
1. Använd kärnspolar på L2 och Lt. Spolarna är relativt små och strömmen måttlig. Skillnaden mot luftspolar är mätbar men sannolikt liten vid hemmavolym.
2. Använd skruvplintar i stället för Speakon för kabeln till högtalaren. Plintar är billiga och ändå reversibla.
3. **Om budgeten ska ned mot 1 000 kr:** stryk S2 (närvaro) i rev A och ersätt trapen med en bygel. Det sparar Lt, Ct, Rta, Rtb och två omkopplare, cirka 350–450 kr. S1 och S3 ger tillsammans redan en tydlig tonal lutning. S2 kan läggas till senare på samma platta.

**Återanvändning:** inga originalkomponenter återanvänds, eftersom originalet ska behållas intakt. Originalkablar, poster och terminalkopp återanvänds vid återställning.

**Leverantörer** (verifiera lagerstatus): [soundimports.eu](https://www.soundimports.eu) (NL, Intertechnik/Jantzen/Mundorf), lautsprechershop.de (DE), Elfa Distrelec (SE, omkopplare, motstånd, Speakon), Kjell & Co (SE, kabel, plintar).

**Inte i budget men starkt rekommenderat:** mätmikrofon miniDSP UMIK-1 (cirka 1 200 kr) eller ett USB-ljudkort (cirka 300 kr) för impedansmätning med REW (gratis). Se G och I.

---

## F. Mekaniskt koncept

**Fas 1 – extern experimentlåda (rekommenderas för prototypen):**
- Låda cirka 200 × 150 × 80 mm (3D-printad eller MDF), en per högtalare, eller en dubbel.
- Komponenterna monteras på en platta med buntband och varmlim. **Spolarna placeras minst cirka 5 cm från varandra med axlarna vinkelräta**, så att de inte kopplar induktivt.
- Front: tre vippomkopplare med graverade eller printade etiketter (BAS: Fri/Neutral/Vägg · NÄRVARO: Fram/Neutral/Mjuk · DISKANT: +/0/−).
- Bak: förstärkaringång (polklämmor) och 6-polig utgång.
- Varför externt: högtalarna sitter på vägg, så omkopplare på baksidan vore oåtkomliga. Lådan gör A/B-jämförelsen mot originalet trivial och kräver ingen ändring av högtalaren utöver härva och terminalplatta.

**Fas 2 – intern montering (när favoritlägen är hittade):**
- MkII-kortet monteras på en 3D-printad bärplatta på originalets skruvposter (BeoCreate-guiden visar att posterna går att använda för en sådan platta).
- Omkopplarna kan antingen ersättas med fasta byglar för de valda lägena, eller placeras i den nya terminalplattan om högtalaren kan monteras så att baksidan är åtkomlig.

**Monteringsregler:** spolarnas DCR ingår i beräkningen, så använd de specificerade spolarna. Mät DCR före montering. Motstånd på 10 W placeras med luft runt sig och inte mot plast eller dämpmaterial.

---

## G. Säkerhet och elektrisk kontroll

### G1. Före första inkoppling till elementen

1. **Mät elementens impedans** (avsnitt I). Uppdatera `DRIVERS` i `sim/rl6000_mkii_sim.py` och kör om. **Kriterium:** Zmin ≥ 3,5 Ω i alla 27 lägen och diskantens dämpning ≥ 30 dB vid 1 kHz. Skriptet stoppar om Zmin < 3,2 Ω.
2. **Mät varje komponent** före lödning (L, C, R). Spolar och kondensatorer har ofta 5–10 % tolerans.
3. **Kontinuitetstest per omkopplare och läge**, med filtret frånkopplat. Mät likströmsresistansen in → varje elementutgång. Förväntat för W1-grenen: DCR(L1) + {0 | 2,2 | 5,5} Ω. Diskantgrenen ska visa **avbrott** (C3 i serie) i alla lägen. Visar diskantgrenen likströmsgenomgång finns ett kopplingsfel.
4. **Isolationskontroll:** inga förbindelser mellan grenarnas +-ledare utom vid ingången, och ingen kortslutning in+ → in−.

### G2. Första spänningssättning, med dummy-last

5. Ersätt elementen med effektmotstånd på 8 Ω (eller använd elementen men börja på mycket låg volym).
6. Mata **200 Hz sinus** från en tongenerator (REW eller en mobilapp) på låg nivå. Mät växelspänningen över diskantutgången. Den ska vara cirka **1/1000** av ingången (−60 dB eller lägre).
7. Mata 1 kHz och kontrollera att diskantutgången ligger cirka −30 dB under ingången.
8. Svep 20 Hz–20 kHz och kontrollera att varje gren "tar över" i rätt område (enkel AC-voltmeter eller oscilloskop).

### G3. Impedansen för förstärkaren

9. Med REW och en enkel mätjigg mäts den kompletta högtalarens impedans i de extremaste lägena: S1 Fri / S2 Fram / S3 +, och S1 Vägg / S2 Mjuk / S3 −. **Kriterium:** minimum ≥ 3,5 Ω. Kör **inte** SU-V505 i läge A+B med MkII.

### G4. Polaritet och övergång

10. Byt diskantens polaritet tillfälligt. Med rätt polaritet ska det vara **mindre** fyllighet i en djup dipp kring 2–3 kHz (lyssning: rosa brus på 1 m, eller REW-mätning). Simuleringen säger: i fas.

### G5. Kritiska felmoder

| Felmod | Följd | Skydd i konstruktionen |
|---|---|---|
| Glapp eller avbrott i omkopplare | Läget med mest R | Ofarligt, ingår i simulerade lägen |
| Kortslutning i omkopplare | Läget med minst R | Ofarligt, ingår i simulerade lägen |
| C3 kortsluten (dielektrikgenomslag) | Diskanten får mer bas | Kvar finns C4 + L3 (2:a ordningen). MKP 250 V i C3 minskar risken |
| L3 avbrott | Diskantens högpass blir 1:a ordningen + C4 | Hörbart (skarpt). Upptäcks vid G1-kontrollen |
| Rp avbrott | Diskanten cirka +1 dB | Ofarligt |
| Feldimensionerat nät (4 Ω-bas) | Zmin cirka 2,5 Ω | **Spärras av impedansmätningen i steg 1** |
| Klippning i förstärkaren vid hög volym | Övertoner i diskanten | Ingen passiv krets löser det helt. Undvik extrem volym. Polyfuse är ett valbart tillägg (D6) |

**Vad som inte kan verifieras än:** det verkliga skyddet för diskanten (dess effekttålighet är okänd ❓) och verklig Zmin (elementimpedans ❓). Båda löses i steg I.

---

## H. Genomförandeplan

| # | Moment | Vem | Tid |
|---|---|---|---|
| 0 | Dokumentera ljudet med originalfiltret, tillstånd A (lyssning, gärna mätning) | Du | 0,5 h |
| 1 | Öppna en högtalare. Fotografera kortets båda sidor och märkningen på alla element. Mät Re för alla tre element med multimeter | Du | 1 h |
| 2 | Uppdatera simuleringen med uppmätta Re och identifiera originalets topologi från fotona | **Jag** | – |
| 3 | Renovera originalfiltren (DK-kitet), tillstånd B. Behåll layouten | Du | 1,5 h |
| 4 | Impedansmätning med REW + ljudkort och jigg (valfritt men rekommenderat) | Du (jag skriver instruktion) | 1 h |
| 5 | Slutliga komponentvärden och beställningslista med artikelnummer | **Jag** | – |
| 6 | Bygg härva och terminalplatta (3D-print, kabel, kontakter) i båda högtalarna | Du (jag kan ta fram CAD-mått om du mäter urtaget) | 2 h |
| 7 | Bygg två MkII-lådor och lägg originalfiltren i egna lådor | Du | 4–5 h |
| 8 | Elektriska kontroller enligt G1–G4 | Du | 1 h |
| 9 | Lyssning: original B mot MkII neutral, sedan omkopplarna en i taget | Du | 1–2 h, gärna utspritt |
| 10 | Eventuell finjustering (t.ex. trap vid 12,5 kHz, R-steg) | Jag beräknar, du byter komponenter | 1 h |
| | **Summa praktiskt** | | **cirka 12–14 h** |

**Lyssningsmetodik (enkel men ärlig):**
- Nivåmatcha original och MkII vid 1 kHz (±0,5 dB, mätt med mobilapp eller REW) före jämförelse, annars vinner den högre.
- Jämför med samma 4–5 välkända spår. Byt bara en omkopplare åt gången.
- Anteckna intryck *innan* du vet vilket läge som är aktivt, om någon kan hjälpa till.

---

## I. Nästa konkreta steg (prioriterat)

1. **Mät Re (likströmsresistans) för de tre elementen** i en högtalare med multimeter, med elementen bortkopplade från filtret. *Varför:* avgör om vi bygger arkitektur C (Re cirka 5,5–7 Ω per baselement) eller B (Re cirka 3–3,5 Ω). Detta är det enskilt viktigaste.
2. **Fotografera originalfiltret** (komponentsidan och kopparsidan, skarpt och rakt uppifrån) samt **märkningen på elementen**. *Varför:* för att rekonstruera originalschemat, se om basen redan delas som 2,5-väg och identifiera skyddskomponenten.
3. **Skaffa ett enkelt mätupplägg för impedans** (REW + USB-ljudkort med in/ut, t.ex. Behringer UCA202, cirka 300 kr, + motstånd på 10 Ω och 100 Ω). *Varför:* ger Le, fs och verklig impedanskurva. Då kan värdena i rev B räknas fram med god marginal i stället för att vila på antaganden.
4. *(Valfritt, högt värde)* **Mätmikrofon (UMIK-1).** *Varför:* gör att vi kan verifiera simuleringen akustiskt, kontrollera polariteten och hitta dina favoritlägen med data i stället för minnet.
5. Beställ DK-kitet och renovera originalfiltren parallellt. Det är referensen och behöver göras oavsett.

När punkt 1–2 är klara tar jag fram rev B: slutliga värden, beställningslista med artikelnummer och kopplingsschema för omkopplarna.

---

## Bilagor

### Filer
- `data/beocreate_rl6000_curves.json`: extraherade B&O-kurvor (element, DSP-filter, resultat). Källa: [bang-olufsen/create](https://github.com/bang-olufsen/create), MIT.
- `sim/rl6000_mkii_sim.py`: simuleringsmodell. Kör `python3 sim/rl6000_mkii_sim.py` (kräver numpy och matplotlib). Skriver ut alla 27 lägen och genererar plottar.
- `plots/01_neutral.png`: grenar, summa och impedans i neutralläge, jämfört med B&O:s DSP-resultat.
- `plots/02_switches.png`: verkan av varje omkopplare.
- `plots/03_impedance_all.png`: impedans i alla 27 lägen.

### Simuleringsmetod
Elektrisk överföringsfunktion per gren (stegnät med komplexa impedanser, inklusive spolarnas DCR och en modell av elementimpedansen) multipliceras med B&O:s uppmätta elementrespons (magnitud, med minimumfas rekonstruerad via kepstrum). Grenarna summeras komplext. **Detta är en beräknad akustisk respons i B&O:s mätvillkor, inte en verifierad frekvensgång i ditt rum.**

### Känslighetsanalys (🧮)

| Antagande ändras | Zmin (värsta) | Effekt |
|---|---|---|
| Som antaget | 3,64 Ω | Referens |
| Bas 4 Ω (Re 3,3) | **2,47 Ω** | ❌ 2,5-vägaren olämplig → arkitektur B |
| Diskant fs 1,8 kHz | 3,64 Ω | Försumbar |
| Diskant 4 Ω (Re 3,4) | 3,64 Ω | Diskanten cirka −2 dB i toppen, kompenseras med Rs |

Slutsats: **diskantens data påverkar i praktiken bara nivån, som L-padet hanterar. Basens impedans avgör arkitekturen.**

### Källor
- B&O / HiFiBerry BeoCreate: <https://github.com/bang-olufsen/create>. Mappen `Speakers/Beovox RL 6000/`, presetfilen `Beocreate2/beo-speaker-presets/beovox-rl6000.json` och guiden `Guides/Upcycle Beovox RL 6000.pdf` (identisk med <https://www.hifiberry.com/wp-content/uploads/2018/05/rl6000-guide.pdf>)
- Beoworld produktdata: <https://archived.beoworld.org/prod_details.asp?pid=652>
- Beocentral: <https://beocentral.com/beovoxrl6000>
- beo.zone: <https://beo.zone/en/beovox-rl-6000-passive-loudspeakers>
- Hi-Fi News, RL60.2 Lab Report: <https://www.hifinews.com/content/bang-olufsen-beovox-red-line-602-loudspeaker-lab-report> (via sökutdrag)
- DK Soundparts CK-059: <https://www.dksoundparts.com/product/capacitor-kit-beovox-redline-rl6000/> (via sökutdrag)
- Technics SU-V505: <https://hifivintage.co.uk/portfolio/technics-su-v505-amplifier/>, <https://www.radiomuseum.org/r/technics_stereo_integrated_amplifier_su_v505_ek.html>
- Soundimports (priser för spolar): <https://www.soundimports.eu/en/it-intertechnik-hqr32-082-71.html>
