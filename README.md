# Solis API → Prometheus Exporter & Grafana Dashboard

**A self‑contained solution to collect Solis inverter data via the SolisCloud API, export it as Prometheus metrics, and visualize everything in Grafana.**

---

## Repository Structure

```text
.
├── src/
│   └── solice_api/               # Core Python package: API client and data-fetch script
├── exporter.py                   # JSON → Prometheus exporter (polls data/*.json)
├── solis-grafana-dashboard.json  # Grafana dashboard model for import
├── docker-compose.yml            # Docker Compose stack: exporter, Prometheus, Grafana
├── prometheus.yml                # Prometheus scrape configuration
├── pyproject.toml                # Project metadata, dependencies, and CLI scripts
├── .python-version               # Python version for pyenv/uv
├── .gitignore                    # Git ignore rules
├── uv.lock                       # UV CLI lock file
├── data/                         # Directory for Solis JSON snapshots
│   └── *.json                    # Raw inverter detail files (read‑only)
├── README.md                     # This document
└── LICENSE                       # MIT License
```

---

## Features

- **Core package**: `src/solice_api` handles SolisCloud authentication and data fetching.
- **Zero external deps**: the exporter (`exporter.py`) only requires `prometheus_client`.
- **File‑based polling**: reads all snapshots in `data/*.json` at configurable intervals.
- **Dynamic metrics**: add or remove metrics by editing the `METRICS` map in `exporter.py`.
- **Docker‑ready**: `docker-compose.yml` brings up exporter, Prometheus, and Grafana in one command.
- **Dashboard model**: `solis-grafana-dashboard.json` contains a full Grafana dashboard definition for import.

---

## Prerequisites

- **Python 3.11+** (managed via `pyproject.toml` / `uv`)
- **Docker & Docker Compose**
- **Git**

---

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/MuhammadRaffey/solice-api.git
cd solice-api
```

### 2. Fetch inverter data snapshots

Populate `data/` with JSON snapshots using the CLI script in the core package:

```bash
uv run get-data
```

_(Ensure your SolisCloud `config.json` is in the repo root with `key`/`secret` fields.)_

### 3. Verify metrics locally

```bash
pip install --no-cache-dir prometheus_client
python exporter.py
```

Open `http://localhost:8000/metrics` to see raw Prometheus output.

### 4. Launch full monitoring stack

```bash
docker-compose up -d
```

- **Exporter**: `http://localhost:8000/metrics`
- **Prometheus**: `http://localhost:9090`
- **Grafana**: `http://localhost:3000` (default **admin/admin**)

---

## Configuration

| Environment Variable | Default | Description                           |
| -------------------- | ------- | ------------------------------------- |
| `EXPORT_PORT`        | `8000`  | Port for exporter HTTP server         |
| `POLL_SEC`           | `30`    | Seconds between polling `data/*.json` |
| `LOG_LEVEL`          | `INFO`  | Python logging level                  |

---

## Metrics

All published metrics include two labels: `sn` (serial number) and `station` (user‑friendly name).

| Metric                         | Description                     | Unit |
| ------------------------------ | ------------------------------- | ---- |
| `solis_inverter_ac_power_kw`   | Instant AC output power         | kW   |
| `solis_inverter_grid_freq_hz`  | Grid frequency                  | Hz   |
| `solis_inverter_temperature_c` | Inverter internal temperature   | °C   |
| `solis_energy_today_kwh`       | Energy generated today          | kWh  |
| `solis_energy_total_kwh`       | Total lifetime energy (counter) | kWh  |
| `solis_battery_soc_percent`    | Battery state‑of‑charge         | %    |
| `solis_battery_power_kw`       | Battery charge/discharge power  | kW   |
| `solis_home_load_power_kw`     | Instant home load power         | kW   |
| `solis_grid_import_today_kwh`  | Grid import today               | kWh  |
| `solis_grid_export_today_kwh`  | Grid export today               | kWh  |

---

## Grafana Dashboard

1. Login to Grafana: `http://localhost:3000` (admin/admin)
2. Go to **Dashboards → Import**
3. Upload or paste `solis-grafana-dashboard.json`
4. Select **Prometheus** as the data source
5. Enjoy a full view of all `solis_*` metrics with station filtering.

---

## Contributing

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/xyz`)
3. Commit your work (`git commit -m "Add new metric support"`)
4. Push and open a PR
5. We'll review and merge!

---

## License

This project is licensed under the MIT License—see the [LICENSE](LICENSE) file for details.
