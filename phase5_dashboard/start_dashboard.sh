#!/bin/bash
# --------------------------------------------------------
# start_dashboard.sh — Launch ACA Phase-5 environment
# --------------------------------------------------------

echo "🚀 Starting ACA Dashboard Environment..."

# Activate venv
source /home/aravind/ACA/phase5_dashboard/venv/bin/activate

# Launch Logger
echo "📜 Starting data logger..."
nohup python /home/aravind/ACA/phase5_dashboard/scripts/logger.py >/dev/null 2>&1 &

# Start Dashboard
echo "🌐 Starting dashboard at http://127.0.0.1:8050 ..."
python /home/aravind/ACA/phase5_dashboard/scripts/dashboard_app.py
