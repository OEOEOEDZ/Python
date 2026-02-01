"""
Portfolio Management Module
Author: Yacine Abdi

Handles portfolio state, position management, and transaction recording.
"""

import pandas as pd
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Trade:
    """Data class representing a single trade."""
    timestamp: datetime
    action: str  # 'BUY' or 'SELL'
    price: float
    shares: int
    commission: float = 0.0
    
    @property
    def value(self) -> float:
        """Calculate total trade value including commission."""
        return (self.price * self.shares) + self.commission


class Portfolio:
    """
    Manages portfolio state including cash, positions, and trade history.
    """
    
    def __init__(self, initial_capital: float = 100000, 
                 commission: float = 0.0,
                 position_size: float = 1.0):
        """
        Initialize portfolio.
        
        Args:
            initial_capital (float): Starting cash amount
            commission (float): Commission per trade (default: 0)
            position_size (float): Fraction of portfolio to use per trade (0-1)
        """
        self.initial_capital = initial_capital
        self.cash = initial_capital
        self.commission = commission
        self.position_size = max(0.0, min(1.0, position_size))
        
        self.shares = 0
        self.current_position = 0  # 0: neutral, 1: long, -1: short
        self.trades: List[Trade] = []
        self.portfolio_values: List[float] = []
        self.timestamps: List[datetime] = []
        
    def can_buy(self, price: float) -> bool:
        """
        Check if we have enough cash to buy.
        
        Args:
            price (float): Current price
            
        Returns:
            bool: True if we can buy
        """
        capital_to_use = self.cash * self.position_size
        max_shares = int(capital_to_use / (price + self.commission))
        return max_shares > 0
    
    def can_sell(self) -> bool:
        """
        Check if we have shares to sell.
        
        Returns:
            bool: True if we can sell
        """
        return self.shares > 0
    
    def buy(self, price: float, timestamp: datetime) -> Optional[Trade]:
        """
        Execute a buy order.
        
        Args:
            price (float): Purchase price
            timestamp (datetime): Trade timestamp
            
        Returns:
            Trade: Trade object if successful, None otherwise
        """
        if not self.can_buy(price):
            return None
        
        # Calculate shares to buy
        capital_to_use = self.cash * self.position_size
        shares = int(capital_to_use / (price + self.commission))
        total_cost = (shares * price) + (shares * self.commission)
        
        if total_cost > self.cash:
            shares -= 1
            total_cost = (shares * price) + (shares * self.commission)
        
        if shares <= 0:
            return None
        
        # Execute trade
        self.cash -= total_cost
        self.shares += shares
        self.current_position = 1
        
        trade = Trade(
            timestamp=timestamp,
            action='BUY',
            price=price,
            shares=shares,
            commission=shares * self.commission
        )
        self.trades.append(trade)
        
        return trade
    
    def sell(self, price: float, timestamp: datetime) -> Optional[Trade]:
        """
        Execute a sell order.
        
        Args:
            price (float): Sale price
            timestamp (datetime): Trade timestamp
            
        Returns:
            Trade: Trade object if successful, None otherwise
        """
        if not self.can_sell():
            return None
        
        shares = self.shares
        total_value = (shares * price) - (shares * self.commission)
        
        # Execute trade
        self.cash += total_value
        self.shares = 0
        self.current_position = 0
        
        trade = Trade(
            timestamp=timestamp,
            action='SELL',
            price=price,
            shares=shares,
            commission=shares * self.commission
        )
        self.trades.append(trade)
        
        return trade
    
    def update_value(self, current_price: float, timestamp: datetime):
        """
        Update portfolio value tracking.
        
        Args:
            current_price (float): Current market price
            timestamp (datetime): Current timestamp
        """
        portfolio_value = self.cash + (self.shares * current_price)
        self.portfolio_values.append(portfolio_value)
        self.timestamps.append(timestamp)
    
    def get_total_value(self, current_price: float) -> float:
        """
        Calculate current total portfolio value.
        
        Args:
            current_price (float): Current market price
            
        Returns:
            float: Total portfolio value
        """
        return self.cash + (self.shares * current_price)
    
    def get_returns(self) -> pd.Series:
        """
        Calculate portfolio returns over time.
        
        Returns:
            pd.Series: Returns series
        """
        if not self.portfolio_values:
            return pd.Series()
        
        returns = pd.Series(self.portfolio_values, index=self.timestamps)
        return returns.pct_change().dropna()
    
    def get_trade_history(self) -> pd.DataFrame:
        """
        Get trade history as DataFrame.
        
        Returns:
            pd.DataFrame: Trade history
        """
        if not self.trades:
            return pd.DataFrame()
        
        trade_data = []
        for trade in self.trades:
            trade_data.append({
                'Timestamp': trade.timestamp,
                'Action': trade.action,
                'Price': trade.price,
                'Shares': trade.shares,
                'Commission': trade.commission,
                'Total': trade.value
            })
        
        return pd.DataFrame(trade_data)
    
    def reset(self):
        """Reset portfolio to initial state."""
        self.cash = self.initial_capital
        self.shares = 0
        self.current_position = 0
        self.trades.clear()
        self.portfolio_values.clear()
        self.timestamps.clear()
    
    def get_summary(self) -> Dict:
        """
        Get portfolio summary statistics.
        
        Returns:
            Dict: Summary statistics
        """
        current_value = self.portfolio_values[-1] if self.portfolio_values else self.initial_capital
        total_return = (current_value - self.initial_capital) / self.initial_capital
        
        return {
            'initial_capital': self.initial_capital,
            'final_value': current_value,
            'total_return': total_return,
            'total_return_pct': total_return * 100,
            'cash': self.cash,
            'shares': self.shares,
            'num_trades': len(self.trades),
            'current_position': self.current_position
        }
