import Rubik
from collections import deque
import random

#g0 is all moves
#g1 - L,R,F,B,U2,D2
#g2 - L,R,F2,B2,U2,D2
#g3 - L2,R2,F2,B2,U2,D2
G0_MOVES = Rubik.moves
G1_MOVES = [Rubik.L, Rubik.R, Rubik.F, Rubik.B, Rubik.perm_apply(Rubik.U, Rubik.U), Rubik.perm_apply(Rubik.D, Rubik.D)]
G2_MOVES = [Rubik.L, Rubik.R, Rubik.perm_apply(Rubik.F, Rubik.F), Rubik.perm_apply(Rubik.B, Rubik.B),
            Rubik.perm_apply(Rubik.U, Rubik.U), Rubik.perm_apply(Rubik.D, Rubik.D)]
G3_MOVES = [Rubik.perm_apply(Rubik.L, Rubik.L), Rubik.perm_apply(Rubik.R, Rubik.R), Rubik.perm_apply(Rubik.F, Rubik.F),
            Rubik.perm_apply(Rubik.B, Rubik.B), Rubik.perm_apply(Rubik.U, Rubik.U), Rubik.perm_apply(Rubik.D, Rubik.D)]

U2 = Rubik.perm_apply(Rubik.U, Rubik.U)
print(Rubik.perm_apply(U2, U2))


def check_complete_g1(cube):
    return Rubik.check_edge_orientation(cube)


def check_complete_g2(cube):
    # is this a bad design? Assume true turn false seems worse than assume false turn true?
    check_edge_placement = True
    check_corner_orientation = True

    m_edges = [24,25, 30,31, 36,37, 38,39]
    for cubie in [cube[24], cube[30], cube[36], cube[38]]:
        if cubie not in m_edges:
            check_edge_placement = False

    compact_corners = [i % 3 for i in Rubik.compact_cube(cube)[0:8]]
    if sum(compact_corners) > 0:
        check_corner_orientation = False

    return check_edge_placement & check_corner_orientation



def prettify_cube_list(cube_list):
    if not cube_list:
        raise Exception("Empty cube_list provided")
    return [Rubik.perm_to_string_dict_htm[m] for m in cube_list]


def cube_bfs(start, condition_function, valid_moves):
    max_depth = 0
    visited = deque()
    visited.append((start, []))
    while visited:
        next_cube = visited.popleft()
        for m in valid_moves:
            moves = next_cube[1] + [m]
            if len(moves) > max_depth:
                max_depth += 1
            new_cube = Rubik.perm_apply(m, next_cube[0])
            if condition_function(new_cube):
                return moves
            visited.append((new_cube, moves))
        if max_depth > 15:
            break
    return None


def stage_one(cube):
    return cube_bfs(cube, Rubik.check_edge_orientation)


if __name__ == "__main__":
    # TODO: Turn these into tests
    scramble = [Rubik.F, Rubik.R, Rubik.Bi, Rubik.U, Rubik.L, Rubik.F]
    #scramble = []
    #for i in range(20):
    #    scramble.append(random.choice(Rubik.moves))
    #print(prettify_cube_list(scramble))

    #scramble = [Rubik.F, Rubik.R, Rubik.Bi]
    scrambled = Rubik.multiple_perm_apply(scramble, Rubik.I)
    #solution = cube_bfs(scrambled, Rubik.check_edge_orientation, G0_MOVES)
    #print(solution)
    #print("fix_eo: ", prettify_cube_list(solution))


    print(check_complete_g2(scrambled))
    g1_sol = cube_bfs(scrambled, Rubik.check_edge_orientation, G0_MOVES)
    print(prettify_cube_list(g1_sol))
    #scrambled = Rubik.generate_cube()
    solution = cube_bfs(Rubik.multiple_perm_apply(g1_sol, scrambled), check_complete_g2, G1_MOVES)
    print(solution)
    print(prettify_cube_list(solution))

