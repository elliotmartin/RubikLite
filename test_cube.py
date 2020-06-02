from Rubik import *
import unittest

class TestCube(unittest.TestCase):


    def test_all_basic_moves(self):
        """Tests each by move by applying it 4 times on a solve cube and confirming that it returns a solved cube"""
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

    """sexy refers to the alg RUR'U' which is really nice to perform. when done 6 times it acts as the identity.
    # Testing all cases of this tests all interactions of turns with eachother"""
    def test_R_sexy(self):
        self.assertEqual(I, multiple_perm_apply([R, U, Ri, Ui] * 6, I))
        self.assertEqual(I, multiple_perm_apply([R, F, Ri, Fi] * 6, I))
        self.assertEqual(I, multiple_perm_apply([R, D, Ri, Di] * 6, I))
        self.assertEqual(I, multiple_perm_apply([R, B, Ri, Bi] * 6, I))

    def test_L_sexy(self):
        self.assertEqual(I, multiple_perm_apply([L, U, Li, Ui] * 6, I))
        self.assertEqual(I, multiple_perm_apply([L, F, Li, Fi] * 6, I))
        self.assertEqual(I, multiple_perm_apply([L, D, Li, Di] * 6, I))
        self.assertEqual(I, multiple_perm_apply([L, B, Li, Bi] * 6, I))

    def test_U_sexy(self):
        self.assertEqual(I, multiple_perm_apply([U, F, Ui, Fi] * 6, I))
        self.assertEqual(I, multiple_perm_apply([U, B, Ui, Bi] * 6, I))
        self.assertEqual(I, multiple_perm_apply([U, R, Ui, Ri] * 6, I))
        self.assertEqual(I, multiple_perm_apply([U, L, Ui, Li] * 6, I))

    def test_D_sexy(self):
        self.assertEqual(I, multiple_perm_apply([D, F, Di, Fi] * 6, I))
        self.assertEqual(I, multiple_perm_apply([D, B, Di, Bi] * 6, I))
        self.assertEqual(I, multiple_perm_apply([D, R, Di, Ri] * 6, I))
        self.assertEqual(I, multiple_perm_apply([D, L, Di, Li] * 6, I))

    def test_F_sexy(self):
        self.assertEqual(I, multiple_perm_apply([F, U, Fi, Ui] * 6, I))
        self.assertEqual(I, multiple_perm_apply([F, D, Fi, Di] * 6, I))
        self.assertEqual(I, multiple_perm_apply([F, R, Fi, Ri] * 6, I))
        self.assertEqual(I, multiple_perm_apply([F, L, Fi, Li] * 6, I))

    def test_B_sexy(self):
        self.assertEqual(I, multiple_perm_apply([B, U, Bi, Ui] * 6, I))
        self.assertEqual(I, multiple_perm_apply([B, D, Bi, Di] * 6, I))
        self.assertEqual(I, multiple_perm_apply([B, R, Bi, Ri] * 6, I))
        self.assertEqual(I, multiple_perm_apply([B, L, Bi, Li] * 6, I))

    def test_all_turns_by_solving_(self):
        """tests all moves by scrambling and then solving a cube"""
        scramble = multiple_perm_apply([Ri, Ui, F, Di, L, L, B, B, R, R, B, B, U, F, F, D, U, F, F, R, R, F, D, R, R, B,
                                        L, Di, B, B, Ri, Di, F, F, Ri, Ui, F], I)
        solution = multiple_perm_apply([R, Li, Di, L, Ui, R, R, Di, L, L, Di, L, L, D, F, F, U, U, F, F, L, L, F, R, R],
                                       scramble)
        self.assertEqual(I, solution)
        self.assertEqual(multiple_perm_apply([R, U, Ri, Ui, Li, U, L, F, Ui, Fi, R, Ui, Ri, Ui, Li, U, U, L, Ui, Li, U,
                                              L, Ui, F, R, U, Ri, Ui, Fi, Ui, Li, U, U, L, U, U, Li,U, L, F, R, U, Ri,
                                              Ui, Fi, F, R, U, Ri, Ui, Fi, Ri, Fi, Li, F, R, Fi, L, F, R, Ui, R, U, R,
                                              U, R, Ui, Ri, Ui, R, R, Ui, R, U, Ri, Ui, Ri, F, R, R, Ui, Ri, Ui, R, U,
                                              Ri, Fi, U], I)
                         , I)

    def test_compact_cube(self):
        """Tests the compact cube method by compacting, then expanding a cube"""
        self.assertEqual(I, expand_cube(compact_cube(I)))
        self.assertEqual(multiple_perm_apply([R,U,F,B,D,L,R,U,L,B], I), expand_cube(compact_cube(multiple_perm_apply([R,U,F,B,D,L,R,U,L,B],I))))

    def test_check_corner_orientation_validity(self):
        self.assertEqual(check_corner_orientation_validity(I), True)
        self.assertEqual(check_corner_orientation_validity(F), True)
        self.assertEqual(check_corner_orientation_validity(Fi), True)
        self.assertEqual(check_corner_orientation_validity(R), True)
        self.assertEqual(check_corner_orientation_validity(Ri), True)
        self.assertEqual(check_corner_orientation_validity(U), True)
        self.assertEqual(check_corner_orientation_validity(Ui), True)
        self.assertEqual(check_corner_orientation_validity(B), True)
        self.assertEqual(check_corner_orientation_validity(Bi), True)
        self.assertEqual(check_corner_orientation_validity(D), True)
        self.assertEqual(check_corner_orientation_validity(Di), True)
        self.assertEqual(check_corner_orientation_validity(L), True)
        self.assertEqual(check_corner_orientation_validity(Li), True)
        corner_twist = (
        2, 0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
        30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47)
        self.assertEqual(check_corner_orientation_validity(corner_twist), False)

    def test_check_edge_orientation_validity(self):
        self.assertEqual(check_edge_orientation_validity(I), True)
        self.assertEqual(check_edge_orientation_validity(F), True)
        self.assertEqual(check_edge_orientation_validity(Fi), True)
        self.assertEqual(check_edge_orientation_validity(R), True)
        self.assertEqual(check_edge_orientation_validity(Ri), True)
        self.assertEqual(check_edge_orientation_validity(U), True)
        self.assertEqual(check_edge_orientation_validity(Ui), True)
        self.assertEqual(check_edge_orientation_validity(B), True)
        self.assertEqual(check_edge_orientation_validity(Bi), True)
        self.assertEqual(check_edge_orientation_validity(D), True)
        self.assertEqual(check_edge_orientation_validity(Di), True)
        self.assertEqual(check_edge_orientation_validity(L), True)
        self.assertEqual(check_edge_orientation_validity(Li), True)
        edge_flip = (
        0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
        30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 47, 46)
        self.assertEqual(check_edge_orientation_validity(edge_flip), False)

    def test_check_permutation_parity(self):
        for m in moves:
            self.assertEqual(check_permutation_parity(I), True)
            self.assertEqual(check_permutation_parity(R), True)
            self.assertEqual(check_permutation_parity(Ri), True)
            self.assertEqual(check_permutation_parity(L), True)
            self.assertEqual(check_permutation_parity(Li), True)
            self.assertEqual(check_permutation_parity(U), True)
            self.assertEqual(check_permutation_parity(Ui), True)
            self.assertEqual(check_permutation_parity(D), True)
            self.assertEqual(check_permutation_parity(Di), True)
            self.assertEqual(check_permutation_parity(F), True)
            self.assertEqual(check_permutation_parity(Fi), True)
            self.assertEqual(check_permutation_parity(B), True)
            self.assertEqual(check_permutation_parity(Bi), True)
            bad_perm_corner = (3, 4, 5, 0, 1, 2, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47)
            bad_perm_edge = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 46, 47, 44, 45)
            self.assertEqual(check_permutation_parity(bad_perm_corner), False)
            self.assertEqual(check_permutation_parity(bad_perm_edge), False)

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

    def test_generate_cube(self):
        for i in range(100):
            self.assertEqual(is_valid(generate_cube()), True)


if __name__ == '__main__':
    unittest.main()


