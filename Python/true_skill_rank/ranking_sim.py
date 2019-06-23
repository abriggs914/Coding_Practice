import pandas as pd


class RankingSim:

    def __init__(self):
        self.game_number = 0
        self.START_MMR = 25
        self.CONFIDENCE = float(25 / 3)
        self.schedule = {}
        self.games = {}

    def populate_games_dict(self, games_file):
        for i in range(len(games_file)):
            # row = games_file.iloc[i]
            col_names = ['team_1', 'team_2', 'location', 'result', 'date', 'team_1_score', 'team_2_score']
            row = pd.Series(games_file.iloc[i])
            # print(row['date'])
            if not self.same_game_check(row):
                # print('append')
                if row['date'] not in self.schedule.keys():
                    print('adding game', row['team_1'], 'vs', row['team_2'], 'date:', row['date'])
                    self.schedule[row['date']] = [row]
                    self.add_team_record(row['team_1'], row)
                    self.add_team_record(row['team_2'], self.swap_stats_team1_team2(row))
                else:
                    print('adding game', row['team_1'], 'vs', row['team_2'], 'date:', row['date'])
                    self.schedule[row['date']].append(row)
                    self.add_team_record(row['team_1'], row)
                    self.add_team_record(row['team_2'], self.swap_stats_team1_team2(row))
            # print(self.schedule)


    def same_game_check(self, game):
        day = game['date']
        if day in self.schedule.keys():
            team_1_a = game['team_1']
            team_1_b = game['team_2']
            team_2_a = [self.schedule[day][i]['team_1'] for i in range(len(self.schedule[day]))]
            team_2_b = [self.schedule[day][i]['team_2'] for i in range(len(self.schedule[day]))]
            # print('schedule team_2_a',team_2_a)
            # print('schedule team_2_b',team_2_b)
            if team_1_a in team_2_a or team_1_a in team_2_b:
                return True
            if team_1_b in team_2_a or team_1_b in team_2_b:
                return True
        return False

    def add_team_record(self, team_name, param_record):
        print('PARAM',param_record)
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
            print('key', key)
            if key == team_name:
                print('APPENDING HERE')
                self.game_number += 1
                # print('team_name:',team_name, 'record[\'num_games\']', record['num_games/'],'type(record):', type(record))\
                x = len(self.games[key])
                print('x:',x)
                record_df.at[team_name, 'num_games'] = x + 1
                # record_df.loc[record_df.num_games] = len(self.games[key]) + 1
                # record = param_record.copy()
                print('already exists', team_name)
                print('\nrecord::',record_df,'\n')
                print('ILOC[0]:', record_df.iloc[0])
                print('ILOC[1]:', record_df.iloc[1])
                self.games[team_name][self.game_number].append(record_df)
                return
        if team_name not in self.games.keys():
            self.game_number += 1
            print('FIRST ADDITION')
            # record_df.insert(len(record_df.columns), 'num_games', 1)
            record_df['num_games'] = 1
            # record = param_record.copy()
            # t = record
            # print('team_name:',team_name, 'record[\'num_games\']', t['num_games'],'type(record):', type(t))
            # print(record.at[team_name, 'num_games'])
            print('new', team_name)
            print('\nrecord::',record_df,'\n')
            self.games[team_name][self.game_number] = record_df

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
        print('res:', res)
        # print('SWAPPED')
        return res


def read_games_file():
    # file = pd.read_csv('games.csv')
    # file = pd.read_csv('test_1.csv')
    file = pd.read_csv('test_2.csv')
    return file


def create_df_from_series(series):
    print('CONVERTING')
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
    print('df_dict:', df_dict)
    res = pd.DataFrame(df_dict)
    # print(res)
    # print('res.values:', res.values)
    # print('list(res.index):', list(res.index))
    # print('res.columns:', res.columns)
    # print('list(res.index[0])', list(res.index)[0])
    # print('list(res.index[1:])', list(res.index)[1:])
    print('res', res)
    print('CONVERTED')
    return res


games = read_games_file()
print(games)
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
rank_sim = RankingSim()
rank_sim.populate_games_dict(games)
# print('\n')
# print('rank_sim.schedule:', rank_sim.schedule)
# print('\n')
print('-----------------------------------------------------------------------------')
for record in rank_sim.games.keys():
    print(record)
    for game in rank_sim.games[record]:
        print(game)
    print('\n')
    # print('\nRECORD\n', rank_sim.games[record])
    # print('\nRECORD ', rank_sim.games[record][0]['team_1'], '\n', rank_sim.games[record])
    # print('\nRECORD ', rank_sim.games[record][0]['team_1'], '\n')