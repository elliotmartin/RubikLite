from Rubik import *
import unittest

class test_cube(unittest.TestCase):

    def test_all_basic_moves(self):
        self.assertEqual(I, multiple_perm_apply([F] * 4, I))
        self.assertEqual(I, multiple_perm_apply([R] * 4, I))
        self.assertEqual(I, multiple_perm_apply([U] * 4, I))
        self.assertEqual(I, multiple_perm_apply([B] * 4, I))
        self.assertEqual(I, multiple_perm_apply([D] * 4, I))
        self.assertEqual(I, multiple_perm_apply([L] * 4, I))
        self.assertEqual(I, multiple_perm_apply([Fi] * 4, I))
        self.assertEqual(I, multiple_perm_apply([Ri] * 4, I))
        self.assertEqual(I, multiple_perm_apply([Ui] * 4, I))
        self.assertEqual(I, multiple_perm_apply([Bi] * 4, I))
        self.assertEqual(I, multiple_perm_apply([Di] * 4, I))
        self.assertEqual(I, multiple_perm_apply([Li] * 4, I))

    #sexy refers to the alg RUR'U' which is really nice to perform. when done 6 times it acts as the identity.
    #Testing all cases of this tests all interactions of turns with eachother.
    def test_R_sexy(self):
        self.assertEqual(I, multiple_perm_apply([R,U,Ri,Ui]*6, I))
        self.assertEqual(I, multiple_perm_apply([R,F,Ri,Fi]*6, I))
        self.assertEqual(I, multiple_perm_apply([R,D,Ri,Di]*6, I))
        self.assertEqual(I, multiple_perm_apply([R,B,Ri,Bi]*6, I))

    def test_L_sexy(self):
        self.assertEqual(I, multiple_perm_apply([L,U,Li,Ui]*6, I))
        self.assertEqual(I, multiple_perm_apply([L,F,Li,Fi]*6, I))
        self.assertEqual(I, multiple_perm_apply([L,D,Li,Di]*6, I))
        self.assertEqual(I, multiple_perm_apply([L,B,Li,Bi]*6, I))

    def test_U_sexy(self):
        self.assertEqual(I, multiple_perm_apply([U,F,Ui,Fi]*6, I))
        self.assertEqual(I, multiple_perm_apply([U,B,Ui,Bi]*6, I))
        self.assertEqual(I, multiple_perm_apply([U,R,Ui,Ri]*6, I))
        self.assertEqual(I, multiple_perm_apply([U,L,Ui,Li]*6, I))

    def test_D_sexy(self):
        self.assertEqual(I, multiple_perm_apply([D,F,Di,Fi]*6, I))
        self.assertEqual(I, multiple_perm_apply([D,B,Di,Bi]*6, I))
        self.assertEqual(I, multiple_perm_apply([D,R,Di,Ri]*6, I))
        self.assertEqual(I, multiple_perm_apply([D,L,Di,Li]*6, I))

    def test_F_sexy(self):
        self.assertEqual(I, multiple_perm_apply([F,U,Fi,Ui]*6, I))
        self.assertEqual(I, multiple_perm_apply([F,D,Fi,Di]*6, I))
        self.assertEqual(I, multiple_perm_apply([F,R,Fi,Ri]*6, I))
        self.assertEqual(I, multiple_perm_apply([F,L,Fi,Li]*6, I))

    def test_B_sexy(self):
        self.assertEqual(I, multiple_perm_apply([B,U,Bi,Ui]*6, I))
        self.assertEqual(I, multiple_perm_apply([B,D,Bi,Di]*6, I))
        self.assertEqual(I, multiple_perm_apply([B,R,Bi,Ri]*6, I))
        self.assertEqual(I, multiple_perm_apply([B,L,Bi,Li]*6, I))

    def test_compact_then_flatten(self):
        self.assertEqual(I, expand_cube(compact_cube(I)))
        self.assertEqual(multiple_perm_apply([R,U,F,B,D,L,R,U,L,B], I), expand_cube(compact_cube(multiple_perm_apply([R,U,F,B,D,L,R,U,L,B],I))))

    def test_is_valid(self):
        self.assertEqual(is_valid(I), True)
        corner_twist = (2, 0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47)
        edge_flip = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 47, 46)
        bad_perm_corner = (3, 4, 5, 0, 1, 2, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47)
        bad_perm_edge = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 46, 47, 44, 45)
        self.assertEqual(is_valid(I), True)
        self.assertEqual(is_valid(R), True)
        self.assertEqual(is_valid(multiple_perm_apply([L,R,D,B,R,U,F,R,D], I)), True)
        self.assertEqual(is_valid(corner_twist), False)
        self.assertEqual(is_valid(edge_flip), False)
        self.assertEqual(is_valid(bad_perm_corner), False)
        self.assertEqual(is_valid(bad_perm_edge), False)

if __name__ == '__main__':
    unittest.main()


