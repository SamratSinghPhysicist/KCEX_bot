import os, sys
EXPERIMENT_DIR = os.path.abspath('experiments/btc_eth_reverse_experiment')
ROOT_DIR = os.path.abspath('.')
sys.path.insert(0, ROOT_DIR)

from experiments.btc_eth_reverse_experiment.engine import load_candles_from_dir, parse_date_to_ms

base_dir = os.path.join(ROOT_DIR, 'BACKTESTER/OHLCV_Data_Binance')
start_ms = parse_date_to_ms('2020-01-01')
end_ms = parse_date_to_ms('2026-09-30') + (24 * 3600 * 1000 - 1)

btc_c = load_candles_from_dir('BTCUSDT', '1h', base_dir, start_ms, end_ms)
eth_c = load_candles_from_dir('ETHUSDT', '1h', base_dir, start_ms, end_ms)

btc_dict = {c.open_time_ms: c for c in btc_c}
eth_dict = {c.open_time_ms: c for c in eth_c}
common_times = sorted(list(set(btc_dict.keys()) & set(eth_dict.keys())))
tot_len = len(common_times)

p_tp = 1.50
p_sl = 1.50
part_price = 0.20
cut_adv = 0.40
fee_rt = 0.060 # Limit In + Market Out
leg_alloc = 0.75 # $750

for be_level in [0.00, 0.03, 0.05, 0.06, 0.07, 0.08, 0.09, 0.10]:
    cycles = []
    i = 0
    while i < tot_len - 1:
        entry_ts = common_times[i]
        p_b = btc_dict[entry_ts].open
        p_e = eth_dict[entry_ts].open

        tp_b = p_b * (1.0 + p_tp / 100.0)
        sl_b = p_b * (1.0 - p_sl / 100.0)
        tp_e = p_e * (1.0 - p_tp / 100.0)
        sl_e = p_e * (1.0 + p_sl / 100.0)

        b_exit = None; e_exit = None
        b_series = []; e_series = []

        j = i
        while j < tot_len:
            ts = common_times[j]
            c_b = btc_dict[ts]; c_e = eth_dict[ts]

            fav_b = (c_b.high - p_b) / p_b * 100.0
            adv_b = (p_b - c_b.low) / p_b * 100.0
            b_series.append((fav_b, adv_b, ts))

            fav_e = (p_e - c_e.low) / p_e * 100.0
            adv_e = (c_e.high - p_e) / p_e * 100.0
            e_series.append((fav_e, adv_e, ts))

            if b_exit is None:
                if c_b.high >= tp_b or c_b.low <= sl_b or adv_b >= cut_adv:
                    b_exit = j
            if e_exit is None:
                if c_e.low <= tp_e or c_e.high >= sl_e or adv_e >= cut_adv:
                    e_exit = j

            if b_exit is not None and e_exit is not None:
                break
            j += 1

        if b_exit is None or e_exit is None:
            break

        free_idx = max(b_exit, e_exit)

        # BTC return
        b_hit_partial = False
        b_return = None
        for fav, adv, ts in b_series[:free_idx - i + 1]:
            if fav >= part_price and not b_hit_partial:
                b_hit_partial = True
            if b_hit_partial:
                if fav >= p_tp:
                    b_return = 0.5 * part_price + 0.5 * p_tp - fee_rt
                    break
                elif adv > 0 and fav < be_level:
                    b_return = 0.5 * part_price + 0.5 * be_level - fee_rt
                    break
            else:
                if adv >= cut_adv:
                    b_return = -cut_adv - fee_rt
                    break
                elif fav >= p_tp:
                    b_return = 0.5 * part_price + 0.5 * p_tp - fee_rt
                    break
        if b_return is None:
            b_return = 0.5 * part_price + 0.5 * be_level - fee_rt if b_hit_partial else -cut_adv - fee_rt

        # ETH return
        e_hit_partial = False
        e_return = None
        for fav, adv, ts in e_series[:free_idx - i + 1]:
            if fav >= part_price and not e_hit_partial:
                e_hit_partial = True
            if e_hit_partial:
                if fav >= p_tp:
                    e_return = 0.5 * part_price + 0.5 * p_tp - fee_rt
                    break
                elif adv > 0 and fav < be_level:
                    e_return = 0.5 * part_price + 0.5 * be_level - fee_rt
                    break
            else:
                if adv >= cut_adv:
                    e_return = -cut_adv - fee_rt
                    break
                elif fav >= p_tp:
                    e_return = 0.5 * part_price + 0.5 * p_tp - fee_rt
                    break
        if e_return is None:
            e_return = 0.5 * part_price + 0.5 * be_level - fee_rt if e_hit_partial else -cut_adv - fee_rt

        cycles.append({
            'b_return': b_return,
            'e_return': e_return
        })
        i = free_idx + 1

    tot_pnl = sum((1000.0 * leg_alloc * c['b_return'] / 100.0) + (1000.0 * leg_alloc * c['e_return'] / 100.0) for c in cycles)
    print(f"BE Lock Level: +{be_level:.2f}% | Total Net Profit on $1k: +${tot_pnl:,.2f}")
