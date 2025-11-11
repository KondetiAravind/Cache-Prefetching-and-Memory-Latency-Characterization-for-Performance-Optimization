#!/usr/bin/env python3
"""
collect_phase4_data.py
Phase-4 → Phase-5 data aggregator.

Reads:
  /home/aravind/ACA/phase4_cpu_perf/results/memlat_output.txt
  /home/aravind/ACA/phase4_cpu_perf/results/latencies_only.txt
  /home/aravind/ACA/phase4_cpu_perf/power_model/results/power_summary.csv
and exports cleaned CSVs for the dashboard.
"""

import re
import csv
from pathlib import Path
import shutil

RESULTS_DIR = Path("/home/aravind/ACA/phase4_cpu_perf/results")
POWER_DIR   = Path("/home/aravind/ACA/phase4_cpu_perf/power_model/results")
OUT_DIR     = Path("/home/aravind/ACA/phase5_dashboard/data")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# 1️⃣ Parse memlat_output.txt → memlat.csv
memlat_in = RESULTS_DIR / "memlat_output.txt"
memlat_out = OUT_DIR / "memlat.csv"
if memlat_in.exists():
    rows = []
    for line in memlat_in.read_text(errors="ignore").splitlines():
        m = re.match(r"\s*\d+\s*,\s*([0-9.]+)\s*,\s*([0-9.]+)", line)
        if m:
            rows.append((float(m.group(1)), float(m.group(2))))
    if rows:
        with memlat_out.open("w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["size_mib", "latency_ns"])
            w.writerows(rows)
        print(f"✅ Wrote {len(rows)} lines → {memlat_out}")
    else:
        print("⚠️ No valid data found in memlat_output.txt")
else:
    print(f"❌ File not found: {memlat_in}")

# 2️⃣ Copy latencies_only.txt
lat_file = RESULTS_DIR / "latencies_only.txt"
if lat_file.exists():
    shutil.copy2(lat_file, OUT_DIR / "latencies_only.txt")
    print("✅ Copied latencies_only.txt")
else:
    print(f"⚠️ latencies_only.txt missing in {RESULTS_DIR}")

# 3️⃣ Copy power_summary.csv
power_file = POWER_DIR / "power_summary.csv"
if power_file.exists():
    shutil.copy2(power_file, OUT_DIR / "power_summary.csv")
    print("✅ Copied power_summary.csv")
else:
    print(f"⚠️ power_summary.csv missing in {POWER_DIR}")

# 4️⃣ Quick summary text
summary_path = OUT_DIR / "summary_report.txt"
summary_path.write_text(
    f"Phase-4 → Phase-5 data summary\n"
    f"memlat_output.txt : {'FOUND' if memlat_in.exists() else 'MISSING'}\n"
    f"latencies_only.txt: {'FOUND' if lat_file.exists() else 'MISSING'}\n"
    f"power_summary.csv : {'FOUND' if power_file.exists() else 'MISSING'}\n"
    f"Output directory  : {OUT_DIR}\n"
)
print(f"📄 Summary report saved → {summary_path}")
