"""
🌙 Moon Dev's Grid Trading Agent - Live Trading Version
Manages grid orders during choppy/sideways market conditions
Built with love by Moon Dev 🚀

USAGE:
    python src/agents/grid_agent.py

CONFIGURATION:
    Edit the GRID_CONFIG dictionary below to customize grid behavior
"""

from src.config import *
from src import nice_funcs as n
from termcolor import cprint
import pandas as pd
import pandas_ta as ta
import talib
import time
import json
import os
from datetime import datetime

# ====== GRID CONFIGURATION ======
GRID_CONFIG = {
    'enabled': True,                    # Enable/disable grid trading
    'grid_levels': 5,                   # Number of grid levels above/below price
    'grid_spacing_pct': 1.5,           # % spacing between grid levels
    'profit_per_grid_pct': 1.0,        # % profit target per grid trade
    'max_grid_positions': 10,           # Maximum concurrent grid positions
    'position_size_usd': 50,            # USD size per grid order
    'chop_threshold': 61.8,             # CI > this = choppy market
    'adx_threshold': 25,                # ADX < this = weak trend
    'lookback_period': 20,              # Bars to calculate range
    'min_range_width_pct': 2.0,        # Minimum range width to trade (%)
    'refresh_interval_minutes': 5,      # How often to refresh grid
}

class GridTradingAgent:
    def __init__(self):
        """Initialize the Grid Trading Agent"""
        self.config = GRID_CONFIG
        self.active_grids = {}  # Track active grid orders
        self.last_grid_update = None
        self.data_folder = 'src/data/grid_agent'

        # Create data folder if it doesn't exist
        os.makedirs(self.data_folder, exist_ok=True)

        cprint("🌙 Moon Dev's Grid Trading Agent Initialized 🚀", "cyan")
        self.print_config()

    def print_config(self):
        """Print current grid configuration"""
        cprint("\n📋 Grid Configuration:", "yellow")
        for key, value in self.config.items():
            print(f"  • {key}: {value}")
        print()

    def get_market_data(self, token_address, timeframe='15m', days_back=3):
        """Fetch OHLCV data for analysis"""
        try:
            df = n.get_ohlcv_data(
                token_address,
                timeframe=timeframe,
                days_back=days_back
            )

            if df is None or df.empty:
                cprint(f"❌ No data available for {token_address}", "red")
                return None

            return df

        except Exception as e:
            cprint(f"❌ Error fetching market data: {e}", "red")
            return None

    def calculate_indicators(self, df):
        """Calculate chop detection indicators"""
        try:
            # Choppiness Index
            ci = ta.ci(
                high=df['high'],
                low=df['low'],
                close=df['close'],
                length=14
            )

            # ADX
            adx = talib.ADX(
                df['high'].values,
                df['low'].values,
                df['close'].values,
                timeperiod=14
            )

            # Range high/low
            range_high = df['high'].rolling(window=self.config['lookback_period']).max()
            range_low = df['low'].rolling(window=self.config['lookback_period']).min()

            # Add to dataframe
            df['ci'] = ci
            df['adx'] = adx
            df['range_high'] = range_high
            df['range_low'] = range_low

            return df

        except Exception as e:
            cprint(f"❌ Error calculating indicators: {e}", "red")
            return None

    def is_choppy_market(self, df):
        """Determine if market is in choppy/sideways condition"""
        try:
            latest = df.iloc[-1]

            ci_value = latest['ci']
            adx_value = latest['adx']

            # Check for NaN values
            if pd.isna(ci_value) or pd.isna(adx_value):
                return False

            # Market is choppy if CI is high and ADX is low
            is_choppy = (ci_value > self.config['chop_threshold'] and
                        adx_value < self.config['adx_threshold'])

            cprint(f"\n📊 Market Analysis:", "cyan")
            print(f"  Choppiness Index: {ci_value:.1f} (Choppy if > {self.config['chop_threshold']})")
            print(f"  ADX: {adx_value:.1f} (Weak trend if < {self.config['adx_threshold']})")

            if is_choppy:
                cprint(f"  ✅ Market is CHOPPY - Grid trading conditions MET! 🌊", "green")
            else:
                cprint(f"  ❌ Market is TRENDING - No grid trading 📈", "yellow")

            return is_choppy

        except Exception as e:
            cprint(f"❌ Error checking market conditions: {e}", "red")
            return False

    def calculate_grid_levels(self, df, current_price):
        """Calculate buy and sell grid levels"""
        try:
            latest = df.iloc[-1]
            range_high = latest['range_high']
            range_low = latest['range_low']
            range_width = range_high - range_low
            range_width_pct = (range_width / current_price) * 100

            # Check if range is wide enough
            if range_width_pct < self.config['min_range_width_pct']:
                cprint(f"⚠️ Range too narrow ({range_width_pct:.2f}%) - Need at least {self.config['min_range_width_pct']}%", "yellow")
                return None, None

            cprint(f"\n📏 Range Analysis:", "cyan")
            print(f"  Range High: ${range_high:.4f}")
            print(f"  Range Low: ${range_low:.4f}")
            print(f"  Range Width: {range_width_pct:.2f}%")
            print(f"  Current Price: ${current_price:.4f}")

            # Calculate grid spacing
            grid_spacing = current_price * (self.config['grid_spacing_pct'] / 100)

            # Buy levels below current price
            buy_levels = []
            for i in range(1, self.config['grid_levels'] + 1):
                level = current_price - (grid_spacing * i)
                if level > range_low:  # Within range
                    buy_levels.append(level)

            # Sell levels above current price
            sell_levels = []
            for i in range(1, self.config['grid_levels'] + 1):
                level = current_price + (grid_spacing * i)
                if level < range_high:  # Within range
                    sell_levels.append(level)

            cprint(f"\n🎯 Grid Levels Calculated:", "green")
            print(f"  Buy Levels ({len(buy_levels)}): {[f'${l:.4f}' for l in buy_levels]}")
            print(f"  Sell Levels ({len(sell_levels)}): {[f'${l:.4f}' for l in sell_levels]}")

            return buy_levels, sell_levels

        except Exception as e:
            cprint(f"❌ Error calculating grid levels: {e}", "red")
            return None, None

    def place_grid_order(self, token_address, level, order_type='BUY'):
        """Place a grid order (buy or sell)"""
        try:
            # Calculate take profit
            if order_type == 'BUY':
                take_profit_price = level * (1 + self.config['profit_per_grid_pct'] / 100)
            else:
                take_profit_price = level * (1 - self.config['profit_per_grid_pct'] / 100)

            # For now, execute market orders when price hits level
            current_price = n.token_price(token_address)

            # Check if price is at the grid level (within tolerance)
            tolerance = 0.005  # 0.5% tolerance
            price_at_level = abs(current_price - level) / level < tolerance

            if not price_at_level:
                return False

            # Execute order
            if order_type == 'BUY':
                cprint(f"\n🟢 Executing GRID BUY at ${current_price:.4f}", "green")
                result = n.market_buy(
                    token_address,
                    self.config['position_size_usd'],
                    slippage
                )
            else:
                cprint(f"\n🔴 Executing GRID SELL at ${current_price:.4f}", "red")
                result = n.market_sell(
                    token_address,
                    self.config['position_size_usd'],
                    slippage
                )

            if result:
                # Track this grid position
                grid_key = f"{order_type}_{level:.4f}"
                self.active_grids[grid_key] = {
                    'type': order_type,
                    'entry_price': current_price,
                    'target_price': take_profit_price,
                    'timestamp': datetime.now().isoformat(),
                    'size_usd': self.config['position_size_usd']
                }

                self.save_grid_state()
                cprint(f"✅ Grid order placed! Target: ${take_profit_price:.4f} ({self.config['profit_per_grid_pct']}% profit)", "green")
                return True

            return False

        except Exception as e:
            cprint(f"❌ Error placing grid order: {e}", "red")
            return False

    def check_take_profits(self, token_address):
        """Check if any grid positions hit their take profit targets"""
        try:
            if not self.active_grids:
                return

            current_price = n.token_price(token_address)
            positions_to_close = []

            for grid_key, grid_data in self.active_grids.items():
                target_price = grid_data['target_price']
                order_type = grid_data['type']

                # Check if target hit
                target_hit = False
                if order_type == 'BUY' and current_price >= target_price:
                    target_hit = True
                elif order_type == 'SELL' and current_price <= target_price:
                    target_hit = True

                if target_hit:
                    cprint(f"\n🎯 Take Profit HIT for {grid_key}!", "green")
                    print(f"  Entry: ${grid_data['entry_price']:.4f}")
                    print(f"  Target: ${target_price:.4f}")
                    print(f"  Current: ${current_price:.4f}")

                    # Close position
                    if order_type == 'BUY':
                        n.market_sell(token_address, grid_data['size_usd'], slippage)
                    else:
                        n.market_buy(token_address, grid_data['size_usd'], slippage)

                    positions_to_close.append(grid_key)

            # Remove closed positions
            for grid_key in positions_to_close:
                del self.active_grids[grid_key]

            if positions_to_close:
                self.save_grid_state()

        except Exception as e:
            cprint(f"❌ Error checking take profits: {e}", "red")

    def save_grid_state(self):
        """Save current grid state to file"""
        try:
            filepath = os.path.join(self.data_folder, 'active_grids.json')
            with open(filepath, 'w') as f:
                json.dump(self.active_grids, f, indent=2)
        except Exception as e:
            cprint(f"⚠️ Could not save grid state: {e}", "yellow")

    def load_grid_state(self):
        """Load grid state from file"""
        try:
            filepath = os.path.join(self.data_folder, 'active_grids.json')
            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    self.active_grids = json.load(f)
                    cprint(f"✅ Loaded {len(self.active_grids)} active grid positions", "green")
        except Exception as e:
            cprint(f"⚠️ Could not load grid state: {e}", "yellow")

    def run_grid_cycle(self, token_address):
        """Execute one cycle of grid trading"""
        try:
            cprint(f"\n{'='*60}", "cyan")
            cprint(f"🌙 GRID TRADING CYCLE - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", "cyan")
            cprint(f"{'='*60}", "cyan")

            # Check if grid trading is enabled
            if not self.config['enabled']:
                cprint("⏸️ Grid trading is disabled in config", "yellow")
                return

            # Get market data
            cprint(f"\n📊 Fetching market data for {token_address}...", "cyan")
            df = self.get_market_data(token_address, timeframe='15m', days_back=3)

            if df is None:
                return

            # Calculate indicators
            df = self.calculate_indicators(df)
            if df is None:
                return

            # Check if market is choppy
            if not self.is_choppy_market(df):
                cprint("\n⏸️ Market not choppy - closing existing grid positions", "yellow")
                # Close all grid positions when market starts trending
                if self.active_grids:
                    for grid_key in list(self.active_grids.keys()):
                        order_type = self.active_grids[grid_key]['type']
                        size_usd = self.active_grids[grid_key]['size_usd']

                        if order_type == 'BUY':
                            n.market_sell(token_address, size_usd, slippage)
                        else:
                            n.market_buy(token_address, size_usd, slippage)

                    self.active_grids = {}
                    self.save_grid_state()
                    cprint("✅ All grid positions closed", "green")
                return

            # Get current price
            current_price = n.token_price(token_address)
            cprint(f"\n💰 Current Price: ${current_price:.4f}", "cyan")

            # Check take profits on existing positions
            self.check_take_profits(token_address)

            # Check if we can place more grid orders
            if len(self.active_grids) >= self.config['max_grid_positions']:
                cprint(f"\n⚠️ Maximum grid positions reached ({self.config['max_grid_positions']})", "yellow")
                return

            # Calculate grid levels
            buy_levels, sell_levels = self.calculate_grid_levels(df, current_price)

            if buy_levels is None or sell_levels is None:
                return

            # Try to place grid orders at levels
            for buy_level in buy_levels:
                if len(self.active_grids) >= self.config['max_grid_positions']:
                    break

                grid_key = f"BUY_{buy_level:.4f}"
                if grid_key not in self.active_grids:
                    self.place_grid_order(token_address, buy_level, 'BUY')

            for sell_level in sell_levels:
                if len(self.active_grids) >= self.config['max_grid_positions']:
                    break

                grid_key = f"SELL_{sell_level:.4f}"
                if grid_key not in self.active_grids:
                    self.place_grid_order(token_address, sell_level, 'SELL')

            # Print current grid status
            cprint(f"\n📊 Active Grid Positions: {len(self.active_grids)}", "cyan")
            for grid_key, grid_data in self.active_grids.items():
                print(f"  • {grid_key}: Entry ${grid_data['entry_price']:.4f} → Target ${grid_data['target_price']:.4f}")

        except Exception as e:
            cprint(f"❌ Error in grid cycle: {e}", "red")
            import traceback
            traceback.print_exc()

    def run(self, token_address=None):
        """Main loop for grid trading agent"""
        try:
            # Load previous grid state
            self.load_grid_state()

            # Use token from config if not specified
            if token_address is None:
                if MONITORED_TOKENS:
                    token_address = MONITORED_TOKENS[0]
                else:
                    cprint("❌ No token specified and MONITORED_TOKENS is empty", "red")
                    return

            cprint(f"\n🚀 Starting Grid Trading Agent for {token_address}", "green")
            cprint(f"💤 Refresh interval: {self.config['refresh_interval_minutes']} minutes\n", "cyan")

            while True:
                try:
                    self.run_grid_cycle(token_address)

                    # Sleep until next cycle
                    sleep_seconds = self.config['refresh_interval_minutes'] * 60
                    cprint(f"\n💤 Sleeping for {self.config['refresh_interval_minutes']} minutes...", "cyan")
                    time.sleep(sleep_seconds)

                except KeyboardInterrupt:
                    cprint("\n\n🛑 Grid Trading Agent stopped by user", "yellow")
                    break
                except Exception as e:
                    cprint(f"\n❌ Error in main loop: {e}", "red")
                    import traceback
                    traceback.print_exc()
                    time.sleep(60)  # Wait a minute before retrying

        except Exception as e:
            cprint(f"❌ Fatal error: {e}", "red")
            import traceback
            traceback.print_exc()


# ====== STANDALONE EXECUTION ======
if __name__ == "__main__":
    cprint("🌙 Moon Dev's Grid Trading Agent 🚀", "cyan")
    cprint("="*60 + "\n", "cyan")

    agent = GridTradingAgent()
    agent.run()
