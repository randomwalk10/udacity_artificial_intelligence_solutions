
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
    def __init__(self, player_id, collect_data=True):
        super().__init__(player_id)
        self.collect_data = collect_data
        if self.collect_data and (not self.data):
            self.data = defaultdict(Counter)

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
            # check to collect statistical data or not
            if self.collect_data:
                # collect statistics and randomly choose an action
                action = random.choice(state.actions())
                self.build_tree(state, self.data,
                                NUM_OF_PLIES-state.ply_count, action)
                # save data
                filename = "data.pickle"
                f = open(filename, 'wb')
                pickle.dump(self.data, f)
                f.close()
            else:
                # read openning book
                # choose the estimated best action, or random action if N/A
                if self.data and state in self.data:
                    action = max(self.data[state], key=self.data[state].get)
                else:
                    action = random.choice(state.actions())
            # put random action into queue
            self.queue.put(action)
        else:
            self.queue.put(self.minimax(state, depth=3))
            pass

    def build_tree(self, state, book, depth=8, action=None):
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
        if not action:
            action = random.choice(state.actions())
        # search into subtrees and get the reward for state and action
        reward = self.build_tree(state.result(action), book, depth-1)
        book[state][action] += reward
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

    # directly use the same minimax implemented in sample_players.py
    def minimax(self, state, depth):

        def min_value(state, depth):
            if state.terminal_test(): return state.utility(self.player_id)
            if depth <= 0: return self.score(state)
            value = float("inf")
            for action in state.actions():
                value = min(value, max_value(state.result(action), depth - 1))
            return value

        def max_value(state, depth):
            if state.terminal_test(): return state.utility(self.player_id)
            if depth <= 0: return self.score(state)
            value = float("-inf")
            for action in state.actions():
                value = max(value, min_value(state.result(action), depth - 1))
            return value

        return max(state.actions(), key=lambda x: min_value(state.result(x), depth - 1))

    def score(self, state):
        own_loc = state.locs[self.player_id]
        opp_loc = state.locs[1 - self.player_id]
        own_liberties = state.liberties(own_loc)
        opp_liberties = state.liberties(opp_loc)
        return len(own_liberties) - len(opp_liberties)
