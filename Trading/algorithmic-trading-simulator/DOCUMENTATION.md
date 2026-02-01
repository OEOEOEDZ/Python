# Documentation - Algorithmic Trading Simulator

**Author:** Yacine Abdi

## Table of Contents

1. [Installation](#installation)
2. [Quick Start](#quick-start)
3. [Core Concepts](#core-concepts)
4. [Strategies](#strategies)
5. [Backtesting](#backtesting)
6. [Performance Metrics](#performance-metrics)
7. [Visualization](#visualization)
8. [API Reference](#api-reference)
9. [Advanced Usage](#advanced-usage)

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Install from source

```bash
git clone https://github.com/yourusername/algorithmic-trading-simulator.git
cd algorithmic-trading-simulator
pip install -r requirements.txt
```

### Install as package

```bash
pip install -e .
```

## Quick Start

### Basic Example

```python
from src.data.data_loader import DataLoader
from src.strategies import RSIStrategy
from src.backtester.engine import BacktestEngine

# Load data
loader = DataLoader()
data = loader.fetch_data('AAPL', '2023-01-01', '2024-01-01')

# Initialize strategy
strategy = RSIStrategy(rsi_period=14, oversold=30, overbought=70)

# Run backtest
engine = BacktestEngine(initial_capital=100000)
results = engine.run(data, strategy)

print(f"Total Return: {results['total_return_pct']:.2f}%")
print(f"Sharpe Ratio: {results['sharpe_ratio']:.2f}")
```

### Command Line Usage

```bash
# Basic usage
python main.py --symbol AAPL --strategy RSI

# With custom parameters
python main.py --symbol MSFT --strategy MACD \
    --start-date 2023-01-01 --end-date 2024-01-01 \
    --capital 50000 --commission 0.002

# Show plots
python main.py --symbol TSLA --strategy MA --plot

# Save plots
python main.py --symbol GOOGL --strategy BB --save-plots ./results
```

### Interactive Dashboard

```bash
streamlit run dashboard.py
```

## Core Concepts

### Data Structure

All market data uses pandas DataFrame with OHLCV columns:
- `Open`: Opening price
- `High`: Highest price
- `Low`: Lowest price
- `Close`: Closing price
- `Volume`: Trading volume

Index should be datetime for proper time series handling.

### Trading Signals

Strategies generate signals:
- `1`: Buy signal
- `-1`: Sell signal
- `0`: Hold/No action

### Portfolio Management

The Portfolio class tracks:
- Cash balance
- Current position (shares held)
- Trade history
- Portfolio value over time

## Strategies

### RSI Strategy

Relative Strength Index mean reversion strategy.

```python
strategy = RSIStrategy(
    rsi_period=14,      # RSI calculation period
    oversold=30,        # Buy threshold
    overbought=70       # Sell threshold
)
```

**Logic:**
- Buy when RSI < oversold
- Sell when RSI > overbought

### MACD Strategy

Moving Average Convergence Divergence momentum strategy.

```python
strategy = MACDStrategy(
    fast_period=12,     # Fast EMA period
    slow_period=26,     # Slow EMA period
    signal_period=9     # Signal line period
)
```

**Logic:**
- Buy when MACD crosses above signal line
- Sell when MACD crosses below signal line

### MA Crossover Strategy

Classic moving average crossover.

```python
strategy = MACrossoverStrategy(
    short_window=50,    # Short MA period
    long_window=200,    # Long MA period
    ma_type='SMA'       # 'SMA' or 'EMA'
)
```

**Logic:**
- Buy on golden cross (short MA > long MA)
- Sell on death cross (short MA < long MA)

### Bollinger Bands Strategy

Volatility-based mean reversion.

```python
strategy = BollingerBandsStrategy(
    period=20,          # Moving average period
    std_dev=2.0         # Standard deviation multiplier
)
```

**Logic:**
- Buy when price touches lower band
- Sell when price touches upper band

### Mean Reversion Strategy

Statistical arbitrage using z-scores.

```python
strategy = MeanReversionStrategy(
    lookback_period=20,  # Period for mean/std calculation
    z_entry=2.0,         # Entry z-score threshold
    z_exit=0.5           # Exit z-score threshold
)
```

**Logic:**
- Buy when z-score < -z_entry
- Sell when z-score > z_entry
- Exit when z-score approaches 0

## Backtesting

### BacktestEngine

The main backtesting engine.

```python
engine = BacktestEngine(
    initial_capital=100000,  # Starting capital
    commission=0.001,        # Commission rate (0.1%)
    position_size=0.95       # % of capital per trade
)

results = engine.run(data, strategy, verbose=True)
```

### Results Dictionary

The backtest returns comprehensive metrics:

```python
{
    'initial_capital': 100000,
    'final_value': 115000,
    'total_return': 0.15,
    'total_return_pct': 15.0,
    'buy_hold_return': 0.12,
    'excess_return': 0.03,
    'sharpe_ratio': 1.5,
    'max_drawdown': -0.08,
    'volatility': 0.2,
    'num_trades': 45,
    'win_rate': 0.62,
    'avg_trade_return': 0.003
}
```

## Performance Metrics

### Risk-Adjusted Returns

**Sharpe Ratio**: Return per unit of risk
```python
sharpe = (returns.mean() - risk_free_rate) / returns.std()
```

**Sortino Ratio**: Like Sharpe but only considers downside risk
```python
sortino = excess_returns.mean() / downside_std
```

**Calmar Ratio**: Return over maximum drawdown
```python
calmar = annual_return / abs(max_drawdown)
```

### Risk Metrics

**Maximum Drawdown**: Largest peak-to-trough decline
**Value at Risk (VaR)**: Potential loss at confidence level
**Conditional VaR (CVaR)**: Expected loss beyond VaR

### Trade Metrics

**Win Rate**: Percentage of profitable trades
**Profit Factor**: Gross profit / Gross loss
**Average Trade Return**: Mean return per trade

## Visualization

### Basic Plots

```python
from src.visualization.plotter import Plotter

plotter = Plotter()

# Price and signals
fig1 = plotter.plot_price_and_signals(data_with_signals)

# Portfolio value
fig2 = plotter.plot_portfolio_value(portfolio_history, initial_capital)

# Returns distribution
fig3 = plotter.plot_returns_distribution(returns)

# Drawdown
fig4 = plotter.plot_drawdown(portfolio_history)
```

### Comprehensive Dashboard

```python
fig = plotter.create_dashboard(
    data_with_signals,
    portfolio_history,
    returns,
    initial_capital,
    results,
    save_path='dashboard.png'
)
```

### Strategy Comparison

```python
results_dict = {
    'RSI': rsi_portfolio_history,
    'MACD': macd_portfolio_history,
    'MA': ma_portfolio_history
}

fig = plotter.plot_strategy_comparison(results_dict)
```

## API Reference

### DataLoader

```python
class DataLoader:
    def fetch_data(symbol, start_date, end_date, interval='1d')
    def fetch_multiple_symbols(symbols, start_date, end_date)
    def get_latest_data(symbol, days=365)
    def load_from_csv(filepath)
    def save_to_csv(data, filepath)
```

### BaseStrategy

```python
class BaseStrategy:
    def generate_signals(data) -> DataFrame
    def calculate_indicators(data) -> DataFrame
    def validate_data(data) -> bool
    def get_strategy_info() -> Dict
```

### Portfolio

```python
class Portfolio:
    def buy(price, timestamp) -> Trade
    def sell(price, timestamp) -> Trade
    def update_value(current_price, timestamp)
    def get_total_value(current_price) -> float
    def get_returns() -> Series
    def get_trade_history() -> DataFrame
```

## Advanced Usage

### Custom Strategy

Create your own strategy by extending BaseStrategy:

```python
from src.strategies.base_strategy import BaseStrategy

class MyCustomStrategy(BaseStrategy):
    def __init__(self, param1, param2):
        super().__init__(name='My Custom Strategy')
        self.param1 = param1
        self.param2 = param2
    
    def calculate_indicators(self, data):
        # Add your indicators
        data['my_indicator'] = ...
        return data
    
    def generate_signals(self, data):
        if not self.validate_data(data):
            raise ValueError("Invalid data")
        
        data = self.calculate_indicators(data)
        data['signal'] = 0
        
        # Your signal logic
        data.loc[condition1, 'signal'] = 1   # Buy
        data.loc[condition2, 'signal'] = -1  # Sell
        
        return data
```

### Parameter Optimization

```python
import itertools

# Define parameter grid
rsi_periods = [10, 14, 20]
oversold_levels = [20, 25, 30]
overbought_levels = [70, 75, 80]

best_sharpe = -np.inf
best_params = None

# Grid search
for rsi, oversold, overbought in itertools.product(
    rsi_periods, oversold_levels, overbought_levels
):
    strategy = RSIStrategy(rsi, oversold, overbought)
    engine = BacktestEngine(initial_capital=100000)
    results = engine.run(data, strategy, verbose=False)
    
    if results['sharpe_ratio'] > best_sharpe:
        best_sharpe = results['sharpe_ratio']
        best_params = (rsi, oversold, overbought)

print(f"Best parameters: {best_params}")
print(f"Best Sharpe: {best_sharpe:.2f}")
```

### Walk-Forward Analysis

```python
from datetime import datetime, timedelta

def walk_forward_backtest(data, strategy, train_days=180, test_days=30):
    results = []
    start = data.index[0]
    end = data.index[-1]
    
    current = start
    while current + timedelta(days=train_days + test_days) < end:
        # Training period
        train_end = current + timedelta(days=train_days)
        train_data = data[current:train_end]
        
        # Test period
        test_start = train_end
        test_end = test_start + timedelta(days=test_days)
        test_data = data[test_start:test_end]
        
        # Run backtest on test period
        engine = BacktestEngine(initial_capital=100000)
        result = engine.run(test_data, strategy, verbose=False)
        results.append(result)
        
        current = test_start
    
    return results
```

## Tips and Best Practices

1. **Always validate your data** before running backtests
2. **Use realistic commission rates** (typically 0.1% - 0.3%)
3. **Consider slippage** in real trading
4. **Avoid overfitting** - test on out-of-sample data
5. **Use proper position sizing** - don't risk too much per trade
6. **Account for transaction costs** in your metrics
7. **Test across multiple time periods** and market conditions
8. **Compare to buy-and-hold** benchmark
9. **Monitor maximum drawdown** for risk management
10. **Keep strategies simple** - complex doesn't mean better

## Troubleshooting

### Common Issues

**"No data found for symbol"**
- Check if ticker symbol is correct
- Verify internet connection
- Try different date range

**"Invalid data format"**
- Ensure data has required OHLCV columns
- Check for missing values
- Validate datetime index

**"Not enough data for indicators"**
- Some indicators need minimum periods
- Extend date range or reduce indicator periods

**Memory issues with large datasets**
- Process data in chunks
- Use smaller date ranges
- Reduce data frequency

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License - see [LICENSE](LICENSE) file.

---

**Author:** Yacine Abdi | 2026

For questions or issues, please open an issue on GitHub.
