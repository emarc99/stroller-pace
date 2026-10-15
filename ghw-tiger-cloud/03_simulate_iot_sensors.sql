-- ==============================================================================
-- Challenge 9: Simulate an IoT Sensor Dataset for Testing & Development
-- Generates synthetic multi-device telemetry data spanning 7 days (5,000+ rows)
-- ==============================================================================

-- 1. Insert synthetic IoT telemetry using generate_series and sinusoidal variations
INSERT INTO sensor_telemetry (recorded_at, device_id, location, temperature, humidity, vibration_g, battery_level, status)
SELECT
    ts AS recorded_at,
    'sensor_node_' || LPAD(dev_id::text, 2, '0') AS device_id,
    CASE (dev_id % 3)
        WHEN 0 THEN 'Industrial Warehouse A'
        WHEN 1 THEN 'Cold Storage Facility B'
        ELSE 'Outdoor Solar Array C'
    END AS location,
    -- Realistic diurnal temperature cycle + sensor noise
    ROUND((22.0 + 8.0 * sin(EXTRACT(epoch FROM ts) / 86400.0 * 2.0 * pi()) + (random() * 2.0 - 1.0))::numeric, 2) AS temperature,
    -- Relative humidity inversely correlated to temperature
    ROUND((55.0 - 15.0 * sin(EXTRACT(epoch FROM ts) / 86400.0 * 2.0 * pi()) + (random() * 4.0 - 2.0))::numeric, 2) AS humidity,
    -- Mechanical vibration with occasional high-shock spikes
    ROUND((0.05 + 0.02 * random() + CASE WHEN random() > 0.98 THEN random() * 2.5 ELSE 0 END)::numeric, 4) AS vibration_g,
    -- Battery slowly draining over time
    ROUND((98.0 - (EXTRACT(epoch FROM (NOW() - ts)) / 86400.0 * 1.5) + (random() * 0.5))::numeric, 1) AS battery_level,
    CASE 
        WHEN random() > 0.98 THEN 'WARNING'
        ELSE 'OK'
    END AS status
FROM 
    generate_series(NOW() - INTERVAL '7 days', NOW(), INTERVAL '10 minutes') AS ts,
    generate_series(1, 5) AS dev_id;

-- 2. Query 1: Total rows and time range verification
SELECT 
    COUNT(*) AS total_telemetry_rows,
    MIN(recorded_at) AS earliest_timestamp,
    MAX(recorded_at) AS latest_timestamp,
    COUNT(DISTINCT device_id) AS active_devices
FROM sensor_telemetry;

-- 4. Query 2: Analytical query on Continuous Aggregate (Hourly rollups by device)
SELECT 
    hour_bucket,
    device_id,
    location,
    sample_count,
    avg_temperature,
    peak_vibration,
    avg_battery
FROM sensor_hourly_cagg
ORDER BY hour_bucket DESC, device_id ASC
LIMIT 10;

-- 5. Query 3: Anomaly detection query (Find high mechanical shock events > 1.0g)
SELECT 
    recorded_at,
    device_id,
    location,
    vibration_g,
    status
FROM sensor_telemetry
WHERE vibration_g > 1.0
ORDER BY vibration_g DESC
LIMIT 5;
