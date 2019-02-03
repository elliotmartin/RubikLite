import numpy as np

# flu refers to the front face (because f is first) of the cubie that
# has a front face, a left face, and an upper face.
# yob refers to the colors yellow, orange, blue that are on the
# respective faces if the cube is in the solved position.

# Corners
rgw = flu = 0  # (0-th cubie; front face)
gwr = luf = 1  # (0-th cubie; left face)
wrg = ufl = 2  # (0-th cubie; up face)

rwb = fur = 3  # (1-st cubie; front face)
wbr = urf = 4  # (1-st cubie; up face)
brw = rfu = 5  # (1-st cubie; right face)

ryg = fdl = 6  # (2-nd cubie; front face)
ygr = dlf = 7  # (2-nd cubie; down face)
gry = lfd = 8  # (2-nd cubie; left face)

rby = frd = 9  # (3-rd cubie; front face)
byr = rdf = 10  # (3-rd cubie; right face)
yrb = dfr = 11  # (3-rd cubie; down face)

owg = bul = 12  # (4-th cubie; back face)
wgo = ulb = 13  # (4-th cubie; up face)
gow = lbu = 14  # (4-th cubie; left face)

obw = bru = 15  # (5-th cubie; back face)
bwo = rub = 16  # (5-th cubie; right face)
wob = ubr = 17  # (5-th cubie; up face)

ogy = bld = 18  # (6-th cubie; back face)
gyo = ldb = 19  # (6-th cubie; left face)
yog = dbl = 20  # (6-th cubie; down face)

oyb = bdr = 21  # (7-th cubie; back face)
ybo = drb = 22  # (7-th cubie; down face)
boy = rbd = 23  # (7-th cubie; right face)

# Edges
fu = rw = 24  # (8-th cubie; front face)
uf = wr = 25  # (8-th cubie; up face)

fr = rb = 26  # (9th cubie; front face)
rf = br = 27  # (9th cubie; right face)

fl = rg = 28  # (10th cubie; front face)
lf = gr = 29  # (10th cubie; left face)

fd = ry = 30  # (11th cubie; front face)
df = yr = 31  # (11th cubie; down face)

br = ob = 32  # (12th cubie; back face)
rb = bo = 33  # (12th cubie; right face)

bl = og = 34  # (13th cubie; back face)
lb = og = 35  # (13th cubie; left face)

bd = oy = 36  # (14th cubie; back face)
db = yo = 37  # (14th cubie; down face)

bu = ow = 38  # (15th cubie; back face)
ub = wo = 39  # (15th cubie; up face)

ur = wb = 40  # (16th cubie; up face)
ru = bw = 41  # (16th cubie; right face)

ul = wg = 42  # (17th cubie; up face)
lu = gw = 43  # (17th cubie; back face)

dr = yb = 44  # (18th cubie; down face)
rd = by = 45  # (18th cubie; right face)

dl = yg = 46  # (19th cubie; down face)
ld = gy = 47  # (19th cubie; left face)

# preperations for playing with an API
"""
edges_to_nums = {'rgw': 0, 'gwr': 1, 'wrg': 2, 'rwb': 3, 'wbr': 4, 'brw': 5, 'ryg': 6, 'ygr': 7, 'gry': 8, 'rby': 9,
                 'byr': 10, 'yrb': 11, 'owg': 12, 'wgo': 13, 'gow': 14, 'obw': 15, 'bwo': 16, 'wob': 17, 'ogy': 18,
                 'gyo': 19, 'yog': 20, 'oyb': 21, 'ybo': 22, 'boy': 23, 'fu': 24, 'uf': 25, 'fr': 26, 'rf': 27, 'fl': 28,
                 'lf': 29, 'fd': 30, 'df': 31, 'br': 32, 'rb': 33, 'bl': 34, 'lb': 35, 'bd': 36, 'db': 37, 'bu': 38,
                 'ub': 39, 'ur': 40, 'ru': 41, 'ul': 42, 'lu': 43, 'dr': 44, 'rd': 45, 'dl': 46, 'ld': 47}

nums_to_edges = {0: 'rgw', 1: 'gwr', 2: 'wrg', 3: 'rwb', 4: 'wbr', 5: 'brw', 6: 'ryg', 7: 'ygr', 8: 'gry', 9: 'rby',
                 10: 'byr', 11: 'yrb', 12: 'owg', 13: 'wgo', 14: 'gow', 15: 'obw', 16: 'bwo', 17: 'wob', 18: 'ogy', 19:
                     'gyo', 20: 'yog', 21: 'oyb', 22: 'ybo', 23: 'boy', 24: 'fu', 25: 'uf', 26: 'fr', 27: 'rf',
                 28: 'fl', 29: 'lf', 30: 'fd', 31: 'df', 32: 'br', 33: 'rb', 34: 'bl', 35: 'lb', 36: 'bd', 37: 'db',
                 38: 'bu', 39: 'ub', 40: 'ur', 41: 'ru', 42: 'ul', 43: 'lu', 44: 'dr', 45: 'rd', 46: 'dl', 47: 'ld'}


def extract_front(cube):

    None
"""

def perm_apply(perm, cube):
    """
    Applies a permutation to a cube

    :param perm: a permutation (0, 1, 2, ... , 47)
    :param cube: a permutation (0, 1, 2, ... , 47)
    :return a new permutation with cube permutated according to cube
    """
    return (tuple(cube[i] for i in perm))



def perm_inverse(perm):
    '''Computes the inverse of a permutation'''
    inv_perm = [0]*len(perm)
    for i in range(len(perm)):
        inv_perm[perm[i]] = i
    return tuple(inv_perm)


def multiple_perm_apply(perms, cube):
    """
    Applies a list of permutations to a cube

    :param perms: list of a permutations,
    :param cube: a cube
    :return a cube
    """
    cube = cube
    for p in perms:
        cube = perm_apply(p, cube)
    return cube

"""
Definitions for all the moves as permutations. 
The identity is a do nothing move, everything else permutes correlating to the move. 
Moves are in standard Rubik's cube notation with no double turns. 
"""
I = (flu, luf, ufl, fur, urf, rfu, fdl, dlf, lfd, frd, rdf, dfr ,bul ,ulb, lbu, bru ,rub, ubr, bld ,ldb ,dbl, bdr, drb,
     rbd, fu, uf, fr, rf, fl, lf, fd, df, br, rb, bl, lb, bd, db, bu, ub, ur, ru, ul, lu, dr, rd, dl, ld)

F = (fdl, dlf, lfd, flu, luf, ufl, frd, rdf, dfr, fur, urf, rfu, bul, ulb, lbu, bru, rub, ubr, bld, ldb, dbl, bdr, drb,
     rbd, fl, lf, fu, uf, fd, df, fr, rf, br, rb, bl, lb, bd, db, bu, ub, ur, ru, ul, lu, dr, rd, dl, ld)
Fi = perm_inverse(F)

B = (flu, luf, ufl, fur, urf, rfu, fdl, dlf, lfd, frd, rdf, dfr, bru, rub, ubr, bdr, drb, rbd, bul, ulb, lbu, bld, ldb,
     dbl, fu, uf, fr, rf, fl, lf, fd, df, bd, db, bu, ub, bl, lb, br, rb, ur, ru, ul, lu, dr, rd, dl, ld)
Bi = perm_inverse(B)

U = (rfu, fur, urf, rub, ubr, bru, fdl, dlf, lfd, frd, rdf, dfr, luf, ufl, flu, lbu, bul, ulb, bld, ldb, dbl, bdr, drb,
     rbd, ru, ur, fr, rf, fl, lf, fd, df, br, rb, bl, lb, bd, db, lu, ul, ub, bu, uf, fu, dr, rd, dl, ld)
Ui = perm_inverse(U)

D = (flu, luf, ufl, fur, urf, rfu, ldb, dbl, bld, lfd, fdl, dlf, bul, ulb, lbu, bru, rub, ubr, rbd, bdr, drb, rdf, dfr,
     frd, fu, uf, fr, rf, fl, lf, ld, dl, br, rb, bl, lb, rd, dr, bu, ub, ur, ru, ul, lu, df, fd, db, bd)
Di = perm_inverse(D)

R =  (flu, luf, ufl, dfr, frd, rdf, fdl, dlf, lfd, drb, rbd, bdr, bul, ulb, lbu, urf, rfu, fur, bld, ldb, dbl, ubr, bru,
      rub, fu, uf, dr, rd, fl, lf, fd, df, ur, ru, bl, lb, bd, db, bu, ub, fr, rf, ul, lu, br, rb, dl, ld)
Ri = perm_inverse(R)

L = (ulb, lbu, bul, fur, urf, rfu, ufl, flu, luf, frd, rdf, dfr, dbl, bld, ldb, bru, rub, ubr, dlf, lfd, fdl, bdr, drb,
     rbd, fu, uf, fr, rf, ul, lu, fd, df, br, rb, dl, ld, bd, db, bu, ub, ur, ru, bl, lb, dr, rd, fl, lf)
Li = perm_inverse(L)

moves = (F, Fi, U, Ui, R, Ri, B, Bi, D, Di, L, Li)
# Dictionary of move names so that we can parse strings of moves
move_names = {F: 'F', Fi: 'Fi', U: 'U', Ui: 'Ui', R: 'R', Ri: 'Ri', B: 'B', Bi: 'Bi', D: 'D', Di: 'Di', L: 'L', Li: 'Li'
              }


def perms_only(cube):
    """
    grabs every corners position by extracting each corner and edge and ignoring orientation changes
    :param cube: 48 length cube
    :return 20 length cube
    """
    return corner_perms_only(cube[:24]) + edge_perms_only(cube[24:])


def corner_perms_only(corners):
    """
    returns the permutations of each corner
    :param corners: just the corners of a cube
    :return the permutation of every corner
    """
    corner_perms = [i for i in corners if i % 3 == 0]
    return tuple(corner_perms)


def edge_perms_only(edges):
    '''
    returns the permutations of each edge
    :param edges: just the edges of a cube
    :return the permutation of every edge
    '''
    edge_perms = [i for i in edges if i % 2 == 0]
    return tuple(edge_perms)


def compact_cube(cube):
    """
    Given a 48 length tuple cube compacts down to 20
    :param cube: 48 length cube
    :return: 20 length cube
    """
    corners = cube[:24]
    edges = cube[24:]
    compact_corners = corners[::3]
    compact_edges = edges[::2]
    return tuple(compact_corners) + tuple(compact_edges)


def expand_cube(compact_cube):
    """
    Expands a given 20 length tuple cube into a 48 length tuple cube
    This is non-trivial and requires expanding each cubie ex 0 become 0, 1, 2 or 1 because 1, 2, 0
    Pretty sure the numbers always have to stay in order so that's the key - can't have have 0 2 1 only 0 1 2, 1 2 0, 2 0 1
    Edges just expand to include 1 up or down from where they are based on whether they're even or not
    """
    flatten = lambda l: [item for sublist in l for item in sublist]
    corners = []
    compact_corners = compact_cube[:8]
    edges =[]
    compact_edges = compact_cube[8:]

    for c in compact_corners:
        if c % 3 == 0:
            corners.append([c, c + 1, c+2])
        if c % 3 == 1:
            corners.append([c, c+1, c-1])
        if c % 3 == 2:
            corners.append([c, c-2, c-1])
    corners = tuple(flatten(corners))

    for e in compact_edges:
        if e % 2 == 0:
            edges.append([e, e+1])
        if e % 2 == 1:
            edges.append([e, e-1])
    edges = tuple(flatten(edges))

    return corners+edges



def is_valid(cube):
    """
    Checks if a given permutation is a valid cube
    :param: 48 length cube
    :return: True if it's a valid Rubik's cube, otherwise False
    """
    return check_edge_orientation(cube) & check_corner_orientation(cube) & check_permutation_parity(cube)


def check_corner_orientation(cube):
    """
    Sum of corner orientations is always divisible by 3. Thus, the sum of all first corners mod 3 must be divisible by 3
    Take each first corner number and mod it by 3. If the result is 2 subtract 1 otherwise add the number you get.
    This number must be divisble by 3
    :param cube:
    :return boolean:  True if corner orientation is valid, otherwise False
    """
    # we only care about the firsts, so we convert to a compact cube
    firsts = compact_cube(cube)

    # now we get just the corners and mod by 3
    compact_corners = [i % 3 for i in firsts[0:8]]
    compact_corners_sum = sum(compact_corners)

    if (compact_corners_sum % 3) != 0:
        return False

    return True


def check_edge_orientation(cube):
    """
    Edge parity:
    Even number of edges flipped
    The sum of first edge tuples must be even
    :param cube:
    :return boolean: True if edge orientation is valid, otherwise False
    """
    # we only care about the firsts, so we convert to a compact cube
    firsts = compact_cube(cube)
    compact_edges = firsts[8:]
    # this time we just need to tell if there's an even number of flipped edges.
    # An edge is flipped if it's odd parity so we just sum them all and check if even
    compact_edges_sum = sum(compact_edges)
    # if there's an odd number of flipped edges, then the cube is invalid
    if (compact_edges_sum % 2) != 0:
        return False

    return True


def cyclic_decomp(perm):
    """
    https://en.wikipedia.org/wiki/Permutation#Cycle_notation
    https://gist.github.com/begriffs/2211881
    :param perm:
    :return list: The cyclic decomposition of the permutation, omitting one cycles
    """
    remain = set(perm)
    result = []
    while len(remain) > 0:
        n = remain.pop()
        cycle = [n]
        while True:
            n = perm[n]
            if n not in remain:
                break
            remain.remove(n)
            cycle.append(n)
        result.append(cycle)

    return [i for i in result if len(i) > 1]


def check_permutation_parity(cube):
    """
    Can only perform an even number of swaps
    Compare each piece to where it is on a solved cube, regardless of orientation.
    Must be an even number of pieces changed
    :param cube:
    :return boolean: True if permutation parity is valid, otherwise False
    """
    corners = cube[:24]
    edges = cube[24:]
    edges = [e - 24 for e in edges]

    corner_perms = corner_perms_only(corners)
    edge_perms = edge_perms_only(edges)

    normalized_corners = [int(c/3) for c in corner_perms]
    normalized_edges = [int(e/2) for e in edge_perms]

    corners_perm_parity = len(cyclic_decomp(normalized_corners)) % 2
    edges_perm_parity = len(cyclic_decomp(normalized_edges)) % 2

    if corners_perm_parity != edges_perm_parity:
        return False

    return True


def generate_cube():
    """
    Randomly generates permutations until a valid cube is found
    :return: A random valid cube
    """
    corners = np.random.permutation(np.arange(0, 24))
    edges = np.random.permutation(np.arange(24, 48))
    cube = tuple(corners) + tuple(edges)

    while not is_valid(cube):
        corners = np.random.permutation(np.arange(0, 24))
        edges = np.random.permutation(np.arange(24, 48))
        cube = tuple(corners) + tuple(edges)

    return cube
