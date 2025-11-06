# 🌙 Grid Trading Bot - Complete Guide

## Overview

The Grid Trading Bot is a specialized AI agent for trading during **choppy/sideways market conditions**. It automatically detects range-bound markets and places buy/sell orders at different price levels (the "grid"), profiting from price oscillations.

**Built by Moon Dev 🚀**

---

## 📚 Table of Contents

1. [What is Grid Trading?](#what-is-grid-trading)
2. [How It Works](#how-it-works)
3. [Components](#components)
4. [Installation & Setup](#installation--setup)
5. [Configuration](#configuration)
6. [Usage](#usage)
7. [Backtesting](#backtesting)
8. [Live Trading](#live-trading)
9. [Risk Management](#risk-management)
10. [Examples](#examples)

---

## What is Grid Trading?

Grid trading is a mechanical trading strategy that places buy and sell orders at predetermined intervals (grid levels) above and below a set price. It profits from price volatility within a range, making it ideal for **choppy/sideways markets**.

### Key Concepts:

- **Grid Levels**: Pre-defined buy and sell price points
- **Grid Spacing**: Distance between each grid level (e.g., 1.5% apart)
- **Profit Target**: Expected profit from each grid trade (e.g., 1% per trade)
- **Choppy Market**: Range-bound price action with no clear trend

### When to Use:

✅ **Good For:**
- Sideways/choppy markets
- High volatility within a range
- Consolidation phases
- Stable support/resistance levels

❌ **Bad For:**
- Strong trending markets (up or down)
- Low volatility periods
- Breaking support/resistance levels

---

## How It Works

### 1. Market Detection
The bot uses two indicators to detect choppy markets:

- **Choppiness Index (CI)**: Measures market choppiness
  - CI > 61.8 = Choppy market ✅
  - CI < 38.2 = Trending market ❌

- **ADX (Average Directional Index)**: Measures trend strength
  - ADX < 25 = Weak trend (good for grid) ✅
  - ADX > 25 = Strong trend (avoid grid) ❌

### 2. Grid Setup
Once a choppy market is detected:

1. Calculate the price range (high/low over lookback period)
2. Set current price as the center point
3. Place buy orders below current price
4. Place sell orders above current price
5. Each level is spaced by a percentage (e.g., 1.5%)

### 3. Order Execution

**Buy Orders** (below current price):
- Execute when price drops to grid level
- Take profit when price rises by target % (e.g., 1%)
- Re-buy if price drops back to that level

**Sell Orders** (above current price):
- Execute when price rises to grid level
- Take profit when price drops by target % (e.g., 1%)
- Re-sell if price rises back to that level

### 4. Exit Conditions
The bot closes all positions when:
- Market becomes trending (CI < 61.8 or ADX > 25)
- Maximum drawdown reached
- User manually stops the bot

---

## Components

The Grid Trading Bot has three implementations:

### 1. **Backtest Version** (`GridChop_BT.py`)
- Tests strategy on historical data
- Located: `src/data/rbi/GridChop_BT.py`
- Tests multiple configurations automatically
- Outputs: Return %, Sharpe Ratio, Max Drawdown, Win Rate

### 2. **Live Trading Agent** (`grid_agent.py`)
- Standalone bot for live trading
- Located: `src/agents/grid_agent.py`
- Runs continuously with configurable refresh intervals
- Tracks active grid positions
- Auto-saves state to recover from crashes

### 3. **Strategy Module** (`grid_chop_strategy.py`)
- Integration with Strategy Agent
- Located: `src/strategies/grid_chop_strategy.py`
- Can be combined with other strategies
- Uses AI confirmation before trades

---

## Installation & Setup

### Prerequisites

```bash
# 1. Activate conda environment
conda activate tflow

# 2. Ensure all dependencies are installed
pip install -r requirements.txt

# Required packages:
# - pandas
# - pandas_ta
# - talib (TA-Lib)
# - backtesting
# - termcolor
```

### Setup API Keys

Ensure your `.env` file has required keys:

```bash
# Market Data (required for live trading)
BIRDEYE_API_KEY=your_birdeye_key
COINGECKO_API_KEY=your_coingecko_key

# AI Models (required for strategy agent)
ANTHROPIC_KEY=your_claude_key  # or
OPENAI_KEY=your_gpt_key
```

### Configuration

Edit grid settings in `src/agents/grid_agent.py` (lines 32-45):

```python
GRID_CONFIG = {
    'enabled': True,                    # Enable/disable grid trading
    'grid_levels': 5,                   # Number of grid levels (3-10 recommended)
    'grid_spacing_pct': 1.5,           # % spacing between levels (1-3% typical)
    'profit_per_grid_pct': 1.0,        # % profit target per trade (0.5-2% typical)
    'max_grid_positions': 10,           # Max concurrent positions
    'position_size_usd': 50,            # USD per grid order
    'chop_threshold': 61.8,             # CI > this = choppy
    'adx_threshold': 25,                # ADX < this = weak trend
    'lookback_period': 20,              # Bars to calculate range
    'min_range_width_pct': 2.0,        # Min range to trade (%)
    'refresh_interval_minutes': 5,      # Update frequency
}
```

---

## Configuration

### Grid Parameters

#### `grid_levels` (3-10)
Number of buy/sell levels above/below current price.

- **Lower (3-5)**: Fewer positions, less capital required
- **Higher (7-10)**: More positions, captures more price action

**Example:**
- 3 levels: Buy at -1.5%, -3%, -4.5% | Sell at +1.5%, +3%, +4.5%
- 5 levels: Buy at -1.5%, -3%, -4.5%, -6%, -7.5% | Sell at +1.5%, +3%, +4.5%, +6%, +7.5%

#### `grid_spacing_pct` (1.0-3.0%)
Distance between each grid level.

- **Tighter (1.0-1.5%)**: More frequent trades, lower profit per trade
- **Wider (2.0-3.0%)**: Fewer trades, higher profit per trade

**Recommendation:**
- High volatility tokens: 2.0-3.0%
- Stable tokens: 1.0-1.5%

#### `profit_per_grid_pct` (0.5-2.0%)
Profit target for each grid trade.

- **Lower (0.5-1.0%)**: Faster exits, higher win rate
- **Higher (1.5-2.0%)**: Slower exits, more profit per trade

**Formula:**
Total profit = grid_levels × profit_per_grid_pct × win_rate

Example: 5 levels × 1.0% × 70% win rate = 3.5% potential per cycle

#### `position_size_usd` (10-100)
USD amount per grid order.

**Risk Calculation:**
```
Total Risk = grid_levels × position_size_usd × 2
```

Example: 5 levels × $50 = $250 max exposure per side ($500 total)

### Market Detection Parameters

#### `chop_threshold` (55-70)
Choppiness Index threshold for market detection.

- **Default: 61.8** (Fibonacci level)
- Higher values = Stricter (only very choppy markets)
- Lower values = More lenient (includes slightly trending)

#### `adx_threshold` (20-30)
ADX threshold for trend strength.

- **Default: 25**
- Lower values = Stricter (only very weak trends)
- Higher values = More lenient (includes moderate trends)

#### `min_range_width_pct` (2.0-5.0%)
Minimum range width to enable grid trading.

- **Default: 2.0%**
- Prevents trading in extremely tight ranges
- Should be > (grid_spacing_pct × grid_levels)

---

## Usage

### Backtesting (Recommended First!)

Test the strategy on historical data before risking real money:

```bash
# Activate environment
conda activate tflow

# Run backtest
python src/data/rbi/GridChop_BT.py
```

**Output:**
```
🌙 Moon Dev's Grid Trading Backtest Starting... 🚀

Testing: 5 levels, 1.5% spacing, 1.0% profit
============================================================

🌙 RESULTS 🌙
Return: 12.34%
Buy & Hold: 5.67%
Sharpe Ratio: 1.82
Max Drawdown: -3.21%
Trades: 247
Win Rate: 68.4%

🏆 BEST CONFIGURATION 🏆
Grid Levels: 5
Grid Spacing: 1.5%
Profit per Grid: 1.0%
```

**Analyze Results:**
- Return > Buy & Hold = Strategy outperforms ✅
- Sharpe Ratio > 1.0 = Good risk-adjusted returns ✅
- Win Rate > 60% = Consistent profitability ✅
- Max Drawdown < 10% = Acceptable risk ✅

### Live Trading (After Backtesting!)

Run the standalone grid agent:

```bash
# Configure your token in src/config.py
# Edit MONITORED_TOKENS = ['YOUR_TOKEN_ADDRESS']

# Run the agent
python src/agents/grid_agent.py
```

**Agent Output:**
```
🌙 Moon Dev's Grid Trading Agent 🚀
============================================================

📋 Grid Configuration:
  • grid_levels: 5
  • grid_spacing_pct: 1.5
  • position_size_usd: 50

🌙 GRID TRADING CYCLE - 2025-01-15 10:30:00
============================================================

📊 Fetching market data for 9BB6NFEcjBCtnNLFko2FqVQBq8HHM13kCyYcdQbgpump...
✅ Loaded data: 288 rows

📊 Market Analysis:
  Choppiness Index: 64.2 (Choppy if > 61.8)
  ADX: 18.3 (Weak trend if < 25)
  ✅ Market is CHOPPY - Grid trading conditions MET! 🌊

💰 Current Price: $0.1234

📏 Range Analysis:
  Range High: $0.1456
  Range Low: $0.1012
  Range Width: 18.65%
  Current Price: $0.1234

🎯 Grid Levels Calculated:
  Buy Levels (3): ['$0.1215', '$0.1196', '$0.1177']
  Sell Levels (3): ['$0.1253', '$0.1272', '$0.1291']

🟢 GRID BUY TRIGGERED 🟢
Entry: $0.1215
Target: $0.1227 (1.0% profit)
Size: 411

✅ Grid order placed! Target: $0.1227 (1.0% profit)

📊 Active Grid Positions: 1
  • BUY_0.1215: Entry $0.1215 → Target $0.1227

💤 Sleeping for 5 minutes...
```

### Integration with Strategy Agent

Add grid strategy to your strategy mix:

```python
# In src/agents/strategy_agent.py
from src.strategies.grid_chop_strategy import GridChopStrategy

# Add to enabled strategies
self.enabled_strategies.extend([
    GridChopStrategy()
])
```

Then run the main orchestrator:

```bash
python src/main.py
```

The Strategy Agent will:
1. Collect signals from Grid Chop Strategy
2. Validate with AI (Claude/GPT)
3. Execute approved trades
4. Combine with other active strategies

---

## Backtesting

### Test Different Configurations

Edit the `configs` list in `GridChop_BT.py`:

```python
configs = [
    # Conservative (tight grid, small profit)
    {'grid_levels': 3, 'grid_spacing_pct': 1.0, 'profit_per_grid': 0.8},

    # Balanced (default)
    {'grid_levels': 5, 'grid_spacing_pct': 1.5, 'profit_per_grid': 1.0},

    # Aggressive (wide grid, large profit)
    {'grid_levels': 7, 'grid_spacing_pct': 2.0, 'profit_per_grid': 1.5},
]
```

### Optimize Parameters

The backtest automatically finds the best configuration:

```python
# Runs all configs and compares results
best_result = None
best_return = -999999

for config in configs:
    stats = bt.run(**config)
    if stats['Return [%]'] > best_return:
        best_return = stats['Return [%]']
        best_result = (config, stats, bt)

# Shows winner
print(f"🏆 BEST CONFIGURATION 🏆")
print(best_result)
```

### Test on Different Data

Add your own datasets:

```python
# Test on different tokens
datasets = [
    'src/data/rbi/BTC-USD-15m.csv',
    'src/data/rbi/ETH-USD-15m.csv',
    'src/data/rbi/SOL-USD-15m.csv',
]

for dataset in datasets:
    df = pd.read_csv(dataset)
    bt = Backtest(df, GridChopStrategy, cash=10000, commission=0.002)
    stats = bt.run()
    print(f"{dataset}: {stats['Return [%]']:.2f}%")
```

---

## Live Trading

### Start the Agent

```bash
# 1. Configure token in src/config.py
MONITORED_TOKENS = ['YOUR_TOKEN_ADDRESS']

# 2. Adjust grid settings in src/agents/grid_agent.py
GRID_CONFIG = {
    'position_size_usd': 50,  # Start small!
    'grid_levels': 5,
    # ... other settings
}

# 3. Run the agent
python src/agents/grid_agent.py
```

### Monitor Performance

The agent saves state to `src/data/grid_agent/active_grids.json`:

```json
{
  "BUY_0.1215": {
    "type": "BUY",
    "entry_price": 0.1215,
    "target_price": 0.1227,
    "timestamp": "2025-01-15T10:30:00",
    "size_usd": 50
  },
  "SELL_0.1253": {
    "type": "SELL",
    "entry_price": 0.1253,
    "target_price": 0.1240,
    "timestamp": "2025-01-15T10:35:00",
    "size_usd": 50
  }
}
```

### Recovery from Crashes

The agent auto-loads previous state on restart:

```python
# On startup
agent.load_grid_state()
# ✅ Loaded 2 active grid positions

# Resumes monitoring existing positions
# Places new orders as needed
```

### Stop the Agent

Press `Ctrl+C` for graceful shutdown:

```
^C
🛑 Grid Trading Agent stopped by user
✅ Grid state saved to src/data/grid_agent/active_grids.json
```

---

## Risk Management

### Position Sizing

Calculate total exposure:

```
Max Exposure = grid_levels × position_size_usd × 2
```

**Example:**
- 5 levels × $50 × 2 = $500 total max exposure
- This assumes all grid levels get filled on both sides

**Recommendation:**
```
position_size_usd = (Portfolio Size × Risk %) / (grid_levels × 2)
```

For $10,000 portfolio with 5% risk:
```
position_size_usd = ($10,000 × 0.05) / (5 × 2) = $50
```

### Risk Controls

The grid agent has built-in protections:

1. **Max Grid Positions**: Limits concurrent trades
   ```python
   'max_grid_positions': 10  # Cap at 10 positions
   ```

2. **Minimum Range Width**: Prevents tight ranges
   ```python
   'min_range_width_pct': 2.0  # Need 2% range minimum
   ```

3. **Chop Detection**: Only trades suitable markets
   ```python
   if not is_choppy_market():
       close_all_positions()  # Exit on trending
   ```

4. **Take Profit**: Auto-closes at targets
   ```python
   if current_price >= target_price:
       close_position()  # Take profit hit
   ```

### Circuit Breakers

Use Moon Dev's global risk settings in `src/config.py`:

```python
# Maximum loss before stopping
MAX_LOSS_USD = 100  # Stop at $100 loss

# Minimum balance to continue
MINIMUM_BALANCE_USD = 500  # Stop if balance < $500

# Use AI confirmation for closes
USE_AI_CONFIRMATION = True  # Ask AI before closing
```

The Risk Agent monitors these limits across all agents.

---

## Examples

### Example 1: Conservative Grid (Low Risk)

**Setup:**
```python
GRID_CONFIG = {
    'grid_levels': 3,
    'grid_spacing_pct': 1.0,
    'profit_per_grid_pct': 0.5,
    'position_size_usd': 25,
    'max_grid_positions': 6,
}
```

**Characteristics:**
- Only 3 levels (less capital)
- Tight spacing (1%)
- Small profit targets (0.5%)
- Quick exits, high win rate

**Best For:**
- Small accounts (<$1000)
- High volatility tokens
- Learning grid trading

**Expected Results:**
- Win Rate: 70-80%
- Return per trade: 0.5%
- Drawdown: Low (<5%)

---

### Example 2: Balanced Grid (Medium Risk)

**Setup:**
```python
GRID_CONFIG = {
    'grid_levels': 5,
    'grid_spacing_pct': 1.5,
    'profit_per_grid_pct': 1.0,
    'position_size_usd': 50,
    'max_grid_positions': 10,
}
```

**Characteristics:**
- 5 levels (moderate capital)
- Medium spacing (1.5%)
- Standard profit (1%)
- Balanced risk/reward

**Best For:**
- Medium accounts ($1000-$10,000)
- Most tokens
- Default recommendation

**Expected Results:**
- Win Rate: 65-75%
- Return per trade: 1.0%
- Drawdown: Medium (5-10%)

---

### Example 3: Aggressive Grid (High Risk)

**Setup:**
```python
GRID_CONFIG = {
    'grid_levels': 7,
    'grid_spacing_pct': 2.5,
    'profit_per_grid_pct': 2.0,
    'position_size_usd': 100,
    'max_grid_positions': 14,
}
```

**Characteristics:**
- 7 levels (high capital)
- Wide spacing (2.5%)
- Large profit targets (2%)
- Higher profit potential, lower win rate

**Best For:**
- Large accounts (>$10,000)
- Low volatility tokens
- Experienced traders

**Expected Results:**
- Win Rate: 55-65%
- Return per trade: 2.0%
- Drawdown: High (10-20%)

---

## Troubleshooting

### Issue: No Grid Orders Placed

**Cause:** Market not meeting chop conditions

**Solution:**
- Lower `chop_threshold` (try 55-60)
- Raise `adx_threshold` (try 30-35)
- Lower `min_range_width_pct` (try 1.5%)

---

### Issue: Too Many Losing Trades

**Cause:** Grid spacing too tight or market trending

**Solution:**
- Increase `grid_spacing_pct` (try 2.0-2.5%)
- Increase `profit_per_grid_pct` (try 1.5-2.0%)
- Tighten chop detection (raise `chop_threshold`)

---

### Issue: Not Enough Trades

**Cause:** Grid spacing too wide

**Solution:**
- Decrease `grid_spacing_pct` (try 1.0-1.5%)
- Increase `grid_levels` (try 7-10)
- Loosen chop detection (lower `chop_threshold`)

---

### Issue: Large Drawdown

**Cause:** Too many positions, trending market

**Solution:**
- Reduce `position_size_usd`
- Reduce `max_grid_positions`
- Tighten chop detection
- Use stop losses (add to config)

---

## Advanced Features

### Custom Indicators

Add your own chop detection logic in `calculate_indicators()`:

```python
def calculate_indicators(self, df):
    # ... existing code ...

    # Add custom indicator
    df['custom_chop'] = your_indicator(df)

    return df
```

### Dynamic Grid Spacing

Adjust grid based on volatility:

```python
# In calculate_grid_levels()
atr = df['atr'].iloc[-1]  # Average True Range
dynamic_spacing = (atr / current_price) * 100

# Use dynamic spacing instead of fixed
grid_spacing = current_price * (dynamic_spacing / 100)
```

### AI-Enhanced Grid

Let AI adjust parameters based on market conditions:

```python
from src.models.model_factory import ModelFactory

model = ModelFactory.create_model('anthropic')

prompt = f"""
Market: CI={ci}, ADX={adx}, Range={range_width}%
Current grid: {grid_levels} levels, {grid_spacing_pct}% spacing

Should I adjust parameters? If yes, suggest new values.
"""

response = model.generate_response(system_prompt, prompt)
# Parse response and adjust config
```

---

## Performance Tips

### Optimize for Your Token

Different tokens need different settings:

**High Volatility (Meme Coins)**
- Wider spacing: 2.5-3.0%
- Larger profit targets: 1.5-2.0%
- Fewer levels: 3-5

**Medium Volatility (SOL, ETH)**
- Medium spacing: 1.5-2.0%
- Standard profit: 1.0-1.5%
- Medium levels: 5-7

**Low Volatility (Stablecoins, BTC)**
- Tight spacing: 0.5-1.0%
- Small profit: 0.3-0.5%
- Many levels: 7-10

### Timeframe Selection

Grid trading works best on certain timeframes:

- **15m**: Best for most tokens (default)
- **1H**: Slower, fewer trades, larger moves
- **5m**: Faster, more trades, requires more capital

Edit in `run_grid_cycle()`:
```python
df = self.get_market_data(token_address, timeframe='15m', days_back=3)
```

### Backtesting Multiple Tokens

Test which tokens work best for grid:

```bash
# Create test script
for token in BTC ETH SOL DOGE; do
    python GridChop_BT.py --token $token
done
```

Tokens with high win rates (>65%) are good candidates.

---

## FAQ

**Q: How much capital do I need?**
A: Minimum = grid_levels × position_size_usd × 2.
For default config: 5 × $50 × 2 = $500

**Q: Can I run multiple tokens?**
A: Yes! Run separate agent instances or add to MONITORED_TOKENS

**Q: What win rate should I expect?**
A: 60-75% is typical for well-configured grids in choppy markets

**Q: Does this work in bull/bear markets?**
A: No. Grid trading requires choppy/sideways markets. It will close positions when markets trend.

**Q: Can I manually close positions?**
A: Yes, but the agent will re-open them if price returns to grid levels

**Q: How often does it trade?**
A: Depends on volatility. Could be 5-20 trades per day in choppy conditions

**Q: What fees should I expect?**
A: ~0.2-0.5% per trade. Make sure profit_per_grid > fees × 2

---

## Support & Resources

- **Discord**: [discord.gg/8UPuVZ53bh](https://discord.gg/8UPuVZ53bh)
- **YouTube**: [Moon Dev's Channel](https://www.youtube.com/@moondevonyt)
- **Website**: [moondev.com](https://moondev.com)
- **GitHub**: [moondevonyt/moon-dev-ai-agents](https://github.com/moondevonyt/moon-dev-ai-agents)

---

## Disclaimer

Grid trading involves substantial risk. This bot is for **educational purposes only**.

- No guarantee of profits
- Past performance ≠ future results
- Always backtest before live trading
- Start with small position sizes
- Never risk more than you can afford to lose

**Moon Dev is not responsible for any trading losses.**

---

🌙 **Built with love by Moon Dev** 🚀

*"Code is the great equalizer"*
