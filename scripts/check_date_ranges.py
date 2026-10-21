import os, glob, pandas as pd

for root, dirs, files in os.walk('BACKTESTER'):
    for f in files:
        if f == '1h.csv':
            path = os.path.join(root, f)
            try:
                df = pd.read_csv(path)
                col_map = {c: c.lower().strip() for c in df.columns}
                df.rename(columns=col_map, inplace=True)
                t0 = pd.to_datetime(df['open_time'].min(), unit='ms')
                t1 = pd.to_datetime(df['open_time'].max(), unit='ms')
                rows = len(df)
                sym = os.path.basename(root)
                category = "Crypto" if "Crypto" in root else ("Stocks" if "Stocks" in root else "Other")
                print(f"{category:<7} | {sym:<6} | Bars: {rows:>6,} | Span: {t0.strftime('%Y-%m-%d')} to {t1.strftime('%Y-%m-%d')}")
            except Exception as e:
                print(f"Error on {path}: {e}")
