import time
import skills
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
script_execution_time = time.time()
from ranking_sim import RankingSim, rank_sim_regular_season
rank_sim_execution_time = time.time() - script_execution_time

# return string representation of dict
def print_dict(dict_in):
    res_string = ''
    if len(dict_in) == 0:
        return '\nEMPTY DICT\n'
    for key, val in dict_in.items():
        res_string += '{ ' + str(key) + ':\t' + str(val) + ' }\n'
    return res_string

# %B %m, %d -> %Y-%m-%d
def convert_date(date_in):
    date = datetime.strptime(date_in, '%B %d, %Y')
    #print('DATE PRE-ADJUSTED:\t' + str(date) +'\t=>\t' + str(date_in))
    date = datetime.strftime(date, '%Y-%m-%d')
    #print('DATE POST-ADJUSTED:\t' + str(date))
    return date

# print(generate_date().__next__())
def generate_date():
    global start_date
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    #print('date:\t' + str(start_date) + ',\ttype:\t' + str(type(start_date)))
    start_date += timedelta(days=1)
    new_day = start_date.strftime('%Y-%m-%d')
    start_date = new_day
    yield start_date


#print(dir(skills))


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
        players = self.list_of_players
        players_str = ''
        for player in players:
            players_str += str(player) + '\n'
        if players_str == '':
            players_str = 'NO PLAYERS CURRENTLY SIGNED'

        '''
        for player_id, player_obj in players.items():
            #idx = 0
            #if len(player_obj) > 3:
            idx = len(player_obj) - 1
            #else:
            #idx = len(player_obj) % 2
            #print('len(player_obj):\t' + str(len(player_obj)) + ', idx:\t' + str(idx))
            players_str += str(player_obj[idx]) + '\n'
        '''
        string_repr = '\tTEAM:\t' + str(self.name) + ',\t' \
                      + str(self.acronym) + '\n\tFROM:\t' + \
                      str(self.location) + '\n' + '\tPLAYERS:\n' \
                      + players_str + ' )'
        return string_repr

    def get_team_roster_on_day(self, day):
        ''' Return a list of tuples containing team roster on day
        :param day: The day in question.
        :returns roster_on_day: List of tuples containing player names, objects.
        '''
        inv_teams_dict = {acronym: team for team, acronym in teams_dict.items()}
        #print('\tinv_teams_dict:')
        #print(print_dict(inv_teams_dict))
        roster_on_day = []
        for player_id, player_obj in list_of_players.items():
            player_name = player_obj[0].name
            #player_team = None
            player_team_acronym = player_obj[len(player_obj) - 1].team
            player_team = inv_teams_dict[player_obj[len(player_obj) - 1].team]
            if team_obj_name == player_team:
                player_signed_at_date = player_playing_on_date(player_id, day)
                team_obj_name = self.name
                #print('player:  ' + str(player_name) + '  start_date:  ' + str(start_date) + '  player_signed_at_season_start:  ' + str(player_signed_at_season_start))
                if player_signed_at_date:
                    roster_on_day.append((player_id, player_obj))
        return roster_on_day
                #print('UNSIGNED player name:\t' + str(player_name) + ', team:\t' + str(player_team))
                #team.list_of_players = 

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
        #print('team:\t' + str(team))
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

#-------------------------------------------------------------------------------
        

list_of_players = create_players()
#print(print_dict(list_of_players))
list_of_teams = create_teams()
prev_player = ''

def get_transaction_dates():
    # play up until retirement
    retired_players = {'October 19, 2018': 'Jordin Tootoo',
                       'November 12, 2018': 'Luke Opilka',
                       'November 14, 2018': 'Paul Martin',
                       'January 11, 2019': 'Rick Nash',
                       'January 14, 2019': 'Josh Gorges',
                       'January 16, 2019': 'Brandon Bollig',
                       'January 31, 2019': 'Antoine Vermette'}
    # signed on during season
    free_agents = {'October 17, 2018': 'Jake Dotchin',
                       'October 30, 2018': 'Brandon Hagel',
                       'November 30, 2018': 'Justin Falk',
                       'February 19, 2019': 'Michael Leighton',
                       'February 24, 2019': 'Lee Stempniak'}
    # called up during season
    import_players = {'November 2, 2018': ['Colton Beck'],
                      'November 4, 2018': ['Matt Donovan'],
                      'November 11, 2018': ['Logan Shaw'],
                      'December 14, 2018': ['Mitch Eliot'],
                      'February 5, 2019': ['Turner Elson'],
                      'February 19, 2019': ['Tom McCollum'],
                      'February 20, 2019': ['Joseph Cramarossa'],
                      'February 24, 2019': ['Jeremy Smith',
                                            'Chris Driedger',
                                            'Adam Wilcox',
                                            'Evan Cormier',
                                            'Parker Milner'],         
                      'February 25, 2019': ['Ken Appleby'],
                      'March 1, 2019': ['Jimmy Huntington',
                                        'Tye Felhaber'],
                      'March 4, 2019': ['Simon Benoit'],
                      'March 6, 2019': ['Reese Johnson'],
                      'March 11, 2019': ['Jake Lucchini'],
                      'March 12, 2019': ['Max Veronneau',
                                         'Ryan Kuffner',
                                         'Josh Teves',
                                         'Taro Hirose'],
                      'March 13, 2019':	['Joseph Duszak'],
                      'March 15, 2019':	['Jacob Elmer'],
                      'March 18, 2019':	['Joe Snively',
                                         'Mat Robson',
                                         'Brady Keeper'],
                      'March 19, 2019':	['Josh Melnick',
                                         'Luke Philp'],
                      'March 21, 2019':	['Grant Hutton'],
                      'March 26, 2019':	['Bobo Carpenter'],
                      'March 30, 2019':	['Patrick Newell',
                                         'Artyom Zagidulin'],
                      'April 1, 2019': ['Nico Sturm',
                                        'Jake Kielly',
                                        'Brogan Rafferty'],
                      'April 2, 2019': ['Mason Jobst',
                                        'Blake Lizotte'],
                      'April 3, 2019': ['Andrew Shortridge',
                                        'Jimmy Schuldt'],
                      'April 5, 2019': ['Bobby Nardella',
                                        'Lukas Craggs',
                                        'Brandon Fortunato']}
    # played for one team, then transferred
    # {date: ((to team, player), (to team, player))}
    traded_players = {'October 3, 2018': [(('Montreal Canadiens','Gustav Olofsson'), ('Minnesota Wild', 'William Bitten'))],
                      'October 18, 2018': [(('Tampa Bay Lightning', 'Mitch Hults'), ('Anaheim Ducks',''))],
                      'November 10, 2018': [(('Dallas Stars', 'Taylor Fedun'), ('Buffalo Sabres', ''))],
                      'November 14, 2018': [(('Los Angeles Kings', 'Carl Hagelin'), ('Pittsburgh Penguins', 'Tanner Pearson'))],
                      'November 16, 2018': [(('New York Rangers', 'Ryan Strome'), ('Edmonton Oilers', 'Ryan Spooner'))],
                      'November 21, 2018': [(('Los Angeles Kings', 'Pavel Jenys'), ('Minnesota Wild', 'Stepan Falkovsky'))],
                      'November 22, 2018': [(('Edmonton Oilers', 'Chris Wideman'), ('Ottawa Senators', ''))],
                      'November 25, 2018': [(('Chicago Blackhawks', 'Dylan Strome', 'Brendan Perlini'), ('Arizona Coyotes', 'Nick Schmaltz'))],
                      'November 27, 2018': [(('Toronto Maple Leafs', 'Morgan Klimchuk'), ('Calgary Flames', 'Andrew Nielsen'))],
                      'December 3, 2018': [(('Vancouver Canucks', 'Josh Leivo'), ('Toronto Maple Leafs', 'Michael Carcone'))],
                      'December 3, 2018': [(('Anaheim Ducks', 'Daniel Sprong'), ('Pittsburgh Penguins', 'Marcus Pettersson'))],
                      'December 5, 2018': [(('Ottawa Senators', 'Stefan Elliott', 'Tobias Lindberg'), ('Pittsburgh Penguins', 'Ben Sexton', 'Macoy Erkamps'))],
                      'December 10, 2018': [(('Anaheim Ducks', 'Adam Cracknell'), ('Toronto Maple Leafs', 'Steven Oleksy'))],
                      'December 28, 2018': [(('Anaheim Ducks', 'Trevor Murphy'), ('Arizona Coyotes', 'Giovanni Fiore'))],
                      'December 29, 2018': [(('Toronto Maple Leafs', 'Michael Hutchinson'), ('Florida Panthers', ''))],
                      'December 30, 2018': [(('Edmonton Oilers', 'Alex Petrovic'), ('Florida Panthers', 'Chris Wideman')), (('Chicago Blackhawks', 'Drake Caggiula', 'Jason Garrison'), ('Edmonton Oilers', 'Brandon Manning', 'Robin Norell'))],
                      'January 2, 2019': [(('Ottawa Senators', 'Anders Nilsson', 'Darren Archibald'), ('Vancouver Canucks', 'Mike McKenna', 'Tom Pyatt'))],
                      'January 3, 2019': [(('St. Louis Blues', 'Jared Coreau'), ('Anaheim Ducks', '')), (('Winnipeg Jets', 'Jimmy Oligny'), ('Vegas Golden Knights', ''))],
                      'January 11, 2019': [(('Ottawa Senators', 'Morgan Klimchuk'), ('Toronto Maple Leafs', 'Gabriel Gagne')), (('Ottawa Senators', 'Cody Goloubef'),	('Boston Bruins', 'Paul Carey')), (('Arizona Coyotes', 'Jordan Weal'), ('Philadelphia Flyers', 'Jacob Graves')), (('Chicago Blackhawks', 'Slater Koekkoek'), ('Tampa Bay Lightning', 'Jan Rutta'))],
                      'January 14, 2019': [(('Dallas Stars', 'Andrew Cogliano'), ('Anaheim Ducks', 'Devin Shore')), (('New York Rangers', 'Connor Brickley'), ('Nashville Predators', 'Cole Schneider'))],
                      'January 16, 2019': [(('Minnesota Wild', 'Pontus Aberg'), ('Anaheim Ducks', 'Justin Kloos'))],
                      'January 17, 2019': [(('Anaheim Ducks', 'Michael Del Zotto'), ('Vancouver Canucks', 'Luke Schenn')), (('Anaheim Ducks', 'Derek Grant'), ('Pittsburgh Penguins', 'Joseph Blandisi')), (('Carolina Hurricanes', 'Nino Niederreiter'), ('Minnesota Wild', 'Victor Rask')), (('Philadelphia Flyers', 'Justin Bailey'), ('Buffalo Sabres', 'Taylor Leier'))],
                      'January 21, 2019': [(('Minnesota Wild', 'Brad Hunt'), ('Vegas Golden Knights', ''))],
                      'January 24, 2019': [(('Chicago Blackhawks', 'Dominik Kubalik'), ('Los Angeles Kings', ''))],
                      'January 28, 2019': [(('Dallas Stars', 'Jamie Oleksiak'), ('Pittsburgh Penguins', '')), (('Toronto Maple Leafs', 'Jake Muzzin'), ('Los Angeles Kings', 'Carl Grundstrom', 'Sean Durzi'))],
                      'January 30, 2019': [(('New Jersey Devils', 'Ryan Murphy'), ('Minnesota Wild', 'Michael Kapla'))],
                      'February 1, 2019': [(('Pittsburgh Penguins', 'Nick Bjugstad', 'Jared McCann'), ('Florida Panthers', 'Derick Brassard', 'Riley Sheahan'))],
                      'February 6, 2019': [(('Colorado Avalanche', 'Max McCormick'), ('Ottawa Senators', 'J.C. Beaudin')), (('Nashville Predators', 'Brian Boyle'), ('New Jersey Devils', '')), (('Nashville Predators', 'Cody McLeod'), ('New York Rangers', ''))],
                      'February 8, 2019': [(('Arizona Coyotes', 'Emil Pettersson'), ('Nashville Predators', 'Adam Helewka', 'Laurent Dauphin'))],
                      'February 9, 2019': [(('Montreal Canadiens', 'Dale Weise', 'Christian Folin'), ('Philadelphia Flyers', 'David Schlemko', 'Byron Froese'))],
                      'February 11, 2019': [(('Montreal Canadiens', 'Nate Thompson'), ('Los Angeles Kings', '')), (('Pittsburgh Penguins', 'Blake Siebenaler'), ('Columbus Blue Jackets', ''))],
                      'February 12, 2019': [(('Vancouver Canucks', 'Marek Mazanec'), ('New York Rangers', ''))],
                      'February 15, 2019': [(('Philadelphia Flyers', 'Cam Talbot'), ('Edmonton Oilers', 'Anthony Stolarz'))],
                      'February 16, 2019': [(('Edmonton Oilers', 'Sam Gagner'), ('Vancouver Canucks', 'Ryan Spooner'))],
                      'February 18, 2019': [(('Chicago Blackhawks', 'Peter Holland'), ('New York Rangers', 'Darren Raddysh'))],
                      'February 20, 2019': [(('Boston Bruins', 'Charlie Coyle'), ('Minnesota Wild', 'Ryan Donato'))],
                      'February 21, 2019': [(('Washington Capitals', 'Carl Hagelin'), ('Los Angeles Kings', ''))],
                      'February 22, 2019': [(('Columbus Blue Jackets', 'Matt Duchene', 'Julius Bergman'), ('Ottawa Senators', 'Vitaly Abramov', 'Jonathan Davidsson')), (('Florida Panthers', 'Vincent Praplan'), ('San Jose Sharks', '')), (('Washington Capitals', 'Nick Jensen'), ('Detroit Red Wings', 'Madison Bowey'))],
                      'February 23, 2019': [(('Dallas Stars', 'Ben Lovejoy'), ('New Jersey Devils', 'Connor Carrick')), (('Columbus Blue Jackets', 'Ryan Dzingel'), ('Ottawa Senators', 'Anthony Duclair')), (('Dallas Stars', 'Mats Zuccarello'), ('New York Rangers', ''))],
                      'February 24, 2019': [(('Chicago Blackhawks', 'Spencer Watson'), ('Los Angeles Kings', 'Matt Iacopelli')), (('Buffalo Sabres', 'Brandon Montour'), ('Anaheim Ducks', 'Brendan Guhle')), (('Toronto Maple Leafs', 'Nicholas Baptiste'), ('Nashville Predators', ''))],
                      'February 25, 2019': [(('San Jose Sharks', 'Gustav Nyquist'), ('Detroit Red Wings', '')), (('Ottawa Senators', 'Brian Gibbons'), ('Anaheim Ducks', 'Patrick Sieloff')), (('Columbus Blue Jackets', 'Keith Kinkaid'), ('New Jersey Devils', '')), (('Winnipeg Jets', 'Kevin Hayes'), ('New York Rangers', 'Brendan Lemieux')), (('Montreal Canadiens', 'Jordan Weal'), ('Arizona Coyotes', 'Michael Chaput')), (('Florida Panthers', 'Cliff Pu'), ('Carolina Hurricanes', '')), (('Colorado Avalanche', 'Derick Brassard'), ('Florida Panthers', '')), (('Columbus Blue Jackets', 'Adam McQuaid'), ('New York Rangers', 'Julius Bergman')), (('Calgary Flames', 'Oscar Fantenberg'), ('Los Angeles Kings', '')), (('Nashville Predators', 'Mikael Granlund'), ('Minnesota Wild', 'Kevin Fiala')), (('Vegas Golden Knights', 'Mark Stone', 'Tobias Lindberg'), ('Ottawa Senators', 'Erik Brannstrom', 'Oscar Lindberg')), (('Nashville Predators', 'Wayne Simmonds'), ('Philadelphia Flyers', 'Ryan Hartman')), (('St Louis Blues', 'Michael Del Zotto'), ('Anaheim Ducks', '')), (('Boston Bruins', 'Marcus Johansson'), ('New Jersey Devils', '')), (('Winnipeg Jets', 'Matt Hendricks'), ('Minnesota Wild', '')), (('Pittsburgh Penguins', 'Erik Gudbranson'), ('Vancouver Canucks', 'Tanner Pearson')), (('Winnipeg Jets', 'Nathan Beaulieu'), ('Buffalo Sabres', '')), (('Winnipeg Jets', 'Bogdan Kiselevich'), ('Florida Panthers', '')), (('San Jose Sharks', 'Jonathan Dahlen'), ('Vancouver Canucks', 'Linus Karlsson')), (('Toronto Maple Leafs', 'Nic Petan'), ('Winnipeg Jets', 'Par Lindholm')), (('Pittsburgh Penguins', 'Chris Wideman'), ('Florida Panthers', 'Jean-Sebastien Dea')), (('Winnipeg Jets', 'Alex Broadhurst'), ('Columbus Blue Jackets', ''))]}

    # signed unrestricted free agent
    waivered_players = {'October 15, 2018': ('Marko Dano', 'Colorado Avalanche', 'Winnipeg Jets'),
                        'October 17, 2018': ('Jacob de la Rose', 'Detroit Red Wings', 'Montreal Canadiens'),
                        'November 23, 2018': ('Marko Dano', 'Winnipeg Jets', 'Colorado Avalanche'),
                        'November 29, 2018': ('Jean-Sebastien Dea', 'Pittsburgh Penguins', 'New Jersey Devils'),
                        'November 29, 2018': ('Calvin Pickard', 'Arizona Coyotes', 'Philadelphia Flyers'),
                        'November 30, 2018': ('Valentin Zykov', 'Edmonton Oilers', 'Carolina Hurricanes'),
                        'December 2, 2018': ('Nikita Scherbak', 'Los Angeles Kings', 'Montreal Canadiens'),
                        'December 3, 2018': ('Brendan Leipsic', 'Los Angeles Kings', 'Vancouver Canucks'),
                        'December 6, 2018': ('Gemel Smith', 'Boston Bruins', 'Dallas Stars'),
                        'December 11, 2018': ('Chad Johnson', 'Anaheim Ducks', 'St. Louis Blues'),
                        'December 29, 2018': ('Valentin Zykov', 'Vegas Golden Knights', 'Edmonton Oilers'),
                        'January 1, 2019': ('Phillip Di Giuseppe', 'Nashville Predators', 'Carolina Hurricanes'),
                        'January 4, 2019': ('Mike McKenna', 'Philadelphia Flyers', 'Vancouver Canucks'),
                        'January 15, 2019': ('Colby Cave', 'Edmonton Oilers', 'Boston Bruins'),
                        'January 25, 2019': ('Anthony Bitetto', 'Minnesota Wild', 'Nashville Predators'),
                        'February 11, 2019': ('Kenny Agostino',	'New Jersey Devils', 'Montreal Canadiens'),
                        'February 20, 2019': ('Micheal Haley', 'San Jose Sharks', 'Florida Panthers')}
    ret_set = set([x for x in list(retired_players.values())])
    retired_players_list = list(ret_set)
    fa_set = set([x for x in list(free_agents.values())])
    free_agents_list = list(fa_set)
    import_players_lst = [[y for y in x] for x in import_players.values()]

    import_players_list = []
    for date in import_players_lst:
        for player in date:
            import_players_list.append(player)
    im_set = set(import_players_list)
    import_players_list = list(im_set)
    traded_players_list = []
    inv_traded_players = {}
    pick_considerations = 0
    for date, transactions in traded_players.items():
        #print('date:\t' + str(date) + '\ttransactions[0]:\t' + str(transactions[0]))
        for transaction in transactions:
            for team in transaction:
                lst = list(team)
                for name in lst[1:]:
                    if name != '':
                        traded_players_list.append(name)
                        if name in inv_traded_players.keys():
                            inv_traded_players[name].append(date)
                        else:
                            inv_traded_players[name] = [date]
                    else:
                        pick_considerations += 1

    wa_set = set([waivered_players[transaction][0] for transaction in waivered_players])
    waivered_players_list = list(wa_set)
    inv_waivered_players = {}
    for date, transaction in waivered_players.items():
        player = transaction[0]
        if player in inv_waivered_players.keys():
            inv_waivered_players[player].append(date)
        else:
            inv_waivered_players[player] = [date]
            
    unique_traded_players = set(traded_players_list)
    traded_players_list = list(unique_traded_players)
    retired_players_list.sort()
    import_players_list.sort()
    free_agents_list.sort()
    traded_players_list.sort()
    waivered_players_list.sort()
    '''
    print('--------------------v-LISTS-v---------------------------' + '\n')
    print('RETIRED PLAYERS LIST\t' + str(len(retired_players_list)) + '\t' + str(retired_players_list) + '\n')
    print('WAIVERED PLAYERS LIST\t' + str(len(waivered_players_list)) + '\t' + str(waivered_players_list) + '\n')
    print('IMPORT PLAYERS LIST\t' + str(len(import_players_list)) + '\t' + str(import_players_list) + '\n')
    print('TRADED PLAYERS LIST\t' + str(len(traded_players_list)) + '\t' + str(traded_players_list) + '\n')
    print('TRADED PLAYERS DICT\t' + str(len(traded_players)) + '\t\n' + print_dict(traded_players) + '\n')
    print('INV TRADED PLAYERS DICT\t' + str(len(inv_traded_players)) + '\t\n' + print_dict(inv_traded_players) + '\n')
    print('FREE AGENTS LIST:\t' + str(len(free_agents_list)) + '\t' + str(free_agents_list) + '\n')
    print('--------------------^-LISTS-^---------------------------')
    '''

    print_found_player_in_dataset = False
    transactions = {}
    players_counted = 0
    for id, player in list_of_players.items():
        name = player[0].name.title()
        if name in retired_players_list:
            players_counted += 1
            if print_found_player_in_dataset:
                print('FOUND RETIRED PLAYER IN DATASET\t' + str(name))
            date = convert_date([key for key, value in retired_players.items() if value == name][0])
            if date in transactions.keys():
                transactions[date].append((name, 'retired'))
            else:
                transactions[date] = [(name, 'retired')]
            #raise ValueError('RETIRED PLAYER IN DATASET')
        if name in free_agents_list:
            players_counted += 1
            if print_found_player_in_dataset:
                print('FOUND FREE AGENT IN DATASET\t' + str(name))
            date = convert_date([key for key, value in free_agents.items() if value == name][0])
            if date in transactions.keys():
                transactions[date].append((name, 'free_agent'))
            else:
                transactions[date] = [(name, 'free_agent')]
            #raise ValueError('FREE AGENT IN DATASET')
        if name in import_players_list:
            players_counted += 1
            if print_found_player_in_dataset:
                print('FOUND IMPORT PLAYER IN DATASET\t' + str(name))
            date = convert_date([key for key, value in import_players.items() if name in value][0])
            if date in transactions.keys():
                transactions[date].append((name, 'import'))
            else:
                transactions[date] = [(name, 'import')]
            #raise ValueError('IMPORT PLAYER IN DATASET')
        if name in traded_players_list:
            if print_found_player_in_dataset:
                print('FOUND TRADED PLAYER IN DATASET\t' + str(name))
            while len(inv_traded_players[name]) > 0:
                players_counted += 1
                date = convert_date(inv_traded_players[name][0])# [key for key, value in traded_players.items() if name in value][0]
                new_list_of_dates = inv_traded_players[name].copy()
                #print('NEW DATES COPY:\t' + str(new_list_of_dates))
                new_list_of_dates.reverse()
                new_list_of_dates.pop()
                inv_traded_players[name] = new_list_of_dates
                #print('NEW DATES POPPED:\t' + str(new_list_of_dates))
                if date in transactions.keys():
                    transactions[date].append((name, 'traded'))
                else:
                    transactions[date] = [(name, 'traded')]
            #raise ValueError('IMPORT PLAYER IN DATASET')
        
        if name in waivered_players_list:
            if print_found_player_in_dataset:
                print('FOUND WAIVERED PLAYER IN DATASET\t' + str(name))
            while len(inv_waivered_players[name]) > 0:
                players_counted += 1
                date = convert_date(inv_waivered_players[name][0])# [key for key, value in traded_players.items() if name in value][0]
                new_list_of_dates = inv_waivered_players[name].copy()
                #print('NEW DATES COPY:\t' + str(new_list_of_dates))
                new_list_of_dates.reverse()
                new_list_of_dates.pop()
                inv_waivered_players[name] = new_list_of_dates
                #print('NEW DATES POPPED:\t' + str(new_list_of_dates))
                if date in transactions.keys():
                    transactions[date].append((name, 'waivered'))
                else:
                    transactions[date] = [(name, 'waivered')]
            #raise ValueError('IMPORT PLAYER IN DATASET')
        #else:
            #print('UNABLE TO FIND\t' + str(player[0].name.title()))
    total_players = len(free_agents_list) + len(traded_players_list) + len(waivered_players_list) + len(import_players_list) + len(retired_players_list)
    #print('players_counted: '+ str(players_counted) + ' / ' + str(total_players))
    sum_players = [len(val) for key, val in transactions.items()]
    #print('sum_players:\t' + str(sum_players))
    sum_players = sum(sum_players)
    #print('len(transactions) (AKA dates):\t' + str(len(transactions)) + ', num_players:\t' + str(sum_players))
    if print_found_player_in_dataset:
        print('\n\tTRANSACTIONS' + print_dict(transactions) + '\n')
    return transactions
    
def gen_trades():
    transactions = get_transaction_dates()
    #corrected_transactions = {}
    #for key, val in transactions.items():
#        date = convert_date(key)
    #    date = key
    #    corrected_transactions[date] = val
    #    space = '\t' if len(key) < 16 else ''
        #print(str(key) + ':\t' + space + str(val))
    #print('\ncorrected_transactions' + print_dict(corrected_transactions) + '\n')
    return transactions
    
'''
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
'''

transactions = gen_trades()
        
    

#print(players_stats_df.head())

#------------------------------------------------------------------------------

def player_playing_on_date(player_in, date):
    print_traded_and_attendance = False
    player_id = player_in
    player_obj = list_of_players[player_id]
    player_in = player_obj[0].name
    inv_transactions = {}
    for transaction_date, transaction in transactions.items():
        for player in transaction:
            if player[0] in list(inv_transactions.keys()):
                inv_transactions[player[0]].append((transaction_date, player[1]))
            else:
                inv_transactions[player[0]] = [(transaction_date, player[1])]
    for player, transaction_dates in inv_transactions.items():
        transaction_dates.sort()
    #         transacted_players.append(player[0])
    #         # print(transacted_players)
    # if player_in in transacted_players:
    if player_in in list(inv_transactions.keys()):
        if print_traded_and_attendance:
            print('PLAYER WAS MOVED')
        transaction_dates = inv_transactions[player_in]
        for date_transacted in transaction_dates:
            t_date = date_transacted[0]
            type_transaction = date_transacted[1].lower()
            #print('player:\t' + str(player_in) + '\tt_date:\t' + str(t_date) + '\ttype\t' + str(type_transaction))
            if type_transaction == 'import' or type_transaction == 'free_agent':
                if player_obj[0].gp == 82:
                    raise ValueError('IMPORT OR WAIVERED PLAYER SOMEHOW PLAYED 82 GAMES')
                if t_date > date:
                    return False # Entered after date in question
            elif player_obj[0].gp < 82:
                if print_traded_and_attendance:
                    print('DIDNT PLAY THE FULL SEASON')
                
    #print('PLAYER OBJECT:\t' + str(player_obj))
    #if player_obj.team == 'TOT':
        
    inv_transactions_str = print_dict(inv_transactions)
    #print(inv_transactions_str)
    return True # player not involved in a transaction

def populate_teams_season_start():
    inv_teams_dict = {acronym: team for team, acronym in teams_dict.items()}
    #print('\tinv_teams_dict:')
    #print(print_dict(inv_teams_dict))
    print_signed_status = False
    for player_id, player_obj in list_of_players.items():
        player_name = player_obj[0].name
        #player_team = None
        player_signed_at_season_start = player_playing_on_date(player_id, start_date)
        player_team_acronym = player_obj[len(player_obj) - 1].team
        player_team = inv_teams_dict[player_obj[len(player_obj) - 1].team]
        #print('player:  ' + str(player_name) + '  start_date:  ' + str(start_date) + '  player_signed_at_season_start:  ' + str(player_signed_at_season_start))
        if player_signed_at_season_start:
            list_of_teams[player_team].list_of_players.append((player_id, player_obj))
            if print_signed_status:
                print('SIGNED player name:\t' + str(player_name) + ', team:\t' + str(player_team))

            # CURRENTLY ADDING EVERY PLAYER TO EVERY TEAM, NEEDS TO BE ADJUSTED
        else:
            if print_signed_status:
                print('UNSIGNED player name:\t' + str(player_name) + ', team:\t' + str(player_team))
        #team.list_of_players = 


# MAIN LOOP
today = start_date
last_day = '2019-04-07' # day after last day of games ('2019-04-06')
populate_teams_season_start()
#print('transactions dates\t' + str(transactions.keys()))
#print('games dates\t' + str(rank_sim_regular_season.schedule.keys()))
print_games = False
print_transactions = True
print_daily_team_rosters = False # Youll be in for it...
'''
TIME:
	TOTAL:	1 : 37.582151
	TOTAL:	97 : 45.704228

	--- 5865.704228401184 seconds ---
'''
while today != last_day:
    print('vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv')    
    if today not in rank_sim_regular_season.schedule.keys():
        print('\nNO GAMES\t' + str(today) + '\n')
    else:
        print('\n\n\ttoday:\t' + str(today) + '\n')
        print('\tGAMES:')
        todays_games = rank_sim_regular_season.schedule[today]
        if print_games:
            for game in todays_games:
                print(game)
    if today not in transactions.keys():
        print('\nNO TRANSACTIONS\t' + str(today) + '\n')
    else:
        print('\n\n\ttoday:\t' + str(today) + '\n')
        print('\tTRANSACTIONS:')
        todays_transactions = transactions[today]
        if print_transactions:
            for transaction in todays_transactions:
                print(transaction)
    
    if print_daily_team_rosters:
        for name, obj in list_of_teams.items():
            team_roster_today = obj.get_team_roster_on_day(today)
            print('\tTEAM ROSTER ' + str(today) + '\n')
            for player in team_roster_today:
                print(player)
    print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
    today = generate_date().__next__()
'''
for team, team_stats in list_of_teams.items():
    print('\n\t-- TEAM --\n\t' + str(team))
    print(list_of_teams[team])
'''
sum_execution_time = script_execution_time
end_time = time.time()
rank_sim_exec_mins, rank_sim_exec_seconds = divmod(rank_sim_execution_time, 60)

total_seconds = end_time - sum_execution_time
execution_minutes, executon_seconds = divmod(total_seconds, 60)
print('\n\tTIME:\t\tMIN\tSEC')
print('\tRANK SIM:\t( {:0d} : {:0f} )'.format(int(rank_sim_exec_mins), rank_sim_exec_seconds))
print('\tTOTAL:\t\t( {:0d} : {:0f} )'.format(int(execution_minutes), executon_seconds))
print("\n\t--- %s seconds ---" % (total_seconds))
