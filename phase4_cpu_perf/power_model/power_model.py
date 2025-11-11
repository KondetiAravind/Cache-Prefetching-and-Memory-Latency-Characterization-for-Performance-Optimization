#!/usr/bin/env python3
"""
Phase-4 Step-6 — Power / Energy Modelling (Route A)
This script estimates per-access & total energy for L1, L2, L3 and DRAM levels.
"""

import math, csv, os

# === Load latency info ===
lat_file = "/home/aravind/ACA/phase4_cpu_perf/results/latencies_only.txt"
latencies = []
with open(lat_file) as f:
    for line in f:
        line = line.strip()
        if line:
            try:
                latencies.append(float(line))
            except:
                pass

if len(latencies) < 4:
    raise SystemExit("Not enough latency data – rerun memlat step first!")

latencies.sort()
n = len(latencies)
L1_ns  = latencies[int(0.05*n)]
L2_ns  = latencies[int(0.30*n)]
L3_ns  = latencies[int(0.60*n)]
DRAM_ns= latencies[int(0.95*n)]

# === Assumed technology parameters ===
Vdd  = 1.0       # Supply voltage (V)
Ceff = 1e-12     # Effective capacitance (F) per switch event
alpha= 0.15      # Activity factor per access
freq = 2.5e9     # Hz

# Energy per access (J) = α × C × V²
E_access = alpha * Ceff * Vdd**2

# Weighted scaling per hierarchy (~proportional to latency)
E_L1   = E_access * (L1_ns   / L1_ns)
E_L2   = E_access * (L2_ns   / L1_ns)
E_L3   = E_access * (L3_ns   / L1_ns)
E_DRAM = E_access * (DRAM_ns / L1_ns)

# Assume 1 million accesses per level for illustration
N = 1_000_000
total_energy = {
    "L1"   : E_L1   * N,
    "L2"   : E_L2   * N,
    "L3"   : E_L3   * N,
    "DRAM" : E_DRAM * N,
}

outf = "/home/aravind/ACA/phase4_cpu_perf/power_model/results/power_summary.csv"
os.makedirs(os.path.dirname(outf), exist_ok=True)
with open(outf, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["Level","Latency(ns)","Energy/Access(pJ)","Total Energy(mJ)"])
    for lvl, e in zip(["L1","L2","L3","DRAM"], [E_L1,E_L2,E_L3,E_DRAM]):
        w.writerow([lvl,
                    round(eval(f"{lvl}_ns"),3),
                    round(e*1e12,4),
                    round(total_energy[lvl]*1e3,4)])
print("✅ Power model results saved to:", outf)
