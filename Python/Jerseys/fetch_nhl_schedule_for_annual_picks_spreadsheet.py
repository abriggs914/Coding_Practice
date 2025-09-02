import requests
import datetime
import pandas as pd


t_template_0: str = "%Y-%m-%d"
t_template_1: str = "%Y-%m-%dT%H:%M:%SZ"
template: str = "https://api-web.nhle.com/v1/schedule"


class Team:
    
    def __init__(self, data):
        self.data: dict = data
        self.id_: int = data.get("id")
        self.common_name: str = data.get("commonName", {}).get("default")
        self.place_name: str = data.get("placeName", {}).get("default")
        self.place_name_with_preposition: str = data.get("placeNameWithPreposition", {}).get("default")
        self.abbrev: str = data.get("abbrev")
        self.logo: str = data.get("logo")
        self.dark_logo: str = data.get("darkLogo")
        self.away_split_squad: bool = data.get("awaySplitSquad")
        self.radio_link: str = data.get("radioLink")
        
    def __repr__(self):
        return self.abbrev
        
        
data_teams: dict[int: Team] = {}
def get_team(data):
    id_: int = data.get("id")
    if id_ not in data_teams:
        team = Team(data)
        data_teams[id_] = team
    return data_teams[id_]
    

def parse_date(obj, data, attr, key_name, template=t_template_0):
    try:
        setattr(obj, attr, datetime.datetime.strptime(data.get(key_name), template).date())
    except TypeError:
        setattr(obj, attr, None)


class GameData:
    
    def __init__(self, data):
        self.data: dict = data
        self.id_: int = data.get("id")
        self.season: int = data.get("season")
        self.game_type: int = data.get("gameType")
        self.venue: str = data.get("venue", {}).get("default")
        self.neutral_site: bool = data.get("neutralSite")
        parse_date(self, data, "start_time_UTC", "startTimeUTC", t_template_1)
        self.eastern_UTC_offset: str = data.get("easternUTCOffset")
        self.venue_UTC_offset: str = data.get("venueUTCOffset")
        self.venue_timezone: str = data.get("venueTimezone")
        self.game_state: str = data.get("gameState")
        self.game_schedule_state: str = data.get("gameScheduleState")
        self.tv_broadcasts: list[str] = data.get("tvBroadcasts")
        self.away_team: Team = get_team(data.get("awayTeam"))
        self.home_team: Team = get_team(data.get("homeTeam"))
        self.period_descriptor: int = data.get("periodDescriptor", {}).get("maxRegulationPeriods")
        self.tickets_link: str = data.get("ticketsLink")
        self.tickets_link_fr: str = data.get("ticketsLinkFr")
        self.game_center_link: str = data.get("gameCenterLink")
        
    def __repr__(self):
        return f"{self.start_time_UTC.strftime(t_template_1)}  -  {self.id_}  -  {self.away_team} @ {self.home_team}"


data_games: dict[int: GameData] = {}
def get_game(data):
    id_: int = data.get("id")
    if id_ not in data_games:
        game_data = GameData(data)
        data_games[id_] = game_data
    return data_games[id_]
        

class GameDate:
    
    def __init__(self, data):
        self.data: dict = data
        parse_date(self, data, "date", "date")
        self.day_abbrev: str = data.get("dayAbbrev")
        self.number_of_games: int = data.get("numberOfGames", 0)
        self.date_promo: list[str] = data.get("datePromo")
        self.games: list[GameData] = [get_game(gd) for gd in data.get("games", [])]


class GameWeek:
    
    def __init__(self, data):
        self.data: dict = data
        for attr, key_name in [
            ("next_start_date", "nextStartDate"),
            ("pre_season_start_date", "preSeasonStartDate"),
            ("previous_start_date", "previousStartDate"),
            ("regular_season_start_date", "regularSeasonStartDate"),
            ("regular_season_end_date", "regularSeasonEndDate"),
            ("playoff_end_date", "playoffEndDate")
        ]:
            parse_date(self, self.data, attr, key_name)

        self.game_week: list[GameDate] = [GameDate(gd) for gd in data.get("gameWeek", [])]
        self.number_of_games: int = data.get("numberOfGames")
         

if __name__ == "__main__":
    ld = None
    d1 = datetime.datetime(2025, 9, 15).date()
    # d1 = datetime.datetime(2026, 4, 1).date()
    d2 = None
    k = 0
    
    keep_going = True
    while keep_going:
        ld = None
        try:
            url = f"{template}/{d1.strftime(t_template_0)}"
            print(f"{url=}")
            data = requests.get(url).json()
            game_week = GameWeek(data)
            ld = game_week.previous_start_date
            d1 = game_week.next_start_date
            games = [game_date.games for game_date in game_week.game_week]
            n_games = 0
            if games:
                if any(games):
                    n_games = sum([len(game_date) for game_date in games])
                else:
                    n_games = len(games)

            # print(f"N Games: {n_games}")
            # for game_date_games in games:
            #     for game in game_date_games:
            #         print(f"{game}")
            
            if d2 is None:
                d2 = game_week.regular_season_end_date
                
            if d1 is None:
                keep_going = False            
            elif d1 > d2:
                keep_going = False
                
        except Exception as e:
            print(f"{e=}, {e.with_traceback()=}")
            if data is None:
                keep_going = False
        
        # k += 1
        # print(f"{d1.strftime(t_template_0)=}")
        # print(f"{d2.strftime(t_template_0)=}")
        # if k >= 4:
        #     keep_going = False
            
    list_games = list(data_games.values())
    list_games = [game for game in list_games if game.game_type == 2]
    list_games.sort(key=lambda x: x.start_time_UTC)
    
    # print(f"{list_games[:5]}")
    # print(f"{list_games[-5:]}")

    df_data = [
        {
            "PredictionDate": None,
            "GameDate": game.start_time_UTC.strftime(t_template_0),
            "GameID": game.id_,
            "AwayTeam": str(game.away_team),
            "HomeTeam": str(game.home_team)
        }
        for game in list_games
    ]
    df = pd.DataFrame(data=df_data)
    print(f"df")
    print(df)
    # with open(f"fetched_schedule_{datetime.datetime.now():%Y-%m-%m %H%M%S}.xlsx", "w") as f:
    #     df.to_excel(f)    
    df.to_excel(f"fetched_schedule_{datetime.datetime.now():%Y-%m-%m %H%M%S}.xlsx")
