from Rubik import *
import queue

def fix_edge_orientation(cube):
    """
    Given a starting position, output a sequence of moves that when applied to cube solve the edge orientation
    This is traversing from G0 to G1 in Thistlethwaite's Algorithm
    :param cube: starting position
    :return: list of moves
    """

    q = queue
    visited = [cube]