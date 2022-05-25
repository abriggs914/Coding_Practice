import datetime
from dataclasses import dataclass


@dataclass
class Team:
    id_no: int
    name: str
    city: str
    province: str
    _games_played: int
    _points: int
    _points_for: int
    _points_against: int

    _avg_pf: float
    _avg_pa: float

    _last_10: str
    _record: str
    games: dict  # date: [(pf, team, teamPts)]

    def get_gp(self):
        return self._games_played

    def get_pts(self):
        return self._points

    def get_pf(self):
        return self._points_for

    def get_pa(self):
        return self._points_against

    def get_avg_pf(self):
        return self.points_for / (1 if self._games_played == 0 else self._games_played)

    def get_avg_pa(self):
        return self.points_against / (1 if self._games_played == 0 else self._games_played)

    def get_last10(self):
        # print(f"games: {self.games}")
        last_10 = [(key, value) for key, value in self.games.items()]
        last_10.sort(key=lambda tup: tup[0], reverse=True)
        last_10 = last_10[:10]
        res = None
        n_wins, n_losses = 0, 0
        if last_10:
            for date, games_dat in last_10:
                for game_dat in games_dat:
                    pf, team, pa = game_dat
                    if pf > pa:
                        n_wins += 1
                    else:
                        n_losses += 1
                    if n_wins + n_losses >= 10:
                        break
                if n_wins + n_losses >= 10:
                    break
            res = f"{n_wins}-{n_losses}||{n_wins + n_losses}"
        return res

    def get_record(self):
        # print(f"games: {self.games}")
        last_10 = [(key, value) for key, value in self.games.items()]
        last_10.sort(key=lambda tup: tup[0], reverse=True)
        res = None
        n_wins, n_losses = 0, 0
        if last_10:
            for date, games_dat in last_10:
                for game_dat in games_dat:
                    pf, team, pa = game_dat
                    if pf > pa:
                        n_wins += 1
                    else:
                        n_losses += 1
            # res = f"{n_wins}-{n_losses}||{n_wins + n_losses}"
        # return self.record_fmt(n_wins, n_losses)
        return n_wins, n_losses
        # return res

    def set_gp(self, value):
        self._games_played = value

    def set_pts(self, value):
        self._points = value

    def set_pf(self, value):
        self._points_for = value

    def set_pa(self, value):
        self._points_against = value

    def set_avg_pf(self, value):
        self._avg_pf = value

    def set_avg_pa(self, value):
        self._avg_pa = value

    def set_last10(self, value):
        self._last_10 = value

    def set_record(self, value):
        self._record = value

    def add_game(self, date, against, points_for, points_against, points_for_win):
        assert isinstance(date, datetime.datetime)
        assert isinstance(against, Team)
        assert isinstance(points_for, int)
        assert isinstance(points_against, int)
        assert isinstance(points_for_win, int)
        self.games_played += 1
        self.points += points_for_win if points_for > points_against else 0
        self.points_for += points_for
        self.points_against += points_against
        self.avg_pf = self.avg_pf
        self.avg_pa = self.avg_pa
        if date not in self.games:
            self.games[date] = []
        self.games[date].append((points_for, against, points_against))
        self.last_10 = self.last_10
        self.record = self.record

    def del_gp(self):
        del self._games_played

    def del_pts(self):
        del self._points

    def del_pf(self):
        del self._points_for

    def del_pa(self):
        del self._points_against

    def del_avg_pf(self):
        del self._avg_pf

    def del_avg_pa(self):
        del self._avg_pa

    def del_last10(self):
        del self._last_10

    def del_record(self):
        del self._record

    def __hash__(self):
        return self.id_no
        # return f"({self.name}||{self.city}||{self.province})"

    games_played = property(get_gp, set_gp, del_gp)
    points = property(get_pts, set_pts, del_pts)
    points_for = property(get_pf, set_pf, del_pf)
    points_against = property(get_pa, set_pa, del_pa)

    avg_pf = property(get_avg_pf, set_avg_pf, del_avg_pf)
    avg_pa = property(get_avg_pa, set_avg_pa, del_avg_pa)

    last_10 = property(get_last10, set_last10, del_last10)
    record = property(get_record, set_record, del_record)
    # games: dict  # date: [(pf, team, teamPts)]
