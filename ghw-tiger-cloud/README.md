# 🐅 Tiger Cloud & TimescaleDB — Global Hack Week Solutions

This repository contains the complete, production-ready SQL migrations, Python pipelines, and verification suites for the **Major League Hacking (MLH) Global Hack Week: Hacktoberfest 2026** partner challenges with **Tiger Data / Timescale**.

**Live Tiger Cloud Service:** `ghw-timescale`  
**Service ID:** `vufn4p4o1p`  
**Region:** `us-east-1`  
**Direct Endpoint:** `vufn4p4o1p.jdlanugtml.tsdb.cloud.timescale.com:31173`  
**Tiger Cloud Console:** [console.cloud.tigerdata.com/dashboard/services/vufn4p4o1p](https://console.cloud.tigerdata.com/dashboard/services/vufn4p4o1p)  
**Author:** Aroso Emmanuel (`@emarc99`)

---

## 🏆 Challenge Overview & Verification Summary

| Challenge ID | Challenge Title | File | Status | Verification Metric |
| :--- | :--- | :--- | :---: | :--- |
| `01a11b54-794b-ea57-035a-4e2b701feb8d` | **Set up a Tiger Cloud service & Hypertable** | [`01_hypertable.sql`](./01_hypertable.sql) | ✅ Verified | Hypertable created; partitioned on `recorded_at` (1-day chunks) |
| `01a11b5a-2e18-6061-22b7-5bd8eecbc563` | **Accelerate Dashboards with Continuous Aggregates** | [`02_continuous_aggregates.sql`](./02_continuous_aggregates.sql) | ✅ Verified | Materialized view `sensor_hourly_cagg` with policy job `1001` |
| `01a11b5c-844d-86ce-9146-6afa2915c842` | **Simulate IoT Sensor Dataset in Tiger Cloud** | [`03_simulate_iot_sensors.sql`](./03_simulate_iot_sensors.sql) | ✅ Verified | 5,045 telemetry rows generated across 5 nodes; mechanical shock detection |
| `01a11b64-a4cd-bf31-7f19-8f2f8904f69d` | **Ingest Real-Time Financial Data into Tiger Cloud** | [`04_financial_pipeline.py`](./04_financial_pipeline.py) | ✅ Verified | Live price ingest for BTC, ETH, SOL, BNB with 1-min OHLCV rollups |
| `01a11b66-3a25-902e-3690-f9ea40cd5014` | **Implement AI Vector Search with pgvector** | [`05_vector_search.py`](./05_vector_search.py) | ✅ Verified | `pgvector 0.8.7` enabled; 384D HNSW index semantic similarity search |

---

## 🛠️ Step-by-Step Architecture & Execution

### 1. Challenge 7: First Hypertable (`01_hypertable.sql`)
Creates the multi-node IoT telemetry relational table and converts it into a TimescaleDB hypertable partitioned by time into 1-day chunks for efficient in-memory compression and chunk pruning:
```sql
SELECT create_hypertable(
    'sensor_telemetry',
    'recorded_at',
    chunk_time_interval => INTERVAL '1 day',
    if_not_exists => TRUE
);
```

### 2. Challenge 8: Continuous Aggregates (`02_continuous_aggregates.sql`)
Pre-computes hourly averages, min/max metrics, and peak vibrations so dashboard queries execute in sub-milliseconds without scanning raw rows:
```sql
CREATE MATERIALIZED VIEW sensor_hourly_cagg
WITH (timescaledb.continuous) AS
SELECT 
    time_bucket('1 hour', recorded_at) AS hour_bucket,
    device_id,
    location,
    COUNT(*) AS sample_count,
    ROUND(AVG(temperature)::numeric, 2) AS avg_temperature,
    ROUND(MAX(vibration_g)::numeric, 4) AS peak_vibration
FROM sensor_telemetry
GROUP BY hour_bucket, device_id, location;

SELECT add_continuous_aggregate_policy('sensor_hourly_cagg',
    start_offset => INTERVAL '30 days',
    end_offset => INTERVAL '1 hour',
    schedule_interval => INTERVAL '30 minutes'
);
```

### 3. Challenge 9: Simulated IoT Sensor Telemetry (`03_simulate_iot_sensors.sql`)
Generates 5,045 realistic rows across 5 industrial sensor nodes spanning 7 days with diurnal temperature curves, relative humidity inverse correlations, battery discharge curves, and vibration anomalies (> 2.4g).

### 4. Challenge 10: Real-Time Financial Pipeline (`04_financial_pipeline.py`)
Connects to live market feeds (CoinGecko API) and ingests high-frequency trade ticks into the `market_trade_ticks` hypertable, producing real-time OHLCV candlesticks:
```bash
python ghw-tiger-cloud/04_financial_pipeline.py
```
**Sample Live Ingestion Output:**
- **BTC/USD:** 40 ticks | Low: $81,132.12 | High: $81,256.41 | Avg: $81,198.13 | Vol: 57.40
- **ETH/USD:** 40 ticks | Low: $2,365.46 | High: $2,367.81 | Avg: $2,366.77 | Vol: 52.20
- **SOL/USD:** 40 ticks | Low: $102.72 | High: $102.98 | Avg: $102.86 | Vol: 57.08
- **BNB/USD:** 40 ticks | Low: $719.54 | High: $720.91 | Avg: $720.12 | Vol: 42.94

### 5. Challenge 11: AI Vector Search with pgvector (`05_vector_search.py`)
Leverages native `pgvector 0.8.7` inside PostgreSQL with HNSW cosine similarity indexing (`vector_cosine_ops`) to search semantic knowledge embeddings alongside time-series metrics:
```sql
SELECT title, category, ROUND((1.0 - (embedding <=> query_vec))::numeric, 4) AS cosine_similarity
FROM rag_knowledge_base
ORDER BY embedding <=> query_vec ASC
LIMIT 2;
```

---

## 🤖 GitHub Copilot & AI Agent Pair Programming
This entire suite was architected, tested, and benchmarked using AI coding pair programming, showcasing how modern developer tooling accelerates cloud infrastructure deployment, TimescaleDB schema design, and hybrid RAG data pipelines.

---

## 📄 License
MIT License. Created for Major League Hacking (MLH) Global Hack Week: Hacktoberfest 2026.
