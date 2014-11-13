def print_soduko(puzzle, print_lists = False):
    l = ['-------------------\n']
    for row in range(len(puzzle)):
        l.append('|')
        for col in range(len(puzzle)):
            entry = puzzle[row][col]
            if isinstance(entry, list):
                if print_lists:
                    l.append(str(entry))
                else:
                    l.append(' ')
            else:
                l.append(str(entry))
            if (col+1)%3 == 0:
                l.append('|')
            else:
                l.append(' ')
        l.append('\n')
        if (row+1)%3 == 0:
            l.append('-------------------\n')
    print ''.join(l)

def possible_values(puzzle, row, col):
    """Finds the values that an entry may take"""
    # Find values that are certain (not in a list)
    r_vals = [val for val in puzzle[row] if not isinstance(val, list)]
    c_vals = [r[col] for r in puzzle if not isinstance(r[col], list)]
    s_vals = []
    for r in range(3):
        for c in range(3):
            entry = puzzle[(row//3)*3 + r][(col//3)*3 + c]
            if not isinstance(entry, list):
                s_vals.append(entry)
    # Make sets of those values
    r_set = set(r_vals)
    c_set = set(c_vals)
    s_set = set(s_vals)
    # Get inverse of those (i.e. posible values)
    taken_values_set = (r_set.union(c_set)).union(s_set)
    posible_set = set(range(1,10)).difference(taken_values_set)
    if len(posible_set) == 0:
        return None
    elif len(posible_set) == 1:
        return posible_set.pop()
    else:
        return list(posible_set)

def copy_puzzle(puzzle):
    new_puzzle = []
    for r in puzzle:
        new_puzzle.append(list(r))
    return  new_puzzle

def finished(puzzle):
    return all([all([isinstance(e, int) for e in r]) for r in puzzle])

def solve(puzzle):
    # Check puzzle size
    assert len(puzzle) == 9
    assert all(len(column) == 9 for column in puzzle)

    # Check if the puzzle is finished
    if finished(puzzle):
        return puzzle

    # Do a deterministic step
    stuck = False
    while not stuck:
        stuck = True
        for row in range(len(puzzle)):
            for col in range(len(puzzle)):
                if isinstance(puzzle[row][col], list):
                    p_vals = possible_values(puzzle, row, col)
                    # If there is no possible values the given soduko is infeasible
                    if p_vals is None:
                        return None
                    puzzle[row][col] = p_vals
                    if not isinstance(p_vals, list):
                        stuck = False
    if finished(puzzle):
        return puzzle

    # If that didn't solve it, do a guess
    ## Find a branch point
    branch = None
    for row in range(len(puzzle)):
        for col in range(len(puzzle)):
            if isinstance(puzzle[row][col], list):
                branch = {'row':row, 'col':col}
                branch['values'] = possible_values(puzzle, row, col)
                break
        if branch is not None:
            break

    ## Call solve recursively at the branch point
    for v in branch['values']:
        puzzle_copy = copy_puzzle(puzzle)
        puzzle_copy[branch['row']][branch['col']] = v
        solved_puzzle = solve(puzzle_copy)
        if solved_puzzle is not None:
            return solved_puzzle
