"""
Algorithmic Trading Simulator
Author: Yacine Abdi

A comprehensive Python library for backtesting trading strategies.
"""

__version__ = '1.0.0'
__author__ = 'Yacine Abdi'

from .strategies import (
    BaseStrategy,
    RSIStrategy,
    MACDStrategy,
    MACrossoverStrategy,
    BollingerBandsStrategy,
    MeanReversionStrategy
)

from .backtester import BacktestEngine, Portfolio, Trade
from .data import DataLoader
from .analytics import PerformanceMetrics
from .visualization import Plotter

__all__ = [
    'BaseStrategy',
    'RSIStrategy',
    'MACDStrategy',
    'MACrossoverStrategy',
    'BollingerBandsStrategy',
    'MeanReversionStrategy',
    'BacktestEngine',
    'Portfolio',
    'Trade',
    'DataLoader',
    'PerformanceMetrics',
    'Plotter'
]
