import Rubik
from collections import deque

def prettify_cube_list(cube_list):
    if not cube_list:
        raise Exception("Empty cube_list provided")
    return [Rubik.perm_to_string_dict[m] for m in cube_list]

def cube_bfs(goal, condition_function):
    visited = deque()
    visited.append((goal, []))
    while len(visited) < 2:
        next_cube = visited.popleft()
        print("popped ", visited)
        for m in Rubik.moves:
            moves = next_cube[1] + [m]
            new_cube = Rubik.perm_apply(m, next_cube[0])
            print("1 new_cube ", new_cube)
            print("2 result ", condition_function(new_cube))
            print("2.5 prettity", prettify_cube_list(moves))
            if condition_function(new_cube):
                return moves[1]
            visited.append((new_cube, moves))
            print("3 v", visited)
    return None

def stage_one(cube):
    return cube_bfs(cube, Rubik.check_edge_orientation)

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
            if Rubik.check_edge_orientation(new_cube):
                return [moves[1]]
            visited.append((new_cube, moves))
    return None


if __name__ == "__main__":
    scramble = [Rubik.F, Rubik.R, Rubik.Bi]
    scrambled = Rubik.multiple_perm_apply(scramble, Rubik.I)
    solution = stage_one(Rubik.multiple_perm_apply(scramble, Rubik.I))
    print(prettify_cube_list(solution))

