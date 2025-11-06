"""
🌙 Moon Dev's Grid Chop Strategy
Grid trading strategy for choppy/sideways markets
Can be used with the Strategy Agent
"""

from src.strategies.base_strategy import BaseStrategy
from src.config import MONITORED_TOKENS
from src import nice_funcs as n
import pandas as pd
import pandas_ta as ta
import talib
from termcolor import cprint

class GridChopStrategy(BaseStrategy):
    def __init__(self):
        """Initialize the Grid Chop Strategy"""
        super().__init__("Grid Chop Strategy")

        # Strategy parameters
        self.chop_threshold = 61.8      # CI > this = choppy
        self.adx_threshold = 25         # ADX < this = weak trend
        self.grid_spacing_pct = 1.5     # Grid spacing percentage
        self.min_range_width_pct = 2.0  # Minimum range to trade

        cprint(f"✅ {self.name} initialized", "green")

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
            range_high = df['high'].rolling(window=20).max()
            range_low = df['low'].rolling(window=20).min()

            df['ci'] = ci
            df['adx'] = adx
            df['range_high'] = range_high
            df['range_low'] = range_low

            return df

        except Exception as e:
            cprint(f"❌ Error calculating indicators: {e}", "red")
            return None

    def is_choppy_market(self, df):
        """Check if market is in choppy condition"""
        try:
            latest = df.iloc[-1]

            ci_value = latest['ci']
            adx_value = latest['adx']

            if pd.isna(ci_value) or pd.isna(adx_value):
                return False

            return (ci_value > self.chop_threshold and
                   adx_value < self.adx_threshold)

        except Exception as e:
            return False

    def generate_signals(self) -> dict:
        """Generate trading signals based on grid chop conditions"""
        try:
            for token in MONITORED_TOKENS:
                # Get market data
                df = n.get_ohlcv_data(token, timeframe='15m', days_back=3)

                if df is None or df.empty:
                    continue

                # Calculate indicators
                df = self.calculate_indicators(df)
                if df is None:
                    continue

                # Get current values
                latest = df.iloc[-1]
                current_price = latest['close']
                ci_value = latest['ci']
                adx_value = latest['adx']
                range_high = latest['range_high']
                range_low = latest['range_low']

                # Check for NaN
                if pd.isna(ci_value) or pd.isna(adx_value):
                    continue

                # Calculate range width
                range_width_pct = ((range_high - range_low) / current_price) * 100

                # Check if choppy
                is_choppy = self.is_choppy_market(df)

                # Prepare signal
                signal = {
                    'token': token,
                    'signal': 0.0,
                    'direction': 'NEUTRAL',
                    'metadata': {
                        'strategy_type': 'grid_chop',
                        'ci': float(ci_value),
                        'adx': float(adx_value),
                        'range_high': float(range_high),
                        'range_low': float(range_low),
                        'range_width_pct': float(range_width_pct),
                        'current_price': float(current_price),
                        'is_choppy': is_choppy
                    }
                }

                # Generate signal based on conditions
                if is_choppy and range_width_pct >= self.min_range_width_pct:
                    # Calculate position in range (0 = bottom, 1 = top)
                    position_in_range = (current_price - range_low) / (range_high - range_low)

                    # Buy signal if price is in lower part of range
                    if position_in_range < 0.3:
                        signal.update({
                            'signal': 0.8,  # High confidence
                            'direction': 'BUY'
                        })
                        signal['metadata']['reason'] = f"Choppy market, price at bottom {position_in_range*100:.1f}% of range"

                    # Sell signal if price is in upper part of range
                    elif position_in_range > 0.7:
                        signal.update({
                            'signal': 0.8,  # High confidence
                            'direction': 'SELL'
                        })
                        signal['metadata']['reason'] = f"Choppy market, price at top {position_in_range*100:.1f}% of range"

                    # Neutral in middle of range
                    else:
                        signal['metadata']['reason'] = f"Choppy market, price in middle {position_in_range*100:.1f}% of range"

                elif not is_choppy:
                    # Market is trending - close positions
                    signal.update({
                        'signal': 0.9,
                        'direction': 'SELL'
                    })
                    signal['metadata']['reason'] = "Market trending - exit grid positions"

                else:
                    signal['metadata']['reason'] = f"Range too narrow ({range_width_pct:.2f}%)"

                # Return signal if actionable
                if signal['direction'] != 'NEUTRAL':
                    cprint(f"\n🎯 {self.name} Signal for {token}:", "cyan")
                    cprint(f"  Direction: {signal['direction']}", "yellow")
                    cprint(f"  Confidence: {signal['signal']*100:.0f}%", "yellow")
                    cprint(f"  Reason: {signal['metadata']['reason']}", "white")
                    return signal

            return None

        except Exception as e:
            cprint(f"❌ Error generating signals: {str(e)}", "red")
            return None
