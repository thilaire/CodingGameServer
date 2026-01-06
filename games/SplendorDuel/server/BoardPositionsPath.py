
"""Used to generate the list of positions on the board, following the path

Not used in the project anymore.
"""

directions = {
    "N": (-1, 0),
    "S": (1, 0),
    "E": (0, 1),
    "W": (0, -1)
}

boardCompletion = (
            ("E", "E", "E", "E", "S"),	    # North
            ("N", "E", "E", "S", "S"),	    # South
            ("N", "N", "S", "S", "S"),	    # East
            ("N", "N", "W", "S", "S"),	    # West
            ("N", "W", "W", "W", None)
)


# Used for browsing the board. Used to redistribute tokens (see SDGameHandler.redistribute())
def boardPositions():
    """Generator that returns successive positions on the board, following the path."""
    current = (2, 2)        # start with the center of the board
    while current != (4, 4):
        yield current
        dx, dy = directions[boardCompletion[current[0]][current[1]]]    # we follow the `path`
        current = current[0] + dx, current[1] + dy
    yield current



