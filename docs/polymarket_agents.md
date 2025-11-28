# Polymarket AI Agents - Roadmap

Dr. Data Dawg's master plan for intelligent Polymarket trading agents. Building on the proven strategies from the existing bot infrastructure and the AI agent framework from moon-dev-ai-agents-for-trading.

---

## 📋 Project Status

| Project | Status | Progress |
|---------|--------|----------|
| **Paper Trading System** | ✅ Complete | Zero-risk simulation engine with P&L tracking |
| **Whale Tracker & Auto-Copy** | ✅ Complete | Real-time $10k+ trade detection with AI validation |
| **Data Collection System** | ✅ Complete | 11,862 markets in database, real-time monitor active |
| **Sweep Quality Scorer** | 🔜 Next | Ready to build on existing sweep infrastructure |
| **Event Catalyst Agent** | 📝 Planned | Waiting for data foundation |
| **Resolution Probability Recalibrator** | 📝 Planned | Waiting for data foundation |

---

## 🚀 Quick Start

### **New to Polymarket Trading? Start Here!**

```bash
# 1. One-click setup (installs dependencies, configures paper trading)
./RUN_ME_FIRST.sh

# 2. Test paper trading engine
python src/paper_trading_polymarket.py

# 3. Track whale trades (real-time $10k+ trades)
python src/agents/whale_tracker_polymarket.py

# 4. Sync with Moon Dev's latest updates
./SYNC_WITH_MOONDEV.sh
```

### **📖 Documentation:**
- **[Quick Start Guide](QUICK_START_POLYMARKET.md)** - Get running in 5 minutes
- **[Complete Setup Guide](POLYMARKET_SETUP_GUIDE.md)** - Full documentation
- **[Paper Trading Summary](POLYMARKET_PAPER_TRADING_SUMMARY.md)** - System overview
- **[Git Workflow](GIT_WORKFLOW.md)** - Stay synced with Moon Dev

---

## 🎯 Four Core Projects

### 1. Event Catalyst Agent
**Concept:** Real-time information arbitrage. Monitors breaking news/events and instantly scans for related Polymarket markets before the crowd reacts.

**How it works:**
- Monitor news APIs, Twitter/X, Reddit for breaking events
- Match keywords/entities to Polymarket event slugs
- Use sentiment analysis to gauge directional bias
- Check if market odds are stale vs. new information
- Enter position if edge detected

**Existing Assets to Leverage:**
```
/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/agents/sentiment_agent.py
/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/agents/tweet_agent.py
/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/agents/research_agent.py
```

**What to build:**
- News → Polymarket market matcher (keyword/entity extraction)
- Event impact scorer (how much should this move the odds?)
- Integration with existing Polymarket order execution

---

### 2. Resolution Probability Recalibrator Agent
**Concept:** AI-powered price prediction. Estimate the TRUE probability of market resolution vs. current market odds. If there's a significant delta, that's edge.

**How it works:**
- Scrape market description, current odds, resolution criteria
- Feed to 6-model swarm (Claude 4.5, GPT-5, Gemini 2.5, Grok-4, DeepSeek, DeepSeek-R1)
- Each model estimates: "What's the REAL probability this resolves YES?"
- Aggregate responses (average, weighted consensus, outlier removal)
- Compare swarm estimate vs. market odds
- Trade if delta > threshold (e.g., swarm says 70%, market at 55% = 15% edge)

**Existing Assets to Leverage:**
```
/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/agents/swarm_agent.py
/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/agents/base_agent.py
```

**What to build:**
- Market data scraper (descriptions, odds, volume, recent activity)
- Swarm prompt engineering (standardized probability estimation format)
- Consensus algorithm (how to aggregate 6 model outputs)
- Position sizing based on edge size and model agreement
- Continuous monitoring (re-estimate as new info emerges)

**Future enhancements:**
- Add ML models (logistic regression, XGBoost, neural nets)
- Historical calibration (track swarm accuracy over time, adjust weights)
- Market-specific models (political markets vs. entertainment vs. crypto)

---

### 3. Sweep Quality Scorer Agent
**Concept:** Not all sweeps are equal. Score each sweep/cluster based on wallet quality, market type, timing, size, and historical win rate. Only follow the highest-quality signals.

**How it works:**
- Detect sweep (already done via `sweeper_mini.py`)
- Score the sweep on multiple dimensions:
  - **Wallet quality:** Historical win rate, total volume, market selection
  - **Market type:** Political > entertainment > sports (adjustable)
  - **Timing:** High-liquidity hours, proximity to expiration, news events
  - **Relative size:** $10k on $50k market = huge; on $5M market = noise
  - **Outcome bias:** Does this wallet win more on YES or NO?
- Aggregate score (0-10 scale)
- Only alert/trade if score > threshold (e.g., 7/10)
- Optional: Use swarm to validate the sweep (ask AI: "Is this a smart move?")

**Existing Assets to Leverage:**
```
/Users/md/Dropbox/dev/github/Polymarket-Trading-Bots/course/sweeper_mini.py
/Users/md/Dropbox/dev/github/Polymarket-Trading-Bots/course/todays_clusters.py
/Users/md/Dropbox/dev/github/Polymarket-Trading-Bots/data/sweeps_database.csv
```

**What to build:**
- Wallet performance tracker (win rate, P&L, market history)
- Scoring algorithm with configurable weights
- Real-time sweep quality dashboard
- Auto-execution for high-quality sweeps (optional)
- Historical backtesting (would this scoring system have improved performance?)

**Order Book Strategy:**
- Instead of market buying after a sweep, use swarm to estimate fair price
- Place limit orders at swarm consensus price
- Sit on order book and wait for fill (better entry than chasing)

---

### 4. Data Collection System - Market Discovery ✅ COMPLETE
**Concept:** Before we can trade markets, we need to KNOW about all markets. Build a comprehensive data collection system that discovers, tracks, and stores all Polymarket markets.

**Status: ✅ IMPLEMENTED**

**What We Built:**

**1. `fetch_all_markets.py` - Complete Market Database**
- Fetches ALL active markets via Polymarket Gamma API (`https://gamma-api.polymarket.com/markets`)
- Automatic pagination (handles 11,862+ markets across 119+ batches)
- Saves to CSV: `data/polymarket_markets.csv`
- Extracts all critical trading data:
  - `market_id`, `slug`, `condition_id` - unique identifiers
  - `clob_token_ids` - YES/NO token addresses for trading
  - `question`, `description` - for AI analysis
  - `outcome_prices` - current market odds
  - `volume_24h`, `volume_total`, `liquidity` - market activity
  - `category`, `end_date` - for filtering and strategy
  - `url` - direct Polymarket links

**2. `market_monitor.py` - Real-Time New Market Detection**
- Monitors API every 30 seconds for new markets
- Compares against existing CSV database
- Prints new markets to terminal (sweeper_mini style with colors)
- Auto-appends new markets to CSV database
- Configurable filters (sports, crypto, minimum volume)

**Current Database Stats (October 2025):**
- 📊 **11,862** active markets
- 💰 **$90M** daily volume
- 💵 **$2.3B** all-time volume
- 🔥 Top market: NYC mayoral ($12.3M/day)

**Database Schema (CSV):**
```
market_id, slug, condition_id, question, category, end_date,
outcomes (Yes|No), outcome_prices (0.65|0.35), clob_token_ids,
volume_24h, volume_total, liquidity, url, image, description,
market_maker_address, created_at, updated_at, last_fetched
```

**Files Created:**
- `fetch_all_markets.py` - Bulk market fetcher
- `market_monitor.py` - Real-time new market monitor
- `data/polymarket_markets.csv` - Complete market database (15MB, 11,862 markets)
- `MARKET_DISCOVERY_README.md` - Full documentation

**Usage:**
```bash
# Initial database setup (one-time)
python fetch_all_markets.py

# Real-time monitoring (leave running)
python market_monitor.py

# Refresh database (run daily)
python fetch_all_markets.py
```

**Key Integration Points:**
- All market data ready for Event Catalyst (match news → markets)
- Market questions/descriptions ready for Recalibrator (feed to AI swarm)
- Market metadata ready for Sweep Quality Scorer (enrich sweep data)
- Full market universe for any strategy

---

---

## 🛡️ Paper Trading System ✅ COMPLETE

**Concept:** Practice trading strategies with ZERO RISK. All trades are simulated - no real money involved.

**Status: ✅ IMPLEMENTED**

**What We Built:**

### **1. Paper Trading Engine (`src/paper_trading_polymarket.py`)**
- Complete simulation environment (starts with $10,000 virtual USDC)
- Order execution simulation (market & limit orders)
- Position tracking with P&L calculation
- Balance management and trade history
- Performance analytics (win rate, avg win/loss, total return)
- CSV logging for all activity

### **2. Whale Tracker with Auto-Copy (`src/agents/whale_tracker_polymarket.py`)**
- Real-time WebSocket monitoring of Polymarket trades
- Detects large trades ($10k+ configurable threshold)
- Tracks trader performance via PredictFolio API
- AI swarm validation (6-model consensus before copying)
- Auto-copy feature (paper mode safe - simulated only)
- Comprehensive logging (whale_trades.csv, whale_wallets.csv, copy_signals.csv)

### **3. Trading Utilities Library (`src/nice_funcs_polymarket.py`)**
- Market data fetching (Gamma API, Data API)
- Order placement functions (respects PAPER_TRADING_ENABLED flag)
- Trader analytics integration
- AI validation integration
- Safety checks throughout

### **4. Setup & Sync Scripts**
- **`RUN_ME_FIRST.sh`** - One-click dependency installation and .env setup
- **`SYNC_WITH_MOONDEV.sh`** - Automated sync with Moon Dev's original repo

**Safety Features:**
- ✅ `PAPER_TRADING_ENABLED=true` by default (env variable controls everything)
- ✅ Every order function checks flag before executing
- ✅ Real Polymarket client **never initialized** in paper mode
- ✅ Visual warnings throughout (yellow banners for paper mode)
- ✅ **ZERO RISK** of placing real trades

**Files Created:**
- `src/paper_trading_polymarket.py` - Paper trading engine (500+ lines)
- `src/agents/whale_tracker_polymarket.py` - Whale tracker bot (600+ lines)
- `src/nice_funcs_polymarket.py` - Trading utilities (1,045 lines)
- `docs/QUICK_START_POLYMARKET.md` - Quick start guide
- `docs/POLYMARKET_SETUP_GUIDE.md` - Complete documentation
- `docs/POLYMARKET_PAPER_TRADING_SUMMARY.md` - System overview
- `docs/GIT_WORKFLOW.md` - Git workflow guide
- `RUN_ME_FIRST.sh` - Setup script
- `SYNC_WITH_MOONDEV.sh` - Repo sync script

**Usage:**
```bash
# Quick start
./RUN_ME_FIRST.sh

# Test paper trading
python src/paper_trading_polymarket.py

# Track whales (observation mode - no copying)
WHALE_AUTO_COPY=false python src/agents/whale_tracker_polymarket.py

# Enable whale auto-copy (paper mode safe)
WHALE_AUTO_COPY=true python src/agents/whale_tracker_polymarket.py

# Sync with Moon Dev's updates
./SYNC_WITH_MOONDEV.sh
```

**Output Files:**
```
src/data/polymarket_whales/
├── whale_trades.csv      # All $10k+ trades detected
├── whale_wallets.csv     # Whale wallet stats (win rate, P&L)
└── copy_signals.csv      # AI-validated copy opportunities

src/data/polymarket_paper_trading/
├── paper_trades.csv      # All simulated trades
├── paper_positions.csv   # Open positions
└── paper_balance.csv     # Balance history
```

**Key Integration Points:**
- AI swarm validation before every trade (6-model consensus)
- Trader performance tracking (PredictFolio API)
- WebSocket real-time monitoring (Polymarket stream)
- Ready for live trading (just change PAPER_TRADING_ENABLED=false)

---

## 🔄 Staying Synced with Moon Dev

### **Automated Sync Script**

Use `SYNC_WITH_MOONDEV.sh` to stay up-to-date with Moon Dev's original repo:

```bash
# Run this weekly or when Moon Dev announces updates
./SYNC_WITH_MOONDEV.sh
```

**What it does:**
1. ✅ Fetches latest from `moondevonyt/moon-dev-ai-agents`
2. ✅ Shows you what's new (commits and file changes)
3. ✅ Asks before merging
4. ✅ Handles merge conflicts gracefully
5. ✅ Asks before pushing to your fork

**Manual sync (if you prefer):**
```bash
# 1. Fetch from Moon Dev
git fetch upstream

# 2. See what's new
git log --oneline main..upstream/main

# 3. Merge updates
git merge upstream/main

# 4. Push to your fork
git push origin main
```

**See also:** [Git Workflow Guide](GIT_WORKFLOW.md)

---

## 🚀 Implementation Priority

1. ✅ **Paper Trading System** - COMPLETE (zero-risk simulation)
2. ✅ **Whale Tracker** - COMPLETE (real-time detection with AI validation)
3. ✅ **Data Collection System** - COMPLETE (11,862 markets in database)
4. 🔜 **Sweep Quality Scorer** (next up - builds on existing sweeper infrastructure)
5. 📝 **Event Catalyst Agent** (high potential - information arbitrage is powerful)
6. 📝 **Resolution Probability Recalibrator** (most complex - requires prompt engineering and calibration)

---

## 📊 Success Metrics

**Per Agent:**
- Win rate (% of trades that are profitable)
- Average edge captured (difference between entry and exit)
- Sharpe ratio (risk-adjusted returns)
- Max drawdown
- Trade frequency (opportunities per day)

**Aggregate:**
- Total P&L across all agents
- Capital efficiency (return per dollar deployed)
- Latency (time from signal to execution)
- False positive rate (bad signals filtered out)

---

## 🛠️ Tech Stack

**Existing Infrastructure:**
- Python 3.10+
- Pandas (data manipulation)
- Polymarket API/smart contracts
- CSV databases (sweeps, positions, trades)

**AI Framework:**
- Claude 4.5, GPT-5, Gemini 2.5, Grok-4, DeepSeek, DeepSeek-R1
- Swarm consensus voting
- BaseAgent architecture (from moon-dev-ai-agents-for-trading)

**Data Sources:**
- Polymarket API (markets, order book, trades)
- Twitter/X API (breaking news, sentiment)
- Reddit API (community sentiment)
- News APIs (headlines, events)
- On-chain data (whale wallets, sweep detection)

---

## 📝 Notes

- All agents should log decisions (why did we trade? what was the signal?)
- Extensive backtesting before live deployment
- Start with small position sizes, scale up as confidence increases
- Filter out sports markets (gambling > smart money)
- Filter out major crypto price predictions (too much noise)
- Focus on political, policy, and unique event markets (higher edge potential)

---

Built by Dr. Data Dawg 🐕
Let's get this alpha 💰
