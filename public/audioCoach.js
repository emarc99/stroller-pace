/**
 * StrollerPulse Audio Coach (audioCoach.js)
 * Delivers screen-free spoken voice cues through phone speaker / earbuds
 * with strict debouncing and terrain transition hysteresis.
 */

class AudioCoach {
  constructor() {
    this.synth = window.speechSynthesis || null;
    this.lastSpokenText = "";
    this.lastClassAnnounced = null;
    this.lastAnnouncementTime = 0;
    this.minRepeatIntervalMs = 7000; // Do not spam same cue within 7 seconds
    this.isMuted = false;
    this.mode = "stroller"; // "stroller" or "runner"
    this.selectedVoice = null;

    this.initVoice();
  }

  initVoice() {
    if (!this.synth) return;
    const loadVoices = () => {
      const voices = this.synth.getVoices();
      // Prefer high quality English voice (Natural, Google, or Samantha)
      this.selectedVoice = voices.find(v => v.lang.startsWith('en') && (v.name.includes('Natural') || v.name.includes('Google') || v.name.includes('Samantha'))) || voices.find(v => v.lang.startsWith('en')) || null;
    };
    if (this.synth.onvoiceschanged !== undefined) {
      this.synth.onvoiceschanged = loadVoices;
    }
    loadVoices();
  }

  setMode(newMode) {
    this.mode = newMode;
  }

  speak(text, priority = false) {
    if (this.isMuted || !this.synth) return;

    const now = Date.now();
    // Prevent repeated speech if identical text within debounce window
    if (!priority && text === this.lastSpokenText && (now - this.lastAnnouncementTime < this.minRepeatIntervalMs)) {
      return;
    }

    // Cancel current speech if high priority alert
    if (priority) {
      this.synth.cancel();
    }

    const utterance = new SpeechSynthesisUtterance(text);
    if (this.selectedVoice) {
      utterance.voice = this.selectedVoice;
    }
    utterance.rate = 1.0;
    utterance.pitch = 1.0;
    utterance.volume = 1.0;

    utterance.onend = () => {
      this.lastAnnouncementTime = Date.now();
      this.lastSpokenText = text;
    };

    this.synth.speak(utterance);
  }

  handlePrediction(predictionData) {
    const newClass = predictionData.predicted_class;
    const cue = predictionData.audio_cue;
    const hazardScore = predictionData.hazard_score || 0;

    // Trigger immediate alert on hazard class 2 or transition
    if (newClass === 2 && hazardScore > 50) {
      // High-Shock Hazard priority alert
      this.speak(cue, true);
      this.lastClassAnnounced = newClass;
    } else if (newClass !== this.lastClassAnnounced) {
      // Terrain transition event (e.g. Asphalt -> Grass)
      this.speak(cue, false);
      this.lastClassAnnounced = newClass;
    }
  }

  playSevereShockTone() {
    try {
      const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
      const osc = audioCtx.createOscillator();
      const gain = audioCtx.createGain();
      osc.type = "sawtooth";
      osc.frequency.setValueAtTime(440, audioCtx.currentTime);
      osc.frequency.exponentialRampToValueAtTime(880, audioCtx.currentTime + 0.15);
      gain.gain.setValueAtTime(0.3, audioCtx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.2);
      osc.connect(gain);
      gain.connect(audioCtx.destination);
      osc.start();
      osc.stop(audioCtx.currentTime + 0.2);
    } catch (e) {
      // AudioContext not allowed without user gesture
    }
  }
}

window.AudioCoach = AudioCoach;
