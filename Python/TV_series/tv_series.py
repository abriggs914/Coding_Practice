# """
# TV series listings as of 
# March 18 2020
# """



class TVSeries :
    
    def __init__(self, name, episodes_list, average_length_of_episode, start_year, end_year, on_going, genre, where_to_watch) :
        self.name = name
        self.episodes_list = episodes_list
        self.average_length_of_episode = average_length_of_episode
        self.genre = genre
        self.start_year = start_year
        self.end_year = end_year
        self.on_going = on_going
        self.where_to_watch = where_to_watch
        # print("name: " + str(name) + ", episodes_list: " + str(episodes_list) + ", average_length_of_episode: " + str(average_length_of_episode))
        
    def count_episodes(self) :
        num = 0
        for season, episodes in self.episodes_list.items() :
            num += episodes
        return num
        
    def how_long_is_series(self) :
        num_epsiodes = self.count_episodes()
        total_time = num_epsiodes * self.average_length_of_episode
        return (total_time, (float(total_time) / 60))
        
    def number_seasons(self) :
        return len(self.episodes_list)
        
    def calc_episode_per_season(self) :
        return self.count_episodes() / float(self.number_seasons())
        
    def calc_series_run(self) :
        return max(1, self.end_year - self.start_year)
        
    def __repr__(self) :
        mins, hours = self.how_long_is_series()
        res = "\n\t" + str(self.name)
        res += "\nGenre:\t\t\t\t" + str(self.genre)
        res += "\nRun (" + str(self.start_year) + " -> " + str(self.end_year) + "):\t\t" + str(self.calc_series_run())
        res += (" years" if self.calc_series_run() != 1 else " year")
        res += "\nnumber seasons:\t\t\t" + str(self.number_seasons())
        res += "\nnumber episodes:\t\t" + str(self.count_episodes())
        res += "\nepisodes per season:\t\t" + str(self.calc_episode_per_season())
        res += "\naverage length of an episode:\t" + str(self.average_length_of_episode)
        res += "\nTotal minutes:\t\t\t" + str(mins)
        res += "\nTotal hours:\t\t\t" + str(hours)
        res += "\nWhere to watch:\t\t\t" + str(self.where_to_watch)
        return res