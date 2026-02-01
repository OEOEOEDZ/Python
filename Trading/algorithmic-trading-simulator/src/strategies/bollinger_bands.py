"""
Bollinger Bands Trading Strategy
Author: Yacine Abdi

Volatility-based strategy using Bollinger Bands.
Buy when price touches lower band (oversold).
Sell when price touches upper band (overbought).
"""

import pandas as pd
import numpy as np
from .base_strategy import BaseStrategy


class BollingerBandsStrategy(BaseStrategy):
    """
    Bollinger Bands mean reversion strategy.
    """
    
    def __init__(self, period: int = 20, std_dev: float = 2.0):
        """
        Initialize Bollinger Bands strategy.
        
        Args:
            period (int): Moving average period (default: 20)
            std_dev (float): Standard deviation multiplier (default: 2.0)
        """
        super().__init__(name='Bollinger Bands Strategy')
        self.period = period
        self.std_dev = std_dev
    
    def calculate_indicators(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate Bollinger Bands.
        
        Args:
            data (pd.DataFrame): Historical price data
            
        Returns:
            pd.DataFrame: Data with Bollinger Bands
        """
        data = data.copy()
        
        # Calculate middle band (SMA)
        data['BB_Middle'] = data['Close'].rolling(window=self.period).mean()
        
        # Calculate standard deviation
        rolling_std = data['Close'].rolling(window=self.period).std()
        
        # Calculate upper and lower bands
        data['BB_Upper'] = data['BB_Middle'] + (self.std_dev * rolling_std)
        data['BB_Lower'] = data['BB_Middle'] - (self.std_dev * rolling_std)
        
        # Calculate bandwidth (useful metric)
        data['BB_Width'] = (data['BB_Upper'] - data['BB_Lower']) / data['BB_Middle']
        
        return data
    
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Generate trading signals based on Bollinger Bands.
        
        Args:
            data (pd.DataFrame): Historical price data
            
        Returns:
            pd.DataFrame: Data with signal column
        """
        if not self.validate_data(data):
            raise ValueError("Invalid data format. Required columns: OHLCV")
        
        data = self.calculate_indicators(data)
        data['signal'] = 0
        
        # Buy signal: price touches or crosses below lower band
        buy_condition = data['Close'] <= data['BB_Lower']
        data.loc[buy_condition, 'signal'] = 1
        
        # Sell signal: price touches or crosses above upper band
        sell_condition = data['Close'] >= data['BB_Upper']
        data.loc[sell_condition, 'signal'] = -1
        
        # Alternative: Exit when price crosses middle band
        # This provides tighter risk management
        exit_long = (data['position'].shift(1) == 1) & \
                   (data['Close'] > data['BB_Middle'])
        exit_short = (data['position'].shift(1) == -1) & \
                    (data['Close'] < data['BB_Middle'])
        
        data.loc[exit_long | exit_short, 'signal'] = 0
        
        # Create position column
        data['position'] = data['signal'].replace(0, np.nan).ffill().fillna(0)
        
        return data
    
    def get_strategy_info(self) -> dict:
        """Get strategy information and parameters."""
        info = super().get_strategy_info()
        info.update({
            'period': self.period,
            'std_dev': self.std_dev
        })
        return info
