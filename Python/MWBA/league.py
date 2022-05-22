import datetime
from team import Team
from dataclasses import dataclass


@dataclass
class League:
    name: str
    sport: str
    start_date: datetime.datetime
    teams: set  # {teams}
    games: dict  # {founded year: [games]}

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
class RoundRobinLeague(League):
    name: str
    sport: str
    start_date: datetime.datetime
    teams: set  # {teams}
    games: dict  # {date: [games]}
    number_round_robins: int

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

    def total_games_rr(self):
        n_teams = len(self.teams) - 1
        # ab ac ad ae af
        #    bc bd be bf
        #       cd ce cf
        #          de df
        #             ef
        return self.number_round_robins * (((n_teams * (n_teams + 1))) // 2)
