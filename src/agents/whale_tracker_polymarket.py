"""
🌙 Moon Dev's Polymarket Whale Tracker & Copy Bot
Built with love by Moon Dev 🚀

This agent:
1. Tracks large trades ($10k+) on Polymarket in real-time
2. Identifies whale wallets with high win rates (using PredictFolio)
3. Uses AI swarm to validate if whale trades are smart
4. Optionally auto-copies high-quality whale trades

Setup:
    1. Install: pip install websocket-client py-clob-client
    2. Add to .env:
       POLYMARKET_PRIVATE_KEY=...
       POLYMARKET_FUNDER=...
    3. Configure settings below
"""

import os
import sys
import time
import json
import pandas as pd
import websocket
import threading
from datetime import datetime, timedelta
from pathlib import Path
from termcolor import cprint

# Add project root to path
project_root = str(Path(__file__).parent.parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import Moon Dev's Polymarket functions
from src.nice_funcs_polymarket import (
    get_market_by_slug,
    get_market_prices,
    place_limit_order,
    place_market_order,
    ai_validate_trade,
    get_trader_stats,
    get_balance,
    format_usd,
    PAPER_TRADING_ENABLED  # Import the paper trading flag
)

# ==============================================================================
# CONFIGURATION - Customize these settings
# ==============================================================================

# Whale Detection Settings
MIN_WHALE_TRADE_SIZE = 10000  # Only track trades over $10,000
MIN_WHALE_WIN_RATE = 60  # Only copy whales with >60% win rate
MIN_AI_CONSENSUS = 0.70  # Require 70% AI agreement to copy

# Auto-Copy Settings
AUTO_COPY_ENABLED = False  # Set to True to automatically copy whale trades
MAX_POSITION_SIZE = 100  # Maximum USD to risk per trade when copying
COPY_PERCENTAGE = 10  # Copy 10% of whale's position size

# Data Paths
DATA_FOLDER = os.path.join(project_root, "src/data/polymarket_whales")
WHALE_TRADES_CSV = os.path.join(DATA_FOLDER, "whale_trades.csv")
WHALE_WALLETS_CSV = os.path.join(DATA_FOLDER, "whale_wallets.csv")
COPY_SIGNALS_CSV = os.path.join(DATA_FOLDER, "copy_signals.csv")

# WebSocket URL
WEBSOCKET_URL = "wss://ws-live-data.polymarket.com"

# ==============================================================================
# WHALE TRACKER AGENT
# ==============================================================================

class WhaleTrackerAgent:
    """Agent that tracks and optionally copies whale trades on Polymarket"""
    
    def __init__(self):
        """Initialize the Whale Tracker agent"""
        cprint("\n" + "="*80, "cyan")
        cprint("🐋 Moon Dev's Polymarket Whale Tracker - Initializing", "cyan", attrs=['bold'])
        cprint("="*80, "cyan")
        
        # Display paper trading mode prominently
        if PAPER_TRADING_ENABLED:
            cprint("\n" + "="*80, "yellow")
            cprint("📝 PAPER TRADING MODE - NO REAL MONEY", "white", "on_yellow", attrs=['bold'])
            cprint("⚠️  All trades will be SIMULATED ONLY", "white", "on_yellow", attrs=['bold'])
            cprint("="*80, "yellow")
        
        # Create data folder
        os.makedirs(DATA_FOLDER, exist_ok=True)
        
        # Thread-safe lock for CSV access
        self.csv_lock = threading.Lock()
        
        # WebSocket connection
        self.ws = None
        self.ws_connected = False
        
        # Statistics
        self.total_trades_tracked = 0
        self.whale_trades_detected = 0
        self.ai_validated_trades = 0
        self.trades_copied = 0
        
        # Load existing data
        self.whale_trades_df = self._load_whale_trades()
        self.whale_wallets_df = self._load_whale_wallets()
        self.copy_signals_df = self._load_copy_signals()
        
        cprint(f"📊 Loaded {len(self.whale_trades_df)} historical whale trades", "cyan")
        cprint(f"🐋 Tracking {len(self.whale_wallets_df)} known whale wallets", "cyan")
        cprint(f"🎯 Auto-copy: {'✅ ENABLED' if AUTO_COPY_ENABLED else '❌ DISABLED'}", "yellow")
        
        if AUTO_COPY_ENABLED and PAPER_TRADING_ENABLED:
            cprint(f"📝 Auto-copy mode: PAPER TRADING (simulated only)", "yellow")
        elif AUTO_COPY_ENABLED:
            cprint(f"⚠️ Auto-copy mode: LIVE TRADING (REAL MONEY!)", "white", "on_red", attrs=['bold'])
        
        cprint("✨ Initialization complete!\n", "green")
    
    def _load_whale_trades(self) -> pd.DataFrame:
        """Load whale trades history from CSV"""
        if os.path.exists(WHALE_TRADES_CSV):
            try:
                df = pd.read_csv(WHALE_TRADES_CSV)
                return df
            except Exception as e:
                cprint(f"⚠️ Error loading whale trades: {e}", "yellow")
        
        return pd.DataFrame(columns=[
            'timestamp', 'market_slug', 'market_title', 'wallet_address',
            'side', 'price', 'size', 'usd_value', 'trader_win_rate',
            'ai_validated', 'copied'
        ])
    
    def _load_whale_wallets(self) -> pd.DataFrame:
        """Load known whale wallets from CSV"""
        if os.path.exists(WHALE_WALLETS_CSV):
            try:
                df = pd.read_csv(WHALE_WALLETS_CSV)
                return df
            except Exception as e:
                cprint(f"⚠️ Error loading whale wallets: {e}", "yellow")
        
        return pd.DataFrame(columns=[
            'wallet_address', 'win_rate', 'total_volume', 'profit_loss',
            'first_seen', 'last_seen', 'trade_count'
        ])
    
    def _load_copy_signals(self) -> pd.DataFrame:
        """Load copy trading signals from CSV"""
        if os.path.exists(COPY_SIGNALS_CSV):
            try:
                df = pd.read_csv(COPY_SIGNALS_CSV)
                return df
            except Exception as e:
                cprint(f"⚠️ Error loading copy signals: {e}", "yellow")
        
        return pd.DataFrame(columns=[
            'timestamp', 'market_slug', 'market_title', 'whale_wallet',
            'whale_side', 'whale_size', 'our_side', 'our_size',
            'ai_consensus', 'executed', 'outcome'
        ])
    
    def _save_whale_trades(self):
        """Save whale trades to CSV"""
        try:
            with self.csv_lock:
                self.whale_trades_df.to_csv(WHALE_TRADES_CSV, index=False)
        except Exception as e:
            cprint(f"❌ Error saving whale trades: {e}", "red")
    
    def _save_whale_wallets(self):
        """Save whale wallets to CSV"""
        try:
            with self.csv_lock:
                self.whale_wallets_df.to_csv(WHALE_WALLETS_CSV, index=False)
        except Exception as e:
            cprint(f"❌ Error saving whale wallets: {e}", "red")
    
    def _save_copy_signals(self):
        """Save copy signals to CSV"""
        try:
            with self.csv_lock:
                self.copy_signals_df.to_csv(COPY_SIGNALS_CSV, index=False)
        except Exception as e:
            cprint(f"❌ Error saving copy signals: {e}", "red")
    
    def on_ws_message(self, ws, message):
        """Handle incoming WebSocket messages"""
        try:
            data = json.loads(message)
            
            if isinstance(data, dict):
                # Handle subscription confirmation
                if data.get('type') == 'subscribed':
                    cprint("✅ WebSocket subscribed to live trades!", "green")
                    self.ws_connected = True
                    return
                
                # Handle pong
                if data.get('type') == 'pong':
                    return
                
                # Handle trade data
                topic = data.get('topic')
                msg_type = data.get('type')
                payload = data.get('payload', {})
                
                if topic == 'activity' and msg_type == 'orders_matched':
                    self.total_trades_tracked += 1
                    
                    if not self.ws_connected:
                        self.ws_connected = True
                    
                    # Extract trade info
                    price = float(payload.get('price', 0))
                    size = float(payload.get('size', 0))
                    usd_value = price * size
                    
                    # Check if this is a whale trade
                    if usd_value >= MIN_WHALE_TRADE_SIZE:
                        self.process_whale_trade(payload, usd_value)
        
        except json.JSONDecodeError:
            pass
        except Exception as e:
            cprint(f"⚠️ Error processing WebSocket message: {e}", "yellow")
    
    def process_whale_trade(self, trade_data: dict, usd_value: float):
        """Process a detected whale trade"""
        self.whale_trades_detected += 1
        
        # Extract trade details
        market_slug = trade_data.get('eventSlug', '')
        market_title = trade_data.get('title', 'Unknown')
        wallet = trade_data.get('trader', 'Unknown')
        side = trade_data.get('side', '')
        price = float(trade_data.get('price', 0))
        size = float(trade_data.get('size', 0))
        
        cprint(f"\n🐋 WHALE TRADE DETECTED!", "white", "on_cyan")
        cprint(f"   Market: {market_title[:60]}...", "cyan")
        cprint(f"   Wallet: {wallet[:16]}...", "cyan")
        cprint(f"   Side: {side}", "cyan")
        cprint(f"   Size: {format_usd(usd_value)}", "yellow", attrs=['bold'])
        
        # Get trader stats (if available)
        trader_stats = get_trader_stats(wallet)
        win_rate = trader_stats.get('win_rate', 0)
        
        # Check if this is a high-quality whale
        is_quality_whale = win_rate >= MIN_WHALE_WIN_RATE
        
        if is_quality_whale:
            cprint(f"   ✅ Quality Whale! Win Rate: {win_rate:.1f}%", "white", "on_green")
        else:
            cprint(f"   ⚠️ Low win rate: {win_rate:.1f}%", "yellow")
        
        # Save whale trade
        new_trade = {
            'timestamp': datetime.now().isoformat(),
            'market_slug': market_slug,
            'market_title': market_title,
            'wallet_address': wallet,
            'side': side,
            'price': price,
            'size': size,
            'usd_value': usd_value,
            'trader_win_rate': win_rate,
            'ai_validated': False,
            'copied': False
        }
        
        self.whale_trades_df = pd.concat([
            self.whale_trades_df,
            pd.DataFrame([new_trade])
        ], ignore_index=True)
        
        self._save_whale_trades()
        
        # Update whale wallet tracking
        self._update_whale_wallet(wallet, trader_stats)
        
        # Check if we should copy this trade
        if is_quality_whale and AUTO_COPY_ENABLED:
            self._evaluate_copy_trade(market_slug, market_title, side, usd_value, wallet, win_rate)
    
    def _update_whale_wallet(self, wallet: str, stats: dict):
        """Update whale wallet statistics"""
        if wallet in self.whale_wallets_df['wallet_address'].values:
            # Update existing wallet
            mask = self.whale_wallets_df['wallet_address'] == wallet
            self.whale_wallets_df.loc[mask, 'last_seen'] = datetime.now().isoformat()
            self.whale_wallets_df.loc[mask, 'trade_count'] = self.whale_wallets_df.loc[mask, 'trade_count'] + 1
            
            if stats:
                self.whale_wallets_df.loc[mask, 'win_rate'] = stats.get('win_rate', 0)
                self.whale_wallets_df.loc[mask, 'total_volume'] = stats.get('total_volume', 0)
                self.whale_wallets_df.loc[mask, 'profit_loss'] = stats.get('profit_loss', 0)
        else:
            # Add new whale
            new_whale = {
                'wallet_address': wallet,
                'win_rate': stats.get('win_rate', 0) if stats else 0,
                'total_volume': stats.get('total_volume', 0) if stats else 0,
                'profit_loss': stats.get('profit_loss', 0) if stats else 0,
                'first_seen': datetime.now().isoformat(),
                'last_seen': datetime.now().isoformat(),
                'trade_count': 1
            }
            
            self.whale_wallets_df = pd.concat([
                self.whale_wallets_df,
                pd.DataFrame([new_whale])
            ], ignore_index=True)
        
        self._save_whale_wallets()
    
    def _evaluate_copy_trade(
        self,
        market_slug: str,
        market_title: str,
        whale_side: str,
        whale_size_usd: float,
        whale_wallet: str,
        whale_win_rate: float
    ):
        """Evaluate if we should copy this whale trade"""
        cprint(f"\n🤖 Evaluating copy trade opportunity...", "white", "on_magenta")
        
        # Step 1: Ask AI swarm if this is a good trade
        ai_approved = ai_validate_trade(market_slug, whale_side, MIN_AI_CONSENSUS)
        
        if not ai_approved:
            cprint(f"❌ AI rejected this trade - not copying", "red")
            return
        
        self.ai_validated_trades += 1
        
        # Step 2: Calculate our position size
        copy_size_usd = min(
            whale_size_usd * (COPY_PERCENTAGE / 100),
            MAX_POSITION_SIZE
        )
        
        cprint(f"\n✅ AI APPROVED!", "white", "on_green")
        cprint(f"   Whale Size: {format_usd(whale_size_usd)}", "cyan")
        cprint(f"   Our Size: {format_usd(copy_size_usd)} ({COPY_PERCENTAGE}% of whale)", "cyan")
        cprint(f"   Whale Win Rate: {whale_win_rate:.1f}%", "cyan")
        
        # Step 3: Check our balance
        balance = get_balance()
        
        if balance < copy_size_usd:
            cprint(f"❌ Insufficient balance: ${balance:.2f} < ${copy_size_usd:.2f}", "red")
            return
        
        # Step 4: Execute the copy trade
        if AUTO_COPY_ENABLED:
            trading_mode = "PAPER" if PAPER_TRADING_ENABLED else "LIVE"
            cprint(f"\n🚀 Executing {trading_mode} copy trade...", "white", "on_blue")
            
            # TODO: Get token ID for the market
            # For now we'll simulate with a placeholder token ID
            token_id = f"{market_slug}_YES_TOKEN" if whale_side == "YES" else f"{market_slug}_NO_TOKEN"
            
            # Place the order (will route to paper trading if PAPER_TRADING_ENABLED=true)
            order_id = place_market_order(
                token_id=token_id,
                size=copy_size_usd,  # This will be converted to shares in the function
                side="BUY",  # We're copying the whale, so always BUY
                market_slug=market_slug,
                market_title=market_title,
                notes=f"Whale copy: {whale_wallet[:16]}... | Win rate: {whale_win_rate:.1f}% | AI validated"
            )
            
            executed = order_id is not None
            
            # Save copy signal
            copy_signal = {
                'timestamp': datetime.now().isoformat(),
                'market_slug': market_slug,
                'market_title': market_title,
                'whale_wallet': whale_wallet,
                'whale_side': whale_side,
                'whale_size': whale_size_usd,
                'our_side': whale_side,
                'our_size': copy_size_usd,
                'ai_consensus': MIN_AI_CONSENSUS,
                'executed': executed,
                'outcome': 'PENDING'
            }
            
            self.copy_signals_df = pd.concat([
                self.copy_signals_df,
                pd.DataFrame([copy_signal])
            ], ignore_index=True)
            
            self._save_copy_signals()
            
            if executed:
                self.trades_copied += 1
                if PAPER_TRADING_ENABLED:
                    cprint(f"✅ Paper trade simulated! (Trade ID: {order_id})", "white", "on_green")
                else:
                    cprint(f"✅ LIVE trade executed! (Order ID: {order_id})", "white", "on_green")
            else:
                cprint(f"❌ Copy trade failed to execute", "red")
    
    def on_ws_error(self, ws, error):
        """Handle WebSocket errors"""
        cprint(f"❌ WebSocket Error: {error}", "red")
    
    def on_ws_close(self, ws, close_status_code, close_msg):
        """Handle WebSocket close"""
        self.ws_connected = False
        cprint(f"\n🔌 WebSocket connection closed: {close_status_code} - {close_msg}", "yellow")
        cprint("Reconnecting in 5 seconds...", "cyan")
        time.sleep(5)
        self.connect_websocket()
    
    def on_ws_open(self, ws):
        """Handle WebSocket open - send subscription"""
        cprint("🔌 WebSocket connected!", "green")
        
        # Subscribe to all trades
        subscription_msg = {
            "action": "subscribe",
            "subscriptions": [
                {
                    "topic": "activity",
                    "type": "orders_matched"
                }
            ]
        }
        
        cprint(f"📡 Sending subscription for live trades...", "cyan")
        ws.send(json.dumps(subscription_msg))
        
        self.ws_connected = True
        cprint("✅ Subscription sent! Waiting for whale trades...", "green")
        
        # Start ping thread
        def send_ping():
            while True:
                time.sleep(5)
                try:
                    ws.send(json.dumps({"type": "ping"}))
                except:
                    break
        
        ping_thread = threading.Thread(target=send_ping, daemon=True)
        ping_thread.start()
    
    def connect_websocket(self):
        """Connect to Polymarket WebSocket"""
        cprint(f"🚀 Connecting to {WEBSOCKET_URL}...", "cyan")
        
        self.ws = websocket.WebSocketApp(
            WEBSOCKET_URL,
            on_open=self.on_ws_open,
            on_message=self.on_ws_message,
            on_error=self.on_ws_error,
            on_close=self.on_ws_close
        )
        
        # Run WebSocket in a thread
        ws_thread = threading.Thread(target=self.ws.run_forever, daemon=True)
        ws_thread.start()
        
        cprint("✅ WebSocket thread started!", "green")
    
    def status_display_loop(self):
        """Display status updates every 30 seconds"""
        cprint("\n📊 STATUS DISPLAY THREAD STARTED", "cyan", attrs=['bold'])
        
        while True:
            try:
                time.sleep(30)
                
                cprint(f"\n{'='*60}", "cyan")
                cprint(f"🐋 Whale Tracker Status @ {datetime.now().strftime('%H:%M:%S')}", "cyan", attrs=['bold'])
                cprint(f"{'='*60}", "cyan")
                cprint(f"   WebSocket: {'✅ Connected' if self.ws_connected else '❌ Disconnected'}", "green" if self.ws_connected else "red")
                cprint(f"   Total Trades Tracked: {self.total_trades_tracked:,}", "white")
                cprint(f"   Whale Trades Detected: {self.whale_trades_detected:,}", "yellow")
                cprint(f"   AI Validated Trades: {self.ai_validated_trades:,}", "green")
                cprint(f"   Trades Copied: {self.trades_copied:,}", "cyan", attrs=['bold'])
                cprint(f"   Known Whale Wallets: {len(self.whale_wallets_df)}", "white")
                cprint(f"{'='*60}\n", "cyan")
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                cprint(f"❌ Error in status display: {e}", "red")
    
    def run(self):
        """Start the whale tracker"""
        cprint("\n🐋 Starting Whale Tracker...", "white", "on_cyan")
        
        # Connect WebSocket
        self.connect_websocket()
        
        # Start status display
        status_thread = threading.Thread(target=self.status_display_loop, daemon=True)
        status_thread.start()
        
        cprint("\n✅ Whale Tracker is running!", "white", "on_green")
        cprint("🔍 Tracking whale trades in real-time...", "cyan")
        cprint("⏸️  Press Ctrl+C to stop\n", "yellow")
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            cprint("\n\n🛑 Stopping Whale Tracker...", "yellow")
            cprint("💾 Saving final data...", "cyan")
            self._save_whale_trades()
            self._save_whale_wallets()
            self._save_copy_signals()
            cprint("✅ Shutdown complete!\n", "green")


# ==============================================================================
# MAIN
# ==============================================================================

def main():
    """Main entry point"""
    cprint("\n" + "="*80, "cyan")
    cprint("🐋 Moon Dev's Polymarket Whale Tracker & Copy Bot", "cyan", attrs=['bold'])
    cprint("="*80, "cyan")
    
    # Display paper trading mode prominently
    if PAPER_TRADING_ENABLED:
        cprint("\n" + "="*80, "yellow")
        cprint("📝 PAPER TRADING MODE - NO REAL MONEY", "white", "on_yellow", attrs=['bold'])
        cprint("⚠️  All trades will be SIMULATED ONLY", "white", "on_yellow", attrs=['bold'])
        cprint("="*80 + "\n", "yellow")
    else:
        cprint("\n" + "="*80, "red")
        cprint("⚠️ LIVE TRADING MODE - REAL MONEY AT RISK!", "white", "on_red", attrs=['bold'])
        cprint("="*80 + "\n", "red")
    
    cprint(f"💰 Minimum whale trade size: {format_usd(MIN_WHALE_TRADE_SIZE)}", "yellow")
    cprint(f"🎯 Minimum whale win rate: {MIN_WHALE_WIN_RATE}%", "yellow")
    cprint(f"🤖 AI consensus required: {MIN_AI_CONSENSUS:.0%}", "yellow")
    cprint(f"🔄 Auto-copy: {'✅ ENABLED' if AUTO_COPY_ENABLED else '❌ DISABLED'}", "yellow")
    if AUTO_COPY_ENABLED:
        cprint(f"   Max position size: {format_usd(MAX_POSITION_SIZE)}", "cyan")
        cprint(f"   Copy percentage: {COPY_PERCENTAGE}% of whale size", "cyan")
        if PAPER_TRADING_ENABLED:
            cprint(f"   📝 Mode: PAPER TRADING (simulated)", "yellow")
        else:
            cprint(f"   ⚠️ Mode: LIVE TRADING (real money!)", "red", attrs=['bold'])
    cprint("="*80 + "\n", "cyan")
    
    # Initialize and run agent
    agent = WhaleTrackerAgent()
    agent.run()


if __name__ == "__main__":
    main()
