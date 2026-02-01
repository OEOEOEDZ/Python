"""
RSI (Relative Strength Index) Trading Strategy
Author: Yacine Abdi

This strategy uses RSI to identify overbought and oversold conditions.
Buy signal when RSI crosses above oversold threshold.
Sell signal when RSI crosses below overbought threshold.
"""

import pandas as pd
import numpy as np
from .base_strategy import BaseStrategy


class RSIStrategy(BaseStrategy):
    """
    RSI-based mean reversion trading strategy.
    """
    
    def __init__(self, rsi_period: int = 14, oversold: int = 30, 
                 overbought: int = 70):
        """
        Initialize RSI strategy.
        
        Args:
            rsi_period (int): Period for RSI calculation (default: 14)
            oversold (int): Oversold threshold (default: 30)
            overbought (int): Overbought threshold (default: 70)
        """
        super().__init__(name='RSI Strategy')
        self.rsi_period = rsi_period
        self.oversold = oversold
        self.overbought = overbought
        
    def calculate_rsi(self, prices: pd.Series, period: int) -> pd.Series:
        """
        Calculate Relative Strength Index.
        
        Args:
            prices (pd.Series): Price series
            period (int): RSI period
            
        Returns:
            pd.Series: RSI values
        """
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def calculate_indicators(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate RSI indicator.
        
        Args:
            data (pd.DataFrame): Historical price data
            
        Returns:
            pd.DataFrame: Data with RSI column
        """
        data = data.copy()
        data['RSI'] = self.calculate_rsi(data['Close'], self.rsi_period)
        return data
    
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Generate trading signals based on RSI levels.
        
        Args:
            data (pd.DataFrame): Historical price data
            
        Returns:
            pd.DataFrame: Data with signal column
        """
        if not self.validate_data(data):
            raise ValueError("Invalid data format. Required columns: OHLCV")
        
        data = self.calculate_indicators(data)
        data['signal'] = 0
        
        # Generate buy signals when RSI crosses above oversold
        data.loc[data['RSI'] < self.oversold, 'signal'] = 1
        
        # Generate sell signals when RSI crosses above overbought
        data.loc[data['RSI'] > self.overbought, 'signal'] = -1
        
        # Create position column (tracks current position)
        data['position'] = data['signal'].replace(0, np.nan).ffill().fillna(0)
        
        return data
    
    def get_strategy_info(self) -> dict:
        """Get strategy information and parameters."""
        info = super().get_strategy_info()
        info.update({
            'rsi_period': self.rsi_period,
            'oversold_threshold': self.oversold,
            'overbought_threshold': self.overbought
        })
        return info
