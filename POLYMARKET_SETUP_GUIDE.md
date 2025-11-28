# 🌙 Moon Dev's Polymarket Paper Trading Setup Guide

**⚠️ PAPER TRADING ONLY - NO REAL MONEY ⚠️**

This guide will help you set up **simulation-only** trading on Polymarket. Perfect for testing strategies, tracking whale trades, and validating AI predictions **without risking real money**.

---

## 📋 **What You Built**

You now have a complete Polymarket trading system with:

1. **`nice_funcs_polymarket.py`** - Trading utilities library
   - Market data fetching
   - Order placement (limit & market orders)
   - Position tracking
   - Whale trade detection
   - AI validation integration

2. **`whale_tracker_polymarket.py`** - Whale copy bot
   - Real-time whale trade tracking ($10k+ trades)
   - Trader win rate analysis (via PredictFolio)
   - AI swarm validation before copying
   - Auto-copy feature (PAPER MODE)

3. **`paper_trading_polymarket.py`** - Paper trading engine
   - Simulates all trades without real money
   - Tracks hypothetical P&L
   - Position management
   - Performance analytics

---

## 🚀 **Quick Start (Paper Trading)**

### **Step 1: Install Dependencies**

```bash
cd /Users/vamshi/poly/moon-dev-ai-agents

# Install Polymarket trading library
pip install py-clob-client websocket-client

# Verify installation
python -c "import py_clob_client; print('✅ py-clob-client installed')"
```

### **Step 2: Configure Your Credentials**

Copy your API credentials to `.env` file:

```bash
# Add to your existing .env file
cat >> .env << 'EOF'

# ============================================================================
# POLYMARKET CREDENTIALS
# ============================================================================

# API Credentials
POLYMARKET_API_KEY=019ac936-6b23-78e1-9260-d41eecf92560
POLYMARKET_SECRET=pD5w4plBOp7260BR_N0UVwX_5CVFFrD_pDZxvTKO9IE=
POLYMARKET_PASSPHRASE=9d8cf64c002c8c648b58e0ede16ee5dd93d2206deabb22763096af7e9e3d7e9e

# Builder Address
POLYMARKET_BUILDER_ADDRESS=0x8decf989f8e55bc01d1a3e4290869e7b32baaf13

# For py-clob-client (you'll need to export private key from your wallet)
POLYMARKET_PRIVATE_KEY=YOUR_PRIVATE_KEY_HERE
POLYMARKET_FUNDER=0x8decf989f8e55bc01d1a3e4290869e7b32baaf13

# ⚠️ TRADING MODE
POLYMARKET_TRADING_MODE=PAPER  # NEVER change this to LIVE!

# Paper Trading Settings
PAPER_TRADING_ENABLED=true
PAPER_STARTING_BALANCE=10000  # Start with $10k simulated USDC
PAPER_TRACK_PERFORMANCE=true

# Whale Tracker Settings
WHALE_MIN_TRADE_SIZE=10000
WHALE_MIN_WIN_RATE=60
WHALE_AUTO_COPY=false  # Set true to enable auto-copy (PAPER ONLY)
WHALE_COPY_PERCENTAGE=10
WHALE_MAX_POSITION=100

# AI Validation
AI_CONSENSUS_THRESHOLD=0.70

EOF
```

### **Step 3: Test Paper Trading Engine**

```bash
# Test the paper trading engine
python src/paper_trading_polymarket.py
```

**Expected output:**
```
📝 PAPER TRADING MODE - SIMULATION ONLY
⚠️  NO REAL MONEY WILL BE USED
💰 Starting Balance: $10,000.00 USDC (simulated)
💵 Current Balance: $10,000.00 USDC (simulated)
📊 Total Trades: 0
📈 Open Positions: 0

1️⃣ Simulating BUY order
📝 PAPER TRADE SIMULATED
   Trade ID: PAPER_20251128_123456
   Market: Will Trump win 2024 election?
   Side: BUY
   Price: $0.650
   Size: 100.00 shares
   Value: $65.00
✅ Paper trade recorded! New balance: $9,935.00

[continues with more test trades...]

📊 PAPER TRADING PERFORMANCE (SIMULATED)
💰 Starting Balance: $10,000.00
💵 Current Balance:  $10,010.00
📈 Total Return:     +0.10%
✅ Paper trading test complete!
```

### **Step 4: Test Whale Tracker (Read-Only Mode)**

```bash
# Run whale tracker in read-only mode
# This will track whale trades but NOT copy them
python src/agents/whale_tracker_polymarket.py
```

**Expected output:**
```
🐋 Moon Dev's Polymarket Whale Tracker - Initializing
💰 Minimum whale trade size: $10.0K
🎯 Minimum whale win rate: 60%
🤖 AI consensus required: 70%
🔄 Auto-copy: ❌ DISABLED
✨ Initialization complete!

🔌 WebSocket connected!
📡 Sending subscription for live trades...
✅ Subscription sent! Waiting for whale trades...

🐋 WHALE TRADE DETECTED!
   Market: Will Bitcoin hit $100k by end of 2024?
   Wallet: 0x742d35Cc...
   Side: YES
   Size: $15.2K
   ⚠️ Low win rate: 45.0%

[Continues tracking whale trades in real-time...]
```

---

## 📚 **Documentation Resources**

### **Existing Polymarket Docs in Your Repo:**

1. **`docs/polymarket_agent.md`** - AI swarm analysis agent
   - How to analyze markets with AI
   - Consensus picks
   - WebSocket data collection

2. **`docs/polymarket_agents.md`** - Dr. Data Dawg's roadmap
   - 4 core projects
   - Market discovery system
   - Future features

### **Official Polymarket Documentation:**

Since you asked about docs, here are the key resources:

| Resource | URL | Purpose |
|----------|-----|---------|
| **CLOB API Docs** | https://docs.polymarket.com/developers/CLOB/orders | Order placement, cancellation |
| **Gamma API Docs** | https://docs.polymarket.com/developers/gamma-markets-api | Market data, events |
| **py-clob-client** | https://github.com/Polymarket/py-clob-client | Python trading library |
| **WebSocket Docs** | https://docs.polymarket.com/developers/CLOB/websocket | Real-time trade feed |
| **Data API Docs** | https://docs.polymarket.com/developers/data-api | Historical trades, prices |

---

## 🎯 **Features You Can Use RIGHT NOW (Paper Trading)**

### **1. Track Whale Trades**

```bash
# Just watch what whales are doing
# NO trading, just observation
python src/agents/whale_tracker_polymarket.py
```

This will:
- ✅ Track all $10k+ trades in real-time
- ✅ Identify trader win rates (if available)
- ✅ Save whale activity to CSV
- ❌ NOT execute any trades

### **2. Analyze Markets with AI Swarm**

```bash
# Use existing AI swarm agent
python src/agents/polymarket_websearch_agent.py
```

This will:
- ✅ Track live market activity
- ✅ Get 6-model AI consensus predictions
- ✅ Identify top 5 markets with strongest agreement
- ✅ Search web for market context
- ❌ NOT execute any trades

### **3. Simulate Whale Copy Trading**

To enable auto-copy in **PAPER MODE ONLY**:

1. Edit `.env`:
   ```bash
   WHALE_AUTO_COPY=true  # Enable auto-copy simulation
   ```

2. Run whale tracker:
   ```bash
   python src/agents/whale_tracker_polymarket.py
   ```

This will:
- ✅ Detect high-quality whale trades
- ✅ Validate with AI swarm
- ✅ Simulate copying in paper trading engine
- ✅ Track hypothetical P&L
- ❌ NOT execute real trades

---

## 📊 **Understanding Your Data**

All paper trading data is saved to CSV files:

```
src/data/polymarket_whales/
├── whale_trades.csv         # All $10k+ trades tracked
├── whale_wallets.csv         # Known whale wallets + stats
└── copy_signals.csv          # AI-validated copy opportunities

src/data/polymarket_paper_trading/
├── paper_trades.csv          # All simulated trades
├── paper_positions.csv       # Open simulated positions
└── paper_balance.csv         # Balance history over time
```

### **Example: Analyzing Your Paper Trading Performance**

```python
import pandas as pd

# Load your paper trades
df = pd.read_csv('src/data/polymarket_paper_trading/paper_trades.csv')

# Calculate win rate
closed = df[df['status'] == 'CLOSED']
wins = closed[closed['pnl'] > 0]
win_rate = len(wins) / len(closed) * 100

print(f"Win Rate: {win_rate:.1f}%")
print(f"Total P&L: ${closed['pnl'].sum():.2f}")
print(f"Best Trade: ${closed['pnl'].max():.2f}")
print(f"Worst Trade: ${closed['pnl'].min():.2f}")
```

---

## ⚠️ **CRITICAL: Real Trading Safety**

### **Why We're NOT Setting Up Real Trading:**

1. **You Need a Private Key** - The credentials you provided are API keys, but `py-clob-client` requires your wallet's private key (different from API key)

2. **Testnet Doesn't Exist** - Polymarket operates on **Polygon mainnet only**. There is **NO testnet** for Polymarket. The only way to test is paper trading.

3. **Real Money Risk** - Any trades on mainnet use **real USDC** on Polygon. One mistake = real money lost.

### **If You Want Real Trading Later:**

**Step 1:** Export your private key from MetaMask
```
MetaMask → Account Details → Export Private Key → Enter password
⚠️ NEVER share this with anyone!
```

**Step 2:** Add to `.env` (VERY carefully)
```bash
POLYMARKET_PRIVATE_KEY=0x...your...private...key...here
```

**Step 3:** Change trading mode
```bash
POLYMARKET_TRADING_MODE=LIVE  # ⚠️ USE REAL MONEY
PAPER_TRADING_ENABLED=false
```

**Step 4:** Start with TINY positions
```bash
WHALE_MAX_POSITION=5  # Only risk $5 per trade
WHALE_COPY_PERCENTAGE=1  # Only copy 1% of whale size
```

**BUT I STRONGLY RECOMMEND:** Test in paper trading for at least 1-2 weeks first!

---

## 🚀 **Next Steps (Recommended Order)**

### **Week 1: Observation & Data Collection**
```bash
# Run whale tracker in read-only mode
python src/agents/whale_tracker_polymarket.py

# Run AI swarm analyzer
python src/agents/polymarket_websearch_agent.py
```

**Goals:**
- ✅ Collect 100+ whale trades
- ✅ Identify 10+ high win-rate wallets
- ✅ Get 20+ AI consensus predictions

### **Week 2: Paper Trading Validation**
```bash
# Enable auto-copy in paper mode
# Edit .env: WHALE_AUTO_COPY=true

python src/agents/whale_tracker_polymarket.py
```

**Goals:**
- ✅ Simulate copying 20+ whale trades
- ✅ Track paper trading P&L
- ✅ Validate AI predictions vs outcomes
- ✅ Calculate win rate & profitability

### **Week 3: Strategy Refinement**
```bash
# Analyze paper trading results
python -c "
import pandas as pd
from src.paper_trading_polymarket import PaperTradingEngine

engine = PaperTradingEngine()
engine.print_performance()
"
```

**Goals:**
- ✅ Identify best-performing whales
- ✅ Test different AI consensus thresholds
- ✅ Optimize position sizing
- ✅ Refine entry/exit rules

### **Week 4: Live Trading (Optional - if paper trading is profitable)**

**Only proceed if:**
- ✅ Paper trading win rate > 55%
- ✅ Paper trading total return > 10%
- ✅ You understand all risks
- ✅ You've exported your private key safely

---

## 🛠️ **Troubleshooting**

### **"ModuleNotFoundError: No module named 'py_clob_client'"**
```bash
pip install py-clob-client
```

### **"WebSocket connection failed"**
- Check internet connection
- Polymarket WebSocket URL may be down (wait and retry)

### **"AI swarm timeout"**
- Some AI models (Gemini) can be slow
- Agent continues with partial results - this is expected

### **"No whale trades detected"**
- Whale activity varies by day/time
- Try lowering `WHALE_MIN_TRADE_SIZE` to $5000
- Check that WebSocket is connected

### **Network Error (like the one you got earlier)**
```
Error: 500 Post "https://api.anthropic.com/v1/messages?beta=true": 
dial tcp: lookup api.anthropic.com: no such host
```

**Cause:** Internet connection issue or DNS problem

**Fix:**
1. Check internet connection
2. Try different WiFi/network
3. Temporarily disable VPN if using one
4. Clear DNS cache: `sudo dscacheutil -flushcache`

---

## 📞 **Support & Resources**

- **Moon Dev Discord:** https://discord.gg/8UPuVZ53bh
- **Polymarket Docs:** https://docs.polymarket.com
- **Polymarket Discord:** Check their website for link
- **This Repo Issues:** Open an issue on GitHub

---

## ✅ **Summary: What You Have Now**

| Feature | Status | Notes |
|---------|--------|-------|
| Market Data Fetching | ✅ Ready | Via Gamma API |
| Whale Trade Tracking | ✅ Ready | WebSocket + CSV logging |
| AI Swarm Validation | ✅ Ready | 6-model consensus |
| Paper Trading Engine | ✅ Ready | Full P&L tracking |
| Whale Copy Bot | ✅ Ready | Paper trading mode only |
| Real Trading | ❌ Not Setup | Requires private key + LIVE mode |
| PredictFolio Integration | ⚠️ Partial | API endpoint assumed (may need adjustment) |

---

## 🎯 **Your Immediate Action Plan:**

```bash
# 1. Test paper trading
python src/paper_trading_polymarket.py

# 2. Run whale tracker (read-only)
python src/agents/whale_tracker_polymarket.py

# 3. Run AI analyzer
python src/agents/polymarket_websearch_agent.py

# 4. After 1 week, analyze results
python -c "
from src.paper_trading_polymarket import PaperTradingEngine
engine = PaperTradingEngine()
engine.print_performance()
"
```

**Goal:** Collect data for 1-2 weeks before considering real trading.

---

**Built with ❤️ by Moon Dev**

**⚠️ REMEMBER: This is PAPER TRADING ONLY - NO REAL MONEY! ⚠️**
