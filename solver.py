import Rubik
from collections import deque
import random

#g0 is all moves
#g1 - L,R,F,B,U2,D2
#g2 - L,R,F2,B2,U2,D2
#g3 - L2,R2,F2,B2,U2,D2
G0_MOVES = Rubik.h2m_moves
G1_MOVES = [Rubik.L, Rubik.Li, Rubik.R, Rubik.Ri, Rubik.F, Rubik.Fi, Rubik.B, Rubik.Bi, Rubik.U2, Rubik.D2]
G2_MOVES = [Rubik.L, Rubik.R, Rubik.perm_apply(Rubik.F, Rubik.F), Rubik.perm_apply(Rubik.B, Rubik.B),
            Rubik.perm_apply(Rubik.U, Rubik.U), Rubik.perm_apply(Rubik.D, Rubik.D)]
G3_MOVES = [Rubik.perm_apply(Rubik.L, Rubik.L), Rubik.perm_apply(Rubik.R, Rubik.R), Rubik.perm_apply(Rubik.F, Rubik.F),
            Rubik.perm_apply(Rubik.B, Rubik.B), Rubik.perm_apply(Rubik.U, Rubik.U), Rubik.perm_apply(Rubik.D, Rubik.D)]


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

# https://tomas.rokicki.com/g4g9.pdf
# no turns of the same face can be adjacent
# any pair of adjacent commuting single moves (such as U and D) are always given in a particular order
# we use U before D, F before B, and R before L
# if we verify the sequence is canonical every time a new move is added to it, we're only concerned about the last 2 moves
def is_canonical(moves):
    prev = moves[-2]
    prev_string = Rubik.perm_to_string_dict_htm[prev]
    last = moves[-1]
    last_string = Rubik.perm_to_string_dict_htm[last]

    if prev_string[0] == last_string[0]:
        return False

    if prev_string[0] == 'D' and last_string == 'U':
        return False

    if prev_string == 'B' and last_string == 'F':
        return False

    if prev_string == 'R' and last_string == 'L':
        return False

    return True


def cube_bfs(start, condition_function, valid_moves):
    print("start bfs")
    max_depth = 0
    visited = deque()
    visited.append((start, []))
    while visited:
        next_cube = visited.popleft()
        if max_depth > 1:
            None
            #print("list", prettify_cube_list(next_cube[1]))
        for m in valid_moves:
            moves = next_cube[1] + [m]
            if len(moves) > 1:
                if not is_canonical(moves):
                    continue
            if len(moves) > max_depth:
                max_depth += 1
            new_cube = Rubik.perm_apply(m, next_cube[0])
            if condition_function(new_cube):
                return moves
            visited.append((new_cube, moves))
        if max_depth >= 14:
            break
    #print([prettify_cube_list(v[1]) for v in visited])
    return None


def stage_one(cube):
    return cube_bfs(cube, Rubik.check_edge_orientation)


if __name__ == "__main__":
    # TODO: Turn these into tests
    scramble = [Rubik.F, Rubik.R, Rubik.Bi, Rubik.perm_apply(Rubik.U, Rubik.U), Rubik.L, Rubik.F]
    #print(prettify_cube_list(scramble))
    #scramble = [Rubik.F, Rubik.R, Rubik.Bi]
    scrambled = Rubik.multiple_perm_apply(scramble, Rubik.I)
    solve = [Rubik.Fi, Rubik.Li, Rubik.U2, Rubik.B, Rubik.Ri, Rubik.Fi]
    print("solved", Rubik.multiple_perm_apply(solve, scrambled))

    #print(check_complete_g2(scrambled))
    scrambled = Rubik.generate_cube()
    print("scrambled", scrambled)
    g1_sol = cube_bfs(scrambled, check_complete_g1, G0_MOVES)
    print("g1_sol", prettify_cube_list(g1_sol))
    #solution = cube_bfs(scrambled, check_complete_g2, G1_MOVES)
    solution = cube_bfs(Rubik.multiple_perm_apply(g1_sol, scrambled), check_complete_g2, G1_MOVES)
    print(solution)
    print("g2_sol", prettify_cube_list(solution))

