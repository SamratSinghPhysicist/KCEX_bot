# 🧭 Master Quantitative Synthesis Guide: TRUMP_USDT - EMA_CROSSOVER
> **Backtest Run ID:** `backtest_TRUMP_USDT_20260905_113743` | **Total Partitioned Chunks:** `35`

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
| `chunk_01_2026-W01.md` | `Week 01 (2026-W01)` | `57` | `68.42%` | `+0.0026` | `No` |
| `chunk_02_2026-W02.md` | `Week 02 (2026-W02)` | `87` | `59.77%` | `-0.0030` | `No` |
| `chunk_03_2026-W03.md` | `Week 03 (2026-W03)` | `86` | `65.12%` | `+0.0040` | `No` |
| `chunk_04_2026-W04.md` | `Week 04 (2026-W04)` | `90` | `55.56%` | `-0.0100` | `No` |
| `chunk_05_2026-W05.md` | `Week 05 (2026-W05)` | `86` | `51.16%` | `-0.0052` | `No` |
| `chunk_06_2026-W06.md` | `Week 06 (2026-W06)` | `72` | `69.44%` | `-0.0030` | `No` |
| `chunk_07_2026-W07.md` | `Week 07 (2026-W07)` | `85` | `61.18%` | `+0.0004` | `No` |
| `chunk_08_2026-W08.md` | `Week 08 (2026-W08)` | `68` | `61.76%` | `+0.0036` | `No` |
| `chunk_09_2026-W09.md` | `Week 09 (2026-W09)` | `84` | `59.52%` | `-0.0004` | `No` |
| `chunk_10_2026-W10.md` | `Week 10 (2026-W10)` | `81` | `56.79%` | `-0.0002` | `No` |
| `chunk_11_2026-W11.md` | `Week 11 (2026-W11)` | `82` | `64.63%` | `-0.0072` | `No` |
| `chunk_12_2026-W12.md` | `Week 12 (2026-W12)` | `77` | `68.83%` | `+0.0008` | `No` |
| `chunk_13_2026-W13.md` | `Week 13 (2026-W13)` | `95` | `62.11%` | `+0.0080` | `No` |
| `chunk_14_2026-W14.md` | `Week 14 (2026-W14)` | `81` | `58.02%` | `+0.0060` | `No` |
| `chunk_15_2026-W15.md` | `Week 15 (2026-W15)` | `95` | `55.79%` | `+0.0056` | `No` |
| `chunk_16_2026-W16.md` | `Week 16 (2026-W16)` | `88` | `65.91%` | `+0.0078` | `No` |
| `chunk_17_2026-W17.md` | `Week 17 (2026-W17)` | `99` | `64.65%` | `+0.0090` | `No` |
| `chunk_18_2026-W18.md` | `Week 18 (2026-W18)` | `107` | `55.14%` | `+0.0110` | `No` |
| `chunk_19_2026-W19.md` | `Week 19 (2026-W19)` | `80` | `60.00%` | `+0.0094` | `No` |
| `chunk_20_2026-W20.md` | `Week 20 (2026-W20)` | `96` | `52.08%` | `+0.0056` | `No` |
| `chunk_21_2026-W21.md` | `Week 21 (2026-W21)` | `108` | `49.07%` | `+0.0014` | `No` |
| `chunk_22_2026-W22.md` | `Week 22 (2026-W22)` | `103` | `49.51%` | `+0.0054` | `No` |
| `chunk_23_2026-W23.md` | `Week 23 (2026-W23)` | `74` | `56.76%` | `+0.0016` | `No` |
| `chunk_24_2026-W24.md` | `Week 24 (2026-W24)` | `75` | `64.00%` | `+0.0024` | `No` |
| `chunk_25_2026-W25.md` | `Week 25 (2026-W25)` | `82` | `56.10%` | `+0.0106` | `No` |
| `chunk_26_2026-W26.md` | `Week 26 (2026-W26)` | `101` | `42.57%` | `+0.0012` | `No` |
| `chunk_27_2026-W27.md` | `Week 27 (2026-W27)` | `90` | `48.89%` | `+0.0020` | `⚡ Yes` |
| `chunk_28_2026-W28.md` | `Week 28 (2026-W28)` | `126` | `38.10%` | `+0.0020` | `⚡ Yes` |
| `chunk_29_2026-W29.md` | `Week 29 (2026-W29)` | `116` | `38.79%` | `+0.0014` | `⚡ Yes` |
| `chunk_30_2026-W30.md` | `Week 30 (2026-W30)` | `139` | `35.97%` | `+0.0052` | `⚡ Yes` |
| `chunk_31_2026-W31.md` | `Week 31 (2026-W31)` | `142` | `27.46%` | `-0.0028` | `⚡ Yes` |
| `chunk_32_2026-W32.md` | `Week 32 (2026-W32)` | `162` | `29.63%` | `-0.0012` | `⚡ Yes` |
| `chunk_33_2026-W33.md` | `Week 33 (2026-W33)` | `183` | `31.69%` | `+0.0008` | `⚡ Yes` |
| `chunk_34_2026-W34.md` | `Week 34 (2026-W34)` | `113` | `46.90%` | `-0.0092` | `⚡ Yes` |
| `chunk_35_2026-W35.md` | `Week 35 (2026-W35)` | `81` | `80.25%` | `+0.0062` | `⚡ Yes` |