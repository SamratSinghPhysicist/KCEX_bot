# 🧭 Master Quantitative Synthesis Guide: TRUMP_USDT - EMA_CROSSOVER
> **Backtest Run ID:** `backtest_TRUMP_USDT_20260905_061214` | **Total Partitioned Chunks:** `35`

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
| `chunk_01_2026-W01.md` | `Week 01 (2026-W01)` | `344` | `87.21%` | `+0.0320` | `No` |
| `chunk_02_2026-W02.md` | `Week 02 (2026-W02)` | `635` | `82.68%` | `-0.0100` | `No` |
| `chunk_03_2026-W03.md` | `Week 03 (2026-W03)` | `606` | `83.83%` | `+0.0072` | `No` |
| `chunk_04_2026-W04.md` | `Week 04 (2026-W04)` | `592` | `85.81%` | `+0.0352` | `No` |
| `chunk_05_2026-W05.md` | `Week 05 (2026-W05)` | `588` | `85.03%` | `+0.0240` | `No` |
| `chunk_06_2026-W06.md` | `Week 06 (2026-W06)` | `646` | `84.52%` | `+0.0184` | `No` |
| `chunk_07_2026-W07.md` | `Week 07 (2026-W07)` | `570` | `85.61%` | `+0.0312` | `No` |
| `chunk_08_2026-W08.md` | `Week 08 (2026-W08)` | `571` | `84.41%` | `+0.0148` | `No` |
| `chunk_09_2026-W09.md` | `Week 09 (2026-W09)` | `602` | `85.38%` | `+0.0296` | `No` |
| `chunk_10_2026-W10.md` | `Week 10 (2026-W10)` | `572` | `85.14%` | `+0.0248` | `No` |
| `chunk_11_2026-W11.md` | `Week 11 (2026-W11)` | `621` | `86.80%` | `+0.0516` | `No` |
| `chunk_12_2026-W12.md` | `Week 12 (2026-W12)` | `610` | `84.43%` | `+0.0160` | `No` |
| `chunk_13_2026-W13.md` | `Week 13 (2026-W13)` | `540` | `84.81%` | `+0.0192` | `No` |
| `chunk_14_2026-W14.md` | `Week 14 (2026-W14)` | `544` | `84.38%` | `+0.0136` | `No` |
| `chunk_15_2026-W15.md` | `Week 15 (2026-W15)` | `501` | `85.63%` | `+0.0276` | `No` |
| `chunk_16_2026-W16.md` | `Week 16 (2026-W16)` | `574` | `88.50%` | `+0.0712` | `No` |
| `chunk_17_2026-W17.md` | `Week 17 (2026-W17)` | `554` | `87.18%` | `+0.0512` | `No` |
| `chunk_18_2026-W18.md` | `Week 18 (2026-W18)` | `528` | `88.64%` | `+0.0672` | `No` |
| `chunk_19_2026-W19.md` | `Week 19 (2026-W19)` | `542` | `86.53%` | `+0.0416` | `No` |
| `chunk_20_2026-W20.md` | `Week 20 (2026-W20)` | `534` | `88.39%` | `+0.0648` | `No` |
| `chunk_21_2026-W21.md` | `Week 21 (2026-W21)` | `489` | `87.73%` | `+0.0516` | `No` |
| `chunk_22_2026-W22.md` | `Week 22 (2026-W22)` | `453` | `87.20%` | `+0.0420` | `No` |
| `chunk_23_2026-W23.md` | `Week 23 (2026-W23)` | `567` | `87.13%` | `+0.0516` | `No` |
| `chunk_24_2026-W24.md` | `Week 24 (2026-W24)` | `567` | `86.77%` | `+0.0468` | `No` |
| `chunk_25_2026-W25.md` | `Week 25 (2026-W25)` | `548` | `84.12%` | `+0.0104` | `No` |
| `chunk_26_2026-W26.md` | `Week 26 (2026-W26)` | `460` | `85.43%` | `+0.0232` | `No` |
| `chunk_27_2026-W27.md` | `Week 27 (2026-W27)` | `414` | `82.61%` | `-0.0072` | `⚡ Yes` |
| `chunk_28_2026-W28.md` | `Week 28 (2026-W28)` | `425` | `89.41%` | `+0.0620` | `⚡ Yes` |
| `chunk_29_2026-W29.md` | `Week 29 (2026-W29)` | `402` | `83.33%` | `-0.0000` | `⚡ Yes` |
| `chunk_30_2026-W30.md` | `Week 30 (2026-W30)` | `400` | `88.00%` | `+0.0448` | `⚡ Yes` |
| `chunk_31_2026-W31.md` | `Week 31 (2026-W31)` | `357` | `85.43%` | `+0.0360` | `⚡ Yes` |
| `chunk_32_2026-W32.md` | `Week 32 (2026-W32)` | `306` | `83.66%` | `+0.0208` | `⚡ Yes` |
| `chunk_33_2026-W33.md` | `Week 33 (2026-W33)` | `322` | `79.50%` | `-0.0040` | `⚡ Yes` |
| `chunk_34_2026-W34.md` | `Week 34 (2026-W34)` | `537` | `83.80%` | `+0.0120` | `⚡ Yes` |
| `chunk_35_2026-W35.md` | `Week 35 (2026-W35)` | `631` | `84.79%` | `+0.0220` | `⚡ Yes` |