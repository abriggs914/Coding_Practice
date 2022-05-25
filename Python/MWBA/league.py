import dataclasses
import datetime

from typing import Dict, Set

from team import Team
from dataclasses import dataclass


@dataclass
class League:
    name: str
    sport: str
    start_date: datetime.datetime
    teams: Set[Team] = dataclasses.field(default_factory=set)  # {teams}
    games: Dict[datetime.datetime, list] = dataclasses.field(default_factory=list)  # {founded year: [games]}
    points_for_win: int = 2

    @dataclass
    class Game:
        date: datetime.datetime
        team_1: Team
        team_2: Team
        score_team_1: int
        score_team_2: int

        def winner(self):
            return (self.team_1, self.score_team_1) if self.score_team_1 > self.score_team_2 else (self.team_2, self.score_team_2)

        def loser(self):
            return (self.team_2, self.score_team_2) if self.score_team_1 > self.score_team_2 else (self.team_1, self.score_team_1)

    @dataclass
    class Record:
        team: Team
        start_date: datetime.datetime
        end_date: datetime.datetime
        wins: int = 0
        losses: int = 0
        games_played: int = 0
        points_for: int = 0
        points_against: int = 0
        points_for_home: int = 0
        points_against_home: int = 0
        points_for_away: int = 0
        points_against_away: int = 0

    def assert_is_team(self, team, msg="League.assert_is_team"):
        assert isinstance(team, Team), msg

    def assert_team_is_known(self, team, msg="League.assert_team_is_known"):
        assert team in self.teams, msg

    def home_record(self, team_1, team_2=None, start_date=None, end_date=None):
        self.assert_is_team(team_1, msg=f"Param 'team_1' must be a Team object got: {type(team_1)}")
        self.assert_team_is_known(team_1, msg=f"Param team_1 '{team_1.name}' not found in this league.")
        if team_2 is not None:
            self.assert_is_team(team_2, msg=f"Param 'team_2' must be a Team object got: {type(team_2)}")
            self.assert_team_is_known(team_2, msg=f"Param team_2 '{team_2.name}' not found in this league.")
        result = {
            "home": {
                "w": 0,
                "l": 0,
                "gp": 0,
                "pf": 0,
                "pa": 0
            }
        }
        for date, games_lst in self.games.items():
            for game in games_lst:
                winner_team, winner_score = game.winner()
                loser_team, loser_score = game.loser()
                if team_1 == game.team_1:
                    # home team
                    # result["overall"]["gp"] += f"||1"
                    if team_2 is None or team_2 == game.team_2:
                        result["home"]["gp"] += 1
                        result['home']['pf'] += game.score_team_1
                        result['home']['pa'] += game.score_team_2
                # elif team_1 == game.team_2:
                #     result["overall"]["gp"] += 1
                #     if team_2 is None or team_2 == game.team_1:
                #         result['overall']['pf'] += game.score_team_2
                #         result['overall']['pa'] += game.score_team_1

                        if winner_team == team_1:
                            result["home"]["w"] += 1
                        elif loser_team == team_1:
                            result["home"]["l"] += 1
        return result
        # self.assert_is_team(team_1, msg=f"Param 'team_1' must be a Team object got: {type(team_1)}")
        # self.assert_is_team(team_2, msg=f"Param 'team_2' must be a Team object got: {type(team_2)}")
        # self.assert_team_is_known(team_1, msg=f"Param team_1 '{team_1.name}' not found in this league.")
        # self.assert_team_is_known(team_2, msg=f"Param team_2 '{team_2.name}' not found in this league.")
        # team_1_games = team_1.games
        # result = {
        #     "home": {
        #         "w": 0,
        #         "l": 0,
        #         "gp": 0,
        #         "pf": 0,
        #         "pa": 0
        #     }
        # }
        # # print(f"Games: {self.games}")
        # for date, games_lst in self.games.items():
        #     for game in games_lst:
        #         if game.team_1 == team_1 and game.team_2 == team_2:
        #             if game.winner()[0] == team_1:
        #                 result["home"]["w"] += 1
        #             else:
        #                 result["home"]["l"] += 1
        #             result["home"]["gp"] += 1
        #             result["home"]["pf"] += game.score_team_1
        #             result["home"]["pa"] += game.score_team_2
        # return result

    def away_record(self, team_1, team_2=None):
        self.assert_is_team(team_1, msg=f"Param 'team_1' must be a Team object got: {type(team_1)}")
        self.assert_team_is_known(team_1, msg=f"Param team_1 '{team_1.name}' not found in this league.")
        if team_2 is not None:
            self.assert_is_team(team_2, msg=f"Param 'team_2' must be a Team object got: {type(team_2)}")
            self.assert_team_is_known(team_2, msg=f"Param team_2 '{team_2.name}' not found in this league.")
        result = {
            "away": {
                "w": 0,
                "l": 0,
                "gp": 0,
                "pf": 0,
                "pa": 0
            }
        }
        for date, games_lst in self.games.items():
            for game in games_lst:
                winner_team, winner_score = game.winner()
                loser_team, loser_score = game.loser()
                # if team_1 == game.team_1:
                #     # home team
                #     result["overall"]["gp"] += 1
                #     # result["overall"]["gp"] += f"||1"
                #     if team_2 is None or team_2 == game.team_2:
                #         result['overall']['pf'] += game.score_team_1
                #         result['overall']['pa'] += game.score_team_2
                if team_1 == game.team_2:
                    if team_2 is None or team_2 == game.team_1:
                        result["away"]["gp"] += 1
                        result['away']['pf'] += game.score_team_2
                        result['away']['pa'] += game.score_team_1

                        if winner_team == team_1:
                            result["away"]["w"] += 1
                        elif loser_team == team_1:
                            result["away"]["l"] += 1
        return result
        # self.assert_is_team(team_1, msg=f"Param 'team_1' must be a Team object got: {type(team_1)}")
        # self.assert_is_team(team_2, msg=f"Param 'team_2' must be a Team object got: {type(team_2)}")
        # self.assert_team_is_known(team_1, msg=f"Param team_1 '{team_1.name}' not found in this league.")
        # self.assert_team_is_known(team_2, msg=f"Param team_2 '{team_2.name}' not found in this league.")
        # team_1_games = team_1.games
        # result = {
        #     "away": {
        #         "w": 0,
        #         "l": 0,
        #         "gp": 0,
        #         "pf": 0,
        #         "pa": 0
        #     }
        # }
        # # print(f"Games: {self.games}")
        # for date, games_lst in self.games.items():
        #     for game in games_lst:
        #         if game.team_2 == team_1 and game.team_1 == team_2:
        #             if game.winner()[0] == team_1:
        #                 result["away"]["w"] += 1
        #             else:
        #                 result["away"]["l"] += 1
        #             result["away"]["gp"] += 1
        #             result["away"]["pf"] += game.score_team_1
        #             result["away"]["pa"] += game.score_team_2
        # return result

    def overall_record(self, team_1, team_2=None):
        self.assert_is_team(team_1, msg=f"Param 'team_1' must be a Team object got: {type(team_1)}")
        self.assert_team_is_known(team_1, msg=f"Param team_1 '{team_1.name}' not found in this league.")
        if team_2 is not None:
            self.assert_is_team(team_2, msg=f"Param 'team_2' must be a Team object got: {type(team_2)}")
            self.assert_team_is_known(team_2, msg=f"Param team_2 '{team_2.name}' not found in this league.")
        result = {
            "overall": {
                "w": 0,
                "l": 0,
                "gp": 0,
                "pf": 0,
                "pa": 0
            }
        }
        for date, games_lst in self.games.items():
            for game in games_lst:
                winner_team, winner_score = game.winner()
                loser_team, loser_score = game.loser()
                x = result["overall"]["gp"]
                if team_1 == game.team_1:
                    # home team
                    # result["overall"]["gp"] += f"||1"
                    if team_2 is None or team_2 == game.team_2:
                        result["overall"]["gp"] += 1
                        result['overall']['pf'] += game.score_team_1
                        result['overall']['pa'] += game.score_team_2
                elif team_1 == game.team_2:
                    if team_2 is None or team_2 == game.team_1:
                        result["overall"]["gp"] += 1
                        result['overall']['pf'] += game.score_team_2
                        result['overall']['pa'] += game.score_team_1
                if x != result["overall"]["gp"]:
                    if winner_team == team_1:
                        result["overall"]["w"] += 1
                    elif loser_team == team_1:
                        result["overall"]["l"] += 1
        return result

    def record(self, team_1, team_2):
        self.assert_is_team(team_1, msg=f"Param 'team_1' must be a Team object got: {type(team_1)}")
        self.assert_is_team(team_2, msg=f"Param 'team_2' must be a Team object got: {type(team_2)}")
        self.assert_team_is_known(team_1, msg=f"Param team_1 '{team_1.name}' not found in this league.")
        self.assert_team_is_known(team_2, msg=f"Param team_2 '{team_2.name}' not found in this league.")
        # Hw, Hl, Hgp || Tw, Tl, Tgp || Tw, Tl, Tgp
        return

    def record_fmt(self, w, l, gp=None):
        gp = w + l if gp is None else gp
        return f"{w}-{l}||{gp}"


@dataclass
class RoundRobinLeague(League):
    name: str
    sport: str
    start_date: datetime.datetime
    teams: Set[Team] = dataclasses.field(default_factory=set)  # {teams}
    games: Dict[datetime.datetime, list] = dataclasses.field(default_factory=list)  # {founded year: [games]}
    points_for_win: int = 2
    number_round_robins: int = 1

    def add_game(self, date, team_1, team_2, score_team_1, score_team_2):
        assert isinstance(date, datetime.datetime)
        assert isinstance(team_1, Team)
        assert isinstance(team_2, Team)
        assert isinstance(score_team_1, int) and score_team_1 > -1
        assert isinstance(score_team_2, int) and score_team_2 > -1

        if date not in self.games:
            self.games[date] = []
        self.games[date].append(self.Game(date, team_1, team_2, score_team_1, score_team_2))

        if team_1 not in self.teams:
            self.teams.add(team_1)

        if team_2 not in self.teams:
            self.teams.add(team_2)

        team_1.add_game(date, team_2, score_team_1, score_team_2, self.points_for_win)
        team_2.add_game(date, team_1, score_team_2, score_team_1, self.points_for_win)

    def total_games_rr(self):
        n_teams = len(self.teams) - 1
        # ab ac ad ae af
        #    bc bd be bf
        #       cd ce cf
        #          de df
        #             ef
        return self.number_round_robins * (((n_teams * (n_teams + 1))) // 2)

    def total_points_scored(self):
        return sum([team.points_for for team in self.teams])
