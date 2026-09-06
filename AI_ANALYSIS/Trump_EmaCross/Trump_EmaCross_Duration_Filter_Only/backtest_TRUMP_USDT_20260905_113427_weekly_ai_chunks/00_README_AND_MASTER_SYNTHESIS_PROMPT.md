# 🧭 Master Quantitative Synthesis Guide: TRUMP_USDT - EMA_CROSSOVER
> **Backtest Run ID:** `backtest_TRUMP_USDT_20260905_113427` | **Total Partitioned Chunks:** `35`

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
| `chunk_01_2026-W01.md` | `Week 01 (2026-W01)` | `370` | `67.30%` | `+0.0086` | `No` |
| `chunk_02_2026-W02.md` | `Week 02 (2026-W02)` | `695` | `66.19%` | `+0.0028` | `No` |
| `chunk_03_2026-W03.md` | `Week 03 (2026-W03)` | `728` | `60.58%` | `-0.0086` | `No` |
| `chunk_04_2026-W04.md` | `Week 04 (2026-W04)` | `730` | `56.99%` | `+0.0072` | `No` |
| `chunk_05_2026-W05.md` | `Week 05 (2026-W05)` | `682` | `58.06%` | `-0.0074` | `No` |
| `chunk_06_2026-W06.md` | `Week 06 (2026-W06)` | `715` | `66.71%` | `+0.0136` | `No` |
| `chunk_07_2026-W07.md` | `Week 07 (2026-W07)` | `651` | `61.14%` | `+0.0114` | `No` |
| `chunk_08_2026-W08.md` | `Week 08 (2026-W08)` | `654` | `59.63%` | `-0.0008` | `No` |
| `chunk_09_2026-W09.md` | `Week 09 (2026-W09)` | `694` | `62.68%` | `+0.0152` | `No` |
| `chunk_10_2026-W10.md` | `Week 10 (2026-W10)` | `681` | `59.18%` | `+0.0050` | `No` |
| `chunk_11_2026-W11.md` | `Week 11 (2026-W11)` | `695` | `69.21%` | `+0.0294` | `No` |
| `chunk_12_2026-W12.md` | `Week 12 (2026-W12)` | `670` | `63.88%` | `-0.0004` | `No` |
| `chunk_13_2026-W13.md` | `Week 13 (2026-W13)` | `673` | `57.80%` | `+0.0178` | `No` |
| `chunk_14_2026-W14.md` | `Week 14 (2026-W14)` | `718` | `54.87%` | `+0.0178` | `No` |
| `chunk_15_2026-W15.md` | `Week 15 (2026-W15)` | `649` | `55.62%` | `+0.0226` | `No` |
| `chunk_16_2026-W16.md` | `Week 16 (2026-W16)` | `706` | `60.06%` | `+0.0428` | `No` |
| `chunk_17_2026-W17.md` | `Week 17 (2026-W17)` | `695` | `62.30%` | `+0.0592` | `No` |
| `chunk_18_2026-W18.md` | `Week 18 (2026-W18)` | `742` | `55.12%` | `+0.0650` | `No` |
| `chunk_19_2026-W19.md` | `Week 19 (2026-W19)` | `746` | `53.35%` | `+0.0368` | `No` |
| `chunk_20_2026-W20.md` | `Week 20 (2026-W20)` | `772` | `55.70%` | `+0.0564` | `No` |
| `chunk_21_2026-W21.md` | `Week 21 (2026-W21)` | `716` | `49.30%` | `+0.0218` | `No` |
| `chunk_22_2026-W22.md` | `Week 22 (2026-W22)` | `693` | `48.34%` | `+0.0214` | `No` |
| `chunk_23_2026-W23.md` | `Week 23 (2026-W23)` | `670` | `64.78%` | `+0.0446` | `No` |
| `chunk_24_2026-W24.md` | `Week 24 (2026-W24)` | `686` | `64.14%` | `+0.0304` | `No` |
| `chunk_25_2026-W25.md` | `Week 25 (2026-W25)` | `746` | `53.75%` | `+0.0280` | `No` |
| `chunk_26_2026-W26.md` | `Week 26 (2026-W26)` | `769` | `47.98%` | `+0.0222` | `No` |
| `chunk_27_2026-W27.md` | `Week 27 (2026-W27)` | `731` | `42.95%` | `-0.0154` | `⚡ Yes` |
| `chunk_28_2026-W28.md` | `Week 28 (2026-W28)` | `731` | `42.95%` | `+0.0276` | `⚡ Yes` |
| `chunk_29_2026-W29.md` | `Week 29 (2026-W29)` | `729` | `42.94%` | `+0.0170` | `⚡ Yes` |
| `chunk_30_2026-W30.md` | `Week 30 (2026-W30)` | `775` | `41.55%` | `+0.0216` | `⚡ Yes` |
| `chunk_31_2026-W31.md` | `Week 31 (2026-W31)` | `805` | `34.78%` | `+0.0064` | `⚡ Yes` |
| `chunk_32_2026-W32.md` | `Week 32 (2026-W32)` | `738` | `33.74%` | `+0.0028` | `⚡ Yes` |
| `chunk_33_2026-W33.md` | `Week 33 (2026-W33)` | `771` | `34.89%` | `+0.0120` | `⚡ Yes` |
| `chunk_34_2026-W34.md` | `Week 34 (2026-W34)` | `723` | `61.27%` | `+0.0150` | `⚡ Yes` |
| `chunk_35_2026-W35.md` | `Week 35 (2026-W35)` | `658` | `75.38%` | `+0.0290` | `⚡ Yes` |