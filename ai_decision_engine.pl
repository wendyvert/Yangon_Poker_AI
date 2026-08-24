% =====================================================================
% FILENAME: poker_logic.pl
% PROJECT: Myanmar Poker Club (5 AI + 1 Human Dynamic Board)
% TEAM MEMBER: Member 2 (Opponent Profiling & Decision Rules)
% ---------------------------------------------------------------------
% INPUT FROM PYTHON (Member 4):
% Player, HandStrength (0.0 to 1.0), PotSize, ToCall, 
% OpponentBets (A list containing the Human's bet history)
% ---------------------------------------------------------------------
% OUTPUT TO PYTHON:
% Action (call/raise/fold/all_in), Amount, Reason
% =====================================================================

% 1. PLAYER PROFILES (Fixed Personalities)
player_profile(htun_myat, trickster).   % Unpredictable, Bluffer
player_profile(nay_yan, silent_bet).    % Calm, Hard to read, Patient
player_profile(mary, reader).           % Observant, Reads patterns
player_profile(thiri, challenger).      % Aggressive, Loves pressure
player_profile(phoo_ngone, anchor).     % Practical, Stubborn, Plays safe

% --- HTUN MYAT (The Trickster) ---
% He plays mind games and bluffs randomly, but changes rhythm.
action(htun_myat, HandStrength, PotSize, ToCall, OpponentBets, Action, Amount, Reason) :-
    random(1, 100, R),
    ( R > 70 ->
        Action = raise, Amount is PotSize * 0.5, 
        Reason = 'Htun Myat is playing mind games and bluffing!'
    ; HandStrength > 0.8 ->
        Action = raise, Amount is PotSize * 0.2, 
        Reason = 'Htun Myat caught a strong hand and is setting a trap!'
    ; HandStrength < 0.3, ToCall > PotSize / 3 ->
        Action = fold, 
        Reason = 'Htun Myat got bored and folded.'
    ; Action = call, 
      Reason = 'Htun Myat is changing the rhythm, just calling.'
    ).

% --- NAY YAN (The Silent Bet) ---
% Extremely tight, waits for the perfect hand. Ignores the Human's bets.
action(nay_yan, HandStrength, PotSize, ToCall, _, Action, Amount, Reason) :-
    ( HandStrength > 0.85 ->
        Action = raise, Amount is PotSize * 0.5, 
        Reason = 'Nay Yan finally has the perfect hand!'
    ; HandStrength > 0.6 ->
        Action = call, 
        Reason = 'Nay Yan is quietly waiting for the perfect time.'
    ; Action = fold, 
      Reason = 'Nay Yan stays silent and folds.'
    ).

% --- MARY (The Reader) ---
% Reads the HUMAN's patterns. If the Human bets 3 or more times, she knows they are strong.
action(mary, HandStrength, PotSize, ToCall, OpponentBets, Action, Amount, Reason) :-
    ( length(OpponentBets, Len), Len >= 3 ->
        Action = fold, 
        Reason = 'Mary has read the Human player pattern and backs off.'
    ; HandStrength > 0.75 ->
        Action = raise, Amount is PotSize * 0.4, 
        Reason = 'Mary knows she has the winning information.'
    ; HandStrength < 0.45 ->
        Action = fold, 
        Reason = 'Mary does not trust this hand.'
    ; Action = call, 
      Reason = 'Mary is quietly reading the board.'
    ).

% --- THIRI (The Challenger) ---
% Aggressive. She loves putting pressure on the Human to steal the pot.
action(thiri, HandStrength, PotSize, ToCall, _, Action, Amount, Reason) :-
    ( HandStrength > 0.4 ->
        Action = raise, Amount is PotSize * 0.6, 
        Reason = 'Thiri is putting immense pressure on the Human to steal the big pot!'
    ; Action = fold, 
      Reason = 'Thiri hates this hand, but she will be back for revenge.'
    ).

% --- PHOO NGONE (The Anchor) ---
% Plays completely safe. She ignores the Human and only cares about her own cards.
action(phoo_ngone, HandStrength, PotSize, ToCall, _, Action, Amount, Reason) :-
    ( HandStrength > 0.95 ->
        Action = all_in, Amount is ToCall + PotSize, 
        Reason = 'Phoo Ngone is stubbornly going all-in with a monster hand!'
    ; HandStrength > 0.65 ->
        Action = call, 
        Reason = 'Phoo Ngone plays safe and calls.'
    ; Action = fold, 
      Reason = 'Phoo Ngone is practical and folds.'
    ).

% --- DEFAULT SAFETY NET (If no specific rule matches, prevents crashing) ---
action(_, HandStrength, _, ToCall, _, Action, 0, Reason) :-
    ( HandStrength > 0.6, ToCall =< 10 ->
        Action = call, 
        Reason = 'Generic AI decision: Calling due to decent hand.'
    ; Action = fold, 
      Reason = 'Generic AI decision: Folding.'
    ).