% ==============================================
% THE SECRET POKER DEN OF YANGON
% Complete Prolog Logic (Hand Evaluation + AI Personalities)
% ==============================================

% ==============================================
% MEMBER 1: CARD FACTS (All 52 cards)
% ==============================================

% --- Hearts (h) ---
card(card_2h, hearts, 2).
card(card_3h, hearts, 3).
card(card_4h, hearts, 4).
card(card_5h, hearts, 5).
card(card_6h, hearts, 6).
card(card_7h, hearts, 7).
card(card_8h, hearts, 8).
card(card_9h, hearts, 9).
card(card_th, hearts, 10).
card(card_jh, hearts, 11).
card(card_qh, hearts, 12).
card(card_kh, hearts, 13).
card(card_ah, hearts, 14).

% --- Diamonds (d) ---
card(card_2d, diamonds, 2).
card(card_3d, diamonds, 3).
card(card_4d, diamonds, 4).
card(card_5d, diamonds, 5).
card(card_6d, diamonds, 6).
card(card_7d, diamonds, 7).
card(card_8d, diamonds, 8).
card(card_9d, diamonds, 9).
card(card_td, diamonds, 10).
card(card_jd, diamonds, 11).
card(card_qd, diamonds, 12).
card(card_kd, diamonds, 13).
card(card_ad, diamonds, 14).

% --- Clubs (c) ---
card(card_2c, clubs, 2).
card(card_3c, clubs, 3).
card(card_4c, clubs, 4).
card(card_5c, clubs, 5).
card(card_6c, clubs, 6).
card(card_7c, clubs, 7).
card(card_8c, clubs, 8).
card(card_9c, clubs, 9).
card(card_tc, clubs, 10).
card(card_jc, clubs, 11).
card(card_qc, clubs, 12).
card(card_kc, clubs, 13).
card(card_ac, clubs, 14).

% --- Spades (s) ---
card(card_2s, spades, 2).
card(card_3s, spades, 3).
card(card_4s, spades, 4).
card(card_5s, spades, 5).
card(card_6s, spades, 6).
card(card_7s, spades, 7).
card(card_8s, spades, 8).
card(card_9s, spades, 9).
card(card_ts, spades, 10).
card(card_js, spades, 11).
card(card_qs, spades, 12).
card(card_ks, spades, 13).
card(card_as, spades, 14).

% ==============================================
% HELPER PREDICATES
% ==============================================

all_different([]).
all_different([H|T]) :- not(member(H, T)), all_different(T).

member(X, [X|_]).
member(X, [_|T]) :- member(X, T).

combination(0, _, []).
combination(N, [H|T], [H|R]) :- N > 0, N1 is N - 1, combination(N1, T, R).
combination(N, [_|T], R) :- N > 0, combination(N, T, R).

% ==============================================
% MEMBER 1: HAND DETECTION RULES
% ==============================================

has_pair(C1, C2) :- card(C1, _, R), card(C2, _, R), C1 \= C2.

has_three_of_a_kind(C1, C2, C3) :- 
    card(C1, _, R), card(C2, _, R), card(C3, _, R), all_different([C1, C2, C3]).

has_four_of_a_kind(C1, C2, C3, C4) :- 
    card(C1, _, R), card(C2, _, R), card(C3, _, R), card(C4, _, R), all_different([C1, C2, C3, C4]).

has_flush(C1, C2, C3, C4, C5) :- 
    card(C1, Suit, _), card(C2, Suit, _), card(C3, Suit, _), card(C4, Suit, _), card(C5, Suit, _), all_different([C1, C2, C3, C4, C5]).

has_straight(C1, C2, C3, C4, C5) :-
    card(C1, _, R1), card(C2, _, R2), card(C3, _, R3), card(C4, _, R4), card(C5, _, R5),
    all_different([C1, C2, C3, C4, C5]),
    sort([R1, R2, R3, R4, R5], Sorted),
    ( Sorted = [Min, _, _, _, Max], Max - Min =:= 4 ; Sorted = [2, 3, 4, 5, 14] ).

has_full_house(C1, C2, C3, C4, C5) :- 
    has_three_of_a_kind(C1, C2, C3), has_pair(C4, C5), all_different([C1, C2, C3, C4, C5]).

has_straight_flush(C1, C2, C3, C4, C5) :- 
    has_straight(C1, C2, C3, C4, C5), has_flush(C1, C2, C3, C4, C5).

% ==============================================
% MEMBER 1: HAND RANKING
% ==============================================

hand_rank(straight_flush, 9).
hand_rank(four_of_a_kind, 8).
hand_rank(full_house, 7).
hand_rank(flush, 6).
hand_rank(straight, 5).
hand_rank(three_of_a_kind, 4).
hand_rank(two_pair, 3).
hand_rank(pair, 2).
hand_rank(high_card, 1).

% ==============================================
% MEMBER 1: MASTER EVALUATOR
% ==============================================

evaluate_hand(Cards, BestHand) :-
    findall(Combo, combination(5, Cards, Combo), Combos),
    maplist(evaluate_combo, Combos, HandTypes),
    sort_hand_types(HandTypes, Sorted),
    Sorted = [BestHand|_].

evaluate_combo([C1,C2,C3,C4,C5], HandType) :-
    ( has_straight_flush(C1,C2,C3,C4,C5) -> HandType = straight_flush
    ; has_four_of_a_kind(C1,C2,C3,C4) -> HandType = four_of_a_kind
    ; has_full_house(C1,C2,C3,C4,C5) -> HandType = full_house
    ; has_flush(C1,C2,C3,C4,C5) -> HandType = flush
    ; has_straight(C1,C2,C3,C4,C5) -> HandType = straight
    ; has_three_of_a_kind(C1,C2,C3) -> HandType = three_of_a_kind
    ; ( has_pair(C1,C2), has_pair(C3,C4), all_different([C1,C2,C3,C4]) -> HandType = two_pair
      ; has_pair(C1,C2) -> HandType = pair
      ; HandType = high_card )
    ).

sort_hand_types(HandTypes, Sorted) :-
    maplist(hand_rank_to_pair, HandTypes, RankedPairs),
    sort(1, @>=, RankedPairs, SortedPairs),
    pairs_values(SortedPairs, Sorted).

hand_rank_to_pair(HandType, Rank-HandType) :- hand_rank(HandType, Rank).

% ==============================================
% MEMBER 2: AI PERSONALITIES & DECISION RULES
% ==============================================

% Dynamic game state (updated by Python)
:- dynamic pot_size/1.
:- dynamic current_bet/1.
:- dynamic community_cards/3.

% AI Profiles
player_profile(htun_myat, trickster).
player_profile(nay_yan, silent).
player_profile(mary, reader).
player_profile(thiri, challenger).
player_profile(phoo_ngone, anchor).

% Helper: hand strength category
hand_category(HandType, very_strong) :- hand_rank(HandType, R), R >= 8.
hand_category(HandType, strong)      :- hand_rank(HandType, R), R >= 6, R < 8.
hand_category(HandType, medium)      :- hand_rank(HandType, R), R >= 4, R < 6.
hand_category(HandType, weak)        :- hand_rank(HandType, R), R < 4.

% Decision Rules based on Personality

% 1. Trickster (Htun Myat) - Bluffs frequently
decide_action(htun_myat, HandType, raise) :-
    hand_category(HandType, Category),
    ( Category = weak -> random(0.6) ; true ). % 60% bluff chance

% 2. Silent (Nay Yan) - Only calls, rarely raises
decide_action(nay_yan, HandType, call) :- hand_category(HandType, Category), Category \= weak.
decide_action(nay_yan, _, check).

% 3. Reader (Mary) - Aggressive when strong
decide_action(mary, HandType, raise) :- hand_category(HandType, Category), Category = very_strong.
decide_action(mary, HandType, call)  :- hand_category(HandType, Category), Category = strong.
decide_action(mary, _, check).

% 4. Challenger (Thiri) - Always raises if not weak
decide_action(thiri, HandType, raise) :- hand_category(HandType, Category), Category \= weak.
decide_action(thiri, _, check).

% 5. Anchor (Phoo Ngone) - Cautious, only plays strong hands
decide_action(phoo_ngone, HandType, raise) :- hand_category(HandType, Category), Category = very_strong.
decide_action(phoo_ngone, HandType, call)  :- hand_category(HandType, Category), Category = strong.
decide_action(phoo_ngone, _, fold).

% Default fallback
decide_action(_, _, check).

% Random helper (0 to 1)
random(Value) :- random(R), R < 0.6.