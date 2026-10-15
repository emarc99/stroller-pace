-- ==============================================================================
-- Challenge 7: Set up a Tiger Cloud service and create your first Hypertable
-- Service ID: vufn4p4o1p (ghw-timescale)
-- ==============================================================================

-- 1. Create standard relational table for multi-node IoT telemetry
CREATE TABLE IF NOT EXISTS sensor_telemetry (
    recorded_at TIMESTAMPTZ NOT NULL,
    device_id VARCHAR(32) NOT NULL,
    location VARCHAR(64) NOT NULL,
    temperature DOUBLE PRECISION,
    humidity DOUBLE PRECISION,
    vibration_g DOUBLE PRECISION,
    battery_level DOUBLE PRECISION,
    status VARCHAR(16) DEFAULT 'OK'
);

-- 2. Transform the standard table into a TimescaleDB Hypertable partitioned on recorded_at
-- Chunk time interval is set to 1 day for optimal memory residency and chunk pruning
SELECT create_hypertable(
    'sensor_telemetry',
    'recorded_at',
    chunk_time_interval => INTERVAL '1 day',
    if_not_exists => TRUE
);

-- 3. Create index for fast device-specific time-range slicing
CREATE INDEX IF NOT EXISTS idx_sensor_device_time 
ON sensor_telemetry (device_id, recorded_at DESC);

-- 4. Verification queries
SELECT hypertable_schema, hypertable_name, owner, num_dimensions 
FROM timescaledb_information.hypertables 
WHERE hypertable_name = 'sensor_telemetry';
