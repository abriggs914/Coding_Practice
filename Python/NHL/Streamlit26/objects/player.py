import pandas as pd

from objects.league import NHLCountry
from resources.resource import PATH_UNKNOWN_IMAGE
from objects.team import NHLTeam


class NHLPlayer:

    def __init__(self, p_data):
        self.data = p_data
        self.p_id: int = p_data.get("playerId")
        self.path_team_logo = p_data.get("teamLogo", PATH_UNKNOWN_IMAGE)
        self.path_headshot_logo = p_data.get("headshot", PATH_UNKNOWN_IMAGE)
        self.path_hero_shot_logo = p_data.get("heroImage", PATH_UNKNOWN_IMAGE)

        self.name_first = p_data.get("firstName", dict()).get("default")
        self.name_last = p_data.get("lastName", dict()).get("default")
        # print(f" {self.name_first=}, {self.name_last=}")

        self.number = p_data.get("sweaterNumber")
        self.position = p_data.get("position")
        self.shoots_catches = p_data.get("shootsCatches")
        self.height_inch = p_data.get("heightInInches")
        self.height_cent = p_data.get("heightInCentimeters")
        self.weight_lb = p_data.get("weightInPounds")
        self.weight_kg = p_data.get("weightInKilograms")
        self.is_active = p_data.get("isActive")
        self.dob = p_data.get("birthDate")
        self.birth_city = p_data.get("birthCity", dict()).get("default")
        self.birth_province = p_data.get("birthStateProvince", dict()).get("default")
        self.birth_country: NHLCountry = p_data.get("birthCountry")

        self.in_HHOF = p_data.get("inHHOF")

        self.draft_year = p_data.get("draftDetails", dict()).get("year")
        self.draft_team_abbrev = p_data.get("draftDetails", dict()).get("teamAbbrev")
        self.draft_round = p_data.get("draftDetails", dict()).get("round")
        self.draft_pick_in_round = p_data.get("draftDetails", dict()).get("pickInRound")
        self.draft_overall_pick = p_data.get("draftDetails", dict()).get("overallPick")

        self.team: NHLTeam = None
        self.team_id = p_data.get("currentTeamId")
        self.team_abbrev = p_data.get("currentTeamAbbrev")
        self.team_name = p_data.get("fullTeamName", dict()).get("default")
        self.team_name_fr = p_data.get("fullTeamName", dict()).get("fr", self.team_name)
        self.team_common_name = p_data.get("teamCommonName", dict()).get("default", self.team_name)
        self.team_place_name = p_data.get("teamPlaceNameWithPreposition", dict()).get("default")
        self.team_place_name_fr = p_data.get("teamPlaceNameWithPreposition", dict()).get("fr", self.team_place_name)

        self._featured_stats = p_data.get("featuredStats", dict())
        self.career_totals: pd.DataFrame = pd.DataFrame(p_data.get("careerTotals", dict()))
        self.last_5_games = p_data.get("last5Games", list())
        self.season_totals: pd.DataFrame = pd.DataFrame(p_data.get("seasonTotals", list()))
        self.current_team_roster = p_data.get("currentTeamRoster", list())

        # self.career_totals["total"] = self.career_totals["regularSeason"] + self.career_totals["playoffs"]

        # for k, v in self.data.items():
        #     setattr(self, k, v)

    def to_df_row(self) -> dict:
        return {k: v for k, v in self.__dict__.items() if type(v) not in (list, tuple, dict, pd.DataFrame)}

    def get_featured_stats(self) -> tuple[int, pd.DataFrame]:
        featured_stats_season = self._featured_stats["season"]
        obj_featured_stats = pd.DataFrame({
            "regularSeason_sub_season": self._featured_stats.get("regularSeason", {}).get("subSeason"),
            "regularSeason_career": self._featured_stats.get("regularSeason", {}).get("career"),
            "playoffs_sub_season": self._featured_stats.get("playoffs", {}).get("subSeason"),
            "playoffs_career": self._featured_stats.get("playoffs", {}).get("career")
        })
        return featured_stats_season, obj_featured_stats

    def set_featured_stats(self, featured_stats_in):
        self._featured_stats = featured_stats_in

    def del_featured_stats(self):
        del self._featured_stats

    def __eq__(self, other):
        return self.p_id == other.p_id

    def __repr__(self):
        return f"#{self.p_id} {self.name_first} {self.name_last}"

    featured_stats = property(get_featured_stats, set_featured_stats, del_featured_stats)
