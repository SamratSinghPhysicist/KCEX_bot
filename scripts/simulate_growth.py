"""
Capital Progression & Phased Compounding Simulator
==================================================
Simulates dynamic capital growth starting from 0.20 USDT taking into account:
1. Minimum contract notional and margin gating per pair on KCEX.
2. Dynamic pair activation as capital crosses unlocking thresholds.
3. Realistic empirical returns based on backtested performance.
4. Scale-dependent risk tapering (avoiding unrealistic infinite compounding).
5. Week-by-week (Months 1-3), Month-by-month (Months 4-12), Year-by-year (Years 2-10).
6. Comprehensive milestone logging (2x, 3x, 5x, 10x, 1 USDT, 5 USDT, etc.)
"""

import math

def simulate_capital_growth():
    capital = 0.20
    starting_capital = 0.20

    # Minimum balance required to trade 1 contract under 10% margin sizing @ 15x leverage:
    pair_unlocks = [
        ("TRUMP_USDT (15m)", 0.13),
        ("AIXBT_USDT (1d)", 0.13),
        ("AVAX_USDT (1h)", 0.51),
        ("DOGE_USDT (15m)", 0.54),
        ("ETH_USDT (4h)", 1.63),
        ("TRX_USDT (1h)", 2.22),
        ("BTC_USDT (15m)", 5.10),
    ]

    # Milestones to track
    target_multiples = [2, 3, 5, 10, 25, 50, 100, 250, 500, 1000, 2500, 5000, 10000, 25000, 50000, 100000]
    target_dollar_values = [
        0.50, 1.0, 2.0, 3.0, 5.0, 10.0, 15.0, 25.0, 50.0, 100.0,
        250.0, 500.0, 1000.0, 2500.0, 5000.0, 10000.0, 25000.0,
        50000.0, 100000.0, 250000.0, 500000.0, 1000000.0
    ]
    
    passed_multiples = set()
    passed_dollars = set()
    milestones_log = []

    def check_milestones(curr_cap, time_label):
        # Multiples
        for m in target_multiples:
            if m not in passed_multiples and curr_cap >= (starting_capital * m):
                passed_multiples.add(m)
                milestones_log.append({
                    "time": time_label,
                    "milestone": f"{m}x Capital (${starting_capital * m:.2f})",
                    "capital": curr_cap
                })
        # Dollars
        for d in target_dollar_values:
            if d not in passed_dollars and curr_cap >= d:
                passed_dollars.add(d)
                milestones_log.append({
                    "time": time_label,
                    "milestone": f"${d:.2f} USDT Reached",
                    "capital": curr_cap
                })

    def get_active_pairs(curr_cap):
        active = [name for name, min_bal in pair_unlocks if curr_cap >= min_bal]
        return active

    def get_weekly_expected_return(curr_cap):
        """
        Conservative empirical return rate based on active assets & size drag (7 pairs):
        - Phase 1 (< $0.50): TRUMP (15m), AIXBT (1d) active -> ~4.8% / week
        - Phase 2 ($0.50 - $2.22): AVAX (1h), DOGE (15m), ETH (4h) join -> ~4.4% / week
        - Phase 3 ($2.22 - $5.10): TRX (1h) [81.8% WR] joins -> ~4.0% / week
        - Phase 4 ($5.10 - $1,000): BTC (15m) joins, full 7-pair portfolio active -> ~3.5% / week
        - Phase 5 ($1,000 - $10,000): Capital scaling, position sizing reduces -> ~2.7% / week
        - Phase 6 ($10,000 - $100,000): Partial de-risking, slippage friction -> ~1.9% / week
        - Phase 7 ($100k+): Institutional risk model (1-2% margin per trade) -> ~1.2% / week
        """
        if curr_cap < 0.50:
            return 0.048  # 4.8% weekly (~22.5% monthly)
        elif curr_cap < 2.22:
            return 0.044  # 4.4% weekly (~20.5% monthly)
        elif curr_cap < 5.10:
            return 0.040  # 4.0% weekly (~18.5% monthly)
        elif curr_cap < 1000.0:
            return 0.035  # 3.5% weekly (~15.7% monthly)
        elif curr_cap < 10000.0:
            return 0.027  # 2.7% weekly (~12.0% monthly)
        elif curr_cap < 100000.0:
            return 0.019  # 1.9% weekly (~8.2% monthly)
        else:
            return 0.012  # 1.2% weekly (~5.1% monthly)

    # 1. Week-by-Week (Weeks 1 to 13 = Months 1 to 3)
    weekly_records = []
    for w in range(1, 14):
        ret = get_weekly_expected_return(capital)
        pnl = capital * ret
        capital += pnl
        active = get_active_pairs(capital)
        time_label = f"Week {w} (Month {(w-1)//4 + 1})"
        check_milestones(capital, time_label)
        weekly_records.append({
            "week": w,
            "month": (w - 1) // 4 + 1,
            "start_cap": capital - pnl,
            "weekly_return_pct": ret * 100.0,
            "weekly_pnl": pnl,
            "end_cap": capital,
            "active_pairs_count": len(active),
            "active_pairs": [p.split()[0] for p, mb in pair_unlocks if capital >= mb],
            "newly_unlocked": [p.split()[0] for p, mb in pair_unlocks if (capital - pnl) < mb <= capital]
        })

    # 2. Month-by-Month (Months 1 to 24 = Years 1 & 2)
    monthly_records = []
    # Add first 3 months summary
    monthly_records.append({"month": 1, "start_cap": 0.20, "end_cap": weekly_records[3]["end_cap"], "monthly_return_pct": (weekly_records[3]["end_cap"] - 0.20)/0.20*100.0, "active_count": len(get_active_pairs(weekly_records[3]["end_cap"]))})
    monthly_records.append({"month": 2, "start_cap": weekly_records[3]["end_cap"], "end_cap": weekly_records[7]["end_cap"], "monthly_return_pct": (weekly_records[7]["end_cap"] - weekly_records[3]["end_cap"])/weekly_records[3]["end_cap"]*100.0, "active_count": len(get_active_pairs(weekly_records[7]["end_cap"]))})
    monthly_records.append({"month": 3, "start_cap": weekly_records[7]["end_cap"], "end_cap": weekly_records[12]["end_cap"], "monthly_return_pct": (weekly_records[12]["end_cap"] - weekly_records[7]["end_cap"])/weekly_records[7]["end_cap"]*100.0, "active_count": len(get_active_pairs(weekly_records[12]["end_cap"]))})

    for m in range(4, 37): # Track month-by-month through Year 3 (36 months)
        m_start = capital
        for _ in range(4):
            ret = get_weekly_expected_return(capital)
            capital += capital * ret
        ret_part = get_weekly_expected_return(capital) * 0.333
        capital += capital * ret_part
        
        m_pnl = capital - m_start
        m_ret_pct = (m_pnl / m_start) * 100.0
        yr = (m - 1) // 12 + 1
        mo_in_yr = (m - 1) % 12 + 1
        time_label = f"Month {m} (Year {yr} M{mo_in_yr})"
        check_milestones(capital, time_label)
        active = get_active_pairs(capital)
        monthly_records.append({
            "month": m,
            "year": yr,
            "month_in_year": mo_in_yr,
            "start_cap": m_start,
            "monthly_return_pct": m_ret_pct,
            "monthly_pnl": m_pnl,
            "end_cap": capital,
            "active_pairs_count": len(active),
            "newly_unlocked": [p.split()[0] for p, mb in pair_unlocks if m_start < mb <= capital]
        })

    # Year 1 and Year 2 endpoints
    y1_cap = [r for r in monthly_records if r["month"] == 12][0]["end_cap"]
    y2_cap = [r for r in monthly_records if r["month"] == 24][0]["end_cap"]
    y3_cap = [r for r in monthly_records if r["month"] == 36][0]["end_cap"]

    # 3. Year-by-Year (Years 1 to 10)
    yearly_records = [
        {"year": 1, "start_cap": 0.20, "end_cap": y1_cap, "annual_return_pct": (y1_cap - 0.20)/0.20 * 100.0},
        {"year": 2, "start_cap": y1_cap, "end_cap": y2_cap, "annual_return_pct": (y2_cap - y1_cap)/y1_cap * 100.0},
        {"year": 3, "start_cap": y2_cap, "end_cap": y3_cap, "annual_return_pct": (y3_cap - y2_cap)/y2_cap * 100.0},
    ]

    for y in range(4, 11):
        y_start = capital
        for _ in range(52):
            ret = get_weekly_expected_return(capital)
            capital += capital * ret
        
        y_pnl = capital - y_start
        y_ret_pct = (y_pnl / y_start) * 100.0
        time_label = f"Year {y}"
        check_milestones(capital, time_label)
        yearly_records.append({
            "year": y,
            "start_cap": y_start,
            "annual_return_pct": y_ret_pct,
            "annual_pnl": y_pnl,
            "end_cap": capital,
            "active_pairs_count": len(get_active_pairs(capital))
        })

    return {
        "weekly_records": weekly_records,
        "monthly_records": monthly_records,
        "yearly_records": yearly_records,
        "milestones_log": milestones_log,
        "final_capital": capital
    }

if __name__ == "__main__":
    import sys
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

    res = simulate_capital_growth()

    print("=" * 95)
    print("📈 WEEK-BY-WEEK CAPITAL PROJECTION (FIRST 3 MONTHS: WEEKS 1 TO 13)")
    print("=" * 95)
    print(f"{'Week':<8} | {'Start Cap':<11} | {'Return (%)':<11} | {'Weekly PnL':<11} | {'End Cap':<11} | {'Active Pairs':<14} | {'Newly Unlocked'}")
    print("-" * 95)
    for r in res["weekly_records"]:
        unl = ", ".join(r["newly_unlocked"]) if r["newly_unlocked"] else "-"
        print(f"W{r['week']:<7} | ${r['start_cap']:>9.4f} | {r['weekly_return_pct']:>9.2f}% | ${r['weekly_pnl']:>9.4f} | ${r['end_cap']:>9.4f} | {r['active_pairs_count']}/7 pairs     | {unl}")

    print("\n" + "=" * 95)
    print("📅 MONTH-BY-MONTH CAPITAL PROJECTION (YEAR 1: MONTHS 1 TO 12)")
    print("=" * 95)
    print(f"{'Month':<8} | {'Start Cap':<11} | {'Monthly Ret':<11} | {'Monthly PnL':<11} | {'End Cap':<11} | {'Active Pairs':<14} | {'Newly Unlocked'}")
    print("-" * 95)
    for r in res["monthly_records"][:12]:
        m = r["month"]
        m_pnl = r.get("monthly_pnl", r["end_cap"] - r["start_cap"])
        m_ret = r["monthly_return_pct"]
        unl = ", ".join(r.get("newly_unlocked", [])) if r.get("newly_unlocked") else "-"
        act_cnt = r.get("active_count", r.get("active_pairs_count", 2))
        print(f"M{m:<7} | ${r['start_cap']:>9.4f} | {m_ret:>9.2f}% | ${m_pnl:>9.4f} | ${r['end_cap']:>9.4f} | {act_cnt}/7 pairs     | {unl}")

    print("\n" + "=" * 95)
    print("🗓️ YEAR-BY-YEAR CAPITAL PROJECTION (YEARS 1 TO 10)")
    print("=" * 95)
    print(f"{'Year':<8} | {'Start Cap':<14} | {'Annual Ret (%)':<14} | {'Annual PnL':<14} | {'End Cap':<14} | {'Active Pairs'}")
    print("-" * 95)
    for r in res["yearly_records"]:
        pnl = r["end_cap"] - r["start_cap"]
        print(f"Year {r['year']:<3} | ${r['start_cap']:>12.2f} | {r['annual_return_pct']:>12.1f}% | ${pnl:>12.2f} | ${r['end_cap']:>12.2f} | {r.get('active_pairs_count', 7)}/7 pairs")

    print("\n" + "=" * 95)
    print("🏆 CHRONOLOGICAL MILESTONES ACHIEVED (0.20 USDT -> 330,000+ USDT)")
    print("=" * 95)
    for m in res["milestones_log"]:
        print(f"[{m['time']:<24}] -> {m['milestone']:<32} | Capital: ${m['capital']:>12.2f}")

