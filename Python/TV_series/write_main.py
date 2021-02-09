import random
from statistics import mean, median, mode, pstdev, pvariance, stdev, variance
from tv_series import TVSeries
from main import *


# Run this file to update output.txt.


def write_file():
	file_name = "output.txt"
	with open(file_name, "w") as f:
        
		def print_time_line_horizontal_write(series_list, start_year, end_year) :
			metric = ask_print_style_write(series_list)
			metric_val = ""
			if metric :
				rev_val = metric[0]
				sort_metric = metric[1]
				metric_val = metric[2]
				series_list.sort(reverse=rev_val, key=sort_metric)
				
			longest_title_len = longest_series_title(series_list) + len("\t")
			space_border = "".join(["#" for i in range(longest_title_len)])
			
			year_border = space_border
			year_border += "| " + metric_val + " " if metric else "" 
			year_border += "|" + "|".join([str(i) for i in range(start_year, end_year + 1)]) + "|"
			year_border += " " + metric_val + " |" if metric else "" 
			year_border += space_border
			
			top_border = "".join(["#" for i in range(len(year_border))])
			res = top_border + "\n" + year_border + "\n"
			
			for series in series_list :
				res += "|" + "{0:{1}}".format(series.name, longest_title_len - 1)
				if metric :
					value = sort_metric(series)
					int_val = int(value)
					float_val = float(value)
					# print("value BEFORE: " + str(value) + ", int_val: " + str(int_val) + ", float_val: " + str(float_val))
					if int_val != float_val :
						value = "{0:^{1}f}".format(sort_metric(series), len(metric_val))
					else :
						value = str(value)
					# print("after AFTER: " + str(value))
					# else :
					res += "|{0:^{1}s}".format(value, (len(metric_val) + 2))
				for year in range(start_year, end_year + 1) :
					res += "|"
					if series.start_year <= year and year <= series.end_year :
						res += "".join(["*" for i in range(len(str(year)))])
					else :
						res += "".join([" " for i in range(len(str(year)))])
				if metric :
					value = sort_metric(series)
					int_val = int(value)
					float_val = float(value)
					# print("value BEFORE: " + str(value) + ", int_val: " + str(int_val) + ", float_val: " + str(float_val))
					if int_val != float_val :
						value = "{0:^{1}f}".format(sort_metric(series), len(metric_val))
					else :
						value = str(value)
					# print("after AFTER: " + str(value))
					# else :
					res += "|{0:^{1}s}".format(value, (len(metric_val) + 2))
				res += "|" + "{0:{1}}".format(series.name, longest_title_len - 1) + "|\n"
			res += top_border
			return res
			
		def print_series_stats_write(series_list) :
			metric = ask_print_style_write(series_list)
			metric_val = ""
			if metric :
				rev_val = metric[0]
				sort_metric = metric[1]
				metric_val = metric[2]
				series_list.sort(reverse=rev_val, key=sort_metric)
				
			longest_title_len = longest_series_title(series_list) + len("\t")
			top_border = "".join(["#" for i in range(longest_title_len + len(metric_val) + 4)])
			space_border = "".join(["#" for i in range(longest_title_len)])
			res = top_border + "\n"
			res += space_border + "| " + metric_val + " |\n"
			
			for series in series_list :
				res += "|" + "{0:{1}}".format(series.name, longest_title_len - 1)
				if metric :
					value = sort_metric(series)
					int_val = int(value)
					float_val = float(value)
					# print("value BEFORE: " + str(value) + ", int_val: " + str(int_val) + ", float_val: " + str(float_val))
					if int_val != float_val :
						value = "{0:^{1}f}".format(sort_metric(series), len(metric_val))
					else :
						value = str(value)
					# print("after AFTER: " + str(value))
					# else :
					res += "|{0:^{1}s}".format(value, (len(metric_val) + 2))
				else :
					res += "|{0:^{1}s}".format("-", (len(metric_val) + 2))
				res += "|\n"
			res += top_border
			if metric :
			# median', 'median_grouped', 'median_high', 'median_low', 'mode', 'numbers', 'pstdev', 'pvariance', 'stdev', 'variance'
			  stats_list = [sort_metric(series) for series in series_list]
			  res += "\n\nMean:\t\t" + "{0:6.2f}".format(mean(stats_list))
			  res += "\nMedian:\t\t" + "{0:6.2f}".format(median(stats_list))
			  res += "\nPstdev:\t\t" + "{0:6.2f}".format(pstdev(stats_list))
			  res += "\nPvariance:\t" + "{0:6.2f}".format(pvariance(stats_list))
			  res += "\nStdev:\t\t" + "{0:6.2f}".format(stdev(stats_list))
			  res += "\nVariance:\t" + "{0:6.2f}".format(variance(stats_list))
			return res	
	
	
		def ask_print_style_write(series_list) :
			question = "\n\tHow would you like to print the stats?\n"
			for i in range(len(metric_possibilities)) :
				question += str(i + 1) + "\t-\tBy " + metric_possibilities[i] + "\n" 
				
			selection = input(question + "\n")
			metric = None
			if (len(selection) == 0 or len(selection) > 2) :
				f.write("\nNo sorting performed\n")
				return metric
			try :
				selection = int(selection)
			except :
				f.write("\nNo sorting performed\n")
				return metric
			
			if selection == 1 :
				f.write("\nsorting by start year...\n")
				metric = (False, lambda s : s.start_year, metric_possibilities[0])
			elif selection == 2 :
				f.write("\nsorting by end year...")
				metric = (False, lambda s : s.end_year, metric_possibilities[1])
			elif selection == 3 :
				f.write("\nsorting by shortest series length...\n")
				metric = (False, lambda s : s.calc_series_run(), metric_possibilities[2])
			elif selection == 4 :
				f.write("\nsorting by longest series length...\n")
				metric = (True, lambda s : s.calc_series_run(), metric_possibilities[3])
			elif selection == 5 :
				f.write("\nsorting by least number of seasons...\n")
				metric = (False, lambda s : s.number_seasons(), metric_possibilities[4])
			elif selection == 6 :
				f.write("\nsorting by most number of seasons...\n")
				metric = (True, lambda s : s.number_seasons(), metric_possibilities[5])
			elif selection == 7 :
				f.write("\nsorting by least number of episodes...\n")
				metric = (False, lambda s : s.count_episodes(), metric_possibilities[6])
			elif selection == 8 :
				f.write("\nsorting by most number of episodes...\n")
				metric = (True, lambda s : s.count_episodes(), metric_possibilities[7])
			elif selection == 9 :
				f.write("\nsorting by shortest time...\n")
				metric = (False, lambda s : s.how_long_is_series()[1], metric_possibilities[8])
			elif selection == 10 :
				f.write("\nsorting by longest time...\n")
				metric = (True, lambda s : s.how_long_is_series()[1], metric_possibilities[9])
			else :
				f.write("\nNo sorting performed\n")
				
			return metric
	
		for series in series_list :
			f.write(str(series))
		selected_series = random.choice(series_list)
		f.write("\n\n\tWhat to watch?\n")
		f.write("Series:\n" + str(selected_series))
		selected_season = random.choice([seasonKey for seasonKey in selected_series.episodes_list.keys()])
		f.write("\nSeason: " + str(selected_season))
		selected_episode = random.choice([i for i in range(1, selected_series.episodes_list[selected_season] + 1)])
		f.write("Episode: " + str(selected_episode))
		
		
		for i in range(10) :
			f.write(print_time_line_horizontal_write(series_list, 1995, 2021))
			f.write(print_series_stats_write(series_list))
			


if __name__ == "__main__" :
	write_file()