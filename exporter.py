#!/usr/bin/env python3
import json, time, pathlib, threading
from prometheus_client import Gauge, Counter, start_http_server  # pip install prometheus_client

DATA_DIR = pathlib.Path(__file__).parent / "data"
EXPORT_PORT = 8000           # Prometheus will scrape http://host:8000/metrics
POLL_INTERVAL = 30           # seconds

# --- metric objects ----------------------------------------------------------
POWER   = Gauge  ('solis_inverter_ac_power_kw',
                  'Instantaneous AC output power',
                  ['sn', 'station'])
ENERGY  = Counter('solis_inverter_energy_total_kwh',
                  'Total lifetime energy', ['sn', 'station'])
FREQ    = Gauge  ('solis_inverter_grid_freq_hz',
                  'Grid frequency', ['sn', 'station'])
# add more metrics here …

# --- helper ------------------------------------------------------------------
def load_details(detail_file: pathlib.Path):
    with detail_file.open() as f:
        return json.load(f)

def update_metrics(detail):
    lbl = dict(sn=detail['sn'], station=detail['stationName'])
    POWER .labels(**lbl).set(detail.get('pac',   0.0))
    FREQ  .labels(**lbl).set(detail.get('fac',  0.0))
    ENERGY.labels(**lbl).inc(max(detail.get('eTotal', 0.0)
                                 - ENERGY.labels(**lbl)._value.get(), 0.0))

def poll():
    while True:
        for p in DATA_DIR.glob("[1-9]*.json"):
            try:
                detail = load_details(p)
                update_metrics(detail)
            except Exception as e:
                print(f"[WARN] {p.name}: {e}")
        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    start_http_server(EXPORT_PORT)   # non‑blocking
    threading.Thread(target=poll, daemon=True).start()
    print(f"Exporter listening on :{EXPORT_PORT}")
    while True: time.sleep(3600)
