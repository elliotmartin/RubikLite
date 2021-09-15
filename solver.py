import Rubik
from collections import deque
import random

#g0 is all moves
#g1 - L,R,F,B,U2,D2
#g2 - L,R,F2,B2,U2,D2
#g3 - L2,R2,F2,B2,U2,D2
G0_MOVES = [Rubik.moves]
G1_MOVES = [Rubik.L, Rubik.R, Rubik.F, Rubik.B, Rubik.perm_apply(Rubik.U, Rubik.U), Rubik.perm_apply(Rubik.D, Rubik.D)]
G2_MOVES = [Rubik.L, Rubik.R, Rubik.perm_apply(Rubik.F, Rubik.F), Rubik.perm_apply(Rubik.B, Rubik.B),
            Rubik.perm_apply(Rubik.U, Rubik.U), Rubik.perm_apply(Rubik.D, Rubik.D)]
G3_MOVES = [Rubik.perm_apply(Rubik.L, Rubik.L), Rubik.perm_apply(Rubik.R, Rubik.R), Rubik.perm_apply(Rubik.F, Rubik.F),
            Rubik.perm_apply(Rubik.B, Rubik.B), Rubik.perm_apply(Rubik.U, Rubik.U), Rubik.perm_apply(Rubik.D, Rubik.D)]


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

