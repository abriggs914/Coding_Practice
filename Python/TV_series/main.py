import random
from statistics import mean, median, mode, pstdev, pvariance, stdev, variance
from tv_series import TVSeries


the_office = TVSeries("The Office", {
    1 : 6,
    2 : 22,
    3 : 25,
    4 : 19,
    5 : 28,
    6 : 26,
    7 : 26,
    8 : 24,
    9 : 25},
    22,
    2005,
    2012,
    False,
    "Comedy",
    "Netflix")

community = TVSeries("Community", {
    1 : 25,
    2 : 24,
    3 : 22,
    4 : 13,
    5 : 13,
    6 : 13},
    22,
    2009,
    2015,
    False,
    "Comedy",
    "Amazon Prime")

game_of_thrones = TVSeries("Game of Thrones", {
    1 : 10,
    2 : 10,
    3 : 10,
    4 : 10,
    5 : 10,
    6 : 10,
    7 : 7,
    8 : 6},
    50,
    2011,
    2019,
    False,
    "Drama, Adventure",
    "Crave -> HBO")

final_space = TVSeries("Final Space", {
    1 : 10,
    2 : 13},
    22,
    2018,
    2020,
    True,
    "Comedy, Sci-fi",
    "Netflix")

parks_and_rec = TVSeries("Parks and Recreation", {
    1 : 6,
    2 : 24,
    3 : 16,
    4 : 22,
    5 : 22,
    6 : 22,
    7 : 13},
    22,
    2009,
    2015,
    False,
    "Comedy",
    "Prime TV")

silicon_valley = TVSeries("Silicon Valley", {
    1 : 8,
    2 : 10,
    3 : 10,
    4 : 10,
    5 : 8,
    6 : 7},
    22,
    2014,
    2019,
    False,
    "Comedy",
    "Crave -> HBO")

brooklyn_9_9 = TVSeries("Brooklyn Nine-Nine", {
    1 : 22,
    2 : 23,
    3 : 23,
    4 : 22,
    5 : 22,
    6 : 18,
    7 : 13},
    22,
    2013,
    2020,
    True,
    "Comedy",
    "Netflix")

workaholics = TVSeries("Workaholics", {
    1 : 10,
    2 : 10,
    3 : 20,
    4 : 13,
    5 : 13,
    6 : 10,
    7 : 10},
    22,
    2011,
    2017,
    False,
    "Comedy",
    "Crave")
    
trailer_park_boys = TVSeries("Trailer Park Boys", {
    1 : 6,
    2 : 7,
    3 : 8,
    4 : 8,
    5 : 10,
    6 : 6,
    7 : 10,
    8 : 10,
    9 : 10,
    10 : 10,
    11 : 10,
    12 : 10},
    22,
    2001,
    2018,
    False,
    "Comedy",
    "Netflix")
    
arrested_development = TVSeries("Arrested Develpoment", {
    1 : 22,
    2 : 18,
    3 : 13,
    4 : 15,
    5 : 16},
    22,
    2003,
    2019,
    False,
    "Comedy",
    "Netflix")
    
chernobyl = TVSeries("Chernobyl", {
    1 : 5},
    60,
    2019,
    2019,
    False,
    "Drama, Documentary",
    "Crave -> HBO")

breaking_bad = TVSeries("Breaking Bad",{
    1 : 7,
    2 : 13,
    3 : 13,
    4 : 13,
    5 : 16},
    50,
    2008,
    2013,
    False,
    "Drama, Thriller",
    "Netflix")
    
black_mirror = TVSeries("Black Mirror", {
    1 : 3,
    2 : 3,
    3 : 6,
    4 : 6,
    5 : 3},
    60,
    2011,
    2019,
    False,
    "Drama, Sci-fi",
    "Netflix")
    
better_call_saul = TVSeries("Better Call Saul", {
    1 : 10,
    2 : 10,
    3 : 10,
    4 : 10,
    5 : 10},
    50,
    2015,
    2020,
    True,
    "Drama, Law",
    "Netflix")
    
the_it_crowd = TVSeries("The IT Crowd", {
    1 : 6,
    2 : 6,
    3 : 6,
    4 : 7},
    22,
    2006,
    2013,
    False,
    "Comedy, Tech",
    "Netflix")
    
avatar_last_airbender = TVSeries("Avatar, the Last Airbender", {
    1 : 20,
    2 : 20,
    3 : 21},
    22,
    2005,
    2008,
    False,
    "Drama, Adventure",
    "Netflix")
    
peaky_blinders = TVSeries("Peaky Blinders", {
    1 : 6,
    2 : 6,
    3 : 6,
    4 : 6,
    5 : 6},
    50,
    2013,
    2020,
    True,
    "Drama, Period",
    "Netflix")
    
curb_your_enthusiasm = TVSeries("Curb your Enthusiasm", {
    1 : 10,
    2 : 10,
    3 : 10,
    4 : 10,
    5 : 10,
    6 : 10,
    7 : 10,
    8 : 10,
    9 : 10,
    10 : 10},
    30,
    2000,
    2020,
    True,
    "Comedy",
    "Crave -> HBO")
    
letterkenny = TVSeries("Letterkenny", {
    1 : 6,
    2 : 6,
    3 : 6,
    4 : 6,
    5 : 6,
    6 : 6,
    7 : 6,
    8 : 7,
	9 : 7},
    22,
    2016,
    2021,
    True,
    "Comedy",
    "Crave")
	
prison_break = TVSeries("Prison Break", {
    1 : 22,
	2 : 22,
	3 : 13,
	4 : 24,
	5 : 9},
	42,
	2005,
	2017,
	False,
	"Drama, Thriller",
	"Netflix")
	
scrubs = TVSeries("Scrubs", {
	1 : 24,
	2 : 22,
	3 : 22,
	4 : 25,
	5 : 24,
	6 : 22,
	7 : 11,
	8 : 19,
	9 : 13},
	22,
	2001,
	2010,
	False,
	"Comedy",
	"Prime TV")
	
yugioh = TVSeries("Yu-Gi-Oh!", {
	1 : 49,
	2 : 48,
	3 : 47,
	4 : 40,
	5 : 52},
	22,
	1998,
	2006,
	False,
	"Anime",
	"Prime TV")
	
misfits = TVSeries("Misfits", {
	1 : 6,
	2 : 7,
	3 : 8,
	4 : 8,
	5 : 8},
	44,
	2009,
	2013,
	False,
	"Comedy",
	"Netflix")

the_mandalorian = TVSeries("The Mandalorian", {
    1 : 8,
    2 : 8},
    44,
    2019,
    2021,
    True,
    "Drama, Action",
    "Disney+")

recess = TVSeries("Recess", {
    1 : 13,
    2 : 13,
	3 : 8,
	4 : 23,
	5 : 5,
	6 : 6},
    23,
    1997,
    2001,
    False,
    "Comedy, Cartoon",
    "Disney+")

the_proud_family = TVSeries("The Proud Family", {
    1 : 21,
    2 : 31},
    23,
    2001,
    2005,
    False,
    "Comedy, Cartoon",
    "Disney+")
	
my_name_is_earl = TVSeries("My Name is Earl", {
    1 : 24,
    2 : 23,
	3 : 22,
	4 : 27},
    21,
    2005,
    2009,
    False,
    "Comedy",
    "Disney+")
	
futurama = TVSeries("Futurama", {
	1 : 9,
	2 : 20,
	3 : 15,
	4 : 12,
	5 : 16,
	6 : 16,
	7 : 13,
	8 : 13,
	9 : 13,
	10 : 13},
	22,
	1999,
	2013,
	False,
	"Comedy",
	"Disney+")
	
family_guy = TVSeries("Family Guy", {
	1 : 7,
	2 : 21,
	3 : 22,
	4 : 30,
	5 : 18,
	6 : 12,
	7 : 16,
	8 : 21,
	9 : 18,
	10 : 23,
	11 : 22,
	12 : 21,
	13 : 18,
	14 : 20,
	15 : 20,
	16 : 20,
	17 : 20,
	18 : 20,
	19 : 20},
	22,
	1999,
	2021,
	True,
	"Comedy",
	"Disney+")
	
	
its_always_sunny_in_philadelphia = TVSeries("It's Always Sunny in Philadelphia", {
	1 : 7,
	2 : 10,
	3 : 15,
	4 : 13,
	5 : 12,
	6 : 14,
	7 : 13,
	8 : 10,
	9 : 10,
	10 : 10,
	11 : 10,
	12 : 10,
	13 : 10,
	14 : 10},
	22,
	2005,
	2019,
	False,
	"Comedy",
	"Disney+")
	

the_last_man_on_earth = TVSeries("The Last Man on Earth", {
	1 : 13,
	2 : 18,
	3 : 18,
	4 : 18},
	22,
	2015,
	2018,
	False,
	"Comedy",
	"Disney+")
	

the_mick = TVSeries("The Mick", {
	1 : 17,
	2 : 20},
	22,
	2017,
	2018,
	False,
	"Comedy",
	"Disney+")
	

brickleberry = TVSeries("Brickleberry", {
	1 : 10,
	2 : 13,
	3 : 13},
	22,
	2012,
	2015,
	False,
	"Comedy",
	"Disney+")
	
the_simpsons = TVSeries("The Simpsons", {
	1: 13,
	2: 22,
	3: 24,
	4: 22,
	5: 22,
	6: 25,
	7: 25,
	8: 25,
	9: 25,
	10: 23,
	11: 22,
	12: 21,
	13: 22,
	14: 22,
	15: 22,
	16: 21,
	17: 22,
	18: 22,
	19: 20,
	20: 21,
	21: 23,
	22: 22,
	23: 22,
	24: 22,
	25: 22,
	26: 22,
	27: 22,
	28: 22,
	29: 21,
	30: 23,
	31: 22,
	32: 22},
	24,
	1989,
	2021,
	True,
	"Comedy",
	"Disney+")
	

solar_opposites = TVSeries("Solar Opposites", {
	1 : 8,
	2 : 9},
	24,
	2020,
	2021,
	True,
	"Comedy",
	"Disney+")
	

the_orville = TVSeries("The Orville", {
	1 : 12,
	2 : 14,
	3 : 11},
	44,
	2017,
	2022,
	True,
	"Comedy",
	"Disney+")
	

mr_robot = TVSeries("Mr. Robot", {
	1 : 10,
	2 : 12,
	3 : 10,
	4 : 13},
	65,
	2015,
	2019,
	False,
	"Drama / Thriller",
	"Prime TV")
	
	
criminal_minds = TVSeries("Criminal Minds", {
	1: 22,
	2: 23,
	3: 20,
	4: 26,
	5: 23,
	6: 24,
	7: 24,
	8: 24,
	9: 24,
	10: 23,
	11: 22,
	12: 22,
	13: 22,
	14: 15,
	15: 10},
	44,
	2005,
	2020,
	True,
	"Thriller / Drama",
	"Disney+")
	

baskets = TVSeries("Baskets", {
	1 : 10,
	2 : 10,
	3 : 10,
	4 : 10},
	22,
	2016,
	2019,
	False,
	"Comedy",
	"Disney+")
	
	
sherlock = TVSeries("Sherlock", {
	1 : 3,
	2 : 3,
	3 : 3,
	4 : 4},
	90,
	2010,
	2017,
	False,
	"Mystery / Crime / Drama",
	"Prime TV")
	

series_list = [
    the_office,
    community,
    game_of_thrones,
    final_space,
    parks_and_rec,
    silicon_valley,
    brooklyn_9_9,
    workaholics,
    trailer_park_boys,
    arrested_development,
    chernobyl,
    breaking_bad,
    black_mirror,
    better_call_saul,
    the_it_crowd,
    avatar_last_airbender,
    peaky_blinders,
    curb_your_enthusiasm,
    letterkenny,
	prison_break,
	scrubs,
	yugioh,
	misfits,
	the_mandalorian,
	recess,
	the_proud_family,
	my_name_is_earl,
	futurama,
	family_guy,
	its_always_sunny_in_philadelphia,
	the_last_man_on_earth,
	the_mick,
	brickleberry,
	the_simpsons,
	solar_opposites,
	the_orville,
	mr_robot,
	criminal_minds,
	baskets,
	sherlock
]
   
def longest_series_title(series_list) :
    num = 0
    for series in series_list :
        name = series.name
        if len(name) > num :
            num = len(name)
    return num
    
metric_possibilities = [
    "start year",
    "end year",
    "shortest series run length",
    "longest series run length",
    "least number seasons",
    "most number seasons",
    "least number episodes",
    "most number episodes",
    "shortest time",
    "longest time",
	"most episodes per season",
	"least episodes per season"
    ]
    
def ask_print_style(series_list) :
    question = "\n\tHow would you like to print the stats?\n"
    for i in range(len(metric_possibilities)) :
        question += str(i + 1) + "\t-\tBy " + metric_possibilities[i] + "\n" 
        
    selection = input(question + "\n")
    metric = None
    if (len(selection) == 0 or len(selection) > 2) :
        print("\nNo sorting performed\n")
        return metric
    try :
        selection = int(selection)
    except :
        print("\nNo sorting performed\n")
        return metric
    
    if selection == 1 :
        print("\nsorting by start year...\n")
        metric = (False, lambda s : s.start_year, metric_possibilities[0])
    elif selection == 2 :
        print("\nsorting by end year...\n")
        metric = (False, lambda s : s.end_year, metric_possibilities[1])
    elif selection == 3 :
        print("\nsorting by shortest series length...\n")
        metric = (False, lambda s : s.calc_series_run(), metric_possibilities[2])
    elif selection == 4 :
        print("\nsorting by longest series length...\n")
        metric = (True, lambda s : s.calc_series_run(), metric_possibilities[3])
    elif selection == 5 :
        print("\nsorting by least number of seasons...\n")
        metric = (False, lambda s : s.number_seasons(), metric_possibilities[4])
    elif selection == 6 :
        print("\nsorting by most number of seasons...\n")
        metric = (True, lambda s : s.number_seasons(), metric_possibilities[5])
    elif selection == 7 :
        print("\nsorting by least number of episodes...\n")
        metric = (False, lambda s : s.count_episodes(), metric_possibilities[6])
    elif selection == 8 :
        print("\nsorting by most number of episodes...\n")
        metric = (True, lambda s : s.count_episodes(), metric_possibilities[7])
    elif selection == 9 :
        print("\nsorting by shortest time...\n")
        metric = (False, lambda s : s.how_long_is_series()[1], metric_possibilities[8])
    elif selection == 10 :
        print("\nsorting by longest time...\n")
        metric = (True, lambda s : s.how_long_is_series()[1], metric_possibilities[9])
    elif selection == 11 :
        print("\nsorting by most episodes per season...\n")
        metric = (True, lambda s : s.calc_episode_per_season(), metric_possibilities[10])
    elif selection == 12 :
        print("\nsorting by least episodes per season...\n")
        metric = (False, lambda s : s.calc_episode_per_season(), metric_possibilities[11])
    else :
        print("\nNo sorting performed\n")
    
    return metric
        
def print_time_line_horizontal(series_list, start_year, end_year) :
    metric = ask_print_style(series_list)
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
	
def print_series_stats(series_list) :
    metric = ask_print_style(series_list)
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

if __name__ == "__main__" :
  for series in series_list :
    print(series)
    
  selected_series = random.choice(series_list)
  print("\n\n\tWhat to watch?\n")
  print("Series:\n" + str(selected_series))
  selected_season = random.choice([seasonKey for seasonKey in selected_series.episodes_list.keys()])
  print("\nSeason: " + str(selected_season))
  selected_episode = random.choice([i for i in range(1, selected_series.episodes_list[selected_season] + 1)])
  print("Episode: " + str(selected_episode))
    
    
  for i in range(len(metric_possibilities)) :
    print(print_time_line_horizontal(series_list, 1988, 2022))
    print(print_series_stats(series_list))