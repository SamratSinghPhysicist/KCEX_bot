"""
Unit & Integration Tests for Backtest Analytics Engine
"""
import sys
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from BACKTESTER.analytics.indexer import ReportIndexer
from BACKTESTER.analytics.engine import AnalyticsEngine


class TestAnalyticsEngine(unittest.TestCase):

    def setUp(self):
        self.indexer = ReportIndexer()
        self.engine = AnalyticsEngine(self.indexer)

    def test_indexing(self):
        runs = self.indexer.get_all_runs()
        self.assertGreater(len(runs), 0, "Should discover at least one backtest run")
        for r in runs:
            self.assertTrue(r.metadata.symbol, "Symbol should not be empty")
            self.assertGreater(r.scorecard.total_trades, 0, "Trades count should be > 0")

    def test_comparison(self):
        runs = self.indexer.get_all_runs()
        run_ids = [r.metadata.run_id for r in runs]
        cmp_result = self.engine.compare_runs(run_ids)
        self.assertIn("parameter_diffs", cmp_result)
        self.assertIn("comparison_matrix", cmp_result)
        self.assertIn("equity_overlays", cmp_result)
        self.assertIn("radar_footprints", cmp_result)
        self.assertIn("exit_comparison", cmp_result)

    def test_paged_trades(self):
        runs = self.indexer.get_all_runs()
        if runs:
            first_id = runs[0].metadata.run_id
            page_res = self.engine.get_paged_trades(first_id, page=1, page_size=20)
            self.assertIn("trades", page_res)
            self.assertEqual(len(page_res["trades"]), min(20, page_res["total_count"]))


if __name__ == "__main__":
    unittest.main()
