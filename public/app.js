/**
 * StrollerPulse Main Application Controller (app.js)
 * Coordinates SensorEngine, AudioCoach, MapVisualizer, and TabPFN Backend API.
 */

document.addEventListener('DOMContentLoaded', () => {
  // DOM Elements
  const heroCard = document.getElementById('heroStatusCard');
  const terrainHeading = document.getElementById('terrainHeading');
  const terrainDescription = document.getElementById('terrainDescription');
  const terrainBadge = document.getElementById('terrainBadge');
  const modelTagBadge = document.getElementById('modelTagBadge');

  const grassPercentText = document.getElementById('grassPercentText');
  const grassProgressBar = document.getElementById('grassProgressBar');
  const shockHazardText = document.getElementById('shockHazardText');
  const shockProgressBar = document.getElementById('shockProgressBar');

  const audioSpeechText = document.getElementById('audioSpeechText');
  const replayVoiceBtn = document.getElementById('replayVoiceBtn');
  const outdoorModeBtn = document.getElementById('outdoorModeBtn');

  const metricRMS = document.getElementById('metricRMS');
  const metricPeak = document.getElementById('metricPeak');
  const metricCrest = document.getElementById('metricCrest');
  const metricFreq = document.getElementById('metricFreq');
  const metricLatency = document.getElementById('metricLatency');

  const routeDistanceText = document.getElementById('routeDistanceText');
  const cushionScoreSummary = document.getElementById('cushionScoreSummary');

  const modeStroller = document.getElementById('modeStroller');
  const modeRunner = document.getElementById('modeRunner');

  const openBenchmarkBtn = document.getElementById('openBenchmarkBtn');
  const closeBenchmarkBtn = document.getElementById('closeBenchmarkBtn');
  const rerunBenchmarkBtn = document.getElementById('rerunBenchmarkBtn');
  const benchmarkModal = document.getElementById('benchmarkModal');
  const benchmarkTableContainer = document.getElementById('benchmarkTableContainer');

  const enableMobileSensorBtn = document.getElementById('enableMobileSensorBtn');
  const simBtns = document.querySelectorAll('.sim-btn');

  // Core State
  let currentMode = 'stroller'; // 'stroller' or 'runner'
  let latestAudioText = "Natural grass trail detected. Chassis vibration down 44%. Enjoy the cushioned earth.";

  // Initialize Subsystems
  const audioCoach = new window.AudioCoach();
  const mapVis = new window.MapVisualizer('mapContainer');
  const sensorEngine = new window.SensorEngine('waveformCanvas');

  // Connect Sensor Window Ingestion to TabPFN Backend
  sensorEngine.onWindowReady(async (accelZBuffer, speedMps) => {
    try {
      const response = await fetch('/api/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          accel_z: accelZBuffer,
          speed_mps: speedMps,
          mode: currentMode,
          apply_cadence_decoupling: true
        })
      });

      if (!response.ok) return;
      const data = await response.json();
      updateDashboard(data, speedMps);
    } catch (err) {
      console.error('Inference error:', err);
    }
  });

  // Start with default Grass Profile in simulator
  sensorEngine.setSimulationProfile('grass');

  // Update UI with TabPFN prediction
  function updateDashboard(data, speedMps) {
    const pClass = data.predicted_class;
    const hazard = data.hazard_score || 0;
    const metrics = data.metrics || {};

    // 1. Terrain Hero Card
    terrainHeading.textContent = data.class_name;
    terrainDescription.textContent = data.description;
    terrainBadge.textContent = data.badge;

    // Badge color
    terrainBadge.className = 'badge-pill';
    if (pClass === 0) terrainBadge.classList.add('emerald-badge');
    else if (pClass === 1) terrainBadge.classList.add('amber-badge');
    else terrainBadge.classList.add('rose-badge');

    // Hazard card glow
    if (pClass === 2 && hazard > 45) {
      heroCard.classList.add('hazard-active');
    } else {
      heroCard.classList.remove('hazard-active');
    }

    if (data.model_type) {
      modelTagBadge.innerHTML = `<span class="dot"></span> ${data.model_type}`;
    }

    // 2. G-Shock Hazard Level
    shockHazardText.textContent = `${hazard.toFixed(0)} / 100`;
    shockProgressBar.style.width = `${Math.min(100, Math.max(5, hazard))}%`;

    shockHazardText.className = '';
    shockProgressBar.className = 'progress-bar-fill';
    if (hazard < 28) {
      shockHazardText.classList.add('emerald-text');
      shockProgressBar.classList.add('emerald-fill');
    } else if (hazard < 55) {
      shockHazardText.classList.add('amber-text');
      shockProgressBar.classList.add('amber-fill');
    } else {
      shockHazardText.classList.add('rose-text');
      shockProgressBar.classList.add('rose-fill');
    }

    // 3. Audio Coach
    if (data.audio_cue) {
      latestAudioText = data.audio_cue;
      audioSpeechText.textContent = data.audio_cue;
      audioCoach.handlePrediction(data);
    }

    // 4. Kinematics Telemetry
    if (metrics.rms_z !== undefined) metricRMS.textContent = `${metrics.rms_z.toFixed(2)}g`;
    if (metrics.peak_g !== undefined) metricPeak.textContent = `${metrics.peak_g.toFixed(2)}g`;
    if (metrics.crest_factor !== undefined) metricCrest.textContent = `${metrics.crest_factor.toFixed(1)}x`;
    if (metrics.dom_freq !== undefined) metricFreq.textContent = `${metrics.dom_freq.toFixed(1)} Hz`;
    if (data.latency_ms !== undefined) metricLatency.textContent = `${data.latency_ms.toFixed(2)} ms`;

    // 5. Dynamic Map Step & Grass Index Update
    mapVis.addStep(pClass, speedMps);
    const mapMetrics = mapVis.getMetrics();

    grassPercentText.textContent = `${mapMetrics.grassPercent}%`;
    grassProgressBar.style.width = `${mapMetrics.grassPercent}%`;
    routeDistanceText.textContent = `Route Distance: ${mapMetrics.totalDistanceKm} km`;
    cushionScoreSummary.innerHTML = `Cushion Index: <strong>${mapMetrics.cushionGrade}</strong>`;
  }

  // Simulator Buttons
  simBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      simBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const profileId = btn.dataset.profile;
      sensorEngine.setSimulationProfile(profileId);
    });
  });

  // Mobile Accelerometer Sensor Request
  enableMobileSensorBtn.addEventListener('click', async () => {
    const res = await sensorEngine.requestMobileSensor();
    if (res.success) {
      enableMobileSensorBtn.textContent = '✅ Accelerometer Active';
      enableMobileSensorBtn.style.background = '#059669';
      simBtns.forEach(b => b.classList.remove('active'));
    } else {
      alert(res.message);
    }
  });

  // Personality Modes (Stroller vs Runner)
  modeStroller.addEventListener('click', () => {
    modeStroller.classList.add('active');
    modeStroller.setAttribute('aria-selected', 'true');
    modeRunner.classList.remove('active');
    modeRunner.setAttribute('aria-selected', 'false');
    currentMode = 'stroller';
    audioCoach.setMode('stroller');
  });

  modeRunner.addEventListener('click', () => {
    modeRunner.classList.add('active');
    modeRunner.setAttribute('aria-selected', 'true');
    modeStroller.classList.remove('active');
    modeStroller.setAttribute('aria-selected', 'false');
    currentMode = 'runner';
    audioCoach.setMode('runner');
  });

  // Replay Audio Voice Button
  replayVoiceBtn.addEventListener('click', () => {
    audioCoach.speak(latestAudioText, true);
  });

  // Outdoor Sunlight High-Contrast Mode Toggle
  outdoorModeBtn.addEventListener('click', () => {
    document.body.classList.toggle('outdoor-mode');
    const isOutdoor = document.body.classList.contains('outdoor-mode');
    outdoorModeBtn.querySelector('.btn-text').textContent = isOutdoor ? 'Dark Mode' : 'Sunlight Mode';
    outdoorModeBtn.querySelector('.btn-icon').textContent = isOutdoor ? '🌙' : '☀️';
  });

  // Benchmark Modal Handlers
  openBenchmarkBtn.addEventListener('click', () => {
    benchmarkModal.classList.remove('hidden');
    benchmarkModal.setAttribute('aria-hidden', 'false');
    loadBenchmarkTable();
  });

  closeBenchmarkBtn.addEventListener('click', () => {
    benchmarkModal.classList.add('hidden');
    benchmarkModal.setAttribute('aria-hidden', 'true');
  });

  rerunBenchmarkBtn.addEventListener('click', () => {
    loadBenchmarkTable();
  });

  async function loadBenchmarkTable() {
    benchmarkTableContainer.innerHTML = '<div style="padding: 2rem; text-align: center; color: var(--emerald-400);">Running live benchmark on Prior Labs TabPFN & baselines...</div>';
    try {
      const res = await fetch('/api/benchmark');
      if (!res.ok) throw new Error('Benchmark fetch failed');
      const data = await res.json();

      let tableHtml = `
        <table class="benchmark-table">
          <thead>
            <tr>
              <th>Model / Architecture</th>
              <th>Overall Accuracy</th>
              <th>Shock Recall</th>
              <th>CPU Latency</th>
              <th>Cadence False Alarm</th>
              <th>Tuning Required</th>
            </tr>
          </thead>
          <tbody>
      `;

      data.results.forEach(row => {
        const isHighlight = row.foundation_model ? 'class="highlight-row"' : '';
        tableHtml += `
          <tr ${isHighlight}>
            <td><strong>${row.classifier}</strong></td>
            <td><strong>${row.accuracy_pct}%</strong></td>
            <td><strong>${row.hazard_recall_pct}%</strong></td>
            <td><strong>${row.cpu_latency_ms} ms</strong></td>
            <td>${row.cadence_false_alarm_pct}%</td>
            <td><small>${row.tuning_required}</small></td>
          </tr>
        `;
      });

      tableHtml += `</tbody></table>`;
      benchmarkTableContainer.innerHTML = tableHtml;
    } catch (e) {
      benchmarkTableContainer.innerHTML = `<div style="color: var(--rose-400); padding: 1rem;">Failed to load benchmark: ${e.message}</div>`;
    }
  }
});
