"""
KCEX Backtest Analytics & Interactive Comparison Studio Launcher
================================================================
One-click launch script that starts the analytics server and automatically
opens the interactive dashboard in your default web browser.

Usage:
    python run_analytics.py
    python run_analytics.py --port 8080
"""

import sys
import os
import time
import argparse
import webbrowser
import threading

# Reconfigure stdout for UTF-8 on Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)


def open_browser_delayed(url: str, delay_seconds: float = 1.2):
    """Opens browser after server has started."""
    time.sleep(delay_seconds)
    try:
        webbrowser.open(url)
    except Exception:
        pass


def main():
    parser = argparse.ArgumentParser(description="KCEX Backtest Analytics Studio")
    parser.add_argument("--host", default="127.0.0.1", help="Host address (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=8000, help="Port (default: 8000)")
    parser.add_argument("--no-browser", action="store_true", help="Do not auto-open web browser")
    args = parser.parse_args()

    url = f"http://{args.host}:{args.port}"

    banner = r"""
==============================================================================
   _  _______ _______   __  ___              _       _   _          
  | |/ / ____|  ____|\ \ / / / _ \            | |     | | (_)         
  | ' / |    | |__    \ V / / /_\ \_ __   __ _| |_   _| |_ _  ___ ___ 
  |  <| |    |  __|    > <  |  _  | '_ \ / _` | | | | | __| |/ __/ __|
  | . \ |____| |____  / . \ | | | | | | | (_| | | |_| | |_| | (__\__ \
  |_|\_\_____|______|/_/ \_\|_| |_|_| |_|\__,_|_|\__, |\__|_|\___|___/
                                                   __/ |               
        INTERACTIVE STRATEGY COMPARISON & ANALYTICS STUDIO             
=============================================================================="""
    print(banner)
    print(f"🚀 Initializing Strategy Analytics Engine...")
    print(f"🌐 Dashboard URL:    {url}")
    print(f"⚡ Press [Ctrl+C] to stop the server at any time.\n")

    if not args.no_browser:
        threading.Thread(target=open_browser_delayed, args=(url,), daemon=True).start()

    import uvicorn
    uvicorn.run("BACKTESTER.analytics.dashboard:app", host=args.host, port=args.port, log_level="info")


if __name__ == "__main__":
    main()
