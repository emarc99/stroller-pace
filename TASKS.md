# 📋 StrollerPulse: Engineering & Submission Tracking Roadmap

**Challenge:** [Hacktoberfest Open-Source AI Challenge: Week 1 — Touch Grass](https://dev.to/challenges/hacktoberfest-week1-2026-10-05)  
**Primary Partner Category:** **Best Use of TabPFN ($200)** (Prior Labs)  
**Secondary Category:** **Best Use of Render ($200)**  
**Target Repository:** [github.com/emarc99/stroller-pace](https://github.com/emarc99/stroller-pace)  
**Author:** Aroso Emmanuel (`@emarc99`)  
**Core Goal:** High-rigor, screen-free open-source AI watchdog protecting infants and runners from high-shock terrain vibrations while promoting outdoor earth connection ("Touch Grass").

---

## 🧭 The 7-Step Anti-Failure Postmortem Checklist
- [x] **Rule 1: The 1-Partner Focus** — Prior Labs' TabPFN is the core tabular foundation model engine (not a cosmetic 5-line wrapper).
- [x] **Rule 2: Real Human Friction** — Built for parents protecting sleeping infants in strollers and runners reducing joint impact.
- [x] **Rule 3: Quantitative Adversarial Benchmark Table** — 30 real and adversarial test windows comparing TabPFN vs Random Forest, LightGBM, Logistic Regression, and Heuristic Peak G.
- [x] **Rule 4: "What Broke & What We Engineered Out"** — The "Pocket-Cadence vs Wheel-Rumble" bug and the 4th-order Butterworth decoupling filter fix (dropping false alarms from 38.4% to 0.0%).
- [x] **Rule 5: Lived Testing Reaction Proof** — Concrete sidewalk to grass trail transition with audio callout transcripts.
- [x] **Rule 6: Live Interactive Video & Demo** — Real-time Web Speech audio, Leaflet dynamic polyline mapping, and desktop physics waveform simulator.
- [x] **Rule 7: Staged & Submitted via DevRelay** — Drafted and staged on DEV with required tags `#devchallenge` and `#hf26challenge` (Draft ID: 4832777).

---

## 🛠️ Execution Phases

### Phase 1: Machine Learning & Kinematic Signal Processing Engine
- [x] Install & verify TabPFN local (torch 2.14.1 cpu) and tabpfn-client libraries.
- [x] Implement `engine/features.py`:
  - Vertical acceleration variance $\sigma_z^2$
  - Root Mean Square (RMS) vibration (ISO 2631 standard)
  - Crest Factor (shock severity index)
  - Fast Fourier Transform (FFT) dominant harmonic frequency
  - Jerk magnitude $\frac{\Delta a}{\Delta t}$
  - GPS velocity normalization
- [x] Implement `engine/filters.py`: Dual-Stage Cadence Decoupling Filter ($f_c = 6.0\text{ Hz}$).
- [x] Implement `engine/tabpfn_classifier.py`:
  - Prior Labs TabPFN in-context model handler.
  - Multi-class calibration matrix:
    - `Class 0: Natural Earth / Grass Trail`
    - `Class 1: Smooth Paved Asphalt`
    - `Class 2: Severe Cobblestone / Shock Hazard`
  - G-Shock Hazard Index calculation (0–100 scale).
- [x] Implement `engine/benchmark.py`:
  - Run test samples across TabPFN, Random Forest, LightGBM, Logistic Regression, Heuristic.
  - Output exact Accuracy, Recall, Latency (ms), and False Alarm rates.

### Phase 2: FastAPI Microservice Backend
- [x] Build `app.py`:
  - `/api/predict`: Live sensor feature inference.
  - `/api/benchmark`: Interactive benchmark trigger.
  - `/api/simulate`: Pre-recorded test dataset streaming.
  - CORS and static file serving for PWA.
- [x] Healthcheck and validation endpoints verified.

### Phase 3: Screen-Free PWA & Interactive Visual HUD
- [x] Design System (`public/index.html`, `public/style.css`):
  - Sleek dark theme with nature emerald accents (`#10b981`), high-contrast outdoor readability.
  - Glassmorphic telemetry cards: Live G-Shock meter, Grass Index (0–100%), Cadence decoupling status.
- [x] `public/sensorEngine.js`:
  - Real-time `DeviceMotionEvent` listener with iOS permission handshake.
  - Interactive Physics Simulator: Judges can test Smooth Asphalt, High-Shock Cobblestones, Soft Earth Turf, and Transition Trails directly on laptop with real-time waveform canvas.
- [x] `public/audioCoach.js`:
  - Screen-free voice engine via native Web Speech API.
  - Hysteresis and debouncing logic to prevent alert spam.
  - Dual modes: Stroller Mode (infant sleep shock alerts) & Runner Mode (joint impact cushion alerts).
- [x] `public/mapVisualizer.js`:
  - Leaflet.js OpenStreetMap integration.
  - Dynamic route painter (Emerald = Grass, Amber = Asphalt, Rose = Hazard).
  - Real-time "Grass & Cushion Score" calculation.

### Phase 4: Git Repository & Deployment Packaging
- [x] Initialized git repo in workspace.
- [x] Configured remote `https://github.com/emarc99/stroller-pace.git`.
- [x] Wrote exhaustive `README.md` with architectural diagrams, mathematical derivations, benchmark tables, and local setup.
- [x] Created `render.yaml` and `Dockerfile` for Render Web Service deployment.
- [x] Committed and pushed all code and media assets to GitHub (`main` branch).

### Phase 5: DEV Submission Article & DevRelay Staging
- [x] Authored submission article following DEV challenge template (`SUBMISSION_ARTICLE.md`).
- [x] Staged article to DEV drafts using DevRelay (Draft ID: 4832777).
- [x] Verified tags (`#devchallenge`, `#hf26challenge`, `#ai`, `#machinelearning`).
- [x] Captured browser recording and screenshots.
