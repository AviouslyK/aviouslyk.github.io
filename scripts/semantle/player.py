class Player:
    def __init__(self):
        self.high_scores = [0,0,0,0,0]
        self.current_score = 0
    
    def incrementScore(self):
        self.current_score = self.current_score + 1

    def add_score(self):
        score = 100 - self.current_score
        new_high_scores = [l for l in self.high_scores if l > score]
        # Check if we have a new high score
        if len(new_high_scores) < 5:
            self.high_scores.append(score)
            self.high_scores = sorted(self.high_scores, reverse=True)
            self.high_scores = self.high_scores[:5]
            print("New High Score!")
            print(self.high_scores)

    