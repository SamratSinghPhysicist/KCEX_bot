"""
FastAPI Analytics & Comparison Dashboard Server
===============================================
Serves the web dashboard SPA and provides REST endpoints for report indexing,
multi-factor comparisons, normalized equity curves, and paged trade data.
"""

import os
import sys
from typing import List, Optional
from pydantic import BaseModel
from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles

from BACKTESTER.analytics.models import BacktestRunRecord
from BACKTESTER.analytics.indexer import ReportIndexer
from BACKTESTER.analytics.engine import AnalyticsEngine

# Ensure UTF-8
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

app = FastAPI(
    title="KCEX Backtest Analytics & Comparison Studio",
    version="2.0.0",
    description="Institutional-grade analytics and interactive multi-run comparison engine"
)

WEB_DIR = os.path.join(os.path.dirname(__file__), "web")
os.makedirs(WEB_DIR, exist_ok=True)

# Mount static web directory
app.mount("/static", StaticFiles(directory=WEB_DIR), name="static")

indexer = ReportIndexer()
engine = AnalyticsEngine(indexer)


class CompareRequest(BaseModel):
    run_ids: List[str]
    selected_factors: Optional[List[str]] = None


@app.get("/", response_class=HTMLResponse)
async def serve_index():
    index_path = os.path.join(WEB_DIR, "index.html")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content="<h1>Analytics Dashboard building in progress...</h1>")


@app.get("/api/factors")
async def get_factors():
    """Returns all available comparison factors with labels, categories, and formats."""
    return engine.get_all_factors()


@app.get("/api/runs")
async def get_runs(force_reindex: bool = False):
    """Returns all indexed runs with scorecards and metadata."""
    runs = indexer.get_all_runs(force_reindex=force_reindex)
    return [r.to_dict() for r in runs]


@app.get("/api/run/{run_id}")
async def get_run_details(run_id: str):
    """Returns deep-dive metadata, scorecard, directional, and detailed analytics."""
    run = indexer.get_run_by_id(run_id)
    if not run:
        raise HTTPException(status_code=404, detail=f"Run '{run_id}' not found")
    return run.to_dict()


@app.get("/api/run/{run_id}/curve")
async def get_run_curve(run_id: str):
    """Returns downsampled equity curve points for a single run."""
    curve = indexer.get_downsampled_curve(run_id)
    return {"run_id": run_id, "points": curve}


@app.get("/api/run/{run_id}/trades")
async def get_run_trades(
    run_id: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=10, le=200),
    direction: Optional[str] = Query(None),
    exit_reason: Optional[str] = Query(None),
    search: Optional[str] = Query(None)
):
    """Streams and paginates raw trades from CSV without RAM bloat."""
    return engine.get_paged_trades(
        run_id=run_id,
        page=page,
        page_size=page_size,
        direction=direction,
        exit_reason=exit_reason,
        search=search
    )


@app.post("/api/compare")
async def compare_runs(req: CompareRequest):
    """Compares multiple runs across user-selected factors."""
    if not req.run_ids:
        raise HTTPException(status_code=400, detail="run_ids list cannot be empty")
    return engine.compare_runs(run_ids=req.run_ids, selected_factors=req.selected_factors)


@app.post("/api/reindex")
async def trigger_reindex():
    """Forces re-scanning and cache updating of reports directory."""
    runs = indexer.get_all_runs(force_reindex=True)
    return {"status": "success", "indexed_count": len(runs)}


@app.get("/api/storage")
async def get_storage_stats():
    """Returns disk space usage breakdown for backtest reports."""
    reports_dir = indexer.reports_dir
    breakdown = {
        "csv_size_mb": 0.0,
        "jsonl_size_mb": 0.0,
        "zip_size_mb": 0.0,
        "md_size_mb": 0.0,
        "cache_size_mb": 0.0,
        "total_mb": 0.0,
        "jsonl_files_count": 0,
        "csv_files_count": 0,
        "zip_files_count": 0
    }

    if os.path.exists(reports_dir):
        for root, dirs, files in os.walk(reports_dir):
            for f in files:
                fpath = os.path.join(root, f)
                try:
                    sz_mb = os.path.getsize(fpath) / (1024 * 1024)
                    breakdown["total_mb"] += sz_mb
                    ext = os.path.splitext(f)[1].lower()
                    if ".cache" in root:
                        breakdown["cache_size_mb"] += sz_mb
                    elif ext == ".csv":
                        breakdown["csv_size_mb"] += sz_mb
                        breakdown["csv_files_count"] += 1
                    elif ext == ".jsonl":
                        breakdown["jsonl_size_mb"] += sz_mb
                        breakdown["jsonl_files_count"] += 1
                    elif ext == ".zip":
                        breakdown["zip_size_mb"] += sz_mb
                        breakdown["zip_files_count"] += 1
                    elif ext == ".md":
                        breakdown["md_size_mb"] += sz_mb
                except Exception:
                    pass

    for k in ["csv_size_mb", "jsonl_size_mb", "zip_size_mb", "md_size_mb", "cache_size_mb", "total_mb"]:
        breakdown[k] = round(breakdown[k], 2)

    return breakdown


@app.post("/api/storage/purge-jsonl")
async def purge_heavy_jsonl():
    """Purges large raw .jsonl files while keeping .csv, .md, .zip, and cached summaries intact."""
    reports_dir = indexer.reports_dir
    purged_count = 0
    reclaimed_mb = 0.0

    if os.path.exists(reports_dir):
        for f in os.listdir(reports_dir):
            if f.endswith("_trades.jsonl"):
                fpath = os.path.join(reports_dir, f)
                try:
                    sz_mb = os.path.getsize(fpath) / (1024 * 1024)
                    os.remove(fpath)
                    purged_count += 1
                    reclaimed_mb += sz_mb
                except Exception as e:
                    print(f"[!] Could not remove {f}: {e}")

    # Update indexer cache
    indexer.get_all_runs(force_reindex=True)

    return {
        "status": "success",
        "purged_count": purged_count,
        "reclaimed_mb": round(reclaimed_mb, 2)
    }


def start_server(host: str = "127.0.0.1", port: int = 8000):
    import uvicorn
    print(f"\n⚡ Starting KCEX Backtest Analytics & Comparison Studio at http://{host}:{port} ...")
    uvicorn.run("BACKTESTER.analytics.dashboard:app", host=host, port=port, reload=False)


if __name__ == "__main__":
    start_server()
