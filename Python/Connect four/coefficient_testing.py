from statistics import *
from collections import Counter
from time import time


BORDER = "".join(["#" for i in range(120)])

rows = range(4, 51, 2)
cols = range(4, 51, 2)
connect_x = 4
coefficient = 0.00
coefficient_change = 0.05

WRITE = True
PRINT = False


class StatPoint:

	def __init__(self, coefficient):
		self.coefficient = coefficient
		self.fxs = []
		self.min_val = float("inf")
		self.min_stats = None
		self.max_val = float("-inf")
		self.max_stats = None
		self.stats = None
		self.count = 0
		
	def update_stats_dict(self):
		fxs = self.fxs
		self.stats = {
			"fxs_mean": mean(fxs),
			"fxs_median": median(fxs),
			"fxs_harmonic_mean": harmonic_mean(fxs),
			"fxs_median_low": median_low(fxs),
			"fxs_median_high": median_high(fxs),
			"fxs_pstdev": pstdev(fxs),
			"fxs_stdev": stdev(fxs),
			"fxs_pvariance": pvariance(fxs),
			"fxs_variance": variance(fxs),
			"fxs_mode": mode(fxs)
		}
		
	def update_count(self):
		self.count += 1
	
	def update_min_max(self, r, c, m, fx):
		self.fxs.append(fx)
		if fx > self.max_val:
			self.max_val = fx
			self.max_stats = (r, c, m)
		if fx < self.min_val:
			self.min_val = fx
			self.min_stats = (r, c, m)

# This produces a linear relationship between the leftover space and the coefficient.
# def f(r, c, m, coefficient, connect_x):
	# return round(max(connect_x, (((r*c) - m) / 2) * (1 - coefficient)))
	
# less linear... Produces outputs much too large (4 - 5,640,625) at the beginning of the game
def f(r, c, m, coefficient, connect_x):
	return round(max(connect_x, (coefficient * ((r*c) - m))**2))

def mode(lst):
	c = Counter(lst)
	return c.most_common(round(len(lst) * 0.1))
	
def number_format(value):
	if type(value) is tuple or type(value) is list:
		result = []
		for val in value: 
			if type(val) is tuple or type(val) is list:
				v_list = []
				for v in val:
					v_list.append(f'{v:,}')
				v_string = v_list
			else:
				v_string = f'{val:,}'
			result.append(v_string)
	elif type(value) is str:
		result = value
	else:
		result = f'{value:,}'
	return result

def calc_coefficients():
	global coefficient
	coefficients = []
	while coefficient <= 1:
		coefficients.append(StatPoint(coefficient))
		coefficient += coefficient_change
	return coefficients


def main():
	# prevents the file from being overwritten if the WRITE keyword is false
	if not WRITE:
		code = 'r'
	else:
		code = 'w'

	# Write to the file
	file_name = "coefficient_testing_output.txt"
	with open(file_name, code) as output_file:

		start_time = time()
		coefficients = calc_coefficients()

		for r in rows:
			for c in cols:
				moves = range(0, r*c)
				for m in moves:
					for coefficient in coefficients:
						coefficient.update_count()
						fx = f(r, c, m, coefficient.coefficient, connect_x)
						coefficient.update_min_max(r, c, m, fx)
						# if PRINT:
							# print("r: {0}, c: {1}, m: {2}: f: {3}".format(r, c, m, fx))		
			
		for coefficient in coefficients:
			coefficient_start_time = time()
			coefficient.update_stats_dict()
			
			coefficient_line = "\n{0}\n\n\t\tUsing coefficient: {1}\n\n".format(BORDER, coefficient.coefficient)
			if WRITE:
				output_file.write(coefficient_line)
			if PRINT:
				print(coefficient_line)
			
			min_val = number_format(coefficient.min_val)
			min_stats = number_format(coefficient.min_stats)
			max_val = number_format(coefficient.max_val)
			max_stats = number_format(coefficient.max_stats)
			count = number_format(coefficient.count)
			min_max_line = "count: {0}\n\tmin_val: {1}\nr: {2}\nc: {3}\nm: {4}\n\tmax_val: {5}\nr: {6}\nc: {7}\nm: {8}".format(count, min_val, *min_stats,  max_val, *max_stats)
			if WRITE:
				output_file.write(min_max_line + "\n")
			if PRINT:
				print(min_max_line)
			
			
			# Print the statistics
			rjustification = max([len(k + ":") for k in coefficient.stats.keys()])

			for k, v in coefficient.stats.items():
				title = (k + ":").ljust(rjustification, " ")
				val = number_format(v)
				stats_line = "{0} {1}".format(title, val)
				if WRITE:
					output_file.write(stats_line + "\n")
				if PRINT:
					print(stats_line)
				
			how_long = time() - coefficient_start_time
			print("Coefficient:\t{0}\t\tresults after:\t{1} m, {2} s".format(number_format(coefficient.coefficient), *number_format(divmod(how_long, 60))))
			
		end_time = time()
		how_long = end_time - start_time
		print("\n\nAll results in {0} m, {1} s".format(*number_format(divmod(how_long, 60))))
		
if __name__ == "__main__": main()