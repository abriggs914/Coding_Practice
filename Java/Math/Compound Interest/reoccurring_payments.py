
t = 6
n = 5
N = (max(1, t - 1) * n) + ((t + 1) % n)
pmt = 3000
r = 36.9
initial = pmt
total = initial
print("N: " + str(N) + ", n: " + str(n))

def sentence(val) :
	s = "An initial investment of ${s} and re-occurring payments of ${pmt}, compounding ".format(s=initial, pmt=pmt)
	if n == 1 :
		s += "annually"
	elif n == 2 :
		s += "semi-annually"
	elif n == 4 :
		s += "quarterly"
	elif n == 12 :
		s += "monthly"
	elif n == 0.5 :
		s += "bi-annually"
	else:
		if n > 0 :
			"{n} times per year".format(n=n)
		else:
			inverseN = 1.0 / n
			s += "once every {n} years".format(n=inverseN)
	s += " for {t} year".format(t=t) + ("s" if t not in [0, 1] else "")
	s += " at an interest rate of {r}%".format(r=r)
	return s + " will mature to be $ %.2f" % val

for i in range(N) :
	total *= (1 + ((r /100) / n))
	if N > n :
		total += pmt
	print("i: " + str(i+1).ljust(5) + " total: " + str(total))
	
print("\n\n" + sentence(total))