import unittest

from Point import Point
from QuadTree import QuadTree


def p(x, y):
    return Point(float(x), float(y))


class QuadTreesTest(unittest.TestCase):
    _TOPLEFT = 0
    _TOPRIGHT = 1
    _BOTTOMRIGHT = 2
    _BOTTOMLEFT = 3

    def test_build_empty_tree(self):
        qt = QuadTree()
        self.assertEqual('None: (None, None, None, None)', str(qt))

    def test_build_single_tree(self):
        qt = QuadTree(p(0, 0))
        self.assertEqual('[0.0, 0.0]: (None, None, None, None)', str(qt))

    def test_insert_point_in_first_level(self):
        qt = QuadTree()
        qt.insert(p(0, 0))
        self.assertEqual('[0.0, 0.0]: (None, None, None, None)', str(qt))

    def test_insert_3_point_in_the_same_level(self):
        qt = QuadTree()
        qt.insert(p(1, 1))
        qt.insert(p(0, 0))
        qt.insert(p(2, 2))
        self.assertEqual(
            '[1.0, 1.0]: (None, [2.0, 2.0]: (None, None, None, None), None, [0.0, 0.0]: (None, None, None, None))',
            str(qt))

    def test_insert_3_point_in_deep(self):
        qt = QuadTree()
        qt.insert(p(0, 0))
        qt.insert(p(2, 2))
        qt.insert(p(1, 1))
        self.assertEqual(
            '[0.0, 0.0]: (None, [2.0, 2.0]: (None, None, None, [1.0, 1.0]: (None, None, None, None)), None, None)',
            str(qt))

    def test_search_root_point(self):
        qt = QuadTree(p(0, 0))
        res = qt.search(p(0, 0))
        self.assertEqual('[0.0, 0.0]: (None, None, None, None)', str(res))

    def test_search_second_level_point_with_child(self):
        qt = QuadTree()
        qt.insert(p(0, 0))
        qt.insert(p(2, 2))
        qt.insert(p(1, 1))
        res = qt.search(p(2, 2))
        self.assertEqual('[2.0, 2.0]: (None, None, None, [1.0, 1.0]: (None, None, None, None))', str(res))

    def test_search_nonexistent_point(self):
        qt = QuadTree()
        res = qt.search(p(0, 0))
        self.assertEqual('None', str(res))

    def test_get_childs_of_empty_tree(self):
        qt = QuadTree()
        res = qt.get_all_child_points()
        self.assertEqual(0, len(res))

    def test_get_childs_of_single_tree(self):
        qt = QuadTree(p(0, 0))
        res = qt.get_all_child_points()
        self.assertEqual(0, len(res))

    def test_get_childs_of_two_level_tree(self):
        qt = QuadTree(p(1, 1))
        qt.insert(p(0, 0))
        res = qt.get_all_child_points()
        self.assertEqual(1, len(res))
        self.assertEqual('[0.0, 0.0]: (None, None, None, None)', str(res[0]))

    def test_get_childs_of_three_level_tree(self):
        qt = QuadTree(p(0, 0))
        qt.insert(p(1, 1))
        qt.insert(p(2, 2))
        res = qt.get_all_child_points()
        self.assertEqual(2, len(res))
        self.assertEqual('[1.0, 1.0]: (None, [2.0, 2.0]: (None, None, None, None), None, None)', str(res[0]))
        self.assertEqual('[2.0, 2.0]: (None, None, None, None)', str(res[1]))

    def test_delete_unique_point_with_reinserting(self):
        qt = QuadTree(p(0, 0))
        qt.delete_with_full_reinsertion(p(0, 0))
        self.assertEqual('None: (None, None, None, None)', str(qt))

    def test_delete_leaf_point_with_reinserting(self):
        qt = QuadTree(p(0, 0))
        qt.insert(p(1, 1))
        qt.delete_with_full_reinsertion(p(1, 1))
        self.assertEqual('[0.0, 0.0]: (None, None, None, None)', str(qt))

    def test_delete_root_point_with_reinserting(self):
        qt = QuadTree(p(0, 0))
        qt.insert(p(1, 1))
        qt.delete_with_full_reinsertion(p(0, 0))
        self.assertEqual('[1.0, 1.0]: (None, None, None, None)', str(qt))

    def test_delete_intermediate_point_with_reinserting(self):
        qt = QuadTree(p(0, 0))
        qt.insert(p(1, 1))
        qt.insert(p(2, 2))
        qt.delete_with_full_reinsertion(p(1, 1))
        self.assertEqual('[0.0, 0.0]: (None, [2.0, 2.0]: (None, None, None, None), None, None)', str(qt))

    def test_find_candidate_with_single_node(self):
        qt = QuadTree(p(0, 0))
        cand1 = qt.find_candidate(self._TOPRIGHT)
        cand2 = qt.find_candidate(self._TOPLEFT)
        cand3 = qt.find_candidate(self._BOTTOMLEFT)
        cand4 = qt.find_candidate(self._BOTTOMRIGHT)
        self.assertEqual('[0.0, 0.0]: (None, None, None, None)', str(cand1))
        self.assertEqual('[0.0, 0.0]: (None, None, None, None)', str(cand2))
        self.assertEqual('[0.0, 0.0]: (None, None, None, None)', str(cand3))
        self.assertEqual('[0.0, 0.0]: (None, None, None, None)', str(cand4))

    def test_find_candidate_with_a_child(self):
        qt = QuadTree(p(1, 1))
        qt.insert(p(0, 0))
        cand = qt.find_candidate(self._TOPRIGHT)
        self.assertEqual('[0.0, 0.0]: (None, None, None, None)', str(cand))

    def test_delete_unique_point_with_partial_reinserting(self):
        qt = QuadTree(p(0, 0))
        qt.delete_with_partial_reinsertion(p(0, 0))
        self.assertEqual('None: (None, None, None, None)', str(qt))

    def test_delete_leaf_point_with_partial_reinserting(self):
        qt = QuadTree(p(0, 0))
        qt.insert(p(1, 1))
        qt.delete_with_partial_reinsertion(p(1, 1))
        self.assertEqual('[0.0, 0.0]: (None, None, None, None)', str(qt))

    def test_delete_root_point_with_partial_reinserting(self):
        qt = QuadTree(p(0, 0))
        qt.insert(p(1, 1))
        qt.delete_with_partial_reinsertion(p(0, 0))
        self.assertEqual('[1.0, 1.0]: (None, None, None, None)', str(qt))

    def test_delete_intermediate_point_with_partial_reinserting(self):
        qt = QuadTree(p(0, 0))
        qt.insert(p(1, 1))
        qt.insert(p(2, 2))
        qt.delete_with_partial_reinsertion(p(1, 1))
        self.assertEqual('[0.0, 0.0]: (None, [2.0, 2.0]: (None, None, None, None), None, None)', str(qt))

    # Input: Figure 1; Output: Figure 9
    def test_delete_paper_example_with_partial_reinserting(self):
        qt = QuadTree(p(50, 50))  # A
        qt.insert(p(66, 66))  # F
        qt.insert(p(33, 62))  # J
        qt.insert(p(24, 42))  # M
        qt.insert(p(72, 34))  # N
        qt.insert(p(76, 74))  # G
        qt.insert(p(59, 72))  # H
        qt.insert(p(55, 58))  # B
        qt.insert(p(86, 52))  # I
        qt.insert(p(22, 68))  # K
        qt.insert(p(29, 56))  # L
        qt.insert(p(62, 62))  # C
        qt.insert(p(53, 64))  # D
        qt.insert(p(61, 54))  # E

        qt.delete_with_partial_reinsertion(p(50, 50))

        res_qt = QuadTree(p(55, 58))  # B
        res_qt.insert(p(66, 66))  # F
        res_qt.insert(p(33, 62))  # J
        res_qt.insert(p(24, 42))  # M
        res_qt.insert(p(72, 34))  # N
        res_qt.insert(p(76, 74))  # G
        res_qt.insert(p(59, 72))  # H
        res_qt.insert(p(62, 62))  # C
        res_qt.insert(p(53, 64))  # D
        res_qt.insert(p(22, 68))  # K
        res_qt.insert(p(29, 56))  # L
        res_qt.insert(p(86, 52))  # I
        res_qt.insert(p(61, 54))  # E
        self.assertEqual(str(res_qt), str(qt))

    # Figure 4
    def test_delete_paper_example_with_partial_reinserting_that_doesnt_requires_reinsertion(self):
        qt = QuadTree(p(50, 50))  # A
        qt.insert(p(25, 60))  # E
        qt.insert(p(68, 63))  # B
        qt.insert(p(83, 57))  # C
        qt.insert(p(59, 68))  # D
        qt.insert(p(78, 40))  # F
        qt.insert(p(36, 38))  # H
        qt.insert(p(43, 45))  # G

        qt.delete_with_partial_reinsertion(p(50, 50))

        res_qt = QuadTree(p(43, 45))  # G
        res_qt.insert(p(25, 60))  # E
        res_qt.insert(p(68, 63))  # B
        res_qt.insert(p(83, 57))  # C
        res_qt.insert(p(59, 68))  # D
        res_qt.insert(p(78, 40))  # F
        res_qt.insert(p(36, 38))  # H
        self.assertEqual(str(res_qt), str(qt))

    # Figure 5
    def test_delete_paper_example_with_partial_reinserting_with_no_closest_terminal_node(self):
        qt = QuadTree(p(50, 50))  # A
        qt.insert(p(44, 66))  # C
        qt.insert(p(60, 60))  # B
        qt.insert(p(60, 27))  # E
        qt.insert(p(37, 37))  # D

        qt.delete_with_partial_reinsertion(p(50, 50))

        res_qt = QuadTree(p(60, 60))  # B
        res_qt.insert(p(60, 27))  # E
        res_qt.insert(p(37, 37))  # D
        res_qt.insert(p(44, 66))  # C
        self.assertEqual(str(res_qt), str(qt))

    # Figure 6
    def test_delete_paper_example_with_partial_reinserting_with_two_closest_nodes(self):
        p_50_50 = p(50, 50)
        qt = QuadTree(p_50_50)  # A
        qt.insert(p(40, 63))  # C
        qt.insert(p(60, 60))  # B
        qt.insert(p(66, 41))  # E
        qt.insert(p(44, 44))  # D

        qt.delete_with_partial_reinsertion(p_50_50)

        res_qt = QuadTree(p(44, 44))  # D
        res_qt.insert(p(40, 63))  # C
        res_qt.insert(p(60, 60))  # B
        res_qt.insert(p(66, 41))  # E

        self.assertEqual(str(res_qt), str(qt))


if __name__ == '__main__':
    unittest.main()
