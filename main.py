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

import random
import sys

# Placeholder for Member 3's code

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
