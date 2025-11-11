#!/usr/bin/env python3
"""
Compute total energy for a benchmark using simple model:
  total_energy = sum(access_count[level] * energy_per_access[level]) + static_energy
Reads:
  - sim stats file (simple scalar -redir:sim output)
  - /home/aravind/ACA/phase4_cpu_perf/power_model/results/power_summary.csv
Outputs per-benchmark CSV.
"""

import csv, re, sys, os, math

# paths (absolute)
POWER_SUM="/home/aravind/ACA/phase4_cpu_perf/power_model/results/power_summary.csv"

def read_power_summary(path):
    p = {}
    with open(path) as f:
        rdr = csv.DictReader(f)
        for r in rdr:
            lvl = r["Level"].strip()
            e_pJ = float(r["Energy/Access(pJ)"])
            p[lvl] = e_pJ * 1e-12   # convert pJ -> J
    return p

def parse_sim_stats(simfile):
    stats = {}
    with open(simfile) as f:
        for line in f:
            # common keys in SimpleScalar outputs - adjust if your file differs
            m = re.match(r'^\s*sim_num_insn\s+([0-9]+)', line)
            if m: stats['sim_num_insn'] = int(m.group(1))
            # some cache stat names — print your sim file to confirm these
            m = re.match(r'^\s*dl1.accesses\s+([0-9]+)', line)
            if m: stats['L1_accesses'] = int(m.group(1))
            m = re.match(r'^\s*dl1.misses\s+([0-9]+)', line)
            if m: stats['L1_misses'] = int(m.group(1))
            m = re.match(r'^\s*dl2.accesses\s+([0-9]+)', line)
            if m: stats['L2_accesses'] = int(m.group(1))
            m = re.match(r'^\s*dl2.misses\s+([0-9]+)', line)
            if m: stats['L2_misses'] = int(m.group(1))
            m = re.match(r'^\s*ul2.accesses\s+([0-9]+)', line)
            if m: stats['L3_accesses'] = int(m.group(1))
            m = re.match(r'^\s*mem.num_reads\s+([0-9]+)', line)
            if m: stats['DRAM_accesses'] = int(m.group(1))
    return stats

def main():
    power = read_power_summary(POWER_SUM)
    outcsv = "/home/aravind/ACA/phase4_cpu_perf/power_model/results/bench_energy_summary.csv"
    files = sorted([f for f in os.listdir("/home/aravind/ACA/phase4_cpu_perf/results") if f.endswith("_stats.txt")])
    rows = []
    for fn in files:
        simfile = os.path.join("/home/aravind/ACA/phase4_cpu_perf/results", fn)
        stats = parse_sim_stats(simfile)
        # fallback if access counts missing: try to extract any 'accesses' tokens
        if 'L1_accesses' not in stats:
            # generic grep for "accesses" lines
            with open(simfile) as f:
                for line in f:
                    if 'accesses' in line and 'dl1' in line.lower():
                        nums = re.findall(r'([0-9]+)', line)
                        if nums: stats['L1_accesses']=int(nums[0])
        # compute energies (assume 0 when missing)
        L1 = stats.get('L1_accesses', 0)
        L2 = stats.get('L2_accesses', 0)
        L3 = stats.get('L3_accesses', 0)
        DRAM= stats.get('DRAM_accesses', 0)
        totalJ = L1*power.get('L1',0) + L2*power.get('L2',0) + L3*power.get('L3',0) + DRAM*power.get('DRAM',0)
        insns = stats.get('sim_num_insn', 0)
        epinsn = (totalJ/insns) if insns>0 else 0.0
        rows.append([fn, insns, L1, L2, L3, DRAM, totalJ, epinsn])
    # write CSV
    with open(outcsv,"w",newline="") as f:
        w=csv.writer(f)
        w.writerow(["sim_file","insns","L1_access","L2_access","L3_access","DRAM_access(J)","total_J","J_per_insn"])
        for r in rows: w.writerow(r)
    print("Wrote:", outcsv)

if __name__=='__main__':
    main()
