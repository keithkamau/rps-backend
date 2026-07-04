class GameLogic:
    CHOICES = ['rock', 'paper', 'scissors']
    
    WINNING_COMBOS = {
        'rock': 'scissors',
        'paper': 'rock',
        'scissors': 'paper'
    }
    
    @staticmethod
    def validate_choice(choice):
        return choice in GameLogic.CHOICES
    
    @staticmethod
    def determine_winner(choice1, choice2):
        if not choice1 or not choice2:
            return None
        
        if choice1 == choice2:
            return 'tie'
        
        if GameLogic.WINNING_COMBOS[choice1] == choice2:
            return 'player1'
        
        return 'player2'
    
    @staticmethod
    def determine_forfeit_winner(player1_choice, player2_choice):
        # Handle forfeit scenarios
        if player1_choice and not player2_choice:
            return 'player1'
        elif player2_choice and not player1_choice:
            return 'player2'
        elif not player1_choice and not player2_choice:
            return 'double_forfeit'
        return None