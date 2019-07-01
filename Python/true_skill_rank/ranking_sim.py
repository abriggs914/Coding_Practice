import pandas as pd
import requests
from bs4 import BeautifulSoup

class RankingSim:

    def __init__(self):
        self.game_number = 0
        self.START_MMR = 25
        self.CONFIDENCE = float(25 / 3)
        self.schedule = {}
        self.games = {}
        self.skipped_games = []
        self.min_games_required_for_rank = 5

    def populate_games_dict(self, games_file):
        for i in range(len(games_file)):
            # row = games_file.iloc[i]
            col_names = ['team_1', 'team_2', 'location', 'result', 'date', 'team_1_score', 'team_2_score']
            row = pd.Series(games_file.iloc[i])
            # print(row['date'])
            if not self.same_game_check(row):
                # print('append')
                self.game_number += 1
                print('\nadding game', row['team_1'], 'vs', row['team_2'], 'date:', row['date'],'\n')
                if row['date'] not in self.schedule.keys():
                    self.schedule[row['date']] = [row]
                    self.add_team_record(row['team_1'], row)
                    self.add_team_record(row['team_2'], self.swap_stats_team1_team2(row))
                else:
                    # print('adding game', row['team_1'], 'vs', row['team_2'], 'date:', row['date'])
                    self.schedule[row['date']].append(row)
                    self.add_team_record(row['team_1'], row)
                    self.add_team_record(row['team_2'], self.swap_stats_team1_team2(row))
            else:
                self.skipped_games.append(row)
        print('Skipped', self.skipped_games)
            # print(self.schedule)


    def same_game_check(self, game):
        day = game['date']
        # for day in self.schedule.keys():
            # print('date:', day)
        team_1_a, team_1_b = None, None
        if day in self.schedule.keys():
            team_1_a = game['team_1'].strip().upper()
            team_1_b = game['team_2'].strip().upper()
            team_2_a = [self.schedule[day][i]['team_1'].strip().upper() for i in range(len(self.schedule[day]))]
            team_2_b = [self.schedule[day][i]['team_2'].strip().upper() for i in range(len(self.schedule[day]))]
            # print('in keys', day)
            # print('team_1_a', team_1_a,'schedule team_2_a',team_2_a)
            # print('team_1_b', team_1_b,'schedule team_2_b',team_2_b)
            # res = team_1_b in team_2_a
            # print(team_1_b)
            # print(team_2_a[0])
            # print('team_1_b',team_1_b, 'team_2_a', team_2_a, 'type(team_1_b)',type(team_1_b), 'type(team_2_a[0])', type(team_2_a[0]), '___', team_1_b == team_2_a[0])
            # print('res', res)
            if team_1_a in team_2_a or team_1_a in team_2_b:
                # print('exit 1')
                return True
            if team_1_b in team_2_a or team_1_b in team_2_b:
                # print('exit 2')
                return True
        # print('returning false')
        else:
            team_1_a = game['team_1']
            team_1_b = game['team_2']
        if not self.check_team_names(team_1_a, team_1_b):
            raise ValueError('INVALID TEAM NAME: ' + '[' + str(team_1_a) + ', ' + str(team_1_b) + ']')
        return False

    # def gen_alternate_view(self):
    #     games = self.games
    #     for record in games.keys():
    #         # print(record)
    #         # for game in rank_sim.games[record]:
    #         orig_table = games[record]
    #         cols = list(orig_table.columns)
    #         vals = list(orig_table.values)
    #         idx = list(orig_table.index)
    #         print('cols',cols)
    #         print('vals',vals)
    #         print('index',idx)
    #         print(orig_table['team_2'])
    #         new_view = orig_table.pivot(columns = cols, index = orig_table['team_2'], values = vals)
    #         print(new_view)
    #         print('\n')

    def add_team_record(self, team_name, param_record):
        # print('\nPARAM',param_record)
        # col_names = ['team_1', 'team_2', 'location', 'result', 'date', 'team_1_score', 'team_2_score']
        # record_df = param_record.to_frame()
        # record_df.pivot(columns=col_names, index='team_1')
        # print('ROW PIVOTED:', record_df)
        # record_df = pd.DataFrame()
        record_df = create_df_from_series(param_record)
        # record_df.pivot(columns = team_name, index = 'team_1')
        # pd.pivot_table(record_df, values=['date', 'location', 'team_1_score', 'team_2_score', 'result'], index=['team_1'], columns='team_2').reset_index()
        # print('COLUMNS', record_df.columns)
        # record_df.melt(id_vars='0',
        #         # var_name="date",
        #         value_name="Value")

        # print('TYPE:', type(record_df))
        # print('record_df:', record_df)
        for key in self.games.keys():
            # print('key', key)
            if key == team_name:
                # print('APPENDING HERE')
                # self.game_number += 1
                # print('team_name:',team_name, 'record[\'num_games\']', record['num_games/'],'type(record):', type(record))\
                x = len(self.games[key])
                # print('x:',x)
                # record_df.at[team_name, 'num_games'] = x + 1
                # record_df.loc[record_df.num_games] = len(self.games[key]) + 1
                # record = param_record.copy()
                print('already exists', team_name)
                # print('\nrecord::',record_df,'\n')
                # print('ILOC[0]:', record_df.iloc[0])
                # print('ILOC[1]:', record_df.iloc[1])
                record_df['num_games'] = x
                record_df['MMR'] = self.adjust_mmr(record_df)
                record_df['confidence'] = self.adjust_confidence(record_df)
                # print('CONCAT\t', self.games[team_name], '\n\t', record_df, '\n')
                self.games[team_name] = pd.concat([self.games[team_name], record_df], sort=False)#.reset_index()  #[self.game_number]|
                # self.games[team_name].at[team_name, 'num_games'] = x + 1
                return
        if team_name not in self.games.keys():
            # self.game_number += 1
            print('FIRST ADDITION')
            first_addition = self.first_addition(record_df)
            # record_df.insert(len(record_df.columns), 'num_games', 1)
            record_df['num_games'] = 1
            record_df['MMR'] = self.adjust_mmr(record_df)
            record_df['confidence'] = self.adjust_confidence(record_df)
            # print('\nfirst_addition:', len(list(first_addition.columns)), '\nrecord_df',len(list(record_df.columns)))
            self.games[team_name] = pd.concat([first_addition, record_df], sort=False)
            # record = param_record.copy()
            # t = record
            # print('team_name:',team_name, 'record[\'num_games\']', t['num_games'],'type(record):', type(t))
            # print(record.at[team_name, 'num_games'])
            # print('new', team_name)
            # print('\nrecord::',record_df,'\n')
            # print(self.games[team_name])#.insert(self.game_number, str(self.game_number), record_df)

            # print('HEY', self.games[team_name],'\n\n')

    def swap_stats_team1_team2(self, row):
        # print('SWAPPING')
        # columns = row.columns
        values = list(row.values)
        index = list(row.index)
        # print('columns:', columns)
        # print('values:', values)
        # print('index:', index)
        orig_team_1 = values[0]
        orig_team_2 = values[1]
        orig_location = values[2]
        orig_result = values[3]
        orig_date = values[4]
        orig_team_1_score = values[5]
        orig_team_2_score = values[6]
        new_location = 'away' if orig_location == 'home' else 'home'
        # if orig_result == 'W':
        #     new_result = 'L'
        # elif orig_result == 'W'
        new_result = 'W' if orig_result == 'L' else 'L'
        data = [orig_team_2, orig_team_1, new_location, new_result, orig_date, orig_team_2_score, orig_team_1_score]
        res = pd.Series(data, index = index)#.reset_index()
        # print('swap_res:', res)
        # print('SWAPPED')
        return res

    def adjust_mmr(self, param_record):
        mmr_change = self.START_MMR - 3 * self.CONFIDENCE
        team_1 = list(param_record['team_1'])[0]
        team_2 = list(param_record['team_2'])[0]
        if team_1 not in self.games.keys():
            print('First Game for the', team_1)
            return self.START_MMR
        if team_2 not in self.games.keys():
            # print('First Game for team_2', team_2)
            return self.START_MMR
        x = len(self.games[team_1])
        # print('x:',x)
        if x < self.min_games_required_for_rank:
            print('The',team_1,'have not yet played at least',self.min_games_required_for_rank,'games, \nand therefore can\'t be ranked confidently [' + str(x) + ' / ' + str(self.min_games_required_for_rank) + ']')
            return self.START_MMR
        # print('TEST', team_1, '_', team_2)
        # print('GAMES',self.games)
        print('ADJUSTING MMR')
        team_1_rank_list = list(self.games[team_1]['MMR'])
        team_1_rank = team_1_rank_list[len(team_1_rank_list) - 1]
        team_2_rank_list = list(self.games[team_2]['MMR'])
        team_2_rank = team_2_rank_list[len(team_2_rank_list) - 1]
        team_1_confidence_list = list(self.games[team_1]['confidence'])
        team_1_confidence = team_1_confidence_list[len(team_1_confidence_list) - 1]
        team_2_confidence_list = list(self.games[team_2]['confidence'])
        team_2_confidence = team_2_confidence_list[len(team_2_confidence_list) - 1]
        mmr_diff_1 = (1 - (team_1_rank - team_2_rank))
        mmr_diff_2 = mmr_diff_1 // 3
        mmr_diff_3 = mmr_diff_2 // 2
        # win
        mmr_diff_win, mmr_diff_loss = team_1_confidence, team_1_confidence
        mmr_diff_win -= (team_1_confidence - mmr_diff_3) / team_1_confidence
        # loss
        mmr_diff_loss += (team_1_confidence - mmr_diff_3) / team_1_confidence
        # print('PARAM', param_record)
        game_result = list(param_record['result'])[0]
        print(team_1 + ':', game_result)
        confidence = self.CONFIDENCE
        rank_range = (max(0, abs(team_1_rank - confidence)), min(50, abs(team_1_rank + confidence)))
        if game_result == 'W':
            # confidence = mmr_diff_win
            rank_estimate_unround = ((team_1_rank + rank_range[1]) / 2)
        elif game_result == 'L':
            # confidence = mmr_diff_loss
            # rank_range = (team_1_rank - confidence, team_1_rank + confidence)
            rank_estimate_unround = ((rank_range[0] + team_1_rank) / 2)
        rank_estimate = round(rank_estimate_unround)
        print('team_1_rank', team_1_rank, 'team_2_rank', team_2_rank)
        print('team_1_confidence', team_1_confidence, 'team_2_confidence', team_2_confidence)
        print('mmr_diff_1:', mmr_diff_1,'mmr_diff_2:', mmr_diff_2,'mmr_diff_3:', mmr_diff_3, 'mmr_change', mmr_change)
        print('mmr|_diff_win', mmr_diff_win, 'mmr_diff_loss', mmr_diff_loss)
        print('RANK RANGE:', rank_range, 'rank_estimate_unround', rank_estimate_unround, 'rank_estimate', rank_estimate)
        mmr_change = self.START_MMR
        print('MMR ADJUSTED')
        return rank_estimate

    def adjust_confidence(self, param_record):
        confidence = self.CONFIDENCE
        team_1 = list(param_record['team_1'])[0]
        team_2 = list(param_record['team_2'])[0]
        if team_1 not in self.games.keys():
            print('First Game for the', team_1)
            return self.CONFIDENCE
        if team_2 not in self.games.keys():
            # print('First Game for team_2', team_2)
            return self.CONFIDENCE
        x = len(self.games[team_1])
        # print('x:',x)
        if x < self.min_games_required_for_rank:
            print('The',team_1,'have not yet played at least',self.min_games_required_for_rank,'games, \nand therefore can\'t be ranked confidently [' + str(x) + ' / ' + str(self.min_games_required_for_rank) + ']')
            return self.CONFIDENCE
        print('ADJUSTING CONFIDENCE')
        # print('games', self.games)
        team_1_rank_list = list(self.games[team_1]['MMR'])
        team_1_rank = team_1_rank_list[len(team_1_rank_list) - 1]
        team_2_rank_list = list(self.games[team_2]['MMR'])
        team_2_rank = team_2_rank_list[len(team_2_rank_list) - 1]
        team_1_confidence_list = list(self.games[team_1]['confidence'])
        team_1_confidence = team_1_confidence_list[len(team_1_confidence_list) - 1]
        team_2_confidence_list = list(self.games[team_2]['confidence'])
        team_2_confidence = team_2_confidence_list[len(team_2_confidence_list) - 1]
        mmr_diff_1 = (1 - (team_1_rank - team_2_rank))
        mmr_diff_2 = mmr_diff_1 // 3
        mmr_diff_3 = mmr_diff_2 // 2
        # win
        mmr_diff_win, mmr_diff_loss = team_1_confidence, team_1_confidence
        mmr_diff_win -= (team_1_confidence - mmr_diff_3) / team_1_confidence
        # loss
        mmr_diff_loss += (team_1_confidence - mmr_diff_3) / team_1_confidence
        # print('PARAM', param_record)
        print('team_1_rank', team_1_rank, 'team_2_rank', team_2_rank)
        print('team_1_confidence', team_1_confidence, 'team_2_confidence', team_2_confidence)
        print('mmr_diff_1:', mmr_diff_1,'mmr_diff_2:', mmr_diff_2,'mmr_diff_3:', mmr_diff_3)
        print('mmr|_diff_win', mmr_diff_win, 'mmr_diff_loss', mmr_diff_loss)
        print('team_1', team_1, 'team_2', team_2)
        # print('param_record[\'result\']', param_record['result'])
        game_result = list(param_record['result'])[0]
        if game_result == 'W':
            confidence = mmr_diff_win
        elif game_result == 'L':
            confidence = mmr_diff_loss
        confidence = mmr_diff_win
        print('CONFIDENCE ADJUSTED')
        return confidence

    def first_addition(self, record_df):
        # print('ADDING FIRST ROW', record_df)
        team_1 = list(record_df['team_1'])[0]
        team_2 = '---------------------'
        # print('TEST', team_1)
        location_prefixes = ['New', 'Tampa', 'St', 'San', 'Los']
        two_name_mascots = ['Vegas', 'Columbus', 'Toronto', 'Detroit']
        location = team_1.split(' ')
        if len(location) == 3:
            if location[0] in location_prefixes:
                location = location[0] + ' ' + location[1]
            if location[0] in two_name_mascots:
                location = location[0]
        else:
            location = location[0]
        date = '----------'
        team_1_score = 'NA'
        team_2_score = 'NA'
        result = 'NA'
        # print('LOCATION', location)
        df_dict = {'team_1':[team_1],
                   'team_2':[team_2],
                   'location':[location],
                   'date':[date],
                   'result':[result],
                   'team_1_score':[team_1_score],
                   'team_2_score':[team_2_score],
                   'num_games':[0],
                   'MMR':[self.START_MMR],
                   'confidence':[self.CONFIDENCE]}
        # print('df_dict',df_dict)
        # print('type(df_dict)',type(df_dict))
        # for key, val in df_dict.items():
        #     print('key:',key,'val:', val)
        df = pd.DataFrame(df_dict)
        # print('df',df)
        # print('GAMES', self.games, '\nteam_1',team_1)
        # print('type::', type(self.games))
        return df

    def check_team_names(self, team_1, team_2):
        team_cities_split = [team.split(' ') for team in teams]
        team_1_temp = team_1.strip().title()
        team_2_temp = team_2.strip().title()
        special_team_names = ['Red', 'Maple', 'Blue', 'Golden']
        team_1_temp = team_1_temp.split(' ')
        team_2_temp = team_2_temp.split(' ')
        # team_2_temp = [team[0] if len(team) == 2 else team[0] if team[1] in special_team_names else team[0] + ' ' + team[1] for team in team_2_temp.split(' ')]
        # team_1_temp = ' '.join(team_1_temp)
        # team_2_temp = ' '.join(team_2_temp)
        team_1_temp = team_1_temp[0] if len(team_1_temp) == 2 else team_1_temp[0] if team_1_temp[1] in special_team_names else team_1_temp[0] + ' ' + team_1_temp[1]
        team_2_temp = team_2_temp[0] if len(team_2_temp) == 2 else team_2_temp[0] if team_2_temp[1] in special_team_names else team_2_temp[0] + ' ' + team_2_temp[1]
        print('team_1:', team_1_temp, 'team_2:', team_2_temp)
        team_cities = [team[0] if len(team) == 2 else team[0] if team[1] in special_team_names else team[0] + ' ' + team[1] for team in team_cities_split]
        print(team_cities)
        return True if team_1_temp in team_cities and team_2_temp in team_cities else False


def adjust_regular_season_dataframe(orig_frame):

    # need to change the indexes that are used to determine the values
    orig_frame_columns = list(orig_frame.columns)
    columns = ['team_1','team_2','location','result','date','team_1_score','team_2_score']
    df = pd.DataFrame()
    list_of_games = list(orig_frame.values)
    for game in list_of_games:
        game_dict = {}
        date = game[0]
        home_team = game[3]
        away_team = game[1]
        home_score = game[4]
        away_score = game[2]
        extra_result = game[5]
        if type(extra_result) != str:
            attendance_thousands = game[5]
            attendance_ones = game[6]
            log = game[7]
            notes = game[8]

        else:
            attendance_thousands = game[6]
            attendance_ones = game[7]
            log = game[8]
            notes = game[9]

        location_prefixes = ['New', 'Tampa', 'St', 'San', 'Los']
        two_name_mascots = ['Vegas', 'Columbus', 'Toronto', 'Detroit']
        location = home_team.split(' ')
        if len(location) == 3:
            if location[0] == 'St.':
                location[0] = 'St'
            if location[0] in location_prefixes:
                location = location[0] + ' ' + location[1]
            if location[0] in two_name_mascots:
                location = location[0]
        else:
            location = location[0]

        # location = get_location(home_team)
        print('attendance_thousands:', attendance_thousands, 'attendance_ones', attendance_ones)
        print('type(attendance_thousands):', type(attendance_thousands), 'type(attendance_ones)', type(attendance_ones))
        # attendance = attendance_thousands * 1000 + attendance_ones
        attendance = 'ATTENDANCE'

        print('\nhome_team:',home_team,'away_team:',away_team,'home_score:',home_score,'away_score:',away_score,'location:',location,'attendance:',attendance, 'extra_result:',extra_result,'log:', log, 'notes', notes)

        # print('values', game.values)
        # print('index', game.index)
        # print('game',game)
        # for col in list(game):
        #     print('type(col)',type(col),'col', col)
    return orig_frame


def read_games_file():
    # file = pd.read_csv('games.csv')
    # file = pd.read_csv('test_1.csv')
    # file = pd.read_csv('test_2.csv')
    # file = pd.read_csv('test_3.csv')
    file = adjust_regular_season_dataframe(pd.read_csv('regular_season_2018_2019.csv'))
    return file


def create_df_from_series(series):
    # print('CONVERTING')
    df2 = series.to_frame()
    values = join_list(df2.values)
    index = df2.index
    columns = df2.columns
    # print('values:', values)
    # print('list(index):', list(index))
    # print('columns:', columns)
    # print('list(df2.index[0])', list(index)[0])
    # print('list(df2.index[1:])', list(index)[1:])
    df_dict = {}
    i = 0
    for col in index:
        df_dict[col] = [values[i]]
        i += 1
    # print('df_dict:', df_dict)
    res = pd.DataFrame(df_dict)
    # print(res)
    # print('res.values:', res.values)
    # print('list(res.index):', list(res.index))
    # print('res.columns:', res.columns)
    # print('list(res.index[0])', list(res.index)[0])
    # print('list(res.index[1:])', list(res.index)[1:])
    # print('df_res', res)
    # print('CONVERTED')
    return res

#-----------------------------------
# games = read_games_file()
# print(games)
#-----------------------------------


# g = games.iloc[0]
# print(g)
# gf = g.to_frame()
# print(type(gf))
# print(gf.pivot(columns = gf.index, index = gf.columns, values = gf.values))

def join_list(lst):
    res = []
    for sub_lst in lst:
        for el in sub_lst:
            res.append(el)
    return res

# print('joined',join_list(gf.values))
# print(list(gf.index))

# df2 = pd.DataFrame(gf.index, join_list(gf.values))#, index = gf.columns) #, values = gf.values)
# print('values:', df2.values)
# print('list(index):', list(df2.index))
# print('columns:', df2.columns)
# print('list(df2.index[0])', list(df2.index)[0])
# print('list(df2.index[1:])', list(df2.index)[1:])
# create_df_from_series(g)
# df2.pivot(columns = df2.values, index = list(df2.index)[0], values = list(df2.index)[1:])
# print(df2)
print('-----------------------------------------------------------------------------')

teams = ['Anaheim Ducks',
         'Arizona Coyotes',
         'Boston Bruins',
         'Buffalo Sabres',
         'Calgary Flames',
         'Carolina Hurricanes',
         'Chicago Blackhawks',
         'Colorado Avalanche',
         'Columbus Blue Jackets',
         'Dallas Stars',
         'Detroit Red Wings',
         'Edmonton Oilers',
         'Florida Panthers',
         'Los Angeles Kings',
         'Minnesota Wild',
         'Montreal Canadiens',
         'Nashville Predators',
         'New Jersey Devils',
         'New York Islanders',
         'New York Rangers',
         'Ottawa Senators',
         'Philadelphia Flyers',
         'Pittsburgh Penguins',
         'San Jose Sharks',
         'St Louis Blues',
         'Tampa Bay Lightning',
         'Toronto Maple Leafs',
         'Vancouver Canucks',
         'Vegas Golden Knights',
         'Washington Capitals',
         'Winnipeg Jets']

#-----------------------------------
# rank_sim = RankingSim()
# rank_sim.populate_games_dict(games)
#-----------------------------------

# print('\n')
# print('rank_sim.schedule:', rank_sim.schedule)
# print('\n')

#-----------------------------------
print('-----------------------------------------------------------------------------')
# for record in rank_sim.games.keys():
#     # print(record)
#     # for game in rank_sim.games[record]:
#     print(rank_sim.games[record])
#     print('\n')
#     # print('\nRECORD\n', rank_sim.games[record])
#     # print('\nRECORD ', rank_sim.games[record][0]['team_1'], '\n', rank_sim.games[record])
#     # print('\nRECORD ', rank_sim.games[record][0]['team_1'], '\n')

#-----------------------------------

# rank_sim.gen_alternate_view()

# url = 'https://www.nhl.com/schedule/2018-09-01/ET'
# webpage_response = requests.get(url)
# print(webpage_response)
# webpage_content = webpage_response.content
# print(webpage_content)
# soup = BeautifulSoup(webpage_content, "html.parser")
# print(soup)

games_file = read_games_file()
print(games_file.columns)
print(games_file.head())
for col in list(games_file.columns):
    print('col:', col, '_', games_file.iloc[0][col])
print()
for col in list(games_file.columns):
    print('col:', col, '_', games_file.iloc[8][col])

