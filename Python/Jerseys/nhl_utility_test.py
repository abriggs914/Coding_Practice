import os
import datetime
import requests
import pandas as pd
from dateutil import parser
from typing import Any


class APIHandler:
    
    class InvalidInit(Exception):
        pass
    
    class InvalidTeamAcronym(Exception):
        pass
    
    class InvalidGameID(Exception):
        pass
        
    class InvalidYear(Exception):
        pass
        
    class InvalidDate(Exception):
        pass
    
    def __init__(
        self,
        show_query_strings: bool = False
    ):
        
        self.addr_stats_old: str = "https://statsapi.web.nhl.com/api/v1"
        self.addr_api: str = "https://api-web.nhle.com/v1"
        self.addr_stats: str = "https://api.nhle.com/stats"
        self.addr_assets: str = "https://assets.nhle.com"
        
        self.min_year: int = 1900
        self.max_year: int = datetime.datetime.now().year + 1
        self.min_date: datetime.date = datetime.date(self.min_year, 1, 1)
        self.max_date: datetime.date = datetime.date(self.max_year, 12, 31)
        
        self.save_file_name = "./nhl_utility_query_records.txt"
        self.save_file_delim = "|;;|"
        self.max_query_hold_time: int = 2 * 60 * 60  # 2 hours
        self.held_queries: dict[str: dict] = {}
        self.show_query_strings: bool = show_query_strings

        self.load_held_queries()
        
        self.list_season_ids: list[int] = self.load_season_ids(as_df=False)
        self.country_data: dict[str: Any] = self.load_country_data(as_df=False)
        self.franchise_data: dict[str: Any] = self.load_franchise_data(as_df=False)
        
        for i, lst_name in enumerate([
            "list_season_ids",
            "country_data",
            "franchise_data"
        ]):
            lst = getattr(self, lst_name)
            if not lst:
                print(f"{lst_name}={lst}")
                raise APIHandler.InvalidInit(f"Could not initialize properly.")
        
    def load_held_queries(self):
        if not os.path.exists(self.save_file_name):
            with open(self.save_file_name, "w") as f:
                f.write("")
            return
        else:
            with open(self.save_file_name, "r") as f:
                lines = f.readlines()
                for i, line in enumerate(lines):
                    spl = line.split(self.save_file_delim)
                    if not (len(spl) == 3):
                        raise ValueError(f"{line=} is not the right format.")
                    when_s, url, data_s = spl
                    when = datetime.datetime.strptime(when_s, "%x %X")
                    data = eval(data_s)
                    self.held_queries[url] = {
                        "when": when,
                        "data": data,
                        "idx": i
                    }

    def validate_year(
        self,
        year: int
    ) -> int | None:
        try:
            if isinstance(year, str):
                year = int(year)
            return max(self.min_year, min(self.max_year, year))        
        except Exception as e:
            return None
        
    def validate_date(
        self,
        date: str | datetime.datetime | pd.Timestamp
    ) -> datetime.date | None:
        try:
            # print("A")
            if not isinstance(date, (datetime.datetime, datetime.date)):
                # print("B")
                if isinstance(date, str):
                    # print("C")
                    date = parser.parse(date)
                elif isinstance(date, pd.Timestamp):
                    # print("D")
                    date = date.date()
                else:
                    # print("E")
                    date = None
                    
                if not date:
                    # print("F")
                    return None
                    
            # print("G")
            d_y = date.year
            d_m = date.month
            d_d = date.day
            date = datetime.date(d_y, d_m, d_d)
            # print("H")
            return max(self.min_date, min(self.max_date, date))        
        except Exception as e:
            # print(f"EXC {e}")
            return None

    def validate_team_acronym(
        self,
        team: str
    ) -> str | None:
        ## check if this team exists
        ## for now just assume it is a good team name.
        return team.upper().strip()

    def validate_gameid(
        self,
        gameid: int | str
    ) -> int | None:
        try:
            if isinstance(gameid, str):
                gameid = int(gameid)
            
            s_gid = str(gameid)
            
            if len(s_gid) != 10:
                # the gameid is exactly 10 digits
                # print(f"A")
                return None
            if str(self.validate_year(s_gid[:4])) != s_gid[:4]:
                # the prefix of the gameid (year) is not valid
                # print(f"B {str(self.validate_year(s_gid[:4]))=}")
                return None
            
            # All checks pass, this id is assumed good-to-go.
            return gameid
            
        except Exception as e:
            # print(f"EXC {e}")
            return None
            
    def playoff_bracket_by_year(
        self,
        year: int,
        as_df: bool = True,
        current: bool = True
    ) -> pd.DataFrame | dict | None:
        year = self.validate_year(year)
        if year is None:
            raise APIHandler.InvalidYear(f"Year ({year}) is not valid.")
        url = f"{self.addr_api}/playoff-bracket/{year}/"
        return self.query(url, as_df=as_df, current=current)
        
    def playoff_series_carousel_by_season(
        self,
        season_start_year: int,
        as_df: bool = True,
        current: bool = True
    ) -> pd.DataFrame | dict | None:
        season_start_year = min(season_start_year, self.max_year - 1)
        year = self.validate_year(season_start_year)
        year_str = f"{year}{year+1}"
        url = f"{self.addr_api}/playoff-series/carousel/{year_str}/"
        return self.query(url, as_df=as_df, current=current)        
        
    def fetch_team_logo_address(
        self,
        team: int | str,
        dark_version: bool = True
    ) -> str:
        if isinstance(team, int):
            raise ValueError("Int indexing for teams is not supported yet.")
            
        team = self.validate_team_acronym(team)
        
        if team is None:
            raise APIHandler.InvalidTeamAcronym(f"Cannot find a team that matches this name: '{team}'.")
        
        return f"{self.addr_assets}/logos/nhl/svg/{team}_{'dark' if dark_version else 'light'}.svg"
    
    def gamcenter_landing(
        self,
        gameid: int,
        as_df: bool = False,  # this structure is complex
        current: bool = True
    ) -> pd.DataFrame | dict | None:
        gameid = self.validate_gameid(gameid)
        if gameid is None:
            raise APIHandler.InvalidGameID(f"gameid={gameid} could not be validated.")
        url = f"{self.addr_api}/gamecenter/{gameid}/landing"
        return self.query(url, as_df=as_df, current=current)
        
    def week_schedule(
        self,
        date: str | datetime.datetime | pd.Timestamp,
        as_df: bool = False,  # this structure is complex
        current: bool = True
    ) -> pd.DataFrame | dict | None:
        # gathers game data for 7 days worth of games.
        date = self.validate_date(date)
        if date is None:
            raise APIHandler.InvalidDate(f"date ({date}) is invalid.")
        url = f"{self.addr_api}/schedule/{date}"
        return self.query(url, as_df=as_df, current=current)
        
    def load_season_ids(
        self,
        as_df: bool = True
    ) -> pd.DataFrame | list[int] | None:
        url = f"{self.addr_api}/season"
        return self.query(url, as_df=as_df)
    
    def load_country_data(
        self,
        as_df: bool = True
    ) -> pd.DataFrame | dict | None:
        url = f"{self.addr_stats}/rest/en/country/"
        return self.query(url, as_df=as_df)
    
    def load_franchise_data(
        self,
        as_df: bool = True
    ) -> pd.DataFrame | dict | None:
        url = f"{self.addr_stats}/rest/en/franchise/"
        return self.query(url, as_df=as_df)
        
    def search_for_player(
        self,
        search_str: str,
        limit: int = 20,
        as_df: bool = True
    ) -> pd.DataFrame | dict | None:
        # Searches for a string. Culture is the locale, and active=0|1 may be specified.
        if not search_str.strip():
            raise ValueError(f"Must pass a valid search string to search for a player.")
        limit = max(1, min(1000, limit))
        url = f"https://search.d3.nhle.com/api/v1/search/player?culture=en-us&limit={limit}&q={search_str}"
        return self.query(url, as_df=as_df)

    def query(
        self,
        url: str,
        as_df: bool = True,
        current: bool = False
    ) -> pd.DataFrame | dict | None:
        
        url = url.lower()
        
        if self.addr_stats_old in url:
            url = url.replace(self.addr_stats_old, self.addr_stats)

        idx_new_query = len(self.held_queries)
        now = datetime.datetime.now()
        q_data = self.held_queries.get(url, {}) 
        q_time = q_data.get("when", now)
        q_diff = (now - q_time).total_seconds()
        q_result = q_data.get("data")
        hq_idx = q_data.get("idx", idx_new_query)
        if any([current, not any([q_data, q_result]), q_diff > self.max_query_hold_time]):            
            try:
                if self.show_query_strings:
                    print(f"query {url=}")
                response = requests.get(url)
                # print(f"{response=}")
                data = response.json()
                # print(f"{data=}")
                df = pd.DataFrame(data=data) if as_df else None
                self.held_queries[url] = {
                    "when": now,
                    "data": data,
                    "idx": hq_idx
                }
                
                if hq_idx == idx_new_query:
                    # new query, put it at the end
                    with open(self.save_file_name, "a") as f:
                        f.write(f"{now:%x %X}{self.save_file_delim}{url}{self.save_file_delim}{data}\n")
                else:
                    with open(self.save_file_name, "r") as f:
                        lines = f.readlines()
                    with open(self.save_file_name, "w") as f:
                        f.writelines(lines[:hq_idx])
                        f.write(f"{now:%x %X}{self.save_file_delim}{url}{self.save_file_delim}{data}\n")
                        f.writelines(lines[hq_idx + 1:])

                return df if as_df else data
            except Exception as e:
                print(e)
                return None
        else:
            return pd.DataFrame(q_result) if as_df else q_result
            
    
if __name__ == "__main__":
    
    handler = APIHandler(show_query_strings=True)
    # handler.show_query_strings = True
    
    def test_brackets():
        # playoff bracket
        df_playoff_bracket_2024 = handler.playoff_bracket_by_year(2024)
        print(df_playoff_bracket_2024)
        print(df_playoff_bracket_2024.columns.tolist())
        print(df_playoff_bracket_2024.loc[0, "series"])
    
    def test_carousel():
        # playoff carousel
        df_playoff_carousel_20242025 = handler.playoff_series_carousel_by_season(2024, as_df=False)
        print(df_playoff_carousel_20242025)

    def test_team_logo():
        # team logo addresses
        print(handler.fetch_team_logo_address("cgy", dark_version=False))

    def test_gamecenter_landing():
        # gamecenter landing
        print(handler.gamcenter_landing(2024021001))

    def test_week_schedule():
        # Week schedule
        print(handler.week_schedule("2025-03-13"))
        
        
    # test_brackets()
    # test_carousel()
    # test_team_logo()
    # test_gamecenter_landing()
    # test_week_schedule()
    
    # print(handler.list_season_ids)
    # print(handler.country_data)
    # print(handler.franchise_data)

    print(handler.search_for_player("Avery"))
    print(handler.search_for_player("Briggs"))
    print(handler.search_for_player("avery"))
