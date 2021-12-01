from utility import *

data = [
	(4.12, '2019-03-29'),
	(9.36, '2019-04-28'),
	(4.17, '2019-05-28'),
	(5.76, '2019-06-28'),
	(5.49, '2019-07-05'),
	(3.33, '2020-09-06'),
	(1.27, '2020-09-09'),
	(9.54, '2020-09-10'),
	(6.88, '2020-09-11'),
	(4.12, '2021-11-29'),
	(9.36, '2021-11-28'),
	(4.17, '2020-11-28'),
	(5.76, '2020-10-28'),
	(5.49, '2021-11-05'),
	(3.33, '2020-11-16'),
	(1.27, '2020-11-17'),
	(9.54, '2020-11-18'),
	(6.88, '2020-11-19')
]
	

def approx_annual_medians(lst):
	s_data = lst.copy()
	s_data.sort(key=lambda t: t[1])
	years = {}
	for d in s_data:
		val, date = d
		year = int(date[:4])
		if year not in years:
			years[year] = []
		years[year].append(val)
		
	print(dict_print(years, "years"))
	
	for y in years:
		years[y].sort()
		size = len(years[y])
		odd = size % 2 == 1
		print("s: {}, o: {}, a: {}, b: {}".format(size, odd, years[y][size // 2], years[y][(size // 2) + (0 if odd else 1)]))
		years[y] = (years[y][size // 2] + years[y][(size // 2) + (0 if odd else -1)]) / 2
	
	
	return years
		
	
	

if __name__ == "__main__":
	print("approximating median of:\n\t{}\n\n:: {}".format(data, approx_annual_medians(data)))
	# print("approximating median of:\n\t{}\n\n:: {}".format(data, approx_annual_medians([])))
	# print("approximating median of:\n\t{}\n\n:: {}".format(data, approx_annual_medians([(1, '2021-11-11')])))
	# print("approximating median of:\n\t{}\n\n:: {}".format(data, approx_annual_medians([(0, '2021-10-10'),(1, '2020-11-01')])))
	# print("approximating median of:\n\t{}\n\n:: {}".format(data, approx_annual_medians([(-1, '2021-10-10'),(0, '2021-10-10'),(1, '2021-10-10')])))

	