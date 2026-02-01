# Algorithmic Trading Simulator

A sophisticated Python-based algorithmic trading simulator with backtesting capabilities, multiple trading strategies, and real-time visualization dashboard.

**Author:** Yacine Abdi

## 🎯 Features

- **Multiple Trading Strategies**: RSI, MACD, Moving Average Crossover, Bollinger Bands, and Mean Reversion
- **Backtesting Engine**: Test strategies on historical data with detailed performance metrics
- **Real-time Visualization**: Interactive dashboard showing trades, portfolio value, and strategy performance
- **Risk Management**: Position sizing, stop-loss, and take-profit mechanisms
- **Performance Analytics**: Sharpe ratio, maximum drawdown, win rate, and more
- **Historical Data Integration**: Fetch real market data using yfinance
- **Customizable Parameters**: Fine-tune strategy parameters for optimization

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/algorithmic-trading-simulator.git
cd algorithmic-trading-simulator

# Install dependencies
pip install -r requirements.txt
```

### Run the Simulator

```bash
# Run with default strategy (RSI)
python main.py

# Run with specific strategy
python main.py --strategy MACD --symbol AAPL --start-date 2023-01-01 --end-date 2024-01-01

# Launch interactive dashboard
python dashboard.py
```

## 📊 Available Strategies

1. **RSI Strategy**: Relative Strength Index-based mean reversion
2. **MACD Strategy**: Moving Average Convergence Divergence momentum strategy
3. **MA Crossover**: Simple and Exponential Moving Average crossover
4. **Bollinger Bands**: Volatility-based trading strategy
5. **Mean Reversion**: Statistical arbitrage based on price deviations

## 🏗️ Project Structure

```
algorithmic-trading-simulator/
│
├── src/
│   ├── strategies/          # Trading strategy implementations
│   │   ├── base_strategy.py
│   │   ├── rsi_strategy.py
│   │   ├── macd_strategy.py
│   │   ├── ma_crossover.py
│   │   ├── bollinger_bands.py
│   │   └── mean_reversion.py
│   │
│   ├── backtester/          # Backtesting engine
│   │   ├── engine.py
│   │   └── portfolio.py
│   │
│   ├── data/                # Data fetching and processing
│   │   └── data_loader.py
│   │
│   ├── analytics/           # Performance metrics
│   │   └── metrics.py
│   │
│   └── visualization/       # Plotting and dashboard
│       └── plotter.py
│
├── tests/                   # Unit tests
├── examples/                # Example usage scripts
├── requirements.txt
├── main.py
├── dashboard.py
└── README.md
```

## 💡 Example Usage

```python
from src.strategies.rsi_strategy import RSIStrategy
from src.backtester.engine import BacktestEngine
from src.data.data_loader import DataLoader

# Load historical data
data_loader = DataLoader()
data = data_loader.fetch_data('AAPL', '2023-01-01', '2024-01-01')

# Initialize strategy
strategy = RSIStrategy(
    rsi_period=14,
    oversold=30,
    overbought=70
)

# Run backtest
engine = BacktestEngine(initial_capital=100000)
results = engine.run(data, strategy)

# Print performance metrics
print(f"Total Return: {results['total_return']:.2%}")
print(f"Sharpe Ratio: {results['sharpe_ratio']:.2f}")
print(f"Max Drawdown: {results['max_drawdown']:.2%}")
```

## 📈 Performance Metrics

The simulator calculates comprehensive performance metrics:

- **Total Return**: Overall profit/loss percentage
- **Sharpe Ratio**: Risk-adjusted return measure
- **Maximum Drawdown**: Largest peak-to-trough decline
- **Win Rate**: Percentage of profitable trades
- **Profit Factor**: Gross profit / Gross loss
- **Average Trade Duration**: Mean holding period
- **Volatility**: Standard deviation of returns

## 🛠️ Technologies Used

- **Python 3.8+**: Core programming language
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computations
- **yfinance**: Historical market data
- **matplotlib/plotly**: Data visualization
- **streamlit**: Interactive dashboard (optional)
- **pytest**: Testing framework

## 🎓 Learning Outcomes

This project demonstrates:

- Object-oriented programming and design patterns
- Financial markets and trading concepts
- Data analysis and statistical methods
- Algorithm optimization and backtesting
- Software architecture and modularity
- Performance measurement and analytics

## 🔮 Future Enhancements

- [ ] Machine learning-based strategies
- [ ] Multi-asset portfolio optimization
- [ ] Live trading integration (paper trading)
- [ ] Advanced order types (limit, stop-limit)
- [ ] Walk-forward analysis
- [ ] Monte Carlo simulation for risk assessment
- [ ] Strategy parameter optimization (genetic algorithms)

## 📝 License

MIT License - feel free to use this project for learning and development.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## ⚠️ Disclaimer

This is an educational project for learning algorithmic trading concepts. It should not be used for actual trading without thorough testing and understanding of the risks involved. Past performance does not guarantee future results.

---

**Created by Yacine Abdi** | 2026
