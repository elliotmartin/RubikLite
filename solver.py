import Rubik
from collections import deque

def prettify_cube_list(cube_list):
    return [Rubik.perm_to_string_dict[m] for m in cube_list]

def fix_edge_orientation(cube):
    """
    Given a starting position, output a sequence of moves that when applied to cube solve the edge orientation
    This is traversing from G0 to G1 in Thistlethwaite's Algorithm
    :param cube: starting position
    :return: list of moves
    """

    visited = deque()
    visited.append((cube,[]))
    while visited:
        next_cube = visited.popleft()
        for m in Rubik.moves:
            moves = next_cube[1] + [m]
            new_cube = Rubik.perm_apply(m, next_cube[0])
            if Rubik.check_edge_orientation((new_cube)):
                return [moves[1]]
            visited.append((new_cube, moves))
    return None


if __name__ == "__main__":
    scramble = [Rubik.F, Rubik.R, Rubik.Bi]
    scrambled = Rubik.multiple_perm_apply(scramble, Rubik.I)
    #print(Rubik.check_edge_orientation(scrambled))
    solution = fix_edge_orientation(Rubik.multiple_perm_apply(scramble, Rubik.I))
    print(prettify_cube_list(solution))
    #if type(solution) != str and type(solution):
    #    print(prettify_cube_list(solution))

