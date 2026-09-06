# 🧭 Master Quantitative Synthesis Guide: TRUMP_USDT - STOCH_RSI
> **Backtest Run ID:** `backtest_TRUMP_USDT_20260905_113606` | **Total Partitioned Chunks:** `36`

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
| `chunk_01_2026-W01.md` | `Week 01 (2026-W01)` | `167` | `62.87%` | `-0.0050` | `No` |
| `chunk_02_2026-W02.md` | `Week 02 (2026-W02)` | `279` | `69.18%` | `-0.0022` | `No` |
| `chunk_03_2026-W03.md` | `Week 03 (2026-W03)` | `228` | `65.79%` | `+0.0066` | `No` |
| `chunk_04_2026-W04.md` | `Week 04 (2026-W04)` | `256` | `58.20%` | `+0.0048` | `No` |
| `chunk_05_2026-W05.md` | `Week 05 (2026-W05)` | `242` | `64.05%` | `+0.0066` | `No` |
| `chunk_06_2026-W06.md` | `Week 06 (2026-W06)` | `229` | `69.87%` | `-0.0130` | `No` |
| `chunk_07_2026-W07.md` | `Week 07 (2026-W07)` | `272` | `61.76%` | `+0.0018` | `No` |
| `chunk_08_2026-W08.md` | `Week 08 (2026-W08)` | `251` | `60.56%` | `-0.0150` | `No` |
| `chunk_09_2026-W09.md` | `Week 09 (2026-W09)` | `242` | `61.98%` | `-0.0064` | `No` |
| `chunk_10_2026-W10.md` | `Week 10 (2026-W10)` | `251` | `60.96%` | `+0.0010` | `No` |
| `chunk_11_2026-W11.md` | `Week 11 (2026-W11)` | `225` | `72.89%` | `+0.0186` | `No` |
| `chunk_12_2026-W12.md` | `Week 12 (2026-W12)` | `255` | `70.20%` | `+0.0216` | `No` |
| `chunk_13_2026-W13.md` | `Week 13 (2026-W13)` | `255` | `52.94%` | `-0.0068` | `No` |
| `chunk_14_2026-W14.md` | `Week 14 (2026-W14)` | `194` | `69.59%` | `+0.0198` | `No` |
| `chunk_15_2026-W15.md` | `Week 15 (2026-W15)` | `262` | `58.02%` | `+0.0150` | `No` |
| `chunk_16_2026-W16.md` | `Week 16 (2026-W16)` | `225` | `56.44%` | `+0.0046` | `No` |
| `chunk_17_2026-W17.md` | `Week 17 (2026-W17)` | `255` | `59.22%` | `+0.0076` | `No` |
| `chunk_18_2026-W18.md` | `Week 18 (2026-W18)` | `243` | `54.73%` | `+0.0086` | `No` |
| `chunk_19_2026-W19.md` | `Week 19 (2026-W19)` | `256` | `58.98%` | `+0.0218` | `No` |
| `chunk_20_2026-W20.md` | `Week 20 (2026-W20)` | `209` | `51.20%` | `+0.0066` | `No` |
| `chunk_21_2026-W21.md` | `Week 21 (2026-W21)` | `262` | `58.02%` | `+0.0220` | `No` |
| `chunk_22_2026-W22.md` | `Week 22 (2026-W22)` | `241` | `48.13%` | `-0.0028` | `No` |
| `chunk_23_2026-W23.md` | `Week 23 (2026-W23)` | `221` | `55.66%` | `-0.0136` | `No` |
| `chunk_24_2026-W24.md` | `Week 24 (2026-W24)` | `245` | `65.31%` | `+0.0054` | `No` |
| `chunk_25_2026-W25.md` | `Week 25 (2026-W25)` | `209` | `57.89%` | `+0.0118` | `No` |
| `chunk_26_2026-W26.md` | `Week 26 (2026-W26)` | `213` | `56.34%` | `+0.0186` | `No` |
| `chunk_27_2026-W27.md` | `Week 27 (2026-W27)` | `223` | `50.22%` | `+0.0116` | `⚡ Yes` |
| `chunk_28_2026-W28.md` | `Week 28 (2026-W28)` | `295` | `46.10%` | `+0.0128` | `⚡ Yes` |
| `chunk_29_2026-W29.md` | `Week 29 (2026-W29)` | `235` | `39.15%` | `-0.0024` | `⚡ Yes` |
| `chunk_30_2026-W30.md` | `Week 30 (2026-W30)` | `264` | `41.29%` | `+0.0092` | `⚡ Yes` |
| `chunk_31_2026-W31.md` | `Week 31 (2026-W31)` | `258` | `38.76%` | `+0.0088` | `⚡ Yes` |
| `chunk_32_2026-W32.md` | `Week 32 (2026-W32)` | `324` | `34.26%` | `+0.0060` | `⚡ Yes` |
| `chunk_33_2026-W33.md` | `Week 33 (2026-W33)` | `318` | `37.74%` | `+0.0048` | `⚡ Yes` |
| `chunk_34_2026-W34.md` | `Week 34 (2026-W34)` | `270` | `57.41%` | `+0.0054` | `⚡ Yes` |
| `chunk_35_2026-W35.md` | `Week 35 (2026-W35)` | `272` | `78.31%` | `+0.0138` | `⚡ Yes` |
| `chunk_36_2026-W36.md` | `Week 36 (2026-W36)` | `1` | `100.00%` | `+0.0004` | `⚡ Yes` |