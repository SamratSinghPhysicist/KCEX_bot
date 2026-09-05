# 🧭 Master Quantitative Synthesis Guide: TRUMP_USDT - STOCH_RSI
> **Backtest Run ID:** `backtest_TRUMP_USDT_20260905_060642` | **Total Partitioned Chunks:** `36`

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
| `chunk_01_2026-W01.md` | `Week 01 (2026-W01)` | `693` | `80.81%` | `-0.0420` | `No` |
| `chunk_02_2026-W02.md` | `Week 02 (2026-W02)` | `1,260` | `82.30%` | `-0.0312` | `No` |
| `chunk_03_2026-W03.md` | `Week 03 (2026-W03)` | `1,172` | `83.36%` | `+0.0008` | `No` |
| `chunk_04_2026-W04.md` | `Week 04 (2026-W04)` | `1,099` | `82.98%` | `-0.0092` | `No` |
| `chunk_05_2026-W05.md` | `Week 05 (2026-W05)` | `1,110` | `86.40%` | `+0.0816` | `No` |
| `chunk_06_2026-W06.md` | `Week 06 (2026-W06)` | `1,238` | `84.89%` | `+0.0464` | `No` |
| `chunk_07_2026-W07.md` | `Week 07 (2026-W07)` | `1,172` | `84.13%` | `+0.0224` | `No` |
| `chunk_08_2026-W08.md` | `Week 08 (2026-W08)` | `1,193` | `83.24%` | `-0.0028` | `No` |
| `chunk_09_2026-W09.md` | `Week 09 (2026-W09)` | `1,172` | `83.28%` | `-0.0016` | `No` |
| `chunk_10_2026-W10.md` | `Week 10 (2026-W10)` | `1,147` | `83.09%` | `-0.0068` | `No` |
| `chunk_11_2026-W11.md` | `Week 11 (2026-W11)` | `1,267` | `85.48%` | `+0.0652` | `No` |
| `chunk_12_2026-W12.md` | `Week 12 (2026-W12)` | `1,209` | `83.54%` | `+0.0060` | `No` |
| `chunk_13_2026-W13.md` | `Week 13 (2026-W13)` | `1,053` | `85.00%` | `+0.0420` | `No` |
| `chunk_14_2026-W14.md` | `Week 14 (2026-W14)` | `1,039` | `86.53%` | `+0.0796` | `No` |
| `chunk_15_2026-W15.md` | `Week 15 (2026-W15)` | `1,050` | `84.67%` | `+0.0336` | `No` |
| `chunk_16_2026-W16.md` | `Week 16 (2026-W16)` | `1,031` | `83.32%` | `-0.0004` | `No` |
| `chunk_17_2026-W17.md` | `Week 17 (2026-W17)` | `1,080` | `84.72%` | `+0.0360` | `No` |
| `chunk_18_2026-W18.md` | `Week 18 (2026-W18)` | `870` | `85.40%` | `+0.0432` | `No` |
| `chunk_19_2026-W19.md` | `Week 19 (2026-W19)` | `962` | `86.90%` | `+0.0824` | `No` |
| `chunk_20_2026-W20.md` | `Week 20 (2026-W20)` | `914` | `86.65%` | `+0.0728` | `No` |
| `chunk_21_2026-W21.md` | `Week 21 (2026-W21)` | `898` | `86.08%` | `+0.0592` | `No` |
| `chunk_22_2026-W22.md` | `Week 22 (2026-W22)` | `815` | `85.64%` | `+0.0452` | `No` |
| `chunk_23_2026-W23.md` | `Week 23 (2026-W23)` | `1,148` | `83.71%` | `+0.0116` | `No` |
| `chunk_24_2026-W24.md` | `Week 24 (2026-W24)` | `1,147` | `85.27%` | `+0.0532` | `No` |
| `chunk_25_2026-W25.md` | `Week 25 (2026-W25)` | `1,020` | `85.49%` | `+0.0528` | `No` |
| `chunk_26_2026-W26.md` | `Week 26 (2026-W26)` | `833` | `88.24%` | `+0.0980` | `No` |
| `chunk_27_2026-W27.md` | `Week 27 (2026-W27)` | `821` | `86.48%` | `+0.0620` | `⚡ Yes` |
| `chunk_28_2026-W28.md` | `Week 28 (2026-W28)` | `674` | `88.58%` | `+0.0848` | `⚡ Yes` |
| `chunk_29_2026-W29.md` | `Week 29 (2026-W29)` | `663` | `84.46%` | `+0.0180` | `⚡ Yes` |
| `chunk_30_2026-W30.md` | `Week 30 (2026-W30)` | `541` | `85.58%` | `+0.0292` | `⚡ Yes` |
| `chunk_31_2026-W31.md` | `Week 31 (2026-W31)` | `609` | `87.19%` | `+0.0832` | `⚡ Yes` |
| `chunk_32_2026-W32.md` | `Week 32 (2026-W32)` | `502` | `84.06%` | `+0.0392` | `⚡ Yes` |
| `chunk_33_2026-W33.md` | `Week 33 (2026-W33)` | `513` | `81.87%` | `+0.0188` | `⚡ Yes` |
| `chunk_34_2026-W34.md` | `Week 34 (2026-W34)` | `972` | `86.93%` | `+0.0944` | `⚡ Yes` |
| `chunk_35_2026-W35.md` | `Week 35 (2026-W35)` | `1,362` | `83.99%` | `+0.0216` | `⚡ Yes` |
| `chunk_36_2026-W36.md` | `Week 36 (2026-W36)` | `1` | `100.00%` | `+0.0004` | `⚡ Yes` |