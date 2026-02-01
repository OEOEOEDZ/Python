"""
Unit Tests for Backtesting Engine
Author: Yacine Abdi
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime

from src.backtester.engine import BacktestEngine
from src.backtester.portfolio import Portfolio, Trade
from src.strategies import RSIStrategy


@pytest.fixture
def sample_data():
    """Create sample data for testing."""
    dates = pd.date_range(start='2023-01-01', periods=100, freq='D')
    np.random.seed(42)
    
    prices = 100 * np.exp(np.cumsum(np.random.normal(0.001, 0.02, 100)))
    
    data = pd.DataFrame({
        'Open': prices,
        'High': prices * 1.02,
        'Low': prices * 0.98,
        'Close': prices,
        'Volume': np.random.randint(1000000, 10000000, 100)
    }, index=dates)
    
    return data


class TestPortfolio:
    """Test cases for Portfolio class."""
    
    def test_initialization(self):
        """Test portfolio initialization."""
        portfolio = Portfolio(initial_capital=100000, commission=0.001)
        assert portfolio.initial_capital == 100000
        assert portfolio.cash == 100000
        assert portfolio.shares == 0
        assert portfolio.current_position == 0
    
    def test_buy_trade(self):
        """Test buy execution."""
        portfolio = Portfolio(initial_capital=100000, commission=0)
        trade = portfolio.buy(price=100, timestamp=datetime.now())
        
        assert trade is not None
        assert trade.action == 'BUY'
        assert portfolio.shares > 0
        assert portfolio.cash < 100000
        assert portfolio.current_position == 1
    
    def test_sell_trade(self):
        """Test sell execution."""
        portfolio = Portfolio(initial_capital=100000, commission=0)
        portfolio.buy(price=100, timestamp=datetime.now())
        initial_shares = portfolio.shares
        
        trade = portfolio.sell(price=110, timestamp=datetime.now())
        
        assert trade is not None
        assert trade.action == 'SELL'
        assert portfolio.shares == 0
        assert portfolio.current_position == 0
        assert portfolio.cash > 100000  # Profit
    
    def test_cannot_sell_without_position(self):
        """Test that selling without position fails."""
        portfolio = Portfolio(initial_capital=100000)
        trade = portfolio.sell(price=100, timestamp=datetime.now())
        
        assert trade is None
    
    def test_portfolio_value_tracking(self):
        """Test portfolio value tracking."""
        portfolio = Portfolio(initial_capital=100000)
        portfolio.update_value(current_price=100, timestamp=datetime.now())
        
        assert len(portfolio.portfolio_values) == 1
        assert portfolio.portfolio_values[0] == 100000
    
    def test_get_returns(self):
        """Test returns calculation."""
        portfolio = Portfolio(initial_capital=100000)
        
        for i in range(5):
            portfolio.update_value(
                current_price=100 + i,
                timestamp=datetime.now()
            )
        
        returns = portfolio.get_returns()
        assert len(returns) > 0


class TestBacktestEngine:
    """Test cases for Backtest Engine."""
    
    def test_initialization(self):
        """Test engine initialization."""
        engine = BacktestEngine(
            initial_capital=100000,
            commission=0.001,
            position_size=0.95
        )
        assert engine.initial_capital == 100000
        assert engine.commission == 0.001
        assert engine.position_size == 0.95
    
    def test_run_backtest(self, sample_data):
        """Test running a backtest."""
        engine = BacktestEngine(initial_capital=100000)
        strategy = RSIStrategy()
        
        results = engine.run(sample_data, strategy, verbose=False)
        
        assert 'total_return' in results
        assert 'sharpe_ratio' in results
        assert 'max_drawdown' in results
        assert 'num_trades' in results
        assert engine.portfolio is not None
    
    def test_results_structure(self, sample_data):
        """Test results dictionary structure."""
        engine = BacktestEngine(initial_capital=100000)
        strategy = RSIStrategy()
        results = engine.run(sample_data, strategy, verbose=False)
        
        required_keys = [
            'initial_capital', 'final_value', 'total_return',
            'buy_hold_return', 'sharpe_ratio', 'max_drawdown',
            'num_trades', 'win_rate'
        ]
        
        for key in required_keys:
            assert key in results
    
    def test_portfolio_history(self, sample_data):
        """Test portfolio history retrieval."""
        engine = BacktestEngine(initial_capital=100000)
        strategy = RSIStrategy()
        engine.run(sample_data, strategy, verbose=False)
        
        history = engine.get_portfolio_history()
        assert len(history) > 0
        assert 'Portfolio_Value' in history.columns


class TestTrade:
    """Test cases for Trade data class."""
    
    def test_trade_creation(self):
        """Test trade creation."""
        trade = Trade(
            timestamp=datetime.now(),
            action='BUY',
            price=100.0,
            shares=10,
            commission=1.0
        )
        
        assert trade.action == 'BUY'
        assert trade.price == 100.0
        assert trade.shares == 10
        assert trade.commission == 1.0
    
    def test_trade_value(self):
        """Test trade value calculation."""
        trade = Trade(
            timestamp=datetime.now(),
            action='BUY',
            price=100.0,
            shares=10,
            commission=5.0
        )
        
        # Value should be (price * shares) + commission
        assert trade.value == 1005.0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
