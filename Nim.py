from random import randint

nimMax = 3
numPlayers = 2


def play_human(rows):
    row = int(input("Choose a row. (0 to %d)\n" % (len(rows) - 1)))
    while row < 0 or row >= len(rows):
        row = int(input("Try another one. (0 to %d)\n" % (len(rows) - 1)))
    print(rows[row])
    num = int(input("How many matches would you like to take?\n"))
    while num < 1 or num > 3 or num > rows[row]:
        num = int(input("Try again?\n"))
    return row, num


def play_random(rows):
    row = randint(0, len(rows) - 1)
    while rows[row] == 0:
        row = randint(0, len(rows) - 1)
    if rows[row] == 1:
        return row, 1
    return row, randint(1, min(3, rows[row]))


def play_perfect(rows):
    # first, map the game state onto the cyclic N^kxk tensor, where k = nimMax + 1
    lrows = [val % (nimMax+1) for val in rows]
    # zip with index for later, sort in ascending order
    lrows = sorted([val for val in enumerate(lrows)])
    # determine tensor index
    idx = tensor_index(lrows)
    if idx == 0:
        return lrows[-1][0], 1  # this is a losing position, take the minimal amount to prolong game
    else:
        return lrows[-1][0], idx  # this is a winning position, move opponent to losing position


def tensor_index(vals):
    idx = 0

    return idx


def game_round(rows, players, verbose):
    for idx, playFunction in enumerate(players):
        if all(row == 0 for row in rows):
            return idx  # player lost, return their ID
        row, num = playFunction(tuple(rows))  # players get a tuple so they don't mess with game state
        if num < 1 or num > 3 or num > rows[row]:
            raise ValueError("Invalid row/number combination! (row")
        rows[row] -= num
        if verbose > 0:
            print("Player %d took %d matches from %d:" % (idx, num, row))
            print(rows)
    return -1  # game continues


def game_play(rows, players, verbose=0):
    if verbose > 0:
        print("Game Start:")
        print(rows)
    result = game_round(rows, players, verbose)
    while result < 0:
        result = game_round(rows, players, verbose)
    if verbose > 0:
        print("Player %d lost." % result)
    return result


if __name__ == '__main__':
    rows = [int(x) for x in input("Please enter the number of matches per row (separated by spaces).\n").split()]
    while not all(row >= 0 for row in rows):
        rows = [int(x) for x in input('Try again. All numbers must be >= 0.\n').split()]
    playerList = [play_random, play_human, play_perfect]
    players = [playerList[int(p)] for p in input(
        "Choose players (type on same line separated by spaces):\n0: Random\n1: Human\n2: Perfect AI\n").split()]
    loser = game_play(rows, players, verbose=1)

