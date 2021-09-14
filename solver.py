import Rubik
from collections import deque
import random

def prettify_cube_list(cube_list):
    if not cube_list:
        raise Exception("Empty cube_list provided")
    return [Rubik.perm_to_string_dict[m] for m in cube_list]

def cube_bfs(goal, condition_function):
    visited = deque()
    visited.append((goal, []))
    while visited:
        next_cube = visited.popleft()
        for m in Rubik.moves:
            moves = next_cube[1] + [m]
            new_cube = Rubik.perm_apply(m, next_cube[0])
            if condition_function(new_cube):
                return moves
            visited.append((new_cube, moves))
    return None

def stage_one(cube):
    return cube_bfs(cube, Rubik.check_edge_orientation)


if __name__ == "__main__":
    #scramble = [Rubik.F, Rubik.R, Rubik.Bi]
    scramble = []
    for i in range(20):
        scramble.append(random.choice(Rubik.moves))
    print(prettify_cube_list(scramble))

    #scramble = [Rubik.F, Rubik.R, Rubik.Bi]
    scrambled = Rubik.multiple_perm_apply(scramble, Rubik.I)
    solution = cube_bfs(scrambled, Rubik.check_edge_orientation)
    print(solution)
    print("fix_eo: ", prettify_cube_list(solution))

