"""
Backtesting Engine
Author: Yacine Abdi

Core backtesting engine that runs strategies on historical data
and tracks performance.
"""

import pandas as pd
import numpy as np
from typing import Dict, Optional
from datetime import datetime

from .portfolio import Portfolio
from ..strategies.base_strategy import BaseStrategy


class BacktestEngine:
    """
    Main backtesting engine for running trading strategies.
    """
    
    def __init__(self, initial_capital: float = 100000,
                 commission: float = 0.001,
                 position_size: float = 0.95):
        """
        Initialize backtesting engine.
        
        Args:
            initial_capital (float): Starting capital
            commission (float): Commission rate per trade (e.g., 0.001 = 0.1%)
            position_size (float): Fraction of portfolio per trade (0-1)
        """
        self.initial_capital = initial_capital
        self.commission = commission
        self.position_size = position_size
        self.portfolio: Optional[Portfolio] = None
        self.results: Dict = {}
        
    def run(self, data: pd.DataFrame, strategy: BaseStrategy, 
            verbose: bool = True) -> Dict:
        """
        Run backtest on historical data with given strategy.
        
        Args:
            data (pd.DataFrame): Historical OHLCV data
            strategy (BaseStrategy): Trading strategy to test
            verbose (bool): Print progress messages
            
        Returns:
            Dict: Backtest results and performance metrics
        """
        if verbose:
            print(f"Running backtest: {strategy.name}")
            print(f"Data period: {data.index[0]} to {data.index[-1]}")
            print(f"Initial capital: ${self.initial_capital:,.2f}")
        
        # Initialize portfolio
        self.portfolio = Portfolio(
            initial_capital=self.initial_capital,
            commission=self.commission,
            position_size=self.position_size
        )
        
        # Generate signals
        data_with_signals = strategy.generate_signals(data.copy())
        
        # Run through each bar
        for i in range(len(data_with_signals)):
            row = data_with_signals.iloc[i]
            timestamp = row.name
            price = row['Close']
            signal = row['signal']
            
            # Execute trades based on signals
            if signal == 1:  # Buy signal
                if self.portfolio.current_position == 0:
                    trade = self.portfolio.buy(price, timestamp)
                    if verbose and trade:
                        print(f"BUY: {trade.shares} shares @ ${price:.2f} on {timestamp}")
                        
            elif signal == -1:  # Sell signal
                if self.portfolio.current_position == 1:
                    trade = self.portfolio.sell(price, timestamp)
                    if verbose and trade:
                        print(f"SELL: {trade.shares} shares @ ${price:.2f} on {timestamp}")
            
            # Update portfolio value
            self.portfolio.update_value(price, timestamp)
        
        # Close any open positions at the end
        if self.portfolio.current_position == 1:
            last_price = data_with_signals.iloc[-1]['Close']
            last_timestamp = data_with_signals.index[-1]
            self.portfolio.sell(last_price, last_timestamp)
            if verbose:
                print(f"Closing position @ ${last_price:.2f}")
        
        # Calculate performance metrics
        self.results = self._calculate_metrics(data_with_signals)
        
        if verbose:
            self._print_results()
        
        return self.results
    
    def _calculate_metrics(self, data: pd.DataFrame) -> Dict:
        """
        Calculate comprehensive performance metrics.
        
        Args:
            data (pd.DataFrame): Data with signals
            
        Returns:
            Dict: Performance metrics
        """
        portfolio_summary = self.portfolio.get_summary()
        returns = self.portfolio.get_returns()
        trades = self.portfolio.get_trade_history()
        
        # Basic metrics
        total_return = portfolio_summary['total_return']
        final_value = portfolio_summary['final_value']
        
        # Calculate buy and hold benchmark
        buy_hold_return = (data['Close'].iloc[-1] - data['Close'].iloc[0]) / data['Close'].iloc[0]
        
        # Risk metrics
        if len(returns) > 0:
            sharpe_ratio = self._calculate_sharpe_ratio(returns)
            max_drawdown = self._calculate_max_drawdown(
                pd.Series(self.portfolio.portfolio_values, 
                         index=self.portfolio.timestamps)
            )
            volatility = returns.std() * np.sqrt(252)  # Annualized
        else:
            sharpe_ratio = 0
            max_drawdown = 0
            volatility = 0
        
        # Trade metrics
        if len(trades) > 0:
            winning_trades = self._calculate_winning_trades(trades)
            win_rate = winning_trades / len(trades) if len(trades) > 0 else 0
            avg_trade_return = self._calculate_avg_trade_return(trades)
        else:
            win_rate = 0
            avg_trade_return = 0
        
        return {
            'strategy_name': self.portfolio.trades[0].timestamp if self.portfolio.trades else 'N/A',
            'initial_capital': self.initial_capital,
            'final_value': final_value,
            'total_return': total_return,
            'total_return_pct': total_return * 100,
            'buy_hold_return': buy_hold_return,
            'buy_hold_return_pct': buy_hold_return * 100,
            'excess_return': total_return - buy_hold_return,
            'sharpe_ratio': sharpe_ratio,
            'max_drawdown': max_drawdown,
            'volatility': volatility,
            'num_trades': len(trades),
            'win_rate': win_rate,
            'avg_trade_return': avg_trade_return,
            'portfolio_summary': portfolio_summary,
            'trade_history': trades
        }
    
    def _calculate_sharpe_ratio(self, returns: pd.Series, 
                               risk_free_rate: float = 0.02) -> float:
        """
        Calculate Sharpe ratio (annualized).
        
        Args:
            returns (pd.Series): Return series
            risk_free_rate (float): Annual risk-free rate
            
        Returns:
            float: Sharpe ratio
        """
        if len(returns) == 0 or returns.std() == 0:
            return 0.0
        
        excess_returns = returns - (risk_free_rate / 252)  # Daily risk-free rate
        return np.sqrt(252) * excess_returns.mean() / returns.std()
    
    def _calculate_max_drawdown(self, portfolio_values: pd.Series) -> float:
        """
        Calculate maximum drawdown.
        
        Args:
            portfolio_values (pd.Series): Portfolio value over time
            
        Returns:
            float: Maximum drawdown (negative value)
        """
        if len(portfolio_values) == 0:
            return 0.0
        
        cumulative_max = portfolio_values.expanding().max()
        drawdown = (portfolio_values - cumulative_max) / cumulative_max
        return drawdown.min()
    
    def _calculate_winning_trades(self, trades: pd.DataFrame) -> int:
        """
        Count number of winning trades.
        
        Args:
            trades (pd.DataFrame): Trade history
            
        Returns:
            int: Number of winning trades
        """
        if len(trades) < 2:
            return 0
        
        winning = 0
        for i in range(0, len(trades) - 1, 2):
            if i + 1 < len(trades):
                buy_price = trades.iloc[i]['Price']
                sell_price = trades.iloc[i + 1]['Price']
                if sell_price > buy_price:
                    winning += 1
        
        return winning
    
    def _calculate_avg_trade_return(self, trades: pd.DataFrame) -> float:
        """
        Calculate average return per trade.
        
        Args:
            trades (pd.DataFrame): Trade history
            
        Returns:
            float: Average trade return
        """
        if len(trades) < 2:
            return 0.0
        
        returns = []
        for i in range(0, len(trades) - 1, 2):
            if i + 1 < len(trades):
                buy_price = trades.iloc[i]['Price']
                sell_price = trades.iloc[i + 1]['Price']
                ret = (sell_price - buy_price) / buy_price
                returns.append(ret)
        
        return np.mean(returns) if returns else 0.0
    
    def _print_results(self):
        """Print formatted results."""
        print("\n" + "="*60)
        print("BACKTEST RESULTS")
        print("="*60)
        print(f"Initial Capital:     ${self.results['initial_capital']:>15,.2f}")
        print(f"Final Value:         ${self.results['final_value']:>15,.2f}")
        print(f"Total Return:        {self.results['total_return_pct']:>15.2f}%")
        print(f"Buy & Hold Return:   {self.results['buy_hold_return_pct']:>15.2f}%")
        print(f"Excess Return:       {self.results['excess_return']*100:>15.2f}%")
        print("-"*60)
        print(f"Sharpe Ratio:        {self.results['sharpe_ratio']:>15.2f}")
        print(f"Max Drawdown:        {self.results['max_drawdown']*100:>15.2f}%")
        print(f"Volatility:          {self.results['volatility']*100:>15.2f}%")
        print("-"*60)
        print(f"Number of Trades:    {self.results['num_trades']:>15}")
        print(f"Win Rate:            {self.results['win_rate']*100:>15.2f}%")
        print(f"Avg Trade Return:    {self.results['avg_trade_return']*100:>15.2f}%")
        print("="*60 + "\n")
    
    def get_portfolio_history(self) -> pd.DataFrame:
        """
        Get portfolio value history as DataFrame.
        
        Returns:
            pd.DataFrame: Portfolio values over time
        """
        if not self.portfolio or not self.portfolio.portfolio_values:
            return pd.DataFrame()
        
        return pd.DataFrame({
            'Portfolio_Value': self.portfolio.portfolio_values
        }, index=self.portfolio.timestamps)
