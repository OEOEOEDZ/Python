"""
Example Usage Script
Author: Yacine Abdi

Demonstrates how to use the Algorithmic Trading Simulator.
"""

from src.data.data_loader import DataLoader
from src.strategies import RSIStrategy, MACDStrategy
from src.backtester.engine import BacktestEngine
from src.visualization.plotter import Plotter
import matplotlib.pyplot as plt


def example_basic_backtest():
    """Basic backtest example with RSI strategy."""
    print("="*60)
    print("EXAMPLE 1: Basic Backtest with RSI Strategy")
    print("="*60)
    
    # Load data
    data_loader = DataLoader()
    data = data_loader.fetch_data('AAPL', '2023-01-01', '2024-01-01')
    
    # Initialize strategy
    strategy = RSIStrategy(rsi_period=14, oversold=30, overbought=70)
    
    # Run backtest
    engine = BacktestEngine(initial_capital=100000)
    results = engine.run(data, strategy, verbose=True)
    
    # Plot results
    plotter = Plotter()
    data_with_signals = strategy.generate_signals(data.copy())
    portfolio_history = engine.get_portfolio_history()
    
    fig1 = plotter.plot_price_and_signals(data_with_signals)
    fig2 = plotter.plot_portfolio_value(portfolio_history, 100000)
    
    plt.show()


def example_strategy_comparison():
    """Compare multiple strategies on the same stock."""
    print("\n" + "="*60)
    print("EXAMPLE 2: Strategy Comparison")
    print("="*60)
    
    # Load data
    data_loader = DataLoader()
    data = data_loader.fetch_data('MSFT', '2023-01-01', '2024-01-01')
    
    # Test multiple strategies
    strategies = {
        'RSI': RSIStrategy(),
        'MACD': MACDStrategy()
    }
    
    results_dict = {}
    
    for name, strategy in strategies.items():
        print(f"\nTesting {name}...")
        engine = BacktestEngine(initial_capital=100000)
        results = engine.run(data, strategy, verbose=False)
        results_dict[name] = engine.get_portfolio_history()
        
        print(f"{name} Total Return: {results['total_return_pct']:.2f}%")
        print(f"{name} Sharpe Ratio: {results['sharpe_ratio']:.2f}")
    
    # Plot comparison
    plotter = Plotter()
    fig = plotter.plot_strategy_comparison(results_dict)
    plt.show()


def example_custom_parameters():
    """Example with custom strategy parameters."""
    print("\n" + "="*60)
    print("EXAMPLE 3: Custom Strategy Parameters")
    print("="*60)
    
    # Load data
    data_loader = DataLoader()
    data = data_loader.fetch_data('TSLA', '2023-01-01', '2024-01-01')
    
    # Create strategy with custom parameters
    strategy = RSIStrategy(
        rsi_period=10,  # Shorter period for more signals
        oversold=25,     # More aggressive entry
        overbought=75    # More aggressive exit
    )
    
    # Run backtest with custom settings
    engine = BacktestEngine(
        initial_capital=50000,
        commission=0.002,  # 0.2% commission
        position_size=0.8   # Use 80% of capital per trade
    )
    
    results = engine.run(data, strategy, verbose=True)


def example_multiple_stocks():
    """Backtest same strategy on multiple stocks."""
    print("\n" + "="*60)
    print("EXAMPLE 4: Multiple Stock Analysis")
    print("="*60)
    
    symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN']
    strategy = RSIStrategy()
    
    data_loader = DataLoader()
    
    results_summary = []
    
    for symbol in symbols:
        try:
            print(f"\nAnalyzing {symbol}...")
            data = data_loader.fetch_data(symbol, '2023-01-01', '2024-01-01')
            
            engine = BacktestEngine(initial_capital=100000)
            results = engine.run(data, strategy, verbose=False)
            
            results_summary.append({
                'Symbol': symbol,
                'Return': f"{results['total_return_pct']:.2f}%",
                'Sharpe': f"{results['sharpe_ratio']:.2f}",
                'Max DD': f"{results['max_drawdown']*100:.2f}%",
                'Trades': results['num_trades']
            })
            
        except Exception as e:
            print(f"Error with {symbol}: {e}")
    
    # Print summary
    print("\n" + "="*60)
    print("RESULTS SUMMARY")
    print("="*60)
    for result in results_summary:
        print(f"\n{result['Symbol']}:")
        print(f"  Return: {result['Return']}")
        print(f"  Sharpe: {result['Sharpe']}")
        print(f"  Max Drawdown: {result['Max DD']}")
        print(f"  Trades: {result['Trades']}")


def example_full_dashboard():
    """Create comprehensive dashboard."""
    print("\n" + "="*60)
    print("EXAMPLE 5: Full Dashboard")
    print("="*60)
    
    # Load data
    data_loader = DataLoader()
    data = data_loader.fetch_data('AAPL', '2023-01-01', '2024-01-01')
    
    # Run backtest
    strategy = RSIStrategy()
    engine = BacktestEngine(initial_capital=100000)
    results = engine.run(data, strategy, verbose=True)
    
    # Create dashboard
    plotter = Plotter()
    data_with_signals = strategy.generate_signals(data.copy())
    portfolio_history = engine.get_portfolio_history()
    returns = engine.portfolio.get_returns()
    
    fig = plotter.create_dashboard(
        data_with_signals,
        portfolio_history,
        returns,
        100000,
        results,
        save_path='dashboard_example.png'
    )
    
    plt.show()


if __name__ == '__main__':
    # Run examples
    print("Algorithmic Trading Simulator - Examples")
    print("Author: Yacine Abdi\n")
    
    # Choose which example to run
    print("Available examples:")
    print("1. Basic Backtest")
    print("2. Strategy Comparison")
    print("3. Custom Parameters")
    print("4. Multiple Stocks")
    print("5. Full Dashboard")
    print("6. Run All")
    
    choice = input("\nEnter example number (1-6): ")
    
    if choice == '1':
        example_basic_backtest()
    elif choice == '2':
        example_strategy_comparison()
    elif choice == '3':
        example_custom_parameters()
    elif choice == '4':
        example_multiple_stocks()
    elif choice == '5':
        example_full_dashboard()
    elif choice == '6':
        example_basic_backtest()
        example_strategy_comparison()
        example_custom_parameters()
        example_multiple_stocks()
        example_full_dashboard()
    else:
        print("Invalid choice. Running basic example...")
        example_basic_backtest()
