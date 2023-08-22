from player import Player
from word_correlator import WordCorrelator


def beginGame(correlator):

    print("Rules:\n(1) Only use present tense\n\nOkay, Let's Begin! I'm thinking of a word ....")
    correlator.setup_data()
    print(".... O.K. Got it!")
    

def endGame(player, correlator, win):
    if win:
        print("Wow congrats you won, the word was: ",  correlator.target)
    else:
        print("Sorry you lost, the word was: ",  correlator.target)
    
    # Check for high score
    player.add_score()




def main():

    # Initialize game objects
    player = Player()
    correlator = WordCorrelator()

    beginGame(correlator)

    # Game loop
    while True:
        player.incrementScore()
        score = correlator.doGuess()

        if score == 100:
            endGame(player, correlator, win=True)
            break
        
        if player.current_score == 100:
            print("Sorry, your 100 guesses are up")
            break
        pass 
    
if __name__ == "__main__":
    main()