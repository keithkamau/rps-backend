from app.services.game_logic import GameLogic

def test_validate_choice_valid():
    assert GameLogic.validate_choice('rock') == True
    assert GameLogic.validate_choice('paper') == True
    assert GameLogic.validate_choice('scissors') == True

def test_validate_choice_invalid():
    assert GameLogic.validate_choice('lizard') == False
    assert GameLogic.validate_choice('') == False
    assert GameLogic.validate_choice(None) == False

def test_rock_beats_scissors():
    assert GameLogic.determine_winner('rock', 'scissors') == 'player1'
    assert GameLogic.determine_winner('scissors', 'rock') == 'player2'

def test_paper_beats_rock():
    assert GameLogic.determine_winner('paper', 'rock') == 'player1'
    assert GameLogic.determine_winner('rock', 'paper') == 'player2'

def test_scissors_beats_paper():
    assert GameLogic.determine_winner('scissors', 'paper') == 'player1'
    assert GameLogic.determine_winner('paper', 'scissors') == 'player2'

def test_tie():
    assert GameLogic.determine_winner('rock', 'rock') == 'tie'
    assert GameLogic.determine_winner('paper', 'paper') == 'tie'
    assert GameLogic.determine_winner('scissors', 'scissors') == 'tie'

def test_forfeit_player1_wins():
    assert GameLogic.determine_forfeit_winner('rock', None) == 'player1'
    assert GameLogic.determine_forfeit_winner('paper', None) == 'player1'

def test_forfeit_player2_wins():
    assert GameLogic.determine_forfeit_winner(None, 'scissors') == 'player2'

def test_double_forfeit():
    assert GameLogic.determine_forfeit_winner(None, None) == 'double_forfeit'

def test_determine_winner_with_none():
    assert GameLogic.determine_winner(None, 'rock') is None
    assert GameLogic.determine_winner('paper', None) is None