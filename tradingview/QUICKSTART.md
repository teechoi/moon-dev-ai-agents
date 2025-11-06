# 🌙 TradingView Grid Trading - Quick Start

Get grid trading signals in **5 minutes**!

---

## 📱 Setup in 3 Steps

### **Step 1: Copy the Code** (30 seconds)

1. Go to [TradingView.com](https://www.tradingview.com)
2. Open any chart (BTC, ETH, SOL, etc.)
3. Click **"Pine Editor"** at bottom of screen
4. Copy ALL code from: `grid_chop_indicator.pine`
5. Paste into Pine Editor
6. Click **"Save"** then **"Add to Chart"**

✅ **Done!** You should see grid lines and a dashboard.

---

### **Step 2: Configure** (2 minutes)

Click the ⚙️ gear icon next to "🌙 Grid Chop Trading":

**Copy these settings:**
```
Grid Levels: 5
Grid Spacing %: 1.5
Profit Target %: 1.0
───────────────────────
Chop Threshold: 61.8
ADX Threshold: 25
Range Lookback: 20
Min Range Width %: 2.0
───────────────────────
✅ Show Grid Lines
✅ Show Range
✅ Show Signals
✅ Show Dashboard
```

Click **"OK"**

---

### **Step 3: Set Alerts** (2 minutes)

1. Click the 🔔 bell icon on the indicator name
2. **Condition:** Choose "Grid Buy Signal"
3. **Frequency:** "Once Per Bar Close"
4. **Expiration:** "Never"
5. **Notifications:** ✅ Email, ✅ App
6. **Message:**
   ```
   🟢 BUY SIGNAL at {{close}}
   Target profit: +1.0%
   ```
7. Click **"Create"**

Repeat for:
- "Grid Sell Signal"
- "Choppy Market Started"

✅ **Done!** You'll get alerts when signals appear.

---

## 📊 What You'll See

### **When Market is CHOPPY** (good for grid)

```
Dashboard shows: ACTIVE 🟢

Chart shows:
─────── Sell 3 (red line)
─────── Sell 2 (red line)
─────── Sell 1 (red line)
        [Blue Range Box]
─────── Buy 1 (green line)
─────── Buy 2 (green line)
─────── Buy 3 (green line)
```

**Background:** Light green tint

---

### **When Market is TRENDING** (bad for grid)

```
Dashboard shows: INACTIVE 🔴

Chart shows:
No grid lines
Background: Light red tint
```

**Action:** Don't trade! Wait for choppy conditions.

---

## 🎯 How to Trade

### **Manual Trading**

1. **Wait for "CHOP" marker** 🔵
   - Means: Market became choppy, grid active

2. **Buy when you see** 🟢
   - Green triangle with "BUY" text
   - Buy at that price

3. **Sell for profit when** 🔴
   - Price rises 1% (or your profit target)
   - Or when you see red triangle "SELL"

4. **Exit all when "TREND" marker** 🟠
   - Means: Market trending, close positions

### **With Alerts**

1. Set up all 4 alert types (above)
2. Wait for notifications
3. Execute manually when alerted
4. Track profit/loss in spreadsheet

### **Fully Automated** (Advanced)

Use webhook alerts to trigger your bot:
- See `tradingview/README.md` "Integration" section
- Requires webhook endpoint + coding

---

## ⚙️ Quick Settings Guide

### **Too Many Signals?**
```
Increase:
  Grid Spacing: 2.0-2.5%
  Chop Threshold: 65-68
  Min Range: 3.0-4.0%
```

### **Too Few Signals?**
```
Decrease:
  Grid Spacing: 1.0-1.2%
  Chop Threshold: 55-58
  Min Range: 1.5%
  ADX Threshold: 30
```

### **Losing Too Much?**
```
Increase:
  Profit Target: 1.5-2.0%
  Grid Spacing: 2.0%
  Chop Threshold: 65

Decrease:
  Grid Levels: 3
```

### **Not Enough Profit?**
```
Increase:
  Grid Levels: 7-10
  Profit Target: 1.5-2.0%

Decrease:
  Grid Spacing: 1.0%
```

---

## 📱 Mobile Setup

### **TradingView Mobile App**

1. Install TradingView app
2. Open chart
3. Tap chart → "Indicators"
4. Search "Grid Chop" (if published)
5. Or use web version and sync

### **Alerts on Phone**

1. Enable TradingView notifications in phone settings
2. Create alerts as above
3. Receive push notifications
4. Execute trades from exchange app

---

## 🎓 Understanding Signals

### **Dashboard Indicators**

```
Chop Index: 64.2
```
- **> 61.8 (green)** = Choppy market ✅
- **< 61.8 (red)** = Trending market ❌

```
ADX: 18.3
```
- **< 25 (green)** = Weak trend ✅
- **> 25 (red)** = Strong trend ❌

```
Range Width: 3.45%
```
- **> 2.0% (green)** = Sufficient range ✅
- **< 2.0% (red)** = Range too narrow ❌

### **When All 3 are Green**
✅ Grid trading is ACTIVE
✅ Safe to take signals
✅ Market conditions ideal

### **When Any is Red**
❌ Grid trading INACTIVE
❌ Don't take signals
❌ Wait for conditions to improve

---

## 🔔 Alert Messages Explained

### **"🌊 CHOPPY MARKET DETECTED!"**
```
Meaning: Grid conditions met
Action: Prepare to trade grid signals
Note: Watch for buy/sell signals
```

### **"🟢 GRID BUY SIGNAL at $0.1215"**
```
Meaning: Price hit buy level
Action: Enter long position at ~$0.1215
Target: Sell at $0.1227 (+1%)
```

### **"🔴 GRID SELL SIGNAL at $0.1253"**
```
Meaning: Price hit sell level OR take profit
Action: Close long OR enter short
Target: Buy back at $0.1240 (-1%)
```

### **"📈 TRENDING MARKET!"**
```
Meaning: Market no longer choppy
Action: Close ALL grid positions
Note: Wait for next choppy period
```

---

## 📊 Backtest First!

Before trading with real money:

1. Use the **Strategy version**: `grid_chop_strategy.pine`
2. Add to chart (same as indicator)
3. Look at "Strategy Tester" tab
4. Check these metrics:

```
✅ Net Profit: > 0%
✅ Win Rate: > 60%
✅ Max Drawdown: < 10%
✅ Total Trades: > 50
```

5. **Only trade live if all ✅**

---

## ⚠️ Common Mistakes

### ❌ **Trading During Trends**
Dashboard shows "INACTIVE" but you trade anyway.
→ **Result:** Losses pile up

**Solution:** Only trade when "ACTIVE"

### ❌ **Ignoring Take Profits**
Hit +1% profit but hold for more.
→ **Result:** Profit turns to loss

**Solution:** Stick to profit target

### ❌ **Too Many Grid Levels**
Using 10 levels with small account.
→ **Result:** Overexposed, large drawdown

**Solution:** Start with 3-5 levels

### ❌ **Wrong Timeframe**
Using 1-minute chart with default settings.
→ **Result:** Too many false signals

**Solution:** Use 15m or 1H

### ❌ **No Stop Loss**
Never exiting losing positions.
→ **Result:** One bad trade wipes account

**Solution:** Exit when "TREND" marker appears

---

## 💰 Position Sizing

### **Conservative** (Recommended for beginners)
```
Account: $1,000
Risk per grid: 2%
Max grids: 5

Per trade: $20
Max exposure: $100 (10% of account)
```

### **Moderate**
```
Account: $5,000
Risk per grid: 3%
Max grids: 7

Per trade: $150
Max exposure: $1,050 (21% of account)
```

### **Aggressive** (Experienced only)
```
Account: $10,000
Risk per grid: 5%
Max grids: 10

Per trade: $500
Max exposure: $5,000 (50% of account)
```

**Formula:**
```
Per Trade = Account × Risk % ÷ Grid Levels
```

---

## 🎯 Best Tokens for Grid Trading

### ✅ **Good Candidates**
- Tokens with clear support/resistance
- Moderate volatility (5-15% daily)
- High liquidity
- Frequent consolidation periods

**Examples:**
- BTC in sideways markets
- ETH during accumulation
- SOL in range
- Large-cap altcoins

### ❌ **Bad Candidates**
- Very low volatility (<2% daily)
- Extreme volatility (>30% daily)
- Low liquidity
- Constantly trending up or down

**Examples:**
- Stablecoins (USDC, USDT)
- Dead coins
- Brand new meme coins
- Coins with major news

---

## 📈 Expected Results

### **Realistic Expectations**

**Good Day (Choppy Market):**
```
Trades: 3-8 signals
Win Rate: 70%
Profit: +2-5%
```

**Bad Day (Trending Market):**
```
Trades: 0-1 signals
Win Rate: 30%
Profit: -1% to 0%
```

**Weekly Average:**
```
Choppy days: 3-4 out of 7
Total signals: 15-30
Win rate: 65%
Weekly return: +3-8%
```

### **Not Normal** (Check Settings)

**Too Good:**
```
Win rate: 90%+
→ Backtest longer period
→ Verify settings
```

**Too Bad:**
```
Win rate: <50%
→ Widen grid spacing
→ Increase profit target
→ Try different token
```

---

## 🆘 Quick Troubleshooting

| Problem | Quick Fix |
|---------|-----------|
| No signals appearing | Lower chop threshold to 55 |
| Too many signals | Raise chop threshold to 68 |
| Grid not activating | Lower min range to 1.5% |
| Grid lines not showing | Enable in settings ⚙️ |
| Alerts not working | Recreate with "Once Per Bar Close" |
| Bad performance | Try different token or timeframe |
| Dashboard not showing | Enable "Show Dashboard" |
| Losing money | Increase grid spacing to 2.5% |

---

## 📚 Next Steps

1. ✅ **Add indicator to chart**
2. ✅ **Backtest with strategy version**
3. ✅ **Set up alerts**
4. ✅ **Paper trade for 1 week**
5. ✅ **Start with small position sizes**
6. ✅ **Track performance**
7. ✅ **Gradually increase size if profitable**

---

## 🔗 More Resources

- **Complete Guide:** `tradingview/README.md` (40+ pages)
- **Python Bot:** `src/agents/grid_agent.py`
- **Strategy Docs:** `docs/grid_trading_bot.md`
- **Discord:** discord.gg/8UPuVZ53bh

---

## ⚠️ Final Reminder

```
🌊 Grid trading ONLY works in CHOPPY markets

📈 It FAILS in strong trends

⚠️ ALWAYS check dashboard shows "ACTIVE" before trading

💰 Start small and scale gradually

📊 Backtest before live trading
```

---

🌙 **Happy Grid Trading!** 🚀

*Built by Moon Dev - "Code is the great equalizer"*

---

**Questions?** Join Discord: discord.gg/8UPuVZ53bh
