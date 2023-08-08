import billiard3d
import sys

def get_stats(i, j, k, mult):
	for r1 in range(i+1):
		for r2 in range(j+1):
			for r3 in range(k+1):
				d = billiard3d.get_multiplicities(3, [i, j, k], [r1, r2, r3])
				for key in d:
					mult[d[key]] += 1

def print_stats(N):
	mult = [0] * 10
	for i in range(1, N+1):
		for j in range(i, N+1):
			for k in range(j, N+1):
				get_stats(i, j, k, mult)

	print("Statistics for paths with 0 < a <= b <= c <= {0}".format(N))
	print("Considering all paths starting from any possible point")
	for i in range(1, 10):
		if mult[i] != 0:
			print("Multiplicity {0}: {1} points".format(i, mult[i]))
	print("There are no points of positive multiplicity different from those listed above")

def print_stats_single(a, b, c):
	mult = [0] * 10
	get_stats(a, b, c, mult)

	print("Statistics for paths with a={0}, b={1} and c={2}".format(a, b, c))
	print("Considering all paths starting from any possible point")
	for i in range(1, 10):
		if mult[i] != 0:
			print("Multiplicity {0}: {1} points".format(i, mult[i]))
	print("There are no points of positive multiplicity different from those listed above")

if len(sys.argv) == 2:
	N = int(sys.argv[1])
	print_stats(N)
elif len(sys.argv) == 4:
	a, b, c = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
	print_stats_single(a, b, c)
else:	
	print("Use one of the following options:")
	print("\tpython multiplicity_stats.py N\t\t # For all possible sizes up to N")
	print("\tpython multiplicity_stats.py a b c\t # For all starting points for the single 3d box (a,b,c)")
