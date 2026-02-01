"""
Base Strategy Class for Algorithmic Trading
Author: Yacine Abdi
"""

from abc import ABC, abstractmethod
import pandas as pd
from typing import Dict, Optional


class BaseStrategy(ABC):
    """
    Abstract base class for all trading strategies.
    All strategies must implement the generate_signals method.
    """
    
    def __init__(self, name: str):
        """
        Initialize the base strategy.
        
        Args:
            name (str): Name of the strategy
        """
        self.name = name
        self.position = 0  # Current position: 0 (neutral), 1 (long), -1 (short)
        
    @abstractmethod
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Generate trading signals based on the strategy logic.
        
        Args:
            data (pd.DataFrame): Historical price data with OHLCV columns
            
        Returns:
            pd.DataFrame: Data with added 'signal' column (1: buy, -1: sell, 0: hold)
        """
        pass
    
    def calculate_indicators(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate technical indicators needed for the strategy.
        To be overridden by child classes if needed.
        
        Args:
            data (pd.DataFrame): Historical price data
            
        Returns:
            pd.DataFrame: Data with calculated indicators
        """
        return data
    
    def validate_data(self, data: pd.DataFrame) -> bool:
        """
        Validate that the input data has required columns.
        
        Args:
            data (pd.DataFrame): Input data to validate
            
        Returns:
            bool: True if data is valid, False otherwise
        """
        required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        return all(col in data.columns for col in required_columns)
    
    def get_strategy_info(self) -> Dict[str, str]:
        """
        Get information about the strategy.
        
        Returns:
            Dict[str, str]: Strategy metadata
        """
        return {
            'name': self.name,
            'type': self.__class__.__name__,
            'description': self.__doc__ or 'No description available'
        }
    
    def reset(self):
        """Reset strategy state."""
        self.position = 0
