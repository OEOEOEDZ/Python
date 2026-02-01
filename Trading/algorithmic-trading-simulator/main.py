"""
Main Script for Algorithmic Trading Simulator
Author: Yacine Abdi

Run backtests with different strategies and parameters.
"""

import argparse
import sys
from datetime import datetime, timedelta

from src.data.data_loader import DataLoader
from src.strategies import (
    RSIStrategy, MACDStrategy, MACrossoverStrategy,
    BollingerBandsStrategy, MeanReversionStrategy
)
from src.backtester.engine import BacktestEngine
from src.visualization.plotter import Plotter


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Algorithmic Trading Simulator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --symbol AAPL --strategy RSI
  python main.py --symbol MSFT --strategy MACD --start-date 2023-01-01 --end-date 2024-01-01
  python main.py --symbol TSLA --strategy MA --capital 50000
        """
    )
    
    parser.add_argument('--symbol', type=str, default='AAPL',
                       help='Stock ticker symbol (default: AAPL)')
    parser.add_argument('--strategy', type=str, default='RSI',
                       choices=['RSI', 'MACD', 'MA', 'BB', 'MR'],
                       help='Trading strategy (default: RSI)')
    parser.add_argument('--start-date', type=str, default=None,
                       help='Start date (YYYY-MM-DD, default: 1 year ago)')
    parser.add_argument('--end-date', type=str, default=None,
                       help='End date (YYYY-MM-DD, default: today)')
    parser.add_argument('--capital', type=float, default=100000,
                       help='Initial capital (default: 100000)')
    parser.add_argument('--commission', type=float, default=0.001,
                       help='Commission rate (default: 0.001)')
    parser.add_argument('--plot', action='store_true',
                       help='Show plots')
    parser.add_argument('--save-plots', type=str, default=None,
                       help='Save plots to directory')
    
    return parser.parse_args()


def get_strategy(strategy_name: str):
    """
    Get strategy instance based on name.
    
    Args:
        strategy_name (str): Strategy name
        
    Returns:
        BaseStrategy: Strategy instance
    """
    strategies = {
        'RSI': RSIStrategy(rsi_period=14, oversold=30, overbought=70),
        'MACD': MACDStrategy(fast_period=12, slow_period=26, signal_period=9),
        'MA': MACrossoverStrategy(short_window=50, long_window=200, ma_type='SMA'),
        'BB': BollingerBandsStrategy(period=20, std_dev=2.0),
        'MR': MeanReversionStrategy(lookback_period=20, z_entry=2.0, z_exit=0.5)
    }
    
    return strategies.get(strategy_name)


def main():
    """Main function."""
    args = parse_arguments()
    
    # Set default dates if not provided
    if args.end_date is None:
        end_date = datetime.now().strftime('%Y-%m-%d')
    else:
        end_date = args.end_date
    
    if args.start_date is None:
        start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
    else:
        start_date = args.start_date
    
    print("="*70)
    print("ALGORITHMIC TRADING SIMULATOR")
    print("Author: Yacine Abdi")
    print("="*70)
    
    try:
        # Load data
        print(f"\nFetching data for {args.symbol}...")
        data_loader = DataLoader()
        data = data_loader.fetch_data(args.symbol, start_date, end_date)
        
        # Initialize strategy
        strategy = get_strategy(args.strategy)
        if strategy is None:
            print(f"Error: Unknown strategy '{args.strategy}'")
            sys.exit(1)
        
        print(f"\nUsing strategy: {strategy.name}")
        print(f"Parameters: {strategy.get_strategy_info()}")
        
        # Run backtest
        engine = BacktestEngine(
            initial_capital=args.capital,
            commission=args.commission
        )
        
        results = engine.run(data, strategy, verbose=True)
        
        # Visualizations
        if args.plot or args.save_plots:
            print("\nGenerating visualizations...")
            plotter = Plotter()
            
            # Generate signals for plotting
            data_with_signals = strategy.generate_signals(data.copy())
            portfolio_history = engine.get_portfolio_history()
            returns = engine.portfolio.get_returns()
            
            # Create dashboard
            fig = plotter.create_dashboard(
                data_with_signals,
                portfolio_history,
                returns,
                args.capital,
                results,
                save_path=f"{args.save_plots}/dashboard.png" if args.save_plots else None
            )
            
            if args.plot:
                import matplotlib.pyplot as plt
                plt.show()
        
        print("\n" + "="*70)
        print("Backtest completed successfully!")
        print("="*70)
        
    except Exception as e:
        print(f"\nError: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
