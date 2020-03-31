import math
import graph
import random
import signal
import timeit
import numpy as np
import matplotlib.pyplot as plt
from math import pi, sin, cos, sqrt
from timeit import default_timer as timer

# Custom exception class


class TimeoutException(Exception):
    pass

# Custom signal handler


def timeout_handler(signum, frame):
    raise TimeoutException


# Change the behavior of SIGALRM
signal.signal(signal.SIGALRM, timeout_handler)


def check_triangle(arr):
    n = len(arr)
    for i in range(n-2):
        for j in range(i+1, n-1):
            for k in range(j+1, n):
                a, b, c = arr[i], arr[j], arr[k]
                if a + b < c or b + c < a or a + c < b:
                    return False
    return True


def euclid(p, q):
    x = p[0]-q[0]
    y = p[1]-q[1]
    return math.sqrt(x*x+y*y)


def euclidean_points(n, window):
    random.seed(n)
    points = []
    for i in range(n):
        points.append((random.randint(-window, window),
                       random.randint(-window, window)))
    return points


def euclidean_points_cirlce(r, n=10):
    return [(cos(2*pi/n*x)*r, sin(2*pi/n*x)*r) for x in range(0, n)]


def write_x_y_points_to_file(points, i, name):
    random.shuffle(points)
    with open(f"tests/{name}_{i}", "w+") as f:
        for p in points:
            p = tuple(map(round, p))
            f.write(f"{p[0]} {p[1]}\n")


def gen_euclidean_tests_circle():
    for i in range(100, 1100, 100):
        test_graph = euclidean_points_cirlce(i*10, i)
        write_x_y_points_to_file(test_graph, i, "euclid_circle")


def gen_euclidean_points():
    for i in range(10, 110, 10):
        test_graph = euclidean_points(i*10, i)
        write_x_y_points_to_file(test_graph, i, "euclid")


def gen_metric_points():
    for i in range(10, 110, 10):
        with open(f"tests/metric_10_{i}", 'w+') as f:
            flag = True
            arr = []
            while flag:
                arr = [random.randint(100, 150) for i in range(45)]
                flag = not(check_triangle(arr))
            for x in range(10):
                for y in range(x+1, 10):
                    rand = arr.pop()
                    string = f"{x} {y} {rand}\n"
                    f.write(string)


def gen_non_metric_points():
    for i in range(10, 110, 10):
        with open(f"tests/non_metric_{i}", 'w+') as f:
            for x in range(i):
                for y in range(x+1, i):
                    rand = random.randint(0, 5000)
                    string = f"{x} {y} {rand}\n"
                    f.write(string)


def test(test_name):

    n = -1

    for i in range(10, 110, 10):
        if test_name in {"metric", "non_metric"}:
            if test_name == "non_metric":
                n = i
            else:
                n = 10

        g = graph.Graph(n, f"tests/{test_name}_{i}")
        g.swapHeuristic()
        swap = g.tourValue()

        g = graph.Graph(n, f"tests/{test_name}_{i}")
        g.TwoOptHeuristic()
        two_opt = g.tourValue()

        g = graph.Graph(n, f"tests/{test_name}_{i}")
        g.Greedy()
        greedy = g.tourValue()

        g = graph.Graph(n, f"tests/{test_name}_{i}")
        g.myPartC()
        approx2 = g.tourValue()

        with open(f"results/{test_name}", "a+") as f:
            string = f"{test_name}_{i} & {swap} & {two_opt} & {greedy} & {approx2} \\\\\n"
            f.write(string)


def execution_time(func):
    signal.alarm(60)
    try:
        time = timeit.timeit(f'{func()}', globals=globals())
        return round(time, 6)
    except TimeoutException as e:
        return "Too Long"


# We are going to test performance of our algorithms on euclid_cirle becuase of the large no. of nodes
def test_performance(test_name):
    n = -1
    test_name = "euclid_circle"
    for i in range(10, 1100, 10):
        if test_name in {"metric", "non_metric"}:
            if test_name == "non_metric":
                n = i
            else:
                n = 10
        g = graph.Graph(n, f"tests/{test_name}_{i}")
        swap = execution_time(g.swapHeuristic)

        g = graph.Graph(n, f"tests/{test_name}_{i}")
        two_opt = execution_time(g.TwoOptHeuristic)

        g = graph.Graph(n, f"tests/{test_name}_{i}")
        greedy = execution_time(g.Greedy)

        g = graph.Graph(n, f"tests/{test_name}_{i}")
        approx2 = execution_time(g.myPartC)

        with open(f"results/time_{test_name}", "a+") as f:
            string = f"{test_name}_{i} & {swap} & {two_opt} & {greedy} & {approx2} \\\\\n"
            f.write(string)


# Generate and run the tests
def main():
    gen_euclidean_points()
    gen_euclidean_tests_circle()
    gen_metric_points()
    gen_non_metric_points()

    test_names = ["euclid", "euclid_cirle", "metric_10", "non_metric"]

    for test_name in test_names:
        test(test_name)
    for test_name in test_names:
        test_performance(test_name)


if __name__ == "__main__":
    main()
