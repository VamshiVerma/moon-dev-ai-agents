"""
🌙 Moon Dev's Polymarket PAPER TRADING Engine
Built with love by Moon Dev 🚀

⚠️ SIMULATION ONLY - NO REAL MONEY ⚠️

This module simulates trading on Polymarket without placing real orders.
Perfect for:
- Testing trading strategies
- Tracking whale copy performance
- Validating AI predictions
- Learning without risk

All "trades" are recorded to CSV with hypothetical P&L tracking.
"""

import os
import sys
import json
import pandas as pd
from datetime import datetime
from pathlib import Path
from termcolor import cprint
from typing import Optional, Dict
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project root to path
project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# ==============================================================================
# PAPER TRADING CONFIGURATION
# ==============================================================================

PAPER_TRADING_ENABLED = os.getenv("PAPER_TRADING_ENABLED", "true").lower() == "true"
PAPER_STARTING_BALANCE = float(os.getenv("PAPER_STARTING_BALANCE", 10000))
PAPER_DATA_FOLDER = os.path.join(project_root, "src/data/polymarket_paper_trading")
PAPER_TRADES_CSV = os.path.join(PAPER_DATA_FOLDER, "paper_trades.csv")
PAPER_POSITIONS_CSV = os.path.join(PAPER_DATA_FOLDER, "paper_positions.csv")
PAPER_BALANCE_CSV = os.path.join(PAPER_DATA_FOLDER, "paper_balance.csv")

# Create data folder
os.makedirs(PAPER_DATA_FOLDER, exist_ok=True)

# ==============================================================================
# PAPER TRADING ENGINE
# ==============================================================================

class PaperTradingEngine:
    """Simulates Polymarket trading without real money"""
    
    def __init__(self, starting_balance: float = PAPER_STARTING_BALANCE):
        """Initialize paper trading engine"""
        cprint("\n" + "="*80, "yellow")
        cprint("📝 PAPER TRADING MODE - SIMULATION ONLY", "white", "on_yellow", attrs=['bold'])
        cprint("⚠️  NO REAL MONEY WILL BE USED", "white", "on_yellow", attrs=['bold'])
        cprint("="*80, "yellow")
        
        self.starting_balance = starting_balance
        self.balance = starting_balance
        
        # Load or initialize data
        self.trades_df = self._load_trades()
        self.positions_df = self._load_positions()
        self.balance_history = self._load_balance_history()
        
        # Calculate current balance from trades
        self._recalculate_balance()
        
        cprint(f"💰 Starting Balance: ${self.starting_balance:,.2f} USDC (simulated)", "cyan")
        cprint(f"💵 Current Balance: ${self.balance:,.2f} USDC (simulated)", "green")
        cprint(f"📊 Total Trades: {len(self.trades_df)}", "cyan")
        cprint(f"📈 Open Positions: {len(self.positions_df)}", "cyan")
        cprint("="*80 + "\n", "yellow")
    
    def _load_trades(self) -> pd.DataFrame:
        """Load paper trading history"""
        if os.path.exists(PAPER_TRADES_CSV):
            try:
                return pd.read_csv(PAPER_TRADES_CSV)
            except Exception as e:
                cprint(f"⚠️ Error loading trades: {e}", "yellow")
        
        return pd.DataFrame(columns=[
            'timestamp', 'trade_id', 'market_slug', 'market_title',
            'side', 'token_id', 'price', 'size', 'usd_value',
            'order_type', 'status', 'pnl', 'notes'
        ])
    
    def _load_positions(self) -> pd.DataFrame:
        """Load open positions"""
        if os.path.exists(PAPER_POSITIONS_CSV):
            try:
                return pd.read_csv(PAPER_POSITIONS_CSV)
            except Exception as e:
                cprint(f"⚠️ Error loading positions: {e}", "yellow")
        
        return pd.DataFrame(columns=[
            'market_slug', 'market_title', 'token_id', 'side',
            'entry_price', 'current_price', 'shares', 'entry_value',
            'current_value', 'unrealized_pnl', 'opened_at'
        ])
    
    def _load_balance_history(self) -> pd.DataFrame:
        """Load balance history"""
        if os.path.exists(PAPER_BALANCE_CSV):
            try:
                return pd.read_csv(PAPER_BALANCE_CSV)
            except Exception as e:
                cprint(f"⚠️ Error loading balance history: {e}", "yellow")
        
        return pd.DataFrame(columns=['timestamp', 'balance', 'total_pnl'])
    
    def _save_trades(self):
        """Save trades to CSV"""
        try:
            self.trades_df.to_csv(PAPER_TRADES_CSV, index=False)
        except Exception as e:
            cprint(f"❌ Error saving trades: {e}", "red")
    
    def _save_positions(self):
        """Save positions to CSV"""
        try:
            self.positions_df.to_csv(PAPER_POSITIONS_CSV, index=False)
        except Exception as e:
            cprint(f"❌ Error saving positions: {e}", "red")
    
    def _save_balance(self):
        """Save balance history to CSV"""
        try:
            self.balance_history.to_csv(PAPER_BALANCE_CSV, index=False)
        except Exception as e:
            cprint(f"❌ Error saving balance: {e}", "red")
    
    def _recalculate_balance(self):
        """Recalculate balance from trade history"""
        if self.trades_df.empty:
            self.balance = self.starting_balance
            return
        
        # Calculate realized P&L from closed trades
        closed_trades = self.trades_df[self.trades_df['status'] == 'CLOSED']
        realized_pnl = closed_trades['pnl'].sum() if not closed_trades.empty else 0
        
        # Calculate unrealized P&L from open positions
        unrealized_pnl = self.positions_df['unrealized_pnl'].sum() if not self.positions_df.empty else 0
        
        self.balance = self.starting_balance + realized_pnl
        total_pnl = realized_pnl + unrealized_pnl
        
        # Update balance history
        balance_update = {
            'timestamp': datetime.now().isoformat(),
            'balance': self.balance,
            'total_pnl': total_pnl
        }
        
        self.balance_history = pd.concat([
            self.balance_history,
            pd.DataFrame([balance_update])
        ], ignore_index=True)
        
        self._save_balance()
    
    def place_order(
        self,
        market_slug: str,
        market_title: str,
        token_id: str,
        side: str,
        price: float,
        size: float,
        order_type: str = "LIMIT",
        notes: str = ""
    ) -> str:
        """
        Simulate placing an order
        
        Args:
            market_slug: Market identifier
            market_title: Human-readable market name
            token_id: YES or NO token ID
            side: "BUY" or "SELL"
            price: Price per share (0-1)
            size: Number of shares
            order_type: "LIMIT" or "MARKET"
            notes: Optional notes (e.g., "Whale copy trade", "AI signal")
        
        Returns:
            Trade ID
        """
        usd_value = price * size
        
        # Check balance for BUY orders
        if side == "BUY" and usd_value > self.balance:
            cprint(f"❌ Insufficient balance: ${self.balance:.2f} < ${usd_value:.2f}", "red")
            return None
        
        # Generate trade ID
        trade_id = f"PAPER_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        cprint(f"\n📝 PAPER TRADE SIMULATED", "white", "on_yellow")
        cprint(f"   Trade ID: {trade_id}", "cyan")
        cprint(f"   Market: {market_title[:50]}...", "cyan")
        cprint(f"   Side: {side}", "cyan")
        cprint(f"   Price: ${price:.3f}", "cyan")
        cprint(f"   Size: {size:.2f} shares", "cyan")
        cprint(f"   Value: ${usd_value:.2f}", "yellow", attrs=['bold'])
        if notes:
            cprint(f"   Notes: {notes}", "white")
        
        # Record trade
        trade = {
            'timestamp': datetime.now().isoformat(),
            'trade_id': trade_id,
            'market_slug': market_slug,
            'market_title': market_title,
            'side': side,
            'token_id': token_id,
            'price': price,
            'size': size,
            'usd_value': usd_value,
            'order_type': order_type,
            'status': 'OPEN',
            'pnl': 0,
            'notes': notes
        }
        
        self.trades_df = pd.concat([
            self.trades_df,
            pd.DataFrame([trade])
        ], ignore_index=True)
        
        self._save_trades()
        
        # Update balance if BUY
        if side == "BUY":
            self.balance -= usd_value
        
        # Add to positions if BUY
        if side == "BUY":
            self._add_position(market_slug, market_title, token_id, side, price, size, usd_value)
        # Close position if SELL
        else:
            self._close_position(market_slug, token_id, price, size)
        
        self._recalculate_balance()
        
        cprint(f"✅ Paper trade recorded! New balance: ${self.balance:,.2f}", "green")
        
        return trade_id
    
    def _add_position(
        self,
        market_slug: str,
        market_title: str,
        token_id: str,
        side: str,
        entry_price: float,
        shares: float,
        entry_value: float
    ):
        """Add a new position"""
        position = {
            'market_slug': market_slug,
            'market_title': market_title,
            'token_id': token_id,
            'side': side,
            'entry_price': entry_price,
            'current_price': entry_price,  # Will be updated
            'shares': shares,
            'entry_value': entry_value,
            'current_value': entry_value,
            'unrealized_pnl': 0,
            'opened_at': datetime.now().isoformat()
        }
        
        self.positions_df = pd.concat([
            self.positions_df,
            pd.DataFrame([position])
        ], ignore_index=True)
        
        self._save_positions()
    
    def _close_position(self, market_slug: str, token_id: str, exit_price: float, shares: float):
        """Close a position and calculate P&L"""
        # Find matching position
        mask = (self.positions_df['market_slug'] == market_slug) & \
               (self.positions_df['token_id'] == token_id)
        
        if not self.positions_df[mask].empty:
            position = self.positions_df[mask].iloc[0]
            entry_price = position['entry_price']
            entry_value = position['entry_value']
            
            # Calculate P&L
            exit_value = exit_price * shares
            pnl = exit_value - entry_value
            
            # Update balance
            self.balance += exit_value
            
            # Update trade with P&L
            # Find the original BUY trade
            buy_trade_mask = (self.trades_df['market_slug'] == market_slug) & \
                            (self.trades_df['token_id'] == token_id) & \
                            (self.trades_df['side'] == 'BUY') & \
                            (self.trades_df['status'] == 'OPEN')
            
            if not self.trades_df[buy_trade_mask].empty:
                self.trades_df.loc[buy_trade_mask, 'status'] = 'CLOSED'
                self.trades_df.loc[buy_trade_mask, 'pnl'] = pnl
                self._save_trades()
            
            # Remove from positions
            self.positions_df = self.positions_df[~mask]
            self._save_positions()
            
            cprint(f"💰 Position closed! P&L: ${pnl:+.2f}", "green" if pnl > 0 else "red")
    
    def update_position_prices(self, market_slug: str, current_price: float):
        """Update current prices for a position to calculate unrealized P&L"""
        mask = self.positions_df['market_slug'] == market_slug
        
        if not self.positions_df[mask].empty:
            self.positions_df.loc[mask, 'current_price'] = current_price
            self.positions_df.loc[mask, 'current_value'] = \
                self.positions_df.loc[mask, 'shares'] * current_price
            self.positions_df.loc[mask, 'unrealized_pnl'] = \
                self.positions_df.loc[mask, 'current_value'] - self.positions_df.loc[mask, 'entry_value']
            
            self._save_positions()
    
    def get_performance_summary(self) -> Dict:
        """Get overall performance statistics"""
        closed_trades = self.trades_df[self.trades_df['status'] == 'CLOSED']
        
        if closed_trades.empty:
            return {
                'total_trades': 0,
                'winning_trades': 0,
                'losing_trades': 0,
                'win_rate': 0,
                'total_pnl': 0,
                'avg_win': 0,
                'avg_loss': 0,
                'current_balance': self.balance,
                'total_return': 0
            }
        
        winning = closed_trades[closed_trades['pnl'] > 0]
        losing = closed_trades[closed_trades['pnl'] < 0]
        
        total_pnl = closed_trades['pnl'].sum()
        total_return = ((self.balance - self.starting_balance) / self.starting_balance) * 100
        
        return {
            'total_trades': len(closed_trades),
            'winning_trades': len(winning),
            'losing_trades': len(losing),
            'win_rate': (len(winning) / len(closed_trades)) * 100 if len(closed_trades) > 0 else 0,
            'total_pnl': total_pnl,
            'avg_win': winning['pnl'].mean() if len(winning) > 0 else 0,
            'avg_loss': losing['pnl'].mean() if len(losing) > 0 else 0,
            'current_balance': self.balance,
            'total_return': total_return
        }
    
    def print_performance(self):
        """Pretty print performance statistics"""
        stats = self.get_performance_summary()
        
        cprint("\n" + "="*80, "cyan")
        cprint("📊 PAPER TRADING PERFORMANCE (SIMULATED)", "white", "on_cyan", attrs=['bold'])
        cprint("="*80, "cyan")
        cprint(f"💰 Starting Balance: ${self.starting_balance:,.2f}", "white")
        cprint(f"💵 Current Balance:  ${stats['current_balance']:,.2f}", "green" if stats['current_balance'] > self.starting_balance else "red", attrs=['bold'])
        cprint(f"📈 Total Return:     {stats['total_return']:+.2f}%", "green" if stats['total_return'] > 0 else "red", attrs=['bold'])
        cprint(f"💸 Total P&L:        ${stats['total_pnl']:+,.2f}", "green" if stats['total_pnl'] > 0 else "red")
        cprint("", "white")
        cprint(f"📊 Total Trades:     {stats['total_trades']}", "white")
        cprint(f"✅ Winning Trades:   {stats['winning_trades']}", "green")
        cprint(f"❌ Losing Trades:    {stats['losing_trades']}", "red")
        cprint(f"🎯 Win Rate:         {stats['win_rate']:.1f}%", "yellow")
        cprint(f"💚 Avg Win:          ${stats['avg_win']:,.2f}", "green")
        cprint(f"💔 Avg Loss:         ${stats['avg_loss']:,.2f}", "red")
        cprint("", "white")
        cprint(f"📂 Open Positions:   {len(self.positions_df)}", "cyan")
        cprint("="*80 + "\n", "cyan")


# ==============================================================================
# GLOBAL PAPER TRADING INSTANCE
# ==============================================================================

# Create global instance
paper_engine = PaperTradingEngine() if PAPER_TRADING_ENABLED else None

# ==============================================================================
# EXAMPLE USAGE
# ==============================================================================

if __name__ == "__main__":
    cprint("\n🌙 Moon Dev's Paper Trading Engine - Test Mode", "white", "on_blue")
    cprint("="*80, "cyan")
    
    engine = PaperTradingEngine(starting_balance=10000)
    
    # Simulate some trades
    cprint("\n1️⃣ Simulating BUY order", "yellow")
    trade1 = engine.place_order(
        market_slug="presidential-election-2024",
        market_title="Will Trump win 2024 election?",
        token_id="YES_TOKEN_123",
        side="BUY",
        price=0.65,
        size=100,
        notes="AI signal - 85% confidence"
    )
    
    cprint("\n2️⃣ Simulating another BUY order", "yellow")
    trade2 = engine.place_order(
        market_slug="bitcoin-100k-2024",
        market_title="Will Bitcoin hit $100k in 2024?",
        token_id="YES_TOKEN_456",
        side="BUY",
        price=0.45,
        size=50,
        notes="Whale copy trade"
    )
    
    # Wait a bit (simulated)
    cprint("\n⏳ Simulating price movement...", "cyan")
    
    # Close first position at a profit
    cprint("\n3️⃣ Simulating SELL order (profit)", "yellow")
    trade3 = engine.place_order(
        market_slug="presidential-election-2024",
        market_title="Will Trump win 2024 election?",
        token_id="YES_TOKEN_123",
        side="SELL",
        price=0.75,  # +0.10 profit per share
        size=100,
        notes="Taking profit"
    )
    
    # Print performance
    engine.print_performance()
    
    cprint("\n✅ Paper trading test complete!", "white", "on_green")
    cprint(f"📁 Data saved to: {PAPER_DATA_FOLDER}\n", "cyan")
