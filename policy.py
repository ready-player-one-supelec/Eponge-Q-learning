

class Policy():
    def __init__(self):
        self.end = False
    
    def init_Q(self, Qfunction):
        self.Qfunction = Qfunction
    
    def reset(self):
        self.end = False

class MostGain(Policy):
    def __init__(self, min_value, max_value):
        Policy.__init__(self)
        self.score = 0
        self.min_value = min_value
        self.max_value = max_value
    
    def reset(self):
        self.end = False
        self.score = 0
    
    def is_over(self):
        self.score += self.Qfunction.current_state.reward
        return self.score <= self.min_value or self.score >= self.max_value
    
    def hasFailed(self):
        return self.score <= self.min_value

class DeadOrAlive(Policy):
    def __init__(self, min_value, max_value):
        Policy.__init__(self)
        self.min_value = min_value
        self.max_value = max_value

    
    def is_over(self):
        #le jeu est terminé si on a rencontré soit un état gagnant, soit un état perdant
        self.end = self.Qfunction.current_state.reward == self.min_value or self.Qfunction.current_state.reward == self.max_value
        return self.end
    
    def hasFailed(self):
        return self.Qfunction.current_state.reward == self.min_value
