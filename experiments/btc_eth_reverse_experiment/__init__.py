"""
BTC vs ETH Reverse Trading Experiment Package
============================================
Experiment evaluating synchronized dual-account reverse trading:
Account A: Trades strictly BTC
Account B: Trades strictly ETH
Both trade simultaneously with 100% capital and 2x leverage.
Trades are reverse (Case 1: Long BTC / Short ETH; Case 2: Short BTC / Long ETH).
New trades are executed only when and as soon as both accounts become free.
"""

__version__ = "1.0.0"
