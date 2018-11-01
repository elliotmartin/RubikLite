import numpy as np
"""
We'll call the six sides, as usual:
   Front Back   Up Down   Left Right
or F, B, U, D, L, R.

Permutations:

We'll number the cubie positions starting
at 0, front to back, up to down, left to right.
We give an alphabetic name to the cubies as well,
by listing the faces it contains, starting with
F or B, in clockwise order (looking in from outside).
   0th cubie = FLU
   1st cubie = FUR
   2nd cubie = FDL
   3rd cubie = FRD
   4th cubie = BUL
   5th cubie = BRU
   6th cubie = BLD
   7th cubie = BDR
Each cubie has three faces, so we have 24 face
positions.  We'll label them as 0 to 23, but also
with a 3-letter name that specifies the name
of the cubie it is on, cyclically rotated to
put the name of the face first (so cubie FLU
has faces flu, luf, and ufl, on sides F, L,
and U, respectively). We'll use lower case
here for clarity.  Here are the face names,
written as variables for later convenience.
We also save each number in a second variable,
where the positions are replaced by the colors that
would be there if the cube were solved and had its
orange-yellow-blue cubie in position 7, with yellow
facing down.
"""

"""
red - Front
blue - right
white - up
orange - Back
green - Left
yellow - Down
Face - Color

F - R
R - B
U - W
B - O
L - G
D - Y

FU
FR
FL
FD
BR
BL
BD
BU
"""

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

ur = wb = 40  # (16th cubie; back face)
ru = bw = 41  # (16th cubie; back face)

ul = wg = 42  # (17th cubie; back face)
lu = gw = 43  # (17th cubie; back face)

dr = yb = 44  # (18th cubie; back face)
rd = by = 45  # (18th cubie; back face)

dl = yg = 46  # (19th cubie; back face)
ld = gy = 47  # (19th cubie; Back face)

# do we keep the edges seperate or meld the entire thing? Really easy to implement
# if we dont
# cant see any way in which having edges seperate could be better. Can always take
# slice of the cube tuple to get just edges or just corners
# have to copy all perms, including the edges this time

# look at implementations for diff algs


'''
Applies a permutation to a cube
Input is a permutation, all of which are defined below and a cube which is also just a permutation
'''
def perm_apply(perm, cube):
    return (tuple(cube[i] for i in perm))


'''
Computes the inverse of a permutation
'''
def perm_inverse(perm):
    inv_perm = [0]*len(perm)
    for i in range(len(perm)):
        inv_perm[perm[i]] = i
    return tuple(inv_perm)


'''
Applies a list of permutations to a cube
Perms - list of a permutations, cube is a cube
returns a cube
'''
def multiple_perm_apply(perms, cube):
    cube = cube
    for p in perms:
        cube = perm_apply(p, cube)
    return cube

#I = (flu, luf, ufl, fur, urf, rfu, fdl, dlf, lfd, frd, rdf, dfr ,bul ,ulb, lbu, bru ,rub, ubr, bld ,ldb ,dbl, bdr, drb, rbd, fu, uf, fr, rf, fl, lf, fd, df, br, rb, bl, lb, bd, db, bu, ub, ur, ru, ul, lu, dr, rd, dl, ld)
#cu= (0,    1,   2,   3,   4,   5,   6,   7,   8,   9,   10, 11,  12,  13,  14,  15,  16,  17,  18,  19,  20,  21,  22,  23,  24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47)


'''
Definitions for all the moves as permutations. 
The identity is a do nothing move, everything else permutes correlating to the move. 
Moves are in standard Rubik's cube notation with no double turns. 
'''
I = (flu, luf, ufl, fur, urf, rfu, fdl, dlf, lfd, frd, rdf, dfr ,bul ,ulb, lbu, bru ,rub, ubr, bld ,ldb ,dbl, bdr, drb, rbd, fu, uf, fr, rf, fl, lf, fd, df, br, rb, bl, lb, bd, db, bu, ub, ur, ru, ul, lu, dr, rd, dl, ld)
I = (0,    1,   2,   3,   4,   5,   6,   7,   8,   9,   10, 11,  12,  13,  14,  15,  16,  17,  18,  19,  20,  21,  22,  23,  24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47)


F = (fdl, dlf, lfd, flu, luf, ufl, frd, rdf, dfr, fur, urf, rfu, bul, ulb, lbu, bru, rub, ubr, bld, ldb, dbl, bdr, drb, rbd, fr, rf, fd, df, fu, uf, fl, lf, br, rb, bl, lb, bd, db, bu, ub, ur, ru, ul, lu, dr, rd, dl, ld)
F = (6, 7, 8, 0, 1, 2, 9, 10, 11, 3, 4, 5, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 26, 27, 30, 31, 24, 25, 28, 29, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47)

Fi = perm_inverse(F)
Fi = (3, 4, 5, 9, 10, 11, 0, 1, 2, 6, 7, 8, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 28, 29, 24, 25, 30, 31, 26, 27, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47)

B = (flu, luf, ufl, fur, urf, rfu, fdl, dlf, lfd, frd, rdf, dfr, bld, ldb, dbl, bul, ulb, lbu, bdr, drb, rbd, bru, rub, ubr, fu, uf, fr, rf, fd, df, fl, lf, br, rb, bd, db, bl, lb, bu, ub, ur, ru, ul, lu, dr, rd, dl, ld)
B = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 18, 19, 20, 12, 13, 14, 21, 22, 23, 15, 16, 17, 24, 25, 26, 27, 30, 31, 28, 29, 32, 33, 36, 37, 34, 35, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47)

Bi = perm_inverse(B)
Bi = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 15, 16, 17, 21, 22, 23, 12, 13, 14, 18, 19, 20, 24, 25, 26, 27, 30, 31, 28, 29, 32, 33, 36, 37, 34, 35, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47)

U = (rfu, fur, urf, rub, ubr, bru, fdl, dlf, lfd, frd, rdf, dfr, luf, ufl, flu, lbu, bul, ulb, bld, ldb, dbl, bdr, drb, rbd, lu, ul, fr, rf, fl, lf, fd, df, br, rb, bl, lb, bd, db, ru, ur, uf, fu, ub, bu, dr, rd, dl, ld)
U = (5, 3, 4, 16, 17, 15, 6, 7, 8, 9, 10, 11, 1, 2, 0, 14, 12, 13, 18, 19, 20, 21, 22, 23, 43, 42, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 41, 40, 25, 24, 39, 38, 44, 45, 46, 47)

Ui = perm_inverse(U)
Ui = (14, 12, 13, 1, 2, 0, 6, 7, 8, 9, 10, 11, 16, 17, 15, 5, 3, 4, 18, 19, 20, 21, 22, 23, 41, 40, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 43, 42, 39, 38, 25, 24, 44, 45, 46, 47)

D = (flu, luf, ufl, fur, urf, rfu, frd, rdf, dfr, bdr, drb, rbd, bul, ulb, lbu, bru, rub, ubr, fdl, dlf, lfd, bld, ldb, dbl, fu, uf, fr, rf, fl, lf, rd, dr, br, rb, bl, lb, ld, dl, bu, ub, ur, ru, ul, lu, db, bd, df, fd)
D = (0, 1, 2, 3, 4, 5, 9, 10, 11, 21, 22, 23, 12, 13, 14, 15, 16, 17, 6, 7, 8, 18, 19, 20, 24, 25, 26, 27, 28, 29, 45, 44, 32, 33, 34, 35, 47, 46, 38, 39, 40, 41, 42, 43, 37, 36, 31, 30)

Di = perm_inverse(D)
Di = (0, 1, 2, 3, 4, 5, 18, 19, 20, 6, 7, 8, 12, 13, 14, 15, 16, 17, 21, 22, 23, 9, 10, 11, 24, 25, 26, 27, 28, 29, 47, 46, 32, 33, 34, 35, 45, 44, 38, 39, 40, 41, 42, 43, 31, 30, 37, 36)

R = (flu, luf, ufl, dfr, frd, rdf, fdl, dlf, lfd, drb, rbd, bdr, bul, ulb, lbu, urf, rfu, fur, bld, ldb, dbl, ubr, bru, rub, fu, uf, ur, ru, fl, lf, fd, df, dr, rd, bl, lb, bd, db, bu, ub, br, rb, ul, lu, fr, rf, dl, ld)
R = (0, 1, 2, 11, 9, 10, 6, 7, 8, 22, 23, 21, 12, 13, 14, 4, 5, 3, 18, 19, 20, 17, 15, 16, 24, 25, 40, 41, 28, 29, 30, 31, 44, 45, 34, 35, 36, 37, 38, 39, 32, 33, 42, 43, 26, 27, 46, 47)


Ri = perm_inverse(R)
Ri = (0, 1, 2, 17, 15, 16, 6, 7, 8, 4, 5, 3, 12, 13, 14, 22, 23, 21, 18, 19, 20, 11, 9, 10, 24, 25, 44, 45, 28, 29, 30, 31, 40, 41, 34, 35, 36, 37, 38, 39, 26, 27, 42, 43, 32, 33, 46, 47)
     #                              #              #              #                             #                                             #                       #                               #               #
#I = (flu, luf, ufl, fur, urf, rfu, fdl, dlf, lfd, frd, rdf, dfr ,bul ,ulb, lbu, bru ,rub, ubr, bld ,ldb ,dbl, bdr, drb, rbd, fu, uf, fr, rf, fl, lf, fd, df, br, rb, bl, lb, bd, db, bu, ub, ur, ru, ul, lu, dr, rd, dl, ld)
L = (ulb, lbu, bul, fur, urf, rfu, ufl, flu, luf, frd, rdf, dfr, dbl, bld, ldb, bru, rub, ubr, dlf, lfd, fdl, bdr, drb, rbd, fu, uf, fr, rf, dl, ld, fd, df, br, rb, ul, lu, bd, db, bu, ub, ur, ru, fl, lf, dr, rd, bl, lb)
L = (13, 14, 12, 3, 4, 5, 2, 0, 1, 9, 10, 11, 20, 18, 19, 15, 16, 17, 7, 8, 6, 21, 22, 23, 24, 25, 26, 27, 46, 47, 30, 31, 32, 33, 42, 43, 36, 37, 38, 39, 40, 41, 28, 29, 44, 45, 34, 35)

Li = perm_inverse(L)
Li = (7, 8, 6, 3, 4, 5, 20, 18, 19, 9, 10, 11, 2, 0, 1, 15, 16, 17, 13, 14, 12, 21, 22, 23, 24, 25, 26, 27, 42, 43, 30, 31, 32, 33, 46, 47, 36, 37, 38, 39, 40, 41, 34, 35, 44, 45, 28, 29)

'''
Stores all the moves in a tuple (why not as a list?) 
'''
moves = (F, Fi, U, Ui, R, Ri, B, Bi, D, Di, L, Li)

'''
Dictionary of move names so that we can parse strings of moves
'''
move_names = {}
move_names[F] = 'F'
move_names[Fi] = 'Fi'
move_names[U] = 'U'
move_names[Ui] = 'Ui'
move_names[R] = 'R'
move_names[Ri] = 'Ri'
move_names[B] = 'B'
move_names[Bi] = 'Bi'
move_names[D] = 'D'
move_names[Di] = 'Di'
move_names[L] = 'L'
move_names[Li] = 'Li'

'''
Checks if a given permutation is a valid cube
Algorithm TBD
Corner parity:
Sum of corner orientations is always divisible by 3 which means that the sum of all first corners mod 3 must be divisible by 3
Take each first corner number and mod it by 3 if it's 2 subtract 1 otherwise add the number you get. This number must be divisble by 3
Edge parity:
Even number of edges flipped 
The sum of first edge tuples must be even
Permutation parity:
Can only perform an even number of swaps
Compare each piece to where it is on a solved cube, regardless of orientation. Must be an even number of pieces changed
:param: 48 length cube
:return: True if it's a valid Rubik's cube, otherwise False
'''
#TODO: Test this method.
def is_valid(cube):
    #sum first of all corners - up to the 24th position in the tuple
    #we only care about the firsts, so we convert to a compact cube
    firsts = compact_cube(cube)

    #now we get just the corners and mod by 3
    corners = [i % 3 for i in firsts[0:7]]
    #then we sum based on our alg - subtract 1 if it's 2, otherwise add the value
    corners_sum = 0
    for _ in corners:
        if _ == 2:
            corners_sum += -1
        else:
            corners_sum += _
    #if it's not divisible by 3, then the cube is invalid
    if(corners_sum % 3) != 0:
        return False

    #now we look at the edges
    edges = firsts[8:]
    #this time we just need to tell if there's an even number of flipped edges.
    # An edge is flipped if it's odd parity so we just sum them all and check if even
    edges_sum = sum(edges)
    #if there's an odd number of flipped edges, then the cube is invalid
    if (edges_sum % 2) != 0:
        return False

    #TODO: figure this out
    #requires a couple of helper methods. First a cyclic decomposition method, then a method to check the parity of the cycle. Computer cyclic decomp. of corners, edges and compare. If equal return true
    #now we compare to the base cube
    base = compact_cube(I)
    #and find the number of pieces that have been permuted
    permuted = 0
    for _ in len(firsts):
        if firsts[_] != base[_]:
            permuted += 1


'''
Computes the cyclic decomposition of a permutation group
:param: 48 length cube
:return: a list of list containing the cyclic decomposition of the cube
'''
def cyclic_decomp(cube):
    perms = perms_only(cube)
    base = perms_only(I)

    cycles = []
    a = min(perms)
    while a != max(perms):
        cycle = [a]

    #grab the lowest value

    None


'''
grabs every corners position by extracting each corner and edge and ignoring permutation changes
:param: 48 length cube
:return: 20 length cube
'''
def perms_only(cube):
    corners = cube[0:24]
    edges = cube[24:]
    corner_perms = [i for i in corners if i % 3 == 0]
    edge_perms = [i for i in edges if i % 2 == 0]
    return tuple(corner_perms+edge_perms)


'''
Given a 48 length tuple cube compacts down to 20
This is trivial
:param: 48 length cube
:return: 20 length cube
'''
#take a 48 cube and compact it to 20
def compact_cube(cube):
    None


'''
Expands a given 20 length tuple cube into a 48 length tuple cube
This is non-trivial and requires expanding each cubie ex 0 become 0, 1, 2 or 1 because 1, 2, 0
Pretty sure the numbers always have to stay in order so that's the key - can't have have 0 2 1 only 0 1 2, 1 2 0, 2 0 1
Edges just expand to include 1 up or down from where they are based on whether they're even or not
'''
#takes a 20 lenth cube and expands it to 48
def expand_cube(cube):
    None

#TODO: Generate random cube states for solution
'''
Generates a random, valid cube
First we need to generate a random sequence of 0-23 for the corners and 24-47 for the edges
Then we need to randomly increase all the corners by 0, 1, or 2 and all the edges by 0 or 1
'''
def generate_cube():

    #generate random permutations of corners and edges
    #have to regenerate if corners are invalid. do same for edges
    corners = np.random.choice(24, 24, replace = False)
    edges = np.random.choice(np.arange(24, 48), 24, replace = False)
    None