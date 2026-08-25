% ==============================================
% MEMBER 1: CARD FACTS (All 52 cards)
% Naming format: card_{rank}{suit}
% Suits: h=hearts, d=diamonds, c=clubs, s=spades
% Ranks: 2-10, j=jack, q=queen, k=king, a=ace
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

% 1. Check if all cards in a list are unique (no duplicates)
all_different([]).
all_different([H|T]) :-
    not(member(H, T)),
    all_different(T).

% 2. Built-in 'member' usually exists, but we define it explicitly just in case.
member(X, [X|_]).
member(X, [_|T]) :- member(X, T).

% 3. Generate all possible 5-card combinations from a 7-card list.
%    Usage: combination(5, [7 cards], [Resulting 5 cards]).
combination(0, _, []).
combination(N, [H|T], [H|R]) :-
    N > 0,
    N1 is N - 1,
    combination(N1, T, R).
combination(N, [_|T], R) :-
    N > 0,
    combination(N, T, R).

% ==============================================
% HAND DETECTION RULES
% ==============================================

% --- 1. PAIR (Two cards, same rank) ---
has_pair(C1, C2) :-
    card(C1, _, R),
    card(C2, _, R),
    C1 \= C2.

% --- 2. THREE OF A KIND ---
has_three_of_a_kind(C1, C2, C3) :-
    card(C1, _, R),
    card(C2, _, R),
    card(C3, _, R),
    all_different([C1, C2, C3]).

% --- 3. FOUR OF A KIND ---
has_four_of_a_kind(C1, C2, C3, C4) :-
    card(C1, _, R),
    card(C2, _, R),
    card(C3, _, R),
    card(C4, _, R),
    all_different([C1, C2, C3, C4]).

% --- 4. FLUSH (5 cards, same suit) ---
has_flush(C1, C2, C3, C4, C5) :-
    card(C1, Suit, _),
    card(C2, Suit, _),
    card(C3, Suit, _),
    card(C4, Suit, _),
    card(C5, Suit, _),
    all_different([C1, C2, C3, C4, C5]).

% --- 5. STRAIGHT (FIXED! Uses =:= for arithmetic comparison) ---
% Handles Ace-low straight (A,2,3,4,5) correctly.
has_straight(C1, C2, C3, C4, C5) :-
    card(C1, _, R1),
    card(C2, _, R2),
    card(C3, _, R3),
    card(C4, _, R4),
    card(C5, _, R5),
    all_different([C1, C2, C3, C4, C5]),
    sort([R1, R2, R3, R4, R5], Sorted),
    (   % Normal straight: Check if max - min = 4
        Sorted = [Min, _, _, _, Max],
        Max - Min =:= 4   % <--- FIXED! Use =:= instead of =
    ;   % Ace-low straight: [2, 3, 4, 5, 14]
        Sorted = [2, 3, 4, 5, 14]
    ).

% --- 6. FULL HOUSE (3 of a kind + 1 Pair) ---
has_full_house(C1, C2, C3, C4, C5) :-
    % Find the three of a kind
    has_three_of_a_kind(C1, C2, C3),
    % Find the pair using the remaining two cards
    has_pair(C4, C5),
    % Ensure ALL five cards are different
    all_different([C1, C2, C3, C4, C5]).

% --- 7. STRAIGHT FLUSH (Straight + Flush combined) ---
has_straight_flush(C1, C2, C3, C4, C5) :-
    has_straight(C1, C2, C3, C4, C5),
    has_flush(C1, C2, C3, C4, C5).

% ==============================================
% HAND RANKING (Higher number = Better hand)
% ==============================================

% Maps a hand type to a numeric strength (9 is best, 1 is worst)
hand_rank(straight_flush, 9).
hand_rank(four_of_a_kind, 8).
hand_rank(full_house, 7).
hand_rank(flush, 6).
hand_rank(straight, 5).
hand_rank(three_of_a_kind, 4).
hand_rank(two_pair, 3).
hand_rank(pair, 2).
hand_rank(high_card, 1).

% Helper to detect Two Pair (will be used by the evaluator)
has_two_pair(C1, C2, C3, C4, C5) :-
    has_pair(C1, C2),
    has_pair(C3, C4),
    all_different([C1, C2, C3, C4]),
    % The 5th card is a kicker, we just ignore it in the check.
    member(C5, [C1,C2,C3,C4]) ; true. % Dummy to satisfy arity, but we handle this better in the evaluator.

% ==============================================
% MASTER EVALUATOR: evaluate_hand(+All7Cards, -BestHandType)
% ==============================================

evaluate_hand(Cards, BestHand) :-
    % Step 1: Generate all possible 5-card combinations from the 7 cards
    findall(Combo, combination(5, Cards, Combo), Combos),
    % Step 2: Evaluate each combo and collect its rank
    maplist(evaluate_combo, Combos, HandTypes),
    % Step 3: Sort the hand types by strength (highest first)
    sort_hand_types(HandTypes, Sorted),
    % Step 4: The best hand is the first element in the sorted list
    Sorted = [BestHand|_].

% Evaluates a single 5-card combination and returns its hand type
evaluate_combo([C1,C2,C3,C4,C5], HandType) :-
    (   has_straight_flush(C1,C2,C3,C4,C5) -> HandType = straight_flush
    ;   has_four_of_a_kind(C1,C2,C3,C4) -> HandType = four_of_a_kind
    ;   has_full_house(C1,C2,C3,C4,C5) -> HandType = full_house
    ;   has_flush(C1,C2,C3,C4,C5) -> HandType = flush
    ;   has_straight(C1,C2,C3,C4,C5) -> HandType = straight
    ;   has_three_of_a_kind(C1,C2,C3) -> HandType = three_of_a_kind
    ;   (   has_pair(C1,C2), has_pair(C3,C4), all_different([C1,C2,C3,C4]) -> HandType = two_pair
        ;   has_pair(C1,C2) -> HandType = pair
        ;   HandType = high_card
        )
    ).

% Sorts a list of hand types by their numeric rank (descending)
sort_hand_types(HandTypes, Sorted) :-
    % Map each hand type to its rank
    maplist(hand_rank_to_pair, HandTypes, RankedPairs),
    % Sort by rank descending (higher number first)
    sort(1, @>=, RankedPairs, SortedPairs),
    % Extract only the hand types
    pairs_values(SortedPairs, Sorted).

% Helper to convert hand type to a key-value pair for sorting
hand_rank_to_pair(HandType, Rank-HandType) :-
    hand_rank(HandType, Rank).