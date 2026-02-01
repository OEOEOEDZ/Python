"""
Moving Average Crossover Trading Strategy
Author: Yacine Abdi

Classic trend-following strategy using short and long moving averages.
Buy when short MA crosses above long MA (golden cross).
Sell when short MA crosses below long MA (death cross).
"""

import pandas as pd
import numpy as np
from .base_strategy import BaseStrategy


class MACrossoverStrategy(BaseStrategy):
    """
    Moving Average Crossover strategy.
    """
    
    def __init__(self, short_window: int = 50, long_window: int = 200, 
                 ma_type: str = 'SMA'):
        """
        Initialize MA Crossover strategy.
        
        Args:
            short_window (int): Short moving average period (default: 50)
            long_window (int): Long moving average period (default: 200)
            ma_type (str): Type of MA - 'SMA' or 'EMA' (default: 'SMA')
        """
        super().__init__(name='MA Crossover Strategy')
        self.short_window = short_window
        self.long_window = long_window
        self.ma_type = ma_type.upper()
        
        if self.ma_type not in ['SMA', 'EMA']:
            raise ValueError("ma_type must be 'SMA' or 'EMA'")
    
    def calculate_sma(self, prices: pd.Series, window: int) -> pd.Series:
        """Calculate Simple Moving Average."""
        return prices.rolling(window=window).mean()
    
    def calculate_ema(self, prices: pd.Series, window: int) -> pd.Series:
        """Calculate Exponential Moving Average."""
        return prices.ewm(span=window, adjust=False).mean()
    
    def calculate_indicators(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate moving averages.
        
        Args:
            data (pd.DataFrame): Historical price data
            
        Returns:
            pd.DataFrame: Data with MA columns
        """
        data = data.copy()
        
        if self.ma_type == 'SMA':
            data['MA_Short'] = self.calculate_sma(data['Close'], self.short_window)
            data['MA_Long'] = self.calculate_sma(data['Close'], self.long_window)
        else:  # EMA
            data['MA_Short'] = self.calculate_ema(data['Close'], self.short_window)
            data['MA_Long'] = self.calculate_ema(data['Close'], self.long_window)
        
        return data
    
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Generate trading signals based on MA crossovers.
        
        Args:
            data (pd.DataFrame): Historical price data
            
        Returns:
            pd.DataFrame: Data with signal column
        """
        if not self.validate_data(data):
            raise ValueError("Invalid data format. Required columns: OHLCV")
        
        data = self.calculate_indicators(data)
        data['signal'] = 0
        
        # Previous MA values for crossover detection
        data['MA_Short_prev'] = data['MA_Short'].shift(1)
        data['MA_Long_prev'] = data['MA_Long'].shift(1)
        
        # Golden Cross: Buy signal
        golden_cross = (data['MA_Short'] > data['MA_Long']) & \
                      (data['MA_Short_prev'] <= data['MA_Long_prev'])
        data.loc[golden_cross, 'signal'] = 1
        
        # Death Cross: Sell signal
        death_cross = (data['MA_Short'] < data['MA_Long']) & \
                     (data['MA_Short_prev'] >= data['MA_Long_prev'])
        data.loc[death_cross, 'signal'] = -1
        
        # Create position column
        data['position'] = data['signal'].replace(0, np.nan).ffill().fillna(0)
        
        # Clean up temporary columns
        data.drop(['MA_Short_prev', 'MA_Long_prev'], axis=1, inplace=True)
        
        return data
    
    def get_strategy_info(self) -> dict:
        """Get strategy information and parameters."""
        info = super().get_strategy_info()
        info.update({
            'short_window': self.short_window,
            'long_window': self.long_window,
            'ma_type': self.ma_type
        })
        return info
