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

def perm_apply(perm, cube):
    return (tuple(cube[i] for i in perm))

def perm_inverse(perm):
    inv_perm = [0]*len(perm)
    for i in range(len(perm)):
        inv_perm[perm[i]] = i
    return tuple(inv_perm)

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

#I = (flu, luf, ufl, fur, urf, rfu, fdl, dlf, lfd, frd, rdf, dfr ,bul ,ulb, lbu, bru ,rub, ubr, bld ,ldb ,dbl, bdr, drb, rbd, fu, uf, fr, rf, fl, lf, fd, df, br, rb, bl, lb, bd, db, bu, ub, ur, ru, ul, lu, dr, rd, dl, ld)
#cu= (0,    1,   2,   3,   4,   5,   6,   7,   8,   9,   10, 11,  12,  13,  14,  15,  16,  17,  18,  19,  20,  21,  22,  23,  24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47)
D = (flu, luf, ufl, fur, urf, rfu, frd, rdf, dfr, bdr, drb, rbd, bul, ulb, lbu, bru, rub, ubr, fdl, dlf, lfd, bld, ldb, dbl, fu, uf, fr, rf, fl, lf, rd, dr, br, rb, bl, lb, ld, dl, bu, ub, ur, ru, ul, lu, db, bd, df, fd)
D = (0, 1, 2, 3, 4, 5, 9, 10, 11, 21, 22, 23, 12, 13, 14, 15, 16, 17, 6, 7, 8, 18, 19, 20, 24, 25, 26, 27, 28, 29, 45, 44, 32, 33, 34, 35, 47, 46, 38, 39, 40, 41, 42, 43, 37, 36, 31, 30)

Di = perm_inverse(D)
Di = (0, 1, 2, 3, 4, 5, 18, 19, 20, 6, 7, 8, 12, 13, 14, 15, 16, 17, 21, 22, 23, 9, 10, 11, 24, 25, 26, 27, 28, 29, 47, 46, 32, 33, 34, 35, 45, 44, 38, 39, 40, 41, 42, 43, 31, 30, 37, 36)

R = (flu, luf, ufl, dfr, frd, rdf, fdl, dlf, lfd, drb, rbd, bdr, bul, ulb, lbu, urf, rfu, fur, bld, ldb, dbl, ubr, bru, rub, fu, uf, ur, ru, fl, lf, fd, df, dr, rd, bl, lb, bd, db, bu, ub, br, rb, ul, lu, fr, rf, dl, ld)
R = (0, 1, 2, 11, 9, 10, 6, 7, 8, 22, 23, 21, 12, 13, 14, 4, 5, 3, 18, 19, 20, 17, 15, 16, 24, 25, 40, 41, 28, 29, 30, 31, 44, 45, 34, 35, 36, 37, 38, 39, 32, 33, 42, 43, 26, 27, 46, 47)


Ri = perm_inverse(R)
Ri = (0, 1, 2, 17, 15, 16, 6, 7, 8, 4, 5, 3, 12, 13, 14, 22, 23, 21, 18, 19, 20, 11, 9, 10, 24, 25, 44, 45, 28, 29, 30, 31, 40, 41, 34, 35, 36, 37, 38, 39, 26, 27, 42, 43, 32, 33, 46, 47)

L = (ulb, lbu, bul, fur, urf, rfu, ufl, flu, luf, frd, rdf, dfr, dbl, bld, ldb, bru, rub, ubr, dlf, lfd, fdl, bdr, drb, rbd, fu, uf, fr, rf, fd, df, ul, lu, bu, ub, br, rb, bd, db, dl, ld, ur, ru, dr, rd, fl, lf, bl, lb)
L = (13, 14, 12, 3, 4, 5, 2, 0, 1, 9, 10, 11, 20, 18, 19, 15, 16, 17, 7, 8, 6, 21, 22, 23, 24, 25, 26, 27, 30, 31, 42, 43, 38, 39, 32, 33, 36, 37, 46, 47, 40, 41, 44, 45, 28, 29, 34, 35)

Li = perm_inverse(L)
Li = (7, 8, 6, 3, 4, 5, 20, 18, 19, 9, 10, 11, 2, 0, 1, 15, 16, 17, 13, 14, 12, 21, 22, 23, 24, 25, 26, 27, 44, 45, 28, 29, 34, 35, 46, 47, 36, 37, 32, 33, 40, 41, 30, 31, 42, 43, 38, 39)

moves = (F, Fi, U, Ui, R, Ri, B, Bi, D, Di, L, Li)
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

def test_cube(Move):
    cube = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47)
    perms = [Move]*4
    for p in perms:
        cube = perm_apply(p,cube)
    return cube

#test if four turns does nothing to the cube and if the identity does nothing
def test_four():
    moves = [F, R, U, B, D, L]

    base_cube = (
    0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31,
    32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47)

    for m in moves:
        print(base_cube == perm_apply(I, base_cube))
        print("Move is: " + move_names[m])
        print(test_cube(m))
        print(base_cube == test_cube(m))
        wrong_spots = []
        for b in base_cube:
            if base_cube[b] != test_cube(m)[b]:
                wrong_spots.append(b)
        print('Wrong spots' + str(wrong_spots))
        if len(wrong_spots) % 2 != 0:
            print('you really fucked up here')
        print('__________________________________________________________________________________________________________________________________________________________________')

#write a test for all forms of sexy:
#RURiUi, LULiUi, FUFiUi, BUBiUi
#RDRiDi, LDLiDi, FDFiDi, BDBiDi

#See if we can reduce to only 1 of each corner per tuple and 1 edge by checking to see if the other ones rotate all about clockwise.
#thus if we know 1 we can know the other 3. This could cut down to 20 digits in the tuple instead of 48
#then cube is represented as 0-23 counting by and 24-47 counting by 2

#see if we can determine validity of a cube by the 1st, 4th, etc number and modding by 3 and every 2nd edge mod 2. Should be a way to do this
#find a good way to generate random cube states based on the rules we find for validity

def test_sexy():
    base_cube = (
    0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
    30, 31,
    32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47)

    cube = (
    0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
    31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47)

    sexy = [R, U, Ri, Ui] * 6
    for s in sexy:
        cube = perm_apply(s, cube)
    print(cube)
    print(base_cube == cube)

test_sexy()

#TEST