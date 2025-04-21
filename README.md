# Solis API → Prometheus Exporter & Grafana Dashboard

**A self‑contained solution to collect Solis inverter data via the SolisCloud API, export it as Prometheus metrics, and visualize everything in Grafana.**

---

## Repository Structure

```text
.
├── src/solice_api/               # Core Python package (API client & data-fetch logic)
├── exporter.py                   # JSON → Prometheus exporter (polls data/*.json)
├── config.example.json           # Example SolisCloud API credentials file
├── prometheus.yml                # Prometheus scrape configuration
├── docker-compose.yml            # Docker Compose stack (exporter, Prometheus, Grafana)
├── solis-grafana-dashboard.json  # Provisioned Grafana dashboard JSON
├── data/                         # Directory for Solis JSON snapshots
│   └── *.json                    # Raw inverter detail files
├── pyproject.toml                # Python project metadata & dependencies
├── uv.lock                       # Dependency lock file for UV
└── README.md                     # This document
```

---

## Prerequisites

- **Python 3.8+**
- **Docker & Docker Compose**
- **UV** (optional; used for `get-data` script)

---

## Configuration

1. **Copy** the example config into place:

   ```bash
   cp config.example.json config.json
   ```

2. **Edit** `config.json` to add your SolisCloud credentials:

   ```json
   {
     "key": "YOUR_API_KEY",
     "secret": "YOUR_API_SECRET"
   }
   ```

3. (Optional) Adjust environment variables:
   | Variable | Default | Description |
   |--------------|---------|-------------------------------------------|
   | `EXPORT_PORT`| `8000` | HTTP port for exporter metrics endpoint |
   | `POLL_SEC` | `30` | Seconds between JSON directory polls |
   | `LOG_LEVEL` | `INFO` | Python logging level |

---

## Quick Start

### 1. Fetch inverter data

Use the built‑in UV script to retrieve inverter snapshots:

```bash
uv run get-data
```

This populates `data/` with one JSON file per inverter.

### 2. Run exporter locally

```bash
pip install prometheus_client
python exporter.py
```

Visit http://localhost:8000/metrics to confirm metrics are exposed.

### 3. Launch full stack with Docker Compose

```bash
docker-compose up -d
```

- **Exporter** → `:8000/metrics`
- **Prometheus** → http://localhost:9090
- **Grafana** → http://localhost:3000 (admin/admin)

---

## Metrics Published

Each metric is labeled by `sn` (serial number) and `station`:

| Name                           | Description                      | Unit |
| ------------------------------ | -------------------------------- | ---- |
| `solis_inverter_ac_power_kw`   | Instant AC output power          | kW   |
| `solis_inverter_grid_freq_hz`  | Grid frequency                   | Hz   |
| `solis_inverter_temperature_c` | Inverter temperature             | °C   |
| `solis_energy_today_kwh`       | Energy generated today           | kWh  |
| `solis_energy_total_kwh`       | Lifetime energy (counter)        | kWh  |
| `solis_battery_soc_percent`    | Battery state of charge          | %    |
| `solis_battery_power_kw`       | Battery power (charge/discharge) | kW   |
| `solis_home_load_power_kw`     | Home load power                  | kW   |
| `solis_grid_import_today_kwh`  | Grid import energy today         | kWh  |
| `solis_grid_export_today_kwh`  | Grid export energy today         | kWh  |

---

## Grafana Dashboard

1. In Grafana UI → **Dashboards → Import**
2. Upload `solis-grafana-dashboard.json`
3. Select **Prometheus** as data source
4. Enjoy your Solis metrics dashboard with station‑level filtering

---

## Development & Contributing

1. Fork the repo
2. Create a feature branch (`git checkout -b feature-name`)
3. Commit your changes (`git commit -m "Add feature"`)
4. Push and open a pull request

---

## License

Distributed under the MIT License. See [LICENSE](LICENSE) for details.
