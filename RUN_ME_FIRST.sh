#!/bin/bash

# 🌙 Moon Dev's Polymarket Paper Trading - Quick Setup
# Run this script to get started with paper trading

echo ""
echo "================================================================================"
echo "🌙 Moon Dev's Polymarket Paper Trading - Setup Script"
echo "================================================================================"
echo ""

# Check if we're in the right directory
if [ ! -f "src/nice_funcs_polymarket.py" ]; then
    echo "❌ Error: Please run this script from the moon-dev-ai-agents directory"
    exit 1
fi

echo "✅ Step 1: Checking Python installation..."
python3 --version || { echo "❌ Python not found! Please install Python 3.10+"; exit 1; }

echo ""
echo "✅ Step 2: Installing dependencies..."
pip install py-clob-client websocket-client requests pandas termcolor python-dotenv

echo ""
echo "✅ Step 3: Setting up .env file..."
if ! grep -q "PAPER_TRADING_ENABLED" .env 2>/dev/null; then
    echo "" >> .env
    echo "# Polymarket Paper Trading" >> .env
    echo "PAPER_TRADING_ENABLED=true" >> .env
    echo "PAPER_STARTING_BALANCE=10000" >> .env
    echo "WHALE_AUTO_COPY=false" >> .env
    echo "WHALE_MIN_TRADE_SIZE=10000" >> .env
    echo "WHALE_MIN_WIN_RATE=60" >> .env
    echo "✅ Added paper trading settings to .env"
else
    echo "✅ Paper trading already configured in .env"
fi

echo ""
echo "✅ Step 4: Creating data directories..."
mkdir -p src/data/polymarket_whales
mkdir -p src/data/polymarket_paper_trading

echo ""
echo "================================================================================"
echo "🎉 Setup Complete! Now you can:"
echo "================================================================================"
echo ""
echo "1. Test paper trading:"
echo "   python src/paper_trading_polymarket.py"
echo ""
echo "2. Track whale trades:"
echo "   python src/agents/whale_tracker_polymarket.py"
echo ""
echo "3. Run AI market analyzer:"
echo "   python src/agents/polymarket_websearch_agent.py"
echo ""
echo "📖 For detailed docs, see: QUICK_START_POLYMARKET.md"
echo ""
echo "⚠️  REMEMBER: This is PAPER TRADING ONLY - NO REAL MONEY"
echo ""
echo "================================================================================"
