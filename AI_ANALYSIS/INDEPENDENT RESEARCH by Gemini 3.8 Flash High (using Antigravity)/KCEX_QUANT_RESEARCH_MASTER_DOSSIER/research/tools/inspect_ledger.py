import csv

LEDGER = "research_agent_output/03_EXPERIMENT_LEDGER.csv"
target_ids = ['EXP_0001', 'EXP_0007', 'EXP_0039', 'EXP_0040', 'EXP_0044', 'EXP_0045', 'EXP_0048', 'EXP_0049']

with open(LEDGER, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row['experiment_id'] in target_ids:
            print(f"{row['experiment_id']}: period={row.get('training_period')} {row.get('validation_period')} {row.get('test_period')} | params={row['parameters']} | PnL={row['PnL']} | WR={row['win_rate']} | PF={row['profit_factor']} | DD={row['drawdown']} | trades={row['trade_count']}")
