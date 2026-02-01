"""
Interactive Dashboard for Algorithmic Trading Simulator
Author: Yacine Abdi

Run with: streamlit run dashboard.py
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

from src.data.data_loader import DataLoader
from src.strategies import (
    RSIStrategy, MACDStrategy, MACrossoverStrategy,
    BollingerBandsStrategy, MeanReversionStrategy
)
from src.backtester.engine import BacktestEngine
from src.visualization.plotter import Plotter


# Page configuration
st.set_page_config(
    page_title="Algorithmic Trading Simulator",
    page_icon="📈",
    layout="wide"
)

# Title and description
st.title("📈 Algorithmic Trading Simulator")
st.markdown("**Author:** Yacine Abdi")
st.markdown("---")

# Sidebar for inputs
st.sidebar.header("Configuration")

# Stock selection
symbol = st.sidebar.text_input("Stock Symbol", value="AAPL").upper()

# Date range
col1, col2 = st.sidebar.columns(2)
with col1:
    start_date = st.date_input(
        "Start Date",
        value=datetime.now() - timedelta(days=365)
    )
with col2:
    end_date = st.date_input(
        "End Date",
        value=datetime.now()
    )

# Strategy selection
strategy_choice = st.sidebar.selectbox(
    "Trading Strategy",
    ["RSI Strategy", "MACD Strategy", "MA Crossover", 
     "Bollinger Bands", "Mean Reversion"]
)

# Strategy parameters based on selection
st.sidebar.subheader("Strategy Parameters")

if strategy_choice == "RSI Strategy":
    rsi_period = st.sidebar.slider("RSI Period", 5, 30, 14)
    oversold = st.sidebar.slider("Oversold Threshold", 20, 40, 30)
    overbought = st.sidebar.slider("Overbought Threshold", 60, 80, 70)
    strategy = RSIStrategy(rsi_period=rsi_period, oversold=oversold, overbought=overbought)
    
elif strategy_choice == "MACD Strategy":
    fast_period = st.sidebar.slider("Fast Period", 5, 20, 12)
    slow_period = st.sidebar.slider("Slow Period", 20, 40, 26)
    signal_period = st.sidebar.slider("Signal Period", 5, 15, 9)
    strategy = MACDStrategy(fast_period=fast_period, slow_period=slow_period, signal_period=signal_period)
    
elif strategy_choice == "MA Crossover":
    short_window = st.sidebar.slider("Short MA Period", 10, 100, 50)
    long_window = st.sidebar.slider("Long MA Period", 100, 300, 200)
    ma_type = st.sidebar.radio("MA Type", ["SMA", "EMA"])
    strategy = MACrossoverStrategy(short_window=short_window, long_window=long_window, ma_type=ma_type)
    
elif strategy_choice == "Bollinger Bands":
    bb_period = st.sidebar.slider("Period", 10, 30, 20)
    std_dev = st.sidebar.slider("Std Dev Multiplier", 1.0, 3.0, 2.0, 0.1)
    strategy = BollingerBandsStrategy(period=bb_period, std_dev=std_dev)
    
else:  # Mean Reversion
    lookback = st.sidebar.slider("Lookback Period", 10, 50, 20)
    z_entry = st.sidebar.slider("Z-Score Entry", 1.0, 3.0, 2.0, 0.1)
    z_exit = st.sidebar.slider("Z-Score Exit", 0.1, 1.0, 0.5, 0.1)
    strategy = MeanReversionStrategy(lookback_period=lookback, z_entry=z_entry, z_exit=z_exit)

# Backtest parameters
st.sidebar.subheader("Backtest Settings")
initial_capital = st.sidebar.number_input(
    "Initial Capital ($)", 
    min_value=1000, 
    max_value=1000000, 
    value=100000, 
    step=1000
)
commission = st.sidebar.number_input(
    "Commission Rate (%)", 
    min_value=0.0, 
    max_value=1.0, 
    value=0.1, 
    step=0.01
) / 100

# Run backtest button
run_button = st.sidebar.button("🚀 Run Backtest", type="primary")

# Main content area
if run_button:
    try:
        with st.spinner(f"Fetching data for {symbol}..."):
            # Load data
            data_loader = DataLoader()
            data = data_loader.fetch_data(
                symbol, 
                start_date.strftime('%Y-%m-%d'),
                end_date.strftime('%Y-%m-%d')
            )
        
        st.success(f"✅ Loaded {len(data)} bars of data")
        
        with st.spinner("Running backtest..."):
            # Run backtest
            engine = BacktestEngine(
                initial_capital=initial_capital,
                commission=commission
            )
            results = engine.run(data, strategy, verbose=False)
        
        st.success("✅ Backtest complete!")
        
        # Display results
        st.header("📊 Performance Summary")
        
        # Metrics in columns
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Total Return",
                f"{results['total_return_pct']:.2f}%",
                delta=f"{results['total_return_pct']:.2f}%"
            )
        
        with col2:
            st.metric(
                "Sharpe Ratio",
                f"{results['sharpe_ratio']:.2f}"
            )
        
        with col3:
            st.metric(
                "Max Drawdown",
                f"{results['max_drawdown']*100:.2f}%"
            )
        
        with col4:
            st.metric(
                "Win Rate",
                f"{results['win_rate']*100:.2f}%"
            )
        
        # Additional metrics
        col5, col6, col7, col8 = st.columns(4)
        
        with col5:
            st.metric("Final Value", f"${results['final_value']:,.2f}")
        
        with col6:
            st.metric("# of Trades", f"{results['num_trades']}")
        
        with col7:
            st.metric("Buy & Hold", f"{results['buy_hold_return_pct']:.2f}%")
        
        with col8:
            st.metric("Excess Return", f"{results['excess_return']*100:.2f}%")
        
        st.markdown("---")
        
        # Generate visualizations
        data_with_signals = strategy.generate_signals(data.copy())
        portfolio_history = engine.get_portfolio_history()
        returns = engine.portfolio.get_returns()
        plotter = Plotter()
        
        # Price and signals chart
        st.subheader("📈 Price and Trading Signals")
        fig1 = plotter.plot_price_and_signals(
            data_with_signals,
            title=f"{symbol} - {strategy.name}"
        )
        st.pyplot(fig1)
        plt.close()
        
        # Portfolio value chart
        st.subheader("💰 Portfolio Value Over Time")
        fig2 = plotter.plot_portfolio_value(
            portfolio_history,
            initial_capital,
            title="Portfolio Growth"
        )
        st.pyplot(fig2)
        plt.close()
        
        # Two column layout for additional charts
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.subheader("📊 Returns Distribution")
            fig3 = plotter.plot_returns_distribution(returns)
            st.pyplot(fig3)
            plt.close()
        
        with col_right:
            st.subheader("📉 Drawdown Analysis")
            fig4 = plotter.plot_drawdown(portfolio_history)
            st.pyplot(fig4)
            plt.close()
        
        # Trade history
        st.subheader("📋 Trade History")
        trade_history = results['trade_history']
        if len(trade_history) > 0:
            st.dataframe(trade_history, use_container_width=True)
        else:
            st.info("No trades executed during this period")
        
        # Download results
        st.markdown("---")
        st.subheader("💾 Export Results")
        
        # Create CSV download
        csv = trade_history.to_csv(index=False)
        st.download_button(
            label="Download Trade History (CSV)",
            data=csv,
            file_name=f"{symbol}_{strategy.name}_trades.csv",
            mime="text/csv"
        )
        
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        import traceback
        st.code(traceback.format_exc())

else:
    # Welcome message
    st.info("""
    👋 Welcome to the Algorithmic Trading Simulator!
    
    **How to use:**
    1. Enter a stock symbol (e.g., AAPL, MSFT, TSLA)
    2. Select a date range for backtesting
    3. Choose a trading strategy and adjust parameters
    4. Set your initial capital and commission rate
    5. Click 'Run Backtest' to see results
    
    **Available Strategies:**
    - **RSI Strategy**: Mean reversion based on Relative Strength Index
    - **MACD Strategy**: Momentum strategy using MACD crossovers
    - **MA Crossover**: Classic moving average crossover (Golden/Death Cross)
    - **Bollinger Bands**: Volatility-based mean reversion
    - **Mean Reversion**: Statistical arbitrage using z-scores
    """)
    
    # Show example
    st.markdown("---")
    st.subheader("📚 Quick Start Example")
    st.code("""
# Try these settings for a quick demo:
Symbol: AAPL
Date Range: Last 365 days
Strategy: RSI Strategy
Initial Capital: $100,000
    """)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
        <p>Created by Yacine Abdi | 2026</p>
        <p><i>This is an educational project. Not financial advice.</i></p>
    </div>
    """,
    unsafe_allow_html=True
)
