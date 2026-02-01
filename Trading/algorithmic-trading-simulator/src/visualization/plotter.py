"""
Visualization Module
Author: Yacine Abdi

Plotting and visualization tools for backtest results.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from typing import Optional, Dict
import seaborn as sns


class Plotter:
    """
    Visualization tools for trading strategies and backtest results.
    """
    
    def __init__(self, style: str = 'seaborn-v0_8-darkgrid'):
        """
        Initialize plotter with style.
        
        Args:
            style (str): Matplotlib style
        """
        try:
            plt.style.use(style)
        except:
            plt.style.use('default')
        
        self.colors = {
            'buy': 'green',
            'sell': 'red',
            'portfolio': 'blue',
            'benchmark': 'orange',
            'profit': 'green',
            'loss': 'red'
        }
    
    def plot_price_and_signals(self, data: pd.DataFrame, 
                               title: str = 'Price and Trading Signals',
                               figsize: tuple = (14, 7)):
        """
        Plot price chart with buy/sell signals.
        
        Args:
            data (pd.DataFrame): Data with price and signals
            title (str): Plot title
            figsize (tuple): Figure size
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        # Plot price
        ax.plot(data.index, data['Close'], label='Close Price', 
                color='black', linewidth=1.5, alpha=0.7)
        
        # Plot buy signals
        buy_signals = data[data['signal'] == 1]
        ax.scatter(buy_signals.index, buy_signals['Close'], 
                  color=self.colors['buy'], marker='^', s=100, 
                  label='Buy Signal', zorder=5)
        
        # Plot sell signals
        sell_signals = data[data['signal'] == -1]
        ax.scatter(sell_signals.index, sell_signals['Close'], 
                  color=self.colors['sell'], marker='v', s=100, 
                  label='Sell Signal', zorder=5)
        
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Price ($)', fontsize=12)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.legend(loc='best')
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def plot_portfolio_value(self, portfolio_history: pd.DataFrame,
                            initial_capital: float,
                            title: str = 'Portfolio Value Over Time',
                            figsize: tuple = (14, 7)):
        """
        Plot portfolio value over time.
        
        Args:
            portfolio_history (pd.DataFrame): Portfolio values
            initial_capital (float): Starting capital
            title (str): Plot title
            figsize (tuple): Figure size
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        # Plot portfolio value
        ax.plot(portfolio_history.index, portfolio_history['Portfolio_Value'],
               label='Portfolio Value', color=self.colors['portfolio'], 
               linewidth=2)
        
        # Plot initial capital line
        ax.axhline(y=initial_capital, color='gray', linestyle='--', 
                  label='Initial Capital', alpha=0.7)
        
        # Fill area
        ax.fill_between(portfolio_history.index, 
                       portfolio_history['Portfolio_Value'],
                       initial_capital, 
                       where=portfolio_history['Portfolio_Value'] >= initial_capital,
                       alpha=0.3, color=self.colors['profit'])
        ax.fill_between(portfolio_history.index, 
                       portfolio_history['Portfolio_Value'],
                       initial_capital,
                       where=portfolio_history['Portfolio_Value'] < initial_capital,
                       alpha=0.3, color=self.colors['loss'])
        
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Portfolio Value ($)', fontsize=12)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.legend(loc='best')
        ax.grid(True, alpha=0.3)
        
        # Format y-axis as currency
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
        
        plt.tight_layout()
        return fig
    
    def plot_returns_distribution(self, returns: pd.Series,
                                 title: str = 'Returns Distribution',
                                 figsize: tuple = (12, 6)):
        """
        Plot returns distribution histogram.
        
        Args:
            returns (pd.Series): Returns series
            title (str): Plot title
            figsize (tuple): Figure size
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
        
        # Histogram
        ax1.hist(returns, bins=50, edgecolor='black', alpha=0.7,
                color=self.colors['portfolio'])
        ax1.axvline(returns.mean(), color='red', linestyle='--', 
                   linewidth=2, label=f'Mean: {returns.mean():.4f}')
        ax1.set_xlabel('Returns', fontsize=12)
        ax1.set_ylabel('Frequency', fontsize=12)
        ax1.set_title('Returns Histogram', fontsize=12, fontweight='bold')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Q-Q plot
        from scipy import stats
        stats.probplot(returns, dist="norm", plot=ax2)
        ax2.set_title('Q-Q Plot', fontsize=12, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        
        fig.suptitle(title, fontsize=14, fontweight='bold', y=1.02)
        plt.tight_layout()
        return fig
    
    def plot_drawdown(self, portfolio_history: pd.DataFrame,
                     title: str = 'Drawdown Over Time',
                     figsize: tuple = (14, 6)):
        """
        Plot drawdown over time.
        
        Args:
            portfolio_history (pd.DataFrame): Portfolio values
            title (str): Plot title
            figsize (tuple): Figure size
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        # Calculate drawdown
        portfolio_values = portfolio_history['Portfolio_Value']
        cumulative_max = portfolio_values.expanding().max()
        drawdown = (portfolio_values - cumulative_max) / cumulative_max
        
        # Plot drawdown
        ax.fill_between(drawdown.index, 0, drawdown, 
                       color=self.colors['loss'], alpha=0.5)
        ax.plot(drawdown.index, drawdown, color=self.colors['loss'], 
               linewidth=1.5)
        
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Drawdown (%)', fontsize=12)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        # Format y-axis as percentage
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x*100:.1f}%'))
        
        plt.tight_layout()
        return fig
    
    def plot_strategy_comparison(self, results_dict: Dict[str, pd.DataFrame],
                               title: str = 'Strategy Comparison',
                               figsize: tuple = (14, 7)):
        """
        Compare multiple strategies.
        
        Args:
            results_dict (Dict): Dictionary of strategy names to portfolio histories
            title (str): Plot title
            figsize (tuple): Figure size
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        for strategy_name, portfolio_history in results_dict.items():
            ax.plot(portfolio_history.index, 
                   portfolio_history['Portfolio_Value'],
                   label=strategy_name, linewidth=2)
        
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Portfolio Value ($)', fontsize=12)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.legend(loc='best')
        ax.grid(True, alpha=0.3)
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
        
        plt.tight_layout()
        return fig
    
    def plot_monthly_returns_heatmap(self, returns: pd.Series,
                                    title: str = 'Monthly Returns Heatmap',
                                    figsize: tuple = (12, 6)):
        """
        Create heatmap of monthly returns.
        
        Args:
            returns (pd.Series): Returns series
            title (str): Plot title
            figsize (tuple): Figure size
        """
        # Resample to monthly returns
        monthly_returns = returns.resample('M').apply(lambda x: (1 + x).prod() - 1)
        
        # Create pivot table
        monthly_returns_df = pd.DataFrame({
            'Year': monthly_returns.index.year,
            'Month': monthly_returns.index.month,
            'Return': monthly_returns.values
        })
        pivot = monthly_returns_df.pivot(index='Month', columns='Year', values='Return')
        
        # Create heatmap
        fig, ax = plt.subplots(figsize=figsize)
        sns.heatmap(pivot * 100, annot=True, fmt='.2f', cmap='RdYlGn', 
                   center=0, ax=ax, cbar_kws={'label': 'Return (%)'})
        
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_ylabel('Month', fontsize=12)
        ax.set_xlabel('Year', fontsize=12)
        
        # Set month labels
        month_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                       'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        ax.set_yticklabels(month_labels, rotation=0)
        
        plt.tight_layout()
        return fig
    
    def create_dashboard(self, data: pd.DataFrame, 
                        portfolio_history: pd.DataFrame,
                        returns: pd.Series,
                        initial_capital: float,
                        results: Dict,
                        save_path: Optional[str] = None):
        """
        Create comprehensive dashboard with all visualizations.
        
        Args:
            data (pd.DataFrame): Price data with signals
            portfolio_history (pd.DataFrame): Portfolio values
            returns (pd.Series): Returns series
            initial_capital (float): Starting capital
            results (Dict): Backtest results
            save_path (str, optional): Path to save figure
        """
        fig = plt.figure(figsize=(20, 12))
        gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
        
        # Price and signals
        ax1 = fig.add_subplot(gs[0, :])
        ax1.plot(data.index, data['Close'], color='black', linewidth=1.5, alpha=0.7)
        buy_signals = data[data['signal'] == 1]
        sell_signals = data[data['signal'] == -1]
        ax1.scatter(buy_signals.index, buy_signals['Close'], 
                   color='green', marker='^', s=100, zorder=5)
        ax1.scatter(sell_signals.index, sell_signals['Close'], 
                   color='red', marker='v', s=100, zorder=5)
        ax1.set_title('Price and Trading Signals', fontsize=14, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        
        # Portfolio value
        ax2 = fig.add_subplot(gs[1, :])
        ax2.plot(portfolio_history.index, portfolio_history['Portfolio_Value'],
                color='blue', linewidth=2)
        ax2.axhline(y=initial_capital, color='gray', linestyle='--', alpha=0.7)
        ax2.fill_between(portfolio_history.index, 
                        portfolio_history['Portfolio_Value'],
                        initial_capital,
                        where=portfolio_history['Portfolio_Value'] >= initial_capital,
                        alpha=0.3, color='green')
        ax2.set_title('Portfolio Value', fontsize=14, fontweight='bold')
        ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
        ax2.grid(True, alpha=0.3)
        
        # Returns distribution
        ax3 = fig.add_subplot(gs[2, 0])
        ax3.hist(returns, bins=50, edgecolor='black', alpha=0.7)
        ax3.axvline(returns.mean(), color='red', linestyle='--', linewidth=2)
        ax3.set_title('Returns Distribution', fontsize=12, fontweight='bold')
        ax3.grid(True, alpha=0.3)
        
        # Drawdown
        ax4 = fig.add_subplot(gs[2, 1])
        portfolio_values = portfolio_history['Portfolio_Value']
        cumulative_max = portfolio_values.expanding().max()
        drawdown = (portfolio_values - cumulative_max) / cumulative_max
        ax4.fill_between(drawdown.index, 0, drawdown, color='red', alpha=0.5)
        ax4.set_title('Drawdown', fontsize=12, fontweight='bold')
        ax4.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x*100:.1f}%'))
        ax4.grid(True, alpha=0.3)
        
        # Performance metrics table
        ax5 = fig.add_subplot(gs[2, 2])
        ax5.axis('off')
        metrics_text = f"""
        Performance Metrics
        {'='*30}
        Total Return: {results['total_return_pct']:.2f}%
        Sharpe Ratio: {results['sharpe_ratio']:.2f}
        Max Drawdown: {results['max_drawdown']*100:.2f}%
        Win Rate: {results['win_rate']*100:.2f}%
        Trades: {results['num_trades']}
        """
        ax5.text(0.1, 0.5, metrics_text, fontsize=11, family='monospace',
                verticalalignment='center')
        
        fig.suptitle('Trading Strategy Dashboard', fontsize=16, fontweight='bold')
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Dashboard saved to {save_path}")
        
        return fig
