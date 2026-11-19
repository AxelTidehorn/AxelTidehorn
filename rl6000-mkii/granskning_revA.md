# Svar på teknisk granskning av rev A

**RL6000 MkII · 2026-11-19**

Alla siffror nedan är **beräknade** i samma modell som tidigare: B&O:s elementdata och **antagen** elementimpedans. De kan reproduceras med:

```
cd rl6000-mkii/sim
python3 rl6000_mkii_sim.py      # rev A (oförändrad), plots 01–03
python3 review_revA.py          # granskningsanalyser av rev A, plots 05–06
python3 revB_candidate.py       # rev B-kandidat, plots 07–08
python3 schematic.py            # schema rev A (kräver schemdraw)
```

Rådata: `data/beocreate_rl6000_curves.json`. Källan är B&O:s egna PDF-filer i [bang-olufsen/create](https://github.com/bang-olufsen/create), MIT-licens.

---

## Punkt 2 – Klassificeringen av originalfiltret

**Bedömning: håller med.** Min slutsats "troligen tvåvägare" var för svagt underbyggd och dras tillbaka.

- **Motivering:**
  - Två synliga spolar utesluter inte 2,5-väg. Exempel: nedre basen får en seriespole som enda lågpass, övre basen går utan spole eller med ett enklare nät, och diskanten har C–L–C. Fler spolar kan dessutom ha legat utanför bilden.
  - [Hi-Fi News test (2024)](https://www.hifinews.com/content/bang-olufsen-beovox-red-line-602-loudspeaker) av RL60.2 skriver att de två baselementen delar vid olika frekvenser ("two-and-a-half way").
  - Enligt [Beocentral](https://beocentral.com/beovoxrl60-2) har RL60.2 två 13 cm-element, varav ett tar mellanregistret. RL6000 har samma elementuppsättning.
- **Verifierat:**
  - RL60.2 är 2,5-väg (Hi-Fi News).
  - RL60 hade 16 cm-baselement och passivt basmembran. RL60.2 bytte till 2 × 13 cm ([Beocentral](https://beocentral.com/beovoxrl60-2)).
  - Någon gång i serien byttes en Philips-diskant mot en Vifa-diskant och delningen "lightly revised" (Hi-Fi News, via sökutdrag). Exakt vilken modell det gällde är oklart.
- **Sannolikt:** RL6000 är också 2,5-väg.
- **Okänt:**
  - RL6000:s schema.
  - Exakta skillnader mellan RL60.2 och RL6000. Jag hittade ingen källa, och Beoworld och Hi-Fi News gick bara att läsa via sökutdrag från den här miljön.
- **Konsekvens:**
  - Argumentet "2,5-väg som förbättring" i rev A försvagas. Förbättringen måste i stället komma från diskantgrenens utformning, anpassning till väggen, justerbarhet och nya komponenter.
  - Ett rekonstruerat original blir en starkare kandidat som bas för basgrenarna (se punkt 10).
- **Åtgärd rev B:** rita av originalkortet från foton, simulera originalet i samma modell med B&O-data och jämför. **Det här är det enskilt mest värdefulla analyssteget.** Det ger oss ett mått på hur stor förbättringspotentialen är, utan akustisk mätning.

## Punkt 3 – Impedans och förstärkarbelastning

**Bedömning: håller delvis med.** Granskaren har rätt i att jag bara redovisade |Z|. Jag hittade dessutom ett eget fel som gör rev A sämre än rapporterat.

**Underlag** (`review_revA.py`, avsnitt 1–2):

| | rev A (rapport) | rev A, korrigerad L1-DCR | rev A, toleranser (Monte Carlo) | rev B-kandidat | RL60.2 uppmätt (Hi-Fi News) |
|---|---|---|---|---|---|
| \|Z\| min | 3,64 Ω | **3,34 Ω** | median 3,62 / 5 % 3,35 / min 3,15 | 3,49 Ω (6,6 kHz) / 3,57 Ω (190 Hz) | 4,75 Ω @ 172 Hz |
| Fas | – | −50…+46° | – | – | −42…+33° |
| EPDR min | – | 1,75 Ω @ 110 Hz | – | 1,80 Ω | 2,3 Ω @ 124 Hz |

- **Eget fel:** rev A modellerade L1 (3,9 mH) med luftspolens likströmsresistans, cirka 1,8 Ω. Rapporten föreskriver en kärnspole, som har cirka 0,5 Ω. Lägre seriemotstånd ger lägre Zmin.
- **Monte Carlo-antaganden:** komponenter ±5 % (1σ), elektrolyter ±10 %. Elementen: Re ±7 %, Le ±25 %, fs ±15 %, Q ±15–20 %.
- **EPDR** (Keith Howards mått, beräknat numeriskt) är den resistiva last som skulle ge samma toppeffekt i slutsteget. EPDR cirka 1,8–1,9 Ω motsvarar en vanlig "4 Ω-högtalare". Det är något tyngre än RL60.2 enligt Hi-Fi News mätning.
- **Gränsvärde:** IEC 60268-5 anger att minimum inte bör understiga 80 % av märkimpedansen. För 4 Ω innebär det 3,2 Ω. Rev B ligger på 3,5 Ω nominellt och kring 3,2 Ω i toleransernas värsta fall. Det är en **4 Ω-klassad last**, inte en 8 Ω-last.
- **SU-V505:**
  - 60 W/8 Ω och last 4–16 Ω enligt [HiFi Vintage](https://hifivintage.co.uk/portfolio/technics-su-v505-amplifier/) och [Radiomuseum](https://www.radiomuseum.org/r/technics_stereo_integrated_amplifier_su_v505_ek.html).
  - Systermodellen SU-V500:s bruksanvisning anger A eller B 4–16 Ω och A+B 8–16 Ω ([archive.org](https://ia800808.us.archive.org/30/items/manual_SUV500_OM_TECHNICS_EN/SUV500_OM_TECHNICS_EN_text.pdf)).
  - Bruksanvisningen för V505 ([HiFi Engine](https://www.hifiengine.com/manual_library/technics/su-v505.shtml)) kunde jag inte öppna härifrån.
  - **Slutsats:** fungerar med en högtalarutgång, men använd aldrig A+B.
- **Viktig observation:** modellen ger lägre Zmin än RL60.2:s uppmätta 4,75 Ω. Antingen är min antagna basimpedans för låg, eller så har originalet mer seriemotstånd i basgrenen. Det går inte att avgöra utan impedansmätning.
- **Re mot impedansmätning:**

| Beslut | Re räcker | Kräver impedanskurva |
|---|---|---|
| Arkitektur: 2,5-väg parallell (Re cirka 5,5–7 Ω) eller serie (Re cirka 3–3,5 Ω) | ✅ | |
| Grov Zmin-uppskattning i basen (cirka 0,9–1,0 × Re per elementpar) | ✅ (±15 %) | |
| Zobel-värden (kräver Le) | | ✅ |
| Lådans och portens resonanser, EPDR i basen | | ✅ |
| Diskantens fs (påverkar högpassets Q och skyddet) | | ✅ |
| Slutlig verifiering av Zmin och EPDR för alla lägen | | ✅ |

- **Åtgärd rev B:**
  - Krav: Zmin ≥ 3,2 Ω inklusive toleranser och EPDR ≥ cirka 1,7 Ω.
  - **Impedansmätning blir obligatorisk före beställning.** Tidigare var den bara rekommenderad.
  - Värsta Zmin i rev B ligger vid 6,6 kHz (S3 + och S2 Mjuk), där strömbehovet vid musik är litet. Att höja den kostar diskantomfång. Jag har behållit värdena och dokumenterar avvägningen här.

## Punkt 4 – Simuleringsmodellens tillförlitlighet

**Bedömning: håller delvis med.**

- **Minimumfas:** rimligt för konelement och kalotter i deras arbetsområde. Det är standardpraxis, och VituixCAD och XSim gör likadant när fasdata saknas. Approximationen blir sämre vid brytningar, till exempel basens topp vid 12,6 kHz, men där spelar basen inte. **Verklig fas finns inte i B&O-datat:** SigmaStudio-projektet (`.dspproj`) innehåller bara DSP-block och inga mätningar.
- **Argumentet om nollfördröjning:** granskaren har rätt i att det är svagt. B&O kan ha accepterat en förskjutning. Jag drar tillbaka det som indicium och ersätter det med en känslighetsanalys (`plots/05_delay_sensitivity.png`):

| Diskantens förskjutning (+ = diskanten senare) | Variation 1,5–5 kHz relativt 1 kHz |
|---|---|
| −60 µs (−21 mm) | −1,9 / +1,8 dB |
| −30 µs (−10 mm) | −1,7 / +1,9 dB |
| 0 | −2,0 / +1,2 dB |
| +30 µs (+10 mm) | −3,0 / +0,9 dB |
| +60 µs (+21 mm) | **−5,0** / +0,6 dB |
| +90 µs (+31 mm) | **−8,5** / +0,3 dB |
| Diskant inverterad | −11,5 dB (tydlig dipp, alltså hörbart testbart) |

- **Fysisk förväntan:** på en plan front sitter konens akustiska centrum normalt bakom kalottens. Diskanten kommer då *tidigare*, vilket motsvarar negativa värden, och där är summan robust. Om diskanten sitter försänkt eller i en djup vågledare kan läget vara det omvända.
- **Toleranser:** spridningen (5–95 %) är median 1,5 dB och som mest 2,8 dB vid 1,8 kHz.
- **Slutsats:** "±2 dB" är ett **modellresultat**. Det håller för −20…+10 mm förskjutning och normala toleranser, men det är inte en verifierad frekvensgång.
- **Åtgärd:**
  - Mät med linjal djupet från frontens plan till kalottens topp och till baselementets dammkåpa (två minuter). Då vet vi åt vilket håll förskjutningen går.
  - Gör ett polaritetstest vid första lyssningen.
  - Alla filer är versionerade i repot (se ovan).

## Punkt 5 – Närvarokontrollen

**Bedömning: håller med.** Det här är granskningens viktigaste punkt för dina mål. Rev A:s S2 verkade vid 0,7–2 kHz, och 3–5 kHz saknade en egen kontroll.

Jag har testat tre lösningar:

| Lösning | Verkan vid 3–5 kHz | Varför |
|---|---|---|
| W2-trapen flyttad uppåt (2,3 kHz) | Max cirka 1,3 dB vid 1–2 kHz, under 0,5 dB vid 3 kHz | W2 är redan på väg ut vid 2,5 kHz. Det är en fysisk gräns |
| Trap i **serie** med diskanten (3,4 kHz) | ±0,6 dB | Högre lastimpedans ger mer överslängning i högpassfiltret, som **kompenserar** sänkningen |
| **Shunt**-notch över diskanten (Ln–Cn–Rn, 3,4 kHz) | **+2,5 / −1,6 dB** | Lägre lastimpedans ger mindre överslängning i högpasset, som **förstärker** sänkningen |

- **Konsekvens:** rev B får S2 som shuntnotch över diskanten. Läget "Fram" kopplar bort shunten, vilket bara höjer diskantnivån och aldrig rör högpasset.
- **Samverkan med S3:** S2 Fram + S3 + ger cirka +2,5…+3,5 dB vid 3–6 kHz. S2 Mjuk + S3 − ger motsvarande sänkning. De två kontrollerna går att förstå: S2 är ett band vid 3–5 kHz och S3 en hylla från 3 kHz och uppåt.
- **Ärlig reservation:** i rev B:s neutralläge ligger 2,5–4 kHz cirka 2,5 dB under nivån vid 1 kHz. B&O:s DSP-resultat ligger cirka 1 dB under. "Fram" ligger alltså närmast B&O:s mål. Om du konsekvent föredrar Fram centrerar vi om efter lyssning.

## Punkt 6 – Varför cirka 450 Hz för nedre basen?

**Bedömning: håller delvis med.** Motiveringen saknades i rapporten.

- **Varför 450 Hz:** värdet kom ur anpassningen till B&O:s mätningar i fritt fält. Det var inte ett försök att efterlikna B&O:s DSP. B&O delar vid 801 Hz men sänker *båda* baselementen 6 dB i basen. Det går inte att göra passivt utan att förlora 6 dB känslighet i ett motstånd. Passivt får vi i stället naturlig baffle step-kompensation genom att båda elementen spelar i basen och W1 tonar ut tidigare.
- **Svep** (`review_revA.py` avsnitt 4, `plots/06_w1_crossover_sweep.png`; S1 Fri, relativt 1,5 kHz):

| W1-delning | Zmin | Fritt fält 150 / 400 Hz | Vägg (modell) 150 / 400 Hz |
|---|---|---|---|
| cirka 300 Hz (6,8 mH, 33 µF) | 4,14 | +1,6 / +1,0 | +5,5 / +2,9 |
| cirka 450 Hz (3,9 mH, 15 µF) | 3,69 | +0,8 / +1,3 | +4,7 / +3,1 |
| cirka 600 Hz (2,7 mH, 10 µF) | 3,51 | −0,3 / +1,0 | +3,6 / +2,8 |
| cirka 800 Hz (1,8 mH, 6,8 µF) | 3,39 | −1,1 / +0,9 | +2,7 / +2,7 |

- **Spridning:** de två baselementen ger ingen utsläckning utanför axeln under cirka c/(2d) ≈ 1,0 kHz, med *antaget* centrumavstånd d = 0,17 m. Alla alternativ upp till 800 Hz är därför likvärdiga i det avseendet.
- **Slutsats:**
  - I fritt fält skiljer alternativen bara cirka ±1 dB.
  - **Vid väggmontering blir alla alternativ 3–5 dB för basstarka.** Det är S1:s uppgift, inte brytfrekvensens.
  - 450 Hz behålls som kompromiss mellan Zmin (högre fc ger lägre Zmin), spolkostnad (lägre fc ger större spole) och tonbalans.
  - Väggmodellen är ett antagande: +5 dB under cirka 250 Hz, eftersom baffle step försvinner vid montering tätt mot vägg.

## Punkt 7 – Omkopplingssäkerhet och komponentbelastning

**Bedömning: håller delvis med.**

- **Kontaktfel:** jag har nu verifierat ett *starkare* påstående än i rapporten. Varje omkopplare har två kontaktvägar, och **alla fyra kombinationerna** (av/på × av/på) ger ett tillstånd med värden inom de simulerade, oavsett kontaktbild och i vilken ordning kontakterna bryter. Exempel: S1 med bara R1a kortsluten ger R = 3,3 Ω och Zmin 4,24 Ω (`review_revA.py` avsnitt 7).
- **Transienter:** inga omkopplare bryter strömmen i en ensam spole. I rev B bryter S2 en serie-LCR-gren. Energin i Ln är ½·L·I² ≈ 0,5 · 0,47 mH · (0,5 A)² ≈ 60 µJ, vilket är försumbart. Däremot ger nivåsteg under spel knäppar.
- **Beslut:** **omkoppling sker med förstärkaren avstängd.** Du har sagt att det fungerar för dig. Det eliminerar alla frågor om kopplingsförlopp och gör att omkopplarna bara behöver dimensioneras för *ledningsström*, inte brytförmåga.
- **DPDT ON-ON-ON:** sådana finns, till exempel i C&K 7000-serien och hos APEM, men kontaktbilden varierar. Rev B:s S3 använder båda omkopplingsvägarna per pol och förutsätter standardbilden: läge 1 = 2-1 och 5-4, läge 2 = 2-3 och 5-4, läge 3 = 2-3 och 5-6. **Kontrollera med multimeter före inlödning.** Om bilden avviker byter vi till en 2-polig vridomkopplare med 3 lägen, vilket fungerar eftersom brytförmåga inte längre krävs.
- **Effekt i motstånd:** rosa brus som musikproxy (avsnitt 5), värsta läge:

| Motstånd | 2 W medel (högt) | 10 W medel (nära klippning) | Föreslagen märkeffekt |
|---|---|---|---|
| R1 (W1-serie, Vägg) | 0,19 W | 0,95 W | 10 W (5 W räcker) |
| Rta+Rtb (rev A) | 0,10 W | 0,51 W | utgår i rev B |
| Rz (Zobel) | 0,04 W | 0,20 W | 5 W |
| Rs-kedjan | 0,38 W | 1,9 W | **10 W** |
| Rp | 0,07 W | 0,35 W | 5 W |

Sinusvärdena i rapporten (upp till 68 W) gällde full effekt med sinus över 1 kHz. Det är ett orealistiskt fall där diskanten själv skulle gå sönder först. 10 W-motstånd ger mer än 5 gångers marginal vid musik.
- **Felmoder i diskantgrenen** (avsnitt 6, elektrisk dämpning till diskanten):

| Fel | 500 Hz | 1 kHz | Zmin | Bedömning |
|---|---|---|---|---|
| Intakt | −49 | −32,5 | 4,09 | |
| **C3 kortsluten** | −11 | −5,6 | **0,32 Ω** | **Nytt fynd:** L3 hamnar direkt över förstärkaren. Typiskt för C–L–C-filter |
| C4 kortsluten | −45 | −32 | 4,09 | Ofarligt |
| L3 avbrott | −25 | −16 | 4,09 | Risk för diskanten vid hög volym |
| Rp avbrott | −46 | −30 | 4,09 | Ofarligt |
| Rp kortsluten | – | – | 4,09 | Diskanten tyst, ofarligt |

**Åtgärd:**
- C3 ska vara en metalliserad polypropenkondensator (MKP). Den är självläkande och felar normalt genom att tappa kapacitans, inte genom kortslutning.
- **En polyfuse (PTC) läggs in före C3.** Den skyddar förstärkaren vid genomslag i C3 och diskanten vid extrem överbelastning. Kall resistans cirka 0,1–0,2 Ω ingår i modellen. Detta reviderar min tidigare hållning "ingen säkring", eftersom komponenten nu har en verifierbar funktion.
- L3 kontrolleras med kontinuitetstest vid bygget.

**Diskantnivån: granskaren har rätt.** Rev A:s S3 ändrar högpassets överföring: +1,7 dB vid 2,5 kHz, +0,6 vid 4 kHz och +1,5…1,9 vid 10–16 kHz. Det är ingen ren nivåkontroll. Rev B använder ett **L-pad med konstant impedans**: serie- och shuntmotstånd byts parvis med en DPDT, och ger en jämn ändring på cirka 0,8…1,6 dB från 3 kHz.

## Punkt 8 – Antal reglage

**Bedömning: tre reglage behålls, med nya roller.**

| Rev B | Band | Verkan (beräknad) |
|---|---|---|
| S1 Bas/vägg | 100–400 Hz | Fri +0,8 / Vägg −1,6 dB relativt neutral. Med väggmodell: Vägg ger +0,6 dB vid 150 Hz, alltså nästan rakt |
| S2 Närvaro | 3–5 kHz | Fram +2,5 / Mjuk −1,6 dB |
| S3 Diskantnivå | 3–20 kHz (hylla) | ±0,8…2 dB |

- Rev A:s "kropp"-kontroll vid 0,7–2 kHz utgår. Den var den minst efterfrågade och överlappade S1:s verkan på tonbalansen.
- **Billigare S1:** eftersom dina högtalare sitter på vägg räcker en tvålägesomkopplare (SPDT ON-ON: Vägg/Neutral). Vill du spara mer kan den ersättas av en bygel.

## Punkt 9 – Kostnad

**Bedömning: håller med om inriktningen.** Rev B är ungefär lika komplex som rev A:

- **Tas bort:** W2-trapen (Lt, Ct, Rta, Rtb och en omkopplare).
- **Läggs till:** närvaronotch (Ln, Cn, Rn), fast trap vid 13 kHz (Lh, Ch, Rh), två shuntmotstånd och en polyfuse.

**Besparingar:**
1. Kravet på avstängd förstärkare vid omkoppling gör att billigare omkopplare räcker.
2. S1 som tvålägesomkopplare.
3. Kärnspolar på L2 och Ln.
4. 5 W-motstånd utom i Rs-kedjan.

Uppskattning cirka 1 300–1 900 kr för paret. Det är **ej verifierat**, och en ny BOM tas fram i rev B.

## Punkt 10 – Strategi

| | A. Rekonstruerat original + justeringar | B. Rev A (helt ny 2,5-väg) | **C. Hybrid (rekommenderas)** |
|---|---|---|---|
| Basgrenar | Originalets | Nya | **Originalets topologi och värden** om de visar sig rimliga, annars rev B:s |
| Diskantgren | Originalets + tillägg | Ny | **Rev B:s:** C–L–C-högpass, närvaronotch, L-pad med konstant impedans, trap vid 13 kHz, polyfuse |
| S1 vägg | Kan läggas till som seriemotstånd i originalets nedre basgren | Ja | Ja |
| Last och impedans | Känd god (B&O) | Ny risk | Bas: känd god. Diskantgren: verifierad i modell |
| Kan bedömas nu | Nej, schema saknas | Ja | Efter foton |

**Motivering för C:**
- Det mesta av det du efterfrågar (närvaro, diskant, väggbalans) ligger i diskantgrenen och i nedre basens nivå.
- B&O:s basgrenar är sannolikt redan 2,5-väg och har en impedans som fungerat med vanliga förstärkare i 30 år.
- Att behålla dem minskar både risk och antal nya komponenter. Om simuleringen av originalet visar svagheter i basgrenarna byter vi dem mot rev B:s.

## Punkt 11 – Vad kräver vilken mätning?

| Nivå | Vad vi kan göra | Vad den eliminerar | Värde för första prototypen |
|---|---|---|---|
| Ingen mätning (nu) | Topologi, preliminära värden, alla reglage, säkerhetsprinciper | – | Räcker för att planera, inte för att beställa |
| **Foton av originalkortet** | Rekonstruera och simulera originalet. Beslutet A/B/C | Den största strategiska osäkerheten | **Mycket högt** |
| **Re (multimeter)** | 2,5-väg parallell eller serie. Grov Zmin | Arkitekturvalet | **Mycket högt**, 5 minuter |
| **Djupmått med linjal** | Riktning på diskantens tidsförskjutning | Om summan kring 2,5 kHz är robust | Högt, 2 minuter |
| **Impedanskurva** (REW + USB-ljudkort cirka 300 kr + motstånd) | Le, fs, lådans resonanser. Verklig Zmin och EPDR, Zobel | Lastrisken och värdenas noggrannhet | **Högt.** Krävs före beställning |
| Akustisk mätning (mätmikrofon cirka 1 200 kr) | Verifierar summan, polariteten och originalets faktiska kurva | Modellfelet (±1,5–3 dB) | Medel för prototyp 1. Lyssning och de elektriska kontrollerna räcker för att börja |

---

## Ytterligare svagheter som varken granskaren eller jag uppmärksammat tidigare

1. **L1:s likströmsresistans var felmodellerad.** Verklig Zmin för rev A är cirka 3,34 Ω, inte 3,64 Ω (punkt 3).
2. **En kortsluten C3 lägger cirka 0,3 Ω över förstärkaren** (punkt 7). Åtgärdas med MKP och polyfuse.
3. **S1 i rev A hade för litet omfång** (±0,9 dB) i förhållande till väggens effekt (+3…5 dB) (punkt 6).
4. **Rev A lämnade diskantens topp vid 12,5 kHz okorrigerad.** S3 + gav +5,5 dB där, alltså risk för vasshet, raka motsatsen till vad du bad om. B&O sänker den med 4,8 dB. Rev B har en fast trap.
5. **B&O:s data använder samma mätning för båda baselementen.** Det nedre elementets verkliga respons, med annan placering och diffraktion, är okänd.
6. **B&O:s mätaxel och mätavstånd är okända.** Summan gäller "B&O:s axel", sannolikt diskantaxeln.
7. **Basmodellen har en enda resonans.** En basreflexlåda har två impedanstoppar, så EPDR i basen är osäker tills impedansen är mätt.
8. **Lampan eller PTC:n i originalet är fortfarande obekräftad.** Den ska identifieras på kortet.

---

## A. Teknisk replik

- **Korrekt kritik:**
  - Klassificeringen av originalet (punkt 2).
  - Att |Z| inte räcker och att modellen behöver toleranser (punkt 3).
  - Att argumentet om nollfördröjning var svagt (punkt 4).
  - **Närvarokontrollen låg i fel band** (punkt 5).
  - Att 450 Hz saknade motivering (punkt 6).
  - **Att S3 inte var en ren nivåkontroll** (punkt 7).
- **Delvis överdriven:**
  - Oron för minimumfas är rimlig i princip, men känslighetsanalysen visar att summan håller inom −20…+10 mm.
  - Oron för kontaktfel: alla kontaktkombinationer är nu verifierat ofarliga.
  - Oron för impedansen: rev A och rev B är normala 4 Ω-laster enligt IEC:s 80 %-regel och i nivå med en uppmätt systermodell, inte aggressiva konstruktioner.
- **Felaktigt eller missförstånd:** inget väsentligt. Granskarens "4 Ω-gräns" för SU-V505 gäller nominell impedans, inte minimum. Det stärker slutsatsen att lasten är normal snarare än att den är för låg.

## B. Uppdaterad rekommendation

**Arkitekturen behålls i grunden. Reglagen och diskantgrenen ändras. Strategin blir C (hybrid).**

- S2 flyttas till 3–5 kHz som shuntnotch över diskanten.
- S3 blir ett L-pad med konstant impedans.
- S1 får större omfång (1 / 3,3 / 10 Ω) och kan förenklas till två lägen.
- Fast trap vid cirka 13 kHz, polyfuse före C3 och MKP i C3.
- W2-trapen utgår.
- Basgrenarna tas från originalet om simuleringen av originalet visar att de är bra. Annars används rev B:s.

Rev B-kandidatens värden finns i `sim/revB_candidate.py` och verkan i `plots/07_revB_switches.png`. **Värdena är preliminära, med antagen impedans.**

## C. Prioriterad plan för rev B

| # | Uppgift | Vem | Blockerar beställning? |
|---|---|---|---|
| 1 | Foton av originalkortet (båda sidor) och elementens märkning | **Du** | Ja |
| 2 | Re för alla tre element, och djupmått kalott/dammkåpa | **Du** | Ja |
| 3 | Rekonstruera originalschemat och simulera originalet med B&O-data. Beslut om basgrenarna (strategi C) | Jag | Ja |
| 4 | Impedanskurva per element (REW + USB-ljudkort). Jag skriver en steg-för-steg-instruktion | Du (jag instruerar) | **Ja** |
| 5 | Uppdatera modellen med uppmätta data: Monte Carlo för Zmin och EPDR, krav Zmin ≥ 3,2 Ω och EPDR ≥ 1,7 Ω | Jag | Ja |
| 6 | Slutliga värden, schema med omkopplarnas kontaktbild, BOM med artikelnummer | Jag | Ja |
| 7 | Bekräfta omkopplarnas kontaktbild (multimeter) när de anlänt | Du | Nej, vid bygget |
| 8 | Bygga, köra de elektriska kontrollerna (rapportens avsnitt G, kompletterat med C3- och L3-kontroll), lyssna | Du | – |

Det jag kan göra direkt utan mer information är redan gjort: analyserna och rev B-kandidaten ovan. Allt annat väntar på punkterna 1, 2 och 4.
