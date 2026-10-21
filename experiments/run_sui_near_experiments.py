#!/usr/bin/env python3
"""
SUI & NEAR Comprehensive Backtester
===================================
Runs no-stop-loss 1x leverage experiments for SUI and NEAR across:
- Long Only and Bidirectional (Both)
- Fixed 0.1% TP and Mode Dynamic TP
- Strategies: ema_cross, rsi_momentum
- Generates detailed trade CSVs and monthly breakdown
"""

import os
import sys
import subprocess

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

configurations = [
    # SUI
    {"asset": "SUI", "timeframe": "1h", "direction": "long", "tp_rule": "mode_dynamic", "strategy": "ema_cross"},
    {"asset": "SUI", "timeframe": "1h", "direction": "long", "tp_rule": "fixed_0.1", "strategy": "rsi_momentum"},
    {"asset": "SUI", "timeframe": "1h", "direction": "both", "tp_rule": "fixed_0.1", "strategy": "ema_cross"},
    {"asset": "SUI", "timeframe": "1h", "direction": "both", "tp_rule": "mode_dynamic", "strategy": "ema_cross"},

    # NEAR
    {"asset": "NEAR", "timeframe": "1h", "direction": "long", "tp_rule": "mode_dynamic", "strategy": "ema_cross"},
    {"asset": "NEAR", "timeframe": "1h", "direction": "long", "tp_rule": "fixed_0.1", "strategy": "rsi_momentum"},
    {"asset": "NEAR", "timeframe": "1h", "direction": "both", "tp_rule": "fixed_0.1", "strategy": "ema_cross"},
    {"asset": "NEAR", "timeframe": "1h", "direction": "both", "tp_rule": "mode_dynamic", "strategy": "ema_cross"},
]

def run_experiment(cfg):
    cmd = [
        sys.executable, "-m", "experiments.no_stop_loss_experiment",
        "--asset", cfg["asset"],
        "--timeframe", cfg["timeframe"],
        "--direction", cfg["direction"],
        "--tp_rule", cfg["tp_rule"],
        "--strategy", cfg["strategy"],
        "--leverage", "1",
        "--no_stop_loss"
    ]
    print(f"\n[*] Running: {cfg['asset']} | {cfg['timeframe']} | {cfg['direction']} | {cfg['tp_rule']} | {cfg['strategy']}")
    p = subprocess.run(cmd, cwd=ROOT_DIR, capture_output=True, text=True)
    if p.returncode == 0:
        print(f"[OK] Completed: {cfg['asset']} {cfg['direction']} {cfg['tp_rule']}")
    else:
        print(f"[ERROR] Failed: {p.stderr}")

if __name__ == "__main__":
    for cfg in configurations:
        run_experiment(cfg)
