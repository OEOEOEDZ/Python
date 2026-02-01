"""
Performance Analytics Module
Author: Yacine Abdi

Advanced performance metrics and analysis tools.
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple
from scipy import stats


class PerformanceMetrics:
    """
    Calculate comprehensive trading performance metrics.
    """
    
    @staticmethod
    def calculate_returns(prices: pd.Series) -> pd.Series:
        """Calculate simple returns."""
        return prices.pct_change().dropna()
    
    @staticmethod
    def calculate_log_returns(prices: pd.Series) -> pd.Series:
        """Calculate logarithmic returns."""
        return np.log(prices / prices.shift(1)).dropna()
    
    @staticmethod
    def calculate_cumulative_returns(returns: pd.Series) -> pd.Series:
        """Calculate cumulative returns."""
        return (1 + returns).cumprod() - 1
    
    @staticmethod
    def sharpe_ratio(returns: pd.Series, risk_free_rate: float = 0.02,
                    periods_per_year: int = 252) -> float:
        """
        Calculate Sharpe Ratio.
        
        Args:
            returns (pd.Series): Return series
            risk_free_rate (float): Annual risk-free rate
            periods_per_year (int): Trading periods per year
            
        Returns:
            float: Sharpe ratio
        """
        if len(returns) == 0 or returns.std() == 0:
            return 0.0
        
        excess_returns = returns - (risk_free_rate / periods_per_year)
        return np.sqrt(periods_per_year) * excess_returns.mean() / returns.std()
    
    @staticmethod
    def sortino_ratio(returns: pd.Series, risk_free_rate: float = 0.02,
                     periods_per_year: int = 252) -> float:
        """
        Calculate Sortino Ratio (uses downside deviation).
        
        Args:
            returns (pd.Series): Return series
            risk_free_rate (float): Annual risk-free rate
            periods_per_year (int): Trading periods per year
            
        Returns:
            float: Sortino ratio
        """
        if len(returns) == 0:
            return 0.0
        
        excess_returns = returns - (risk_free_rate / periods_per_year)
        downside_returns = excess_returns[excess_returns < 0]
        
        if len(downside_returns) == 0 or downside_returns.std() == 0:
            return 0.0
        
        downside_std = downside_returns.std()
        return np.sqrt(periods_per_year) * excess_returns.mean() / downside_std
    
    @staticmethod
    def max_drawdown(prices: pd.Series) -> Tuple[float, pd.Timestamp, pd.Timestamp]:
        """
        Calculate maximum drawdown and its dates.
        
        Args:
            prices (pd.Series): Price series
            
        Returns:
            Tuple: (max_drawdown, peak_date, trough_date)
        """
        cumulative_max = prices.expanding().max()
        drawdown = (prices - cumulative_max) / cumulative_max
        
        max_dd = drawdown.min()
        trough_date = drawdown.idxmin()
        peak_date = prices[:trough_date].idxmax()
        
        return max_dd, peak_date, trough_date
    
    @staticmethod
    def calmar_ratio(returns: pd.Series, prices: pd.Series,
                    periods_per_year: int = 252) -> float:
        """
        Calculate Calmar Ratio (return / max drawdown).
        
        Args:
            returns (pd.Series): Return series
            prices (pd.Series): Price series
            periods_per_year (int): Trading periods per year
            
        Returns:
            float: Calmar ratio
        """
        if len(returns) == 0:
            return 0.0
        
        annual_return = returns.mean() * periods_per_year
        max_dd, _, _ = PerformanceMetrics.max_drawdown(prices)
        
        if max_dd == 0:
            return 0.0
        
        return annual_return / abs(max_dd)
    
    @staticmethod
    def value_at_risk(returns: pd.Series, confidence_level: float = 0.95) -> float:
        """
        Calculate Value at Risk (VaR).
        
        Args:
            returns (pd.Series): Return series
            confidence_level (float): Confidence level (default: 0.95)
            
        Returns:
            float: VaR value
        """
        if len(returns) == 0:
            return 0.0
        
        return np.percentile(returns, (1 - confidence_level) * 100)
    
    @staticmethod
    def conditional_var(returns: pd.Series, confidence_level: float = 0.95) -> float:
        """
        Calculate Conditional Value at Risk (CVaR or Expected Shortfall).
        
        Args:
            returns (pd.Series): Return series
            confidence_level (float): Confidence level
            
        Returns:
            float: CVaR value
        """
        if len(returns) == 0:
            return 0.0
        
        var = PerformanceMetrics.value_at_risk(returns, confidence_level)
        return returns[returns <= var].mean()
    
    @staticmethod
    def information_ratio(returns: pd.Series, benchmark_returns: pd.Series) -> float:
        """
        Calculate Information Ratio.
        
        Args:
            returns (pd.Series): Strategy returns
            benchmark_returns (pd.Series): Benchmark returns
            
        Returns:
            float: Information ratio
        """
        if len(returns) == 0 or len(benchmark_returns) == 0:
            return 0.0
        
        excess_returns = returns - benchmark_returns
        tracking_error = excess_returns.std()
        
        if tracking_error == 0:
            return 0.0
        
        return excess_returns.mean() / tracking_error
    
    @staticmethod
    def omega_ratio(returns: pd.Series, threshold: float = 0.0) -> float:
        """
        Calculate Omega Ratio.
        
        Args:
            returns (pd.Series): Return series
            threshold (float): Threshold return
            
        Returns:
            float: Omega ratio
        """
        if len(returns) == 0:
            return 0.0
        
        gains = returns[returns > threshold] - threshold
        losses = threshold - returns[returns < threshold]
        
        if losses.sum() == 0:
            return float('inf') if gains.sum() > 0 else 0.0
        
        return gains.sum() / losses.sum()
    
    @staticmethod
    def win_rate(trades: pd.DataFrame) -> float:
        """
        Calculate win rate from trade history.
        
        Args:
            trades (pd.DataFrame): Trade history
            
        Returns:
            float: Win rate (0-1)
        """
        if len(trades) < 2:
            return 0.0
        
        winning_trades = 0
        total_pairs = 0
        
        for i in range(0, len(trades) - 1, 2):
            if i + 1 < len(trades):
                buy_price = trades.iloc[i]['Price']
                sell_price = trades.iloc[i + 1]['Price']
                if sell_price > buy_price:
                    winning_trades += 1
                total_pairs += 1
        
        return winning_trades / total_pairs if total_pairs > 0 else 0.0
    
    @staticmethod
    def profit_factor(trades: pd.DataFrame) -> float:
        """
        Calculate profit factor (gross profit / gross loss).
        
        Args:
            trades (pd.DataFrame): Trade history
            
        Returns:
            float: Profit factor
        """
        if len(trades) < 2:
            return 0.0
        
        gross_profit = 0
        gross_loss = 0
        
        for i in range(0, len(trades) - 1, 2):
            if i + 1 < len(trades):
                buy_price = trades.iloc[i]['Price']
                buy_shares = trades.iloc[i]['Shares']
                sell_price = trades.iloc[i + 1]['Price']
                
                pnl = (sell_price - buy_price) * buy_shares
                
                if pnl > 0:
                    gross_profit += pnl
                else:
                    gross_loss += abs(pnl)
        
        return gross_profit / gross_loss if gross_loss > 0 else 0.0
    
    @staticmethod
    def generate_report(returns: pd.Series, prices: pd.Series,
                       trades: pd.DataFrame, initial_capital: float) -> Dict:
        """
        Generate comprehensive performance report.
        
        Args:
            returns (pd.Series): Return series
            prices (pd.Series): Price series
            trades (pd.DataFrame): Trade history
            initial_capital (float): Starting capital
            
        Returns:
            Dict: Complete performance metrics
        """
        if len(returns) == 0:
            return {}
        
        max_dd, peak_date, trough_date = PerformanceMetrics.max_drawdown(prices)
        
        return {
            'Total Return': PerformanceMetrics.calculate_cumulative_returns(returns).iloc[-1],
            'Annual Return': returns.mean() * 252,
            'Volatility': returns.std() * np.sqrt(252),
            'Sharpe Ratio': PerformanceMetrics.sharpe_ratio(returns),
            'Sortino Ratio': PerformanceMetrics.sortino_ratio(returns),
            'Max Drawdown': max_dd,
            'Calmar Ratio': PerformanceMetrics.calmar_ratio(returns, prices),
            'VaR (95%)': PerformanceMetrics.value_at_risk(returns),
            'CVaR (95%)': PerformanceMetrics.conditional_var(returns),
            'Omega Ratio': PerformanceMetrics.omega_ratio(returns),
            'Win Rate': PerformanceMetrics.win_rate(trades),
            'Profit Factor': PerformanceMetrics.profit_factor(trades),
            'Number of Trades': len(trades),
            'Peak Date': peak_date,
            'Trough Date': trough_date
        }
