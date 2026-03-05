import enum
import datetime
import pandas as pd

from objects.game import NHLGame, NHLGameDate
from resources.resource import DATE_FMT, NHL_ASSET_API_URL


class NHLScoreboard:
    def __init__(self, sc_data: dict | pd.Series):
        print("NHLScoreboard")
        self.sc_data: dict = sc_data if isinstance(sc_data, dict) else sc_data.to_dict()
        self.focusedDate: datetime.date = self.sc_data.get("focusedDate")
        self.focusedDateCount: int = sc_data.get("focusedDateCount", 0)
        self.game_dates: dict[datetime.date: list[NHLGame]] = {}
        for date_g_data in self.sc_data.get("gamesByDate", []):
            date = date_g_data.get("date")
            for g_data in date_g_data.get("games", []):
                if date not in self.game_dates:
                    self.game_dates[date] = []
                # for data in g_data:
                #     print(f"{date=}, {data=}")
                self.game_dates[date].append(NHLGame(g_data))


class NHLSchedule:
    def __init__(self, sc_data: dict | pd.Series):
        self.sc_data: dict = sc_data if isinstance(sc_data, dict) else sc_data.to_dict()

        self.next_start_date: str = self.sc_data.get("nextStartDate")
        self.next_start_date: datetime.date = datetime.datetime.strptime(self.next_start_date, DATE_FMT).date() if self.next_start_date else None

        self.previous_start_date: str = self.sc_data.get("previousStartDate")
        self.previous_start_date: datetime.date = datetime.datetime.strptime(self.previous_start_date, DATE_FMT).date() if self.next_start_date else None

        self.pre_season_start_date: str = self.sc_data.get("preSeasonStartDate")
        self.pre_season_start_date: datetime.date = datetime.datetime.strptime(self.pre_season_start_date, DATE_FMT).date() if self.pre_season_start_date else None

        self.regular_season_start_date: str = self.sc_data.get("regularSeasonStartDate")
        self.regular_season_start_date: datetime.date = datetime.datetime.strptime(self.regular_season_start_date, DATE_FMT).date() if self.pre_season_start_date else None

        self.regular_season_end_date: str = self.sc_data.get("regularSeasonEndDate")
        self.regular_season_end_date: datetime.date = datetime.datetime.strptime(self.regular_season_end_date, DATE_FMT).date() if self.pre_season_start_date else None

        self.playoff_end_date: str = self.sc_data.get("playoffEndDate")
        self.playoff_end_date: datetime.date = datetime.datetime.strptime(self.playoff_end_date, DATE_FMT).date() if self.pre_season_start_date else None

        self.game_week: list[NHLGameDate] = [NHLGameDate(gd) for gd in sc_data.get("gameWeek", [])]

    def __repr__(self):
        return f"NHLSchedule {self.previous_start_date:{DATE_FMT}}, {self.next_start_date:{DATE_FMT}}"


class NHLStandings:

    class Abbr(enum.Enum):
        GP: str = "GP"        # games played
        GD: str = "GD"        # goal differential
        GA: str = "GA"        # goals against
        GF: str = "GF"        # goals for
        L: str = "L"          # losses
        W: str = "W"          # wins
        SOL: str = "SOL"      # shootout losses
        OTL: str = "OTL"      # overtime losses
        WPCTG: str = "W%"     # overtime losses
        STRKC: str = "STRKC"  # streak indicator
        STRKN: str = "STRKN"  # streak indicator count
        PTS: str = "PTS"      # points
        LURL: str = "LURL"    # team logo url

    def __init__(self, s_data):
        print("NHLStandings")
        self.s_data = s_data

        self.wild_card_indicator = s_data.get("wild_card_indicator")
        self.standings_datetime_utc = s_data.get("standingsDateTimeUtc")

        self.df_standings: pd.DataFrame = pd.DataFrame(s_data.get("standings", []))
        self.df_standings["team_name"] = ""
        self.df_standings["t_id"] = None
        for i, row in self.df_standings.iterrows():
            self.df_standings.loc[i, "team_name"] = row.get("teamName", {}).get("default")

    def show_cols(self, mode: int = None) -> dict[str: str]:
        cols = {
            "teamLogo": NHLStandings.Abbr.LURL.value,
            "gamesPlayed": NHLStandings.Abbr.GP.value,
            "points": NHLStandings.Abbr.PTS.value,
            "wins": NHLStandings.Abbr.W.value,
            "losses": NHLStandings.Abbr.L.value,
            "otLosses": NHLStandings.Abbr.OTL.value,
            "shootoutLosses": NHLStandings.Abbr.SOL.value,
            "winPctg": NHLStandings.Abbr.WPCTG.value,
            "goalFor": NHLStandings.Abbr.GF.value,
            "goalAgainst": NHLStandings.Abbr.GA.value,
            "goalDifferential": NHLStandings.Abbr.GD.value,
            "streakCode": NHLStandings.Abbr.STRKC.value,
            "streakCount": NHLStandings.Abbr.STRKN.value
        }
        return cols


class NHLSeason:
    def __init__(self, s_data: dict | pd.Series):
        self.s_data: dict = s_data if isinstance(s_data, dict) else s_data.to_dict()
        self.s_id: int = self.s_data.get("id")
        self.conferences_in_use: bool = self.s_data.get("conferencesInUse")
        self.divisions_in_use: bool = self.s_data.get("divisionsInUse")
        self.point_for_ot_loss_in_use: bool = self.s_data.get("pointForOTlossInUse")
        self.regulation_wins_in_use: bool = self.s_data.get("regulationWinsInUse")
        self.row_in_use: bool = self.s_data.get("rowInUse")
        # self.standings_end: datetime.date = datetime.datetime.strptime(self.s_data.get("standingsEnd"), DATE_FMT).date()
        # self.standings_start: datetime.date = datetime.datetime.strptime(self.s_data.get("standingsStart"), DATE_FMT).date()
        self.standings_end: datetime.date = self.s_data.get("standingsEnd")
        self.standings_start: datetime.date = self.s_data.get("standingsStart")
        self.ties_in_use: bool = self.s_data.get("tiesInUse")
        self.wild_card_in_use: bool = self.s_data.get("wildcardInUse")

        self.df_season: pd.DataFrame = None

    def get_season_dates(self) -> pd.DatetimeIndex:
        return pd.date_range(self.standings_start, self.standings_end)

    def __eq__(self, other):
        return self.s_id == other.s_id

    def __repr__(self):
        return f"NHL Season {self.s_id}"


class NHLCountry:

    def __init__(self, c_data):

        self.c_data = c_data
        self.c_id: str = c_data["id"]
        self.country_3_code = c_data.get("country3Code")
        self.country_code = c_data.get("countryCode")
        self.country_name = c_data.get("countryName")
        self.has_player_stats = c_data.get("hasPlayerStats")
        self._image_url = c_data.get("imageUrl")
        self.ioc_code = c_data.get("iocCode")
        self.is_active = c_data.get("isActive")
        self.nationality_name = c_data.get("nationalityName")
        self.olympic_url = c_data.get("olympicUrl")
        self._thumbnail_url = c_data.get("thumbnailUrl")

    def __eq__(self, other):
        return self.c_id == other.c_id

    def __repr__(self):
        return f"{self.country_name}"

    def get_image_url(self):
        return "{0}{1}".format(NHL_ASSET_API_URL, self._image_url.removeprefix("/"))

    def set_image_url(self, image_url_in):
        self._image_url = image_url_in

    def del_image_url(self):
        del self._image_url

    def get_thumbnail_url(self):
        return "{0}{1}".format(NHL_ASSET_API_URL, self._thumbnail_url.removeprefix("/"))

    def set_thumbnail_url(self, thumbnail_url_in):
        self._thumbnail_url = thumbnail_url_in

    def del_thumbnail_url(self):
        del self._thumbnail_url

    image_url = property(get_image_url, set_image_url, del_image_url)
    thumbnail_url = property(get_thumbnail_url, set_thumbnail_url, del_thumbnail_url)