"""
Mean Reversion Trading Strategy
Author: Yacine Abdi

Statistical arbitrage strategy that assumes prices will revert to their mean.
Uses z-score to identify extreme deviations from the mean.
"""

import pandas as pd
import numpy as np
from .base_strategy import BaseStrategy


class MeanReversionStrategy(BaseStrategy):
    """
    Mean reversion strategy using z-score.
    """
    
    def __init__(self, lookback_period: int = 20, z_entry: float = 2.0, 
                 z_exit: float = 0.5):
        """
        Initialize Mean Reversion strategy.
        
        Args:
            lookback_period (int): Period for calculating mean and std (default: 20)
            z_entry (float): Z-score threshold for entry (default: 2.0)
            z_exit (float): Z-score threshold for exit (default: 0.5)
        """
        super().__init__(name='Mean Reversion Strategy')
        self.lookback_period = lookback_period
        self.z_entry = z_entry
        self.z_exit = z_exit
    
    def calculate_zscore(self, prices: pd.Series, window: int) -> pd.Series:
        """
        Calculate z-score (number of standard deviations from mean).
        
        Args:
            prices (pd.Series): Price series
            window (int): Lookback window
            
        Returns:
            pd.Series: Z-score values
        """
        rolling_mean = prices.rolling(window=window).mean()
        rolling_std = prices.rolling(window=window).std()
        
        zscore = (prices - rolling_mean) / rolling_std
        return zscore
    
    def calculate_indicators(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate mean reversion indicators.
        
        Args:
            data (pd.DataFrame): Historical price data
            
        Returns:
            pd.DataFrame: Data with z-score and rolling statistics
        """
        data = data.copy()
        
        # Calculate rolling mean and standard deviation
        data['Rolling_Mean'] = data['Close'].rolling(
            window=self.lookback_period
        ).mean()
        data['Rolling_Std'] = data['Close'].rolling(
            window=self.lookback_period
        ).std()
        
        # Calculate z-score
        data['Z_Score'] = self.calculate_zscore(
            data['Close'], 
            self.lookback_period
        )
        
        return data
    
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Generate trading signals based on z-score thresholds.
        
        Args:
            data (pd.DataFrame): Historical price data
            
        Returns:
            pd.DataFrame: Data with signal column
        """
        if not self.validate_data(data):
            raise ValueError("Invalid data format. Required columns: OHLCV")
        
        data = self.calculate_indicators(data)
        data['signal'] = 0
        data['position'] = 0
        
        # Track current position
        position = 0
        signals = []
        positions = []
        
        for i in range(len(data)):
            z_score = data['Z_Score'].iloc[i]
            signal = 0
            
            if pd.isna(z_score):
                signals.append(signal)
                positions.append(position)
                continue
            
            # Entry signals
            if position == 0:
                if z_score < -self.z_entry:  # Price too low, buy
                    signal = 1
                    position = 1
                elif z_score > self.z_entry:  # Price too high, sell short
                    signal = -1
                    position = -1
            
            # Exit signals
            elif position == 1:  # Long position
                if z_score > -self.z_exit:  # Close to mean, exit
                    signal = -1
                    position = 0
            
            elif position == -1:  # Short position
                if z_score < self.z_exit:  # Close to mean, exit
                    signal = 1
                    position = 0
            
            signals.append(signal)
            positions.append(position)
        
        data['signal'] = signals
        data['position'] = positions
        
        return data
    
    def get_strategy_info(self) -> dict:
        """Get strategy information and parameters."""
        info = super().get_strategy_info()
        info.update({
            'lookback_period': self.lookback_period,
            'z_entry': self.z_entry,
            'z_exit': self.z_exit
        })
        return info
