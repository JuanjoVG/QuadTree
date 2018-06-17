import copy
import random
import statistics
import time

import matplotlib.pyplot as plt

from Point import Point
from QuadTree import QuadTree

plot_filename = 'Timing.PNG'
test_sizes = [16, 32, 64, 128, 256, 512, 1024, 2048, 4096]
replications = 100

random.seed(24011994)


def rand():
    return round(random.uniform(0., 1000.), 3)


def generate_points(n):
    return [Point(rand(), rand()) for _ in range(n)]


def generate_qt(points):
    qt = QuadTree()
    for p in points:
        qt.insert(p)
    return qt


results = {}
for test_size in test_sizes:
    for replication in range(replications):
        print('Executing..', test_size, replication)
        points = generate_points(test_size)
        qt = generate_qt(points)

        points_to_delete = list(points)
        random.shuffle(points_to_delete)

        qt_copy = copy.deepcopy(qt)
        print('- Simple', test_size, replication)
        start_time = time.time()
        for idx, ptd in enumerate(points_to_delete):
            # print('-- Delete point', idx)
            qt_copy.delete_with_full_reinsertion(ptd)
        total_time_simple = (time.time() - start_time) * 1000  # ms

        qt_copy = copy.deepcopy(qt)
        print('- Improved', test_size, replication)
        start_time = time.time()
        for idx, ptd in enumerate(points_to_delete):
            # print('-- Delete point', idx)
            qt_copy.delete_with_partial_reinsertion(ptd)
        total_time_improved = (time.time() - start_time) * 1000  # ms

        if test_size not in results:
            results[test_size] = {}
        results[test_size][replication] = {'Simple': total_time_simple, 'Improved': total_time_improved}

print(results)


def compute_results(version, op):
    return [round(op([v[version] for v in results[size].values()]), 3) for size in test_sizes]


simple_times_mean = compute_results('Simple', statistics.mean)
improved_times_mean = compute_results('Improved', statistics.mean)
simple_times_min = compute_results('Simple', min)
improved_times_min = compute_results('Improved', min)
simple_times_max = compute_results('Simple', max)
improved_times_max = compute_results('Improved', max)
simple_times_stdev = compute_results('Simple', statistics.stdev)
improved_times_stdev = compute_results('Improved', statistics.stdev)

print(simple_times_mean)
print(improved_times_mean)
print(simple_times_min)
print(improved_times_min)
print(simple_times_max)
print(improved_times_max)
print(simple_times_stdev)
print(improved_times_stdev)

plt.plot(test_sizes, simple_times_mean, c='r')
plt.plot(test_sizes, improved_times_mean, c='b')

plt.legend(['Simple', 'Improved'], loc='upper left')

plt.savefig('img/' + plot_filename)
plt.show()
