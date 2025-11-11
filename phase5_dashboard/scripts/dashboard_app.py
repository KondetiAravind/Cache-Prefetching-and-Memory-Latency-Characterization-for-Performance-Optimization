#!/usr/bin/env python3
"""
dashboard_app.py — ACA Project Dashboard (Phases 1 → 5)
Structured sequentially: Summary → Phase1 → Phase2 → Phase3 → Phase4 → Phase5 (Dashboard)
"""

import pandas as pd
from pathlib import Path
from dash import Dash, dcc, html, Input, Output, dash_table
import plotly.express as px

# === Paths ===
DATA_DIR = Path("/home/aravind/ACA/phase5_dashboard/data")
MEMLAT_CSV = DATA_DIR / "memlat.csv"
POWER_CSV = DATA_DIR / "power_summary.csv"
SUMMARY_CSV = DATA_DIR / "all_phase_summary.csv"

# === Initialize App ===
app = Dash(__name__)
app.title = "ACA Project Dashboard — Phases 1 to 5"

# === Layout ===
app.layout = html.Div([
    html.H1("ACA Project — Integrated Performance Dashboard", style={'textAlign': 'center'}),
    html.Hr(),

    dcc.Interval(id="update-interval", interval=30000, n_intervals=0),

    # -------------------------------------------
    # 0️⃣ Global Summary Table
    # -------------------------------------------
    html.H2("📊 All-Phases Summary Overview"),
    html.P("A consolidated table showing key metrics from Phases 1–4 (Baseline → Prefetching → Latency → Power).",
           style={'textAlign': 'center', 'fontStyle': 'italic'}),
    dash_table.DataTable(
        id="summary-table",
        style_table={'width': '95%', 'margin': 'auto', 'border': '1px solid #ccc'},
        style_cell={'textAlign': 'center', 'fontFamily': 'monospace', 'padding': '6px'},
        page_size=15
    ),
    html.Hr(),

    # -------------------------------------------
    # 1️⃣ Phase-1 — Baseline Performance
    # -------------------------------------------
    html.H2("Phase-1: Baseline Pipeline (sim-outorder)"),
    dcc.Graph(id="phase1-graph"),
    html.P("Baseline CPI and IPC values from initial SimpleScalar configuration.",
           style={'textAlign': 'center'}),

    # -------------------------------------------
    # 2️⃣ Phase-2 — Cache Prefetching
    # -------------------------------------------
    html.H2("Phase-2: Cache Prefetching Analysis"),
    dcc.Graph(id="phase2-graph"),
    html.P("Comparison of IPC values for Baseline, Next-Line, One-Block Lookahead, and Stride Prefetchers.",
           style={'textAlign': 'center'}),

    # -------------------------------------------
    # 3️⃣ Phase-3 — Memory Latency Model
    # -------------------------------------------
    html.H2("Phase-3: Memory Latency Characterization"),
    dcc.Graph(id="phase3-graph"),
    html.P("Latency trends across access types (Pointer, Index, Stride, Concurrent).",
           style={'textAlign': 'center'}),

    # -------------------------------------------
    # 4️⃣ Phase-4 — Power/Energy Modeling
    # -------------------------------------------
    html.H2("Phase-4: Power and Energy Model"),
    dcc.Graph(id="phase4-latency"),
    dcc.Graph(id="phase4-energy"),
    html.P("Derived from calibrated L1–DRAM latency values and energy per access.",
           style={'textAlign': 'center'}),

    # -------------------------------------------
    # 5️⃣ Phase-5 — Live Dashboard
    # -------------------------------------------
    html.H2("Phase-5: Real-Time Dashboard (Auto-Refresh)"),
    dcc.Graph(id="phase5-summary-graph"),

    html.P("Auto-refresh enabled every 30 s • Developed for ACA Project",
           style={'fontStyle': 'italic', 'textAlign': 'center'})
])

# === Callbacks ===
@app.callback(
    [Output("summary-table", "data"),
     Output("summary-table", "columns"),
     Output("phase1-graph", "figure"),
     Output("phase2-graph", "figure"),
     Output("phase3-graph", "figure"),
     Output("phase4-latency", "figure"),
     Output("phase4-energy", "figure"),
     Output("phase5-summary-graph", "figure")],
    [Input("update-interval", "n_intervals")]
)
def update_dashboard(_):
    # Load Data
    summary_df = pd.read_csv(SUMMARY_CSV)
    memlat_df = pd.read_csv(MEMLAT_CSV)
    power_df = pd.read_csv(POWER_CSV)

    # =============== TABLE ===============
    columns = [{"name": i, "id": i} for i in summary_df.columns]
    data = summary_df.to_dict("records")

    # =============== PHASE 1 ===============
    phase1 = summary_df[summary_df["Phase"] == "Phase-1"]
    fig_p1 = px.bar(phase1, x="Metric", y="Value", color="Metric",
                    text="Value", title="Phase-1 Baseline CPI and IPC")
    fig_p1.update_traces(textposition="outside")

    # =============== PHASE 2 ===============
    phase2 = summary_df[summary_df["Phase"].str.contains("Phase-2", case=False)]
    fig_p2 = px.bar(phase2, x="Phase", y="Value", color="Metric",
                    text="Value", title="Phase-2 Prefetching IPC Comparison")
    fig_p2.update_traces(textposition="outside")

    # =============== PHASE 3 ===============
    phase3 = summary_df[summary_df["Phase"].str.contains("Phase-3", case=False)]
    fig_p3 = px.line(phase3, x="Phase", y="Value", color="Metric",
                     markers=True, title="Phase-3 Latency Measurements (L1 → DRAM)")
    fig_p3.update_layout(xaxis={'categoryorder': 'total descending'})

    # =============== PHASE 4 ===============
    fig_lat = px.line(memlat_df, x="size_mib", y="latency_ns",
                      title="Phase-4 Measured Memory Latency Curve (ns)",
                      markers=True)
    fig_energy = px.bar(power_df, x="Level", y="Energy/Access(pJ)",
                        title="Phase-4 Energy per Access (pJ)",
                        color="Level", text="Energy/Access(pJ)")
    fig_energy.update_traces(textposition="outside")

    # =============== PHASE 5 (Live Overview) ===============
    phase5_focus = summary_df[
        summary_df["Metric"].str.contains("IPC|CPI|Energy|Latency", case=False, regex=True)
    ]
    fig_p5 = px.bar(phase5_focus, x="Phase", y="Value", color="Metric",
                    text="Value", title="Phase-5 Live Overview (All Metrics)")
    fig_p5.update_traces(textposition="outside")

    return data, columns, fig_p1, fig_p2, fig_p3, fig_lat, fig_energy, fig_p5


if __name__ == "__main__":
    print("🚀 Launching ACA Full Dashboard → http://127.0.0.1:8050")
    app.run(host="127.0.0.1", port=8050, debug=False)
