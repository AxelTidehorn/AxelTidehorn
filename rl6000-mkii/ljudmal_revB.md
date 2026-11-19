# Ljudmål och konstruktionsprioriteringar inför rev B

**RL6000 MkII · 2026-11-19 · svar på "Förtydligande av ljudideal och konstruktionsmål"**

**Märkning:**
- **[V]** verifierat ur källa
- **[S]** simulerat eller beräknat i modell
- **[F]** förväntan eller erfarenhet, inte belagt för just RL6000.

Simuleringarna kan reproduceras med `cd sim && python3 imaging_analysis.py`, som ger figur 09–11 och tabellerna nedan.

---

## Sammanfattning – min självständiga bedömning

1. **Dina ljudmål ändrar prioriteringen mer än topologin.** Rev A/B optimerades mot rak frekvensgång på axeln. För ljudbild och separation är **elementintegrationen vid delningen viktigare**: fasföljd, symmetrisk lobing och en stabil delningspunkt. Den var medelmåttig i rev B [S].
2. **Ett fasoptimerat grundfilter (B2) blir nytt utgångsläge** [S]. Jämfört med rev B:
    - Fasskillnaden mellan övre bas och diskant minskar från +21…+73° till −25…+38°.
    - Lobingen vid ±15° blir symmetrisk (−7 / −6 dB i stället för −21 / −7 dB).
    - Delningen ligger stilla vid cirka 2,1 kHz i alla närvarolägen. I rev B vandrade den mellan 2,6 och 3,0 kHz.
    - Priset är cirka 0,3 Ω lägre minimiimpedans i diskantområdet, där musiken innehåller lite effekt. Diskanten arbetar också närmare sin resonans (1,5 kHz).
3. **Närvaro och djup drar delvis åt olika håll** [F]. En tydlig höjning vid 2–5 kHz flyttar fram ljudbilden och kan minska upplevt djup. Det är skälet till att BBC i decennier använde en lätt *sänkning* i det området. Därför bör närvaroreglagets neutralläge vara rakt, och "Fram" bör vara en smakkrydda, inte grundinställningen.
4. **Mycket av det du saknar i ljudbilden ligger utanför filtret** [F]: placering, inåtvinkling, tidiga reflexer, frontduken och väggmonteringen. Flera av de åtgärderna är gratis eller billiga och troligen större än filtrets bidrag till djup och rymd.
5. **Originalschemat finns sannolikt** [V]. En **servicemanual för typ 6522 (= RL6000, 18 sidor)** finns listad på ManualsLib och manuals-in-pdf. Servicemanualen för RL60.2 finns på bland annat beomanuals.com. Jag kommer inte åt någon av dem från den här miljön. Om du laddar ner och laddar upp dem kan jag läsa dem direkt.
6. **Ambitionen att matcha nya högtalare för 8 000–10 000 kr:** sannolikt konkurrenskraftigt i tonbalans, fyllighet och integration, men troligen inte i diskantens jämnhet, spridning och distorsion [F]. De begränsningarna ligger i elementen och lådan, inte i filtret.

---

## 1. Originalschemat – resultat av nytt sök

| Fynd | Källa | Status |
|---|---|---|
| **Bang & Olufsen 6522 Service Manual, 18 sidor** | [ManualsLib – 6522](https://www.manualslib.com/products/Bang-And-Olufsen-6522-14009400.html), [manuals-in-pdf](https://www.manuals-in-pdf.com/plist-236-821.html) | [V] listad. Innehållet går inte att läsa härifrån |
| Typ 6522 = Beovox RL 6000. Ersatte RL60.2 med "very similar technology in new colours" | [Beocentral](https://beocentral.com/beovoxrl6000) | [V] |
| Supplement till servicemanualen för typ 6520–6523 (Redline-serien) | [AnalogAlley](https://www.analogalley.com/m_bando.htm) | [V] listad. Vilka modellnamn som ingår är oklart i utdraget |
| Servicemanual för RL60.2, 12 sidor, med delningsfilterschema | [beomanuals.com](https://beomanuals.com/manuals/Beovox/Beovox%20RL60/), [manualmachine](https://manualmachine.com/bangolufsen/beovoxrl602/8549274-service-manual/) | [V] listad |
| RL60.2: delning vid **350 Hz** (Beoworld) och **2 500 Hz** (Beo.zone) | [Beoworld](https://beoworld.org/beovox-rl-60-2/), [beo.zone](https://beo.zone/en/beovox-rl-60-passive-loudspeakers/) | [V]. Bekräftar 2,5-väg: nedre basen ut vid cirka 350 Hz |
| RL60.2-element: 2 × **LPT 130/25/120 FG** (8 Ω), diskant **Vifa D26TG-05** (6 Ω) | [HomeTheaterShack](https://www.hometheatershack.com/threads/bo-rl-60-2-crossover.74343/) | [V] för RL60.2 |
| Diskantsektionen i ett RL60.2-exemplar avvek från servicemanualen. Bas- och mellansektionerna stämde | samma tråd | [V]. **Filterrevisioner förekom: kontrollera alltid mot kortet** |
| LPT 130/25/120: Re cirka 7,2 Ω | [EdsGoodStuff](https://edsgoodstuff.com/edscart/index.php?main_page=product_info&products_id=2784), uppmätt av säljare | [V] som andrahandsuppgift |
| Vifa D26TG-05-06: Zn 6 Ω, Re 4,6 Ω, fs 1 500 Hz, 92 dB, Bl 3,3 Tm, Mms 0,27 g | [Datablad (Madisound)](https://madisound.com/pdf/vifa/d26tg-05-06e.pdf) | [V] |

**Konsekvenser:**
- Om RL6000 har samma element som RL60.2, vilket är sannolikt men obekräftat, är baselementen 8 Ω. Då håller 2,5-vägsarkitekturen med god marginal.
- Den antagna elementmodellen ersätts nu med RL60.2-data. Lasten i basområdet blir minst cirka 4,0 Ω och EPDR cirka 2,1 Ω, nära RL60.2:s uppmätta 2,3 Ω [S].

**Det behöver jag:** servicemanualen för 6522 som PDF, och gärna den för RL60.2 för jämförelse. Ladda ner och ladda upp dem här. Med schemat kan jag simulera originalet med B&O:s mätdata. Det ger det kvantitativa svaret på hur mycket bättre MkII faktiskt kan bli.

---

## 2. Ljudbild: vad påverkar filtret, och vad inte?

| Egenskap | Påverkas av filtret? | Mekanism | Stöd |
|---|---|---|---|
| **Precision och fokus** (stabil placering av röster) | **Ja, delvis** | Fasföljd vid delningen ger symmetrisk lobing, så att höger och vänster låter lika även lite utanför axeln. Det kräver också **parmatchning**. | [S] figur 09 och 11 |
| **Separation och klarhet i mellanregistret** | **Ja** | Mindre överskott av lägre bas och mellanbas vid väggmontering minskar maskering (S1). Jämn övergång 1,5–4 kHz utan resonanser. | [S] |
| **Diskantens klarhet utan falsk detalj** | **Delvis** | Toppen vid 12,5 kHz kan sänkas (fast trap). Dippen vid 6,5–7 kHz finns i elementet och kan inte fyllas passivt. | [S]/[V] B&O-data |
| **Djup** | **Lite** | Djup kommer främst från inspelningen, rummets reflexer och låg distorsion. Filtret kan *förstöra* djup (för mycket närvaro, ojämn spridning) mer än skapa det. | [F] |
| **Rymd och bredd** | **Lite** | Styrs av spridning, sidoreflexer och placering. Filtret påverkar spridningen bara kring delningen. | [F]/[S] figur 10 |
| **Mellanbasens artikulation** | **Delvis** | Basbalansen ja (S1). Lådans resonanser, porten, distorsion och rummets moder nej. | [F] |
| **Transparens** ("högtalarna försvinner") | **Delvis** | Jämn spridning, inga resonanser, god parmatchning. Lådans resonanser och diffraktion från frontduk och kanter ligger utanför filtret. | [F] |

### Simuleringsresultat [S] – RL60.2-elementdata, alla resultat beräknade

**Fasföljd och delning:**

| | Delning | Fasskillnad W2–diskant 1,8–3,5 kHz | Lobing ±15° (d = 0,15 m, antaget) | Zmin / EPDR under 1 kHz | Zmin / EPDR över 1 kHz |
|---|---|---|---|---|---|
| rev B | 2,6–3,0 kHz (vandrar med S2) | +16…+73° | −21 / −7 dB (osymmetrisk) | 4,04 / 2,11 Ω | 3,52 / 1,83 Ω |
| **B2 (fasoptimerad)** | **2,1 kHz (stabil)** | **−25…+38°** | **−7 / −6 dB (symmetrisk)** | 3,97 / 2,16 Ω | 3,16 / 1,52 Ω |

- **Spridning** (kolvmodell, figur 10): utanför axeln ligger nivån bara cirka 1–3 dB under axeln vid 30–60° kring delningen. Den 13 cm stora basen börjar få riktverkan (ka ≈ 2) vid 2–2,5 kHz, men skillnaden mot diskanten är måttlig. Den här modellen tar **inte** hänsyn till RL6000:s vinklade frontfält, där elementen kan peka åt olika håll.
- **Parmatchning** (figur 11): komponenter med ±5 % ger högst cirka 0,6 dB skillnad mellan vänster och höger vid 1–10 kHz. Med ±2 % blir det 0,2 dB. Elementens egen spridning är troligen större, men den är okänd och kan inte påverkas av filtret.

**Tolkning:**
- Fasföljden är den filteregenskap som har störst betydelse för ljudbilden, och den kan förbättras tydligt.
- Spridning och parmatchning är små bidrag från filtret.
- Lobingvinklarna gäller i det plan där övre basen och diskanten sitter bredvid varandra. Om de sitter **horisontellt** bredvid varandra påverkar det ljudbilden direkt. Om de sitter vertikalt påverkar det främst hur höjden på lyssnarpositionen spelar in. **Elementens placering och vinklar måste mätas.**

---

## 3. Svar på dina sex frågor

**1. Hur maximerar vi soundstage, imaging, djup och separation med befintliga element?**

I ordning efter trolig effekt per insats [F]:
1. **Placering och geometri.** Liksidig triangel, tydlig inåtvinkling mot lyssnaren (vinklade väggfästen), diskanterna i öronhöjd eller lutade mot den, och symmetri i rummet.
2. **Tidiga reflexer.** Absorbent eller diffusor vid sidoväggarnas spegelpunkter förbättrar fokus.
3. **Grundfiltret:** fasföljd, symmetrisk lobing, inga resonanser (B2 + trap vid 13 kHz).
4. **Basbalans för väggen (S1).** Mindre maskering av mellanregistret.
5. **Frontduken.** Tunn ram, akustiskt transparent tyg. Lyssna med och utan.
6. **Parmatchning.** Mät komponenterna och para dem. Renovera båda högtalarna identiskt.

**2. Vad påverkas av filtret, och vad inte?** Se tabellen i avsnitt 2. Kort sagt kan filtret påverka:
- integrationen
- tonbalansen och basbalansen
- resonanstoppar och närvaro.

Det kan inte påverka:
- diskantens dipp vid 6,5 kHz
- elementens distorsion och riktverkan
- lådans resonanser och diffraktion
- rummet.

**3. Hur väl stöder rev B dina mål?**
- **Bra:** S1 (väggbalans), konstant-Z-diskantnivå, trap vid 13 kHz, polyfuse.
- **Svagt:** fasföljden vid delningen, och att S2 flyttar delningspunkten (2,6–3,0 kHz). Neutralläget ligger dessutom 3–5 dB för lågt vid 3–5 kHz med RL60.2-data, alltså tillbakadraget, vilket är tvärtemot ditt mål.
- **B2 åtgärdar de tre svagheterna.**

**4. Finns det bättre topologier för dina preferenser?** Jag har övervägt tre alternativ:
- **Första ordningens filter**, som är tidsriktiga. De förkastas: diskanten (fs 1,5 kHz) tål inte en sådan delning, och lobingen blir bred.
- **Seriefilter.** Ger ingen tydlig vinst med de här elementen.
- **Passiv tidsfördröjning (allpassnät)** för att linjera de akustiska centrumen. Det är dyrt och känsligt och motiveras först om mätningen visar en stor förskjutning.

**Slutsats:** behåll 2,5-väg med akustiskt cirka LR4-liknande delning, men optimera för fasföljd.

**5. Bör prioriteringen ändras?** Ja. Ny ordning:
1. Säkerhet och last.
2. Integration och fasföljd vid delningen.
3. Jämn respons, både på axeln och i lyssningsfönstret ±15–30°.
4. Basbalans för väggen.
5. Resonansfrihet.
6. Justerbarhet.

Reglagen ska dessutom **inte få flytta delningspunkten**. B2 uppfyller det, rev B gjorde det inte.

**6. Finns ett verifierbart originalschema?** Sannolikt ja, i servicemanualen för 6522 (avsnitt 1). Den är inte verifierad av mig än.

---

## 4. Rekommenderade förändringar inför rev B

| # | Förändring | Varför | Status |
|---|---|---|---|
| 1 | **Grundfilter optimeras för fasföljd** (B2-principen, delning cirka 2,1–2,3 kHz) | Precision och lobing | [S]. Slutliga värden efter impedansmätning |
| 2 | **Delningen läggs inte under cirka 2,1 kHz** | Diskantens fs är 1,5 kHz [V]. Lägre delning ökar distorsionen och risken | Princip |
| 3 | **S2 neutralläge = rakt**, Fram = +2 dB, Mjuk = −2 dB vid 3–5 kHz. S2 får inte flytta delningen | Närvaro utan att djupet går förlorat | [S] B2 uppfyller detta |
| 4 | **S1 Vägg = standardläge** för dina väggmonterade högtalare | Mindre maskering av mellanregistret | [S] |
| 5 | Fast trap vid cirka 13 kHz behålls. **Ingen** extra diskanthöjning i neutralläget | Klarhet utan falsk detalj | [S] |
| 6 | **Parmatchade komponenter** (mät och para, ±2 %) | Precision i stereobilden | [S] |
| 7 | Frontduk med tunn, öppen ram (ditt renoveringsprojekt) | Diffraktion och transparens | [F] |
| 8 | **Vinklade väggfästen** (3D-printade eller i metall) för inåtvinkling | Troligen den största ljudbildsvinsten per krona | [F] |
| 9 | Valfritt efter mätning: passiv justering av tidsförskjutningen | Bara om förskjutningen är stor | – |

**Kostnad:** B2 ändrar mest värden, inte antalet komponenter. Uppskattningen cirka 1 300–1 900 kr står sig. Väggfästen tillkommer, men de kan 3D-printas.

---

## 5. Ambitionsnivå: kan RL6000 MkII mäta sig med nya högtalare för 8 000–10 000 kr?

| Egenskap | Bedömning [F] |
|---|---|
| Tonbalans och integration | **Konkurrenskraftig** om B2 och placeringen blir bra |
| Fyllighet och bas (2 × 13 cm, 19 liter) | **Konkurrenskraftig**, ofta bättre än kompakta stativhögtalare |
| Diskantens jämnhet och "kristallklarhet" | **Troligen sämre.** En kalott från 1990 utan vågledare, med dipp vid 6,5 kHz och topp vid 12,5 kHz [V B&O-data]. Moderna diskanter med vågledare ger jämnare spridning |
| Spridning och ljudbild utanför axeln | **Troligen sämre.** Moderna konstruktioner optimeras för jämn spridning, och det är en huvudorsak till deras ljudbild |
| Distorsion och dynamik | **Troligen sämre** vid hög volym |
| Ljudbild med god placering | **Kan bli bra**, men den största vinsten kommer från placeringen, inte från filtret |

**Ärlig slutsats:** målet är rimligt att sträva mot och kan nås i några avseenden, men sannolikt inte i alla. Projektet kan göra RL6000 klart mer engagerande och precisa än i dag. Det är fortfarande ett bra skäl att genomföra det.

---

## 6. Vad jag behöver från dig (prioriterat)

| # | Uppgift | Varför |
|---|---|---|
| 1 | **Servicemanualen för 6522 som PDF** (ManualsLib eller manuals-in-pdf), gärna även för RL60.2 | Originalschema. Avgör strategin |
| 2 | Foton: originalkortet (båda sidor), **fronten utan frontduk**, elementens märkning | Bekräftar elementtyperna och filterversionen |
| 3 | **Mått:** centrumavstånd W2–diskant och W1–W2, frontfältens vinklar, djup till kalott och dammkåpa | Lobing, spridning och tidsförskjutning |
| 4 | Lyssningsgeometri: avstånd mellan högtalarna och till lyssnaren, höjd, om högtalarna monteras liggande eller stående, möjlighet till inåtvinkling | Ljudbilden och planen för lobingen |
| 5 | Re för alla element, sedan impedanskurva (REW + USB-ljudkort) | Slutliga värden för B2 |

Det jag kan göra direkt är gjort: nytt schemasök, elementdata, B2-optimering och ljudbildsanalys. Nästa steg för mig är att simulera originalet så snart schemat finns.
