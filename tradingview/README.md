# 🌙 Moon Dev's Grid Trading - TradingView Indicators

Complete TradingView Pine Script implementation of the Grid Trading algorithm with visual signals and automated alerts.

---

## 📦 What's Included

### 1. **Grid Chop Indicator** (`grid_chop_indicator.pine`)
- Visual indicator showing grid levels and signals
- Real-time alerts for buy/sell opportunities
- Dashboard with market conditions
- Perfect for manual trading with alerts

### 2. **Grid Chop Strategy** (`grid_chop_strategy.pine`)
- Backtestable strategy version
- Automatic position management
- Performance metrics and statistics
- Perfect for validating settings before live trading

---

## 🚀 Quick Start

### **Step 1: Add to TradingView**

1. Open [TradingView.com](https://www.tradingview.com)
2. Open any chart
3. Click "Pine Editor" at the bottom
4. Copy the code from `grid_chop_indicator.pine`
5. Click "Add to Chart"

### **Step 2: Configure Settings**

Click the ⚙️ gear icon next to the indicator name:

**Recommended Settings:**
```
Grid Levels: 5
Grid Spacing %: 1.5
Profit Target %: 1.0

Chop Threshold: 61.8
ADX Threshold: 25
Range Lookback: 20
Min Range Width %: 2.0
```

### **Step 3: Set Up Alerts**

1. Click the 🔔 bell icon on the indicator
2. Choose alert condition:
   - "Choppy Market Started" - When grid conditions met
   - "Grid Buy Signal" - When price hits buy level
   - "Grid Sell Signal" - When price hits sell level
3. Set notification preferences (email, SMS, webhook)
4. Click "Create"

---

## 📊 Understanding the Visual Display

### **Dashboard (Top Right)**

```
🌙 Grid Chop | ACTIVE 🟢
─────────────────────────
Chop Index   | 64.2  ✅
ADX          | 18.3  ✅
Range Width  | 3.45% ✅
─────────────────────────
Buy Levels   | 3
Sell Levels  | 3
Grid Spacing | 1.5%
Profit Target| 1.0%
```

**What It Means:**
- **ACTIVE 🟢**: Grid trading conditions are met
- **Chop Index**: Green = choppy (good), Red = trending (bad)
- **ADX**: Green = weak trend (good), Red = strong trend (bad)
- **Range Width**: Green = sufficient range, Red = range too narrow

### **Grid Lines on Chart**

```
─────── Sell 3: $0.1291 (red dashed line)
─────── Sell 2: $0.1272 (red dashed line)
─────── Sell 1: $0.1253 (red dashed line)

        ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
        ▓  Price Range    ▓
        ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓

─────── Buy 1:  $0.1215 (green dashed line)
─────── Buy 2:  $0.1196 (green dashed line)
─────── Buy 3:  $0.1177 (green dashed line)
```

- **Green dashed lines** = Buy levels (enter long)
- **Red dashed lines** = Sell levels (enter short or take profit)
- **Blue box** = Current tradeable range
- **Background color** = Green tint when choppy, red when trending

### **Signal Markers**

- **🟢 Green triangle up** = BUY signal (price hit grid level)
- **🔴 Red triangle down** = SELL signal (price hit grid level)
- **🔵 Blue circle "CHOP"** = Market became choppy (start grid trading)
- **🟠 Orange circle "TREND"** = Market trending (exit grid positions)

---

## ⚙️ Configuration Guide

### **Grid Settings**

#### Grid Levels (1-10)
Number of buy/sell levels above/below current price.

- **Low (3)**: Conservative, fewer positions
- **Medium (5)**: Balanced (recommended)
- **High (7-10)**: Aggressive, more positions

**Example with 3 levels:**
```
Sell 3: +4.5%
Sell 2: +3.0%
Sell 1: +1.5%
─────────────
Buy 1:  -1.5%
Buy 2:  -3.0%
Buy 3:  -4.5%
```

#### Grid Spacing % (0.5-5.0)
Distance between each grid level.

- **Tight (1.0%)**: More frequent trades, smaller profits
- **Medium (1.5%)**: Balanced (recommended)
- **Wide (2.5%+)**: Fewer trades, larger profits

**Formula:**
```
Level spacing = Current Price × (Grid Spacing % / 100)
```

#### Profit Target % (0.1-5.0)
Expected profit from each grid trade.

- **Small (0.5-1.0%)**: Quick exits, high win rate
- **Medium (1.0-1.5%)**: Balanced (recommended)
- **Large (2.0%+)**: Patient exits, higher profit per trade

**Note:** Profit target should be > trading fees (typically 0.2-0.5%)

### **Market Detection Settings**

#### Chop Threshold (50-100)
Choppiness Index threshold for detecting sideways markets.

- **Default: 61.8** (Fibonacci level)
- **Lower (55-60)**: More lenient, trades more often
- **Higher (65-70)**: Stricter, only very choppy markets

**How it works:**
```
CI > 61.8  →  Choppy market ✅ (good for grid)
CI < 61.8  →  Trending market ❌ (exit grid)
```

#### ADX Threshold (10-50)
Threshold for trend strength detection.

- **Default: 25**
- **Lower (20-23)**: Stricter, only very weak trends
- **Higher (27-30)**: More lenient, includes moderate trends

**How it works:**
```
ADX < 25  →  Weak trend ✅ (good for grid)
ADX > 25  →  Strong trend ❌ (exit grid)
```

#### Range Lookback (10-50)
Number of bars to calculate price range.

- **Short (10-15)**: Adapts quickly to new ranges
- **Medium (20)**: Balanced (recommended)
- **Long (30-50)**: More stable, slower to adapt

#### Min Range Width % (0.5-10.0)
Minimum range width required to enable grid.

- **Default: 2.0%**
- Prevents trading in extremely tight ranges
- Should be larger than (Grid Spacing × Grid Levels)

**Example:**
```
Grid: 5 levels × 1.5% spacing = 7.5% total range needed
Min Range: 2.0% is insufficient
Min Range: 8.0% would work better
```

### **Alert Settings**

Enable/disable different alert types:

- ✅ **Alert on Choppy Market**: Notifies when grid conditions met
- ✅ **Alert on Trending Market**: Notifies when to exit positions
- ✅ **Alert on Buy Signal**: Notifies at each buy opportunity
- ✅ **Alert on Sell Signal**: Notifies at each sell opportunity

**Recommended:** Enable all alerts, then filter based on your preference.

### **Visual Settings**

- ✅ **Show Grid Lines**: Display buy/sell levels on chart
- ✅ **Show Range**: Display tradeable range box
- ✅ **Show Signals**: Display buy/sell markers
- ✅ **Show Dashboard**: Display metrics table

**Tip:** Disable visuals if chart looks too cluttered.

---

## 📈 Using the Strategy Version

The **Strategy** version allows you to backtest and see performance metrics.

### **Step 1: Add Strategy**

1. Open Pine Editor
2. Copy code from `grid_chop_strategy.pine`
3. Click "Add to Chart"

### **Step 2: View Performance**

Look at the "Strategy Tester" tab (bottom of screen):

```
Net Profit: $1,234 (12.34%)
Win Rate: 68.4%
Profit Factor: 1.82
Max Drawdown: -3.21%
Total Trades: 247
```

**Good Strategy Indicators:**
- ✅ Net Profit > 0
- ✅ Win Rate > 60%
- ✅ Profit Factor > 1.5
- ✅ Max Drawdown < 10%

### **Step 3: Optimize Settings**

Use TradingView's optimizer to find best parameters:

1. Click ⚙️ on strategy
2. Click "Optimization" tab
3. Select parameters to optimize:
   - Grid Levels (3, 5, 7)
   - Grid Spacing (1.0, 1.5, 2.0)
   - Profit Target (0.8, 1.0, 1.5)
4. Click "Optimize"

TradingView will test all combinations and show the best performer.

### **Strategy-Specific Settings**

**Risk Management:**
```
Max Grid Positions: 10       - Maximum concurrent trades
Position Size %: 10          - % of equity per trade
Use Stop Loss: false         - Enable stop loss protection
Stop Loss %: 3.0             - Stop loss percentage
```

**Position Size Example:**
```
Account: $10,000
Position Size: 10%
Per Trade: $1,000

With 5 grid levels filled:
Total Exposure: $5,000 (50% of account)
```

---

## 🎯 Best Practices

### **1. Start with Conservative Settings**

```
Grid Levels: 3
Grid Spacing: 1.5%
Profit Target: 1.0%
Position Size: 5% (strategy only)
```

Test for 1 week before increasing risk.

### **2. Match Settings to Token Volatility**

**High Volatility (Meme Coins, New Tokens):**
```
Grid Spacing: 2.5-3.0%
Profit Target: 1.5-2.0%
Grid Levels: 3-5
```

**Medium Volatility (SOL, ETH):**
```
Grid Spacing: 1.5-2.0%
Profit Target: 1.0-1.5%
Grid Levels: 5-7
```

**Low Volatility (BTC, Stablecoins):**
```
Grid Spacing: 0.8-1.2%
Profit Target: 0.5-0.8%
Grid Levels: 7-10
```

### **3. Use Appropriate Timeframes**

- **5m**: Fast scalping, many signals
- **15m**: Balanced (recommended)
- **1H**: Slower, fewer signals, larger moves
- **4H**: Very slow, high-quality signals

### **4. Combine with Other Indicators**

Grid trading works well alongside:
- **Volume Profile**: Identify price acceptance zones
- **Support/Resistance**: Validate range boundaries
- **RSI**: Confirm overbought/oversold at grid levels

### **5. Monitor Market Conditions**

Grid trading only works in choppy markets:

✅ **Trade When:**
- Dashboard shows "ACTIVE"
- CI > 61.8 (green)
- ADX < 25 (green)
- Range width sufficient

❌ **Don't Trade When:**
- Dashboard shows "INACTIVE"
- Strong uptrend or downtrend
- Breaking major support/resistance
- News events or high impact announcements

---

## 🔔 Setting Up Alerts

### **Method 1: Quick Alerts (Indicator)**

1. Add indicator to chart
2. Click 🔔 next to indicator name
3. Condition: Choose from dropdown
   - "Choppy Market Started"
   - "Grid Buy Signal"
   - "Grid Sell Signal"
   - "Trending Market Started"
4. Options:
   - **Frequency**: Once Per Bar Close (recommended)
   - **Expiration**: Never
5. Notifications:
   - ✅ Popup on website
   - ✅ Email
   - ✅ SMS (if enabled)
   - ✅ Webhook (for automation)
6. Create alert

### **Method 2: Webhook Alerts (Automation)**

For automated trading bots:

1. Create alert as above
2. Enable "Webhook URL"
3. Enter your webhook endpoint
4. Message format:
```json
{
  "action": "{{strategy.order.action}}",
  "ticker": "{{ticker}}",
  "price": "{{close}}",
  "signal_type": "grid_buy",
  "profit_target": "{{plot_2}}",
  "timestamp": "{{time}}"
}
```

5. Your bot receives this and executes trade

### **Alert Message Templates**

**Buy Alert:**
```
🟢 GRID BUY SIGNAL
Token: {{ticker}}
Price: {{close}}
Target: +{{plot_2}}%
CI: {{plot_0}}
ADX: {{plot_1}}
Action: Enter long position
```

**Sell Alert:**
```
🔴 GRID SELL SIGNAL
Token: {{ticker}}
Price: {{close}}
Target: +{{plot_2}}%
CI: {{plot_0}}
ADX: {{plot_1}}
Action: Take profit or enter short
```

**Choppy Market Alert:**
```
🌊 CHOPPY MARKET DETECTED
Token: {{ticker}}
Price: {{close}}
CI: {{plot_0}} (choppy if >61.8)
ADX: {{plot_1}} (weak trend if <25)
Action: Activate grid trading
```

### **Alert Best Practices**

1. **Use "Once Per Bar Close"** to avoid false signals during bar formation
2. **Set expiration to "Never"** so alerts persist
3. **Enable multiple notification methods** for redundancy
4. **Test alerts** with small positions first
5. **Monitor alert frequency** - too many alerts = settings too sensitive

---

## 🎨 Customization

### **Changing Colors**

Edit these lines in the code:

**Grid lines:**
```pine
color.new(color.green, 50)  // Buy levels - change 'green' and transparency '50'
color.new(color.red, 50)    // Sell levels
```

**Background:**
```pine
bgcolor(grid_enabled ? color.new(color.green, 95) : color.new(color.red, 95))
```

**Signal markers:**
```pine
color=color.new(color.green, 0)  // Buy signals
color=color.new(color.red, 0)    // Sell signals
```

### **Adjusting Dashboard Position**

Change table position:
```pine
table.new(position.top_right, 2, 8)  // Options: top_right, top_left, bottom_right, bottom_left
```

### **Adding Custom Metrics**

Add row to dashboard:
```pine
table.cell(dashboard, 0, 8, "My Metric", text_size=size.small)
table.cell(dashboard, 1, 8, "Value", text_size=size.small)
```

---

## 📊 Performance Analysis

### **Key Metrics to Monitor**

**From Indicator:**
- Number of buy/sell signals per day
- Win rate (track manually or use strategy)
- Average time to take profit
- Frequency of "choppy" vs "trending" periods

**From Strategy:**
- **Net Profit**: Total profit/loss
- **Win Rate**: % of profitable trades
- **Profit Factor**: Gross profit ÷ gross loss (>1.5 is good)
- **Max Drawdown**: Largest peak-to-trough decline
- **Sharpe Ratio**: Risk-adjusted returns (>1.0 is good)
- **Recovery Factor**: Net profit ÷ max drawdown

### **Good vs Bad Performance**

**Good Performance:**
```
Net Profit: +15%
Win Rate: 68%
Profit Factor: 2.1
Max Drawdown: -4.2%
Sharpe Ratio: 1.8
Total Trades: 156
```

**Bad Performance:**
```
Net Profit: -5%
Win Rate: 45%
Profit Factor: 0.8
Max Drawdown: -18%
Sharpe Ratio: 0.3
Total Trades: 89
```

If performance is bad:
1. Widen grid spacing
2. Increase profit targets
3. Reduce grid levels
4. Tighten chop detection (raise CI threshold)

---

## 🐛 Troubleshooting

### **Issue: No Signals Appearing**

**Possible Causes:**
1. Market not choppy (CI < 61.8 or ADX > 25)
2. Range too narrow (below min_range setting)
3. Wrong timeframe (try 15m or 1H)

**Solutions:**
- Lower chop_threshold to 55-58
- Raise adx_threshold to 28-30
- Lower min_range to 1.5%
- Switch to higher volatility token

### **Issue: Too Many Losing Trades**

**Possible Causes:**
1. Grid spacing too tight
2. Market trending (not choppy)
3. Profit target too large

**Solutions:**
- Increase grid_spacing to 2.0-2.5%
- Raise chop_threshold to 65-68
- Lower profit_target to 0.8-1.0%
- Use stop losses (strategy only)

### **Issue: Grid Lines Not Showing**

**Possible Causes:**
1. "Show Grid Lines" disabled
2. Too many lines (TradingView limit)
3. Grid not active (market trending)

**Solutions:**
- Enable "Show Grid Lines" in settings
- Reduce grid_levels to 3-5
- Wait for choppy market conditions

### **Issue: Alerts Not Triggering**

**Possible Causes:**
1. Alert not set to "Once Per Bar Close"
2. Alert expired
3. Condition never met

**Solutions:**
- Check alert list (🔔 icon, top right)
- Recreate alert with correct settings
- Verify market conditions met alert criteria
- Test on historical data first

### **Issue: Strategy Shows Bad Performance**

**Possible Causes:**
1. Settings not optimized for this token
2. Token too low volatility
3. Time period included strong trends

**Solutions:**
- Run TradingView optimizer
- Test on different tokens
- Filter date range to choppy periods only
- Backtest on longer timeframe (6+ months)

---

## 🔗 Integration with Moon Dev Bot

### **Using TradingView Alerts with Python Bot**

You can use TradingView alerts to trigger the Python bot:

1. **Set up webhook alert** in TradingView
2. **Point webhook** to your bot's endpoint
3. **Bot receives signal** and executes trade

**Example Webhook Handler (Python):**

```python
from flask import Flask, request
import json

app = Flask(__name__)

@app.route('/tradingview-webhook', methods=['POST'])
def webhook():
    data = request.json

    if data['signal_type'] == 'grid_buy':
        # Execute buy via grid agent
        agent.place_grid_order(token, data['price'], 'BUY')

    elif data['signal_type'] == 'grid_sell':
        # Execute sell via grid agent
        agent.place_grid_order(token, data['price'], 'SELL')

    return {'status': 'success'}

if __name__ == '__main__':
    app.run(port=5000)
```

### **Syncing Settings**

Keep TradingView and Python bot settings aligned:

**TradingView:**
```
Grid Levels: 5
Grid Spacing: 1.5%
Profit Target: 1.0%
```

**Python (`src/agents/grid_agent.py`):**
```python
GRID_CONFIG = {
    'grid_levels': 5,
    'grid_spacing_pct': 1.5,
    'profit_per_grid_pct': 1.0,
}
```

---

## 📚 Resources

### **Learning Pine Script**
- [TradingView Pine Script Docs](https://www.tradingview.com/pine-script-docs/en/v5/)
- [Pine Script Reference](https://www.tradingview.com/pine-script-reference/v5/)
- [TradingView Community Scripts](https://www.tradingview.com/scripts/)

### **Grid Trading Education**
- See `docs/grid_trading_bot.md` for complete strategy guide
- See `GRID_TRADING_README.md` for quick start
- Join Moon Dev Discord: discord.gg/8UPuVZ53bh

### **Support**
- GitHub Issues
- Moon Dev Discord
- TradingView Comments

---

## ⚠️ Disclaimers

1. **TradingView alerts are not guaranteed** - Use proper error handling
2. **Backtesting ≠ future performance** - Always paper trade first
3. **Grid trading requires choppy markets** - Doesn't work in trends
4. **Trading involves risk** - Only risk what you can afford to lose
5. **This is educational software** - No guarantees of profitability

---

## 🎯 Quick Reference

### **Indicator Files**
- `grid_chop_indicator.pine` - Visual indicator with alerts
- `grid_chop_strategy.pine` - Backtestable strategy

### **Default Settings**
```
Grid Levels: 5
Grid Spacing: 1.5%
Profit Target: 1.0%
Chop Threshold: 61.8
ADX Threshold: 25
Min Range: 2.0%
```

### **Alert Types**
- Choppy Market Started 🌊
- Trending Market Started 📈
- Grid Buy Signal 🟢
- Grid Sell Signal 🔴

### **Key Indicators**
- **CI > 61.8** = Choppy ✅
- **ADX < 25** = Weak trend ✅
- **Range > 2%** = Sufficient ✅

---

## 🌙 Built by Moon Dev

*"Code is the great equalizer"*

For questions, join the Discord: discord.gg/8UPuVZ53bh

---

**Last Updated:** January 2025
**Version:** 1.0
**Pine Script Version:** 5
