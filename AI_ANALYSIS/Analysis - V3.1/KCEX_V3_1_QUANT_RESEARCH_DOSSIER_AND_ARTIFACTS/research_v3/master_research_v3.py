"""
KCEX ZERO-FEE 75X LEVERAGE HFT / SCALPING QUANT RESEARCH ENGINE (V3)
====================================================================
Lead Autonomous Quant Researcher & Microstructure Scientist
Continuous Autonomous Discovery & Empirical Hypothesis Testing Engine
"""

import os
import sys
import time
import math
import json
import random
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional, Tuple

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from kcex.engine.models import (
    ExecutionConfig,
    OrderDirection,
    EngineMode,
    ExitReason,
    TradeSignal,
    TradeOutcome
)
from BACKTESTER.engine.config import BacktestConfig
from BACKTESTER.engine.execution_sim import BacktestExecutionEngine
from BACKTESTER.engine.metrics import PerformanceCalculator, PerformanceSummary
from BACKTESTER.engine.github_runner import GitHubBacktestRunner


@dataclass
class SlippageTierResult:
    tier_name: str
    slippage_ticks: int
    slippage_price_delta: float
    total_trades: int
    winning_trades: int
    win_rate_pct: float
    profit_factor: float
    net_pnl_usdt: float
    max_drawdown_pct: float
    sharpe_ratio: float
    sortino_ratio: float
    liquidations: int
    expectancy_usdt: float


@dataclass
class ExperimentResult:
    experiment_id: str
    title: str
    domain: str
    mathematical_definition: str
    parameters: Dict[str, Any]
    tier_results: Dict[str, SlippageTierResult]
    slippage_gradient: float  # dPnL / dTick
    critical_s_max: float     # Analytical critical slippage boundary
    in_sample_metrics: Optional[Dict[str, Any]] = None
    oos_metrics: Optional[Dict[str, Any]] = None
    rdi: float = 1.0          # Robustness Degradation Index (OOS PF / IS PF)
    monte_carlo_ruin_prob: float = 0.0
    monte_carlo_max_dd_95ci: float = 0.0
    key_insights: List[str] = None
    next_mutation: str = ""


class MasterQuantResearchEngineV3:
    """
    Autonomous Quantitative Research Orchestrator for KCEX 75x Scalping Engine V3.
    """

    def __init__(self, reports_base_dir: Optional[str] = None):
        self.reports_base_dir = reports_base_dir or os.path.join(ROOT_DIR, "AI_ANALYSIS", "Analysis - V3")
        self.experiments_dir = os.path.join(self.reports_base_dir, "experiments")
        os.makedirs(self.experiments_dir, exist_ok=True)
        self.results_history: List[ExperimentResult] = []

    def run_slippage_tier_evaluation(
        self,
        base_config: BacktestConfig,
        sample_range: Optional[Tuple[str, str]] = None
    ) -> Dict[str, SlippageTierResult]:
        """
        Evaluates a strategy across the non-negotiable 4-Tier Slippage Matrix:
        Tier 0: 0 Ticks ($0.00000) [Theoretical Maker Baseline]
        Tier 1: 1 Tick ($0.00001 DOGE / $0.001 TRUMP) [Normal Micro-friction]
        Tier 2: 2 Ticks ($0.00002 DOGE / $0.002 TRUMP) [High Volatility Sweep]
        Tier 3: 3 Ticks ($0.00003 DOGE / $0.003 TRUMP) [Flash Liquidity Depletion]
        """
        tiers = [
            ("0T (Maker)", 0),
            ("1T (Normal)", 1),
            ("2T (Sweep)", 2),
            ("3T (Flash)", 3)
        ]
        
        tier_results = {}
        pu = 0.001 if "TRUMP" in base_config.symbol.upper() else 0.0001

        for tier_name, s_ticks in tiers:
            cfg = BacktestConfig(
                symbol=base_config.symbol,
                timeframe=base_config.timeframe,
                strategy_mode=base_config.strategy_mode,
                ema_preset=base_config.ema_preset,
                stoch_preset=base_config.stoch_preset,
                start_time=sample_range[0] if sample_range else base_config.start_time,
                end_time=sample_range[1] if sample_range else base_config.end_time,
                volume_mode=base_config.volume_mode,
                volume_contracts=base_config.volume_contracts,
                volume_multiplier=base_config.volume_multiplier,
                tp_ticks=base_config.tp_ticks,
                sl_mode=base_config.sl_mode,
                sl_ticks=base_config.sl_ticks,
                sl_roe_pct=base_config.sl_roe_pct,
                sl_price_pct=base_config.sl_price_pct,
                leverage=75,  # Non-negotiable exactly 75x leverage
                initial_balance_usdt=base_config.initial_balance_usdt,
                max_trades=base_config.max_trades,
                use_tick_data=True,  # Non-negotiable always enabled
                fee_mode="ZERO",     # Non-negotiable 0% fee schedule on KCEX zero-fee contracts
                slippage_enabled=(s_ticks > 0),
                slippage_ticks=s_ticks,
                slippage_tier=s_ticks,
                queue_dynamics_enabled=base_config.queue_dynamics_enabled,
                maker_queue_timeout_seconds=base_config.maker_queue_timeout_seconds,
                maker_queue_timeout_action=base_config.maker_queue_timeout_action,
                maker_latency_ms=base_config.maker_latency_ms,
                liquidation_buffer_pct=0.01333,
                simulate_intra_tick_liquidation=True,
                invert_signal=base_config.invert_signal,
                ratchet_enabled=base_config.ratchet_enabled,
                ratchet_trigger_ticks=base_config.ratchet_trigger_ticks,
                ratchet_stall_seconds=base_config.ratchet_stall_seconds,
                ratchet_tighten_ticks=base_config.ratchet_tighten_ticks,
                ratchet_breakeven_ticks=base_config.ratchet_breakeven_ticks,
                execution_style=base_config.execution_style,
                smart_atr_filter_enabled=getattr(base_config, "smart_atr_filter_enabled", True),
                smart_min_atr_ticks=getattr(base_config, "smart_min_atr_ticks", 2.5),
                smart_chop_ceiling=getattr(base_config, "smart_chop_ceiling", 58.0),
                smart_adx_trend_threshold=getattr(base_config, "smart_adx_trend_threshold", 26.0),
                smart_use_ema200_filter=getattr(base_config, "smart_use_ema200_filter", False),
                smart_climax_filter_enabled=getattr(base_config, "smart_climax_filter_enabled", True),
                smart_max_atr_expansion=getattr(base_config, "smart_max_atr_expansion", 2.2),
                duration_filter_enabled=base_config.duration_filter_enabled,
                adx_filter_enabled=base_config.adx_filter_enabled
            )

            engine = BacktestExecutionEngine(config=cfg)
            outcomes = engine.run()
            summary = PerformanceCalculator.calculate(
                outcomes=outcomes,
                initial_balance_usdt=cfg.initial_balance_usdt,
                inr_rate=cfg.inr_rate
            )

            tier_res = SlippageTierResult(
                tier_name=tier_name,
                slippage_ticks=s_ticks,
                slippage_price_delta=s_ticks * pu,
                total_trades=summary.total_trades,
                winning_trades=summary.winning_trades,
                win_rate_pct=summary.win_rate_pct,
                profit_factor=summary.profit_factor,
                net_pnl_usdt=summary.net_pnl_usdt,
                max_drawdown_pct=summary.max_drawdown_pct,
                sharpe_ratio=summary.sharpe_ratio,
                sortino_ratio=summary.sortino_ratio,
                liquidations=summary.liquidations,
                expectancy_usdt=summary.expectancy_usdt
            )
            tier_results[tier_name] = tier_res

        return tier_results

    def compute_monte_carlo(self, outcomes: List[TradeOutcome], num_simulations: int = 1000) -> Tuple[float, float]:
        """
        Runs Monte Carlo trade-order reshuffling to calculate:
        1. Probability of Ruin (drawdown >= 50%)
        2. 95th Percentile Maximum Drawdown %
        """
        if not outcomes:
            return 0.0, 0.0

        pnls = [o.realized_pnl_usdt for o in outcomes]
        n = len(pnls)
        max_dds = []
        ruin_count = 0

        for _ in range(num_simulations):
            shuffled = random.sample(pnls, n)
            peak = 100.0
            equity = 100.0
            max_dd = 0.0
            for p in shuffled:
                equity += p
                if equity > peak:
                    peak = equity
                dd = (peak - equity) / peak if peak > 0 else 0.0
                if dd > max_dd:
                    max_dd = dd
                if equity <= 50.0:  # 50% drawdown ruin
                    ruin_count += 1
                    break
            max_dds.append(max_dd * 100.0)

        max_dds.sort()
        idx_95 = int(num_simulations * 0.95)
        p95_dd = max_dds[min(idx_95, len(max_dds) - 1)]
        p_ruin = (ruin_count / num_simulations) * 100.0

        return p_ruin, p95_dd

    def execute_experiment(
        self,
        experiment_id: str,
        title: str,
        domain: str,
        mathematical_definition: str,
        config: BacktestConfig,
        key_insights: List[str],
        next_mutation: str,
        is_date_range: Tuple[str, str] = ("2026-07-01", "2026-08-12"),
        oos_date_range: Tuple[str, str] = ("2026-08-13", "2026-08-31")
    ) -> ExperimentResult:
        """
        Executes a full 6-step quant research cycle:
        1. Multi-tier slippage evaluation on full range
        2. Walk-forward In-Sample vs Out-of-Sample validation
        3. Monte Carlo permutations
        4. Structured report generation
        """
        print(f"\n{'='*80}\n[*] EXECUTING RESEARCH CYCLE: {experiment_id} - {title}\n{'='*80}")
        
        # 1. 4-Tier Slippage Stress Matrix Evaluation
        tier_results = self.run_slippage_tier_evaluation(config)

        # 2. Compute Slippage Sensitivity Gradient: dPnL / dTick
        pnl_0t = tier_results["0T (Maker)"].net_pnl_usdt
        pnl_3t = tier_results["3T (Flash)"].net_pnl_usdt
        slippage_gradient = (pnl_3t - pnl_0t) / 3.0

        # 3. Compute Analytical Critical Slippage Boundary S_max
        w = tier_results["0T (Maker)"].win_rate_pct / 100.0
        tp = float(config.tp_ticks)
        sl = float(config.sl_ticks if config.sl_ticks else 10.0)
        # S_max = (W*TP - (1-W)*SL) / (2 - W)
        if (2.0 - w) > 0:
            s_max = (w * tp - (1.0 - w) * sl) / (2.0 - w)
        else:
            s_max = 0.0

        # 4. Walk-Forward In-Sample & Out-of-Sample Analysis (70% IS / 30% OOS)
        print(f"[*] Running Walk-Forward Split: IS {is_date_range} | OOS {oos_date_range} ...")
        is_engine = BacktestExecutionEngine(config=BacktestConfig(
            symbol=config.symbol,
            timeframe=config.timeframe,
            strategy_mode=config.strategy_mode,
            start_time=is_date_range[0],
            end_time=is_date_range[1],
            tp_ticks=config.tp_ticks,
            sl_mode=config.sl_mode,
            sl_ticks=config.sl_ticks,
            leverage=75,
            fee_mode="ZERO",
            use_tick_data=True,
            queue_dynamics_enabled=config.queue_dynamics_enabled,
            maker_queue_timeout_seconds=config.maker_queue_timeout_seconds,
            ratchet_enabled=config.ratchet_enabled,
            invert_signal=config.invert_signal,
            execution_style=config.execution_style
        ))
        is_outcomes = is_engine.run()
        is_summary = PerformanceCalculator.calculate(is_outcomes)

        oos_engine = BacktestExecutionEngine(config=BacktestConfig(
            symbol=config.symbol,
            timeframe=config.timeframe,
            strategy_mode=config.strategy_mode,
            start_time=oos_date_range[0],
            end_time=oos_date_range[1],
            tp_ticks=config.tp_ticks,
            sl_mode=config.sl_mode,
            sl_ticks=config.sl_ticks,
            leverage=75,
            fee_mode="ZERO",
            use_tick_data=True,
            queue_dynamics_enabled=config.queue_dynamics_enabled,
            maker_queue_timeout_seconds=config.maker_queue_timeout_seconds,
            ratchet_enabled=config.ratchet_enabled,
            invert_signal=config.invert_signal,
            execution_style=config.execution_style
        ))
        oos_outcomes = oos_engine.run()
        oos_summary = PerformanceCalculator.calculate(oos_outcomes)

        rdi = (oos_summary.profit_factor / is_summary.profit_factor) if is_summary.profit_factor > 0 else 1.0

        # 5. Monte Carlo Permutation Bootstrap on all outcomes
        p_ruin, p95_dd = self.compute_monte_carlo(oos_outcomes)

        exp_result = ExperimentResult(
            experiment_id=experiment_id,
            title=title,
            domain=domain,
            mathematical_definition=mathematical_definition,
            parameters={
                "symbol": config.symbol,
                "timeframe": config.timeframe,
                "strategy_mode": config.strategy_mode,
                "tp_ticks": config.tp_ticks,
                "sl_ticks": config.sl_ticks,
                "execution_style": config.execution_style,
                "queue_dynamics": config.queue_dynamics_enabled,
                "maker_timeout": config.maker_queue_timeout_seconds,
                "ratchet_enabled": config.ratchet_enabled,
                "invert_signal": config.invert_signal,
                "leverage": 75,
                "fee_mode": "0.00% Zero Fees"
            },
            tier_results=tier_results,
            slippage_gradient=slippage_gradient,
            critical_s_max=s_max,
            in_sample_metrics={
                "trades": is_summary.total_trades,
                "pf": is_summary.profit_factor,
                "win_rate": is_summary.win_rate_pct,
                "net_pnl": is_summary.net_pnl_usdt
            },
            oos_metrics={
                "trades": oos_summary.total_trades,
                "pf": oos_summary.profit_factor,
                "win_rate": oos_summary.win_rate_pct,
                "net_pnl": oos_summary.net_pnl_usdt
            },
            rdi=rdi,
            monte_carlo_ruin_prob=p_ruin,
            monte_carlo_max_dd_95ci=p95_dd,
            key_insights=key_insights,
            next_mutation=next_mutation
        )

        self.results_history.append(exp_result)
        self.generate_experiment_report(exp_result)
        return exp_result

    def generate_experiment_report(self, res: ExperimentResult) -> str:
        """
        Generates structured markdown report matching Section 5 instructions.
        """
        t = res.tier_results
        report = f"""# 🔬 Quantitative Experiment Report: {res.experiment_id}
## {res.title}

> **Research Domain:** {res.domain}  
> **Execution Timestamp:** `{time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}`  
> **Leverage:** Exactly 75x | **Fee Schedule:** 0.00% Zero Maker & Taker Fees  

---

### 1. Mathematical Definition & Feature Logic
{res.mathematical_definition}

**Configuration Parameters:**
```json
{json.dumps(res.parameters, indent=2)}
```

---

### 2. Empirical Results Table (4-Tier Slippage Stress Matrix)

| Slippage Tier | Total Trades | Win Rate (%) | Profit Factor | Net PnL (USDT) | Max DD (%) | Sharpe Ratio | Sortino Ratio | Liquidations | Expectancy (USDT) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **0T (Maker Baseline)** | {t['0T (Maker)'].total_trades} | {t['0T (Maker)'].win_rate_pct:.2f}% | **{t['0T (Maker)'].profit_factor:.2f}** | **{t['0T (Maker)'].net_pnl_usdt:+.4f}** | {t['0T (Maker)'].max_drawdown_pct:.3f}% | {t['0T (Maker)'].sharpe_ratio:.2f} | {t['0T (Maker)'].sortino_ratio:.2f} | {t['0T (Maker)'].liquidations} | {t['0T (Maker)'].expectancy_usdt:+.5f} |
| **1T ($0.00001 / $0.001)** | {t['1T (Normal)'].total_trades} | {t['1T (Normal)'].win_rate_pct:.2f}% | **{t['1T (Normal)'].profit_factor:.2f}** | **{t['1T (Normal)'].net_pnl_usdt:+.4f}** | {t['1T (Normal)'].max_drawdown_pct:.3f}% | {t['1T (Normal)'].sharpe_ratio:.2f} | {t['1T (Normal)'].sortino_ratio:.2f} | {t['1T (Normal)'].liquidations} | {t['1T (Normal)'].expectancy_usdt:+.5f} |
| **2T ($0.00002 / $0.002)** | {t['2T (Sweep)'].total_trades} | {t['2T (Sweep)'].win_rate_pct:.2f}% | **{t['2T (Sweep)'].profit_factor:.2f}** | **{t['2T (Sweep)'].net_pnl_usdt:+.4f}** | {t['2T (Sweep)'].max_drawdown_pct:.3f}% | {t['2T (Sweep)'].sharpe_ratio:.2f} | {t['2T (Sweep)'].sortino_ratio:.2f} | {t['2T (Sweep)'].liquidations} | {t['2T (Sweep)'].expectancy_usdt:+.5f} |
| **3T ($0.00003 / $0.003)** | {t['3T (Flash)'].total_trades} | {t['3T (Flash)'].win_rate_pct:.2f}% | **{t['3T (Flash)'].profit_factor:.2f}** | **{t['3T (Flash)'].net_pnl_usdt:+.4f}** | {t['3T (Flash)'].max_drawdown_pct:.3f}% | {t['3T (Flash)'].sharpe_ratio:.2f} | {t['3T (Flash)'].sortino_ratio:.2f} | {t['3T (Flash)'].liquidations} | {t['3T (Flash)'].expectancy_usdt:+.5f} |

---

### 3. Slippage Sensitivity & Theoretical Boundaries
- **Slippage Sensitivity Gradient ($\\Delta \\text{{PnL}} / \\Delta \\text{{Tick}}$):** `{res.slippage_gradient:+.4f} USDT/tick`
- **Critical Slippage Threshold ($S_{{max}}$):** `{res.critical_s_max:.3f} ticks`
  * Strategy preserves positive expectancy when adverse entry/exit friction is below $S_{{max}}$.

---

### 4. Walk-Forward (70% IS / 30% OOS) & Monte Carlo Validation
- **In-Sample (70%):** {res.in_sample_metrics.get('trades', 0)} trades | Win Rate: {res.in_sample_metrics.get('win_rate', 0):.2f}% | Profit Factor: {res.in_sample_metrics.get('pf', 0):.2f} | PnL: {res.in_sample_metrics.get('net_pnl', 0):+.4f} USDT
- **Out-of-Sample (30%):** {res.oos_metrics.get('trades', 0)} trades | Win Rate: {res.oos_metrics.get('win_rate', 0):.2f}% | Profit Factor: {res.oos_metrics.get('pf', 0):.2f} | PnL: {res.oos_metrics.get('net_pnl', 0):+.4f} USDT
- **Robustness Degradation Index (RDI = OOS PF / IS PF):** `{res.rdi:.3f}` {"(High Stability, Zero Overfitting)" if res.rdi >= 0.85 else "(Potential Degradation)"}
- **Monte Carlo Ruin Probability ($P(\\text{{DD}} \\ge 50\\%)$):** `{res.monte_carlo_ruin_prob:.4f}%`
- **Monte Carlo 95% Confidence Interval Max DD:** `{res.monte_carlo_max_dd_95ci:.3f}%`

---

### 5. Key Insights & Decision
"""
        for insight in res.key_insights:
            report += f"- {insight}\n"

        report += f"\n**Next Logical Mutation / Hypothesis:**\n> {res.next_mutation}\n"

        file_path = os.path.join(self.experiments_dir, f"{res.experiment_id}_report.md")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"[+] Saved experiment report to: {file_path}")
        return file_path
