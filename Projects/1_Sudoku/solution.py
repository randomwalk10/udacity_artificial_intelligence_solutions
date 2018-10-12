
from utils import *


row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units

# TODO: Update the unit list to add the new diagonal units
unitlist.append([r+c for r, c in zip(rows, cols)])
unitlist.append([r+c for r, c in zip(rows, list(reversed(cols)))])


# Must be called after all units (including diagonals) are added to the unitlist
units = extract_units(unitlist, boxes)
peers = extract_peers(units, boxes)


def naked_twins(values):
    """Eliminate values using the naked twins strategy.

    The naked twins strategy says that if you have two or more unallocated boxes
    in a unit and there are only two digits that can go in those two boxes, then
    those two digits can be eliminated from the possible assignments of all other
    boxes in the same unit.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the naked twins eliminated from peers

    Notes
    -----
    Your solution can either process all pairs of naked twins from the input once,
    or it can continue processing pairs of naked twins until there are no such
    pairs remaining -- the project assistant test suite will accept either
    convention. However, it will not accept code that does not process all pairs
    of naked twins from the original input. (For example, if you start processing
    pairs of twins and eliminate another pair of twins before the second pair
    is processed then your code will fail the PA test suite.)

    The first convention is preferred for consistency with the other strategies,
    and because it is simpler (since the reduce_puzzle function already calls this
    strategy repeatedly).
    """
    # TODO: Implement this function!
    for unit in unitlist:
        pair_dict = {}
        # collect two pairs
        for box in unit:
            if len(values[box])==2:
                if values[box] in pair_dict:
                    pair_dict[values[box]].append(box)
                    pass
                else:
                    pair_dict[values[box]] = [box]
                    pass
                pass
            pass
        # eliminate digits in two pairs in other boxes of the same unit
        for pair in pair_dict.keys():
            if len(pair_dict[pair])>=2:
                reserved_boxes = pair_dict[pair][:2]
                for box in set(unit)-set(reserved_boxes):
                    values[box] = values[box].replace(pair[0],'')
                    values[box] = values[box].replace(pair[1],'')
                    pass
                pass
            pass
        pass
    return values


def eliminate(values):
    """Apply the eliminate strategy to a Sudoku puzzle

    The eliminate strategy says that if a box has a value assigned, then none
    of the peers of that box can have the same value.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the assigned values eliminated from peers
    """
    # TODO: Copy your code from the classroom to complete this function
    for key in values.keys():
        if 1==len(values[key]):
            neighbors = peers[key]
            for neighbor in neighbors:
                values[neighbor] = values[neighbor].replace(values[key], '')
                pass
            pass
        pass
    return values


def only_choice(values):
    """Apply the only choice strategy to a Sudoku puzzle

    The only choice strategy says that if only one box in a unit allows a certain
    digit, then that box must be assigned that digit.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with all single-valued boxes assigned

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    """
    # TODO: Copy your code from the classroom to complete this function
    for unit in unitlist:
        frequency_table = {}
        for box in unit:
            for number in values[box]:
                if number in frequency_table:
                    frequency_table[number] += 1
                    pass
                else:
                    frequency_table[number] = 1
                    pass
                pass
            pass
        for number in frequency_table:
            if frequency_table[number] == 1:
                for box in unit:
                    if number in values[box]:
                        values[box] = number
                        break;
                    pass
                pass
            pass
        pass
    return values


def reduce_puzzle(values):
    """Reduce a Sudoku puzzle by repeatedly applying all constraint strategies

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary after continued application of the constraint strategies
        no longer produces any changes, or False if the puzzle is unsolvable
    """
    # TODO: Copy your code from the classroom and modify it to complete this function
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Your code here: Use the Eliminate Strategy
        values = eliminate(values)

        # Your code here: Use the Only Choice Strategy
        values = only_choice(values)

        # Use naked pair Strategy
        values = naked_twins(values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    """Apply depth first search to solve Sudoku puzzles in order to solve puzzles
    that cannot be solved by repeated reduction alone.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary with all boxes assigned or False

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    and extending it to call the naked twins strategy.
    """
    # TODO: Copy your code from the classroom to complete this function
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if not values:
        return False

    # Choose one of the unfilled squares with the fewest possibilities
    min_len_unfilled = 1
    search_box = 'A1'
    for box in values.keys():
        if len(values[box])>1:
            if min_len_unfilled==1 or len(values[box])<min_len_unfilled:
                min_len_unfilled = len(values[box])
                search_box = box
                pass
            pass
        pass
    if min_len_unfilled==1:
        return values

    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    digits = values[search_box]
    for digit in digits:
        temp = values.copy()
        temp[search_box] = digit
        temp = search(temp)
        if temp:
            return temp
        pass

    # If you're stuck, see the solution.py tab!
    return False


def solve(grid):
    """Find the solution to a Sudoku puzzle using search and constraint propagation

    Parameters
    ----------
    grid(string)
        a string representing a sudoku grid.

        Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

    Returns
    -------
    dict or False
        The dictionary representation of the final sudoku grid or False if no solution exists.
    """
    values = grid2values(grid)
    values = search(values)
    return values


if __name__ == "__main__":
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(grid2values(diag_sudoku_grid))
    result = solve(diag_sudoku_grid)
    display(result)

    try:
        import PySudoku
        PySudoku.play(grid2values(diag_sudoku_grid), result, history)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
