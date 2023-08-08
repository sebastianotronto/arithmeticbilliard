import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from math import pi, sin, cos, degrees, gcd #, lcm (python3.9+ only)

# Python 3.8 or lower
def lcm(a, b):
	return a*b // gcd(a,b)

###############################################################################
# This part is generic for any size
###############################################################################
def is_corner(n, sizes, point):
	for i in range(n):
		if point[i] % sizes[i] != 0:
			return False
	return True

def is_bouncing(n, sizes, point):
	for i in range(n):
		if point[i] % sizes[i] == 0:
			return True
	return False

def lcm_list(L):
	ret = 1
	for e in L:
		ret = lcm(ret, e)
	return ret

# Generic n-dimensional path.
def get_path(n, sizes, r):
	if n <= 1 or len(sizes) != n or len(r) != n:
		print("Invalid sizes or starting point:", n, sizes, r)
		return

	path = [r]
	p = r
	d = [1] * n
	steps = 1
	while steps < 2*lcm_list(sizes):
		p = [p[i] + d[i] for i in range(n)]
		path.append(p)
		steps = steps+1
		d = [d[i] if p[i] % sizes[i] != 0 else -d[i] for i in range(n)]
	return path

def is_double(path):
	# A path is double if and only at some point the ball bounces on a
	# corner and bounces back in the opposite direction. This happens if
	# and only if for some i we have path[i] = path[i+2]
	for i in range(0, len(path)-2):
		if path[i] == path[i+2]:
			return True

	return False

def get_multiplicities(n, sizes, r):
	d = dict()
	path = [tuple(x) for x in get_path(n, sizes, r)]

	for point in path:
		if point in d:
			d[point] += 1
		else:
			d[point] = 1

	if is_double(path):
		for p in d:
			d[p] //= 2

	return d

def print_multiplicities(n, sizes, r):
	d = get_multiplicities(n, sizes, r)

	print("")
	print("Points with multiplicity > 1:")
	print("")

	for i in range(2, max(d.values())+1):
		L = []
		for point in d:
			if d[point] == i:
				L.append(point)

		if len(L) != 0:
			print(len(L), "point of multiplicity", i)
			print(L)
			print("")


###############################################################################
# This part is specific for 2d drawings
###############################################################################
class Transformation:
	def __init__(self, angle=0.0, mirror=False, shift=(0,0)):
		self.angle = angle
		self.mirror = mirror
		self.shift = shift

	def rotate(self, point):
		c, s = cos(self.angle), sin(self.angle)
		return [c*point[0] - s*point[1], s*point[0] + c*point[1]]

	def reflect(self, point):
		return [point[0], -point[1] if self.mirror else point[1]]
		
	def translate(self, point):
		return [point[i] + self.shift[i] for i in range(2)]

	def apply_to(self, point):
		return self.translate(self.rotate(self.reflect(point)))

def draw_line_2d(p1, p2, c="black", w=1):
	plt.plot([p1[0], p2[0]], [p1[1], p2[1]], color=c, linewidth=w)
		
def draw_grid_and_rectangle(sizes, t):
	for i in range(0, sizes[0]+1):
		p1 = t.apply_to([i,0])
		p2 = t.apply_to([i,sizes[1]])
		color, width = ("red", 1) if i % sizes[0] == 0 else ("grey", 0.5)
		draw_line_2d(p1, p2, c=color, w=width)
	for i in range(0, sizes[1]+1):
		p1 = t.apply_to([0,i])
		p2 = t.apply_to([sizes[0],i])
		color, width = ("red", 1) if i % sizes[1] == 0 else ("grey", 0.5)
		draw_line_2d(p1, p2, c=color, w=width)

def draw_path_2d(sizes, r, transformation):
	if len(sizes) != 2:
		print("Cannot draw non-2d path")
		return

	plt.axis("off")
	plt.axis("equal")
	draw_grid_and_rectangle(sizes, transformation)

	path = [transformation.apply_to(p) for p in get_path(2, sizes, r)]
	plt.plot([p[0] for p in path], [p[1] for p in path], color="blue")

###############################################################################
# This part is specific for 3d billiards
###############################################################################
class Face:
	def __init__(self, fixed_coordinate, value, transformation):
		self.f = fixed_coordinate
		self.v = value
		self.t = transformation

	def contains(self, point):
		return point[self.f] == self.v

	def proj(self, point):
		return [point[i] for i in range(3) if i != self.f]

def draw_bouncing_points_3d2d(sizes, r, face):
	path_3d = get_path(3, sizes, r)
	bp = [face.t.apply_to(face.proj(p))
	      for p in path_3d if is_bouncing(3, sizes, p) and face.contains(p)]

	plt.scatter([p[0] for p in bp], [p[1] for p in bp], color="green")

def draw_3d_projections(sizes, r):
	a, b, c = sizes

	bottom = Face(2, 0, Transformation())
	top    = Face(2, c, Transformation(shift=(a+c, -(b+c))))
	front  = Face(1, 0, Transformation(mirror=True))
	back   = Face(1, b, Transformation(shift=(0,b)))
	left   = Face(0, 0, Transformation(angle=pi/2))
	right  = Face(0, a, Transformation(angle=pi/2, mirror=True, shift=(a,0)))

	for face in [bottom, top, front, back, left, right]:
		draw_path_2d(face.proj(sizes), face.proj(r), face.t)
		draw_bouncing_points_3d2d(sizes, r, face)
	plt.show()

def draw_line_3d(ax, p1, p2, c="black", w=1):
	ax.plot([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]], color=c, lw=w)

def draw_box_3d(ax, s):
	color, width = ("red", 1)

	draw_line_3d(ax, (   0,    0,    0), (s[0],    0,    0), color, width)
	draw_line_3d(ax, (   0, s[1],    0), (s[0], s[1],    0), color, width)
	draw_line_3d(ax, (   0,    0, s[2]), (s[0],    0, s[2]), color, width)
	draw_line_3d(ax, (   0, s[1], s[2]), (s[0], s[1], s[2]), color, width)

	draw_line_3d(ax, (   0,    0,    0), (   0, s[1],    0), color, width)
	draw_line_3d(ax, (s[0],    0,    0), (s[0], s[1],    0), color, width)
	draw_line_3d(ax, (   0,    0, s[2]), (   0, s[1], s[2]), color, width)
	draw_line_3d(ax, (s[0],    0, s[2]), (s[0], s[1], s[2]), color, width)

	draw_line_3d(ax, (   0,    0,    0), (   0,    0, s[2]), color, width)
	draw_line_3d(ax, (s[0],    0,    0), (s[0],    0, s[2]), color, width)
	draw_line_3d(ax, (   0, s[1],    0), (   0, s[1], s[2]), color, width)
	draw_line_3d(ax, (s[0], s[1],    0), (s[0], s[1], s[2]), color, width)

def draw_3d_picture(sizes, r):
	ax = plt.figure().add_subplot(111, projection="3d")

	plt.axis("off")
	ax.set_xlim(0, max(sizes))
	ax.set_ylim(0, max(sizes))
	ax.set_zlim(0, max(sizes))
	
	draw_box_3d(ax, sizes)

	path = get_path(3, sizes, r)
	plt.plot([p[0] for p in path], [p[1] for p in path], [p[2] for p in path],
	         color="blue")

	plt.show()

def edge_number(c1, c2):
	a = 0 if c1 == 0 else 1
	b = 0 if c2 == 0 else 1
	return a + 2*b

def print_points_on_edges_coord(s, path, i):
	L = [[], [], [], []]
	Lname = [['*','*','*'],['*','*','*'],['*','*','*'],['*','*','*']]
	# Kinda ugly way of saying "j and k are the other 2 coordinates"
	j = 0 if i != 0 else 1
	k = 2 if i != 2 else 1
	for p in path:
		if (p[j] == 0 or p[j] == s[j]) and (p[k] == 0 or p[k] == s[k]):
			en = edge_number(p[j], p[k])
			L[en].append(p[i])
			Lname[en][j] = p[j]
			Lname[en][k] = p[k]

	for l in range(0,4):
		if len(L[l]) != 0:
			so = list(set(L[l]))
			so.sort()
			print(len(so), "points on edge", Lname[l], ":", so)
	

def print_points_on_edges(size, r):
	# TODO: show a picture of this

	print("")

	path = get_path(3, sizes, r)
	for i in range(0,3):
		print_points_on_edges_coord(sizes, path, i)
		print("")

###############################################################################
# Billiard data / user input
###############################################################################
def user_input():
	a = int(input("Value for a: "))
	b = int(input("Value for b: "))
	c = int(input("Value for c: "))
	ra = int(input("a-coordinate of r: "))
	rb = int(input("b-coordinate of r: "))
	rc = int(input("c-coordinate of r: "))
	pic = input("Choose p for projections or 3 for 3d (empty = all, one after the other): ")
	return [a,b,c], [ra,rb,rc], pic

###############################################################################
# Main routine below
###############################################################################

if __name__ == '__main__':
	# You can choose to write your input here or to get it interactively
	#sizes, r, pic = [15, 9, 7], [2, 0, 0], "p"
	#sizes, r, pic = [2, 3, 4], [0, 0, 0], "3"
	sizes, r, pic = user_input()

	print("---------------------------------")
	print_multiplicities(len(sizes), sizes, r)
	print("---------------------------------")
	print_points_on_edges(sizes, r)
	print("---------------------------------")

	if pic == "p":
		draw_3d_projections(sizes, r)
	elif pic == "3":
		draw_3d_picture(sizes, r)
	else:
		draw_3d_projections(sizes, r)
		draw_3d_picture(sizes, r)
