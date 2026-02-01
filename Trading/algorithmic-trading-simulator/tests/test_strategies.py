"""
Unit Tests for Trading Strategies
Author: Yacine Abdi
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

from src.strategies import (
    RSIStrategy, MACDStrategy, MACrossoverStrategy,
    BollingerBandsStrategy, MeanReversionStrategy
)


@pytest.fixture
def sample_data():
    """Create sample OHLCV data for testing."""
    dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
    np.random.seed(42)
    
    # Generate realistic price data
    returns = np.random.normal(0.001, 0.02, len(dates))
    prices = 100 * np.exp(np.cumsum(returns))
    
    data = pd.DataFrame({
        'Open': prices * (1 + np.random.uniform(-0.01, 0.01, len(dates))),
        'High': prices * (1 + np.random.uniform(0, 0.02, len(dates))),
        'Low': prices * (1 - np.random.uniform(0, 0.02, len(dates))),
        'Close': prices,
        'Volume': np.random.randint(1000000, 10000000, len(dates))
    }, index=dates)
    
    return data


class TestRSIStrategy:
    """Test cases for RSI Strategy."""
    
    def test_initialization(self):
        """Test strategy initialization."""
        strategy = RSIStrategy(rsi_period=14, oversold=30, overbought=70)
        assert strategy.rsi_period == 14
        assert strategy.oversold == 30
        assert strategy.overbought == 70
    
    def test_generate_signals(self, sample_data):
        """Test signal generation."""
        strategy = RSIStrategy()
        result = strategy.generate_signals(sample_data)
        
        assert 'signal' in result.columns
        assert 'position' in result.columns
        assert 'RSI' in result.columns
        assert result['signal'].isin([0, 1, -1]).all()
    
    def test_rsi_calculation(self, sample_data):
        """Test RSI calculation."""
        strategy = RSIStrategy()
        result = strategy.calculate_indicators(sample_data)
        
        assert 'RSI' in result.columns
        assert result['RSI'].min() >= 0
        assert result['RSI'].max() <= 100


class TestMACDStrategy:
    """Test cases for MACD Strategy."""
    
    def test_initialization(self):
        """Test strategy initialization."""
        strategy = MACDStrategy(fast_period=12, slow_period=26, signal_period=9)
        assert strategy.fast_period == 12
        assert strategy.slow_period == 26
        assert strategy.signal_period == 9
    
    def test_generate_signals(self, sample_data):
        """Test signal generation."""
        strategy = MACDStrategy()
        result = strategy.generate_signals(sample_data)
        
        assert 'signal' in result.columns
        assert 'MACD' in result.columns
        assert 'MACD_Signal' in result.columns
        assert 'MACD_Histogram' in result.columns


class TestMACrossoverStrategy:
    """Test cases for MA Crossover Strategy."""
    
    def test_initialization(self):
        """Test strategy initialization."""
        strategy = MACrossoverStrategy(short_window=50, long_window=200, ma_type='SMA')
        assert strategy.short_window == 50
        assert strategy.long_window == 200
        assert strategy.ma_type == 'SMA'
    
    def test_invalid_ma_type(self):
        """Test invalid MA type raises error."""
        with pytest.raises(ValueError):
            MACrossoverStrategy(ma_type='INVALID')
    
    def test_generate_signals(self, sample_data):
        """Test signal generation."""
        strategy = MACrossoverStrategy(short_window=20, long_window=50)
        result = strategy.generate_signals(sample_data)
        
        assert 'signal' in result.columns
        assert 'MA_Short' in result.columns
        assert 'MA_Long' in result.columns


class TestBollingerBandsStrategy:
    """Test cases for Bollinger Bands Strategy."""
    
    def test_initialization(self):
        """Test strategy initialization."""
        strategy = BollingerBandsStrategy(period=20, std_dev=2.0)
        assert strategy.period == 20
        assert strategy.std_dev == 2.0
    
    def test_generate_signals(self, sample_data):
        """Test signal generation."""
        strategy = BollingerBandsStrategy()
        result = strategy.generate_signals(sample_data)
        
        assert 'signal' in result.columns
        assert 'BB_Upper' in result.columns
        assert 'BB_Middle' in result.columns
        assert 'BB_Lower' in result.columns
        assert (result['BB_Upper'] >= result['BB_Middle']).all()
        assert (result['BB_Middle'] >= result['BB_Lower']).all()


class TestMeanReversionStrategy:
    """Test cases for Mean Reversion Strategy."""
    
    def test_initialization(self):
        """Test strategy initialization."""
        strategy = MeanReversionStrategy(lookback_period=20, z_entry=2.0, z_exit=0.5)
        assert strategy.lookback_period == 20
        assert strategy.z_entry == 2.0
        assert strategy.z_exit == 0.5
    
    def test_generate_signals(self, sample_data):
        """Test signal generation."""
        strategy = MeanReversionStrategy()
        result = strategy.generate_signals(sample_data)
        
        assert 'signal' in result.columns
        assert 'Z_Score' in result.columns
        assert 'Rolling_Mean' in result.columns
        assert 'Rolling_Std' in result.columns


class TestBaseStrategy:
    """Test cases for base strategy functionality."""
    
    def test_validate_data(self, sample_data):
        """Test data validation."""
        strategy = RSIStrategy()
        assert strategy.validate_data(sample_data) == True
        
        # Test with invalid data
        invalid_data = pd.DataFrame({'Close': [1, 2, 3]})
        assert strategy.validate_data(invalid_data) == False
    
    def test_get_strategy_info(self):
        """Test strategy info retrieval."""
        strategy = RSIStrategy()
        info = strategy.get_strategy_info()
        
        assert 'name' in info
        assert 'type' in info
        assert info['name'] == 'RSI Strategy'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
