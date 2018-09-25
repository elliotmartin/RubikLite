import Rubik

def test_cube(Move):
    cube = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47)
    perms = [Move]*4
    for p in perms:
        cube = Rubik.perm_apply(p,cube)
    return cube

#test if four turns does nothing to the cube and if the identity does nothing
def test_four():
    moves = [Rubik.F, Rubik.R, Rubik.U, Rubik.B, Rubik.D, Rubik.L]

    base_cube = (
    0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31,
    32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47)

    for m in moves:
        print(base_cube == Rubik.perm_apply(Rubik.I, base_cube))
        print("Move is: " + Rubik.move_names[m])
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

    sexy = [Rubik.R, Rubik.U, Rubik.Ri, Rubik.Ui] * 6
    for s in sexy:
        cube = Rubik.perm_apply(s, cube)
    print(cube)
    print(base_cube == cube)

test_sexy()