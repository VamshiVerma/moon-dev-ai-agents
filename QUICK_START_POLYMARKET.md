# 🚀 QUICK START - Polymarket Paper Trading

**⚠️ PAPER TRADING ONLY - NO REAL MONEY ⚠️**

## 📝 TL;DR - Run This Right Now

```bash
# 1. Make sure you're in the right directory
cd /Users/vamshi/poly/moon-dev-ai-agents

# 2. Install dependencies (one time only)
pip install py-clob-client websocket-client

# 3. Add paper trading flag to your .env
echo "PAPER_TRADING_ENABLED=true" >> .env

# 4. Test the paper trading engine
python src/paper_trading_polymarket.py

# 5. Track whale trades (read-only)
python src/agents/whale_tracker_polymarket.py
```

---

## ✅ What Just Happened?

### **Step 1: Test Paper Trading**
When you ran `python src/paper_trading_polymarket.py`:
- ✅ Created a simulated account with $10,000 USDC
- ✅ Simulated 3 test trades
- ✅ Calculated P&L
- ✅ Saved everything to CSV files

**Output files:**
```
src/data/polymarket_paper_trading/
├── paper_trades.csv      # All your simulated trades
├── paper_positions.csv   # Open positions
└── paper_balance.csv     # Balance history
```

### **Step 2: Track Whales**
When you ran `python src/agents/whale_tracker_polymarket.py`:
- ✅ Connected to Polymarket WebSocket
- ✅ Tracking $10k+ trades in real-time
- ✅ Identifying whale wallets
- ❌ NOT placing any trades (just watching)

**Output files:**
```
src/data/polymarket_whales/
├── whale_trades.csv      # All $10k+ trades detected
├── whale_wallets.csv     # Whale wallet stats
└── copy_signals.csv      # AI-validated copy opportunities
```

---

## 🎯 Key Environment Variables

### **In your `.env` file:**

```bash
# CRITICAL - This controls everything
PAPER_TRADING_ENABLED=true    # NEVER change this to false!

# Optional - For auto-copying whales (in paper mode)
WHALE_AUTO_COPY=false         # Set to true to enable whale copying
WHALE_MIN_TRADE_SIZE=10000    # Track trades over $10k
WHALE_MIN_WIN_RATE=60         # Only copy whales with >60% win rate
WHALE_MAX_POSITION=100        # Max $100 per trade
WHALE_COPY_PERCENTAGE=10      # Copy 10% of whale size

# AI Settings
AI_CONSENSUS_THRESHOLD=0.70   # Require 70% AI agreement
```

---

## 🔄 Enable Whale Auto-Copy (Paper Trading)

Want to simulate copying whale trades?

### **Step 1: Enable auto-copy**
```bash
# Edit .env file
echo "WHALE_AUTO_COPY=true" >> .env
```

### **Step 2: Run whale tracker**
```bash
python src/agents/whale_tracker_polymarket.py
```

### **What happens:**
1. ✅ Detects whale trades ($10k+)
2. ✅ Checks whale win rate (must be >60%)
3. ✅ Asks AI swarm if trade is good
4. ✅ Simulates copying in paper trading engine
5. ✅ Tracks your hypothetical P&L

---

## 📊 Check Your Paper Trading Performance

```bash
# Run this anytime to see your stats
python -c "
from src.paper_trading_polymarket import PaperTradingEngine
engine = PaperTradingEngine()
engine.print_performance()
"
```

**Output:**
```
📊 PAPER TRADING PERFORMANCE (SIMULATED)
💰 Starting Balance: $10,000.00
💵 Current Balance:  $10,150.00
📈 Total Return:     +1.50%
💸 Total P&L:        $+150.00

📊 Total Trades:     12
✅ Winning Trades:   8
❌ Losing Trades:    4
🎯 Win Rate:         66.7%
💚 Avg Win:          $35.00
💔 Avg Loss:         $-18.75

📂 Open Positions:   2
```

---

## 🛡️ Safety Checks Built In

### **Every function checks the PAPER_TRADING flag:**

| Function | Paper Mode | Live Mode |
|----------|------------|-----------|
| `place_limit_order()` | ✅ Routes to paper trading engine | ⚠️ Places real order |
| `place_market_order()` | ✅ Routes to paper trading engine | ⚠️ Places real order |
| `cancel_order()` | ✅ Simulates cancellation | ⚠️ Cancels real order |
| `get_balance()` | ✅ Returns paper balance ($10k) | ⚠️ Returns real USDC balance |
| `get_positions()` | ✅ Returns paper positions | ⚠️ Returns real positions |

### **Visual indicators:**

```bash
# When PAPER_TRADING_ENABLED=true, you'll see:
================================================================================
📝 PAPER TRADING MODE - NO REAL MONEY
⚠️  All trades will be SIMULATED ONLY
================================================================================

# If you ever set PAPER_TRADING_ENABLED=false, you'll see:
================================================================================
⚠️ LIVE TRADING MODE - REAL MONEY AT RISK!
================================================================================
```

---

## 🎓 Learning Path

### **Week 1: Data Collection**
```bash
# Just observe whale trades
WHALE_AUTO_COPY=false
python src/agents/whale_tracker_polymarket.py

# Let it run for a few days
# Review whale_trades.csv and whale_wallets.csv
```

### **Week 2: Paper Trading**
```bash
# Enable auto-copy in paper mode
WHALE_AUTO_COPY=true
python src/agents/whale_tracker_polymarket.py

# Let it run and track performance
python -c "from src.paper_trading_polymarket import PaperTradingEngine; PaperTradingEngine().print_performance()"
```

### **Week 3: Analysis**
```python
import pandas as pd

# Load whale trades
whales = pd.read_csv('src/data/polymarket_whales/whale_trades.csv')

# Find best whales
whales[whales['trader_win_rate'] > 70].groupby('wallet_address').size()

# Load your paper trades
trades = pd.read_csv('src/data/polymarket_paper_trading/paper_trades.csv')

# Calculate your win rate
closed = trades[trades['status'] == 'CLOSED']
win_rate = len(closed[closed['pnl'] > 0]) / len(closed) * 100
print(f"Your win rate: {win_rate:.1f}%")
```

### **Week 4: Decision Time**
- ✅ If paper trading profitable: Consider testing with tiny amounts ($5)
- ❌ If paper trading unprofitable: Refine strategy, stay in paper mode

---

## ⚠️ How to Switch to Live Trading (NOT RECOMMENDED)

**DON'T DO THIS unless you:**
1. ✅ Tested in paper mode for 2+ weeks
2. ✅ Have >55% win rate in paper trading
3. ✅ Have >10% total return in paper trading
4. ✅ Exported your private key from MetaMask
5. ✅ Understand you could lose real money

**If you still want to:**
```bash
# 1. Add private key to .env (DANGEROUS)
POLYMARKET_PRIVATE_KEY=0x...your...private...key...
POLYMARKET_FUNDER=0x8decf989f8e55bc01d1a3e4290869e7b32baaf13

# 2. Disable paper trading (DANGER!)
PAPER_TRADING_ENABLED=false

# 3. Set TINY position sizes
WHALE_MAX_POSITION=5  # Only $5 per trade!
WHALE_COPY_PERCENTAGE=1  # Only 1% of whale size

# 4. Run with extreme caution
python src/agents/whale_tracker_polymarket.py
```

**You will see:**
```
================================================================================
⚠️ LIVE TRADING MODE - REAL MONEY AT RISK!
================================================================================
⚠️ Auto-copy mode: LIVE TRADING (REAL MONEY!)
```

---

## 🆘 Troubleshooting

### **"ModuleNotFoundError: No module named 'py_clob_client'"**
```bash
pip install py-clob-client websocket-client
```

### **"No whale trades detected"**
- Whale activity varies - be patient
- Try lowering threshold: `WHALE_MIN_TRADE_SIZE=5000`

### **"Paper trading engine not initialized"**
```bash
# Make sure this is in your .env
PAPER_TRADING_ENABLED=true
```

### **Want to reset paper trading?**
```bash
# Delete paper trading data
rm -rf src/data/polymarket_paper_trading/

# Start fresh
python src/paper_trading_polymarket.py
```

---

## 📁 File Structure

```
moon-dev-ai-agents/
├── src/
│   ├── nice_funcs_polymarket.py          # Trading library (respects PAPER flag)
│   ├── paper_trading_polymarket.py       # Paper trading engine
│   ├── agents/
│   │   ├── whale_tracker_polymarket.py   # Whale tracker (respects PAPER flag)
│   │   ├── polymarket_agent.py           # AI swarm analyzer (no trading)
│   │   └── polymarket_websearch_agent.py # AI + web search (no trading)
│   └── data/
│       ├── polymarket_whales/            # Whale tracking data
│       └── polymarket_paper_trading/     # Paper trading records
├── .env                                  # Your configuration
└── POLYMARKET_SETUP_GUIDE.md            # Full documentation
```

---

## 🎯 Summary

**You now have:**
- ✅ Complete paper trading system
- ✅ Whale tracking & auto-copy (simulated)
- ✅ AI validation before every trade
- ✅ Performance tracking & analytics
- ✅ Safety checks throughout

**What's protected:**
- ✅ Every order function checks `PAPER_TRADING_ENABLED`
- ✅ Visual warnings if trading mode changes
- ✅ All data saved to CSV for analysis
- ✅ Zero risk - no real money involved

**Your next actions:**
1. Let whale tracker run for a few days
2. Enable auto-copy in paper mode
3. Review performance after 1-2 weeks
4. Refine strategy based on results

---

**Built with ❤️ by Moon Dev**

**Remember: Paper trading is ALWAYS safer than live trading!** 🎯
