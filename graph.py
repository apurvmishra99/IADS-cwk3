import math
import sys
import itertools


def euclid(p, q):
    x = p[0]-q[0]
    y = p[1]-q[1]
    return math.sqrt(x*x+y*y)

def route_generator(length):
    for route in itertools.permutations(range(1, length)):
        yield (0, ) + route

class Graph:

    # Complete as described in the specification, taking care of two cases:
    # the -1 case, where we read points in the Euclidean plane, and
    # the n>0 case, where we read a general graph in a different format.
    # self.perm, self.dists, self.n are the key variables to be set up.
    def __init__(self, n, filename):
        if n == -1:
            try:
                self.n = int("".join(filter(str.isdigit, filename)))
            except Exception as e:
                self.n = len(open(filename).readlines(  ))
            self.dists = [[0 for i in range(self.n)] for j in range(self.n)]
            self.perm = [i for i in range(self.n)]
            points = []
            with open(filename) as f:
                all_points = f.readlines()
                for point in all_points:
                    point = list(map(float, point.split()))
                    points.append(point)

            for i in range(self.n):
                start = points[i]
                for j in range(self.n):
                    if i == j:
                        continue
                    end = points[j]
                    self.dists[i][j] = euclid(start, end)
        elif n > 0:
            self.n = n
            self.perm = [i for i in range(self.n)]
            self.dists = [[0 for i in range(self.n)] for j in range(self.n)]
            with open(filename) as f:
                all_points = f.readlines()
                for point in all_points:
                    x, y, dist = list(map(int, point.split()))
                    self.dists[x][y], self.dists[y][x] = dist, dist

    # Complete as described in the spec, to calculate the cost of the
    # current tour (as represented by self.perm).

    def tourValue(self):
        total_value = 0
        journey_order = zip(self.perm, self.perm[1:]+[self.perm[0]])
        for leg in journey_order:
            i, j = leg
            total_value += self.dists[i][j]
        return total_value

    # Generalised tour value method
    # Attempt the swap of cities i and i+1 in self.perm and commit
    # commit to the swap if it improves the cost of the tour.
    # Return True/False depending on success.

    def trySwap(self, i):
        orig_cost = self.tourValue()
        perm_copy = self.perm.copy()
        self.perm[i], self.perm[(
            i+1) % self.n] = self.perm[(i+1) % self.n], self.perm[i]
        swapped_cost = self.tourValue()
        if orig_cost <= swapped_cost:
            self.perm = perm_copy
            return False
        return True
    # Consider the effect of reversiing the segment between
    # self.perm[i] and self.perm[j], and commit to the reversal
    # if it improves the tour value.
    # Return True/False depending on success.

    def tryReverse(self, i, j):
        orig_cost = self.tourValue()
        perm_copy = self.perm.copy()
        while i < j:
            self.perm[i], self.perm[j] = self.perm[j], self.perm[i]
            i += 1
            j -= 1
        swapped_cost = self.tourValue()
        if orig_cost <= swapped_cost:
            self.perm = perm_copy
            return False
        return True

    def swapHeuristic(self):
        better = True
        while better:
            better = False
            for i in range(self.n):
                if self.trySwap(i):
                    better = True

    def TwoOptHeuristic(self):
        better = True
        while better:
            better = False
            for j in range(self.n-1):
                for i in range(j):
                    if self.tryReverse(i, j):
                        better = True

    def nearest_node(self, not_visited, last):
        min_dist = float('inf')
        next_node = last
        for node in not_visited:
            if self.dists[last][node] < min_dist:
                min_dist = self.dists[last][node]
                next_node = node
        return next_node

    # Implement the Greedy heuristic which builds a tour starting
    # from node 0, taking the closest (unused) node as 'next'
    # each time.
    def Greedy(self):
        visited = [0]
        not_visited = set(i for i in range(1, self.n))

        for i in range(self.n - 1):
            last = visited[-1]
            next_node = self.nearest_node(not_visited, last)
            visited.append(next_node)
            not_visited.remove(next_node)

        self.perm = visited

    def MST(self):
        mst = [0] * self.n
        mst[0] = 0

        a = [float('inf')] * self.n
        visited = [0] * self.n

        while not all(visited):
            if sum(visited) == 0:
                u = 0
            else:
                u = a.index(min(a))
            visited[u] = 1
            a[u] = float('inf')

            for v in range(self.n):
                if not visited[v] and self.dists[u][v] < a[v]:
                    a[v] = self.dists[u][v]
                    mst[v] = u

        return mst

    def DFS(self, mst):
        tsp = []
        stack = [0]
        visited = [0] * self.n
        visited[0] = 1

        while len(stack):

            cur = stack.pop()
            tsp.append(cur)

            for i in range(self.n):
                if not visited[i] and mst[i] == cur:
                    stack.append(i)
                    visited[i] = 1

        tsp.append(0)
        return tsp

    # Implementing the 2-Approximation Algorithm
    def myPartC(self):
        mst = self.MST()
        tsp = self.DFS(mst)
        self.perm = tsp

    def brute_force(self):
        values = []
        for route in route_generator(self.n):
            r = list(route)
            self.perm = r 
            tour_val = self.tourValue()
            values.append(tour_val)
        return min(values)