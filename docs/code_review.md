# Revisione del codice numerico

Data: 4 novembre 2026. Oggetto: `src/vlife/`, `experiments/` e `tests/`, confrontati con `docs/` e `README.md`.
Il codice di calcolo non è stato modificato. I problemi sono in ordine di gravità, dal più grave.

## Sintesi

Due problemi possono cambiare risultati dichiarati:

1. La distorsione da monitoraggio discreto delle uscite (dt = 0,05) non è uguale per tutte le strutture, come dicono i documenti. Dipende dalla velocità della struttura, sposta log V di 0,2–0,7 nell'intervallo di velocità dell'ensemble e cambia ρ(C, log V) fino a 0,14 nello stesso mondo.
2. In E4 un filtro scarta il 54 % delle coppie di fusione ammissibili, e non a caso. H4 è stata valutata su questo sottoinsieme.

Gli altri problemi sono di gravità media o bassa: un indicatore di E2 calcolato su parti reali di autovettori complessi, un controllo (H5 in S6b) che non può fallire, il controllo H3 senza numeri casuali comuni, l'uso di KSG fuori dall'intervallo validato, e alcuni difetti minori.

| N. | Gravità | Dove | Problema |
|---|---|---|---|
| 1 | Alta | `viability.simulate_exits`, `agency.simulate_exit_threshold`, LIMITATIONS §6 | Il bias da monitoraggio discreto dipende dalla struttura |
| 2 | Alta | `experiments/e4_merging.py:231` | Il filtro `min(a) > min(b)` scarta il 54 % delle coppie in modo sistematico |
| 3 | Media | `gib.tica_modes`, `gib.subspace_gap`, E2 | Il divario GIB–TICA nei mondi guidati usa parti reali di autovettori complessi |
| 4 | Media | `experiments/e11_selection.py:50`, S6.md (H5) | L'identità di Price viene "verificata" con una formula che la rende vera per costruzione |
| 5 | Media | `experiments/e3_phi_vs_viability.py:43-44` | Rapporto di flusso R senza numeri casuali comuni: il controllo H3 è debole |
| 6 | Media | `estimators.ksg_mi`, E6, E6b | KSG è validato fino a 0,22 nats in 1–3 dimensioni e usato fino a 2,7 nats in 4 dimensioni |
| 7 | Bassa | `viability.GrowthRateViability.survival`, E9 | La curva calcola P(T ≥ a), non P(T > a); con i dati float32 il criterio cambia da punto a punto |
| 8 | Bassa | `gs_opencl.py:26` | Il rumore della GPU si ripete esattamente a certi ritardi temporali |
| 9 | Bassa | `viability.mfpt_from` e copie | Con zero uscite V = esposizione; le interfacce `evaluate` non filtrano le strutture censurate |
| 10 | Bassa | `gib.gib_projection` | Divisione per zero se un autovalore λ_i = 0 |
| 11 | Bassa | E10, E11 (`growth`) | L'esponente della legge di potenza dipende dall'origine dei tempi |
| 12 | Bassa | `nonlinear.draw_units`, S2.md | v₀ non è l'ampiezza del ciclo: la velocità massima sul ciclo è 1,155 v₀ |
| 13 | Nota | vari documenti | Affermazioni superate o in contrasto tra loro |

Le verifiche numeriche sono state fatte con script brevi fuori dal repository, sugli stessi moduli di `src/vlife`. I comandi principali sono riportati nei singoli punti per poterli ripetere. La suite di test passa (34 test superati, 2 saltati perché manca la GPU).

---

## 1. Alta: il bias da monitoraggio discreto non è uguale per tutte le strutture

**Dove.** `viability.simulate_exits` (usato da E3, E4, E9 e da tutte le impostazioni S1), `agency.simulate_exit_threshold` (S3).
Documentazione: docstring di `viability.py` («The bias is systematic (same for every structure at equal dt), so rankings are affected much less»), LIMITATIONS §6 («the bias is systematic across structures»), THEORY §4.

**Che cosa succede.** L'uscita viene controllata solo ai multipli di dt = 0,05. Le escursioni fuori dall'insieme tra due controlli si perdono e V risulta più lungo. Secondo Broadie, Glasserman e Kou l'effetto equivale a spostare il bordo di 0,5826·√(2D·dt). Lo spostamento relativo al raggio dell'insieme vale circa √(2θ·dt / c_k), dove θ è la velocità di rilassamento della struttura. Quindi la distorsione cresce con θ: non è la stessa per strutture lente e veloci.

**Misura 1: OU in una dimensione** (D = 1, p_out = 0,05, dt = 0,05, 6000 traiettorie, MFPT esatto dall'equazione all'indietro di `tests/test_viability.py`):

| θ | MFPT esatto | MFPT simulato | rapporto | bias in log V |
|---|---|---|---|---|
| 0,3 | 12,07 | 15,18 | 1,26 | +0,23 |
| 1 | 3,62 | 5,52 | 1,53 | +0,42 |
| 3 | 1,21 | 2,47 | 2,04 | +0,71 |
| 9 | 0,40 | 1,35 | 3,35 | +1,21 |

Le velocità dei mondi vanno da 0,3 a 3 (`worlds._random_spd`). Nel D-test con r = 3 arrivano a circa 9. Nell'intervallo base il bias in log V cambia di circa 0,5. LIMITATIONS §11 stima la dispersione del segnale tra strutture in 0,07–0,12.

**Misura 2: mondi veri di E3** (stessi seed di E3, tutte le 62 strutture, 1500 traiettorie, t_max = 80, dt = 0,05 contro dt = 0,005):

| Mondo | bias medio in log V (min..max tra strutture) | ρ(log V a dt 0,05, log V a dt 0,005) | ρ(C, log V) a dt 0,05 | a dt 0,005 | log R medio a dt 0,05 | a dt 0,005 |
|---|---|---|---|---|---|---|
| driven #0 | +0,34 (+0,24..+0,41) | 0,927 | +0,270 | +0,132 | −0,131 | −0,162 |
| driven #1 | +0,31 (+0,23..+0,39) | 0,852 | +0,423 | +0,331 | −0,174 | −0,192 |
| modular #0 | +0,37 (+0,18..+0,45) | 0,963 | +0,647 | +0,562 | −0,069 | −0,063 |
| equilibrium #0 | +0,29 (+0,19..+0,38) | 0,984 | +0,192 | +0,250 | 0,000 | 0,000 |

**Conseguenze.**
- L'ordinamento delle strutture per V cambia (ρ tra 0,85 e 0,98 tra i due passi). La statistica principale di E3, ρ(C, log V), cambia fino a 0,14 nello stesso mondo, in entrambe le direzioni. L'affermazione «rankings are affected much less» non regge su questi mondi.
- Il segno del rapporto di flusso non cambia. A dt = 0,05 l'effetto del flusso risulta un po' più piccolo (−0,13 contro −0,16 in driven #0).
- Il D-test (S1, punto 5) cambia le velocità delle singole variabili fino a un fattore 3. Il bias segue le velocità, quindi può spiegare una parte dello spostamento di ρ(−K_H). Non l'ho misurato.
- S3 usa lo stesso dt. La versione intatta e quella scrambled hanno dinamiche di v diverse, quindi il bias non si annulla per forza in VoI = log V_intact − log V_scrambled. Non l'ho misurato.
- `tests/test_viability.py` valida il simulatore a dt = 0,01 e p_out = 0,3, con la correzione del bordo. Il test non copre l'impostazione usata negli esperimenti (dt = 0,05, p_out = 0,05, nessuna correzione).

**Correzione proposta (da decidere, non applicata).** Aggiungere la probabilità di uscita tra due passi con il ponte browniano, oppure ripetere E3 su un sottoinsieme di mondi a dt più piccolo e riportare la sensibilità. In ogni caso va corretta la frase «same for every structure» nel docstring e in LIMITATIONS §6.

**Stato:** in parte corretto, solo documentazione (fase A). Corrette la frase del docstring di `viability.py` e LIMITATIONS §6; la frase vecchia resta, segnata come superata. Non ancora corretto nel codice: il ponte browniano è previsto in fase B e la nuova run di E3 in fase C.

## 2. Alta: E4 scarta il 54 % delle coppie in modo sistematico

**Dove.** `experiments/e4_merging.py:231`:

```python
if set(a) & set(b) or len(a) + len(b) > min(5, d["B"].shape[0] - 1) or min(a) > min(b):
    continue
```

**Che cosa succede.** `itertools.combinations(subs, 2)` restituisce già ogni coppia non ordinata una sola volta. La condizione `min(a) > min(b)` quindi non elimina doppioni: scarta coppie valide. `all_subsets` ordina i sottoinsiemi per dimensione e poi in ordine lessicografico. Le coppie di sottoinsiemi della stessa dimensione passano sempre. Tra le coppie di dimensioni diverse passa solo quella in cui la parte più piccola contiene l'indice minimo.

Conteggio per mondo (script su `functional.all_subsets`):

| N | coppie ammissibili | tenute | scartate, per (|A|, |B|) |
|---|---|---|---|
| 5 | 75 | 40 | (1,2): 20, (1,3): 15 |
| 6 | 270 | 125 | (1,2): 40, (1,3): 45, (1,4): 24, (2,3): 36 |
| 7 | 686 | 301 | (1,2): 70, (1,3): 105, (1,4): 84, (2,3): 126 |

Con N = 6 restano 125 coppie per mondo: 90 × 125 = 11 250, il numero riportato in RESULTS.md come «11,250 merge pairs», come se fossero tutte.

**Perché conta.** Lo scarto dipende dall'indice delle variabili. Per esempio, il singoletto {5} non viene mai fuso con un insieme più grande. Nella famiglia `modular_driven` l'indice coincide con i blocchi (blocchi [3, 2, 1]): la variabile 5 è il blocco di dimensione 1. Il campione di E4 quindi esclude in modo sistematico alcune fusioni tra blocchi. Il verdetto su H4 (non supportata in tutte le 9 impostazioni) è stato calcolato su questo sottoinsieme. Probabilmente regge, perché I(A;B) batte ΔΦ di molto, ma non è verificato. I file `.pkl` non sono nel repository, quindi non ho potuto ripetere l'analisi.

**Correzione proposta.** Togliere `or min(a) > min(b)` e ripetere E4 e `s1_summary.py`.

**Stato:** corretto nel codice (fase B). Le coppie ora vengono da `functional.merge_pairs`, senza il filtro `min(a) > min(b)`: 270 coppie per mondo con N = 6. Test: `tests/test_merging.py` (numero di coppie, nessun doppione, nessuna coppia mancante, indipendenza dall'etichetta delle variabili). I risultati di E4 vanno rifatti: previsto in fase C.

## 3. Media: divario GIB–TICA calcolato su parti reali di autovettori complessi (E2)

**Dove.** `gib.tica_modes` usa `scipy.linalg.eig` su C_tica non simmetrica. `gib.subspace_gap` prende `np.real` dei vettori. E2 confronta i primi k modi per k = 1, 2, 3.

**Che cosa succede.** Nei mondi guidati C(τ) non è simmetrica e gli autovalori di TICA sono spesso complessi coniugati. Un modo complesso occupa un piano reale, generato da Re v e Im v. La sola parte reale è una direzione arbitraria, perché dipende dalla fase che LAPACK assegna all'autovettore. Inoltre l'ordinamento per |μ| può separare una coppia coniugata tra la posizione k e la posizione k + 1.

Misura sui 20 mondi guidati di E2 (seed 100–119): in 20 su 20 c'è almeno un autovalore complesso tra i primi tre; in 18 su 20 una coppia coniugata è spezzata a k = 1 o k = 3.

**Conseguenza.** Il divario «≈ 0,5–0,9 rad» nei mondi guidati (RESULTS.md, PROVENANCE riga 32) è in parte un artefatto di questa scelta. Per i mondi reversibili il risultato (≈ 1e-13 rad) resta valido, perché lì C è simmetrica e gli autovalori sono reali. Nota a margine: per dinamiche non reversibili le direzioni GIB coincidono con le direzioni canoniche (CCA), cioè con i vettori singolari di VAMP. Un confronto con VAMP darebbe divario zero per costruzione. Va quindi chiarito che cosa il divario dovrebbe misurare.

**Correzione proposta.** Usare la forma di Schur reale (o Re e Im insieme) e non spezzare le coppie coniugate. In alternativa, dichiarare in RESULTS che il numero dipende dalla convenzione.

**Stato:** corretto nel codice (fase B). Nuova funzione `gib.tica_subspace`: base reale da Re v e Im v, con le coppie coniugate tenute insieme (dimensione k o k + 1). `tica_modes` resta com'era. Test in `tests/test_gib.py`: la base è ortonormale e invariante per S⁻¹C_tica in tutti i 20 mondi guidati di E2 (il metodo vecchio ha un residuo mediano di 0,85) e coincide con GIB nei mondi reversibili. E2 scrive ora su `e2_gib_slowmodes_realbasis.*`. Nuova run di E2 (regole in RESULTS.md, scritte prima): nei mondi reversibili il divario resta sotto 1e-11; nei mondi guidati il divario medio passa da 0,91 / 0,54 / 0,89 a 0,62 / 0,67 / 0,72 rad (k = 1, 2, 3) ed è sopra 0,12 rad in ogni mondo. La conclusione qualitativa regge, i valori vecchi sono superati.

## 4. Media: il controllo H5 dell'identità di Price non può fallire

**Dove.** `experiments/e11_selection.py:49-51` (S6b, regola H5). Stessa costruzione per S e T in `e12_mutation.py`.

```python
wb = w.mean(); s = np.mean(w * z) / wb - z.mean(); t = np.mean(w * (zd - z)) / wb
dz = np.sum(w * zd) / np.sum(w) - z.mean()
err = max(err, abs(dz - (s + t)))
```

**Che cosa succede.** s + t = mean(w·zd)/w̄ − z̄ = Σ w·zd / Σ w − z̄ = dz per qualsiasi insieme di numeri. Il controllo misura solo l'errore di arrotondamento (1,1e-16). S6.md conclude invece: «The Price identity holds to 1e-16 in every generation, so the bookkeeping is correct». Il controllo non dice nulla sulla correttezza della contabilità (generazioni, figli, tipi).

**Correzione proposta (solo documentazione).** Riscrivere H5 come controllo aritmetico, oppure calcolare Δz̄ in modo indipendente: per esempio dalla frazione di tipo A tra tutti i figli registrati dal tracker, senza passare da w e zd.

**Stato:** solo documentazione (fase A). In S6.md una nota sotto la tabella dei risultati spiega che H5 non può fallire. La frase «so the bookkeeping is correct» resta, barrata e segnata come superata, con il testo nuovo accanto. Il codice di `e11_selection.py` non cambia: un controllo indipendente richiederebbe di rifare S6b, che qui non si può lanciare senza GPU.

## 5. Media: il rapporto di flusso non usa numeri casuali comuni; il controllo H3 è debole

**Dove.** `experiments/e3_phi_vs_viability.py:43-44`: `d_on` e `d_eq` usano lo stesso generatore in sequenza, quindi flussi casuali diversi.

**Che cosa succede.** Nella famiglia di equilibrio B_eq = D S⁻¹ coincide con B a meno di 1e-15. Con lo stesso seed per le due simulazioni log R è esattamente 0: l'ho verificato (riga «equilibrium #0» della tabella del punto 1). Con seed diversi il controllo vale +0,019 ± 0,005 nella base, cioè 3,9 errori standard. Nelle altre impostazioni va da −0,006 a +0,012. RESULTS.md lo attribuisce, senza verifica, al rumore Monte Carlo. Il rumore è l'unica spiegazione possibile, perché le due dinamiche sono identiche. Però la soglia della regola H3 (|media| < 0,05) è circa 10 errori standard: il controllo passerebbe anche con un errore sistematico di qualche percento.

Nelle famiglie guidate gli stessi numeri casuali ridurrebbero anche il rumore su R.

**Correzione proposta.** Usare lo stesso seed per `d_on` e `d_eq`, come già fa E6 per V_on e V_off. Con questa scelta il controllo H3 diventa esatto: log R = 0 nella famiglia di equilibrio.

**Stato:** corretto nel codice (fase B), come opzione `--crn` di `e3_phi_vs_viability.py` (`build_dataset(..., crn=True)`). Il valore predefinito resta quello vecchio, così i risultati vecchi restano riproducibili. Il dataset registra `crn` e `dt`. Test: `tests/test_e3_crn.py` (con `crn` il controllo di equilibrio dà V_on = V_eq esattamente). La nuova run di E3 è prevista in fase C.

## 6. Media: KSG usato fuori dall'intervallo validato

**Dove.** `estimators.ksg_mi`, usato in E6 (C = I(z_t; z_{t+1}) in 4 dimensioni, TC = I(x; v)) e in E6b.

**Che cosa succede.** E1 valida KSG su variabili gaussiane con MI esatta di 0,07 e 0,22 nats, in 1–3 dimensioni (bias ≤ 0,011 nats). In S2 la C mediana degli oscillatori è 2,71 nats, in 4 dimensioni, su una distribuzione ad anello. Per MI alte e dipendenze quasi deterministiche KSG sottostima molto e la sottostima dipende dalla forma della distribuzione (Gao, Ver Steeg e Galstyan, AISTATS 2015). Il confronto tra classi in F2 (AUC 0,00) probabilmente regge, perché il distacco è grande. I valori assoluti (2,71 contro 1,57 nats) e il confronto rocce–oscillatori in S2b (segnali di 0,01 nats, che S2.md riconosce già vicini al rumore) non sono validati.

**Correzione proposta.** Aggiungere a E1 un caso con MI di 2–3 nats in 4 dimensioni, per esempio un OU con τ piccolo, oppure riportare i valori di C di S2 come solo ordinali.

**Stato:** non ancora corretto, previsto in fase D.

## 7. Bassa: la curva di sopravvivenza di S4 è spostata di un passo, e il float32 la rende irregolare

**Dove.** `viability.GrowthRateViability.survival`; dati da `e3_phi_vs_viability.py:48` (`exit_t.astype(np.float32)`), letti da `e9_growth.py`.

**Che cosa succede.**
- Il docstring dice «fraction with exit time > a». Il codice, con `searchsorted(t, grid - 1e-9, side="right")`, conta come morti solo i tempi strettamente minori di a e restituisce P(T ≥ a). Esempio: tempi (0,05; 0,10; 0,10) danno l = (1; 1; 0,667; 0; 0) sulla griglia (0; 0,05; 0,10; 0,15; 0,20), invece di (1; 0,667; 0; 0; 0).
- E3 salva i tempi in float32. La tolleranza 1e-9 è più piccola dell'arrotondamento float32. Nel 40 % dei punti di griglia il tempo arrotondato cade sotto `grid - 1e-9` e lì la curva calcola P(T > a); negli altri calcola P(T ≥ a).

**Effetto misurato** (un mondo guidato, 62 strutture, a_m = 4,4): differenza massima tra le curve 0,026; differenza di r al massimo 1e-3. Le conclusioni di S4 non cambiano.

**Correzione proposta.** Salvare l'indice del passo (intero) invece del tempo, oppure usare una tolleranza di dt/2, e allineare il docstring.

**Stato:** corretto nel codice (fase B). `survival` ora usa una tolleranza di dt/2 e restituisce P(T > a), come dice il docstring; con il nuovo argomento `event` le traiettorie censurate restano vive a t_max (prima a t_max contavano anche le uscite all'ultimo passo). Test in `tests/test_growth.py`: esempio a mano, curve identiche per tempi float32 e float64, l(t_max) uguale alla frazione censurata. Effetto misurato su un mondo guidato (62 strutture, a_m = 4,4): r cambia al massimo di 0,0013, Spearman tra r vecchio e nuovo 0,99995. Le conclusioni di S4 non dovrebbero cambiare; E9 verrà rifatto in fase C sui dati nuovi.

## 8. Bassa: il rumore della GPU si ripete a certi ritardi temporali

**Dove.** `gs_opencl.py:26`: `uint s = h(seed ^ h(t * 2654435761U + (uint)c * 2U));`

**Che cosa succede.** La chiave interna t·K + 2c (mod 2³²) coincide per coppie diverse (t, c) quando Δt·K ≡ 2Δc (mod 2³²). K è vicino a 2³² diviso il rapporto aureo, quindi i ritardi sono numeri di Fibonacci. Sulla griglia 300 × 300 e fino a 150 000 passi ho trovato sei ritardi con collisione esatta: 10 946 passi (scostamento di 41 233 celle), 21 892, 90 152, 101 098, 112 044 e 122 990. Le corse di S6c durano 18 600–26 000 passi, quindi i primi due ritardi capitano. Il rumore in una cella al passo t è identico a quello di un'altra cella 10 946 passi dopo.

**Effetto.** Probabilmente trascurabile: il rumore (deviazione standard 5e-4) serve solo a rompere la simmetria. La descrizione «counter-based hash» fa però pensare a rumore indipendente.

**Correzione proposta.** Combinare t e c in due passaggi di hash (per esempio `h(h(t) ^ c)`) o usare un generatore a contatore come Philox.

**Stato:** corretto nel codice (fase B), con una soluzione diversa da quella proposta. Una chiave a 32 bit non può bastare: le coppie (t, c) sono circa 2³⁵, e anche `h(h(t) ^ c)` darebbe ripetizioni strutturate (a XOR fisso). Il kernel ora usa splitmix64 sulla chiave a 64 bit (t << 32 | c), che è biiettiva: due coppie diverse non danno mai lo stesso valore. La funzione è in `src/vlife/gpu_noise.py`, con un riferimento numpy. Test in `tests/test_grayscott.py`: la vecchia chiave si ripete a (t + 10946, c − 41233), la nuova no; nessun doppione su 300 000 coppie; media e deviazione standard del rumore; il kernel OpenCL (eseguito qui con pocl sulla CPU) dà lo stesso rumore del riferimento. S6b e S6c restano calcolati con l'hash vecchio: rifarli richiede il kernel (fase E).

## 9. Bassa: comportamento con zero uscite

**Dove.** `viability.mfpt_from`, e le copie in `agency.simulate_exit_threshold` e `nonlinear.exit_times*`.

Con zero uscite la funzione restituisce l'esposizione totale (`exposure / max(ev, 1)`): è un limite inferiore, non una stima. E3, E5 e E9 scartano le strutture con meno di 5 uscite, quindi gli esperimenti non ne sono toccati. `MFPTViability.evaluate` e `GrowthRateViability.evaluate` invece restituiscono questi valori senza filtro. Chi usa l'interfaccia `ViabilityMeasure` può ricevere valori censurati senza saperlo. Proposta: restituire anche il numero di uscite, oppure `nan` sotto una soglia.

**Stato:** corretto nel codice (fase B). `MFPTViability.evaluate` e `GrowthRateViability.evaluate` restituiscono `nan` sotto `min_events` uscite (predefinito 5, la stessa soglia degli esperimenti). `mfpt_from` non cambia, ma il docstring dice che con zero uscite il valore è un limite inferiore. Le copie in `agency` e `nonlinear` non cambiano: chi le usa (E5, E6, E6b) controlla già il numero di uscite. Test in `tests/test_viability.py`. Nessun risultato cambia: nessun esperimento usa `evaluate`.

## 10. Bassa: divisione per zero in `gib_projection`

`gib_projection` calcola `sqrt((beta*(1-l) - 1) / l)`. Se una direzione di X è determinata da Y, λ_i = 0 e la divisione dà infinito (verificato con Sx = I, Sxy = diag(1; 0,5)). Negli esperimenti non succede, perché c'è sempre rumore. Proposta: un controllo esplicito con un messaggio d'errore.

**Stato:** corretto nel codice (fase B). `gib_projection` solleva `ValueError` se un modo attivo ha λ ≤ 1e-12; `gib_modes` non emette più l'avviso di divisione per zero quando λ = 1 (β critico infinito, come prima). Test in `tests/test_gib.py`. Nessun risultato cambia.

## 11. Bassa: l'esponente della legge di potenza dipende dall'origine dei tempi

**Dove.** `e10_grayscott.growth`, `e11_selection.growth`.

Il fit di log N contro log t usa il tempo dall'inizio della simulazione. L'esponente di una legge N ∝ (t − t₀)^p cambia con t₀, e le prime divisioni avvengono dopo centinaia di passi. Il verdetto «polynomial, exponent 1.92, close to the area law 2» di S6b dipende quindi da una scelta non dichiarata. `e11_selection.growth` non ha neppure il controllo `N.max() < 8` di E10. Proposta: stimare t₀ nel fit o riportare la sensibilità.

**Stato:** corretto nel codice (fase B). Nuova funzione `vlife.growthlaw.growth_fits`, usata da E10 ed E11: stessa finestra e stessi R2_exp, R2_pow e power di prima (le regole preregistrate R1 e H6 non cambiano), più t₀ stimato (ricerca a griglia sul miglior R² di log N contro log(t − t₀)) e l'esponente con quel t₀, solo come descrizione. Restituisce `None` anche in E11 se la colonia non arriva a 8 macchie. Test in `tests/test_growthlaw.py`. Effetto sui risultati: non misurabile qui, perché i dati delle run di S6 e S6b (`e10_runs.pkl`, `e11_runs.pkl`) non sono nel repository. Si potrà misurare con le nuove run della fase E.

## 12. Bassa: v₀ non è l'ampiezza del ciclo dell'oscillatore

**Dove.** `nonlinear.draw_units`, S2.md (pilota 1).

Con l'attrito di Rayleigh γ = γ₀ − α + βv² e β = (α − γ₀)/v₀², il bilancio energetico su un ciclo armonico dà una velocità massima di √(4(α − γ₀)/(3β)) = (2/√3)·v₀ ≈ 1,155 v₀. v₀ è la velocità a cui l'attrito si annulla. Il codice è coerente con sé stesso, perché le condizioni iniziali vengono rilassate per 200 unità di tempo. La spiegazione del pilota in S2.md («v₀/√T ≥ 3.2») sottostima però la distanza del ciclo dal centro del 15 %. Il cambio di intervallo di v₀ resta giustificato.

**Stato:** solo documentazione (fase A). Aggiunta una nota in S2.md dopo il pilota 1 (rapporti corretti: circa 3,0 invece di 2,6 e almeno 3,7 invece di 3,2) e una riga nel docstring di `nonlinear.py`. Nessun risultato cambia.

## 13. Nota: affermazioni superate o in contrasto tra loro

- `price.py`, docstring: «In this project only the SELECTION term can be measured». S4 e S6 misurano anche il termine di trasmissione.
- PROVENANCE riga 37: `GrowthRateViability` «(stub) / not implemented». È implementata (S4, riga 51).
- LIMITATIONS §1, §2 e §9 descrivono solo mondi lineari, passivi e senza ereditarietà. S2, S3 e S6 hanno aggiunto unità non lineari, un anello d'azione e la replicazione.
- LIMITATIONS §10: «References not machine-verified». ROADMAP S0 dice che tutte le 62 voci sono state controllate su Crossref.
- LIMITATIONS §6 e il docstring di `viability.py`: vedi punto 1.
- RESULTS.md: «11,250 merge pairs» descrive il sottoinsieme del punto 2, non tutte le coppie.
- S6.md (S6b): «so the bookkeeping is correct»: vedi punto 4.
- `experiments/run_all.py`: il docstring stima 12 minuti, README e RESULTS 30 minuti (1631 s per E3).
- `e3_phi_vs_viability.py`: i valori predefiniti da riga di comando (`--n_traj 200`, `--t_max 150`) sono diversi da quelli dei documenti (600 e 200). `run_all.py` passa i valori giusti, ma chi lancia lo script a mano ottiene un'altra impostazione. È la stessa causa dell'intestazione sbagliata trovata in S0.

**Stato:** in parte corretto, solo documentazione (fase A). Corretti, con il testo vecchio segnato come superato: docstring di `price.py`, PROVENANCE riga 37, LIMITATIONS §1, §2, §9 e §10, il titolo di RESULTS.md (nota sulle 11 250 coppie), il docstring di `run_all.py`. LIMITATIONS §6 e S6.md sono trattati ai punti 1 e 4. Non ancora corretto: i valori predefiniti di `e3_phi_vs_viability.py`, perché cambiano il codice (fase B).

---

## Che cosa ho controllato e risulta corretto

- Covarianza stazionaria (equazione di Lyapunov BS + SBᵀ = 2D), covarianza ritardata e^{−Bτ}S, blocchi della covarianza congiunta.
- Formule gaussiane di entropia, MI, MI condizionata e total correlation (−½ log det R).
- Produzione di entropia tr(MᵀD⁻¹MS) con M = B − DS⁻¹: derivazione di THEORY §2 ricontrollata. Decomposizione σ_A, valida per D diagonale come dichiarato.
- Controparte di equilibrio B_eq = DS⁻¹ e trasformazione B = D(B_s + G) del D-test, che conserva il bilancio dettagliato.
- Propagatore esatto dell'OU, covarianza del rumore S − ΦSΦᵀ, soglie χ² per la palla di Mahalanobis, stimatore esposizione/uscite.
- Formule GIB di Chechik (autovettori sinistri, r_i = 1, β critico, obiettivo) e dimostrazione GIB ≡ TICA per C simmetrica (THEORY §6; manca solo una trasposta, irrilevante nel caso simmetrico).
- Implementazione KSG (algoritmo 1) e formula del bias dell'istogramma (B_x − 1)(B_y − 1)/(2n).
- Decomposizione di Price in `price.py`: esatta.
- Coda esponenziale nell'equazione di Euler–Lotka e radice con `brentq`.
- Omeostato di S3: var(h) = 1; c = 1,2816·sd(v) dà il 20 % del tempo fuori; τ_v = (B⁻¹S)_vv / S_vv.
- Bilancio energetico di S2c: γ₀(⟨v²⟩ − T) = ⟨(α − βv²)v²⟩.
- Soglie di errore di S6c: μ_c = 1 − 2^(T_A/T_B − 1) = 0,114 e (1 − T_A/T_B)/2 = 0,088.
- S5: correlazioni parziali dalla matrice di precisione. Il ramo principale di `logm` è sicuro: max |Im λ(B)|·Δ = 0,61 su 40 mondi guidati, contro un limite di π.
- Gray–Scott: condizione di stabilità del Laplaciano esplicito (D_u·dt = 0,16 ≤ 0,25); `label_periodic`; coerenza tra le versioni numpy, numba e OpenCL (test con tolleranza 1e-10).
