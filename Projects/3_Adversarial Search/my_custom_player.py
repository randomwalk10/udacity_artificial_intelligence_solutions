
from sample_players import DataPlayer
from collections import defaultdict, Counter
import pickle
import random


class CustomPlayer(DataPlayer):
    """ Implement your own agent to play knight's Isolation

    The get_action() method is the only *required* method. You can modify
    the interface for get_action by adding named parameters with default
    values, but the function MUST remain compatible with the default
    interface.

    **********************************************************************
    NOTES:
    - You should **ONLY** call methods defined on your agent class during
      search; do **NOT** add or call functions outside the player class.
      The isolation library wraps each method of this class to interrupt
      search when the time limit expires, but the wrapper only affects
      methods defined on this class.

    - The test cases will NOT be run on a machine with GPU access, nor be
      suitable for using any other machine learning techniques.
    **********************************************************************
    """
    def get_action(self, state):
        """ Employ an adversarial search technique to choose an action
        available in the current state calls self.queue.put(ACTION) at least

        This method must call self.queue.put(ACTION) at least once, and may
        call it as many times as you want; the caller is responsible for
        cutting off the function after the search time limit has expired.

        See RandomPlayer and GreedyPlayer in sample_players for more examples.

        **********************************************************************
        NOTE:
        - The caller is responsible for cutting off search, so calling
          get_action() from your own code will create an infinite loop!
          Refer to (and use!) the Isolation.play() function to run games.
        **********************************************************************
        """
        # TODO: Replace the example implementation below with your own search
        #       method by combining techniques from lecture
        #
        # EXAMPLE: choose a random move without any search--this function MUST
        #          call self.queue.put(ACTION) at least once before time
        #          expires (the timer is automatically managed for you)
        # import random
        # self.queue.put(random.choice(state.actions()))

        # initialize and load data.pickle
        NUM_ROUNDS = 10
        if not self.data:
            self.data = defaultdict(Counter)

        # run openbook of depth level = 4
        for _ in range(NUM_ROUNDS):
            self.build_tree(state)

        # return an action of current state with the highest reward
        self.queue.put(max(self.data[state], key=self.data[state].get))

    def __del__(self):
        if self.data:
            filename = "data.pickle"
            f = open(filename, 'wb')
            pickle.dump(self.data, f)
            f.close()

    def build_tree(self, state, depth=4):
        """randomly choose an action from current state, until the game
        terminates or reaches the maximum depth level, and update this action
        at this state with the estimated reward, calculated by function
        "simulate"

        :state: game state
        :book: dictionary that maps state and action to reward(integer)
        :depth: search depth level(>=0)
        :returns: reward to the upper level(the other player)

        """
        # check if depth level reaches zero or game terminates
        if depth <= 0 or state.terminal_test():
            return -self.simulate(state)
        # randomly choose an action from current state
        action = random.choice(state.actions())
        # search into subtrees and get the reward for state and action
        reward = self.build_tree(state.result(action), depth-1)
        self.data[state][action] += reward
        # return -reward for upper level(the other player)
        return -reward

    def simulate(self, state):
        """randomly search down through game tree from current state,
        until the game terminates, return +1 if the active player of
        current state wins, -1 otherwise

        :state: game state
        :returns: reward(+1 if the active player of current state wins,
        -1 otherwise

        """
        player_id = state.player()
        while not state.terminal_test():
            state = state.result(random.choice(state.actions()))
        return -1 if state.utility(player_id) < 0 else 1
