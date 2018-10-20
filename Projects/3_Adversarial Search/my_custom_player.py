
from sample_players import DataPlayer
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
        NUM_OF_PLIES = 4
        if state.ply_count < NUM_OF_PLIES:
            # if self.data is None, randomly choose an action;
            # else, choose the action according to opening book
            if not self.data:
                # collect a random action
                action = random.choice(state.actions())
            else:
                # read openning book
                # choose the estimated best action, or random action if N/A
                if state in self.data:
                    action = self.data[state]
                else:
                    action = random.choice(state.actions())
            # put random action into queue
            self.queue.put(action)
        else:
            # choose an action according to minimax
            self.queue.put(self.minimax(state, depth=3))
            pass

    # directly use the same minimax implemented in sample_players.py
    def minimax(self, state, depth):

        def min_value(state, depth):
            if state.terminal_test():
                return state.utility(self.player_id)
            if depth <= 0:
                return self.score(state)
            value = float("inf")
            for action in state.actions():
                value = min(value, max_value(state.result(action), depth - 1))
            return value

        def max_value(state, depth):
            if state.terminal_test():
                return state.utility(self.player_id)
            if depth <= 0:
                return self.score(state)
            value = float("-inf")
            for action in state.actions():
                value = max(value, min_value(state.result(action), depth - 1))
            return value

        return max(state.actions(),
                   key=lambda x: min_value(state.result(x), depth - 1))

    def score(self, state):
        own_loc = state.locs[self.player_id]
        opp_loc = state.locs[1 - self.player_id]
        own_liberties = state.liberties(own_loc)
        opp_liberties = state.liberties(opp_loc)
        return len(own_liberties) - len(opp_liberties)


class BaselinePlayer(CustomPlayer):
    """
    BaselinePlayer is a subclass of CustomPlayer and is basically the same with
    the only difference that no open book data is loaded. Therefore a
    BaselinePlayer selects opening moves randomly.
    """
    def __init__(self, player_id):
        from sample_players import BasePlayer
        BasePlayer.__init__(self, player_id)
