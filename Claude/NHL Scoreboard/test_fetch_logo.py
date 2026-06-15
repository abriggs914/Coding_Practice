from streamlit_utility import display_df
import streamlit as st
import pandas as pd


TEAM_META = {
    "ANA": {"name": "Anaheim Ducks",       "conf": "Western", "div": "Pacific",    "id": 24, "active": True},
    # "ARI": {"name": "Utah Hockey Club",     "conf": "Western", "div": "Central",    "id": 53, "active": False},
    "UTA": {"name": "Utah Mammoth",         "conf": "Western", "div": "Central",    "id": 59, "active": True},
    "BOS": {"name": "Boston Bruins",        "conf": "Eastern", "div": "Atlantic",   "id": 6, "active": True},
    "BUF": {"name": "Buffalo Sabres",       "conf": "Eastern", "div": "Atlantic",   "id": 7, "active": True},
    "CGY": {"name": "Calgary Flames",       "conf": "Western", "div": "Pacific",    "id": 20, "active": True},
    "CAR": {"name": "Carolina Hurricanes",  "conf": "Eastern", "div": "Metropolitan","id": 12, "active": True},
    "CHI": {"name": "Chicago Blackhawks",   "conf": "Western", "div": "Central",    "id": 16, "active": True},
    "COL": {"name": "Colorado Avalanche",   "conf": "Western", "div": "Central",    "id": 21, "active": True},
    "CBJ": {"name": "Columbus Blue Jackets","conf": "Eastern", "div": "Metropolitan","id": 29, "active": True},
    "DAL": {"name": "Dallas Stars",         "conf": "Western", "div": "Central",    "id": 25, "active": True},
    "DET": {"name": "Detroit Red Wings",    "conf": "Eastern", "div": "Atlantic",   "id": 17, "active": True},
    "EDM": {"name": "Edmonton Oilers",      "conf": "Western", "div": "Pacific",    "id": 22, "active": True},
    "FLA": {"name": "Florida Panthers",     "conf": "Eastern", "div": "Atlantic",   "id": 13, "active": True},
    "LAK": {"name": "Los Angeles Kings",    "conf": "Western", "div": "Pacific",    "id": 26, "active": True},
    "MIN": {"name": "Minnesota Wild",       "conf": "Western", "div": "Central",    "id": 30, "active": True},
    "MTL": {"name": "Montréal Canadiens",   "conf": "Eastern", "div": "Atlantic",   "id": 8, "active": True},
    "NSH": {"name": "Nashville Predators",  "conf": "Western", "div": "Central",    "id": 18, "active": True},
    "NJD": {"name": "New Jersey Devils",    "conf": "Eastern", "div": "Metropolitan","id": 1, "active": True},
    "NYI": {"name": "New York Islanders",   "conf": "Eastern", "div": "Metropolitan","id": 2, "active": True},
    "NYR": {"name": "New York Rangers",     "conf": "Eastern", "div": "Metropolitan","id": 3, "active": True},
    "OTT": {"name": "Ottawa Senators",      "conf": "Eastern", "div": "Atlantic",   "id": 9, "active": True},
    "PHI": {"name": "Philadelphia Flyers",  "conf": "Eastern", "div": "Metropolitan","id": 4, "active": True},
    "PIT": {"name": "Pittsburgh Penguins",  "conf": "Eastern", "div": "Metropolitan","id": 5, "active": True},
    "SJS": {"name": "San Jose Sharks",      "conf": "Western", "div": "Pacific",    "id": 28, "active": True},
    "SEA": {"name": "Seattle Kraken",       "conf": "Western", "div": "Pacific",    "id": 55, "active": True},
    "STL": {"name": "St. Louis Blues",      "conf": "Western", "div": "Central",    "id": 19, "active": True},
    "TBL": {"name": "Tampa Bay Lightning",  "conf": "Eastern", "div": "Atlantic",   "id": 14, "active": True},
    "TOR": {"name": "Toronto Maple Leafs",  "conf": "Eastern", "div": "Atlantic",   "id": 10, "active": True},
    "VAN": {"name": "Vancouver Canucks",    "conf": "Western", "div": "Pacific",    "id": 23, "active": True},
    "VGK": {"name": "Vegas Golden Knights", "conf": "Western", "div": "Pacific",    "id": 54, "active": True},
    "WSH": {"name": "Washington Capitals",  "conf": "Eastern", "div": "Metropolitan","id": 15, "active": True},
    "WPG": {"name": "Winnipeg Jets",        "conf": "Western", "div": "Central",    "id": 52, "active": True},
}


PWHL_META = [
    {"name": "Ottawa Charge", "acronym": "OTT", "logo": r"C:\Users\abrig\Documents\Coding_Practice\Python\Hockey pool\Images\ottawa_charge.png",},
    {"name": "Montreal Victoire", "acronym": "MTL", "logo": r"C:\Users\abrig\Documents\Coding_Practice\Python\Hockey pool\Images\montreal_victoire.png",},
    {"name": "Toronto Sceptres", "acronym": "TOR", "logo": r"C:\Users\abrig\Documents\Coding_Practice\Python\Hockey pool\Images\toronto_sceptres.png",},
    {"name": "Vancouver Goldeneyes", "acronym": "VAN", "logo": r"C:\Users\abrig\Documents\Coding_Practice\Python\Hockey pool\Images\vancouver_goldeneyes.png",},
    {"name": "New York Sirens", "acronym": "NY", "logo": r"C:\Users\abrig\Documents\Coding_Practice\Python\Hockey pool\Images\new_york_sirens.png",},
    {"name": "Seattle Torrent", "acronym": "SEA", "logo": r"C:\Users\abrig\Documents\Coding_Practice\Python\Hockey pool\Images\seattle_torrent.png",},
    {"name": "Boston Fleet", "acronym": "BOS", "logo": r"C:\Users\abrig\Documents\Coding_Practice\Python\Hockey pool\Images\boston_fleet.png",},
    {"name": "Minnesota Frost", "acronym": "MIN", "logo": r"C:\Users\abrig\Documents\Coding_Practice\Python\Hockey pool\Images\minnesota_frost.png",},
]

df_pwhl = pd.DataFrame(PWHL_META)
df_pwhl[["league", "active"]] = ["PWHL", True]
df_pwhl = df_pwhl.rename(columns={"acronym": "team"})
# display_df(df_pwhl, "PWHL")

df_teams = pd.DataFrame(TEAM_META).T.reset_index(names="team")
df_teams["league"] = "NHL"
for team, name, league in [
    ("ARI", "Arizona Coyotes", "NHL"),
    
    ("CAN", "Team Canada", "IIHF"),
    ("USA", "Team United States", "IIHF"),
    ("SWE", "Team Sweden", "IIHF"),
    ("FIN", "Team Finland", "IIHF"),
    ("CAN", "Team Canada", "IIHF"),
    
    ("SJ", "Saint John SeaDogs", "QMJHL"),
]:
    df_teams.loc[len(df_teams), df_teams.columns] = [team, name, None, None, None, True, league]
    
df_teams.loc[df_teams["team"] == "ARI", ["active", "conf", "div"]] = [False, "Western", "Central"]

df_teams["alt"] = None
for t, a in [
    ("LAK", "LA"),
    ("TBL", "TB"),
    ("NJD", "NJ"),
    ("SJS", "SJ"),
    ("WSH", "WAS"),
]:
    df_teams.loc[df_teams["team"] == t, "alt"] = a

df_teams = pd.concat([df_teams, df_pwhl], ignore_index=True)
df_teams["teamLeague"] = df_teams["team"] + " - " + df_teams["league"]


def team_fmt(s):
    return str(s).replace(" ", "").upper().strip()
    
    
def find_team(team):
    for i, row in df_teams.iterrows():
        if team_fmt(row["team"]) == team_fmt(team):
            return row["team"]
        elif team_fmt(team) == team_fmt(row["name"]):
            return row["team"]    
        elif team_fmt(team) == team_fmt(row["alt"]):
            return row["team"]


def fetch_team_logo(team_abbr: str, dark: bool = True, err_on_not_found: bool = False, league: str = "NHL", debug: bool = False) -> str:
    """Get NHL team logo URL from NHL API."""
    s_t = team_fmt(find_team(team_abbr))
    s_l = team_fmt(str(league))
    df_s = df_teams.copy()
    df_s["team_s"] = df_s["team"].apply(team_fmt)
    df_s["league_s"] = df_s["league"].apply(team_fmt)
    df_s = df_s[(df_s["team_s"] == s_t) & (df_s["league_s"] == s_l)].reset_index()
    c = len(df_s)
    if debug:
        display_df(df_s, f"df_s {team_abbr=}, {dark=}, err={err_on_not_found}, {league=}")
    if c == 1:
        if s_l == team_fmt("NHL"):
            return f"https://assets.nhle.com/logos/nhl/svg/{df_s.loc[0, 'team'].upper()}_{'dark' if dark else 'light'}.svg"
        elif s_l == team_fmt("PWHL"):
            return df_s.iloc[0]["logo"]
    elif (c == 0) and err_on_not_found:
        raise ValueError(f"{team_abbr=} not found in df_teams")
    elif c > 0:
        raise ValueError(f"Multiple teams found matching {team_abbr=} found in df_teams")
    
    return ""


if __name__ == "__main__":

    display_df(df_teams, "Teams")
    team_l = st.selectbox("TEAM", sorted(df_teams["teamLeague"].values.tolist()))
    if team_l:
        team, league = df_teams[df_teams["teamLeague"] == team_l].reset_index().loc[0, ["team", "league"]]
        logo = fetch_team_logo(team, league=league)
        if logo:
            st.image(logo, logo)
        else:
            st.write(f"No image found")
    