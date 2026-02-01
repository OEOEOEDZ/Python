# Examples Directory

This directory contains example scripts demonstrating various features of the Algorithmic Trading Simulator.

**Author:** Yacine Abdi

## Available Examples

### example_usage.py

Comprehensive examples covering:

1. **Basic Backtest**: Simple RSI strategy backtest
2. **Strategy Comparison**: Compare multiple strategies
3. **Custom Parameters**: Using custom strategy parameters
4. **Multiple Stocks**: Analyze multiple symbols
5. **Full Dashboard**: Create comprehensive visualizations

## Running Examples

### Run All Examples
```bash
cd examples
python example_usage.py
# Choose option 6 to run all examples
```

### Run Specific Example
```bash
python example_usage.py
# Enter 1-5 to run specific example
```

### Run from Command Line
```bash
# Direct execution
python -c "from example_usage import example_basic_backtest; example_basic_backtest()"
```

## Example Outputs

Each example will:
- Print performance metrics to console
- Display plots (if matplotlib is available)
- Save some results to files

## Creating Your Own Examples

Feel free to create your own examples by following this template:

```python
"""
My Custom Example
Author: Your Name
"""

from src.data.data_loader import DataLoader
from src.strategies import RSIStrategy
from src.backtester.engine import BacktestEngine

def my_custom_example():
    """Description of what this example does."""
    
    # Your code here
    loader = DataLoader()
    data = loader.fetch_data('AAPL', '2023-01-01', '2024-01-01')
    
    strategy = RSIStrategy()
    engine = BacktestEngine(initial_capital=100000)
    results = engine.run(data, strategy)
    
    print(f"Results: {results}")

if __name__ == '__main__':
    my_custom_example()
```

## Tips

- Start with example 1 to understand the basics
- Example 2 is good for comparing strategies
- Example 4 shows how to analyze multiple stocks
- Example 5 demonstrates all visualization features

## Requirements

All examples require the packages listed in `requirements.txt`. Make sure to install them:

```bash
pip install -r ../requirements.txt
```

## Need Help?

- Check the main [README.md](../README.md)
- Read [DOCUMENTATION.md](../DOCUMENTATION.md)
- Open an issue on GitHub

---

**Happy Trading!** 📈
