from Point import Point
from QuadTree import QuadTree

p1 = Point(5., 5.)
p2 = Point(10., 10.)
p3 = Point(8., 8.)
p4 = Point(2., 2.)
p5 = Point(3., 3.)
p6 = Point(7., 3.)

qt = QuadTree(p1)
qt.insert(p2)
qt.insert(p3)
qt.insert(p4)
qt.insert(p5)
qt.insert(p6)
print(qt)
