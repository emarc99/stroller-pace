-- ==============================================================================
-- Challenge 8: Accelerate Dashboards with Continuous Aggregates (CAGGs)
-- Service: ghw-timescale (vufn4p4o1p)
-- ==============================================================================

-- 1. Create a Continuous Aggregate (CAGG) for hourly IoT sensor statistics
-- Pre-computes rollups so dashboard widgets load instantaneously with zero overhead
CREATE MATERIALIZED VIEW IF NOT EXISTS sensor_hourly_cagg
WITH (timescaledb.continuous) AS
SELECT 
    time_bucket('1 hour', recorded_at) AS hour_bucket,
    device_id,
    location,
    COUNT(*) AS sample_count,
    ROUND(AVG(temperature)::numeric, 2) AS avg_temperature,
    ROUND(MIN(temperature)::numeric, 2) AS min_temperature,
    ROUND(MAX(temperature)::numeric, 2) AS max_temperature,
    ROUND(AVG(humidity)::numeric, 2) AS avg_humidity,
    ROUND(AVG(vibration_g)::numeric, 4) AS avg_vibration,
    ROUND(MAX(vibration_g)::numeric, 4) AS peak_vibration,
    ROUND(AVG(battery_level)::numeric, 1) AS avg_battery
FROM sensor_telemetry
GROUP BY hour_bucket, device_id, location
WITH NO DATA;

-- 2. Add an automated Continuous Aggregate Refresh Policy
-- Automatically materializes new chunks every 30 minutes in the background
SELECT add_continuous_aggregate_policy('sensor_hourly_cagg',
    start_offset => INTERVAL '30 days',
    end_offset => INTERVAL '1 hour',
    schedule_interval => INTERVAL '30 minutes',
    if_not_exists => TRUE
);

-- 3. Verify the continuous aggregate registration
SELECT view_name, materialization_hypertable_name, compression_enabled 
FROM timescaledb_information.continuous_aggregates
WHERE view_name = 'sensor_hourly_cagg';
