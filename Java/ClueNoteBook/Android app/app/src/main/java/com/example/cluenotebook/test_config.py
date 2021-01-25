N_P = 6
N_W = 9
N_R = 9

C = N_P * N_W * N_R
inB = lambda l, v, h : max(l, min(h, v))
pL = lambda x: (N_P - x) / N_P
wL = lambda x: (N_W - x) / N_W
rL = lambda x: (N_R - x) / N_R
config = lambda a, b, c : round(pL(a) * wL(b) * rL(c) * C)
config3 = lambda a, b, c: str(config(inB(0, a+1, N_P),b,c)) + "\n" + str(config(a,inB(0, b+1, N_W),c)) + "\n" + str(config(a, b, inB(0, c+1, N_R)))

def best_choices():
	def helper(a, b, c):
		print("a: " + str(a) + ", b: " + str(b) + ", c: " + str(c) + " ==> " + str(config(a, b, c)))
		if a == N_P or b == N_W or c == N_R:
			return a, b, c;
		c1 = config(a + 1, b, c)
		c2 = config(a, b + 1, c)
		c3 = config(a, b, c + 1)
		# print(config3(a, b, c))
		l = [c1, c2, c3]
		l = [v for v in l if v > 0]
		if not l:
			return a, b, c
		if min(l) == c1 and a != N_P - 1:
			return helper(a + 1, b, c)
		elif min(l) == c2 and b != N_W - 1:
			return helper(a, b + 1, c)
		elif min(l) == c3 and c != N_R - 1:
			return helper(a, b, c + 1)
		else:
			return a, b, c
	return helper(0, 0, 0)

# with open("output.txt", "w") as f:
	# f.write("p, w, r, config,\n")
	# for p in range(N_P - 1, -1, -1):
		# for w in range(N_W - 1, -1, -1) :
			# for r in range(N_R - 1, -1, -1) :
				# m = str(p) + ", " + str(w) + ", " + str(r) + ", " + str(config(p, w, r))
				# if (p > 0 or w > 0 or r > 0) :
					# m += ","
				# f.write(m + "\n")
print(config3(0,0,0))
print(best_choices())