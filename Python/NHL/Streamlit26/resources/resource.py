import datetime


# Emojis
E_strl_RUNNING: str = f":ice_hockey_stick_and_puck:"
E_strl_STOPWATCH: str = f":stopwatch:"
E_html_STOPPAGE: str = f"&#128721"
E_html_PLAYING: str = f"&#127954"

# API url
NHL_ASSET_API_URL: str = "https://assets.nhle.com/"
NHL_STATS_API_URL: str = "https://api.nhle.com/stats/rest/en/"
NHL_URL: str = "https://www.nhl.com/"
NHL_API_URL: str = "https://api-web.nhle.com/"
NHL_API_URL_V1: str = "{0}v1/".format(NHL_API_URL)
NHL_PLAYER_API_URL: str = "{0}player/".format(NHL_API_URL_V1)

# File and folder paths
PATH_UNKNOWN_IMAGE: str = r"C:\Users\abrig\Documents\Coding_Practice\Resources\Flags\unknown_flag.png"
PATH_FOLDER_JERSEY_COLLECTION: str = r"D:\NHL jerseys\Jerseys 20250927"
PATH_JERSEY_COLLECTION_DATA: str = r"C:\Users\abrig\Documents\Coding_Practice\Python\Jerseys\Jerseys_20260103.xlsx"
JERSEY_COLOUR_SAVE_FILE: str = "new_colours_save.json"

# Formats
UTC_FMT: str = "%Y-%m-%dT%H:%M:%SZ"
DATE_FMT: str = "%Y-%m-%d"

# Defaults
DEFAULT_SEASON_END_DATE: datetime.date = datetime.date(datetime.datetime.now().year + (1 if 8 < datetime.datetime.now().month else 0), 4, 16)
DEFAULT_TEAM: str = "Calgary Flames"
