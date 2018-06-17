import copy
import math
from typing import List

from Point import Point


class QuadTree:
    _TOPLEFT = 0
    _TOPRIGHT = 1
    _BOTTOMRIGHT = 2
    _BOTTOMLEFT = 3
    _POINT_DIRECTIONS = [_TOPLEFT, _TOPRIGHT, _BOTTOMRIGHT, _BOTTOMLEFT]

    _EXTREME_TOPLEFT_POINT = Point(-math.inf, math.inf)
    _EXTREME_TOPRIGHT_POINT = Point(math.inf, math.inf)
    _EXTREME_BOTTOMRIGHT_POINT = Point(math.inf, -math.inf)
    _EXTREME_BOTTOMLEFT_POINT = Point(-math.inf, -math.inf)
    _EXTREME_POINTS = [_EXTREME_TOPLEFT_POINT, _EXTREME_TOPRIGHT_POINT, _EXTREME_BOTTOMRIGHT_POINT,
                       _EXTREME_BOTTOMLEFT_POINT]

    def __init__(self, point: Point = None):
        self.point = point
        self.sons = [None, None, None, None]  # TOPLEFT, TOPRIGHT, BOTTOMRIGHT, BOTTOMLEFT

    def insert(self, p: Point):
        self.insert_quadtree(QuadTree(p))

    def insert_quadtree(self, qt: 'QuadTree'):
        if not self.point:
            self.point = qt.point
            self.sons = qt.sons
        elif self.point == qt.point:
            return
        else:
            child_idx = self._select_child(qt.point)
            if self.sons[child_idx]:
                self.sons[child_idx].insert_quadtree(qt)
            else:
                self.sons[child_idx] = qt

    def search(self, p: Point):
        if not self.point:
            return None
        elif self.point == p:
            return self
        else:
            child_idx = self._select_child(p)
            if self.sons[child_idx]:
                return self.sons[child_idx].search(p)
            else:
                return None

    def delete_with_full_reinsertion(self, p: Point):
        if not self.point:
            return
        elif self.point == p:
            child_points = self.get_all_child_points()
            self.__init__()
            for cp in child_points:
                self.insert(cp.point)
        else:
            child_idx = self._select_child(p)
            if self.sons[child_idx]:
                self.sons[child_idx].delete_with_full_reinsertion(p)
                if not self.sons[child_idx].point:
                    self.sons[child_idx] = None

    def delete_with_partial_reinsertion(self, p: Point):
        if not self.point:
            return
        elif self.point == p:
            if not self._has_sons():
                self.__init__()
            else:
                selected_candidate_child = self._select_node_to_change(p)
                selected_node = self.sons[selected_candidate_child].find_candidate(selected_candidate_child)
                adjacent_nodes = self._get_adjacent_nodes(selected_candidate_child)
                nodes_to_reinsert = []
                for adj_node in (an for an in adjacent_nodes if self.sons[an]):
                    nodes_to_reinsert += self._apply_adj(adj_node, p, selected_node.point)
                self.sons[selected_candidate_child].newroot(selected_candidate_child, self, selected_node.point)
                self._replace_deleted_node(selected_node)
                for node_to_reinsert in nodes_to_reinsert:
                    self.insert_quadtree(node_to_reinsert)
        else:
            child_idx = self._select_child(p)
            if self.sons[child_idx]:
                self.sons[child_idx].delete_with_partial_reinsertion(p)
                if not self.sons[child_idx].point:
                    self.sons[child_idx] = None

    def __repr__(self):
        return str(self.point) + ': (' + \
               str(self.sons[self._TOPLEFT]) + ', ' + \
               str(self.sons[self._TOPRIGHT]) + ', ' + \
               str(self.sons[self._BOTTOMRIGHT]) + ', ' + \
               str(self.sons[self._BOTTOMLEFT]) + ')'

    def get_all_child_points(self):
        child_trees = [child for child in self.sons if child]
        subchild_trees = []
        for c in child_trees:
            subchild_trees += c.get_all_child_points()
        return child_trees + subchild_trees

    def _replace_deleted_node(self, selected_node: 'QuadTree'):
        selected_point = copy.copy(selected_node.point)
        self.delete_with_full_reinsertion(selected_node.point)
        self.point = selected_point

    def _apply_adj(self, adj_node: int, point_to_delete: Point, selected_point: Point):
        nodes_to_reinsert, to_remove = self.sons[adj_node].adj(point_to_delete, selected_point)
        if to_remove:
            self.sons[adj_node] = None
        return nodes_to_reinsert

    def adj(self, point_to_be_deleted: Point, selected_point: Point):
        if not self.point_in_crosshatched(point_to_be_deleted, selected_point):
            susceptible_sons = self._get_susceptible_nodes(point_to_be_deleted, selected_point)
            nodes_to_reinsert = []
            for susceptible_child in (sc for sc in susceptible_sons if self.sons[sc]):
                nodes_to_reinsert += self._apply_adj(susceptible_child, point_to_be_deleted, selected_point)
            return nodes_to_reinsert, False
        else:
            return [self], True

    def newroot(self, i, node_to_be_deleted: 'QuadTree', selected_point: Point):
        adjacent_nodes = self._get_adjacent_nodes(i)
        for adj_node in (an for an in adjacent_nodes if self.sons[an]):
            nodes_to_reinsert = self._apply_adj(adj_node, node_to_be_deleted.point, selected_point)
            for node in nodes_to_reinsert:
                if node_to_be_deleted.sons[adj_node]:
                    node_to_be_deleted.sons[adj_node].insert_quadtree(node)
                else:
                    node_to_be_deleted.sons[adj_node] = node
        if self.sons[self._conjugate(i)]:
            self.sons[self._conjugate(i)].newroot(i, node_to_be_deleted, selected_point)

    def _select_child(self, p: Point):
        return self.get_point_direction(p, self.point)

    def get_point_direction(self, p: Point, reference_point: Point):
        if p.y >= reference_point.y:
            if p.x >= reference_point.x:
                return self._TOPRIGHT
            else:
                return self._TOPLEFT
        else:
            if p.x >= reference_point.x:
                return self._BOTTOMRIGHT
            else:
                return self._BOTTOMLEFT

    @staticmethod
    def _conjugate(n: int):
        return (n + 2) % 4

    def find_candidate(self, quadrant: int):
        conjugate_quadrant = self._conjugate(quadrant)
        if not self.sons[conjugate_quadrant]:
            return self
        else:
            return self.sons[conjugate_quadrant].find_candidate(quadrant)

    def _get_candidates(self):
        candidates = []
        for idx, child in enumerate(self.sons):
            if child:
                candidates.append(child.find_candidate(idx).point)
            else:
                candidates.append(self._EXTREME_POINTS[idx])
        return candidates

    def _check_first_property(self, candidates: List[Point]):
        p_tl = candidates[self._TOPLEFT]
        p_tr = candidates[self._TOPRIGHT]
        p_bl = candidates[self._BOTTOMLEFT]
        p_br = candidates[self._BOTTOMRIGHT]

        candidates_fp_x = [False] * 4
        candidates_fp_x[self._TOPLEFT] = p_tl.y < p_tr.y
        candidates_fp_x[self._TOPRIGHT] = p_tr.y < p_tl.y
        candidates_fp_x[self._BOTTOMLEFT] = p_bl.y > p_br.y
        candidates_fp_x[self._BOTTOMRIGHT] = p_br.y > p_bl.y

        candidates_fp_y = [False] * 4
        candidates_fp_y[self._TOPLEFT] = p_tl.x > p_bl.x
        candidates_fp_y[self._BOTTOMLEFT] = p_bl.x > p_tl.x
        candidates_fp_y[self._TOPRIGHT] = p_tr.x < p_br.x
        candidates_fp_y[self._BOTTOMRIGHT] = p_br.x < p_tr.x

        return [x and y for (x, y) in zip(candidates_fp_x, candidates_fp_y)]

    @staticmethod
    def _get_adjacent_nodes(node: int):
        return [(node + 1) % 4, (node - 1) % 4]

    def point_in_crosshatched(self, point_to_be_deleted: Point, selected_point: Point):
        up_bound = max(point_to_be_deleted.y, selected_point.y)
        bottom_bound = min(point_to_be_deleted.y, selected_point.y)
        right_bound = max(point_to_be_deleted.x, selected_point.x)
        left_bound = min(point_to_be_deleted.x, selected_point.x)
        return up_bound > self.point.y > bottom_bound or left_bound < self.point.x < right_bound

    def _get_susceptible_nodes(self, point_to_be_deleted: Point, selected_point: Point):
        direction_change = self.get_point_direction(selected_point, point_to_be_deleted)
        direction_point = self.get_point_direction(self.point, point_to_be_deleted)
        directions = [d for d in list(self._POINT_DIRECTIONS) if d not in [direction_change, direction_point]]
        return directions

    def _has_sons(self):
        return any(c is not None for c in self.sons)

    def _select_node_to_change(self, p: Point):
        candidates = self._get_candidates()
        candidates_fp = self._check_first_property(candidates)
        if candidates_fp.count(True) == 1:
            return candidates_fp.index(True)
        elif candidates_fp.count(True) > 1:
            l1_values = [math.inf] * len(candidates)
            for idx, c_fp in enumerate(candidates_fp):
                if c_fp:
                    l1_values[idx] = self._compute_l1(candidates[idx], p)
            selected_candidate, _ = min(enumerate(l1_values), key=lambda v: v[1])
            return selected_candidate
        else:
            l1_values = [self._compute_l1(cand, p) for cand in candidates]
            selected_candidate, _ = min(enumerate(l1_values), key=lambda v: v[1])
            return selected_candidate

    @staticmethod
    def _compute_l1(cand, p):
        return abs(p.x - cand.x) + abs(p.y - cand.y)
