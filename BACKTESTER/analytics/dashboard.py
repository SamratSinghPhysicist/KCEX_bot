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
from fastapi import FastAPI, Query, HTTPException, Response
from fastapi.responses import HTMLResponse, FileResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles

from BACKTESTER.analytics.models import BacktestRunRecord
from BACKTESTER.analytics.indexer import ReportIndexer
from BACKTESTER.analytics.engine import AnalyticsEngine
from BACKTESTER.analytics.exporter import AIDossierExporter
from BACKTESTER.analytics.forensics import ForensicsEngine

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
exporter = AIDossierExporter(engine)
forensics = ForensicsEngine(indexer=indexer)


class CompareRequest(BaseModel):
    run_ids: List[str]
    selected_factors: Optional[List[str]] = None


class ExportCompareRequest(BaseModel):
    run_ids: List[str]
    selected_factors: Optional[List[str]] = None
    format: str = "markdown"  # "markdown" or "json"


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


@app.get("/api/export/run/{run_id}")
async def export_single_run_ai(run_id: str, format: str = Query("markdown")):
    """Exports a single run as an in-depth AI-ready analytical dossier (Markdown or JSON)."""
    run = indexer.get_run_by_id(run_id)
    if not run:
        raise HTTPException(status_code=404, detail=f"Run '{run_id}' not found")

    if format.lower() == "json":
        return exporter.export_json_dossier([run], is_comparison=False)
    else:
        md = exporter.export_single_markdown(run)
        return PlainTextResponse(
            content=md,
            media_type="text/markdown",
            headers={"Content-Disposition": f'attachment; filename="{run_id}_ai_dossier.md"'}
        )


@app.post("/api/export/compare")
async def export_comparison_ai(req: ExportCompareRequest):
    """Exports multi-run comparative analytics as an in-depth AI dossier (Markdown or JSON)."""
    runs = [r for r in indexer.get_all_runs() if r.metadata.run_id in set(req.run_ids)]
    if not runs:
        raise HTTPException(status_code=400, detail="No valid runs found to export")

    if req.format.lower() == "json":
        return exporter.export_json_dossier(runs, is_comparison=True)
    else:
        md = exporter.export_comparison_markdown(runs, selected_factors=req.selected_factors)
        return PlainTextResponse(
            content=md,
            media_type="text/markdown",
            headers={"Content-Disposition": 'attachment; filename="strategy_comparison_ai_dossier.md"'}
        )


@app.get("/api/export/all")
async def export_all_runs_ai(format: str = Query("markdown")):
    """Exports complete backtest library into a unified AI dossier."""
    runs = indexer.get_all_runs()
    if not runs:
        raise HTTPException(status_code=400, detail="No indexed runs available to export")

    if format.lower() == "json":
        return exporter.export_json_dossier(runs, is_comparison=True)
    else:
        md = exporter.export_comparison_markdown(runs)
        return PlainTextResponse(
            content=md,
            media_type="text/markdown",
            headers={"Content-Disposition": 'attachment; filename="all_backtests_ai_dossier.md"'}
        )


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


# =============================================================================
# FORENSICS & REPLAY LAB ENDPOINTS
# =============================================================================

class WhatIfRequest(BaseModel):
    timeout_seconds: Optional[float] = None
    tp_ticks: Optional[int] = None
    sl_roe_pct: Optional[float] = None


@app.get("/api/forensics/catalog")
async def get_forensics_catalog():
    """Returns available symbols, timeframes, dates, and runs for forensic charting."""
    return forensics.get_catalog()


@app.get("/api/forensics/candles")
async def get_forensics_candles(
    symbol: str = Query(...),
    timeframe: str = Query("1m"),
    start_ms: Optional[int] = Query(None),
    end_ms: Optional[int] = Query(None),
    limit: int = Query(1500, ge=1, le=5000)
):
    """Returns candlestick array formatted for Lightweight Charts."""
    candles = forensics.get_candles(
        symbol=symbol,
        timeframe=timeframe,
        start_ms=start_ms,
        end_ms=end_ms,
        limit=limit
    )
    return {"symbol": symbol, "timeframe": timeframe, "candles": candles}


@app.get("/api/forensics/run/{run_id}/trades-all")
async def get_forensics_all_trades(run_id: str):
    """Returns complete catalog of all trades in a run with quick stats and tick data availability."""
    return forensics.get_all_trades_catalog(run_id)


@app.get("/api/forensics/trade/{run_id}/{trade_id}")
async def get_forensics_trade_context(
    run_id: str,
    trade_id: int,
    timeframe: str = Query("1m"),
    pad_before: int = Query(80, ge=20, le=300),
    pad_after: int = Query(50, ge=10, le=200),
    include_candles: bool = Query(False)
):
    """Returns complete trade context, surrounding candles (optional), ticks, MFE/MAE, and post-exit."""
    try:
        return forensics.get_trade_forensic_context(
            run_id=run_id,
            trade_id=trade_id,
            timeframe=timeframe,
            pad_candles_before=pad_before,
            pad_candles_after=pad_after,
            include_candles=include_candles
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Forensics error: {str(e)}")


@app.get("/api/forensics/run/{run_id}/candles")
async def get_forensics_run_candles(
    run_id: str,
    timeframe: str = Query(default="1m"),
    limit: int = Query(default=100000)
):
    """Loads complete OHLCV candlestick series covering the full evaluation date range of the run."""
    try:
        return forensics.get_run_candles(run_id=run_id, timeframe=timeframe, limit=limit)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Run candles error: {str(e)}")


@app.post("/api/forensics/trade/{run_id}/{trade_id}/what-if")
async def simulate_forensics_what_if(
    run_id: str,
    trade_id: int,
    req: WhatIfRequest
):
    """Simulates counterfactual exit rules against the trade's recorded historical tick stream."""
    try:
        return forensics.simulate_what_if(
            run_id=run_id,
            trade_id=trade_id,
            timeout_seconds=req.timeout_seconds,
            tp_ticks=req.tp_ticks,
            sl_roe_pct=req.sl_roe_pct
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"What-if simulation error: {str(e)}")



def start_server(host: str = "127.0.0.1", port: int = 8000):
    import uvicorn
    print(f"\n⚡ Starting KCEX Backtest Analytics & Comparison Studio at http://{host}:{port} ...")
    uvicorn.run("BACKTESTER.analytics.dashboard:app", host=host, port=port, reload=False)


if __name__ == "__main__":
    start_server()
