#!/usr/bin/env python3
"""
logger.py — Monitors dashboard data and logs updates.
Writes timestamps and file changes to a rotating log file.
"""

import os
import time
from datetime import datetime
from pathlib import Path

DATA_DIR = Path("/home/aravind/ACA/phase5_dashboard/data")
LOG_FILE = Path("/home/aravind/ACA/phase5_dashboard/results/dashboard_log.txt")

def get_size(file):
    try:
        return os.path.getsize(file)
    except FileNotFoundError:
        return 0

def log(msg):
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")

def main():
    log("✅ Logger started. Monitoring Phase-4 & Phase-5 data...")
    known_sizes = {str(f): get_size(f) for f in DATA_DIR.glob("*.*")}

    while True:
        for f in DATA_DIR.glob("*.*"):
            size = get_size(f)
            if str(f) not in known_sizes or known_sizes[str(f)] != size:
                log(f"🟢 Updated file detected: {f.name} (size={size} bytes)")
                known_sizes[str(f)] = size
        time.sleep(30)

if __name__ == "__main__":
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    main()
