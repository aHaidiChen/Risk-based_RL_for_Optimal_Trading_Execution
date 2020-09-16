import random
from enviroment.action_state import ActionState

class QLearn:
    """Qlearner."""

    def __init__(self, actions, epsilon=0.1, alpha=0.1, gamma=0.1, exploration_decay=1.000001):
        """Initialize Q-table and assign parameters."""
        self.q = {}
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma
        self.exploration_decay = exploration_decay
        self.actions = actions

    def getQ(self, state, action, default=0.0):
        """Q-value lookup for state and action,  or else returns default."""
        return self.q.get((state, action), default)

    def getQAction(self, state, default=0.0):
        """Best action based on Q-Table for given state."""
        values = []
        for x in list(reversed(self.actions)):
            q_value = self.q.get((state, x), 0.0)
            #if q_value is not 0.0:
            values.append(q_value)
            # else:
            #    raise Exception("Q-Table does not contain: " + str((state, x)))

        if len(values) == 0:
            return default

        maxQ = max(values)
        a = list(reversed(self.actions))[values.index(maxQ)]
        return a

    def learnQ(self, state, action, reward, value):
        oldv = self.q.get((state, action), 0.0)
        if oldv is 0.0:
            self.q[(state, action)] = reward
        else:
            self.q[(state, action)] = oldv + self.alpha * (value - oldv)

    def learn(self, state1, action1, reward, state2):
        maxqnew = max([self.getQ(state2, a) for a in self.actions])
        self.learnQ(state1, action1, reward, reward + self.gamma * maxqnew)

    def chooseAction(self, state, return_q=False):
        """Chooses most rewarding action."""
        self.epsilon = max(self.exploration_decay * self.epsilon, 0.1)

        if random.random() > self.epsilon:
            action = random.choice(self.actions)
        else:
            q = [self.getQ(state, a) for a in self.actions]
            maxQ = max(q)
            count = q.count(maxQ)
            if count > 1:
                best = [i for i in range(len(self.actions)) if q[i] == maxQ]
                i = random.choice(best)
            else:
                i = q.index(maxQ)

            action = self.actions[i]
        return action
