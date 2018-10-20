from collections import defaultdict, Counter
from isolation import DebugState
import pickle
f = open("data.pickle", 'rb')
book = pickle.load(f)
from isolation import Isolation
state = Isolation()
if state in book:
    print("empty state is in data.pickle")
    # first move
    action = book[state]
    print("The best action for an empty board is ", action)
    state = state.result(action)
    debug_board = DebugState.from_state(state)
    print("Board after first move")
    print(debug_board)
    # best response
    action = book[state]
    print("The best response for it from the opponent is ", action)
    state = state.result(action)
    debug_board = DebugState.from_state(state)
    print("Board after the response")
    print(debug_board)
else:
    print("empty state is NOT found in data.pickle")
