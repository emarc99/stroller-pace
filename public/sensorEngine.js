/**
 * StrollerPulse Sensor Engine (sensorEngine.js)
 * Manages raw accelerometer ingestion via DeviceMotionEvent API
 * and provides physics-based signal synthesis for desktop evaluation.
 */

class SensorEngine {
  constructor(canvasId) {
    this.canvas = document.getElementById(canvasId);
    this.ctx = this.canvas ? this.canvas.getContext('2d') : null;
    this.bufferSize = 100; // 2.0 seconds at 50 Hz
    this.accelZBuffer = new Array(this.bufferSize).fill(1.0); // 1.0g baseline
    this.samplingRate = 50.0;
    this.isMobileActive = false;
    this.activeProfile = 'grass';
    this.speedMps = 1.4;
    this.simTimer = null;
    this.simIndex = 0;
    this.cachedProfileData = null;
    this.onWindowCallback = null;

    this.startRenderingLoop();
  }

  // Set callback for when a rolling window of 100 samples is ready
  onWindowReady(callback) {
    this.onWindowCallback = callback;
  }

  // Request Mobile Permissions (required for iOS Safari 13+)
  async requestMobileSensor() {
    if (typeof DeviceMotionEvent !== 'undefined' && typeof DeviceMotionEvent.requestPermission === 'function') {
      try {
        const state = await DeviceMotionEvent.requestPermission();
        if (state === 'granted') {
          this.attachDeviceMotionListener();
          return { success: true, message: 'Motion sensor granted' };
        } else {
          return { success: false, message: 'Motion permission denied by user' };
        }
      } catch (err) {
        return { success: false, message: err.message };
      }
    } else if ('ondevicemotion' in window) {
      this.attachDeviceMotionListener();
      return { success: true, message: 'Device motion supported natively' };
    } else {
      return { success: false, message: 'DeviceMotionEvent not available on this device' };
    }
  }

  attachDeviceMotionListener() {
    this.stopSimulator();
    this.isMobileActive = true;
    window.addEventListener('devicemotion', (e) => {
      let z = 1.0;
      if (e.accelerationIncludingGravity && e.accelerationIncludingGravity.z !== null) {
        // Convert m/s^2 to g
        z = e.accelerationIncludingGravity.z / 9.81;
      } else if (e.acceleration && e.acceleration.z !== null) {
        z = 1.0 + (e.acceleration.z / 9.81);
      }
      this.pushSample(z);
    });

    // Fire window callback periodically
    setInterval(() => {
      if (this.isMobileActive && this.onWindowCallback) {
        this.onWindowCallback(this.accelZBuffer.slice(), this.speedMps);
      }
    }, 1500);
  }

  pushSample(val) {
    this.accelZBuffer.shift();
    this.accelZBuffer.push(val);
  }

  // Start desktop physics simulator with specified profile
  async setSimulationProfile(profileId) {
    this.isMobileActive = false;
    this.activeProfile = profileId;

    try {
      const res = await fetch(`/api/simulate/${profileId}`);
      if (res.ok) {
        const data = await res.json();
        this.cachedProfileData = data;
        this.speedMps = data.speed_mps || 1.4;
      }
    } catch (e) {
      console.warn('Fallback to client synthesizer:', e);
    }

    this.startSimulator();
  }

  startSimulator() {
    this.stopSimulator();
    this.simIndex = 0;
    
    // Interval runs at 50 Hz (every 20ms)
    this.simTimer = setInterval(() => {
      let sample = 1.0;
      if (this.cachedProfileData && this.cachedProfileData.accel_z.length > 0) {
        sample = this.cachedProfileData.accel_z[this.simIndex % this.cachedProfileData.accel_z.length];
        this.simIndex++;
      } else {
        // Client synthetic fallback
        sample = 1.0 + (Math.random() - 0.5) * 0.1;
      }
      this.pushSample(sample);
    }, 20);

    // Evaluation window trigger every 1.5 seconds
    this.evalTimer = setInterval(() => {
      if (this.onWindowCallback) {
        this.onWindowCallback(this.accelZBuffer.slice(), this.speedMps);
      }
    }, 1500);
  }

  stopSimulator() {
    if (this.simTimer) clearInterval(this.simTimer);
    if (this.evalTimer) clearInterval(this.evalTimer);
    this.simTimer = null;
    this.evalTimer = null;
  }

  // High performance Canvas Waveform Rendering
  startRenderingLoop() {
    const render = () => {
      this.drawWaveform();
      requestAnimationFrame(render);
    };
    requestAnimationFrame(render);
  }

  drawWaveform() {
    if (!this.canvas || !this.ctx) return;
    const ctx = this.ctx;
    const w = this.canvas.width;
    const h = this.canvas.height;

    // Clear background
    ctx.fillStyle = '#040705';
    ctx.fillRect(0, 0, w, h);

    // Draw grid lines
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.05)';
    ctx.lineWidth = 1;
    ctx.beginPath();
    // 1.0g center line
    const zeroY = h * 0.5;
    ctx.moveTo(0, zeroY);
    ctx.lineTo(w, zeroY);
    // +2.0g and -0.0g lines
    ctx.moveTo(0, h * 0.25);
    ctx.lineTo(w, h * 0.25);
    ctx.moveTo(0, h * 0.75);
    ctx.lineTo(w, h * 0.75);
    ctx.stroke();

    // Pick line color based on profile
    let strokeColor = '#10B981'; // Emerald
    if (this.activeProfile === 'asphalt') strokeColor = '#F59E0B';
    if (this.activeProfile === 'cobblestones') strokeColor = '#EF4444';

    ctx.strokeStyle = strokeColor;
    ctx.lineWidth = 2.2;
    ctx.beginPath();

    const step = w / (this.bufferSize - 1);
    for (let i = 0; i < this.bufferSize; i++) {
      const z = this.accelZBuffer[i];
      // Normalize: 1.0g = center, 3.0g = top, -1.0g = bottom
      // range is [-1.0, 3.0], span = 4.0
      const normY = (z - (-1.0)) / 4.0;
      const y = h - (normY * h);
      const x = i * step;

      if (i === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    }
    ctx.stroke();
  }
}

window.SensorEngine = SensorEngine;
