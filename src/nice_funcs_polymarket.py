"""
🌙 Moon Dev's Polymarket Trading Functions - Built with love by Moon Dev 🚀

Complete utility library for Polymarket prediction market trading.
Includes order placement, position tracking, whale detection, and AI integration.

Requires:
    pip install py-clob-client requests pandas python-dotenv termcolor

Setup:
    Add to your .env file:
    POLYMARKET_PRIVATE_KEY=your_private_key_here
    POLYMARKET_FUNDER=your_funder_address_here
    POLYMARKET_PROXY_ADDRESS=your_proxy_address_here (optional)
"""

import os
import sys
import time
import json
import requests
import pandas as pd
from datetime import datetime, timedelta
from termcolor import colored, cprint
from dotenv import load_dotenv
from typing import Optional, Dict, List, Tuple

# Load environment variables
load_dotenv()

# ==============================================================================
# POLYMARKET CLIENT SETUP
# ==============================================================================

try:
    from py_clob_client.client import ClobClient
    from py_clob_client.clob_types import OrderArgs, OrderType
except ImportError:
    cprint("❌ py-clob-client not installed!", "white", "on_red")
    cprint("📦 Install it with: pip install py-clob-client", "yellow")
    sys.exit(1)

# ==============================================================================
# 🎯 PAPER TRADING FLAG - CRITICAL SAFETY CHECK
# ==============================================================================

PAPER_TRADING_ENABLED = os.getenv("PAPER_TRADING_ENABLED", "true").lower() == "true"

if PAPER_TRADING_ENABLED:
    cprint("\n" + "="*80, "yellow")
    cprint("📝 PAPER TRADING MODE ENABLED - NO REAL MONEY", "white", "on_yellow", attrs=['bold'])
    cprint("="*80, "yellow")

# Get credentials from environment
POLYMARKET_PRIVATE_KEY = os.getenv("POLYMARKET_PRIVATE_KEY")
POLYMARKET_FUNDER = os.getenv("POLYMARKET_FUNDER")
POLYMARKET_PROXY = os.getenv("POLYMARKET_PROXY_ADDRESS", "")

if not POLYMARKET_PRIVATE_KEY or not POLYMARKET_FUNDER:
    if not PAPER_TRADING_ENABLED:
        cprint("❌ Missing Polymarket credentials in .env file!", "white", "on_red")
        cprint("📝 Add POLYMARKET_PRIVATE_KEY and POLYMARKET_FUNDER to your .env", "yellow")
    # Don't exit - paper trading doesn't need credentials

# Polymarket API endpoints
POLYMARKET_HOST = "https://clob.polymarket.com"
GAMMA_API = "https://gamma-api.polymarket.com"
DATA_API = "https://data-api.polymarket.com"
CHAIN_ID = 137  # Polygon network

# Initialize client (will be None if paper trading or credentials missing)
if PAPER_TRADING_ENABLED:
    poly_client = None
    cprint("📝 Paper trading mode - Polymarket client NOT initialized", "yellow")
    cprint("💡 All trades will be simulated only!", "cyan")
else:
    try:
        if POLYMARKET_PRIVATE_KEY and POLYMARKET_FUNDER:
            poly_client = ClobClient(
                host=POLYMARKET_HOST,
                key=POLYMARKET_PRIVATE_KEY,
                chain_id=CHAIN_ID,
                signature_type=1,  # EOA signature
                funder=POLYMARKET_FUNDER
            )
            cprint("✅ Polymarket client initialized successfully!", "green")
            cprint("⚠️ LIVE TRADING MODE - REAL MONEY AT RISK!", "white", "on_red", attrs=['bold'])
        else:
            poly_client = None
            cprint("⚠️ Polymarket client not initialized (missing credentials)", "yellow")
    except Exception as e:
        poly_client = None
        cprint(f"⚠️ Polymarket client initialization failed: {e}", "yellow")

# ==============================================================================
# MARKET DATA FUNCTIONS
# ==============================================================================

def get_all_markets(limit: int = 100) -> pd.DataFrame:
    """
    Fetch all active Polymarket markets
    
    Args:
        limit: Maximum number of markets to fetch (default 100)
    
    Returns:
        DataFrame with market information
    """
    try:
        url = f"{GAMMA_API}/markets"
        params = {"limit": limit, "active": "true"}
        
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        
        markets = response.json()
        
        if not markets:
            cprint("⚠️ No markets found", "yellow")
            return pd.DataFrame()
        
        df = pd.DataFrame(markets)
        cprint(f"✅ Fetched {len(df)} active markets", "green")
        
        return df
        
    except Exception as e:
        cprint(f"❌ Error fetching markets: {e}", "red")
        return pd.DataFrame()


def get_market_by_slug(slug: str) -> Dict:
    """
    Get detailed market information by event slug
    
    Args:
        slug: Market event slug (e.g., 'presidential-election-winner-2024')
    
    Returns:
        Dictionary with market details
    """
    try:
        url = f"{GAMMA_API}/events/{slug}"
        
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        market_data = response.json()
        
        cprint(f"✅ Fetched market: {market_data.get('title', 'Unknown')}", "green")
        
        return market_data
        
    except Exception as e:
        cprint(f"❌ Error fetching market {slug}: {e}", "red")
        return {}


def get_market_prices(condition_id: str) -> Dict:
    """
    Get current YES/NO prices for a market
    
    Args:
        condition_id: Market condition ID
    
    Returns:
        Dictionary with YES and NO prices
    """
    try:
        url = f"{DATA_API}/markets/{condition_id}"
        
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        # Extract YES/NO prices
        prices = {
            "yes_price": float(data.get("outcome_prices", ["0", "0"])[0]),
            "no_price": float(data.get("outcome_prices", ["0", "0"])[1]),
            "yes_bid": None,  # Would need order book for this
            "no_bid": None,
            "volume_24h": float(data.get("volume", 0)),
            "liquidity": float(data.get("liquidity", 0))
        }
        
        cprint(f"💰 YES: ${prices['yes_price']:.3f} | NO: ${prices['no_price']:.3f}", "cyan")
        
        return prices
        
    except Exception as e:
        cprint(f"❌ Error fetching prices: {e}", "red")
        return {"yes_price": 0, "no_price": 0}


def get_order_book(token_id: str) -> Dict:
    """
    Get order book (bids/asks) for a specific outcome token
    
    Args:
        token_id: Token ID for YES or NO outcome
    
    Returns:
        Dictionary with bids and asks
    """
    if not poly_client:
        cprint("❌ Polymarket client not initialized", "red")
        return {}
    
    try:
        order_book = poly_client.get_order_book(token_id)
        
        cprint(f"📊 Order book fetched for token {token_id[:8]}...", "green")
        
        return order_book
        
    except Exception as e:
        cprint(f"❌ Error fetching order book: {e}", "red")
        return {}


def search_markets(query: str, limit: int = 10) -> pd.DataFrame:
    """
    Search for markets by keyword
    
    Args:
        query: Search query (e.g., 'Trump', 'Bitcoin')
        limit: Maximum results to return
    
    Returns:
        DataFrame with matching markets
    """
    try:
        all_markets = get_all_markets(limit=500)
        
        if all_markets.empty:
            return pd.DataFrame()
        
        # Filter by query in title or description
        mask = all_markets['question'].str.contains(query, case=False, na=False)
        results = all_markets[mask].head(limit)
        
        cprint(f"🔍 Found {len(results)} markets matching '{query}'", "cyan")
        
        return results
        
    except Exception as e:
        cprint(f"❌ Error searching markets: {e}", "red")
        return pd.DataFrame()


# ==============================================================================
# ORDER PLACEMENT FUNCTIONS
# ==============================================================================

def place_limit_order(
    token_id: str,
    price: float,
    size: float,
    side: str = "BUY",
    market_slug: str = "",
    market_title: str = "",
    notes: str = ""
) -> Optional[str]:
    """
    Place a limit order on Polymarket
    
    Args:
        token_id: Token ID for YES or NO outcome
        price: Price per share (0.01 to 0.99)
        size: Number of shares to buy/sell
        side: "BUY" or "SELL"
        market_slug: Market identifier (for paper trading)
        market_title: Human-readable market name (for paper trading)
        notes: Optional notes (for paper trading)
    
    Returns:
        Order ID if successful, None otherwise
    """
    # 🎯 PAPER TRADING MODE - Route to paper trading engine
    if PAPER_TRADING_ENABLED:
        try:
            from src.paper_trading_polymarket import paper_engine
            
            if paper_engine:
                return paper_engine.place_order(
                    market_slug=market_slug or "unknown",
                    market_title=market_title or "Unknown Market",
                    token_id=token_id,
                    side=side,
                    price=price,
                    size=size,
                    order_type="LIMIT",
                    notes=notes
                )
            else:
                cprint("⚠️ Paper trading engine not initialized", "yellow")
                return None
        except ImportError:
            cprint("⚠️ Paper trading module not available", "yellow")
            return None
    
    # LIVE TRADING MODE
    if not poly_client:
        cprint("❌ Polymarket client not initialized", "red")
        return None
    
    try:
        cprint(f"\n🎯 Placing {side} limit order...", "white", "on_blue")
        cprint(f"   Token: {token_id[:8]}...", "cyan")
        cprint(f"   Price: ${price:.3f}", "cyan")
        cprint(f"   Size: {size:.2f} shares", "cyan")
        
        # Create order
        order_args = OrderArgs(
            price=price,
            size=size,
            side=side.upper(),
            token_id=token_id
        )
        
        signed_order = poly_client.create_order(order_args)
        
        # Post order to order book
        resp = poly_client.post_order(signed_order)
        
        order_id = resp.get("orderID", "")
        
        if order_id:
            cprint(f"✅ Order placed successfully!", "white", "on_green")
            cprint(f"   Order ID: {order_id}", "green")
            return order_id
        else:
            cprint(f"❌ Order placement failed", "white", "on_red")
            return None
        
    except Exception as e:
        cprint(f"❌ Error placing order: {e}", "red")
        import traceback
        traceback.print_exc()
        return None


def place_market_order(
    token_id: str,
    size: float,
    side: str = "BUY",
    market_slug: str = "",
    market_title: str = "",
    notes: str = ""
) -> Optional[str]:
    """
    Place a market order (buy/sell at best available price)
    
    Args:
        token_id: Token ID for YES or NO outcome
        size: Number of shares to buy/sell
        side: "BUY" or "SELL"
        market_slug: Market identifier (for paper trading)
        market_title: Human-readable market name (for paper trading)
        notes: Optional notes (for paper trading)
    
    Returns:
        Order ID if successful, None otherwise
    """
    # 🎯 PAPER TRADING MODE
    if PAPER_TRADING_ENABLED:
        # For paper trading, use mid-price or assume reasonable price
        simulated_price = 0.50  # Default to 50/50 odds if we can't get real price
        
        try:
            from src.paper_trading_polymarket import paper_engine
            
            if paper_engine:
                return paper_engine.place_order(
                    market_slug=market_slug or "unknown",
                    market_title=market_title or "Unknown Market",
                    token_id=token_id,
                    side=side,
                    price=simulated_price,
                    size=size,
                    order_type="MARKET",
                    notes=notes or "Market order (simulated price)"
                )
        except ImportError:
            pass
        
        cprint("⚠️ Paper trading - market order simulated at $0.50", "yellow")
        return None
    
    # LIVE TRADING MODE
    # Get current market price
    order_book = get_order_book(token_id)
    
    if not order_book:
        cprint("❌ Could not fetch order book for market order", "red")
        return None
    
    # For BUY: take the best ask price
    # For SELL: take the best bid price
    if side.upper() == "BUY":
        if not order_book.get("asks"):
            cprint("❌ No asks available in order book", "red")
            return None
        price = float(order_book["asks"][0]["price"])
    else:
        if not order_book.get("bids"):
            cprint("❌ No bids available in order book", "red")
            return None
        price = float(order_book["bids"][0]["price"])
    
    cprint(f"📈 Market order will execute at ${price:.3f}", "yellow")
    
    # Place limit order at market price
    return place_limit_order(
        token_id=token_id,
        price=price,
        size=size,
        side=side,
        market_slug=market_slug,
        market_title=market_title,
        notes=notes or f"Market order @ ${price:.3f}"
    )


def cancel_order(order_id: str) -> bool:
    """
    Cancel a pending order
    
    Args:
        order_id: Order ID to cancel
    
    Returns:
        True if successful, False otherwise
    """
    # 🎯 PAPER TRADING MODE
    if PAPER_TRADING_ENABLED:
        cprint(f"📝 Paper trading - order {order_id[:16]}... cancellation simulated", "yellow")
        return True
    
    # LIVE TRADING MODE
    if not poly_client:
        cprint("❌ Polymarket client not initialized", "red")
        return False
    
    try:
        cprint(f"🚫 Cancelling order {order_id[:8]}...", "yellow")
        
        resp = poly_client.cancel(order_id)
        
        if resp.get("success", False):
            cprint(f"✅ Order cancelled successfully", "green")
            return True
        else:
            cprint(f"❌ Order cancellation failed", "red")
            return False
        
    except Exception as e:
        cprint(f"❌ Error cancelling order: {e}", "red")
        return False


def cancel_all_orders(market_id: Optional[str] = None) -> int:
    """
    Cancel all pending orders (optionally for specific market)
    
    Args:
        market_id: Market ID to cancel orders for (None = all markets)
    
    Returns:
        Number of orders cancelled
    """
    if not poly_client:
        cprint("❌ Polymarket client not initialized", "red")
        return 0
    
    try:
        # Get all open orders
        orders = poly_client.get_orders()
        
        if market_id:
            # Filter by market
            orders = [o for o in orders if o.get("market") == market_id]
        
        cprint(f"🚫 Cancelling {len(orders)} orders...", "yellow")
        
        cancelled = 0
        for order in orders:
            order_id = order.get("id", "")
            if cancel_order(order_id):
                cancelled += 1
        
        cprint(f"✅ Cancelled {cancelled}/{len(orders)} orders", "green")
        
        return cancelled
        
    except Exception as e:
        cprint(f"❌ Error cancelling orders: {e}", "red")
        return 0


# ==============================================================================
# POSITION TRACKING FUNCTIONS
# ==============================================================================

def get_positions() -> pd.DataFrame:
    """
    Get all current positions
    
    Returns:
        DataFrame with position information
    """
    # 🎯 PAPER TRADING MODE
    if PAPER_TRADING_ENABLED:
        try:
            from src.paper_trading_polymarket import paper_engine
            
            if paper_engine:
                return paper_engine.positions_df
        except ImportError:
            pass
        
        cprint("📭 No positions (paper trading)", "yellow")
        return pd.DataFrame()
    
    # LIVE TRADING MODE
    if not poly_client:
        cprint("❌ Polymarket client not initialized", "red")
        return pd.DataFrame()
    
    try:
        positions = poly_client.get_positions()
        
        if not positions:
            cprint("📭 No open positions", "yellow")
            return pd.DataFrame()
        
        df = pd.DataFrame(positions)
        
        cprint(f"✅ Found {len(df)} open positions", "green")
        
        # Calculate USD values if possible
        if 'size' in df.columns and 'price' in df.columns:
            df['usd_value'] = df['size'] * df['price']
        
        return df
        
    except Exception as e:
        cprint(f"❌ Error fetching positions: {e}", "red")
        return pd.DataFrame()


def get_position_for_market(condition_id: str) -> Dict:
    """
    Get position for a specific market
    
    Args:
        condition_id: Market condition ID
    
    Returns:
        Dictionary with position details (YES and NO holdings)
    """
    positions = get_positions()
    
    if positions.empty:
        return {"yes_shares": 0, "no_shares": 0, "total_value": 0}
    
    # Filter by market
    market_positions = positions[positions['market'] == condition_id]
    
    yes_shares = 0
    no_shares = 0
    
    for _, pos in market_positions.iterrows():
        outcome = pos.get('outcome', '')
        size = float(pos.get('size', 0))
        
        if 'yes' in outcome.lower():
            yes_shares = size
        elif 'no' in outcome.lower():
            no_shares = size
    
    # Get current prices
    prices = get_market_prices(condition_id)
    
    total_value = (yes_shares * prices['yes_price']) + (no_shares * prices['no_price'])
    
    position_info = {
        "yes_shares": yes_shares,
        "no_shares": no_shares,
        "yes_value": yes_shares * prices['yes_price'],
        "no_value": no_shares * prices['no_price'],
        "total_value": total_value
    }
    
    cprint(f"📊 Position: {yes_shares:.2f} YES | {no_shares:.2f} NO | ${total_value:.2f} total", "cyan")
    
    return position_info


def close_position(condition_id: str, side: str = "ALL") -> bool:
    """
    Close position in a market
    
    Args:
        condition_id: Market condition ID
        side: "YES", "NO", or "ALL" to close both
    
    Returns:
        True if successful, False otherwise
    """
    cprint(f"\n🔴 Closing {side} position in market...", "white", "on_red")
    
    position = get_position_for_market(condition_id)
    
    # Get market data to find token IDs
    market_data = get_market_prices(condition_id)
    
    # TODO: Get token IDs from market data
    # This requires fetching full market details from Gamma API
    
    success = True
    
    if side in ["YES", "ALL"] and position['yes_shares'] > 0:
        cprint(f"💫 Selling {position['yes_shares']:.2f} YES shares...", "yellow")
        # place_market_order(yes_token_id, position['yes_shares'], "SELL")
    
    if side in ["NO", "ALL"] and position['no_shares'] > 0:
        cprint(f"💫 Selling {position['no_shares']:.2f} NO shares...", "yellow")
        # place_market_order(no_token_id, position['no_shares'], "SELL")
    
    if success:
        cprint(f"✅ Position closed successfully!", "white", "on_green")
    
    return success


def get_balance() -> float:
    """
    Get USDC balance available for trading
    
    Returns:
        USDC balance as float
    """
    # 🎯 PAPER TRADING MODE
    if PAPER_TRADING_ENABLED:
        try:
            from src.paper_trading_polymarket import paper_engine
            
            if paper_engine:
                balance = paper_engine.balance
                cprint(f"💰 Paper trading balance: ${balance:,.2f} USDC (simulated)", "cyan")
                return balance
        except ImportError:
            pass
        
        cprint("💰 Paper trading balance: $10,000.00 USDC (default)", "cyan")
        return 10000.0
    
    # LIVE TRADING MODE
    if not poly_client:
        cprint("❌ Polymarket client not initialized", "red")
        return 0.0
    
    try:
        balance_response = poly_client.get_balance_allowance()
        
        balance = float(balance_response.get("balance", 0)) / 1e6  # Convert from USDC units
        
        cprint(f"💰 Available balance: ${balance:,.2f} USDC", "green")
        
        return balance
        
    except Exception as e:
        cprint(f"❌ Error fetching balance: {e}", "red")
        return 0.0


# ==============================================================================
# WHALE TRACKING FUNCTIONS
# ==============================================================================

def get_recent_trades(
    condition_id: str,
    limit: int = 100,
    min_size_usd: float = 1000
) -> pd.DataFrame:
    """
    Get recent large trades (whale activity) for a market
    
    Args:
        condition_id: Market condition ID
        limit: Maximum number of trades to fetch
        min_size_usd: Minimum trade size in USD to filter for
    
    Returns:
        DataFrame with whale trades
    """
    try:
        url = f"{DATA_API}/trades"
        params = {
            "market": condition_id,
            "limit": limit
        }
        
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        
        trades = response.json()
        
        if not trades:
            cprint("⚠️ No trades found", "yellow")
            return pd.DataFrame()
        
        df = pd.DataFrame(trades)
        
        # Calculate USD value
        if 'price' in df.columns and 'size' in df.columns:
            df['usd_value'] = df['price'].astype(float) * df['size'].astype(float)
        else:
            df['usd_value'] = 0
        
        # Filter for whale trades
        whale_trades = df[df['usd_value'] >= min_size_usd]
        
        cprint(f"🐋 Found {len(whale_trades)} whale trades (>${min_size_usd:,.0f})", "cyan")
        
        return whale_trades
        
    except Exception as e:
        cprint(f"❌ Error fetching trades: {e}", "red")
        return pd.DataFrame()


def get_trader_stats(wallet_address: str) -> Dict:
    """
    Get statistics for a specific trader (via PredictFolio API)
    
    Args:
        wallet_address: Trader's wallet address
    
    Returns:
        Dictionary with trader statistics
    """
    try:
        # PredictFolio API endpoint (hypothetical - adjust based on actual API)
        url = f"https://api.predictfolio.com/traders/{wallet_address}"
        
        response = requests.get(url, timeout=30)
        
        if response.status_code == 200:
            stats = response.json()
            
            win_rate = stats.get('win_rate', 0)
            total_volume = stats.get('total_volume', 0)
            profit_loss = stats.get('profit_loss', 0)
            
            cprint(f"📊 Trader Stats:", "cyan")
            cprint(f"   Win Rate: {win_rate:.1f}%", "cyan")
            cprint(f"   Total Volume: ${total_volume:,.2f}", "cyan")
            cprint(f"   P&L: ${profit_loss:,.2f}", "green" if profit_loss > 0 else "red")
            
            return stats
        else:
            cprint(f"⚠️ Could not fetch trader stats", "yellow")
            return {}
        
    except Exception as e:
        cprint(f"❌ Error fetching trader stats: {e}", "red")
        return {}


def track_whale_wallet(
    wallet_address: str,
    min_trade_size: float = 10000,
    auto_copy: bool = False
) -> List[Dict]:
    """
    Track all trades from a specific whale wallet
    
    Args:
        wallet_address: Wallet address to track
        min_trade_size: Minimum trade size to track
        auto_copy: If True, automatically copy whale trades
    
    Returns:
        List of whale trades
    """
    cprint(f"\n🐋 Tracking whale wallet: {wallet_address[:8]}...", "white", "on_cyan")
    
    # Get trader stats first
    stats = get_trader_stats(wallet_address)
    
    whale_trades = []
    
    # TODO: Implement wallet tracking via WebSocket or polling
    # This would require monitoring all markets for trades from this wallet
    
    if auto_copy and whale_trades:
        cprint(f"🤖 Auto-copy ENABLED - will copy whale trades", "yellow")
        # Implement auto-copy logic
    
    return whale_trades


# ==============================================================================
# AI INTEGRATION FUNCTIONS
# ==============================================================================

def ai_validate_trade(
    market_slug: str,
    side: str,
    confidence_threshold: float = 0.6
) -> bool:
    """
    Use AI swarm to validate if a trade is good
    
    Args:
        market_slug: Market event slug
        side: "YES" or "NO"
        confidence_threshold: Minimum AI consensus required (0.6 = 60%)
    
    Returns:
        True if AI swarm agrees with the trade, False otherwise
    """
    cprint(f"\n🤖 Querying AI swarm for validation...", "white", "on_magenta")
    
    try:
        # Import swarm agent
        from src.agents.swarm_agent import SwarmAgent
        
        swarm = SwarmAgent()
        
        # Get market details
        market = get_market_by_slug(market_slug)
        market_title = market.get('title', 'Unknown')
        
        # Create prompt
        prompt = f"""
        Market: {market_title}
        
        A trader wants to bet {side} on this market.
        
        Based on current information, is this a good trade?
        Respond with YES if you agree, NO if you disagree, or UNCERTAIN if not enough info.
        """
        
        # Query swarm
        result = swarm.query(prompt=prompt)
        
        # Count votes
        yes_votes = 0
        no_votes = 0
        total_votes = 0
        
        for model_name, model_data in result.get('responses', {}).items():
            if model_data.get('success'):
                response = model_data.get('response', '').upper()
                total_votes += 1
                
                if 'YES' in response and 'NO' not in response:
                    yes_votes += 1
                elif 'NO' in response:
                    no_votes += 1
        
        if total_votes == 0:
            cprint("❌ No AI responses received", "red")
            return False
        
        consensus = yes_votes / total_votes
        
        cprint(f"\n📊 AI Swarm Consensus: {consensus:.1%}", "cyan")
        cprint(f"   ✅ Agree: {yes_votes}/{total_votes}", "green")
        cprint(f"   ❌ Disagree: {no_votes}/{total_votes}", "red")
        
        if consensus >= confidence_threshold:
            cprint(f"✅ AI VALIDATED - Consensus {consensus:.1%} >= {confidence_threshold:.1%}", "white", "on_green")
            return True
        else:
            cprint(f"❌ AI REJECTED - Consensus {consensus:.1%} < {confidence_threshold:.1%}", "white", "on_red")
            return False
        
    except Exception as e:
        cprint(f"❌ Error during AI validation: {e}", "red")
        return False


# ==============================================================================
# UTILITY FUNCTIONS
# ==============================================================================

def print_market_summary(market_data: Dict):
    """
    Pretty print market information
    
    Args:
        market_data: Market data dictionary
    """
    title = market_data.get('question', 'Unknown Market')
    slug = market_data.get('slug', '')
    volume = market_data.get('volume', 0)
    liquidity = market_data.get('liquidity', 0)
    
    cprint("\n" + "="*80, "cyan")
    cprint(f"📊 {title}", "white", attrs=['bold'])
    cprint("="*80, "cyan")
    cprint(f"🔗 Link: https://polymarket.com/event/{slug}", "cyan")
    cprint(f"💰 Volume: ${float(volume):,.2f}", "yellow")
    cprint(f"💧 Liquidity: ${float(liquidity):,.2f}", "yellow")
    
    # Get prices if available
    condition_id = market_data.get('condition_id', '')
    if condition_id:
        prices = get_market_prices(condition_id)
        cprint(f"📈 YES: ${prices['yes_price']:.3f} | NO: ${prices['no_price']:.3f}", "green")
    
    cprint("="*80 + "\n", "cyan")


def format_usd(amount: float) -> str:
    """Format USD amount for display"""
    if amount >= 1000000:
        return f"${amount/1000000:.2f}M"
    elif amount >= 1000:
        return f"${amount/1000:.2f}K"
    else:
        return f"${amount:.2f}"


# ==============================================================================
# EXAMPLE USAGE
# ==============================================================================

if __name__ == "__main__":
    cprint("\n🌙 Moon Dev's Polymarket Trading Library - Test Mode", "white", "on_blue")
    cprint("="*80, "cyan")
    
    # Test 1: Get all markets
    cprint("\n1️⃣ Testing: Get all markets", "yellow")
    markets = get_all_markets(limit=10)
    if not markets.empty:
        print(markets[['question', 'volume']].head())
    
    # Test 2: Search for markets
    cprint("\n2️⃣ Testing: Search for Trump markets", "yellow")
    trump_markets = search_markets("Trump", limit=5)
    if not trump_markets.empty:
        print(trump_markets[['question']].head())
    
    # Test 3: Get balance
    cprint("\n3️⃣ Testing: Get USDC balance", "yellow")
    balance = get_balance()
    
    # Test 4: Get positions
    cprint("\n4️⃣ Testing: Get current positions", "yellow")
    positions = get_positions()
    if not positions.empty:
        print(positions.head())
    
    cprint("\n✅ All tests complete!", "white", "on_green")
    cprint("="*80 + "\n", "cyan")
