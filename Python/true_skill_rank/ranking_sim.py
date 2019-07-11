import pandas as pd
# import trueskill

#import requests
#from bs4 import BeautifulSoup

games_answers = True
START_CONFIDENCE = float(float(25)/float(3))
START_MMR = 25
print_details = False
print_more_details = False
print_window = False

class RankingSim:

    def __init__(self):
        self.game_number = 0
        self.START_MMR = START_MMR
        self.CONFIDENCE = START_CONFIDENCE
        self.schedule = {}
        self.games = {}
        self.skipped_games = []
        self.min_games_required_for_rank = 0

    def __repr__(self):
        string_res = ''
        highest_MMR_list = []
        lowest_MMR_list = []
        avg_MMR_list = []
        predictions = {}
        for team in self.games.keys():
            string_res += '\n\tTeam:\t' + str(team) + '\n'
            df = self.games[team]  # pd.DataFrame(
            results_guesses = list(df['guess_result'])
            predictions[team] = results_guesses
            print('results_guesses:\t' + str(results_guesses))
            show_dict = {'DATE': list(df['date']),
                         'VS': list(df['team_2']),
                         'RES': list(df['result']),
                         'GF': list(df['team_1_score']),
                         'GA': list(df['team_2_score']),
                         'WSTK': list(df['consec_wins']),
                         'LSTK': list(df['consec_losses']),
                         'MMR': list(df['MMR']),
                         'CONFD': list(df['confidence'])}
            show_df = pd.DataFrame.from_dict(show_dict)#, orient='index', columns=['DATE','VS','RES','GF','GA','WSTK','LSTK','MMR','CONFD'])
            columns = ['DATE', 'VS', 'RES', 'GF', 'GA', 'WSTK', 'LSTK', 'MMR', 'CONFD']
            show_df = show_df[columns]
            max_mmr = max(list(show_df['MMR'])[1:])
            min_mmr = min(list(show_df['MMR'])[1:])
            avg_mmr = sum(list(show_df['MMR'])[1:]) / len(list(show_df['MMR'])) - 1
            # print('len(list(show_df[\'MMR\'])) - 1:\t' + str(len(list(show_df['MMR'])) - 1))
            highest_MMR_list.append(max_mmr)
            lowest_MMR_list.append(min_mmr)
            avg_MMR_list.append(avg_mmr)
            space = ''
            # print('length:\t' + str(length))
            while len(team) + len(space) <= 25: # 4 tab spaces
                space += ' '
            mmr_space = ''
            while len(str(min_mmr)) + len(mmr_space) <= 3:
                mmr_space += ' '
            space_1 = ''
            while len(str(max_mmr)) + len(space_1) <= 3:
                space_1 += ' '
            print('TEAM:\t' + str(team) + str(space) + '\t\tHIGHEST MMR:\t' + str(max_mmr) + str(space_1) + '\tLOWEST MMR:\t' + str(min_mmr) + mmr_space + '\tAVERAGE MMR:\t' + str(avg_mmr))
            string_res += str(show_df)
        print('HIGHEST_MMR_LIST:\t' + str(highest_MMR_list))
        print('LOWEST_MMR_LIST:\t' + str(lowest_MMR_list))
        print('AVG_MMR_LIST:\t' + str(avg_MMR_list))
        print('GUESS RESULTS:\t' + str(self.showify_predictions_list(predictions)))
        return string_res

    def print_df(self, df):
        string_res = ''
        team = list(df['team_1'])[0]
        # for team in self.games.keys():
        string_res += '\n\tTeam:\t' + str(team) + '\n'
        # df = self.games[team]  # pd.DataFrame(
        show_dict = {'DATE': list(df['date']),
                         'VS': list(df['team_2']),
                         'RES': list(df['result']),
                         'GF': list(df['team_1_score']),
                         'GA': list(df['team_2_score']),
                         'WSTK': list(df['consec_wins']),
                         'LSTK': list(df['consec_losses']),
                         'MMR': list(df['MMR']),
                         'CONFD': list(df['confidence'])}
        show_df = pd.DataFrame.from_dict(show_dict)  # , orient='index', columns=['DATE','VS','RES','GF','GA','WSTK','LSTK','MMR','CONFD'])
        columns = ['DATE', 'VS', 'RES', 'GF', 'GA', 'WSTK', 'LSTK', 'MMR', 'CONFD']
        show_df = show_df[columns]
        # print('TEAM:\t' + str(team) + '\t\t\tHIGHEST MMR:\t' + str(max(list(show_df['MMR']))))
        string_res += str(show_df)
        return string_res

    def populate_games_dict(self, games_file):
        for i in range(len(games_file)):
            # row = games_file.iloc[i]
            col_names = ['team_1', 'team_2', 'location', 'result', 'date', 'team_1_score', 'team_2_score','consec_wins','consec_losses']
            row = pd.Series(games_file.iloc[i])
            # print('incoming date:  ' + str(row['date']))


            #THESE LINES SHOULD BE CHANGED
            # row['consec_wins'] = 0
            # row['consec_losses'] = 0
            # print('row', row)
            if not self.same_game_check(row):
                # print('append')
                self.game_number += 1
                print('\nadding game', row['team_1'], '@', row['team_2'], 'date:', row['date'],'\n')
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
        print('\n\t-- Skipped Games --\n' + str(self.skipped_games))
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
        # print('\nPARAM' + str(param_record) + str('\n\n\n\n\n'))
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
            # print('HEY', self.games[team_name],'\n\n')

        # col_names = list(record_df.columns)
        # consec = ('consec_wins', 'consec_losses')
        # if consec[0] not in col_names:
        #     record_df[consec[0]] = self.look_up_team_2_consec_wins(list(record_df['team_1'])[0])
        # if consec[1] not in col_names:
        #     record_df[consec[1]] = self.look_up_team_2_consec_losses(list(record_df['team_1'])[0])


        # print('TYPE:', type(record_df))
        # print('record_df:', record_df)
        for key in self.games.keys():
            # print('key', key)
            if key == team_name:

                game_num = len(record_df['team_1_score']) - 1
                team_1_score = record_df['team_1_score'][game_num]
                team_2_score = record_df['team_2_score'][game_num]
                win = True if team_1_score > team_2_score else False
                # print('APPENDING HERE')
                # self.game_number += 1
                # print('team_name:',team_name, 'record[\'num_games\']', record['num_games/'],'type(record):', type(record))\
                x = len(self.games[key])
                # print('x:',x)
                # record_df.at[team_name, 'num_games'] = x + 1
                # record_df.loc[record_df.num_games] = len(self.games[key]) + 1
                # record = param_record.copy()
                # print('already exists', team_name)

                record_df['consec_wins'] = 0 if not win else self.look_up_team_2_consec_wins(list(record_df['team_1'])[0]) + 1
                record_df['consec_losses'] = 0 if win else self.look_up_team_2_consec_losses(list(record_df['team_1'])[0]) + 1
                record_df['num_games'] = x
                record_df['MMR'] = self.adjust_mmr(record_df)
                record_df['confidence'] = self.adjust_confidence(record_df)
                team_2 = list(record_df['team_2'])[0]
                if print_window:
                    print('x:\t' + str(x) + '\tteam_2:\t' + str(team_2) + '\tteam_1_rank:\t' + str(list(record_df['MMR'])))
                team_1_rank = list(record_df['MMR'])[len(record_df['MMR']) - 1]
                if team_2 not in self.games.keys():
                    team_2_rank = START_MMR
                else:
                    team_2_rank = list(self.games[team_2]['MMR'])[len(list(self.games[team_2]['MMR'])) - 1]
                    
                if print_window:
                    print('x:\t' + str(x) + '\tteam_2:\t' + str(team_2) + '\tteam_1_rank:\t' + str(team_1_rank) + '\tteam_2_rank:\t' + str(team_2_rank))
                guess_result = True if (((team_1_rank >= team_2_rank) and win) or ((team_1_rank <= team_2_rank) and not win)) else False
                record_df['guess_result'] = guess_result
                # print('\nrecord::',record_df,'\n')
                # print('ILOC[0]:', record_df.iloc[0])
                # print('ILOC[1]:', record_df.iloc[1])
                # print('record_df.columns', record_df.columns)
                team_1_consec_wins = record_df['consec_wins'][game_num]
                team_1_consec_losses = record_df['consec_losses'][game_num]
                # print('team_1_score:',team_1_score,'team_2_score',team_2_score)
                # print('team_1_consec_wins:',team_1_consec_wins,'team_1_consec_losses',team_1_consec_losses)
                # print('CONCAT\t', self.games[team_name], '\n\t', record_df, '\n')
                self.games[team_name] = pd.concat([self.games[team_name], record_df], sort=False)#.reset_index()  #[self.game_number]|
                # self.games[team_name].at[team_name, 'num_games'] = x + 1
                return

        if team_name not in self.games.keys():
            # self.game_number += 1
            # if print_more_details:
            print('FIRST ADDITION')
            first_addition = self.first_addition(record_df)
            # first_addition['consec_wins'] = 0
            # first_addition['consec_losses'] = 0
            # record_df.insert(len(record_df.columns), 'num_games', 1)
            record_df['num_games'] = 1
            record_df['MMR'] = self.adjust_mmr(record_df)
            record_df['confidence'] = self.adjust_confidence(record_df)

            game_num = len(record_df['team_1_score']) - 1
            team_1_score = record_df['team_1_score'][game_num]
            team_2_score = record_df['team_2_score'][game_num]
            win = True if team_1_score > team_2_score else False
            record_df['consec_wins'] = 1 if win else 0
            record_df['consec_losses'] = 1 if not win else 0

            team_2 = list(record_df['team_2'])[0]
            print('team_2:\t' + str(team_2) + '\tteam_1_rank:\t' + str(list(record_df['MMR'])))
            team_1_rank = list(record_df['MMR'])[len(record_df['MMR']) - 1]
            if team_2 not in self.games.keys():
                team_2_rank = START_MMR
            else:
                team_2_rank = list(self.games[team_2]['MMR'])[len(list(self.games[team_2]['MMR'])) - 1]

            print('team_2:\t' + str(team_2) + '\tteam_1_rank:\t' + str(
                team_1_rank) + '\tteam_2_rank:\t' + str(team_2_rank))
            guess_result = True if (
                        ((team_1_rank >= team_2_rank) and win) or ((team_1_rank <= team_2_rank) and not win)) else False
            record_df['guess_result'] = guess_result
            # print('\nfirst_addition:', len(list(first_addition.columns)), '\nrecord_df',len(list(record_df.columns)))
            result_df = pd.concat([first_addition, record_df], sort=False)
            # print('result_df:',result_df)
            self.games[team_name] = result_df
            # record = param_record.copy()
            # t = record
            # print('team_name:',team_name, 'record[\'num_games\']', t['num_games'],'type(record):', type(t))
            # print(record.at[team_name, 'num_games'])
            # print('new', team_name)
            # print('\nrecord:: ' + str(record_df) + '\nindex: ' + str(list(record_df.index)) + '\nvalues: ' + str(list(record_df.values)) + '\ncolumns: ' + str(list(record_df.columns)))
            # print(self.games[team_name])#.insert(self.game_number, str(self.game_number), record_df)


    def n_best_ranked_teams(self, n):
        top_list = []
        for team in self.games.keys():
            if len(top_list) < n:
                top_list.append(team)
                if len(top_list) == n:
                    # sorted descending, scan right to left
                    top_list.sort(key=lambda x: self.get_max_MMR(x), reverse=True)
                    if print_details:
                        print('POST_n_best_ranked_SORT:\t' + str(top_list))
                        for t in top_list:
                            print('\tTOP_LIST:\t' + str(t) + ',\t:' + str(self.get_max_MMR(t)))
            else:
                max_team_mmr = self.get_max_MMR(team)
                index = n
                bool = False
                while index > 0 and max_team_mmr > self.get_max_MMR(top_list[index - 1]):
                    bool = True
                    index -= 1
                # shuffle down
                if bool and (-1 < index < n):
                # if team != list(self.games.keys())[len(list(self.games.keys())) - 1]:
                    top_list = top_list[:index] + [team] + top_list[index: len(top_list) - 1]
        print('\n\nTOP MMR TEAMS\n')
        if print_details:
            print('TOP_LIST:' + str(top_list) + '\n\n')
        for top_team in top_list:
            #lst = list(self.games[top_team]['MMR'])
            print('\tteam:\t' + str(top_team) + ', MMR:\t' + str(self.get_max_MMR(top_team)))
        # for team in top_list:
        #     print(self.print_df(self.games[team]))
        return top_list


    def n_worst_ranked_teams(self, n):
        bottom_list = []
        for team in self.games.keys():
            if len(bottom_list) < n:
                bottom_list.append(team)
                if len(bottom_list) == n:
                    bottom_list.sort(key=lambda x: self.get_min_MMR(x))
                    if print_details:
                        print('POST_n_worst_ranked_SORT:\t' + str(bottom_list))
            else:
                min_team_mmr = min(list(self.games[team]['MMR']))
                index = n
                bool = False
                while index > 0 and min_team_mmr < self.get_min_MMR(bottom_list[index - 1]):
                    bool = True
                    index -= 1
                # shuffle down
                if bool and (-1 < index < n):                #)#team != list(self.games.keys())[len(list(self.games.keys())) - 1]:
                    bottom_list = bottom_list[:index] + [team] + bottom_list[index: len(bottom_list) - 1]
        # for top_team in top_list:
        #     lst = list(self.games[top_team]['MMR'])
        #     print('\tteam:\t' + str(top_team) + ', MMR:\t' + str(max(lst)) + '\nLST:\t' + str(lst))
        print('\n\nBOTTOM MMR TEAMS\n')
        if print_details:
            print('BOTTOM_LIST:' + str(bottom_list) + '\n\n')
        for bottom_team in bottom_list:
            #lst = list(self.games[top_team]['MMR'])
            print('\tteam:\t' + str(bottom_team) + ', MMR:\t' + str(self.get_min_MMR(bottom_team)))
        # for team in bottom_list:
        #     print(self.print_df(self.games[team]))
        return bottom_list

    def n_worst_avg_ranked_teams(self, n):
        avg_list = []
        for team in self.games.keys():
            if len(avg_list) < n:
                avg_list.append(team)
                if len(avg_list) == n:
                    avg_list.sort(key=lambda x: self.get_avg_MMR(x))
                    if print_details:
                        print('POST_n_worst_avg_SORT:\t' + str(avg_list))
            else:
                avg_team_mmr = self.get_avg_MMR(team) #sum(list(self.games[team]['MMR'])) / len(list(self.games[team]['MMR']))
                index = n
                bool = False
                while index > 0 and avg_team_mmr < self.get_avg_MMR(avg_list[index - 1]):#"(sum(list(self.games[avg_list[index]]['MMR'])) / len(list(self.games[team]['MMR']))):
                    bool = True
                    index -= 1
                # shuffle down
                if bool and (-1 < index < n):
                # if team != list(self.games.keys())[len(list(self.games.keys())) - 1]:
                    avg_list = avg_list[:index] + [team] + avg_list[index: len(avg_list) - 1]
        # for top_team in top_list:
        #     lst = list(self.games[top_team]['MMR'])
        #     print('\tteam:\t' + str(top_team) + ', MMR:\t' + str(max(lst)) + '\nLST:\t' + str(lst))
        print('\n\nBOTTOM AVERAGE MMR TEAMS\n')
        if print_details:
            print('AVG_LIST:' + str(avg_list) + '\n\n')
        for avg_team in avg_list:
            #lst = list(self.games[top_team]['MMR'])
            print('\tteam:\t' + str(avg_team) + ', MMR:\t' + str(self.get_avg_MMR(avg_team)))
        # for team in avg_list:
        #     print(self.print_df(self.games[team]))
        return avg_list

    def n_best_avg_ranked_teams(self, n):
        avg_list = []
        for team in self.games.keys():
            if len(avg_list) < n:
                avg_list.append(team)
                if len(avg_list) == n:
                    avg_list.sort(key=lambda x: self.get_avg_MMR(x), reverse=True)
                    if print_details:
                        print('POST_n_best_avg_SORT:\t' + str(avg_list))
            else:
                avg_team_mmr = self.get_avg_MMR(team)
                index = n
                bool = False
                while index > 0 and avg_team_mmr > self.get_avg_MMR(avg_list[index - 1]):
                    bool = True
                    index -= 1
                # shuffle down
                if bool and (-1 < index < n):
                # if team != list(self.games.keys())[len(list(self.games.keys())) - 1]:
                    avg_list = avg_list[:index] + [team] + avg_list[index: len(avg_list) - 1]
        # for top_team in top_list:
        #     lst = list(self.games[top_team]['MMR'])
        #     print('\tteam:\t' + str(top_team) + ', MMR:\t' + str(max(lst)) + '\nLST:\t' + str(lst))
        print('\n\nTOP AVERAGE MMR TEAMS\n')
        if print_details:
            print('AVG_LIST:' + str(avg_list) + '\n\n')
        for avg_team in avg_list:
            #lst = list(self.games[top_team]['MMR'])
            print('\tteam:\t' + str(avg_team) + ', MMR:\t' + str(self.get_avg_MMR(avg_team)))
        # for team in avg_list:
        #     print(self.print_df(self.games[team]))
        return avg_list

    # n teams who had the smallest MMR change window
    def n_most_consistent_teams(self, n):
        most_consistent = []
        for team in self.games.keys():
            mmr_change = self.get_mmr_change_window(team)
            if len(most_consistent) < n:
                most_consistent.append(team)
                if len(most_consistent) == n:
                    most_consistent.sort(key=lambda x: self.mmr_diff(self.get_mmr_change_window(x)))
                    if print_details:
                        print('POST_n_most_consistent_SORT:\t' + str(most_consistent))
            else:
                index = n
                bool = False
                while index > 0 and self.mmr_diff(mmr_change) < self.mmr_diff(self.get_mmr_change_window(most_consistent[index - 1])):
                    index -= 1
                    bool = True
                if bool and -1 < index < n:
                    most_consistent = most_consistent[:index] + [team] + most_consistent[index: len(most_consistent) - 1]

        print('\n\nMOST CONSISTENT MMR TEAMS\n')
        if print_details:
            print('CONSISTENT_LIST:' + str(most_consistent) + '\n\n')
        for mc_team in most_consistent:
            #lst = list(self.games[top_team]['MMR'])
            print('\tteam:\t' + str(mc_team) + ', MMR_DIFF:\t' + str(self.mmr_diff(self.get_mmr_change_window(mc_team))))
        return most_consistent

    def n_least_consistent_teams(self, n):
        least_consistent = []
        for team in self.games.keys():
            mmr_change = self.get_mmr_change_window(team)
            if len(least_consistent) < n:
                least_consistent.append(team)
                if len(least_consistent) == n:
                    least_consistent.sort(key=lambda x: self.mmr_diff(self.get_mmr_change_window(x)), reverse=True)
                    if print_details:
                        print('POST_n_least_consistent_SORT:\t' + str(least_consistent))
            else:
                index = n
                bool = False
                while index > 0 and self.mmr_diff(mmr_change) > self.mmr_diff(self.get_mmr_change_window(least_consistent[index - 1])):
                    index -= 1
                    bool = True
                if bool and -1 < index < n:
                    least_consistent = least_consistent[:index] + [team] + least_consistent[index: len(least_consistent) - 1]
        print('\n\nLEAST CONSISTENT MMR TEAMS\n')
        print('CONSISTENT_LIST:' + str(least_consistent) + '\n\n')
        for mc_team in least_consistent:
            # lst = list(self.games[top_team]['MMR'])
            print('\tteam:\t' + str(mc_team) + ', MMR_DIFF:\t' + str(
                self.mmr_diff(self.get_mmr_change_window(mc_team))))
        return least_consistent

    def get_max_MMR(self, team):
        return max(list(self.games[team]['MMR'])[1:])

    def get_min_MMR(self, team):
        return min(list(self.games[team]['MMR'])[1:])

    def get_avg_MMR(self, team):
        return sum(list(self.games[team]['MMR'])[1:]) / (len(list(self.games[team]['MMR'])) - 1)

    def get_mmr_change_window(self, team):
        return (self.get_min_MMR(team), self.get_max_MMR(team))

    def mmr_diff(self, mmr_range):
        return mmr_range[1] - mmr_range[0]


    def swap_stats_team1_team2(self, row):
        # print('SWAPPING')
        # columns = row.columns
        values = list(row.values)
        index = list(row.index) + ['consec_wins', 'consec_losses']
        # print('row',row)
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
        orig_team_1_consec_wins = self.look_up_team_2_consec_wins(orig_team_2) # values[7]
        orig_team_1_consec_losses = self.look_up_team_2_consec_losses(orig_team_2) # values[8]
        new_location = 'away' if orig_location == 'home' else 'home'
        # if orig_result == 'W':
        #     new_result = 'L'
        # elif orig_result == 'W'
        new_result = 'W' if orig_result == 'L' else 'L'
        data = [orig_team_2, orig_team_1, new_location, new_result, orig_date, orig_team_2_score, orig_team_1_score, orig_team_1_consec_wins, orig_team_1_consec_losses]
        # print('data:',data)
        res = pd.Series(data, index = index)#.reset_index()
        # print('swap_res:', res)
        # print('SWAPPED')
        return res

    def adjust_mmr(self, param_record):
        # print('PARAM' + '\ncolumns:\t' + str(list(param_record.columns)) + '\nvalues:\t' + str(list(param_record.values)))
        team_1 = list(param_record['team_1'])[0]
        team_2 = list(param_record['team_2'])[0]
        if team_1 not in self.games.keys():
            print('First Game for the', team_1)
            return START_MMR
        if team_2 not in self.games.keys():
            # print('First Game for team_2', team_2)
            return START_MMR
        team_1_confidence_list = list(self.games[team_1]['confidence'])
        team_1_confidence = team_1_confidence_list[len(team_1_confidence_list) - 1]
        confidence = team_1_confidence
        # mmr_change = sSTART_MMR - 3 * confidence
        x = len(self.games[team_1])
        # print('x:',x)
        if 1 < x < self.min_games_required_for_rank:
            print('The',team_1,'have not yet played at least',self.min_games_required_for_rank,'games, \nand therefore can\'t be ranked confidently [' + str(x) + ' / ' + str(self.min_games_required_for_rank) + ']')
            return START_MMR
        # print('TEST', team_1, '_', team_2)
        # print('GAMES',self.games)
        if print_more_details:
            print('ADJUSTING MMR')
        team_1_rank_list = list(self.games[team_1]['MMR'])
        team_1_rank = team_1_rank_list[len(team_1_rank_list) - 1]
        team_2_rank_list = list(self.games[team_2]['MMR'])
        team_2_rank = team_2_rank_list[len(team_2_rank_list) - 1]
        team_2_confidence_list = list(self.games[team_2]['confidence'])
        team_2_confidence = team_2_confidence_list[len(team_2_confidence_list) - 1]
        mmr_diff_1 = ((2 * START_MMR) - (team_1_rank - team_2_rank))

        team_1_score = list(param_record['team_1_score'])[0]
        team_2_score = list(param_record['team_2_score'])[0]
        win = True if team_1_score > team_2_score else False
        rcwin = ((4 * START_MMR) - mmr_diff_1) / (4 * START_MMR)
        rcloss = 1 - rcwin
        win_rank_window = (team_1_rank - (team_1_confidence * rcwin), team_1_rank + (team_1_confidence * rcwin))
        loss_rank_window = (team_1_rank - (team_1_confidence * rcloss), team_1_rank + (team_1_confidence * rcloss))
        if win:
            estimate_window = (((win_rank_window[0] + win_rank_window[1]) / 2), win_rank_window[1])
        else:
            estimate_window = (loss_rank_window[0], ((loss_rank_window[0] + loss_rank_window[1]) / 2))

        # if win:
        new_rank = min((2 * START_MMR), max(0, round((estimate_window[0] + estimate_window[1]) / 2)))
        if print_window:
            print('\nmmr_delta:\t' + str(mmr_diff_1) + '\nconfd:\t' + str(team_1_confidence) + '\nwin:\t' + ('WIN' if win else 'LOSS') \
            + '\nrcwin:\t' + str(rcwin) + '\nrcloss:\t' + str(rcloss)  \
            + '\nwin_rank_window:\t' + str(win_rank_window) + '\nloss_rank_window:\t' + str(loss_rank_window)\
            + '\nextimate_window:\t' + str(estimate_window) + '\nnew_rank:\t' + str(new_rank))
        return new_rank
        # else:
        #     new_rank =
        #

        # mmr_diff_2 = mmr_diff_1 // 3
        # mmr_diff_3 = mmr_diff_2 // 2
        # # win
        # mmr_diff_win, mmr_diff_loss = team_1_confidence, team_1_confidence
        # mmr_diff_win -= (team_1_confidence - mmr_diff_3) / team_1_confidence
        # # loss
        # mmr_diff_loss += (team_1_confidence - mmr_diff_3) / team_1_confidence
        # # print('PARAM', param_record)
        # game_result = list(param_record['result'])[0]
        # print(team_1 + ':', game_result)
        # rank_range = (max(0, abs(team_1_rank - confidence)), min(50, abs(team_1_rank + confidence)))
        # if game_result == 'W':
        #     # confidence = mmr_diff_win
        #     rank_estimate_unround = ((team_1_rank + rank_range[1]) / 2)
        # elif game_result == 'L':
        #     # confidence = mmr_diff_loss
        #     # rank_range = (team_1_rank - confidence, team_1_rank + confidence)
        #     rank_estimate_unround = ((rank_range[0] + team_1_rank) / 2)
        # rank_estimate = round(rank_estimate_unround)
        #
        #
        # #COMMENTED OUT FOR FASTER RESULTS
        # if print_details:
        #     if print_more_details:
        #         print('team_1_rank', team_1_rank, 'team_2_rank', team_2_rank)
        #         print('team_1_confidence', team_1_confidence, 'team_2_confidence', team_2_confidence)
        #         print('mmr_diff_1:', mmr_diff_1,'mmr_diff_2:', mmr_diff_2,'mmr_diff_3:', mmr_diff_3, 'mmr_change', mmr_change)
        #         print('mmr|_diff_win', mmr_diff_win, 'mmr_diff_loss', mmr_diff_loss)
        #         print('RANK RANGE:', rank_range, 'rank_estimate_unround', rank_estimate_unround, 'rank_estimate', rank_estimate)
        #
        #
        # mmr_change = self.START_MMR
        # # print('MMR ADJUSTED')
        # return rank_estimate

    def adjust_confidence(self, param_record):
        # print('\n\nCOLUMNS' + str(list(param_record.columns)))
        team_1 = list(param_record['team_1'])[0]
        team_2 = list(param_record['team_2'])[0]
        if team_1 not in self.games.keys():
            # print('First Game for the', team_1)
            return START_CONFIDENCE
        if team_2 not in self.games.keys():
            # print('First Game for team_2', team_2)
            return START_CONFIDENCE
        x = len(self.games[team_1])
        # print('x:',x)
        if x < self.min_games_required_for_rank:
            print('The',team_1,'have not yet played at least',self.min_games_required_for_rank,'games, \nand therefore can\'t be ranked confidently [' + str(x) + ' / ' + str(self.min_games_required_for_rank) + ']')
            return START_CONFIDENCE
        if print_more_details:
            print('ADJUSTING CONFIDENCE')
        # confidence = list(param_record['confidence'])[x - 1]
        # print('games', self.games)
        team_1_rank_list = list(self.games[team_1]['MMR'])
        team_1_rank = team_1_rank_list[len(team_1_rank_list) - 1]
        team_2_rank_list = list(self.games[team_2]['MMR'])
        team_2_rank = team_2_rank_list[len(team_2_rank_list) - 1]
        team_1_confidence_list = list(self.games[team_1]['confidence'])
        team_1_confidence = team_1_confidence_list[len(team_1_confidence_list) - 1]
        team_2_confidence_list = list(self.games[team_2]['confidence'])
        team_2_confidence = team_2_confidence_list[len(team_2_confidence_list) - 1]
        mmr_diff_1 = (50 - (team_1_rank - team_2_rank))

        team_1_score = list(param_record['team_1_score'])[0]
        team_2_score = list(param_record['team_2_score'])[0]
        win = True if team_1_score > team_2_score else False
        confidence_delta = START_CONFIDENCE - (team_1_confidence - team_2_confidence)
        win_confidence_delta_coefficient = ((2 * START_CONFIDENCE) - confidence_delta) / (2 * START_CONFIDENCE)
        loss_confidence_delta_coefficient = 1 - win_confidence_delta_coefficient

        # res_confidence = team_1_confidence
        win_conf_window = (team_1_confidence, team_1_confidence - (team_1_confidence * win_confidence_delta_coefficient))
        loss_conf_window = (team_1_confidence - (team_1_confidence * loss_confidence_delta_coefficient), team_1_confidence)
        if win:
            confidence_estimate = ((win_conf_window[0] + win_conf_window[1]) / 2) * win_confidence_delta_coefficient
            confidence_estimate *= (win_confidence_delta_coefficient ** 2)# / 2) ** 2)
        else:
            confidence_estimate = ((loss_conf_window[0] + loss_conf_window[1]) / 2) * loss_confidence_delta_coefficient
            confidence_estimate *= (loss_confidence_delta_coefficient ** 2)# / 2) ** 2)

        # print()
        if print_window:
            print('confidence:\t' + str(confidence_estimate))
        confidence_estimate = team_1_confidence - confidence_estimate
        # print('confidence:\t' + str(confidence_estimate))
        confidence_estimate = max(0, min(START_CONFIDENCE, confidence_estimate))
        if print_window:
            print('confidence:\t' + str(confidence_estimate))
            
            print('\nmmr_delta:\t' + str(mmr_diff_1) + '\nconfd:\t' + str(team_1_confidence) + '\nconfdelta:\t' \
            + str(confidence_delta) + '\nwin:\t' + ('WIN' if win else 'LOSS') \
            + '\nwin_confidence_delta_coefficient:\t' + str(win_confidence_delta_coefficient) \
            + '\nloss_confidence_delta_coefficient:\t' + str(loss_confidence_delta_coefficient)#  \
            + '\nwin_conf_window:\t' + str(win_conf_window) + '\nloss_conf_window:\t' + str(loss_conf_window)\
            + '\nconfidence_estimate:\t' + str(confidence_estimate)
            + '\n\n')

        return confidence_estimate



        # mmr_diff_2 = mmr_diff_1 // 3
        # mmr_diff_3 = mmr_diff_2 // 2
        # # win
        # mmr_diff_win, mmr_diff_loss = team_1_confidence, team_1_confidence
        # mmr_diff_win -= (team_1_confidence - mmr_diff_3) / team_1_confidence
        # # loss
        # mmr_diff_loss -= (team_1_confidence - mmr_diff_3) / team_1_confidence
        # # print('PARAM', param_record)
        #
        # #COMMENTED OUT FOR FASTER RESULTS
        # if print_details:
        #     if print_more_details:
        #         print('team_1_rank', team_1_rank, 'team_2_rank', team_2_rank)
        #         print('team_1_confidence', team_1_confidence, 'team_2_confidence', team_2_confidence)
        #         print('mmr_diff_1:', mmr_diff_1,'mmr_diff_2:', mmr_diff_2,'mmr_diff_3:', mmr_diff_3)
        #         print('mmr|_diff_win', mmr_diff_win, 'mmr_diff_loss', mmr_diff_loss)
        #         print('team_1', team_1, 'team_2', team_2)
        #
        #
        # # print('param_record[\'result\']', param_record['result'])
        # game_result = list(param_record['result'])[0]
        # if game_result == 'W':
        #     confidence = mmr_diff_win
        # elif game_result == 'L':
        #     confidence = mmr_diff_loss
        # # confidence = mmr_diff_win
        # # print('CONFIDENCE ADJUSTED')
        # return confidence

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
        df_dict = {'team_1': [team_1],
                   'team_2': [team_2],
                   'location': [location],
                   'date': [date],
                   'result': [result],
                   'team_1_score': [team_1_score],
                   'team_2_score': [team_2_score],
                   'num_games': [0],
                   'MMR': [START_MMR],
                   'confidence': [START_CONFIDENCE],
                   'consec_wins': 'NaN',
                   'consec_losses': 'NaN',
                   'guess_result': 'NaN'}
        df_dict_order_assert = {}
        columns = ['team_1','team_2','location','result','date','team_1_score','team_2_score','consec_wins','consec_losses','MMR','confidence', 'guess_result']
        for col in columns:
            df_dict_order_assert[col] = df_dict[col]

        # print('df_dict',df_dict)
        # print('type(df_dict)',type(df_dict))
        # if print_more_details:
        # for key, val in df_dict_order_assert.items():
        #     print('key:',key,'val:', val)
        df = pd.DataFrame(df_dict_order_assert)
        # print('first addititon cols:', list(df.columns))
        # print('df.head()',df.head())
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
        # print('team_1:', team_1_temp, 'team_2:', team_2_temp)
        team_cities = [team[0] if len(team) == 2 else team[0] if team[1] in special_team_names else team[0] + ' ' + team[1] for team in team_cities_split]
        # print(team_cities)
        return True if team_1_temp in team_cities and team_2_temp in team_cities else False

    def look_up_team_2_consec_wins(self, orig_team_2):
        teams = list(self.games.keys())
        if orig_team_2 not in teams:
            return 0
        else:
            game_num = len(list(self.games[orig_team_2]['consec_wins'])) - 1
            return list(self.games[orig_team_2]['consec_wins'])[game_num]

    def look_up_team_2_consec_losses(self, orig_team_2):
        teams = list(self.games.keys())
        if orig_team_2 not in teams:
            return 0
        else:
            game_num = len(list(self.games[orig_team_2]['consec_losses'])) - 1
            return list(self.games[orig_team_2]['consec_losses'])[game_num]

    def showify_predictions_list(self, predictions):
        string_res = ''
        for team in predictions.keys():
            lst = predictions[team]
            n_trues = 0
            n_falses = 0
            n_vals = len(lst) - 1
            for val in lst:
                if lst.index(val) != 0:
                    if val:
                        n_trues += 1
                    else:
                        n_falses += 1
            # + ' = ' + str(n_trues / n_vals) +\
            # + ' = ' + str(n_falses / n_vals) +\
            string_res += ('team:\t' + str(team) +\
                          '\t\tcorrect_guesses:\t[' +\
                          str(n_trues) + ' / ' + str(n_vals) +\
                          ']\twrong_guesses:\t[' +\
                          str(n_falses) + ' / ' + str(n_vals) +\
                          ']\tPercent correct:\t[' +\
                          str(float(float(n_trues) / float(n_vals))) + ']\t' +\
                           ('GOOD' if (float(float(n_trues) / float(n_vals)) >= 0.5) else 'BAD') + '\n')
        return string_res



def adjust_regular_season_dataframe(orig_frame):
    global games_answers
    games_answers = False
    # need to change the indexes that are used to determine the values
    orig_frame_columns = list(orig_frame.columns)
    columns = ['team_1','team_2','location','result','date','team_1_score','team_2_score']
    columns_str = ''
    for col in columns:
        if columns.index(col) == len(columns) - 1:
            columns_str += col
        else:
            columns_str += col + ','
    df = pd.DataFrame()
    list_of_games = list(orig_frame.values)
    game_list = []
    # game_num = 0
    # game_num_str = 'game#'
    for game in list_of_games:
        temp_dict = {}
        temp_dict['date'] = game[0]
        if game[3] == 'St. Louis Blues':
            temp_dict['team_1'] = 'St Louis Blues'
        else:
            temp_dict['team_1'] = game[3]

        if game[1] == 'St. Louis Blues':
            temp_dict['team_2'] = 'St Louis Blues'
        else:
            temp_dict['team_2'] = game[1]
        # temp_dict['team_2'] = game[1]
        temp_dict['team_1_score'] = game[4]
        temp_dict['team_2_score'] = game[2]
        extra_result = game[5]
        if type(extra_result) != str:
            temp_dict['attendance_thousands'] = game[5]
            temp_dict['attendance_ones'] = game[6]
            temp_dict['log'] = game[7]
            temp_dict['notes'] = game[8]

        else:
            temp_dict['attendance_thousands'] = game[6]
            temp_dict['attendance_ones'] = game[7]
            temp_dict['log'] = game[8]
            temp_dict['notes'] = game[9]

        # print(temp_dict)

        temp_dict['location'] = get_location(temp_dict['team_1'])
        # location_prefixes = ['New', 'Tampa', 'St', 'San', 'Los']
        # two_name_mascots = ['Vegas', 'Columbus', 'Toronto', 'Detroit']
        # home_team = temp_dict['team_1']
        # location = home_team.split(' ')
        # if len(location) == 3:
        #     if location[0] == 'St.':
        #         location[0] = 'St'
        #     if location[0] in location_prefixes:
        #         temp_dict['location'] = location[0] + ' ' + location[1]
        #     if location[0] in two_name_mascots:
        #         temp_dict['location'] = location[0]
        # else:
        #     temp_dict['location'] = location[0]

        if temp_dict['team_1_score'] > temp_dict['team_2_score']:
            temp_dict['result'] = 'W'
        elif temp_dict['team_1_score'] < temp_dict['team_2_score']:
            temp_dict['result'] = 'L'
        game_list.append(temp_dict)
        # location = get_location(home_team)
        # print('attendance_thousands:', attendance_thousands, 'attendance_ones', attendance_ones)
        # print('type(attendance_thousands):', type(attendance_thousands), 'type(attendance_ones)', type(attendance_ones))
        # attendance = attendance_thousands * 1000 + attendance_ones
        attendance = 'ATTENDANCE'

        # print('\nhome_team:',home_team,'away_team:',away_team,'home_score:',home_score,'away_score:',away_score,'location:',location,'attendance:',attendance, 'extra_result:',extra_result,'log:', log, 'notes', notes)

        # print('values', game.values)
        # print('index', game.index)
        # print('game',game)
        # for col in list(game):
        #     print('type(col)',type(col),'col', col)
    #game_list is populated with to much data, need to trim
    #columns = ['team_1','team_2','location','result','date','team_1_score','team_2_score']
    game_csv = columns_str + '\n'
    for game in game_list:
        for col_title in columns:
            if col_title == 'location':
                # team_name = game['team_1']
                # location_name = get_location(game[col_title])
                # find_index = team_name.find(location_name)
                # print('team_name',team_name,'location_name:', location_name,'find_index', find_index)
                # if find_index >= 0:
                #     location = 'home'
                # else:
                #     location = 'away'
                # game_csv += location + ','
                game_csv += 'home,'
            elif col_title == 'team_2_score':
                game_csv += str(game[col_title])
            else:
                game_csv += str(game[col_title]) + ','
        game_csv += '\n'
    # print(game_csv)
    # return orig_frame
    file = 'regular_season_2018_2019_adjusted.csv'
    f = open(file, 'w')
    f.write(game_csv)  # Give your csv text here.
    ## Python will convert \n to os.linesep
    f.close()
    df = pd.read_csv(file)
    return df

def get_location(team):
    location_prefixes = ['New', 'Tampa', 'St', 'San', 'Los']
    two_name_mascots = ['Vegas', 'Columbus', 'Toronto', 'Detroit']
    # home_team = temp_dict['team_1']
    location = team.split(' ')
    if len(location) == 3:
        if location[0] == 'St.':
            # print('st LOUIS')
            location = 'St Louis'
        elif location[0] in location_prefixes:
            location = location[0] + ' ' + location[1]
        elif location[0] in two_name_mascots:
            location = location[0]
    else:
        location = location[0]
    return location

def read_games_file():
    global games_answers
    games_answers = True
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
# print(games_file.columns)
# print(games_file.head())
# for col in list(games_file.columns):
#     print('col:', col, '_', games_file.iloc[0][col])
# print()
# for col in list(games_file.columns):
#     print('col:', col, '_', games_file.iloc[8][col])
rank_sim_regular_season = RankingSim()
rank_sim_regular_season.populate_games_dict(games_file)

print('-----------------------------------------------------------------------------')

if print_details:
    # print(rank_sim_regular_season.games)
    for record in rank_sim_regular_season.games.keys():
        # print("\trecord:\t", record)
        for record_col in rank_sim_regular_season.games[record].keys():
            game_num = len(list(rank_sim_regular_season.games[record][record_col])) - 1
            # print("\t\trecord_col:\t", record_col,'val:',list(rank_sim_regular_season.games[record][record_col])[game_num])#[game_num])


        # for game in rank_sim_regular_season.games[record]:
        #     print(rank_sim_regular_season.games[record])
        #     print('\n')
        # print('\nRECORD\n', rank_sim_regular_season.games[record])
        # print('\nRECORD ', rank_sim_regular_season.games[record][0]['team_1'], '\n', rank_sim_regular_season.games[record])
        # print('\nRECORD ', rank_sim_regular_season.games[record][0]['team_1'], '\n')
# print('\n\tSORTED\n' + str(rank_sim_regular_season.games.sort_values(by=['MMR'])))
print('\n\tSORTED\n')
print(rank_sim_regular_season)
n_teams = 5
best_teams_list = rank_sim_regular_season.n_best_ranked_teams(n_teams)
worst_teams_list = rank_sim_regular_season.n_worst_ranked_teams(n_teams)
best_avg_teams_list = rank_sim_regular_season.n_best_avg_ranked_teams(n_teams)
worst_avg_teams_list = rank_sim_regular_season.n_worst_avg_ranked_teams(n_teams)
most_consistent_teams_list = rank_sim_regular_season.n_most_consistent_teams(n_teams)
least_consistent_teams_list = rank_sim_regular_season.n_least_consistent_teams(n_teams)

# for team in rank_sim_regular_season.games.keys():
#     print('\n\tTeam:\t' + str(team))
#     df = rank_sim_regular_season.games[team]  #pd.DataFrame(
#     print(df)
#.sort_values(by=['MMR']))
best_teams_list_answer_reg_season = ['San Jose Sharks', 'Montreal Canadiens', 'Vegas Golden Knights', 'New York Islanders', 'Toronto Maple Leafs']
worst_teams_list_answer_reg_season = ['Detroit Red Wings', 'Arizona Coyotes', 'Chicago Blackhawks', 'Ottawa Senators', 'Toronto Maple Leafs']
best_avg_teams_list_answer_reg_season = ['Nashville Predators', 'Tampa Bay Lightning', 'Toronto Maple Leafs', 'Calgary Flames', 'New York Islanders']
worst_avg_teams_list_answer_reg_season = ['Anaheim Ducks', 'Ottawa Senators', 'Pittsburgh Penguins', 'Dallas Stars', 'Toronto Maple Leafs']
most_consistent_teams_list_answer_reg_season = []
least_consistent_teams_list_answer_reg_season = []

best_teams_list_answer_games = ['Florida Panthers', 'Calgary Flames', 'Winnipeg Jets', 'Washington Capitals', 'Los Angeles Kings']
worst_teams_list_answer_games = ['Edmonton Oilers', 'Boston Bruins', 'San Jose Sharks', 'Toronto Maple Leafs', 'Detroit Red Wings']
best_avg_teams_list_answer_games = ['Florida Panthers', 'Calgary Flames', 'Winnipeg Jets', 'Washington Capitals', 'Los Angeles Kings']
worst_avg_teams_list_answer_games = ['Edmonton Oilers', 'Boston Bruins', 'San Jose Sharks', 'Toronto Maple Leafs', 'Detroit Red Wings']
most_consistent_teams_list_answer_games = ['Pittsburgh Penguins', 'New York Islanders', 'Carolina Hurricanes', 'Tampa Bay Lightning', 'Detroit Red Wings']
least_consistent_teams_list_answer_games = ['Edmonton Oilers', 'Boston Bruins', 'Florida Panthers', 'Calgary Flames', 'San Jose Sharks']

if games_answers:
    stats_results = [best_teams_list_answer_games,
                     worst_teams_list_answer_games,
                     best_avg_teams_list_answer_games,
                     worst_avg_teams_list_answer_games,
                     most_consistent_teams_list_answer_games,
                     least_consistent_teams_list_answer_games]
else:
    stats_results = [best_teams_list_answer_reg_season,
                     worst_teams_list_answer_reg_season,
                     best_avg_teams_list_answer_reg_season,
                     worst_avg_teams_list_answer_reg_season,
                     most_consistent_teams_list_answer_reg_season,
                     least_consistent_teams_list_answer_reg_season]

print('\nbest_team_check:\n\tANS\t\t' + str(stats_results[0]) + '\n\t\t\t==\n\tGUESS\t' + str(best_teams_list) + '\n\tRES:\t' + str(best_teams_list == stats_results[0]))
print('\nworst_team_check:\n\tANS\t\t' + str(stats_results[1]) + '\n\t\t\t==\n\tGUESS\t' + str(worst_teams_list) + '\n\tRES:\t' + str(worst_teams_list == stats_results[1]))
print('\nbest_avg_team_check:\n\tANS\t\t' + str(stats_results[2]) + '\n\t\t\t==\n\tGUESS\t' + str(best_avg_teams_list) + '\n\tRES:\t' + str(best_avg_teams_list == stats_results[2]))
print('\nworst_avg_team_check:\n\tANS\t\t' + str(stats_results[3]) + '\n\t\t\t==\n\tGUESS\t' + str(worst_avg_teams_list) + '\n\tRES:\t' + str(worst_avg_teams_list == stats_results[3]))
print('\nmost_consistent_team_check:\n\tANS\t\t' + str(stats_results[4]) + '\n\t\t\t==\n\tGUESS\t' + str(most_consistent_teams_list) + '\n\tRES:\t' + str(most_consistent_teams_list == stats_results[4]))
print('\nleast_consistent_team_check:\n\tANS\t\t' + str(stats_results[5]) + '\n\t\t\t==\n\tGUESS\t' + str(least_consistent_teams_list) + '\n\tRES:\t' + str(least_consistent_teams_list == stats_results[5]))

