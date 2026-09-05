/**
 * KCEX Strategy Forensics & Replay Lab (Forensic Charting Controller)
 * ===================================================================
 * Powered by TradingView Lightweight Charts & High-Fidelity Tick Engine.
 * Features:
 * - Multi-timeframe Candlestick Chart (1m, 3m, 5m, 15m, 30m, 1h, 4h, 1d)
 * - Trade entry/exit markers, TP/SL price lines, and duration bounding
 * - Pure-Python strategy indicator reproduction (EMA 5/13, Stoch RSI %K/%D)
 * - Millisecond-level tick trade overlay & MFE/MAE forensics
 * - Historical Replay Engine (1x - 100x speeds, scrub bar, live unrealized PnL)
 * - "What Happened After Exit?" trajectory tracker
 * - Interactive What-If Exit simulator
 */

class ForensicsController {
  constructor() {
    this.chart = null;
    this.candleSeries = null;
    this.volumeSeries = null;
    this.fastEmaSeries = null;
    this.slowEmaSeries = null;
    
    this.oscChart = null;
    this.stochKSeries = null;
    this.stochDSeries = null;
    
    this.priceLines = [];
    this.activeRunId = null;
    this.activeTradeId = null;
    this.activeSymbol = "TRUMP_USDT";
    this.activeTimeframe = "1m";
    this.tradeContext = null;
    
    // Replay State
    this.isPlaying = false;
    this.replaySpeed = 1.0;
    this.currentTickIndex = 0;
    this.replayInterval = null;
    
    this.catalog = null;
    this.allTrades = [];
    this.filteredTrades = [];
    this.tradeCounts = { all: 0, wins: 0, losses: 0, timeouts: 0, with_ticks: 0 };
    this.activeTradeFilter = "ALL";
    this.modalFilter = "ALL";
  }

  async init() {
    this.bindDOM();
    this.initCharts();
    await this.loadCatalog();
  }

  bindDOM() {
    // Run Selector
    const runSelect = document.getElementById("forensicRunSelect");
    if (runSelect) {
      runSelect.addEventListener("change", (e) => {
        this.activeRunId = e.target.value;
        this.onRunChanged();
      });
    }

    // Trade Selector
    const tradeSelect = document.getElementById("forensicTradeSelect");
    if (tradeSelect) {
      tradeSelect.addEventListener("change", (e) => {
        this.activeTradeId = parseInt(e.target.value, 10);
        this.loadTrade(this.activeRunId, this.activeTradeId);
      });
    }

    // Timeframe buttons
    document.querySelectorAll(".tf-btn").forEach(btn => {
      btn.addEventListener("click", (e) => {
        document.querySelectorAll(".tf-btn").forEach(b => b.classList.remove("active"));
        btn.classList.add("active");
        this.activeTimeframe = btn.dataset.tf;
        if (this.activeRunId && this.activeTradeId) {
          this.loadTrade(this.activeRunId, this.activeTradeId);
        }
      });
    });

    // Replay Controls
    const btnPlay = document.getElementById("btnReplayPlay");
    const btnPause = document.getElementById("btnReplayPause");
    const btnReset = document.getElementById("btnReplayReset");
    const btnStepForward = document.getElementById("btnReplayStepFwd");
    const btnStepBack = document.getElementById("btnReplayStepBack");
    const scrubSlider = document.getElementById("replayScrubSlider");

    if (btnPlay) btnPlay.addEventListener("click", () => this.playReplay());
    if (btnPause) btnPause.addEventListener("click", () => this.pauseReplay());
    if (btnReset) btnReset.addEventListener("click", () => this.resetReplay());
    if (btnStepForward) btnStepForward.addEventListener("click", () => this.stepReplay(1));
    if (btnStepBack) btnStepBack.addEventListener("click", () => this.stepReplay(-1));

    if (scrubSlider) {
      scrubSlider.addEventListener("input", (e) => {
        this.seekReplay(parseInt(e.target.value, 10));
      });
    }

    // Speed chips
    document.querySelectorAll(".speed-chip").forEach(chip => {
      chip.addEventListener("click", () => {
        document.querySelectorAll(".speed-chip").forEach(c => c.classList.remove("active"));
        chip.classList.add("active");
        this.replaySpeed = parseFloat(chip.dataset.speed);
        if (this.isPlaying) {
          this.pauseReplay();
          this.playReplay();
        }
      });
    });

    // Next / Prev Trade Buttons
    const btnPrev = document.getElementById("btnPrevTrade");
    const btnNext = document.getElementById("btnNextTrade");
    if (btnPrev) btnPrev.addEventListener("click", () => this.stepTrade(-1));
    if (btnNext) btnNext.addEventListener("click", () => this.stepTrade(1));

    // Jump to Trade Input
    const jumpInput = document.getElementById("jumpTradeInput");
    const btnJump = document.getElementById("btnJumpTrade");
    if (btnJump) {
      btnJump.addEventListener("click", () => {
        if (jumpInput && jumpInput.value) {
          this.jumpToTrade(parseInt(jumpInput.value, 10));
        }
      });
    }
    if (jumpInput) {
      jumpInput.addEventListener("keydown", (e) => {
        if (e.key === "Enter" && jumpInput.value) {
          this.jumpToTrade(parseInt(jumpInput.value, 10));
        }
      });
    }

    // Trade Filter Chips
    document.querySelectorAll("[data-trade-filter]").forEach(chip => {
      chip.addEventListener("click", () => {
        document.querySelectorAll("[data-trade-filter]").forEach(c => c.classList.remove("active"));
        chip.classList.add("active");
        this.applyTradeFilter(chip.dataset.tradeFilter);
      });
    });

    // All Trades Explorer Modal
    const btnOpenModal = document.getElementById("btnOpenAllTradesModal");
    const btnCloseModal = document.getElementById("btnCloseAllTradesModal");
    const btnCloseFooter = document.getElementById("btnCloseAllTradesFooter");
    const modalSearch = document.getElementById("modalTradeSearch");

    if (btnOpenModal) btnOpenModal.addEventListener("click", () => this.openAllTradesModal());
    if (btnCloseModal) btnCloseModal.addEventListener("click", () => this.closeAllTradesModal());
    if (btnCloseFooter) btnCloseFooter.addEventListener("click", () => this.closeAllTradesModal());

    if (modalSearch) {
      modalSearch.addEventListener("input", () => this.renderModalTable());
    }

    document.querySelectorAll("[data-modal-filter]").forEach(chip => {
      chip.addEventListener("click", () => {
        document.querySelectorAll("[data-modal-filter]").forEach(c => c.classList.remove("active"));
        chip.classList.add("active");
        this.modalFilter = chip.dataset.modalFilter;
        this.renderModalTable();
      });
    });

    // What-If Form
    const btnSimulate = document.getElementById("btnRunWhatIf");
    if (btnSimulate) {
      btnSimulate.addEventListener("click", () => this.runWhatIfSimulation());
    }
  }

  initCharts() {
    const mainContainer = document.getElementById("forensicMainChartContainer");
    const oscContainer = document.getElementById("forensicOscChartContainer");
    if (!mainContainer || !window.LightweightCharts) return;

    // Dark Institutional Theme
    const chartOptions = {
      layout: {
        background: { color: "#080c14" },
        textColor: "#8a99ad",
        fontSize: 11,
        fontFamily: "'JetBrains Mono', monospace"
      },
      grid: {
        vertLines: { color: "rgba(30, 41, 59, 0.45)" },
        horzLines: { color: "rgba(30, 41, 59, 0.45)" }
      },
      crosshair: {
        mode: LightweightCharts.CrosshairMode.Normal,
        vertLine: { color: "rgba(0, 210, 255, 0.4)", width: 1, style: 2 },
        horzLine: { color: "rgba(0, 210, 255, 0.4)", width: 1, style: 2 }
      },
      rightPriceScale: {
        borderColor: "rgba(30, 41, 59, 0.8)",
        scaleMargins: { top: 0.1, bottom: 0.25 }
      },
      timeScale: {
        borderColor: "rgba(30, 41, 59, 0.8)",
        timeVisible: true,
        secondsVisible: true
      }
    };

    // 1. Create Main Chart
    this.chart = LightweightCharts.createChart(mainContainer, chartOptions);

    // Candlestick Series
    this.candleSeries = this.chart.addCandlestickSeries({
      upColor: "#00f090",
      downColor: "#ff3366",
      borderVisible: false,
      wickUpColor: "#00f090",
      wickDownColor: "#ff3366"
    });

    // Volume Series
    this.volumeSeries = this.chart.addHistogramSeries({
      color: "#1e293b",
      priceFormat: { type: "volume" },
      priceScaleId: "",
      scaleMargins: { top: 0.82, bottom: 0 }
    });

    // EMA Overlays
    this.fastEmaSeries = this.chart.addLineSeries({
      color: "#00d2ff",
      lineWidth: 1.5,
      title: "EMA Fast (5)"
    });

    this.slowEmaSeries = this.chart.addLineSeries({
      color: "#ffb800",
      lineWidth: 1.5,
      title: "EMA Slow (13)"
    });

    // 2. Create Oscillator Chart (Stoch RSI)
    if (oscContainer) {
      const oscOptions = {
        ...chartOptions,
        rightPriceScale: {
          borderColor: "rgba(30, 41, 59, 0.8)",
          scaleMargins: { top: 0.1, bottom: 0.1 }
        }
      };
      this.oscChart = LightweightCharts.createChart(oscContainer, oscOptions);

      // Stoch RSI %K and %D
      this.stochKSeries = this.oscChart.addLineSeries({
        color: "#00d2ff",
        lineWidth: 1.5,
        title: "Stoch %K"
      });

      this.stochDSeries = this.oscChart.addLineSeries({
        color: "#ff3366",
        lineWidth: 1.5,
        title: "Stoch %D"
      });

      // Add 20 Oversold & 80 Overbought baseline reference lines
      this.stochKSeries.createPriceLine({
        price: 80,
        color: "rgba(255, 51, 102, 0.5)",
        lineWidth: 1,
        lineStyle: LightweightCharts.LineStyle.Dashed,
        axisLabelVisible: true,
        title: "OB (80)"
      });
      this.stochKSeries.createPriceLine({
        price: 20,
        color: "rgba(0, 240, 144, 0.5)",
        lineWidth: 1,
        lineStyle: LightweightCharts.LineStyle.Dashed,
        axisLabelVisible: true,
        title: "OS (20)"
      });

      // Synchronize time scales
      this.chart.timeScale().subscribeVisibleLogicalRangeChange(range => {
        if (range && this.oscChart) {
          this.oscChart.timeScale().setVisibleLogicalRange(range);
        }
      });
      this.oscChart.timeScale().subscribeVisibleLogicalRangeChange(range => {
        if (range && this.chart) {
          this.chart.timeScale().setVisibleLogicalRange(range);
        }
      });
    }

    // Auto-resize handler
    const resizeObserver = new ResizeObserver(() => {
      if (mainContainer && this.chart) {
        this.chart.applyOptions({
          width: mainContainer.clientWidth,
          height: mainContainer.clientHeight || 460
        });
      }
      if (oscContainer && this.oscChart) {
        this.oscChart.applyOptions({
          width: oscContainer.clientWidth,
          height: oscContainer.clientHeight || 150
        });
      }
    });
    resizeObserver.observe(mainContainer);
    if (oscContainer) resizeObserver.observe(oscContainer);
  }

  async loadCatalog() {
    try {
      const res = await fetch("/api/forensics/catalog");
      if (!res.ok) throw new Error("Could not fetch catalog");
      this.catalog = await res.json();

      const runSelect = document.getElementById("forensicRunSelect");
      if (!runSelect) return;

      runSelect.innerHTML = "";
      if (this.catalog.available_runs.length === 0) {
        runSelect.innerHTML = "<option value=''>No backtest runs found</option>";
        return;
      }

      this.catalog.available_runs.forEach(r => {
        const opt = document.createElement("option");
        opt.value = r.run_id;
        opt.textContent = `[${r.symbol}] ${r.run_name || r.run_id} (${r.total_trades} trades, ${r.win_rate_pct.toFixed(1)}% WR)`;
        runSelect.appendChild(opt);
      });

      // Default to first run
      this.activeRunId = this.catalog.available_runs[0].run_id;
      await this.onRunChanged();
    } catch (e) {
      console.error("[!] Error loading catalog:", e);
    }
  }

  async onRunChanged() {
    if (!this.activeRunId) return;

    try {
      const res = await fetch(`/api/forensics/run/${this.activeRunId}/trades-all`);
      if (!res.ok) throw new Error("Could not fetch complete trades catalog");
      const data = await res.json();

      this.allTrades = data.trades || [];
      this.tradeCounts = data.counts || { all: 0, wins: 0, losses: 0, timeouts: 0, with_ticks: 0 };

      // Update chip counts
      const elAll = document.getElementById("countAllTrades");
      const elWins = document.getElementById("countWinTrades");
      const elLoss = document.getElementById("countLossTrades");
      const elTime = document.getElementById("countTimeoutTrades");
      const elTick = document.getElementById("countTicksTrades");

      if (elAll) elAll.textContent = this.tradeCounts.all;
      if (elWins) elWins.textContent = this.tradeCounts.wins;
      if (elLoss) elLoss.textContent = this.tradeCounts.losses;
      if (elTime) elTime.textContent = this.tradeCounts.timeouts;
      if (elTick) elTick.textContent = this.tradeCounts.with_ticks;

      this.applyTradeFilter(this.activeTradeFilter, true);
    } catch (e) {
      console.error("[!] Error loading all trades for run:", e);
    }
  }

  applyTradeFilter(filterType, isInitial = false) {
    this.activeTradeFilter = filterType;

    if (filterType === "WIN") {
      this.filteredTrades = this.allTrades.filter(t => t.pnl_usdt > 0);
    } else if (filterType === "LOSS") {
      this.filteredTrades = this.allTrades.filter(t => t.pnl_usdt < 0);
    } else if (filterType === "TIMEOUT") {
      this.filteredTrades = this.allTrades.filter(t => (t.exit_reason || "").includes("TIMEOUT"));
    } else if (filterType === "TICKS") {
      this.filteredTrades = this.allTrades.filter(t => t.has_ticks === true);
    } else {
      this.filteredTrades = [...this.allTrades];
    }

    this.populateTradeSelect(isInitial);
  }

  populateTradeSelect(isInitial = false) {
    const tradeSelect = document.getElementById("forensicTradeSelect");
    if (!tradeSelect) return;

    tradeSelect.innerHTML = "";
    if (this.filteredTrades.length === 0) {
      tradeSelect.innerHTML = "<option value=''>No trades match filter</option>";
      return;
    }

    this.filteredTrades.forEach(t => {
      const opt = document.createElement("option");
      opt.value = t.trade_id;
      const pnlVal = Number(t.pnl_usdt || 0);
      const sign = pnlVal >= 0 ? "+" : "";
      const pnlStr = `${sign}${pnlVal.toFixed(4)} USDT`;
      const tickIcon = t.has_ticks ? "⚡" : "📊";
      opt.textContent = `${tickIcon} #${t.trade_id} | ${t.direction} | ${t.exit_reason} | ${pnlStr} (${t.date})`;
      tradeSelect.appendChild(opt);
    });

    const tradeExists = this.filteredTrades.some(t => t.trade_id === this.activeTradeId);
    if (!tradeExists || isInitial) {
      this.activeTradeId = this.filteredTrades[0].trade_id;
    }
    tradeSelect.value = this.activeTradeId;

    const jumpInput = document.getElementById("jumpTradeInput");
    if (jumpInput) jumpInput.value = this.activeTradeId;

    this.loadTrade(this.activeRunId, this.activeTradeId);
  }

  stepTrade(delta) {
    if (!this.filteredTrades || this.filteredTrades.length === 0) return;
    const currIdx = this.filteredTrades.findIndex(t => t.trade_id === this.activeTradeId);
    const nextIdx = Math.max(0, Math.min(this.filteredTrades.length - 1, (currIdx === -1 ? 0 : currIdx) + delta));
    this.activeTradeId = this.filteredTrades[nextIdx].trade_id;

    const tradeSelect = document.getElementById("forensicTradeSelect");
    if (tradeSelect) tradeSelect.value = this.activeTradeId;

    const jumpInput = document.getElementById("jumpTradeInput");
    if (jumpInput) jumpInput.value = this.activeTradeId;

    this.loadTrade(this.activeRunId, this.activeTradeId);
  }

  jumpToTrade(tradeId) {
    if (!tradeId || isNaN(tradeId)) return;
    const target = this.allTrades.find(t => t.trade_id === tradeId);
    if (!target) {
      alert(`Trade #${tradeId} was not found in backtest run ${this.activeRunId}.`);
      return;
    }

    // Check if in current filtered list
    const inFilter = this.filteredTrades.some(t => t.trade_id === tradeId);
    if (!inFilter) {
      // Reset filter chips to ALL
      document.querySelectorAll("[data-trade-filter]").forEach(c => {
        c.classList.toggle("active", c.dataset.tradeFilter === "ALL");
      });
      this.activeTradeFilter = "ALL";
      this.filteredTrades = [...this.allTrades];
      this.populateTradeSelect();
    }

    this.activeTradeId = tradeId;
    const tradeSelect = document.getElementById("forensicTradeSelect");
    if (tradeSelect) tradeSelect.value = tradeId;

    const jumpInput = document.getElementById("jumpTradeInput");
    if (jumpInput) jumpInput.value = tradeId;

    this.loadTrade(this.activeRunId, tradeId);
  }

  openAllTradesModal() {
    const modal = document.getElementById("allTradesModal");
    const titleEl = document.getElementById("modalRunTitle");
    if (!modal) return;

    if (titleEl) titleEl.textContent = this.activeRunId || "--";
    this.modalFilter = "ALL";
    document.querySelectorAll("[data-modal-filter]").forEach(c => {
      c.classList.toggle("active", c.dataset.modalFilter === "ALL");
    });
    const searchInput = document.getElementById("modalTradeSearch");
    if (searchInput) searchInput.value = "";

    this.renderModalTable();
    modal.style.display = "flex";
  }

  closeAllTradesModal() {
    const modal = document.getElementById("allTradesModal");
    if (modal) modal.style.display = "none";
  }

  renderModalTable() {
    const tbody = document.getElementById("allTradesTableBody");
    const countEl = document.getElementById("modalTradesCount");
    const searchInput = document.getElementById("modalTradeSearch");
    if (!tbody) return;

    const query = (searchInput ? searchInput.value.trim().toLowerCase() : "");

    let list = this.allTrades;
    if (this.modalFilter === "WIN") {
      list = list.filter(t => t.pnl_usdt > 0);
    } else if (this.modalFilter === "LOSS") {
      list = list.filter(t => t.pnl_usdt < 0);
    } else if (this.modalFilter === "TIMEOUT") {
      list = list.filter(t => (t.exit_reason || "").includes("TIMEOUT"));
    } else if (this.modalFilter === "TICKS") {
      list = list.filter(t => t.has_ticks === true);
    }

    if (query) {
      list = list.filter(t => 
        String(t.trade_id).includes(query) ||
        (t.time_utc || "").toLowerCase().includes(query) ||
        (t.direction || "").toLowerCase().includes(query) ||
        (t.exit_reason || "").toLowerCase().includes(query) ||
        String(t.pnl_usdt).includes(query)
      );
    }

    if (countEl) countEl.textContent = `Showing ${list.length} of ${this.allTrades.length} trades`;

    // Display first 300 to maintain silky smooth 60fps
    const displayList = list.slice(0, 300);
    tbody.innerHTML = "";

    displayList.forEach(t => {
      const tr = document.createElement("tr");
      const isWin = t.pnl_usdt > 0;
      const isTimeout = (t.exit_reason || "").includes("TIMEOUT");
      const pnlClass = isWin ? "profit mono" : (t.pnl_usdt < 0 ? "loss mono" : "mono");
      const reasonBadgeClass = isWin ? "profit" : (isTimeout ? "timeout" : "loss");
      const sign = t.pnl_usdt >= 0 ? "+" : "";

      tr.innerHTML = `
        <td class="mono" style="font-weight: 700; color: var(--accent-cyan);">#${t.trade_id}</td>
        <td class="mono" style="font-size: 0.75rem;">${t.time_utc}</td>
        <td><span class="status-chip ${t.direction.toLowerCase()}">${t.direction}</span></td>
        <td class="mono">${t.duration_s}s</td>
        <td><span class="status-chip ${reasonBadgeClass}">${t.exit_reason}</span></td>
        <td class="${pnlClass}">${sign}${t.pnl_usdt.toFixed(4)} USDT</td>
        <td class="${pnlClass}">${sign}${t.roe_pct.toFixed(2)}%</td>
        <td>
          <span class="data-feed-badge ${t.has_ticks ? 'high-res' : 'candle-res'}">
            ${t.has_ticks ? '⚡ Millisecond Ticks' : '📊 1m Candle'}
          </span>
        </td>
        <td>
          <button class="btn btn-secondary btn-sm" onclick="window.forensicsLab.jumpToTrade(${t.trade_id}); window.forensicsLab.closeAllTradesModal();">
            Analyze 🔎
          </button>
        </td>
      `;
      tbody.appendChild(tr);
    });

    if (list.length > 300) {
      const trNotice = document.createElement("tr");
      trNotice.innerHTML = `<td colspan="9" style="text-align: center; color: var(--text-dim); padding: 0.75rem;">
        Displaying first 300 matching trades. Use search bar to narrow down further.
      </td>`;
      tbody.appendChild(trNotice);
    }
  }

  async loadTrade(runId, tradeId) {
    if (!runId || !tradeId) return;
    this.activeRunId = runId;
    this.activeTradeId = tradeId;

    // Reset replay state
    this.pauseReplay();
    this.currentTickIndex = 0;

    const overlay = document.getElementById("forensicLoadingOverlay");
    if (overlay) overlay.style.display = "flex";

    try {
      const res = await fetch(`/api/forensics/trade/${runId}/${tradeId}?timeframe=${this.activeTimeframe}`);
      if (!res.ok) throw new Error(`Trade #${tradeId} context fetch failed: ${res.statusText}`);
      this.tradeContext = await res.json();

      this.renderChartData();
      this.renderTradeInspector();
      this.initReplaySlider();
    } catch (e) {
      console.error("[!] Failed loading forensic trade context:", e);
      alert(`Could not load forensic data for trade #${tradeId}: ${e.message}`);
    } finally {
      if (overlay) overlay.style.display = "none";
    }
  }

  renderChartData() {
    if (!this.tradeContext || !this.candleSeries) return;
    const { trade, candles, indicators } = this.tradeContext;

    // 1. Candlesticks
    const candleData = (candles || []).map(c => ({
      time: c.time,
      open: c.open,
      high: c.high,
      low: c.low,
      close: c.close
    }));
    this.candleSeries.setData(candleData);

    // 2. Volumes
    if (this.volumeSeries) {
      const volData = (candles || []).map(c => ({
        time: c.time,
        value: c.volume,
        color: c.close >= c.open ? "rgba(0, 240, 144, 0.25)" : "rgba(255, 51, 102, 0.25)"
      }));
      this.volumeSeries.setData(volData);
    }

    // 3. EMAs
    if (this.fastEmaSeries && indicators && indicators.ema_fast) {
      this.fastEmaSeries.setData(indicators.ema_fast);
    }
    if (this.slowEmaSeries && indicators && indicators.ema_slow) {
      this.slowEmaSeries.setData(indicators.ema_slow);
    }

    // 4. Stoch RSI
    if (this.stochKSeries && indicators && indicators.stoch_rsi) {
      this.stochKSeries.setData(indicators.stoch_rsi.k || []);
      this.stochDSeries.setData(indicators.stoch_rsi.d || []);
    }

    // 5. Clean up old price lines
    this.priceLines.forEach(pl => this.candleSeries.removePriceLine(pl));
    this.priceLines = [];

    // 6. Draw Entry, TP, and SL Price Lines
    const entryLine = this.candleSeries.createPriceLine({
      price: trade.entry_price,
      color: "#00d2ff",
      lineWidth: 1.5,
      lineStyle: LightweightCharts.LineStyle.Solid,
      axisLabelVisible: true,
      title: `ENTRY (${trade.entry_price})`
    });
    this.priceLines.push(entryLine);

    if (trade.tp_price > 0) {
      const tpLine = this.candleSeries.createPriceLine({
        price: trade.tp_price,
        color: "#00f090",
        lineWidth: 1.5,
        lineStyle: LightweightCharts.LineStyle.Dashed,
        axisLabelVisible: true,
        title: `TP (${trade.tp_price})`
      });
      this.priceLines.push(tpLine);
    }

    if (trade.sl_price > 0) {
      const slLine = this.candleSeries.createPriceLine({
        price: trade.sl_price,
        color: "#ff3366",
        lineWidth: 1.5,
        lineStyle: LightweightCharts.LineStyle.Dashed,
        axisLabelVisible: true,
        title: `SL (${trade.sl_price})`
      });
      this.priceLines.push(slLine);
    }

    // 7. Markers (Entry and Exit)
    const entryTimeSec = Math.floor(trade.open_time_ms / 1000);
    const exitTimeSec = Math.floor(trade.close_time_ms / 1000);

    const isLong = trade.direction === "LONG";
    const markers = [];

    markers.push({
      time: entryTimeSec,
      position: isLong ? "belowBar" : "aboveBar",
      color: "#00d2ff",
      shape: isLong ? "arrowUp" : "arrowDown",
      text: `${trade.direction} ENTRY @ ${trade.entry_price}`
    });

    const isWin = trade.realized_pnl_usdt > 0;
    const isTimeout = trade.exit_reason.includes("TIMEOUT");
    const exitColor = isWin ? "#00f090" : (isTimeout ? "#ffb800" : "#ff3366");

    markers.push({
      time: exitTimeSec,
      position: isLong ? "aboveBar" : "belowBar",
      color: exitColor,
      shape: "circle",
      text: `EXIT: ${trade.exit_reason} (${trade.exit_price})`
    });

    this.candleSeries.setMarkers(markers);

    // Zoom chart centered on trade
    if (this.chart) {
      this.chart.timeScale().fitContent();
    }
  }

  renderTradeInspector() {
    if (!this.tradeContext) return;
    const { trade, mfe_mae, filter_state, post_exit, strategy_state, timeline } = this.tradeContext;

    // Header & Badges
    document.getElementById("inspTradeId").textContent = `#${trade.trade_id}`;
    
    const feedBadge = document.getElementById("inspFeedBadge");
    if (feedBadge) {
      if (this.tradeContext.is_synthetic) {
        feedBadge.className = "data-feed-badge candle-res";
        feedBadge.textContent = "📊 1m Candle Fallback";
        feedBadge.title = "Raw tick files not present for this trade's date window. Forensic replay evaluated against 1m candles.";
      } else {
        const tickCount = (this.tradeContext.ticks || []).length;
        feedBadge.className = "data-feed-badge high-res";
        feedBadge.textContent = `⚡ Raw Binance Ticks (${tickCount})`;
        feedBadge.title = "Millisecond-accurate raw Binance tick data loaded from local disk.";
      }
    }

    const dirBadge = document.getElementById("inspDirectionBadge");
    dirBadge.textContent = trade.direction;
    dirBadge.className = `status-chip ${trade.direction.toLowerCase()}`;

    const exitBadge = document.getElementById("inspExitReasonBadge");
    exitBadge.textContent = trade.exit_reason;
    if (trade.realized_pnl_usdt > 0) {
      exitBadge.className = "status-chip profit";
    } else if (trade.exit_reason.includes("TIMEOUT")) {
      exitBadge.className = "status-chip timeout";
    } else {
      exitBadge.className = "status-chip loss";
    }

    // Execution Prices
    document.getElementById("inspEntryPrice").textContent = trade.entry_price;
    document.getElementById("inspExitPrice").textContent = trade.exit_price;
    document.getElementById("inspTpPrice").textContent = trade.tp_price;
    document.getElementById("inspSlPrice").textContent = trade.sl_price;

    // Performance
    const pnlEl = document.getElementById("inspPnl");
    const sign = trade.realized_pnl_usdt >= 0 ? "+" : "";
    pnlEl.textContent = `${sign}${trade.realized_pnl_usdt.toFixed(4)} USDT`;
    pnlEl.className = trade.realized_pnl_usdt >= 0 ? "stat-val profit mono" : "stat-val loss mono";

    const roeEl = document.getElementById("inspRoe");
    roeEl.textContent = `${sign}${trade.roe_percentage.toFixed(2)}%`;
    roeEl.className = trade.roe_percentage >= 0 ? "stat-val profit mono" : "stat-val loss mono";

    document.getElementById("inspDuration").textContent = `${trade.duration_seconds.toFixed(1)}s`;
    document.getElementById("inspOpenTime").textContent = trade.open_time_utc;
    document.getElementById("inspCloseTime").textContent = trade.close_time_utc;

    // MFE / MAE
    if (mfe_mae) {
      document.getElementById("inspMfe").textContent = `+${mfe_mae.mfe_ticks} ticks (+${mfe_mae.mfe_pct}%)`;
      document.getElementById("inspMae").textContent = `-${mfe_mae.mae_ticks} ticks (-${mfe_mae.mae_pct}%)`;
    }

    // Filters
    const filterContainer = document.getElementById("inspFilterContainer");
    if (filterContainer && filter_state) {
      filterContainer.innerHTML = "";
      Object.entries(filter_state).forEach(([k, f]) => {
        const item = document.createElement("div");
        item.className = "filter-badge-item";
        const statusClass = f.status === "PASS" ? "filter-pass" : (f.status === "FAIL" ? "filter-fail" : "filter-disabled");
        item.innerHTML = `
          <span class="filter-name">${f.name}</span>
          <span class="filter-status ${statusClass}">${f.status}</span>
        `;
        filterContainer.appendChild(item);
      });
    }

    // Post Exit Summary
    const postExitEl = document.getElementById("inspPostExitSummary");
    if (postExitEl && post_exit) {
      postExitEl.textContent = post_exit.summary || "No post-exit activity recorded.";
      if (post_exit.tp_reached_after_exit) {
        postExitEl.className = "post-exit-box profit-glow";
      } else if (post_exit.sl_reached_after_exit) {
        postExitEl.className = "post-exit-box loss-glow";
      } else {
        postExitEl.className = "post-exit-box";
      }
    }

    // Timeline List
    const timelineContainer = document.getElementById("inspTimelineContainer");
    if (timelineContainer && timeline) {
      timelineContainer.innerHTML = "";
      timeline.forEach(t => {
        const row = document.createElement("div");
        row.className = "timeline-event-row";
        const deltaClass = t.delta_ticks > 0 ? "profit" : (t.delta_ticks < 0 ? "loss" : "");
        row.innerHTML = `
          <div class="tl-time">${t.elapsed_sec.toFixed(1)}s</div>
          <div class="tl-desc">${t.desc}</div>
          <div class="tl-price mono ${deltaClass}">${t.price} (${t.delta_ticks >= 0 ? "+" : ""}${t.delta_ticks}t)</div>
        `;
        timelineContainer.appendChild(row);
      });
    }
  }

  // =========================================================================
  // REPLAY ENGINE
  // =========================================================================

  initReplaySlider() {
    const slider = document.getElementById("replayScrubSlider");
    const ticks = (this.tradeContext && this.tradeContext.ticks) ? this.tradeContext.ticks : [];
    if (slider) {
      slider.min = 0;
      slider.max = Math.max(0, ticks.length - 1);
      slider.value = 0;
    }
    this.updateReplayDisplay(0);
  }

  playReplay() {
    const ticks = (this.tradeContext && this.tradeContext.ticks) ? this.tradeContext.ticks : [];
    if (ticks.length === 0) return;

    this.isPlaying = true;
    document.getElementById("btnReplayPlay").style.display = "none";
    document.getElementById("btnReplayPause").style.display = "inline-flex";

    const stepMs = Math.max(20, Math.floor(100 / this.replaySpeed));
    this.replayInterval = setInterval(() => {
      if (this.currentTickIndex >= ticks.length - 1) {
        this.pauseReplay();
        return;
      }
      this.currentTickIndex++;
      this.seekReplay(this.currentTickIndex);
    }, stepMs);
  }

  pauseReplay() {
    this.isPlaying = false;
    if (this.replayInterval) {
      clearInterval(this.replayInterval);
      this.replayInterval = null;
    }
    const btnPlay = document.getElementById("btnReplayPlay");
    const btnPause = document.getElementById("btnReplayPause");
    if (btnPlay) btnPlay.style.display = "inline-flex";
    if (btnPause) btnPause.style.display = "none";
  }

  resetReplay() {
    this.pauseReplay();
    this.seekReplay(0);
  }

  stepReplay(delta) {
    this.pauseReplay();
    const ticks = (this.tradeContext && this.tradeContext.ticks) ? this.tradeContext.ticks : [];
    if (ticks.length === 0) return;
    const nextIdx = Math.max(0, Math.min(ticks.length - 1, this.currentTickIndex + delta));
    this.seekReplay(nextIdx);
  }

  seekReplay(index) {
    this.currentTickIndex = index;
    const slider = document.getElementById("replayScrubSlider");
    if (slider) slider.value = index;
    this.updateReplayDisplay(index);
  }

  updateReplayDisplay(index) {
    const ticks = (this.tradeContext && this.tradeContext.ticks) ? this.tradeContext.ticks : [];
    if (ticks.length === 0 || !ticks[index]) return;

    const tick = ticks[index];
    const trade = this.tradeContext.trade;
    const elapsedSec = ((tick.time_ms - trade.open_time_ms) / 1000.0).toFixed(1);

    document.getElementById("replayCurrentPrice").textContent = tick.price.toFixed(4);
    document.getElementById("replayElapsedSec").textContent = `${elapsedSec}s`;

    // Live Unrealized PnL & Distance to TP/SL
    const isLong = trade.direction === "LONG";
    const deltaTicks = tick.delta_ticks;
    const deltaEl = document.getElementById("replayCurrentDelta");
    if (deltaEl) {
      deltaEl.textContent = `${deltaTicks >= 0 ? "+" : ""}${deltaTicks} ticks`;
      deltaEl.className = deltaTicks >= 0 ? "mono profit" : "mono loss";
    }

    const toTp = isLong ? (trade.tp_price - tick.price) : (tick.price - trade.tp_price);
    const toSl = isLong ? (tick.price - trade.sl_price) : (trade.sl_price - tick.price);
    const pu = this.tradeContext.strategy_state.price_unit || 0.0001;

    document.getElementById("replayToTp").textContent = `${(toTp / pu).toFixed(1)}t`;
    document.getElementById("replayToSl").textContent = `${(toSl / pu).toFixed(1)}t`;

    const inPosPill = document.getElementById("replayInPositionPill");
    if (inPosPill) {
      if (tick.is_in_position) {
        inPosPill.textContent = "IN POSITION";
        inPosPill.className = "status-chip active-pulse";
      } else {
        inPosPill.textContent = "POST-EXIT";
        inPosPill.className = "status-chip neutral";
      }
    }
  }

  // =========================================================================
  // WHAT-IF COUNTERFACTUAL EXIT SIMULATOR
  // =========================================================================

  async runWhatIfSimulation() {
    if (!this.activeRunId || !this.activeTradeId) return;

    const timeoutVal = document.getElementById("whatIfTimeoutSelect").value;
    const tpVal = document.getElementById("whatIfTpSelect").value;

    const payload = {
      timeout_seconds: timeoutVal === "NONE" ? null : parseFloat(timeoutVal),
      tp_ticks: tpVal === "DEFAULT" ? null : parseInt(tpVal, 10)
    };

    try {
      const res = await fetch(`/api/forensics/trade/${this.activeRunId}/${this.activeTradeId}/what-if`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      if (!res.ok) throw new Error("What-if calculation error");
      const result = await res.json();

      this.renderWhatIfResult(result);
    } catch (e) {
      console.error("[!] Error in what-if simulation:", e);
      alert(`Simulation failed: ${e.message}`);
    }
  }

  renderWhatIfResult(result) {
    const container = document.getElementById("whatIfResultContainer");
    if (!container) return;

    const { original_outcome, hypothetical_outcome, rules_applied } = result;
    const pnlDiff = hypothetical_outcome.pnl_delta_vs_actual;
    const diffSign = pnlDiff >= 0 ? "+" : "";
    const diffClass = pnlDiff > 0 ? "profit" : (pnlDiff < 0 ? "loss" : "neutral");

    container.innerHTML = `
      <div class="what-if-comparison-grid">
        <div class="wi-col original">
          <div class="wi-header">Original Backtest</div>
          <div class="wi-metric"><span class="wi-label">Reason:</span> <strong>${original_outcome.exit_reason}</strong></div>
          <div class="wi-metric"><span class="wi-label">Price:</span> <strong>${original_outcome.exit_price}</strong></div>
          <div class="wi-metric"><span class="wi-label">Duration:</span> <strong>${original_outcome.duration_seconds.toFixed(1)}s</strong></div>
          <div class="wi-metric"><span class="wi-label">PnL:</span> <strong class="${original_outcome.pnl_usdt >= 0 ? 'profit' : 'loss'}">${original_outcome.pnl_usdt.toFixed(4)} USDT</strong></div>
        </div>

        <div class="wi-col hypothetical">
          <div class="wi-header">Hypothetical Simulation</div>
          <div class="wi-metric"><span class="wi-label">Reason:</span> <strong>${hypothetical_outcome.exit_reason}</strong></div>
          <div class="wi-metric"><span class="wi-label">Price:</span> <strong>${hypothetical_outcome.exit_price}</strong></div>
          <div class="wi-metric"><span class="wi-label">Duration:</span> <strong>${hypothetical_outcome.duration_seconds.toFixed(1)}s</strong></div>
          <div class="wi-metric"><span class="wi-label">PnL:</span> <strong class="${hypothetical_outcome.pnl_usdt >= 0 ? 'profit' : 'loss'}">${hypothetical_outcome.pnl_usdt.toFixed(4)} USDT</strong></div>
        </div>
      </div>

      <div class="wi-delta-badge ${diffClass}">
        <span>PnL Delta:</span> <strong>${diffSign}${pnlDiff.toFixed(4)} USDT (${diffSign}${hypothetical_outcome.roe_pct - original_outcome.roe_pct > 0 ? '+' : ''}${(hypothetical_outcome.roe_pct - original_outcome.roe_pct).toFixed(2)}% ROE)</strong>
      </div>
    `;
    container.style.display = "block";
  }
}

// Global instance
window.forensicsLab = new ForensicsController();
