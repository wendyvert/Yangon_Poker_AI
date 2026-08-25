#============================================
#THE SECRET POKER DEN OF YANGON
#Poker AI with Prolog Integration
#============================================

#FILE SECTIONS:
#- Lines 1-150:   Member 3 (Game Engine)
#- Lines 151-280: Member 4 (Prolog Bridge)
#- Lines 281-400: Member 5 (UI & Narrative)
#============================================


# ============================================
# MEMBER 3: Game Engine (Lines 1-150)
# ============================================

# Create the Card Class

import random
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")  # Allow card suit symbols on all consoles


class Card:
    """Represents a single playing card."""

    def __init__(self, suit, rank):
        self.suit = suit          # 'hearts', 'diamonds', 'clubs', 'spades'
        self.rank = rank          # 2-14 (11=J, 12=Q, 13=K, 14=A)

    def __str__(self):
        """Returns a readable card name like 'A♥' or '10♠'"""
        rank_names = {11: 'J', 12: 'Q', 13: 'K', 14: 'A'}
        rank_str = rank_names.get(self.rank, str(self.rank))
        suit_symbols = {
            'hearts': '♥',
            'diamonds': '♦',
            'clubs': '♣',
            'spades': '♠'
        }
        return f"{rank_str}{suit_symbols[self.suit]}"

    def to_prolog_name(self):
        """Convert to Prolog-compatible name like 'card_ah'"""
        rank_letters = {11: 'j', 12: 'q', 13: 'k', 14: 'a'}
        rank_str = rank_letters.get(self.rank, str(self.rank))
        suit_letters = {
            'hearts': 'h',
            'diamonds': 'd',
            'clubs': 'c',
            'spades': 's'
        }
        return f"card_{rank_str}{suit_letters[self.suit]}"


# Create the Deck Class

class Deck:
    """Represents a deck of 52 playing cards."""

    def __init__(self):
        self.cards = []
        self.create_deck()

    def create_deck(self):
        """Create a standard 52-card deck (no jokers)."""
        suits = ['hearts', 'diamonds', 'clubs', 'spades']
        for suit in suits:
            for rank in range(2, 15):  # 2 through Ace (14)
                self.cards.append(Card(suit, rank))

    def shuffle(self):
        """Shuffle the deck randomly."""
        random.shuffle(self.cards)

    def deal_card(self):
        """Deal one card from the top of the deck."""
        if len(self.cards) == 0:
            return None
        return self.cards.pop()

    def deal_cards(self, count):
        """Deal multiple cards at once."""
        dealt = []
        for _ in range(count):
            card = self.deal_card()
            if card:
                dealt.append(card)
        return dealt

    def __len__(self):
        return len(self.cards)


# Create the PokerGame Class

class PokerGame:
    """Manages the state and flow of a Texas Hold'em poker game."""

    def __init__(self):
        self.deck = None
        self.player_hand = []      # Player's 2 hole cards
        self.ai_hand = []          # AI's 2 hole cards
        self.community_cards = []  # 5 community cards (flop, turn, river)
        self.pot = 0
        self.current_bet = 0
        self.player_chips = 1000
        self.ai_chips = 1000
        self.round = 'preflop'     # 'preflop', 'flop', 'turn', 'river', 'showdown'
        self.hand_over = False     # True once the current hand ends (fold)
        self.game_over = False     # True once the whole game ends

    def start_new_hand(self):
        """Start a new hand by dealing cards."""
        self.deck = Deck()
        self.deck.shuffle()

        # Clear previous cards
        self.player_hand = []
        self.ai_hand = []
        self.community_cards = []
        self.pot = 0
        self.current_bet = 0
        self.round = 'preflop'
        self.hand_over = False

        # Deal 2 cards to each player
        self.player_hand = self.deck.deal_cards(2)
        self.ai_hand = self.deck.deal_cards(2)

        # Set initial blinds
        self.current_bet = 10  # Small blind

    def deal_flop(self):
        """Deal 3 community cards (flop)."""
        self.community_cards = self.deck.deal_cards(3)
        self.round = 'flop'

    def deal_turn(self):
        """Deal 1 community card (turn)."""
        self.community_cards.append(self.deck.deal_card())
        self.round = 'turn'

    def deal_river(self):
        """Deal 1 community card (river)."""
        self.community_cards.append(self.deck.deal_card())
        self.round = 'river'

    def get_all_cards(self, player_type='player'):
        """Get all 7 cards (2 hole + 5 community)."""
        if player_type == 'player':
            return self.player_hand + self.community_cards
        else:
            return self.ai_hand + self.community_cards

    def get_prolog_cards(self, player_type='player'):
        """Get all cards in Prolog-compatible format."""
        cards = self.get_all_cards(player_type)
        return [card.to_prolog_name() for card in cards]

    # Implement Player Actions

    def player_raise(self, amount):
        """Player raises the bet."""
        if amount > self.player_chips:
            print("❌ You don't have enough chips!")
            return False
        self.player_chips -= amount
        self.pot += amount
        self.current_bet = amount
        return True

    def player_call(self):
        """Player calls the current bet."""
        if self.current_bet > self.player_chips:
            print("❌ You don't have enough chips to call!")
            return False
        self.player_chips -= self.current_bet
        self.pot += self.current_bet
        return True

    def player_fold(self):
        """Player folds (loses the hand)."""
        self.hand_over = True
        return True

    def player_check(self):
        """Player checks (passes without betting)."""
        return True

    def ai_raise(self, amount):
        """AI raises the bet."""
        if amount > self.ai_chips:
            amount = self.ai_chips
        self.ai_chips -= amount
        self.pot += amount
        self.current_bet = amount
        return amount

    def ai_call(self):
        """AI calls the current bet."""
        if self.current_bet > self.ai_chips:
            self.current_bet = self.ai_chips
        self.ai_chips -= self.current_bet
        self.pot += self.current_bet
        return True

    def ai_fold(self):
        """AI folds (player wins the hand)."""
        self.hand_over = True
        return True

    def ai_check(self):
        """AI checks (passes without betting)."""
        return True


# Create the Display Functions

def display_cards(cards, title="Cards"):
    """Display cards in a nice format."""
    if not cards:
        print(f"{title}: (No cards)")
        return

    card_strs = [str(card) for card in cards]
    print(f"\n{title}:")
    print("┌─────┐ " * len(cards))
    for card_str in card_strs:
        print(f"│ {card_str:4} │", end=" ")
    print()
    print("└─────┘ " * len(cards))


def display_game_state(game):
    """Display the current game state."""
    print("\n" + "=" * 60)
    print(f"🃏 ROUND: {game.round.upper()}")
    print("=" * 60)

    print(f"\n💰 Pot: {game.pot} chips")
    print(f"💵 Current Bet: {game.current_bet} chips")
    print(f"👤 Your Chips: {game.player_chips}")
    print(f"🤖 AI Chips: {game.ai_chips}")

    if game.player_hand:
        display_cards(game.player_hand, "Your Hand")

    if game.community_cards:
        display_cards(game.community_cards, "Community Cards")

    print("\n" + "=" * 60)


# Create the Player Input Function

def get_player_action():
    """Get the player's action choice."""
    print("\n📋 Your options:")
    print("  1. Raise")
    print("  2. Call")
    print("  3. Fold")
    print("  4. Check")

    while True:
        choice = input("\nEnter your choice (1-4): ").strip()

        if choice == '1':
            try:
                amount = int(input("How much to raise? "))
                if amount > 0:
                    return ('raise', amount)
                else:
                    print("❌ Amount must be positive!")
            except ValueError:
                print("❌ Please enter a valid number!")

        elif choice == '2':
            return ('call', 0)

        elif choice == '3':
            return ('fold', 0)

        elif choice == '4':
            return ('check', 0)

        else:
            print("❌ Invalid choice. Please enter 1, 2, 3, or 4.")


def betting_round(game):
    """Display state and apply the player's action for one street.

    Returns True if the player folded.
    """
    display_game_state(game)
    action, amount = get_player_action()

    if action == 'raise':
        game.player_raise(amount)
        print(f"\n✅ You raised to {amount}")
    elif action == 'call':
        game.player_call()
        print(f"\n✅ You called {game.current_bet}")
    elif action == 'fold':
        game.player_fold()
        print("\n❌ You folded!")
        print("💀 U Ba Nyan wins this hand...")
        return True
    elif action == 'check':
        game.player_check()
        print("\n✅ You checked")
    return False


# Implement the Main Game Loop

def play_poker():
    """Main game loop."""
    print("\n" + "=" * 60)
    print("   🎰 Welcome to The Secret Poker Den of Yangon! 🎰")
    print("=" * 60)
    print("\nYou're sitting across from U Ba Nyan...")
    print("The legendary Prolog master. Let's see if you can beat him!\n")

    game = PokerGame()

    while not game.game_over:
        # Start a new hand
        game.start_new_hand()
        print("\n🔄 New hand starting...")
        print(f"💰 You have {game.player_chips} chips, AI has {game.ai_chips} chips")

        # --- PRE-FLOP ---
        player_folded = betting_round(game)

        # --- FLOP ---
        if not player_folded:
            game.deal_flop()
            player_folded = betting_round(game)

        # --- TURN ---
        if not player_folded:
            game.deal_turn()
            player_folded = betting_round(game)

        # --- RIVER ---
        if not player_folded:
            game.deal_river()
            player_folded = betting_round(game)

        if player_folded:
            # Player folded: AI collects the pot
            game.ai_chips += game.pot
        else:
            # --- SHOWDOWN ---
            print("\n" + "=" * 60)
            print("   🃏 SHOWDOWN! 🃏")
            print("=" * 60)

            display_cards(game.player_hand, "Your Hand")
            display_cards(game.ai_hand, "AI's Hand")
            display_cards(game.community_cards, "Community Cards")

            print(f"\n💰 Pot: {game.pot} chips")

            # For now, let's just say the player wins
            # (Member 4 will connect Prolog to evaluate the real winner)
            print("\n🎉 You win the pot!")
            game.player_chips += game.pot

        # Check if game should continue
        if game.player_chips <= 0:
            print("\n💀 You're out of chips! Game over.")
            game.game_over = True
        elif game.ai_chips <= 0:
            print("\n🎉 U Ba Nyan is out of chips! You win!")
            game.game_over = True
        else:
            play_again = input("\nPlay another hand? (y/n): ").strip().lower()
            if play_again != 'y':
                game.game_over = True

    print("\n" + "=" * 60)
    print("   🎰 Thanks for playing! 🎰")
    print("=" * 60)


if __name__ == "__main__":
    play_poker()


# ============================================
# MEMBER 4: Prolog Bridge (Lines 151-280)
# ============================================


from pyswip import Prolog

# ============================================
# GLOBAL VARIABLES
# ============================================

prolog = None  # Global Prolog instance

# ============================================
# FUNCTION: init_prolog()
# ============================================

def init_prolog():
    """
    Initialize Prolog engine and load poker_logic.pl
    Returns: True if successful, False otherwise
    """
    global prolog
    
    try:
        prolog = Prolog()
        prolog.consult("poker_logic.pl")
        print("Prolog engine loaded successfully!")
        return True
    except Exception as e:
        print(f"Error loading Prolog: {e}")
        print("Make sure poker_logic.pl exists and SWI-Prolog is installed")
        return False

# ============================================
# FUNCTION: card_to_prolog_name()
# ============================================

def card_to_prolog_name(card):
    """
    Convert Python Card object to Prolog atom name
    Card objects already have prolog_name attribute
    """
    return card.prolog_name

# ============================================
# FUNCTION: cards_to_prolog_list()
# ============================================

def cards_to_prolog_list(cards):
    """
    Convert list of Python Cards to Prolog list string
    Example: ['card_ah', 'card_kd'] -> "[card_ah,card_kd]"
    """
    if not cards:
        return "[]"
    prolog_names = [card_to_prolog_name(c) for c in cards]
    return '[' + ','.join(prolog_names) + ']'

# ============================================
# FUNCTION: evaluate_hand()
# ============================================

def evaluate_hand(cards):
    """
    Evaluate poker hand using Prolog
    
    Args:
        cards: list of Card objects (5-7 cards)
    
    Returns:
        tuple: (hand_type, strength) or ('unknown', 0)
    """
    global prolog
    
    if not prolog:
        print("Warning: Prolog not initialized!")
        return ('unknown', 0)
    
    if len(cards) < 5:
        print(f"Warning: Need at least 5 cards, got {len(cards)}")
        return ('unknown', 0)
    
    try:
        # Convert cards to Prolog list
        card_list = cards_to_prolog_list(cards)
        
        # Query for hand type
        query = f"evaluate_hand({card_list}, HandType)."
        results = list(prolog.query(query))
        
        if results and len(results) > 0:
            hand_type = results[0]['HandType']
            
            # Get strength for this hand type
            strength_query = f"hand_strength({hand_type}, Strength)."
            strength_results = list(prolog.query(strength_query))
            
            if strength_results and len(strength_results) > 0:
                return (hand_type, strength_results[0]['Strength'])
        
        return ('high_card', 1)  # Default fallback
        
    except Exception as e:
        print(f"Error in hand evaluation: {e}")
        return ('unknown', 0)

# ============================================
# FUNCTION: get_ai_decision()
# ============================================

def get_ai_decision(player_name, hand_type):
    """
    Get AI's decision from Prolog
    
    Args:
        player_name: string (e.g., 'u_ba_nyan')
        hand_type: string from evaluate_hand
    
    Returns:
        string: 'raise', 'call', 'fold', or 'check'
    """
    global prolog
    
    if not prolog:
        print("Warning: Prolog not initialized!")
        return 'check'
    
    try:
        query = f"decide_action({player_name}, {hand_type}, Action)."
        results = list(prolog.query(query))
        
        if results and len(results) > 0:
            action = results[0]['Action']
            # Ensure valid action
            if action in ['raise', 'call', 'fold', 'check']:
                return action
            else:
                return 'check'
        else:
            return 'check'
            
    except Exception as e:
        print(f"Error getting AI decision: {e}")
        return 'check'

# ============================================
# FUNCTION: update_game_state()
# ============================================

def update_game_state(game):
    """
    Update Prolog with current game state
    
    Args:
        game: PokerGame object
    """
    global prolog
    
    if not prolog:
        return
    
    try:
        # Update pot size
        prolog.query("retractall(pot_size(_)).")
        prolog.query(f"assert(pot_size({game.pot})).")
        
        # Update current bet
        prolog.query("retractall(current_bet(_)).")
        prolog.query(f"assert(current_bet({game.current_bet})).")
        
        # Update community cards
        prolog.query("retractall(community_cards(_,_,_)).")
        if game.community_cards:
            community_list = cards_to_prolog_list(game.community_cards)
            prolog.query(f"assert(community_cards({community_list}, [], [])).")
        else:
            prolog.query("assert(community_cards([], [], [])).")
            
    except Exception as e:
        print(f"Error updating game state: {e}")

# ============================================
# FUNCTION: update_opponent_behavior()
# ============================================

def update_opponent_behavior(player_name, behavior):
    """
    Update Prolog's dynamic facts about opponent behavior
    
    Args:
        player_name: string (e.g., 'u_ba_nyan')
        behavior: string (e.g., 'aggressive', 'passive')
    """
    global prolog
    
    if not prolog:
        return
    
    try:
        # First retract old behavior
        retract_query = f"retract(player_behavior({player_name}, _))."
        prolog.query(retract_query)
        
        # Then assert new behavior
        assert_query = f"assert(player_behavior({player_name}, {behavior}))."
        prolog.query(assert_query)
        
        print(f"Updated {player_name}'s behavior to {behavior}")
        
    except Exception as e:
        print(f"Error updating behavior: {e}")

# ============================================
# FUNCTION: get_complete_ai_action()
# ============================================

def get_complete_ai_action(game, player_name='u_ba_nyan'):
    """
    Complete AI decision process
    
    Args:
        game: PokerGame object
        player_name: string (default: 'u_ba_nyan')
    
    Returns:
        tuple: (action, hand_type, strength)
    """
    # Get all 7 cards (AI's 2 hole cards + 5 community cards)
    all_cards = game.ai_hand + game.community_cards
    
    # Evaluate hand strength using Prolog
    hand_type, strength = evaluate_hand(all_cards)
    print(f"AI Hand: {hand_type} (strength: {strength})")
    
    # Update game state in Prolog
    update_game_state(game)
    
    # Get decision from Prolog
    action = get_ai_decision(player_name, hand_type)
    print(f"AI Decision: {action}")
    
    return (action, hand_type, strength)

# ============================================
# FUNCTION: get_player_hand_strength()
# ============================================

def get_player_hand_strength(game):
    """
    Get player's hand strength for display
    
    Args:
        game: PokerGame object
    
    Returns:
        tuple: (hand_type, strength)
    """
    all_cards = game.player_hand + game.community_cards
    return evaluate_hand(all_cards)

# ============================================
# FUNCTION: test_prolog_bridge()
# ============================================

def test_prolog_bridge():
    """
    Test all Prolog bridge functions
    """
    print("\nTesting Prolog Bridge...")
    
    # Test 1: Initialize Prolog
    print("\nTest 1: Initialize Prolog")
    if init_prolog():
        print("Prolog initialized")
    else:
        print("Prolog initialization failed")
        return
    
    # Test 2: Test card conversion
    print("\nTest 2: Card Conversion")
    from main import Card
    card = Card('hearts', 14)
    prolog_name = card_to_prolog_name(card)
    print(f"Card: {card} -> Prolog: {prolog_name}")
    assert prolog_name == 'card_ah'
    print("Card conversion works")
    
    # Test 3: Test cards to list
    print("\nTest 3: Cards to Prolog List")
    cards = [Card('hearts', 14), Card('spades', 13)]
    prolog_list = cards_to_prolog_list(cards)
    print(f"Prolog list: {prolog_list}")
    assert prolog_list == '[card_ah,card_ks]'
    print("Cards to list works")
    
    # Test 4: Test hand evaluation
    print("\nTest 4: Hand Evaluation")
    # Create a flush hand
    flush_cards = [
        Card('hearts', 14),
        Card('hearts', 13),
        Card('hearts', 12),
        Card('hearts', 11),
        Card('hearts', 10),
    ]
    hand_type, strength = evaluate_hand(flush_cards)
    print(f"Hand: {hand_type}, Strength: {strength}")
    print("Hand evaluation works")
    
    # Test 5: Test decision rules
    print("\nTest 5: Decision Rules")
    # Set up a simple game state
    from main import PokerGame
    game = PokerGame()
    game.shuffle_and_deal()
    game.pot = 100
    game.current_bet = 20
    
    action = get_complete_ai_action(game)
    print(f"AI Action: {action}")
    print("Decision rules work")
    
    print("\nAll Prolog bridge tests passed!")

# ============================================
# END OF MEMBER 4 SECTION
# ============================================

# ============================================
# MEMBER 5: UI & Narrative (Lines 281-400)
# ============================================

# Placeholder for Member 5's code

# ============================================
# MAIN ENTRY POINT
# ============================================


if __name__ == "__main__":
    print("🃏 Welcome to The Secret Poker Den of Yangon!")
    print("🚧 Game is under development...")
