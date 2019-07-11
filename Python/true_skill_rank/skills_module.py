import skills
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from ranking_sim import RankingSim, rank_sim_regular_season

print(dir(skills))


#Teams
#Atlantic: Boston, Buffalo, Detroit, Florida, Montreal, Ottawa, Tampa Bay, Toronto
#Metropolitan: Carolina, Columbus, New Jersey, NY Rangers, NY Islanders, Philadelphia, Pittsburgh, Washington
#Central: Chicago, Colorado, Dallas, Minnesota, Nashville, St. Louis, Winnipeg
#Pacific: Anaheim, Arizona, Calgary, Edmonton, Los Angeles, San Jose, Vancouver, Vegas

start_date = '2018-10-03' # first day of games
players_stats_file = 'players_reg_season_2018_2019.csv'
players_stats_df = pd.read_csv(players_stats_file)
#print(list(players_stats_df.columns))
teams_dict = {'Anaheim Ducks': 'ANA',
         'Arizona Coyotes': 'ARI',
         'Boston Bruins': 'BOS',
         'Buffalo Sabres': 'BUF',
         'Calgary Flames': 'CGY',
         'Carolina Hurricanes': 'CAR',
         'Chicago Blackhawks': 'CHI',
         'Colorado Avalanche': 'COL',
         'Columbus Blue Jackets': 'CBJ',
         'Dallas Stars': 'DAL',
         'Detroit Red Wings': 'DET',
         'Edmonton Oilers': 'EDM',
         'Florida Panthers': 'FLA',
         'Los Angeles Kings': 'LAK',
         'Minnesota Wild': 'MIN',
         'Montreal Canadiens': 'MTL',
         'Nashville Predators': 'NSH',
         'New Jersey Devils': 'NJD',
         'New York Islanders': 'NYI',
         'New York Rangers': 'NYR',
         'Ottawa Senators': 'OTT',
         'Philadelphia Flyers': 'PHI',
         'Pittsburgh Penguins': 'PIT',
         'San Jose Sharks': 'SJS',
         'St Louis Blues': 'STL',
         'Tampa Bay Lightning': 'TBL',
         'Toronto Maple Leafs': 'TOR',
         'Vancouver Canucks': 'VAN',
         'Vegas Golden Knights': 'VEG',
         'Washington Capitals': 'WSH',
         'Winnipeg Jets': 'WPG'}

class Player(object):

    def __init__(self, id, rank, name, age, team, \
                 position, games_played, goals, assists, \
                 points, plus_minus, penalties_in_minutes, \
                 point_share, even_strength_goals, \
                 power_play_goals, shorthanded_goals, \
                 game_winning_goals, even_strength_assists, \
                 power_play_assists, short_handed_assists, \
                 shots, shooting_percentage, time_on_ice, \
                 average_time_on_ice, blocks, hits, \
                 face_offs_won, face_offs_lost, \
                 face_offs_percentage):
        self.id = id
        self.rank = rank
        self.name = name
        self.age = age
        self.team = team
        self.pos = position
        self.gp = games_played
        self.goals = goals
        self.assists = assists
        self.pts = points
        self.p_m = plus_minus
        self.pims = penalties_in_minutes
        self.p_share = point_share
        self.evs_g = even_strength_goals
        self.pp_g = power_play_goals
        self.sh_g = shorthanded_goals
        self.gwg = game_winning_goals
        self.evs_a = even_strength_assists
        self.pp_a = power_play_assists
        self.sh_a = short_handed_assists
        self.shots = shots
        self.shot_p = shooting_percentage
        self.toi = time_on_ice
        self.atoi = average_time_on_ice
        self.blks = blocks
        self.hits = hits        
        self.fow = face_offs_won
        self.fol = goals
        self.fop = assists

    def __repr__(self):
        repr = '( ' + str(self.name) + ' , ' \
               + str(self.team) + ' , GP: ' \
               + str(self.gp) + ' , G: ' \
               + str(self.goals) + ' , A: ' \
               + str(self.assists) + ' )'
        return repr

class Team(object):

    def __init__(self, name, acronym, location, list_of_players):
        self.name = name
        self.acronym = acronym
        self.location = location
        self.list_of_players = list_of_players

    def __repr__(self):
        string_repr = '( ' + str(self.acronym) + ', ' + str(self.location) + ' )'
        return string_repr

def get_team_location(team):
    location_prefixes = ['New', 'Tampa', 'St', 'San', 'Los']
    two_name_mascots = ['Vegas', 'Columbus', 'Toronto', 'Detroit']
    # home_team = temp_dict['team_1']
    location = team.split(' ')
    if len(location) == 3:
        if location[0] == 'St.':
            print('st LOUIS')
            location = 'St Louis'
        elif location[0] in location_prefixes:
            location = location[0] + ' ' + location[1]
        elif location[0] in two_name_mascots:
            location = location[0]
    else:
        location = location[0]
    return location

def create_teams():
    teams = {}
    for team, acronym in teams_dict.items():
        teams[team] = Team(team, acronym, get_team_location(team), [])
    return teams

def create_players():
    i = 0
    players = {}
    for i in range(len(players_stats_df)):
        row = players_stats_df.iloc[i]

        rank = row['Rk']
        name = row['Player']
        id = name.split('\\')[1]
        name = name.split('\\')[0]
        age = row['Age']
        team = row['Tm']
        position = row['Pos']
        games_played = row['GP']
        goals = row['G']
        assists = row['A']
        points = row['PTS']
        plus_minus = row['+/-']
        penalties_in_minutes = row['PIM']
        point_share = row['PS']
        even_strength_goals = row['EV']
        power_play_goals = row['PP']
        shorthanded_goals = row['SH']
        game_winning_goals = row['GW']
        even_strength_assists = row['EV.1']
        power_play_assists = row['PP.1']
        short_handed_assists = row['SH.1']
        shots = row['S']
        shooting_percentage = row['S%']
        time_on_ice = row['TOI']
        average_time_on_ice = row['ATOI']
        blocks = row['BLK']
        hits = row['HIT']
        face_offs_won = row['FOW']
        face_offs_lost = row['FOL']
        face_offs_percentage = row['FO%']
        # print('name:\t' + str(name))
        p1 = Player(id, rank, name, age, team, \
                 position, games_played, goals, assists, \
                 points, plus_minus, penalties_in_minutes, \
                 point_share, even_strength_goals, \
                 power_play_goals, shorthanded_goals, \
                 game_winning_goals, even_strength_assists, \
                 power_play_assists, short_handed_assists, \
                 shots, shooting_percentage, time_on_ice, \
                 average_time_on_ice, blocks, hits, \
                 face_offs_won, face_offs_lost, \
                 face_offs_percentage)
        #print('ID:\t' + str(p1.id))
        if p1.id in players.keys():
            players[p1.id].append(p1)
        else:
            players[p1.id] = [p1]
        #print(p1)
        #players.append(p1)
    return players

# print(generate_date().__next__())
def generate_date():
    global start_date
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    #print('date:\t' + str(start_date) + ',\ttype:\t' + str(type(start_date)))
    start_date += timedelta(days=1)
    new_day = start_date.strftime('%Y-%m-%d')
    start_date = new_day
    yield start_date

today = start_date
last_day = '2019-04-07' # day after last day of games ('2019-04-06')
while today != last_day:
    if today not in rank_sim_regular_season.schedule.keys():
        print('\nDAY OFF\t' + str(today) + '\n')
    else:
        print('\n\n\ttoday:\t' + str(today) + '\n')
        todays_games = rank_sim_regular_season.schedule[today]
        for game in todays_games:
            print(game)
    today = generate_date().__next__()



#-------------------------------------------------------------------------------
        

list_of_players = create_players()
list_of_teams = create_teams()
prev_player = ''

for player_id, teams_played_for in list_of_players.items():
    total_games_played = teams_played_for[0].gp
    #for team_stats in teams_played_for:
        #print(team_stats)
    #    total_games_played += team_stats.gp

    
    #print('\tname: ' + str(teams_played_for[0].name) + ',\tTOT_GP:\t' + str(total_games_played))


    #if total_games_played == 82:
        #print('\nATTENDANCE: 100\n')
        #raise ValueError('WUT')
        #for teams_list in teams_played_for:
        #    print(teams_list)
    if len(teams_played_for) > 1:
        num_games = 2
        while num_games < len(teams_played_for):
            num_games += 1
            #print('Traded')
        

#def create_team_dict(self):
#    for player in list_of_players:
#        player_team = player.team
#        idx = list_of_players.index(prev_player)
#        if idx > 0:
#            prev_player = list_of_players[idx]
#        # player who played for at least 2 different teams
#        if prev_player == player:
#    for team, acronym in teams.items():       
#    print(player)



#for key, val in list_of_teams

        
    

#print(players_stats_df.head())

