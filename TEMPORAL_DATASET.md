# Temporal Monitoring Dataset

**Status**: Phase 3A Foundation (Controlled Synthetic Monitoring Data)
**Purpose**: To provide a historically-aware sequence dataset suitable for training predictive timeseries models (e.g., forecasting upcoming anomalies) rather than just point-in-time snapshot detection. 

## Structure

- **Sequence Length**: 60 timesteps (default).
- **Sampling Interval**: 1 timestep = 1 minute.
- **Total Duration per Sequence**: 1 hour.

## Features

| Feature | Type | Unit | Description |
| :--- | :--- | :--- | :--- |
| `sequence_id` | String | - | Unique identifier for the sequence (e.g., `train_0`). |
| `timestep` | Integer | - | 0-indexed position within the sequence. |
| `timestamp` | String (ISO) | - | Simulated wall-clock timestamp. |
| `cpu_percent` | Float | % | Simulated CPU utilization (0-100). |
| `memory_percent` | Float | % | Simulated memory utilization (0-100). |
| `disk_percent` | Float | % | Simulated disk space utilized (0-100). |
| `net_bytes_sent_rate` | Float | MB/s | Outbound network throughput. |
| `net_bytes_recv_rate` | Float | MB/s | Inbound network throughput. |
| `scenario` | String | - | The behavioral scenario characterizing the sequence. |
| `failure_status` | Integer | 0/1 | Binary indicator: `0` = healthy, `1` = active failure. |
| `failure_start_index` | Integer | - | Timestep index where the progressive failure first begins (null for healthy sequences). |

## Scenarios
1. **`normal_stable`**: Baseline metrics with light natural noise.
2. **`normal_variable`**: Baseline metrics with higher legitimate fluctuation variance.
3. **`cpu_gradual_failure`**: CPU progressively deteriorates following a sloped trajectory plus noise.
4. **`cpu_sudden_failure`**: CPU spikes rapidly from a normal state to critically high usage.
5. **`memory_gradual_leak`**: Linear positive trend in memory usage, simulating a slow application leak.
6. **`disk_gradual_exhaustion`**: Log accumulation simulation—steady positive drift in disk usage.
7. **`network_degradation`**: Traffic rates grow exponentially or linearly over time.
8. **`combined_gradual_failure`**: A multivariable failure where CPU, Memory, and Disk degrade simultaneously.

## Methodology & Leakage Prevention

**Train/Validation/Test Split Strategy**
We do not use standard snapshot splitting (which would randomly separate timesteps belonging to the same hour). We strictly generate completely independent sequences into target arrays by leveraging mathematically independent random seeds:
- Train arrays: generated using `seed`
- Validation arrays: generated using `seed + 1000`
- Test arrays: generated using `seed + 2000`

**Leakage Prevention Checks**:
- `failure_status` is explicitly derived internally. The future predictive model will be trained to forecast `failure_status` ahead of time using historical buffers.
- There are mathematically zero overlapping `sequence_id`s between the training and testing sets.

## Limitations
This dataset is **controlled synthetic monitoring data**, not production telemetry. Real-world clusters often experience complex temporal phenomena like cyclic cron-job spikes, correlated multi-server load balancing artifacts, or cascading hardware crashes which these simulated curves simplify into Gaussian trends.
