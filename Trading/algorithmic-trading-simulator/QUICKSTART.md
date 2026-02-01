# Quick Start Guide

**Algorithmic Trading Simulator**  
Author: Yacine Abdi

## Installation (1 minute)

```bash
cd algorithmic-trading-simulator
pip install -r requirements.txt
```

## Run Your First Backtest (2 minutes)

```bash
# Simple command
python main.py --symbol AAPL --strategy RSI

# With visualization
python main.py --symbol AAPL --strategy RSI --plot
```

## Launch Interactive Dashboard (1 minute)

```bash
streamlit run dashboard.py
```

Then:
1. Enter a stock symbol (e.g., AAPL, TSLA, MSFT)
2. Choose date range
3. Select strategy and adjust parameters
4. Click "Run Backtest"

## Example Code (3 minutes)

Create a file `my_backtest.py`:

```python
from src.data.data_loader import DataLoader
from src.strategies import RSIStrategy
from src.backtester.engine import BacktestEngine

# Load data
loader = DataLoader()
data = loader.fetch_data('AAPL', '2023-01-01', '2024-01-01')

# Create strategy
strategy = RSIStrategy(rsi_period=14, oversold=30, overbought=70)

# Run backtest
engine = BacktestEngine(initial_capital=100000)
results = engine.run(data, strategy)

# Print results
print(f"Total Return: {results['total_return_pct']:.2f}%")
print(f"Sharpe Ratio: {results['sharpe_ratio']:.2f}")
print(f"Max Drawdown: {results['max_drawdown']*100:.2f}%")
print(f"Win Rate: {results['win_rate']*100:.2f}%")
```

Run it:
```bash
python my_backtest.py
```

## Available Strategies

| Strategy | Code | Best For |
|----------|------|----------|
| RSI | `RSIStrategy()` | Mean reversion, oversold/overbought |
| MACD | `MACDStrategy()` | Momentum, trend following |
| MA Crossover | `MACrossoverStrategy()` | Classic trend following |
| Bollinger Bands | `BollingerBandsStrategy()` | Volatility breakouts |
| Mean Reversion | `MeanReversionStrategy()` | Statistical arbitrage |

## Command Line Options

```bash
python main.py \
    --symbol TSLA \              # Stock ticker
    --strategy MACD \            # Strategy choice
    --start-date 2023-01-01 \   # Start date
    --end-date 2024-01-01 \     # End date
    --capital 50000 \           # Initial capital
    --commission 0.002 \        # Commission rate
    --plot                      # Show plots
```

## What's Next?

1. Try different strategies on the same stock
2. Test the same strategy on different stocks
3. Optimize parameters for better performance
4. Read [DOCUMENTATION.md](DOCUMENTATION.md) for advanced usage
5. Check [examples/](examples/) for more complex scenarios

## Common Issues

**"Module not found"**
```bash
pip install -r requirements.txt
```

**"No data found"**
- Check internet connection
- Verify ticker symbol is correct
- Try different date range

**Plots not showing**
```bash
pip install matplotlib
```

## Get Help

- Read [DOCUMENTATION.md](DOCUMENTATION.md)
- Check [examples/example_usage.py](examples/example_usage.py)
- Open an issue on GitHub

---

**Ready to start?** Run your first backtest now! 🚀
