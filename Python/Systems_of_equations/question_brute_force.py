
from time import time

def check(s, d, h, o, f):
	res = True
	res &= (s + d + d + h) == 22
	res &= (d + f + o + s) == 16
	res &= (h + d + s + h) == 18
	res &= (s * d * h) == 64
	res &= (d * f * d) == 0
	res &= (d * o * s) == 96
	res &= (h * s * h) == 32
	return res
	
# Runs in O((high - low)^5), so only meant for small test regions.
def brute_force(low, high):
	low = min(low, min(high, -10))
	high = max(high, max(low, 10))
	res = []
	loop = True
	r = range(low, high)
	for s in r:
		print("s: " + str(s))
		if loop:
			for d in r:
				print("d: " + str(d))
				if loop:
					for h in r:
						print("h: " + str(h))
						if loop:
							for o in r:
								if loop:
									for f in r:
										if loop:
											if check(s, d, h, o, f):
												res.append((s, d, h, o, f))
												# loop = False
										# if not loop:
											# break
								# else:
									# break
						# else:
							# break
				# else:
					# break
		# else:
			# break
	return res

start_time = time()
	
low = -10
high = 10

low = 0
high = 8

print("checking...")
solns = brute_force(low, high)
print("\ndone!\n\n\t\t" + str(len(solns)) + " solution" + ("s" if len(solns) not in [0, 1] else "") + " found:\n")
for soln in solns:
	print("\t-\t" + str(soln))
# correct answer: (2, 8, 4, 6, 0)

end_time = time()
total_time = end_time - start_time
m, s = divmod(total_time, 60)
# mins = total_time // 60

print("\n\n\tTime:\ntotal minutes - " + str(m) + "\ntotal seconds - " + str(total_time) + "\nMM:SS - " + str(int(m)).rjust(2, "0") + ":" + str(round(s)).rjust(2, "0"))