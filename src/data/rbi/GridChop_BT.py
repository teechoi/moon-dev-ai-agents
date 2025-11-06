"""
🌙 Moon Dev's Grid Trading Strategy - Backtest Version
Trades a grid range during choppy/sideways market conditions
Built with love by Moon Dev 🚀
"""

import pandas as pd
import pandas_ta as ta
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
import numpy as np

class GridChopStrategy(Strategy):
    # ====== CONFIGURABLE PARAMETERS ======
    grid_levels = 5           # Number of grid levels (buy/sell zones) 📊
    grid_spacing_pct = 1.5    # % spacing between grid levels (1.5 = 1.5%) 📏
    profit_per_grid = 1.0     # % profit target per grid trade (1.0 = 1%) 🎯
    risk_pct = 0.02          # Risk 2% of equity per trade 🛡️

    # Chop detection thresholds
    chop_threshold = 61.8     # CI > 61.8 = choppy market 🌊
    adx_threshold = 25        # ADX < 25 = weak trend 📉

    def init(self):
        """Initialize indicators for chop detection and grid setup"""
        print("🌙 Moon Dev's Grid Trading Strategy Initializing...")

        # ====== CHOP DETECTION INDICATORS ======
        # Choppiness Index (14-period) - High values = choppy market
        ci = ta.ci(
            high=self.data.High,
            low=self.data.Low,
            close=self.data.Close,
            length=14
        )
        self.ci = self.I(lambda: ci, name='ChopIndex 🌊')

        # ADX (14-period) - Low values = weak trend
        self.adx = self.I(
            talib.ADX,
            self.data.High,
            self.data.Low,
            self.data.Close,
            timeperiod=14,
            name='ADX 📈'
        )

        # ====== GRID CALCULATION ======
        # Calculate grid based on 20-period high/low range
        self.range_high = self.I(
            talib.MAX,
            self.data.High,
            timeperiod=20,
            name='RangeHigh ⛰️'
        )

        self.range_low = self.I(
            talib.MIN,
            self.data.Low,
            timeperiod=20,
            name='RangeLow 🏞️'
        )

        # Bollinger Bands for additional range confirmation
        bb_upper, bb_middle, bb_lower = ta.bbands(
            close=self.data.Close,
            length=20,
            std=2
        )
        self.bb_upper = self.I(lambda: bb_upper, name='BB_Upper 📊')
        self.bb_lower = self.I(lambda: bb_lower, name='BB_Lower 📊')
        self.bb_middle = self.I(lambda: bb_middle, name='BB_Middle 📊')

        # Volume for confirmation
        self.vol_ma = self.I(
            talib.SMA,
            self.data.Volume,
            timeperiod=20,
            name='VolMA 📊'
        )

        # Track grid trades
        self.grid_trades = {}
        self.last_grid_update = 0

    def calculate_grid_levels(self):
        """Calculate buy and sell grid levels based on current range"""
        range_high = self.range_high[-1]
        range_low = self.range_low[-1]
        current_price = self.data.Close[-1]

        # Use the middle of the range as center
        range_center = (range_high + range_low) / 2
        range_size = range_high - range_low

        # Calculate grid spacing in absolute price
        grid_spacing = current_price * (self.grid_spacing_pct / 100)

        # Create buy levels below current price
        buy_levels = []
        for i in range(1, self.grid_levels + 1):
            level = current_price - (grid_spacing * i)
            if level > range_low:  # Only add if within range
                buy_levels.append(level)

        # Create sell levels above current price
        sell_levels = []
        for i in range(1, self.grid_levels + 1):
            level = current_price + (grid_spacing * i)
            if level < range_high:  # Only add if within range
                sell_levels.append(level)

        return buy_levels, sell_levels, range_center

    def is_choppy_market(self):
        """Determine if market is choppy/sideways"""
        # Check if we have enough data
        if len(self.data) < 20:
            return False

        ci_value = self.ci[-1]
        adx_value = self.adx[-1]

        # Market is choppy if:
        # 1. Choppiness Index is high (> threshold)
        # 2. ADX is low (< threshold) indicating weak trend
        is_choppy = (ci_value > self.chop_threshold and
                     adx_value < self.adx_threshold)

        return is_choppy

    def next(self):
        """Execute grid trading logic"""
        # ====== DEBUG PRINT ======
        if len(self.data) % 100 == 0:
            print(f"\n🌙 GRID STATUS @ Bar {len(self.data)} 🌙")
            print(f"Price: ${self.data.Close[-1]:.2f}")
            print(f"CI: {self.ci[-1]:.1f} (Choppy if > {self.chop_threshold})")
            print(f"ADX: {self.adx[-1]:.1f} (Weak trend if < {self.adx_threshold})")
            print(f"Open Positions: {len(self.trades)}")
            print(f"Equity: ${self.equity:.2f}")

        # Check if market is choppy
        if not self.is_choppy_market():
            # Not choppy - close all positions and wait
            if self.position:
                self.position.close()
                print(f"🌊 Market trending - closing grid positions")
            return

        # ====== GRID TRADING LOGIC ======
        current_price = self.data.Close[-1]
        buy_levels, sell_levels, range_center = self.calculate_grid_levels()

        # Calculate position size based on risk
        risk_amount = self.equity * self.risk_pct
        position_size_per_grid = int(risk_amount / (current_price * 0.02))  # 2% stop

        if position_size_per_grid < 1:
            position_size_per_grid = 1

        # ====== BUY AT LOWER GRID LEVELS ======
        for buy_level in buy_levels:
            # Check if price has reached this buy level
            if current_price <= buy_level * 1.001:  # Small tolerance
                # Check if we don't already have a position at this level
                level_key = f"buy_{buy_level:.2f}"

                if level_key not in self.grid_trades:
                    # Calculate take profit at next sell level
                    take_profit = buy_level * (1 + self.profit_per_grid / 100)

                    # Place buy order
                    self.buy(
                        size=position_size_per_grid,
                        tp=take_profit,
                        tag=f"Grid Buy @ {buy_level:.2f} 🟢"
                    )

                    self.grid_trades[level_key] = {
                        'entry': buy_level,
                        'tp': take_profit,
                        'type': 'buy'
                    }

                    print(f"\n🟢 GRID BUY TRIGGERED 🟢")
                    print(f"Entry: ${buy_level:.2f}")
                    print(f"Target: ${take_profit:.2f} ({self.profit_per_grid}% profit)")
                    print(f"Size: {position_size_per_grid}")
                    break  # Only one buy per bar

        # ====== SELL AT UPPER GRID LEVELS ======
        for sell_level in sell_levels:
            # Check if price has reached this sell level
            if current_price >= sell_level * 0.999:  # Small tolerance
                # Check if we don't already have a position at this level
                level_key = f"sell_{sell_level:.2f}"

                if level_key not in self.grid_trades:
                    # Calculate take profit at next buy level
                    take_profit = sell_level * (1 - self.profit_per_grid / 100)

                    # Place sell order (short)
                    self.sell(
                        size=position_size_per_grid,
                        tp=take_profit,
                        tag=f"Grid Sell @ {sell_level:.2f} 🔴"
                    )

                    self.grid_trades[level_key] = {
                        'entry': sell_level,
                        'tp': take_profit,
                        'type': 'sell'
                    }

                    print(f"\n🔴 GRID SELL TRIGGERED 🔴")
                    print(f"Entry: ${sell_level:.2f}")
                    print(f"Target: ${take_profit:.2f} ({self.profit_per_grid}% profit)")
                    print(f"Size: {position_size_per_grid}")
                    break  # Only one sell per bar

        # ====== CLEANUP CLOSED TRADES ======
        # Remove trades that have been closed from tracking
        if len(self.data) % 10 == 0:  # Cleanup every 10 bars
            active_trades = [t.tag for t in self.trades if t.is_open]
            keys_to_remove = []
            for key in list(self.grid_trades.keys()):
                level_str = key.split('_')[1]
                if not any(level_str in str(tag) for tag in active_trades):
                    keys_to_remove.append(key)

            for key in keys_to_remove:
                del self.grid_trades[key]


# ====== BACKTEST EXECUTION ======
if __name__ == '__main__':
    print("🌙 Moon Dev's Grid Trading Backtest Starting... 🚀\n")

    # Load sample data
    data_path = '/home/user/moon-dev-ai-agents/src/data/rbi/BTC-USD-15m.csv'

    try:
        df = pd.read_csv(data_path)
        print(f"✅ Loaded data: {len(df)} rows")

        # Ensure proper column names (backtesting.py expects capitalized OHLCV)
        df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']

        # Run backtest with different grid configurations
        print("\n" + "="*60)
        print("🌙 TESTING GRID CONFIGURATIONS 🌙")
        print("="*60 + "\n")

        configs = [
            {'grid_levels': 3, 'grid_spacing_pct': 1.0, 'profit_per_grid': 0.8},
            {'grid_levels': 5, 'grid_spacing_pct': 1.5, 'profit_per_grid': 1.0},
            {'grid_levels': 7, 'grid_spacing_pct': 2.0, 'profit_per_grid': 1.5},
        ]

        best_result = None
        best_return = -999999

        for config in configs:
            print(f"\n{'='*60}")
            print(f"Testing: {config['grid_levels']} levels, {config['grid_spacing_pct']}% spacing, {config['profit_per_grid']}% profit")
            print(f"{'='*60}\n")

            bt = Backtest(
                df,
                GridChopStrategy,
                cash=10000,
                commission=0.002,  # 0.2% trading fee
                exclusive_orders=False  # Allow multiple positions
            )

            stats = bt.run(
                grid_levels=config['grid_levels'],
                grid_spacing_pct=config['grid_spacing_pct'],
                profit_per_grid=config['profit_per_grid']
            )

            print(f"\n🌙 RESULTS 🌙")
            print(f"Return: {stats['Return [%]']:.2f}%")
            print(f"Buy & Hold: {stats['Buy & Hold Return [%]']:.2f}%")
            print(f"Sharpe Ratio: {stats['Sharpe Ratio']:.2f}")
            print(f"Max Drawdown: {stats['Max. Drawdown [%]']:.2f}%")
            print(f"Trades: {stats['# Trades']}")
            print(f"Win Rate: {stats['Win Rate [%]']:.1f}%")

            if stats['Return [%]'] > best_return:
                best_return = stats['Return [%]']
                best_result = (config, stats, bt)

        # Display best configuration
        if best_result:
            config, stats, bt = best_result
            print(f"\n{'='*60}")
            print(f"🏆 BEST CONFIGURATION 🏆")
            print(f"{'='*60}")
            print(f"Grid Levels: {config['grid_levels']}")
            print(f"Grid Spacing: {config['grid_spacing_pct']}%")
            print(f"Profit per Grid: {config['profit_per_grid']}%")
            print(f"\nReturn: {stats['Return [%]']:.2f}%")
            print(f"Sharpe Ratio: {stats['Sharpe Ratio']:.2f}")
            print(f"Max Drawdown: {stats['Max. Drawdown [%]']:.2f}%")
            print(f"Total Trades: {stats['# Trades']}")

            # Uncomment to see interactive chart
            # bt.plot()

    except FileNotFoundError:
        print(f"❌ Data file not found at: {data_path}")
        print("💡 Please ensure you have OHLCV data in CSV format")
        print("   Required columns: Open, High, Low, Close, Volume")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
