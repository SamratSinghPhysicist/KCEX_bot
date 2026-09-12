"""
Order Block + Demand Block Strategy Integration Module
======================================================
Proxies and exposes the core implementation located in:
'strategies/By Advance Crypto Trader/Order Book + Demand Block Strategy/order_block_demand.py'
ensuring clean, standard Python import ergonomics across the entire KCEX bot codebase.
"""

import os
import sys
import importlib.util

_impl_path = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "By Advance Crypto Trader",
        "Order Book + Demand Block Strategy",
        "order_block_demand.py"
    )
)

if not os.path.exists(_impl_path):
    raise ImportError(f"OrderBlockDemandStrategy implementation file not found at: {_impl_path}")

_spec = importlib.util.spec_from_file_location("strategies._order_block_demand_impl", _impl_path)
if _spec is None or _spec.loader is None:
    raise ImportError(f"Failed to load spec for OrderBlockDemandStrategy from: {_impl_path}")

_mod = importlib.util.module_from_spec(_spec)
sys.modules["strategies._order_block_demand_impl"] = _mod
_spec.loader.exec_module(_mod)

# Export all public symbols
OrderBlockDemandStrategy = _mod.OrderBlockDemandStrategy
OrderBlockDemandSubStrategy = _mod.OrderBlockDemandSubStrategy
OrderBookDemandStrategy = _mod.OrderBookDemandStrategy
SmartMoneyZone = _mod.SmartMoneyZone
ZoneType = _mod.ZoneType
ZoneStatus = _mod.ZoneStatus
SwingPoint = _mod.SwingPoint
SwingStructureDetector = _mod.SwingStructureDetector

__all__ = [
    "OrderBlockDemandStrategy",
    "OrderBlockDemandSubStrategy",
    "OrderBookDemandStrategy",
    "SmartMoneyZone",
    "ZoneType",
    "ZoneStatus",
    "SwingPoint",
    "SwingStructureDetector"
]
