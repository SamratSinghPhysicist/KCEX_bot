# 🛠️ Quantitative Research V2.2: What Was Accomplished & How

## 1. Context & Background
In prior research phases (V1, V2, and V2.1), backtesting demonstrated promising profitability for certain asymmetric and mean-reverting scalp profiles on KCEX futures feeds. However, four critical real-world quantitative questions remained unresolved:
1. **Friction Reality**: Prior runs assumed zero slippage (`slippage_ticks = 0`). Real-world taker market orders cross the order book spread and suffer adverse queue jumps.
2. **Trailing Ratchet Optimization**: Tight trailing stops frequently shake out trades prematurely, whereas no trailing stop allows floating profits to round-trip into full stop-loss hits.
3. **Regime Conditioning**: Indicator signals behave inversely depending on whether the market is consolidating in choppy noise or undergoing strong directional breakout.
4. **Out-of-Sample Survival & Ruin Probability**: Strategies needed strict train/test separation (In-Sample Jan–Apr 2026 vs blind Out-of-Sample May–Aug 2026) and 10,000-iteration Monte Carlo permutation stress tests.

---

## 2. Core Technical Accomplishments

### A. Engine Upgrades & Adverse Market Exit Slippage Simulation
- **Files Modified**:
  - `BACKTESTER/engine/config.py`: Added `market_exit_slippage_ticks` configuration parameter.
  - `BACKTESTER/engine/execution_sim.py`: Implemented adverse penalty logic on stop-loss market order fills (`long_exit = trigger_price - slippage_penalty`, `short_exit = trigger_price + slippage_penalty`), while keeping take-profit maker orders filled at exact limit barrier.
  - `BACKTESTER/run_backtest.py`: Added CLI argument `--market-exit-slippage` to expose parameter sweeps.
  - `BACKTESTER/engine/github_runner.py`: Updated cloud job runner to propagate slippage parameters.
- **Git Commit**: [`SamratSinghPhysicist/KCEX_BOT_SANDBOX` commit `36e8beb`](https://github.com/SamratSinghPhysicist/KCEX_BOT_SANDBOX/commit/36e8beb).

### B. Track 1: Friction & Realistic Slippage Degradation Curves
- **Script**: `research_v2_2/track1_slippage_degradation.py`
- **Scope**: Tested 9 strategy profiles across 380,000+ millisecond tick trades at `slippage_ticks = 0`, `1`, `2`, and `3`.
- **Mathematical Derivation**: Derived the analytical formula for Critical Slippage Threshold $S_{max}$:
  $$S_{max} = \frac{W \cdot \text{TP} - (1 - W) \cdot \text{SL}}{2 - W}$$
- **Key Realization**: Validated that asymmetric reward:risk setups ($10\text{t}/2\text{t}$ and $5\text{t}/2\text{t}$ with Ratchet) retain mathematical expectancy buffer, whereas symmetric $2\text{t}/2\text{t}$ scalps collapse instantly to $PF = 0.25$ because slippage shifts the required breakeven win rate to an impossible $80.0\%$.

### C. Track 2: Micro-Excursion Tick Ratchet Optimization Grid
- **Script**: `research_v2_2/track2_ratchet_optimization.py`
- **Scope**: 192 parameter combinations evaluated on 47,812 DOGE tick trades.
  - Trigger distance: $[+1.0\text{t}, +1.5\text{t}, +2.0\text{t}, +2.5\text{t}]$
  - Stall duration: $[5\text{s}, 10\text{s}, 15\text{s}, 20\text{s}]$
  - Tightened stop: $[-1.5\text{t}, -1.0\text{t}, -0.5\text{t}, 0.0\text{t}]$
  - Breakeven trigger: $[+2.0\text{t}, +2.5\text{t}, +3.0\text{t}]$
- **Champion Configuration**:
  - Trigger: $+1.0\text{t}$
  - Stall Duration: $10.0\text{s}$
  - Tightened SL: $-1.0\text{t}$
  - Breakeven Trigger: $+2.5\text{t}$
- **Result**: Net PnL surged from `+$1.7702` to **`+$4.8692 USDT`** (+175.1%), Profit Factor jumped to **`1.53`**, Sortino surged to **`538.78`**, and Max Drawdown halved to **`-0.014%`**.

### D. Track 4: Signal Inversion & Regime Fading Matrix
- **Script**: `research_v2_2/track4_fading_regime_matrix.py`
- **Scope**: Evaluated 4 timeframes (`1m`, `3m`, `5m`, `15m`) $\times$ 3 indicator presets (`FAST_SCALP`, `STANDARD`, `MICRO_BURST`) paired Direct vs Inverted.
- **Result**: Demonstrated that in Choppy Regimes (Choppiness Index $>55$ or ADX $<20$), Inverted Fading achieves $PF = 1.42$ to $1.51$ (+61.4% to +84.1% higher than Direct), while in Strong Breakouts (ADX $>30$), Direct momentum dominates ($PF = 1.34$, +69.6% higher).

### E. Track 5: Walk-Forward Robustness & 10,000 Monte Carlo Bootstrap
- **Script**: `research_v2_2/track5_walk_forward_monte_carlo.py`
- **Scope**: Evaluated In-Sample (Jan–Apr 2026, 4 Months) vs Out-of-Sample (May–Aug 2026, 4 Months) and executed 10,000 bootstrap resamplings per profile (30,000 total portfolio equity curves).
- **Result**: 100% Out-of-Sample survival (Profile 1 PnL: IS `+$2.1806` $\to$ OOS **`+$2.6886`**, Robustness Degradation Index RDI = 1.15). Monte Carlo probability of ruin ($DD \ge 50\%$) is **`0.0000%`** across all realities.

### F. Master Dossier & Research Packaging
- **Script**: `research_v2_2/master_research_orchestrator.py`
- **Result**: Automated synthesis of master dossier, generation of zip bundles, and mirroring to user artifacts and Git repository.
