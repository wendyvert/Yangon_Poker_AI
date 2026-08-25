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
