###################################
# build opening book
###################################

import random
import argparse
import textwrap
import pickle
from isolation import Isolation


NUM_PLIES = 4
NUM_ROUNDS = 100
FILENAME = "data.pickle"


# Print iterations progress
def printProgressBar (iteration, total, prefix='', suffix='',
                      decimals=1, length=100, fill='█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 *
                                                     (iteration /
                                                      float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end='\r')
    # Print New Line on Complete
    if iteration == total:
        print()


def build_table(num_rounds=NUM_ROUNDS, num_plies=NUM_PLIES):
    """build opening book return it as dictionary

    :num_rounds: number of build_tree to call
    :num_plies: number of plies for this opening book
    :returns: a dictionary mapping state to the best action

    """
    # init
    from collections import defaultdict, Counter
    book = defaultdict(Counter)
    # build
    printProgressBar(0, num_rounds, prefix = 'Progress:',
                     suffix = 'Complete', length = 50)
    for i in range(num_rounds):
        # build tree
        state = Isolation()
        build_tree(state, book, num_plies)
        # show progress
        printProgressBar(i + 1, num_rounds, prefix = 'Progress:',
                         suffix = 'Complete', length = 50)
    # return
    return {k: max(v, key=v.get) for k, v in book.items()}


def build_tree(state, book, depth=NUM_PLIES):
    if depth <= 0 or state.terminal_test():
        return -simulate(state)
    action = random.choice(state.actions())
    reward = build_tree(state.result(action), book, depth - 1)
    book[state][action] += reward
    return -reward


def simulate(state):
    player_id = state.player()
    while not state.terminal_test():
        state = state.result(random.choice(state.actions()))
    return -1 if state.utility(player_id) < 0 else 1


def main(args):
    filename = args.output
    assert isinstance(filename, str) and filename, \
        "invalid file name"
    num_rounds = args.rounds
    assert isinstance(num_rounds, int) and num_rounds > 0, \
        "invalid input for number of rounds"
    num_plies = args.depth
    assert isinstance(num_plies, int) and num_plies > 3, \
        "invalid input for number of plies, must be integer >3"

    print("build opening book with number of plies {} with {} rounds"
          " simulations".format(num_plies, num_rounds))
    book = build_table(num_rounds, num_plies)
    print("opening book is built")

    with open(filename, 'wb') as f:
        pickle.dump(book, f)
    print("data is saved into {}".format(filename))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="build opening book for isolation game",
        epilog=textwrap.dedent("""\
            Example Usage:
            --------------
            - Run 100 rounds and Save to "data.pickle" and Set
                               number of plies to 4(all by default)

                $python build_opening_book.py -r 100 -o data.pickle -d 4
        """)
    )
    parser.add_argument(
        '-r', '--rounds', type=int, default=NUM_ROUNDS,
        help="""\
            Choose the number of rounds to build openning book from empty state
        """
    )
    parser.add_argument(
        '-o', '--output', type=str, default=FILENAME,
        help="""\
            Choose the file name for the pickle data to store at
        """
    )
    parser.add_argument(
        '-d', '--depth', type=int, default=NUM_PLIES,
        help="""\
            Choose the number of plies for opening book
        """
    )

    main(parser.parse_args())
