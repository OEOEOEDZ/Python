"""
MACD (Moving Average Convergence Divergence) Trading Strategy
Author: Yacine Abdi

This strategy uses MACD line and signal line crossovers to identify
trend changes and generate trading signals.
"""

import pandas as pd
import numpy as np
from .base_strategy import BaseStrategy


class MACDStrategy(BaseStrategy):
    """
    MACD-based momentum trading strategy.
    """
    
    def __init__(self, fast_period: int = 12, slow_period: int = 26, 
                 signal_period: int = 9):
        """
        Initialize MACD strategy.
        
        Args:
            fast_period (int): Fast EMA period (default: 12)
            slow_period (int): Slow EMA period (default: 26)
            signal_period (int): Signal line period (default: 9)
        """
        super().__init__(name='MACD Strategy')
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.signal_period = signal_period
        
    def calculate_ema(self, prices: pd.Series, period: int) -> pd.Series:
        """
        Calculate Exponential Moving Average.
        
        Args:
            prices (pd.Series): Price series
            period (int): EMA period
            
        Returns:
            pd.Series: EMA values
        """
        return prices.ewm(span=period, adjust=False).mean()
    
    def calculate_indicators(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate MACD, signal line, and histogram.
        
        Args:
            data (pd.DataFrame): Historical price data
            
        Returns:
            pd.DataFrame: Data with MACD indicators
        """
        data = data.copy()
        
        # Calculate MACD line
        fast_ema = self.calculate_ema(data['Close'], self.fast_period)
        slow_ema = self.calculate_ema(data['Close'], self.slow_period)
        data['MACD'] = fast_ema - slow_ema
        
        # Calculate signal line
        data['MACD_Signal'] = self.calculate_ema(data['MACD'], self.signal_period)
        
        # Calculate MACD histogram
        data['MACD_Histogram'] = data['MACD'] - data['MACD_Signal']
        
        return data
    
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Generate trading signals based on MACD crossovers.
        
        Args:
            data (pd.DataFrame): Historical price data
            
        Returns:
            pd.DataFrame: Data with signal column
        """
        if not self.validate_data(data):
            raise ValueError("Invalid data format. Required columns: OHLCV")
        
        data = self.calculate_indicators(data)
        data['signal'] = 0
        
        # Previous values for crossover detection
        data['MACD_prev'] = data['MACD'].shift(1)
        data['Signal_prev'] = data['MACD_Signal'].shift(1)
        
        # Buy signal: MACD crosses above signal line
        buy_condition = (data['MACD'] > data['MACD_Signal']) & \
                       (data['MACD_prev'] <= data['Signal_prev'])
        data.loc[buy_condition, 'signal'] = 1
        
        # Sell signal: MACD crosses below signal line
        sell_condition = (data['MACD'] < data['MACD_Signal']) & \
                        (data['MACD_prev'] >= data['Signal_prev'])
        data.loc[sell_condition, 'signal'] = -1
        
        # Create position column
        data['position'] = data['signal'].replace(0, np.nan).ffill().fillna(0)
        
        # Clean up temporary columns
        data.drop(['MACD_prev', 'Signal_prev'], axis=1, inplace=True)
        
        return data
    
    def get_strategy_info(self) -> dict:
        """Get strategy information and parameters."""
        info = super().get_strategy_info()
        info.update({
            'fast_period': self.fast_period,
            'slow_period': self.slow_period,
            'signal_period': self.signal_period
        })
        return info
