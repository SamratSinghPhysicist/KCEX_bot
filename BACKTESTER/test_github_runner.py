"""
Unit tests for GitHub Actions Cloud Backtester Runner
=====================================================
Tests workflow input generation, repository detection, artifact naming logic,
and GitHubBacktestRunner configuration.
"""

import os
import sys
import unittest

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from BACKTESTER.engine.config import BacktestConfig
from BACKTESTER.engine.github_runner import (
    GitHubBacktestRunner,
    get_git_remote_repo,
    resolve_github_token
)


class TestGitHubRunner(unittest.TestCase):

    def test_git_remote_repo_detection(self):
        owner, repo = get_git_remote_repo()
        self.assertEqual(owner, "SamratSinghPhysicist")
        self.assertEqual(repo, "KCEX_bot")

    def test_workflow_inputs_generation_trump(self):
        config = BacktestConfig(
            symbol="TRUMP_USDT",
            timeframe="1m",
            strategy_mode="STOCH_RSI",
            stoch_preset="FAST_SCALP",
            start_time="2026-01-01",
            end_time="2026-08-31",
            leverage=75,
            tp_ticks=2,
            sl_mode="ROE",
            sl_roe_pct=25.0,
            volume_mode="MULTIPLIER",
            volume_multiplier=2.0
        )
        runner = GitHubBacktestRunner()
        inputs = runner.build_workflow_inputs(config)

        self.assertEqual(inputs["symbol"], "TRUMP_USDT")
        self.assertEqual(inputs["timeframe"], "1m")
        self.assertEqual(inputs["strategy"], "STOCH_RSI")
        self.assertEqual(inputs["stoch_preset"], "FAST_SCALP")
        self.assertEqual(inputs["leverage"], "75")
        self.assertEqual(inputs["tp_ticks"], "2")
        self.assertEqual(inputs["sl_mode"], "ROE")
        self.assertEqual(inputs["sl_roe"], "25.0")
        self.assertEqual(inputs["volume_mode"], "MULTIPLIER")
        self.assertEqual(inputs["volume_multiplier"], "2.0")
        self.assertEqual(inputs["start_date"], "2026-01-01")
        self.assertEqual(inputs["end_date"], "2026-08-31")

    def test_workflow_inputs_generation_doge(self):
        config = BacktestConfig(
            symbol="DOGE_USDT",
            timeframe="5m",
            strategy_mode="EMA_CROSSOVER",
            ema_preset="5/13",
            leverage=75,
            tp_ticks=2,
            sl_mode="ROE",
            sl_roe_pct=25.0
        )
        runner = GitHubBacktestRunner()
        inputs = runner.build_workflow_inputs(config)

        self.assertEqual(inputs["symbol"], "DOGE_USDT")
        self.assertEqual(inputs["volume_multiplier"], "1.0")  # 1x min for DOGE
        self.assertEqual(inputs["leverage"], "75")

    def test_runner_api_url_and_headers(self):
        runner = GitHubBacktestRunner(owner="TestOwner", repo="TestRepo", token="test_token_123")
        self.assertEqual(runner.api_base, "https://api.github.com/repos/TestOwner/TestRepo")
        self.assertEqual(runner.headers["Authorization"], "Bearer test_token_123")
        self.assertIn("Accept", runner.headers)


if __name__ == "__main__":
    unittest.main()
