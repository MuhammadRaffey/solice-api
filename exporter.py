#!/usr/bin/env python3
"""
Enhanced Solis JSON → Prometheus exporter
-----------------------------------------
- Reads *all* detail snapshots under ./data/*.json
- Converts the most useful operational & energy fields into Prometheus metrics
- Designed to live in a container (see docker‑compose.yml)
- Zero external deps except `prometheus_client`

Add / remove fields by editing the METRIC_MAP below – no other code changes
needed.
"""
from __future__ import annotations

import json
import logging
import pathlib
import os
from dataclasses import dataclass
import threading
import time
from typing import Callable, Dict, Any

from prometheus_client import Gauge, Counter, start_http_server

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
DATA_DIR = pathlib.Path(__file__).parent / "data"      # where UV writes *.json
EXPORT_PORT = int(os.getenv("EXPORT_PORT", "8000"))   # configurable via env
POLL_INTERVAL = int(os.getenv("POLL_SEC", "30"))      # seconds

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=LOG_LEVEL, format="%(asctime)s %(levelname)s %(msg)s")

# ---------------------------------------------------------------------------
# Helper to build metrics dynamically
# ---------------------------------------------------------------------------
MetricFactory = Callable[[str, str, tuple[str, ...]], Any]

@dataclass
class MetricDef:
    name: str
    doc: str
    ptype: str  # "gauge" or "counter"
    json_key: str
    conv: Callable[[Any], float] = float  # conversion, e.g. kW→W

# Map JSON field → Prometheus metric definition
METRICS: list[MetricDef] = [
    MetricDef("solis_inverter_ac_power_kw", "Instant AC output power", "gauge", "pac"),
    MetricDef("solis_inverter_grid_freq_hz", "Grid frequency", "gauge", "fac"),
    MetricDef("solis_inverter_temperature_c", "Inverter internal temperature", "gauge", "inverterTemperature"),
    MetricDef("solis_energy_today_kwh", "Energy generated today", "gauge", "eToday"),
    MetricDef("solis_energy_total_kwh", "Lifetime energy", "counter", "eTotal"),
    MetricDef("solis_battery_soc_percent", "Battery state‑of‑charge", "gauge", "batteryCapacitySoc"),
    MetricDef("solis_battery_power_kw", "Battery charge(+)/discharge(-) power", "gauge", "batteryPower"),
    MetricDef("solis_home_load_power_kw", "Instant home load power", "gauge", "familyLoadPower"),
    MetricDef("solis_grid_import_today_kwh", "Grid purchased energy today", "gauge", "gridPurchasedTodayEnergy"),
    MetricDef("solis_grid_export_today_kwh", "Grid sell energy today", "gauge", "gridSellTodayEnergy"),
]

# Build Prometheus metric objects once ---------------------------------------------------
G_MAP: Dict[str, Gauge] = {}
C_MAP: Dict[str, Counter] = {}
LABELS = ("sn", "station")

for m in METRICS:
    if m.ptype == "gauge":
        G_MAP[m.name] = Gauge(m.name, m.doc, LABELS)
    else:
        C_MAP[m.name] = Counter(m.name, m.doc, LABELS)


def _update_metrics(detail: dict[str, Any]):
    labels = {
        "sn": detail.get("sn", "unknown"),
        "station": detail.get("stationName", "n/a"),
    }
    for m in METRICS:
        raw_val = detail.get(m.json_key)
        if raw_val is None:
            continue  # key missing in this model / firmware
        try:
            val = m.conv(raw_val)
        except (TypeError, ValueError):
            continue
        if m.ptype == "gauge":
            G_MAP[m.name].labels(**labels).set(val)
        else:
            # Only increase counter if the new reading is >= current stored value
            c = C_MAP[m.name].labels(**labels)
            delta = max(val - c._value.get(), 0.0)
            c.inc(delta)


def _poll_files():
    while True:
        for fpath in DATA_DIR.glob("*.json"):
            try:
                with fpath.open() as fp:
                    detail = json.load(fp)
                _update_metrics(detail)
            except Exception as exc:  # pylint: disable=broad-except
                logging.warning("Failed processing %s: %s", fpath.name, exc)
        time.sleep(POLL_INTERVAL)


def main():
    logging.info("Starting Solis exporter on :%s polling %s s", EXPORT_PORT, POLL_INTERVAL)
    start_http_server(EXPORT_PORT)
    threading.Thread(target=_poll_files, daemon=True).start()
    while True:
        time.sleep(3600)


if __name__ == "__main__":
    main()
