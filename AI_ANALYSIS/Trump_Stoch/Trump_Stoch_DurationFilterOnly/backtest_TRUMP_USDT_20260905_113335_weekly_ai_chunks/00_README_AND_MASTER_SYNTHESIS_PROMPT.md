# 🧭 Master Quantitative Synthesis Guide: TRUMP_USDT - STOCH_RSI
> **Backtest Run ID:** `backtest_TRUMP_USDT_20260905_113335` | **Total Partitioned Chunks:** `36`

---

## How to Feed These Cropped Chunks to Your AI Model (Gemini, Claude, ChatGPT)
Feeding an entire 8-month backtest into an AI model overwhelms its context and degrades its reasoning.
This package partitions the backtest into smaller, ultra-dense forensic slices containing granular indicators,
millisecond tick trajectories, MFE/MAE excursions, and post-exit bounce forensics.

### Recommended Step-by-Step AI Interaction Workflow:

1. **Step 1: Feed Chunk 1 (e.g. Month 1)**
   - Upload or paste `chunk_01_*.md` into your AI chat.
   - The AI will analyze the loss autopsy table, compare the control group winners, and provide initial filter rules.

2. **Step 2: Feed Chunks 2 through N Sequentially**
   - Prompt the AI: *'Here is Chunk X. Test your previous filter rules against this new data. Did they prevent the losses in this chunk? What edge cases or new loss patterns emerged?'*

3. **Step 3: Final Synthesis Prompt**
   - After feeding the chunks, prompt the AI:
     *'Synthesize all insights across all chunks into a Unified Regime-to-Strategy Switcher Matrix and provide the final 3 production-ready Python filter rules to eliminate losses.'*

---

## Partitioned Chunks Overview in This Package
| Chunk File | Label / Period | Trades Count | Win Rate | Net PnL (USDT) | Has Ticks |
| :--- | :--- | :---: | :---: | :---: | :---: |
| `chunk_01_2026-W01.md` | `Week 01 (2026-W01)` | `808` | `62.75%` | `-0.0278` | `No` |
| `chunk_02_2026-W02.md` | `Week 02 (2026-W02)` | `1,409` | `64.80%` | `-0.0500` | `No` |
| `chunk_03_2026-W03.md` | `Week 03 (2026-W03)` | `1,386` | `60.89%` | `+0.0008` | `No` |
| `chunk_04_2026-W04.md` | `Week 04 (2026-W04)` | `1,405` | `57.08%` | `-0.0010` | `No` |
| `chunk_05_2026-W05.md` | `Week 05 (2026-W05)` | `1,349` | `62.27%` | `+0.0518` | `No` |
| `chunk_06_2026-W06.md` | `Week 06 (2026-W06)` | `1,362` | `70.26%` | `+0.0526` | `No` |
| `chunk_07_2026-W07.md` | `Week 07 (2026-W07)` | `1,412` | `60.20%` | `+0.0028` | `No` |
| `chunk_08_2026-W08.md` | `Week 08 (2026-W08)` | `1,389` | `63.50%` | `+0.0156` | `No` |
| `chunk_09_2026-W09.md` | `Week 09 (2026-W09)` | `1,353` | `65.71%` | `+0.0492` | `No` |
| `chunk_10_2026-W10.md` | `Week 10 (2026-W10)` | `1,417` | `60.41%` | `+0.0100` | `No` |
| `chunk_11_2026-W11.md` | `Week 11 (2026-W11)` | `1,417` | `69.44%` | `+0.0178` | `No` |
| `chunk_12_2026-W12.md` | `Week 12 (2026-W12)` | `1,425` | `63.30%` | `+0.0126` | `No` |
| `chunk_13_2026-W13.md` | `Week 13 (2026-W13)` | `1,384` | `57.44%` | `+0.0406` | `No` |
| `chunk_14_2026-W14.md` | `Week 14 (2026-W14)` | `1,383` | `54.74%` | `+0.0316` | `No` |
| `chunk_15_2026-W15.md` | `Week 15 (2026-W15)` | `1,372` | `56.12%` | `+0.0334` | `No` |
| `chunk_16_2026-W16.md` | `Week 16 (2026-W16)` | `1,379` | `57.72%` | `+0.0230` | `No` |
| `chunk_17_2026-W17.md` | `Week 17 (2026-W17)` | `1,361` | `60.62%` | `+0.0576` | `No` |
| `chunk_18_2026-W18.md` | `Week 18 (2026-W18)` | `1,392` | `50.57%` | `+0.0454` | `No` |
| `chunk_19_2026-W19.md` | `Week 19 (2026-W19)` | `1,361` | `55.33%` | `+0.0772` | `No` |
| `chunk_20_2026-W20.md` | `Week 20 (2026-W20)` | `1,316` | `53.72%` | `+0.0696` | `No` |
| `chunk_21_2026-W21.md` | `Week 21 (2026-W21)` | `1,390` | `51.37%` | `+0.0614` | `No` |
| `chunk_22_2026-W22.md` | `Week 22 (2026-W22)` | `1,371` | `51.50%` | `+0.0630` | `No` |
| `chunk_23_2026-W23.md` | `Week 23 (2026-W23)` | `1,393` | `59.30%` | `-0.0102` | `No` |
| `chunk_24_2026-W24.md` | `Week 24 (2026-W24)` | `1,401` | `64.17%` | `+0.0550` | `No` |
| `chunk_25_2026-W25.md` | `Week 25 (2026-W25)` | `1,405` | `54.80%` | `+0.0566` | `No` |
| `chunk_26_2026-W26.md` | `Week 26 (2026-W26)` | `1,342` | `50.89%` | `+0.0728` | `No` |
| `chunk_27_2026-W27.md` | `Week 27 (2026-W27)` | `1,347` | `48.85%` | `+0.0482` | `⚡ Yes` |
| `chunk_28_2026-W28.md` | `Week 28 (2026-W28)` | `1,313` | `45.70%` | `+0.0572` | `⚡ Yes` |
| `chunk_29_2026-W29.md` | `Week 29 (2026-W29)` | `1,336` | `42.66%` | `+0.0168` | `⚡ Yes` |
| `chunk_30_2026-W30.md` | `Week 30 (2026-W30)` | `1,321` | `40.35%` | `+0.0370` | `⚡ Yes` |
| `chunk_31_2026-W31.md` | `Week 31 (2026-W31)` | `1,319` | `38.59%` | `+0.0246` | `⚡ Yes` |
| `chunk_32_2026-W32.md` | `Week 32 (2026-W32)` | `1,294` | `36.86%` | `+0.0378` | `⚡ Yes` |
| `chunk_33_2026-W33.md` | `Week 33 (2026-W33)` | `1,298` | `37.06%` | `+0.0348` | `⚡ Yes` |
| `chunk_34_2026-W34.md` | `Week 34 (2026-W34)` | `1,357` | `63.30%` | `+0.0794` | `⚡ Yes` |
| `chunk_35_2026-W35.md` | `Week 35 (2026-W35)` | `1,414` | `75.18%` | `+0.0406` | `⚡ Yes` |
| `chunk_36_2026-W36.md` | `Week 36 (2026-W36)` | `1` | `100.00%` | `+0.0004` | `⚡ Yes` |