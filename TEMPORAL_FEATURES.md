# Temporal Features

**Status**: Phase 3B Predictive Feature Engineering
**Purpose**: Transforms raw synthetic time-series telemetry into rolling, interpretable historical features mapped to future predictive targets.

## Prediction Task
The future ML task is an **early-warning binary classification**: "Based strictly on the current state and recent history, will the system begin experiencing a failure condition within the upcoming prediction horizon?"

## Target Definition (`target_failure_within_10`)
- **Prediction Horizon**: 10 timesteps (10 minutes).
- **Definition**: Evaluates to `1` if *any* timestep within the forward window `[t+1 : t+10]` contains an active failure state (`failure_status == 1`). Evaluates to `0` otherwise.
- **Anti-Triviality**: Because the target looks forward, a system that is currently perfectly healthy (`failure_status == 0` and all metrics `< 85%`) can legitimately be labeled `1` if the historical trend correctly implies an impending breach.

## Features Generated
For each core system metric (`cpu_percent`, `memory_percent`, `disk_percent`, `net_bytes_sent_rate`, `net_bytes_recv_rate`), the following features are extracted over 5-step and 10-step rolling windows:

1. **Current Value** (`_current`): Instantaneous snapshot at `t`.
2. **Moving Averages** (`_mean_5`, `_mean_10`): Simple unweighted rolling mean representing the recent operational baseline.
3. **Deltas** (`_delta_5`, `_delta_10`): Absolute change from the start of the window to the current timestep (`value[t] - value[t-W+1]`).
4. **Slopes** (`_slope_5`, `_slope_10`): The slope coefficient of a simple linear regression fitted over the window, capturing velocity and direction (e.g., accelerating leaks).
5. **Standard Deviation** (`_std_5`, `_std_10`): Rolling volatility / instability metric.

## Boundary Handling
- **Warm-Up Period**: Rolling features require historical context. The script drops the first `max(WINDOWS) - 1` rows of every sequence. Zero-padding or backward-filling is rejected to prevent artificial artifacts.
- **End-of-Sequence Censoring**: Because the target requires 10 future timesteps to be definitively evaluated, the final 10 rows of every sequence are dropped from the supervised dataset rather than falsely being labeled `0` due to truncated horizons.
- **Sequence Isolation**: Features are strictly grouped by `sequence_id`. Rolling calculations perfectly reset at sequence boundaries.

## Leakage Prevention
- **Future Blindness**: Calculating features at timestep `t` mathematically uses only array indices `<= t`. 
- **Metadata Exclusion**: `failure_start_index` and future timestamps are entirely excluded from the numerical predictive feature space.
- **Split Isolation**: The feature extraction maps 1:1 against the previously air-gapped `Train / Validation / Test` datasets, ensuring training sequence context never rolls into validation sequences.

## Limitations
This remains **controlled synthetic monitoring data**. In production, complex auto-scaling rules can temporarily invert slopes (e.g., CPU drops sharply because a new node spun up, not because traffic dropped), which simple linear slopes might misinterpret.
