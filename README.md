# 🧩 Cache Prefetching and Memory Latency Characterization for Performance Optimization

A complete hands-on exploration of **processor performance**, **cache hierarchy**, and **memory behavior** using the **SimpleScalar 3.0 simulator**.  
This project integrates **cache prefetching**, **memory latency modeling**, **CPU performance analysis**, **power estimation**, and an **interactive web dashboard** to provide an end-to-end architectural performance study.

---

## 📘 Overview

This repository is developed as part of the **Advanced Computer Architecture Laboratory** coursework.  
It aims to analyze and optimize processor behavior across multiple phases — from simulation setup to performance visualization.

The work is divided into five experimental phases:

1. **Phase 1:** SimpleScalar Setup and Baseline Pipeline Execution  
2. **Phase 2:** Cache Integration and Prefetching Schemes  
3. **Phase 3:** Memory Latency Modeling and Experiments  
4. **Phase 4:** CPU Performance Analysis and Power/Energy Modeling  
5. **Phase 5:** CPU Performance Dashboard and Visualization  

---

## 🚀 Project Objectives

- Configure and simulate the **SimpleScalar 3.0** environment for performance evaluation.  
- Implement and compare **cache prefetching schemes** (Next-Line, One-Block Lookahead, Stride).  
- Develop a **Memory Latency Model** (`memlat.c`) to characterize real-world latency transitions.  
- Calibrate and analyze **CPU performance** and **power/energy consumption**.  
- Build a **Flask + Dash-based interactive dashboard** to visualize results across all phases.

---

## ⚙️ Installation and Setup

### **1️⃣ SimpleScalar Setup**
```bash
# Create project root
mkdir -p ~/ACA/simplescalar && cd ~/ACA/simplescalar

# Clone SimpleScalar 3.0 source
git clone https://github.com/toddmaustin/simplesim-3.0.git
cd simplesim-3.0

# Configure and build
make config-pisa
make
````

### **2️⃣ Verify Setup**

```bash
# Run functional test
./sim-safe tests/bin.little/test-math

# Run out-of-order simulator
./sim-outorder tests/bin.little/test-math > baseline_report.txt
```

---

## 🧠 Project Phases and Highlights

### 🔹 **Phase 1 – Baseline Pipeline Execution**

**Objective:**
Configure SimpleScalar for the PISA ISA and establish baseline pipeline metrics.

**Key Results:**

| Metric            |  Value | Observation                    |
| :---------------- | :----: | :----------------------------- |
| IPC               |  0.94  | Near one instruction per cycle |
| CPI               |  1.07  | Ideal balanced pipeline        |
| Branch Accuracy   | 90.12% | Stable control prediction      |
| I-Cache Miss Rate |  6.13% | Moderate                       |
| D-Cache Miss Rate |  1.18% | Low                            |

📁 *Outputs:* `baseline_report.txt`, `baseline_summary.txt`
✅ *Result:* Functional simulator and validated baseline configuration.

---

### 🔹 **Phase 2 – Cache Integration and Prefetching Schemes**

**Goal:**
Integrate and test hardware prefetching mechanisms to boost performance.

**Prefetching Modes:**

* `nextline` – Fetches the immediate next line.
* `oneblock` – Prefetches two lines ahead.
* `stride` – Predicts future access based on detected stride pattern.

**Performance Summary:**

| Scheme              |    IPC    |    CPI    | Remarks                 |
| :------------------ | :-------: | :-------: | :---------------------- |
| Baseline            |   0.958   |   1.043   | Reference               |
| Next-Line           |   1.222   |   0.818   | Simple, spatially local |
| One-Block Lookahead | **1.324** | **0.755** | ✅ Best performance      |
| Stride              |   1.210   |   0.826   | Good for array patterns |

**Code Changes:**

* `cache.c`, `cache.h` modified to support dynamic prefetch selection using `PREFETCH_MODE`.

📁 *Outputs:* `/phase2_cache_prefetch/results/*.txt`
🏆 *Result:* One-Block Lookahead Prefetch achieved **38% IPC improvement**.

---

### 🔹 **Phase 3 – Memory Latency Modeling and Experiments**

**Objective:**
Design a latency measurement model (`memlat.c`) to empirically characterize hierarchical memory behavior.

**Key Experiments:**

* Backward & Forward pointer scans
* Index-based access
* Stride-based access (64B, 256B, 1024B)
* Concurrent thread traversal

**Measured Latencies:**

| Memory Level | Typical Latency (ns) | Access Type       |
| :----------- | :------------------: | :---------------- |
| L1 Cache     |          1.1         | Pointer           |
| L2 Cache     |          3.0         | Pointer           |
| L3 Cache     |          6–9         | Pointer           |
| DRAM         |          10+         | Pointer           |
| Index Scan   |        0.3–0.5       | Prefetch-friendly |

📁 *Outputs:* `/phase3_mem_latency/results/`
🧩 *Integration:* Used to calibrate `-cache:lat` and `-mem:lat` parameters in SimpleScalar.
✅ *Result:* Realistic latency calibration achieved.

---

### 🔹 **Phase 4 – CPU Performance and Power/Energy Modeling**

**Objective:**
Correlate CPU performance metrics with measured latency and estimate energy cost per memory level.

**Benchmarks Used:**

* `int_arith.c` – Integer ALU
* `float_arith.c` – Floating Point
* `mem_copy.c` – Memory Transfer
* `mix_load.c` – Mixed Workload

**Latency and Energy Summary:**

| Level | Latency (ns) | Energy (pJ/access) | Relative Power |
| :---- | :----------: | :----------------: | :------------- |
| L1    |     1.142    |        0.150       | 🔹 Low         |
| L2    |     1.320    |        0.173       | 🔹 Moderate    |
| L3    |     2.952    |        0.388       | 🔹 High        |
| DRAM  |    10.092    |        1.326       | 🔸 Very High   |

📁 *Outputs:*
`/phase4_cpu_perf/results/memlat_output.txt`
`/phase4_cpu_perf/power_model/results/power_summary.csv`

✅ *Result:* Established linear **latency ↔ energy** correlation.

---

### 🔹 **Phase 5 – CPU Performance Dashboard**

**Goal:**
Create a live analytical dashboard integrating all phase data using Flask + Dash + Plotly.

**Setup:**

```bash
cd ~/ACA/phase5_dashboard
python3 -m venv venv
source venv/bin/activate
pip install pandas flask matplotlib plotly dash flask-cors numpy
python scripts/dashboard_app.py
```

**Features:**

* 📊 IPC vs CPI Comparison (Phase 1–2)
* 🔍 Latency Curve (Phase 3)
* ⚡ Energy-per-level Bar Chart (Phase 4)
* 🖥️ Unified CPU Performance Summary
* ♻️ Auto-refresh and real-time updates

**Access:**
Dashboard runs on → [http://127.0.0.1:8050](http://127.0.0.1:8050)

📁 *Structure:*

```
phase5_dashboard/
├── scripts/
│   ├── dashboard_app.py
│   ├── collect_phase4_data.py
│   └── logger.py
├── data/
│   ├── memlat.csv
│   ├── power_summary.csv
│   └── summary_report.txt
└── start_dashboard.sh
```

✅ *Result:* Interactive, auto-updating dashboard visualizing CPU and memory performance data.

---

## 🧩 Repository Structure

```
ACA/
├── simplescalar/
│   └── simplesim-3.0/
├── phase2_cache_prefetch/
│   ├── cache.c
│   ├── cache.h
│   └── results/
├── phase3_mem_latency/
│   ├── memlat.c
│   └── results/
├── phase4_cpu_perf/
│   ├── tests/
│   ├── power_model/
│   └── results/
├── phase5_dashboard/
│   ├── scripts/
│   ├── data/
│   └── venv/
└── commands.txt
```

---

## 📈 Key Outcomes

| Area                    | Achievement                                            |
| :---------------------- | :----------------------------------------------------- |
| **Baseline Simulation** | Verified SimpleScalar setup with correct CPI/IPC       |
| **Prefetching Schemes** | Improved IPC by **up to 38%** (One-Block Lookahead)    |
| **Latency Modeling**    | Measured realistic L1–DRAM timings                     |
| **Power Estimation**    | Quantified latency-energy relation                     |
| **Dashboard**           | Integrated all results in a visual analytics interface |

---

## 🧰 Tools and Technologies

* **SimpleScalar 3.0** – Processor simulation
* **C / C++** – Prefetching and latency model implementation
* **Python (Flask, Dash, Pandas, Plotly)** – Visualization and analysis
* **GCC, Make, Bash** – Compilation and automation
* **Ubuntu 22.04 LTS** – Host environment

---

## 👨‍💻 Contributors

| Name                        | Roll No.  |
| :-------------------------- | :-------- |
| **Kondeti Aravind**         | 22CS02008 |
| **Gunupuru Sai Siddhartha** | 22CS02007 |

🧭 Department of Computer Science and Engineering
**Course:** Advanced Computer Architecture Laboratory

📎 GitHub: [Cache-Prefetching-and-Memory-Latency-Characterization-for-Performance-Optimization](https://github.com/KondetiAravind/Cache-Prefetching-and-Memory-Latency-Characterization-for-Performance-Optimization)

---

## 🌟 Future Enhancements

* Add **Phase 6 – Pipeline Visualization** with real-time instruction tracing.
* Implement **ML-based adaptive prefetching** for pattern prediction.
* Extend **Power/Energy model** for multi-core and GPU architectures.
* Enable cloud-based data visualization for large-scale simulation results.

---

## 🪪 License

This repository is intended for **academic and educational purposes**.
Original SimpleScalar components are licensed under their respective open-source terms.

---

## ✨ Acknowledgements

Special thanks to:

* **Dr. Todd M. Austin** – for the SimpleScalar framework.
* **Advanced Computer Architecture Lab, CSE Department** – for guidance and resources.

---

> 🧠 *“Bridging simulation and reality — one cache line at a time.”*

```
