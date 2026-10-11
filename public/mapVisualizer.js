/**
 * StrollerPulse Map Visualizer (mapVisualizer.js)
 * Visualizes dynamic color-coded GPS routes using Leaflet.js and OpenStreetMap.
 * Tracks live distance and calculates the "Touch Grass" Cushion Score.
 */

class MapVisualizer {
  constructor(containerId) {
    this.containerId = containerId;
    this.map = null;
    this.currentMarker = null;
    this.segments = []; // Array of { polyline, classId }
    this.lastLatLng = null;

    // Route Metrics
    this.grassDistanceMeters = 0;
    this.asphaltDistanceMeters = 0;
    this.hazardDistanceMeters = 0;
    this.totalDistanceMeters = 0;

    // Base coordinates (e.g., Central Park Nature Loop)
    this.currentLat = 40.785091;
    this.currentLng = -73.968285;

    this.initMap();
  }

  initMap() {
    if (!window.L) return;

    this.map = L.map(this.containerId, {
      zoomControl: false,
      attributionControl: false
    }).setView([this.currentLat, this.currentLng], 16);

    // Dark cartographic tiles from CartoDB Dark Matter
    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
      maxZoom: 19
    }).addTo(this.map);

    // Initial marker with pulsing icon
    const markerIcon = L.divIcon({
      className: 'custom-pulsing-marker',
      html: '<div class="pulse-marker-core"></div>',
      iconSize: [20, 20]
    });

    this.currentMarker = L.marker([this.currentLat, this.currentLng], { icon: markerIcon }).addTo(this.map);
    this.lastLatLng = [this.currentLat, this.currentLng];

    // Try device geolocation if available
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition((pos) => {
        this.currentLat = pos.coords.latitude;
        this.currentLng = pos.coords.longitude;
        this.map.setView([this.currentLat, this.currentLng], 16);
        this.currentMarker.setLatLng([this.currentLat, this.currentLng]);
        this.lastLatLng = [this.currentLat, this.currentLng];
      }, () => {
        // Fallback to default loop
      });
    }
  }

  addStep(classId, speedMps = 1.4) {
    if (!this.map) return;

    // Simulate small forward step along bearing (or use GPS position)
    const stepDistance = speedMps * 1.5; // step for 1.5s window in meters
    const latOffset = (stepDistance / 111320.0) * (0.8 + Math.random() * 0.4);
    const lngOffset = (stepDistance / (111320.0 * Math.cos(this.currentLat * (Math.PI / 180.0)))) * (0.4 + Math.random() * 0.3);

    const nextLat = this.currentLat + latOffset;
    const nextLng = this.currentLng + lngOffset;
    const nextLatLng = [nextLat, nextLng];

    // Pick segment color
    let color = '#10B981'; // Emerald (Grass)
    if (classId === 1) color = '#F59E0B'; // Amber (Asphalt)
    if (classId === 2) color = '#EF4444'; // Rose (Hazard)

    // Draw dynamic polyline segment
    const segment = L.polyline([this.lastLatLng, nextLatLng], {
      color: color,
      weight: 5,
      opacity: 0.9,
      lineCap: 'round'
    }).addTo(this.map);

    this.segments.push({ polyline: segment, classId: classId });

    // Update distances
    this.totalDistanceMeters += stepDistance;
    if (classId === 0) this.grassDistanceMeters += stepDistance;
    else if (classId === 1) this.asphaltDistanceMeters += stepDistance;
    else this.hazardDistanceMeters += stepDistance;

    // Move marker and pan map
    this.currentLat = nextLat;
    this.currentLng = nextLng;
    this.lastLatLng = nextLatLng;
    this.currentMarker.setLatLng(nextLatLng);
    this.map.panTo(nextLatLng, { animate: true, duration: 0.5 });
  }

  getMetrics() {
    const total = Math.max(this.totalDistanceMeters, 1.0);
    const grassPct = Math.round((this.grassDistanceMeters / total) * 100);
    const distKm = (this.totalDistanceMeters / 1000.0).toFixed(2);

    let cushionGrade = "A+";
    let score = 92;
    if (grassPct >= 70) { cushionGrade = "A+ (Cushioned Haven)"; score = 95; }
    else if (grassPct >= 50) { cushionGrade = "A (Balanced Trail)"; score = 86; }
    else if (grassPct >= 30) { cushionGrade = "B (Mixed Pavement)"; score = 74; }
    else { cushionGrade = "C (Hard Asphalt)"; score = 58; }

    return {
      grassPercent: grassPct,
      totalDistanceKm: distKm,
      cushionGrade: cushionGrade,
      cushionScore: score
    };
  }
}

window.MapVisualizer = MapVisualizer;
