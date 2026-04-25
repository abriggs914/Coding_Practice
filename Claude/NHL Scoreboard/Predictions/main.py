"""
NHL Prediction Performance Dashboard
Run with: streamlit run nhl_dashboard.py
"""

import os
import math
import time
import json
import base64
import random
import requests
import warnings
import pdfplumber
import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import streamlit.components.v1 as components
from streamlit_sortables import sort_items
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from plotly.subplots import make_subplots
from streamlit_pills import pills
from datetime import datetime, timedelta
from typing import Optional, Literal, Sequence
from collections import defaultdict

from colour_utility import Colour, gradient_merge
from json_utility import peek_json, jsonify
from sql_utility import no_specials
from streamlit_utility import display_df, consolidate_df_edits
from streamlit_auth import show_login_register
import nhl_api_reference_examples as api_ref

warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────────────────
# DATA SOURCE — local Excel workbook
# ─────────────────────────────────────────────────────────
path_excel_predictions       = r"C:\\Users\\abrig\\Documents\\Coding_Practice\\Python\\Jerseys\\NHLGamePredictions_2526_copy.xlsx"
path_excel_jerseys           = r"C:\\Users\\abrig\\Documents\\Coding_Practice\\Python\\Jerseys\\Jerseys_20260401.xlsx"
path_jersey_images           = r"D:\\NHL jerseys\\Jerseys 20250927"
path_image_dir               = r"C:\Users\abrig\Documents\Coding_Practice\Python\DataVisualizer"
path_stanley_cup_appearances = r"C:\Users\abrig\Documents\Coding_Practice\Python\DataVisualizer\dataset_nhl_team_apperances.json"
path_stanley_cup_wins        = r"C:\Users\abrig\Documents\Coding_Practice\Python\DataVisualizer\dataset_nhl_team_wins.json"
path_stanley_cup_losses      = r"C:\Users\abrig\Documents\Coding_Practice\Python\DataVisualizer\dataset_nhl_team_losses.json"
path_hockey_pool_data        = r"C:\Users\abrig\Documents\Coding_Practice\Python\Hockey pool\Data\data.json"

# ─────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────
st.set_page_config(
    page_title="NHL Prediction Dashboard",
    page_icon="🏒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────
# STYLES
# ─────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@300;400;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.main { background: #0a0e1a; }

.nhl-header {
    background: linear-gradient(135deg, #0a0e1a 0%, #0d2137 50%, #0a0e1a 100%);
    border-bottom: 3px solid #c8a84b;
    padding: 24px 32px;
    margin-bottom: 24px;
    border-radius: 0 0 12px 12px;
}
.nhl-header h1 {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.8rem;
    letter-spacing: 4px;
    color: #c8a84b;
    margin: 0;
    text-shadow: 0 0 30px rgba(200,168,75,0.3);
}
.nhl-header p { color: #8899aa; margin: 4px 0 0; font-size: 0.9rem; }

.metric-card {
    background: linear-gradient(135deg, #0d1f35, #0a1828);
    border: 1px solid #1e3a5a;
    border-left: 4px solid #c8a84b;
    border-radius: 8px;
    padding: 16px 20px;
    margin: 4px;
}
.metric-card .value {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.2rem;
    color: #c8a84b;
    line-height: 1;
}
.metric-card .label { color: #8899aa; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; margin-top: 4px; }

.section-header {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.6rem;
    letter-spacing: 3px;
    color: #c8a84b;
    border-bottom: 2px solid #1e3a5a;
    padding-bottom: 8px;
    margin: 24px 0 16px;
}

.team-logo { width: 48px; height: 48px; object-fit: contain; }

.stSelectbox > div > div { background: #0d1f35; border-color: #1e3a5a; }
.stMultiSelect > div > div { background: #0d1f35; border-color: #1e3a5a; }

div[data-testid="stMetricValue"] { color: #c8a84b !important; font-family: 'Bebas Neue', sans-serif; font-size: 2rem !important; }
div[data-testid="stMetricLabel"] { color: #8899aa !important; }

.gauntlet-card {
    background: #0d1f35;
    border: 1px solid #1e3a5a;
    border-radius: 8px;
    padding: 16px;
    margin: 8px 0;
}
.gauntlet-title { font-family: 'Bebas Neue', sans-serif; color: #c8a84b; font-size: 1.2rem; letter-spacing: 2px; }

.correct-badge { background: #0d3321; color: #2ecc71; border-radius: 4px; padding: 2px 8px; font-size: 0.8rem; font-weight: 600; }
.incorrect-badge { background: #330d0d; color: #e74c3c; border-radius: 4px; padding: 2px 8px; font-size: 0.8rem; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────
# NHL TEAM METADATA
# ─────────────────────────────────────────────────────────
TEAM_META = {
    "ANA": {"name": "Anaheim Ducks",       "conf": "Western", "div": "Pacific",    "id": 24, "active": True},
    # "ARI": {"name": "Utah Hockey Club",     "conf": "Western", "div": "Central",    "id": 53, "active": False},
    "UTA": {"name": "Utah Hockey Club",     "conf": "Western", "div": "Central",    "id": 59, "active": True},
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

CANADIAN_TEAMS = {"MTL", "OTT", "TOR", "WPG", "EDM", "CGY", "VAN"}

GAUNTLETS = {
    "California Swing 🌴": {
        "teams": ["ANA", "LAK", "SJS", "VGK"],
        "desc": "West Coast swing through California & Vegas",
        "region": "Pacific Coast"
    },
    "Canada West 🍁": {
        "teams": ["CGY", "EDM", "VAN"],
        "desc": "Western Canadian road trip",
        "region": "Western Canada"
    },
    "Canada East 🍁": {
        "teams": ["MTL", "OTT", "TOR"],
        "desc": "Eastern Canadian road trip",
        "region": "Eastern Canada"
    },
    "Metro NY Gauntlet 🗽": {
        "teams": ["NYR", "NYI", "NJD"],
        "desc": "New York metro area tri-team swing",
        "region": "Greater New York"
    },
    "Florida Sunshine Tour ☀️": {
        "teams": ["FLA", "TBL"],
        "desc": "Florida peninsula back-to-back",
        "region": "Florida"
    },
    "Pennsylvania Turnpike 🛣️": {
        "teams": ["PIT", "PHI"],
        "desc": "Keystone State rivalry gauntlet",
        "region": "Pennsylvania"
    },
    "Central Midwest Swing 🌾": {
        "teams": ["CHI", "STL", "NSH", "MIN"],
        "desc": "Central division midwest road stretch",
        "region": "Midwest"
    },
    "Texas Two-Step 🤠": {
        "teams": ["DAL", "COL"],
        "desc": "Southern plains to mountain road trip",
        "region": "South-Central"
    },
    "Pacific Northwest 🌲": {
        "teams": ["VAN", "SEA"],
        "desc": "Cascadia coastal road trip",
        "region": "Pacific Northwest"
    },
    "Original Six Heritage 🏆": {
        "teams": ["BOS", "MTL", "TOR", "DET", "NYR", "CHI"],
        "desc": "Classic Original Six matchups",
        "region": "Historic Rivalry"
    },
}


# ─────────────────────────────────────────────────────────
# NHL TEAM RIVALRIES
# ─────────────────────────────────────────────────────────
TEAM_RIVALS = {
    "ANA": {
        "primary":   ["LAK", "SJS"],
        "secondary": ["VGK", "SEA"],
        "historic":  ["DET"],
        "modern":    ["EDM"],
        "reasons": {
            "LAK": ["same_division", "southern_california", "geographic", "frequent_matchups"],
            "SJS": ["same_division", "california", "geographic"],
            "VGK": ["same_division", "pacific_contention"],
            "SEA": ["same_division", "regional_west"],
            "DET": ["historic_playoffs"],
            "EDM": ["playoff_history"]
        }
    },

    "UTA": {
        "primary":   ["COL", "VGK"],
        "secondary": ["DAL", "NSH", "WPG"],
        "historic":  [],
        "modern":    [],
        "reasons": {
            "COL": ["same_division", "rocky_mountain_region"],
            "VGK": ["regional_west", "newer_franchise_competition"],
            "DAL": ["same_division"],
            "NSH": ["same_division"],
            "WPG": ["same_division"]
        }
    },

    "BOS": {
        "primary":   ["MTL", "TOR"],
        "secondary": ["BUF", "FLA", "TBL"],
        "historic":  ["DET", "NYR", "CHI"],
        "modern":    ["FLA"],
        "reasons": {
            "MTL": ["original_six", "historic", "playoff_history", "atlantic"],
            "TOR": ["original_six", "atlantic", "historic"],
            "BUF": ["atlantic", "regional_east"],
            "FLA": ["atlantic", "recent_playoffs"],
            "TBL": ["atlantic", "recent_contention"],
            "DET": ["original_six", "historic"],
            "NYR": ["original_six", "historic"],
            "CHI": ["original_six"]
        }
    },

    "BUF": {
        "primary":   ["TOR", "OTT"],
        "secondary": ["BOS", "DET", "MTL"],
        "historic":  ["PHI"],
        "modern":    [],
        "reasons": {
            "TOR": ["atlantic", "geographic", "cross_border"],
            "OTT": ["atlantic", "regional"],
            "BOS": ["atlantic"],
            "DET": ["regional", "great_lakes"],
            "MTL": ["atlantic", "regional"],
            "PHI": ["historic"]
        }
    },

    "CGY": {
        "primary":   ["EDM", "VAN"],
        "secondary": ["LAK", "SEA", "VGK", "TOR", "OTT", "MTL"],
        "historic":  ["WPG", "ANA"],
        "modern":    ["EDM"],
        "reasons": {
            "EDM": ["same_division", "same_province", "battle_of_alberta", "historic", "modern"],
            "VAN": ["same_division", "western_canada"],
            "LAK": ["same_division", "playoff_history"],
            "SEA": ["same_division", "regional_west"],
            "VGK": ["same_division", "pacific_contention"],
            "WPG": ["western_canada", "historic"],
            "ANA": ["playoff_history"],
            "TOR": ["canadian_team"],
            "OTT": ["canadian_team"],
            "MTL": ["canadian_team"]
        }
    },

    "CAR": {
        "primary":   ["WSH", "NJD"],
        "secondary": ["NYR", "TBL", "FLA"],
        "historic":  ["MTL", "BOS"],
        "modern":    ["NYR", "FLA"],
        "reasons": {
            "WSH": ["metro", "regional_east"],
            "NJD": ["metro", "playoff_history"],
            "NYR": ["metro", "recent_playoffs", "contention"],
            "TBL": ["regional_southeast", "playoff_history"],
            "FLA": ["east_contention", "recent_playoffs"],
            "MTL": ["former_division", "historic"],
            "BOS": ["east_contention", "historic"]
        }
    },

    "CHI": {
        "primary":   ["DET", "STL"],
        "secondary": ["MIN", "NSH", "COL"],
        "historic":  ["VAN", "LAK", "TOR", "MTL", "NYR", "BOS"],
        "modern":    [],
        "reasons": {
            "DET": ["original_six", "historic", "regional", "old_central"],
            "STL": ["regional", "midwest", "historic"],
            "MIN": ["same_division", "regional"],
            "NSH": ["same_division"],
            "COL": ["same_division"],
            "VAN": ["historic_playoffs"],
            "LAK": ["historic_playoffs"],
            "TOR": ["original_six"],
            "MTL": ["original_six"],
            "NYR": ["original_six"],
            "BOS": ["original_six"]
        }
    },

    "COL": {
        "primary":   ["DET", "MIN"],
        "secondary": ["DAL", "VGK", "STL"],
        "historic":  ["NJD"],
        "modern":    ["DAL", "VGK", "SEA"],
        "reasons": {
            "DET": ["historic", "legendary_playoff_rivalry"],
            "MIN": ["same_division", "proximity"],
            "DAL": ["same_division", "recent_playoffs", "contention"],
            "VGK": ["west_contention", "recent_playoffs"],
            "STL": ["same_division"],
            "NJD": ["historic_cup_final"],
            "SEA": ["recent_playoffs"]
        }
    },

    "CBJ": {
        "primary":   ["PIT", "WSH"],
        "secondary": ["NJD", "CAR", "DET"],
        "historic":  ["TBL"],
        "modern":    [],
        "reasons": {
            "PIT": ["metro", "regional"],
            "WSH": ["metro"],
            "NJD": ["metro"],
            "CAR": ["metro"],
            "DET": ["regional"],
            "TBL": ["historic_sweep_upset"]
        }
    },

    "DAL": {
        "primary":   ["COL", "STL"],
        "secondary": ["NSH", "MIN", "WPG", "EDM"],
        "historic":  ["EDM", "BUF"],
        "modern":    ["VGK", "COL", "EDM"],
        "reasons": {
            "COL": ["same_division", "recent_playoffs", "contention"],
            "STL": ["same_division", "historic_playoffs"],
            "NSH": ["same_division"],
            "MIN": ["same_division"],
            "WPG": ["same_division"],
            "EDM": ["west_contention", "recent_playoffs", "historic_playoffs"],
            "BUF": ["historic_cup_final"],
            "VGK": ["west_contention", "recent_playoffs"]
        }
    },

    "DET": {
        "primary":   ["CHI", "COL", "TOR"],
        "secondary": ["BOS", "MTL", "OTT", "TBL"],
        "historic":  ["STL", "ANA", "NYR"],
        "modern":    ["OTT"],
        "reasons": {
            "CHI": ["original_six", "regional", "historic"],
            "COL": ["historic", "legendary_playoff_rivalry"],
            "TOR": ["original_six", "regional"],
            "BOS": ["original_six", "atlantic"],
            "MTL": ["original_six", "atlantic"],
            "OTT": ["atlantic", "recent_tension"],
            "TBL": ["atlantic"],
            "STL": ["historic_division"],
            "ANA": ["historic_playoffs"],
            "NYR": ["original_six"]
        }
    },

    "EDM": {
        "primary":   ["CGY", "LAK"],
        "secondary": ["VAN", "VGK", "DAL", "WPG", "OTT", "TOR", "MTL"],
        "historic":  ["NYI", "PHI", "DAL"],
        "modern":    ["FLA", "VGK", "DAL"],
        "reasons": {
            "CGY": ["same_division", "same_province", "battle_of_alberta", "historic", "modern"],
            "LAK": ["same_division", "playoff_history", "recent_playoffs"],
            "VAN": ["same_division", "western_canada"],
            "VGK": ["same_division", "west_contention", "recent_playoffs"],
            "DAL": ["west_contention", "recent_playoffs", "historic_playoffs"],
            "NYI": ["historic_cup_final", "1980s_dynasty"],
            "PHI": ["historic_cup_final", "1980s"],
            "FLA": ["modern", "recent_cup_final"],
            "TOR": ["canadian_team"],
            "OTT": ["canadian_team"],
            "MTL": ["canadian_team"],
            "WPG": ["Canadian_team"]
        }
    },

    "FLA": {
        "primary":   ["TBL", "TOR"],
        "secondary": ["BOS", "OTT", "CAR"],
        "historic":  [],
        "modern":    ["EDM", "VGK", "BOS"],
        "reasons": {
            "TBL": ["same_division", "same_state", "sunshine_state"],
            "TOR": ["atlantic", "recent_playoffs"],
            "BOS": ["atlantic", "recent_playoffs"],
            "OTT": ["atlantic", "recent_playoffs"],
            "CAR": ["east_contention", "recent_playoffs"],
            "EDM": ["modern", "recent_cup_final"],
            "VGK": ["modern", "cup_final"],
        }
    },

    "LAK": {
        "primary":   ["ANA", "SJS", "EDM"],
        "secondary": ["VGK", "VAN", "CGY"],
        "historic":  ["CHI", "NJD", "MTL", "NYR"],
        "modern":    ["EDM", "VGK"],
        "reasons": {
            "ANA": ["same_division", "southern_california", "freeway_faceoff"],
            "SJS": ["same_division", "california"],
            "EDM": ["same_division", "recent_playoffs"],
            "VGK": ["same_division", "regional_west"],
            "VAN": ["same_division", "playoff_history"],
            "CGY": ["same_division"],
            "CHI": ["historic_playoffs"],
            "NJD": ["historic_cup_final"],
            "MTL": ["historic_cup_final"],
            "NYR": ["historic_cup_final"]
        }
    },

    "MIN": {
        "primary":   ["COL", "WPG"],
        "secondary": ["DAL", "STL", "CHI", "NSH"],
        "historic":  ["VAN"],
        "modern":    ["DAL", "VGK"],
        "reasons": {
            "COL": ["same_division", "regional"],
            "WPG": ["same_division", "regional"],
            "DAL": ["same_division", "historic_franchise_connection", "recent_playoffs"],
            "STL": ["same_division", "regional"],
            "CHI": ["regional", "historic_division"],
            "NSH": ["same_division"],
            "VAN": ["historic_playoffs"],
            "VGK": ["recent_playoffs"]
        }
    },

    "MTL": {
        "primary":   ["BOS", "TOR"],
        "secondary": ["OTT", "DET", "TBL", "EDM", "VAN", "WPG"],
        "historic":  ["NYR", "PHI", "CGY", "LAK", "CHI"],
        "modern":    ["TOR"],
        "reasons": {
            "BOS": ["original_six", "historic", "playoff_history", "atlantic"],
            "TOR": ["original_six", "atlantic", "historic", "modern"],
            "OTT": ["atlantic", "regional"],
            "DET": ["original_six", "atlantic"],
            "TBL": ["atlantic"],
            "NYR": ["original_six", "historic"],
            "PHI": ["historic_playoffs"],
            "CGY": ["historic_cup_final"],
            "LAK": ["historic_cup_final"],
            "CHI": ["original_six"],
            "EDM": ["canadian_team"],
            "VAN": ["canadian_team"],
            "WPG": ["canadian_team"]
        }
    },

    "NSH": {
        "primary":   ["DAL", "STL"],
        "secondary": ["CHI", "WPG", "MIN", "COL"],
        "historic":  ["ANA", "PIT"],
        "modern":    ["COL", "WPG"],
        "reasons": {
            "DAL": ["same_division"],
            "STL": ["same_division", "regional"],
            "CHI": ["historic_division", "playoff_history"],
            "WPG": ["same_division"],
            "MIN": ["same_division"],
            "COL": ["same_division", "recent_playoffs"],
            "ANA": ["historic_playoffs"],
            "PIT": ["historic_cup_final"]
        }
    },

    "NJD": {
        "primary":   ["NYR", "PHI"],
        "secondary": ["NYI", "CAR", "WSH"],
        "historic":  ["DET", "DAL", "LAK", "ANA"],
        "modern":    ["CAR", "NYR"],
        "reasons": {
            "NYR": ["metro", "greater_new_york", "hudson_river", "historic", "modern"],
            "PHI": ["metro", "regional"],
            "NYI": ["metro", "greater_new_york"],
            "CAR": ["metro", "recent_playoffs"],
            "WSH": ["metro"],
            "DET": ["historic_cup_final"],
            "DAL": ["historic_cup_final"],
            "LAK": ["historic_cup_final"],
            "ANA": ["historic_cup_final"]
        }
    },

    "NYI": {
        "primary":   ["NYR", "NJD"],
        "secondary": ["PHI", "PIT", "WSH"],
        "historic":  ["EDM", "TOR"],
        "modern":    ["CAR", "TBL"],
        "reasons": {
            "NYR": ["metro", "greater_new_york", "historic", "geographic"],
            "NJD": ["metro", "greater_new_york"],
            "PHI": ["metro", "historic_playoffs"],
            "PIT": ["metro"],
            "WSH": ["metro"],
            "EDM": ["historic_cup_final", "1980s_dynasty"],
            "TOR": ["historic"],
            "CAR": ["recent_playoffs"],
            "TBL": ["recent_playoffs"]
        }
    },

    "NYR": {
        "primary":   ["NYI", "NJD", "PHI"],
        "secondary": ["WSH", "PIT", "CAR"],
        "historic":  ["MTL", "VAN", "LAK", "TOR", "BOS", "CHI"],
        "modern":    ["CAR", "FLA", "NJD"],
        "reasons": {
            "NYI": ["metro", "greater_new_york", "historic", "geographic"],
            "NJD": ["metro", "greater_new_york", "historic", "modern"],
            "PHI": ["metro", "historic"],
            "WSH": ["metro"],
            "PIT": ["metro"],
            "CAR": ["metro", "recent_playoffs", "modern"],
            "MTL": ["original_six", "historic"],
            "VAN": ["historic_cup_final"],
            "LAK": ["historic_cup_final"],
            "FLA": ["modern", "recent_east_contention"],
            "TOR": ["original_six"],
            "CHI": ["original_six"],
            "BOS": ["original_six"]
        }
    },

    "OTT": {
        "primary":   ["TOR", "MTL"],
        "secondary": ["BUF", "DET", "BOS", "VAN", "CGY", "EDM", "WPG"],
        "historic":  ["PIT", "NJD"],
        "modern":    ["TOR", "DET"],
        "reasons": {
            "TOR": ["same_division", "battle_of_ontario", "historic", "modern"],
            "MTL": ["same_division", "regional"],
            "BUF": ["same_division", "regional"],
            "DET": ["same_division", "recent_tension"],
            "BOS": ["same_division"],
            "PIT": ["historic_playoffs"],
            "NJD": ["historic_playoffs"],
            "VAN": ["canadian_team"],
            "CGY": ["canadian_team"],
            "EDM": ["canadian_team"],
            "WPG": ["canadian_team"]
        }
    },

    "PHI": {
        "primary":   ["PIT", "NYR", "NJD"],
        "secondary": ["NYI", "WSH", "BOS"],
        "historic":  ["EDM", "MTL", "CHI"],
        "modern":    ["PIT", "NYR"],
        "reasons": {
            "PIT": ["metro", "same_state", "keystone_state", "historic", "modern"],
            "NYR": ["metro", "historic"],
            "NJD": ["metro", "regional"],
            "NYI": ["metro"],
            "WSH": ["metro"],
            "BOS": ["historic_east"],
            "EDM": ["historic_cup_final"],
            "MTL": ["historic_playoffs"],
            "CHI": ["historic_cup_final"]
        }
    },

    "PIT": {
        "primary":   ["PHI", "WSH", "NYR"],
        "secondary": ["CBJ", "NYI", "NJD"],
        "historic":  ["DET", "OTT", "NSH", "SJS"],
        "modern":    ["WSH", "PHI"],
        "reasons": {
            "PHI": ["metro", "same_state", "keystone_state", "historic", "modern"],
            "WSH": ["metro", "era_defining", "crosby_ovechkin"],
            "NYR": ["metro", "playoff_history"],
            "CBJ": ["metro", "regional"],
            "NYI": ["metro"],
            "NJD": ["metro"],
            "DET": ["historic_cup_final"],
            "OTT": ["historic_playoffs"],
            "NSH": ["historic_cup_final"],
            "SJS": ["historic_cup_final"]
        }
    },

    "SJS": {
        "primary":   ["LAK", "ANA", "VGK"],
        "secondary": ["VAN", "SEA", "EDM"],
        "historic":  ["DET", "STL", "DAL", "COL"],
        "modern":    ["VGK"],
        "reasons": {
            "LAK": ["same_division", "california", "historic"],
            "ANA": ["same_division", "california"],
            "VGK": ["same_division", "playoff_history", "modern"],
            "VAN": ["same_division", "playoff_history"],
            "SEA": ["same_division", "regional_west"],
            "EDM": ["same_division"],
            "DET": ["historic_playoffs"],
            "STL": ["historic_playoffs"],
            "DAL": ["historic_playoffs"],
            "COL": ["historic_playoffs"]
        }
    },

    "SEA": {
        "primary":   ["VAN", "VGK"],
        "secondary": ["EDM", "CGY", "ANA", "SJS"],
        "historic":  [],
        "modern":    ["COL", "DAL"],
        "reasons": {
            "VAN": ["same_division", "cascadia", "geographic"],
            "VGK": ["same_division", "newer_west_contention"],
            "EDM": ["same_division"],
            "CGY": ["same_division"],
            "ANA": ["same_division"],
            "SJS": ["same_division"],
            "COL": ["recent_playoffs"],
            "DAL": ["recent_playoffs"]
        }
    },

    "STL": {
        "primary":   ["CHI", "NSH"],
        "secondary": ["DAL", "COL", "MIN", "WPG"],
        "historic":  ["DET", "SJS", "BOS"],
        "modern":    ["COL", "DAL"],
        "reasons": {
            "CHI": ["regional", "historic", "midwest"],
            "NSH": ["same_division", "regional"],
            "DAL": ["same_division", "modern"],
            "COL": ["same_division", "modern"],
            "MIN": ["same_division"],
            "WPG": ["same_division"],
            "DET": ["historic_division"],
            "SJS": ["historic_playoffs"],
            "BOS": ["historic_cup_final"]
        }
    },

    "TBL": {
        "primary":   ["FLA", "TOR"],
        "secondary": ["BOS", "DET", "MTL"],
        "historic":  ["CGY", "CHI", "CBJ"],
        "modern":    ["FLA", "TOR", "NYI"],
        "reasons": {
            "FLA": ["same_division", "same_state", "sunshine_state", "modern"],
            "TOR": ["same_division", "recent_playoffs", "modern"],
            "BOS": ["same_division", "contention"],
            "DET": ["same_division", "historic_realignment_overlap"],
            "MTL": ["same_division"],
            "CGY": ["historic_cup_final"],
            "CHI": ["historic_cup_final"],
            "CBJ": ["historic_upset"],
            "NYI": ["recent_playoffs"]
        }
    },

    "TOR": {
        "primary":   ["MTL", "OTT", "BOS"],
        "secondary": ["BUF", "DET", "TBL", "FLA", "CGY", "EDM", "VAN", "WPG"],
        "historic":  ["NYI", "CHI", "DET", "NYR"],
        "modern":    ["OTT", "TBL", "FLA", "MTL"],
        "reasons": {
            "MTL": ["original_six", "historic", "atlantic", "modern"],
            "OTT": ["same_division", "battle_of_ontario", "historic", "modern"],
            "BOS": ["original_six", "atlantic", "historic"],
            "BUF": ["same_division", "regional"],
            "DET": ["original_six", "regional"],
            "TBL": ["same_division", "recent_playoffs", "modern"],
            "FLA": ["same_division", "recent_playoffs", "modern"],
            "NYI": ["historic"],
            "CHI": ["original_six"],
            "NYR": ["original_six"],
            "VAN": ["canadian_team"],
            "CGY": ["canadian_team"],
            "WPG": ["canadian_team"],
            "EDM": ["canadian_team"]
        }
    },

    "VAN": {
        "primary":   ["CGY", "EDM", "SEA"],
        "secondary": ["LAK", "SJS", "VGK", "MTL", "OTT", "TOR", "WPG"],
        "historic":  ["CHI", "NYR", "BOS"],
        "modern":    ["EDM", "VGK"],
        "reasons": {
            "CGY": ["same_division", "western_canada"],
            "EDM": ["same_division", "western_canada", "modern"],
            "SEA": ["same_division", "cascadia", "geographic"],
            "LAK": ["same_division", "playoff_history"],
            "SJS": ["same_division", "playoff_history"],
            "VGK": ["same_division", "modern"],
            "CHI": ["historic_playoffs"],
            "NYR": ["historic_cup_final"],
            "BOS": ["historic_cup_final"],
            "TOR": ["canadian_team"],
            "OTT": ["canadian_team"],
            "MTL": ["canadian_team"],
            "WPG": ["canadian_team"]
        }
    },

    "VGK": {
        "primary":   ["SJS", "LAK"],
        "secondary": ["EDM", "VAN", "SEA", "ANA"],
        "historic":  ["WSH", "FLA"],
        "modern":    ["DAL", "EDM", "COL", "SEA"],
        "reasons": {
            "SJS": ["same_division", "playoff_history", "modern"],
            "LAK": ["same_division", "regional_west"],
            "EDM": ["same_division", "west_contention", "modern"],
            "VAN": ["same_division"],
            "SEA": ["same_division", "newer_franchise_competition"],
            "ANA": ["same_division"],
            "WSH": ["historic_cup_final"],
            "FLA": ["historic_cup_final"],
            "DAL": ["modern", "recent_playoffs"],
            "COL": ["modern", "recent_playoffs"]
        }
    },

    "WSH": {
        "primary":   ["PIT", "NYR"],
        "secondary": ["CAR", "PHI", "NYI", "NJD"],
        "historic":  ["VGK", "BOS"],
        "modern":    ["PIT", "CAR", "NYR"],
        "reasons": {
            "PIT": ["metro", "era_defining", "crosby_ovechkin", "modern"],
            "NYR": ["metro", "playoff_history", "modern"],
            "CAR": ["metro", "regional", "modern"],
            "PHI": ["metro"],
            "NYI": ["metro"],
            "NJD": ["metro"],
            "VGK": ["historic_cup_final"],
            "BOS": ["historic_playoffs"]
        }
    },

    "WPG": {
        "primary":   ["MIN", "NSH"],
        "secondary": ["DAL", "COL", "STL", "CGY", "EDM", "MTL", "TOR", "OTT", "VAN"],
        "historic":  ["ANA", "VGK"],
        "modern":    ["COL", "DAL", "VGK"],
        "reasons": {
            "MIN": ["same_division", "regional"],
            "NSH": ["same_division"],
            "DAL": ["same_division", "modern"],
            "COL": ["same_division", "modern"],
            "STL": ["same_division"],
            "CGY": ["regional_canada"],
            "EDM": ["regional_canada"],
            "ANA": ["historic_playoffs"],
            "VGK": ["historic_playoffs", "modern"],
            "TOR": ["canadian_team"],
            "OTT": ["canadian_team"],
            "VAN": ["canadian_team"],
            "MTL": ["canadian_team"]
        }
    },
}


GOLD = "#c8a84b"
ICE_BLUE = "#4ab3f4"
RED = "#e74c3c"
GREEN = "#2ecc71"


possible_records = [
    (4, 0, 0),
    (3, 0, 1),
    (3, 0, 0),
    (3, 1, 0),
    (2, 0, 2),
    (2, 0, 1),
    (2, 1, 1),
    (1, 0, 3),
    (2, 0, 0),
    (2, 1, 0),
    (1, 0, 2),
    (2, 2, 0),
    (1, 1, 2),
    (0, 0, 4),
    (1, 0, 1),
    (1, 1, 1),
    (0, 0, 3),
    (1, 2, 1),
    (0, 1, 3),
    (1, 0, 0),
    (1, 1, 0),
    (0, 0, 2),
    (1, 2, 0),
    (0, 1, 2),
    (1, 3, 0),
    (0, 2, 2),
    (0, 0, 1),
    (0, 1, 1),
    (0, 2, 1),
    (0, 3, 1),
    (0, 1, 0),
    (0, 2, 0),
    (0, 3, 0),
    (0, 4, 0)
]
record_grad = gradient_merge([GREEN, RED], (len(possible_records) - 2) // 1, True)
TEAM_RECORD_COLOUR_MAP = {
    tup: dict(
        i=i+1,
        color=record_grad[i],
        score=(2 * tup[0]) + tup[2],
        pct=(0.5 * ((2 * tup[0]) + tup[2])) / sum(tup),
    ) 
    for i, tup in enumerate(possible_records)
}
TEAM_RECORD_COLOUR_MAP[(0,0,0)] = dict(i=0, color="#707070", score=0, pct=0.0)
TEAM_RECORD_COLOUR_MAP.update({str(k): v for k, v in TEAM_RECORD_COLOUR_MAP.items()})

# with st.container(horizontal=True):
#     for t, data in TEAM_RECORD_COLOUR_MAP.items():
#         st.color_picker(str(t), value=data["color"], key=f"{t}_{type(t)}", disabled=True)


# ═══════════════════════════════════════════════════════════
# JERSEY COLLECTION MODULE
# ═══════════════════════════════════════════════════════════

@st.cache_data(ttl=None)
def load_jersey_data(filepath: str) -> pd.DataFrame:
    """Load jersey Excel workbook (skiprows=1 for header offset)."""
    ext = str(filepath).lower()
    if ext.endswith(".xlsx") or ext.endswith(".xls"):
        df = pd.read_excel(filepath)
    else:
        df = pd.read_csv(filepath, encoding="utf-8-sig")
    df.columns = df.columns.str.strip()
    # Drop unnamed first column if present
    if df.columns[0] == "" or df.columns[0].startswith("Unnamed"):
        df = df.iloc[:, 1:]

    # Date parsing
    for col in ["OrderDate", "ReceiveDate", "OpenDate"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    df["PriceF"] = df.apply(
        lambda r:
            (
                (
                    (
                        r["ExchangeRate"] * (
                            r["StickerPriceUS"]
                            + (r["Shipping"] if (str(r["Shipping"]).lower() not in ["nan", "0", "0.0", "none"]) else 0)
                            + (r["Tax"] if (str(r["Tax"]).lower() not in ["nan", "0", "0.0", "none"]) else 0)
                        )
                    )
                    + (r["Duty"] if (str(r["Duty"]).lower() not in ["nan", "0", "0.0", "none"]) else 0)
                    - (r["Discount"] if (str(r["Discount"]).lower() not in ["nan", "0", "0.0", "none"]) else 0)
                ) if (str(r["StickerPriceUS"]).lower() not in ["nan", "0", "0.0", "none"]) else (
                    (
                        (
                            r["StickerPriceCDN"]
                            + (r["Duty"] if (str(r["Duty"]).lower() not in ["nan", "0", "0.0", "none"]) else 0)
                            + (r["Shipping"] if (str(r["Shipping"]).lower() not in ["nan", "0", "0.0", "none"]) else 0)
                            + (r["Tax"] if (str(r["Tax"]).lower() not in ["nan", "0", "0.0", "none"]) else 0)
                        )
                        - (r["Discount"] if (str(r["Discount"]).lower() not in ["nan", "0", "0.0", "none"]) else 0)
                    ) if (str(r["StickerPriceCDN"]).lower() not in ["nan", "0", "0.0", "none"]) else -1
                )
            )
        , axis=1
    )

    # Numeric
    for col in ["PriceC", "PriceM", "PriceF", "StickerPriceCDN", "StickerPriceUS",
                "Duty", "Shipping", "Discount", "Tax", "ExchangeRate", "NHLID"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Bool
    if "Cancelled" in df.columns:
        df["Cancelled"] = df["Cancelled"].astype(str).str.lower().isin(["true", "yes", "1"])

    # Derived fields
    if "OrderDate" in df.columns and "ReceiveDate" in df.columns:
        df["DaysToReceive"] = (df["ReceiveDate"] - df["OrderDate"]).dt.days

    if "ReceiveDate" in df.columns and "OpenDate" in df.columns:
        df["DaysToOpen"] = (df["OpenDate"] - df["ReceiveDate"]).dt.days

    if "OrderDate" in df.columns:
        df["OrderYear"]  = df["OrderDate"].dt.year
        df["OrderMonth"] = df["OrderDate"].dt.to_period("M").astype(str)

    # Player name
    df["PlayerName"] = (
        df.get("PlayerFirst", pd.Series([""] * len(df))).fillna("").astype(str).str.strip()
        + " " +
        df.get("PlayerLast", pd.Series([""] * len(df))).fillna("").astype(str).str.strip()
    ).str.strip()
    # df["PlayerName"] = df["PlayerName"].replace("", pd.NA)
    df["NHLID"] = df["NHLID"].fillna(0)
    df["NHLID"] = df["NHLID"].astype(int)

    return df


@st.cache_data(ttl=86400)
def fetch_nhl_player(nhl_id: int) -> dict:
    """Fetch player bio + stats from NHL API v1."""
    try:
        # Bio
        bio_url = f"https://api-web.nhle.com/v1/player/{nhl_id}/landing"
        r = requests.get(bio_url, timeout=8)
        if r.status_code != 200:
            return {}
        data = r.json()

        bio = {
            "name":        data.get("firstName", {}).get("default", "") + " " + data.get("lastName", {}).get("default", ""),
            "headshot":    data.get("headshot", ""),
            "position":    data.get("position", ""),
            "birthCity":   data.get("birthCity", {}).get("default", "") if isinstance(data.get("birthCity"), dict) else data.get("birthCity", ""),
            "birthCountry":data.get("birthCountry", ""),
            "birthDate":   data.get("birthDate", ""),
            "nationality": data.get("nationality", ""),
            "heightFeet":  data.get("heightInFeet", ""),
            "heightInches":data.get("heightInInches", ""),
            "weightPounds":data.get("weightInPounds", ""),
            "shoots":      data.get("shootsCatches", ""),
            "draftYear":   data.get("draftDetails", {}).get("year", ""),
            "draftRound":  data.get("draftDetails", {}).get("round", ""),
            "draftPick":   data.get("draftDetails", {}).get("pickInRound", ""),
            "draftTeam":   data.get("draftDetails", {}).get("teamAbbrev", ""),
            "currentTeam": data.get("currentTeamAbbrev", ""),
            "sweaterNo":   data.get("sweaterNumber", ""),
            "isRetired":   data.get("isRetired", False),
        }

        # Career regular-season stats (last available season)
        stats_list = data.get("featuredStats", {}).get("regularSeason", {}).get("career", {})
        if not stats_list:
            stats_list = data.get("careerTotals", {}).get("regularSeason", {})

        bio["stats"] = stats_list

        # Bio blurb — try from bio block
        bio["bio"] = data.get("biography", {}).get("default", "") if isinstance(data.get("biography"), dict) else ""

        return bio
    except Exception:
        return {}


def get_jersey_image_paths(jersey_id, base_path: str) -> list:
    """Return list of local image paths for a jersey ID."""
    import os, glob
    j_folder = f"J_{int(jersey_id):03d}"
    folder = os.path.join(base_path, j_folder)
    if not os.path.isdir(folder):
        return []
    # f"{folder=}, {jersey_id=}"
    imgs = sorted(
        glob.glob(os.path.join(folder, "*.jpg")) +
        glob.glob(os.path.join(folder, "*.jpeg")) +
        glob.glob(os.path.join(folder, "*.png")) +
        glob.glob(os.path.join(folder, "*.JPG")) +
        glob.glob(os.path.join(folder, "*.JPEG"))
    )
    return list(set(imgs))


def render_jersey_card(row, base_img_path: str, show_player_data: bool = True):
    """Render a single jersey card with image, details, and optional player info."""
    jersey_id = row.get("ID", "?")
    player    = row.get("PlayerName", "")
    team      = row.get("Team", "Unknown")
    league    = row.get("League", "NHL")
    number    = row.get("Number", "")
    brand     = row.get("Brand", "")
    model     = row.get("Model", "")
    make      = row.get("Make", "")
    size      = row.get("Size", "")
    price     = row.get("PriceF", None)
    nhl_id    = row.get("NHLID", None)
    order_dt  = row.get("OrderDate", None)
    
    k_jersey: str = ''.join(map(str, [jersey_id, player, team, league, number, brand, model, make, size, price, nhl_id, order_dt]))

    # Colour chips
    colours = [str(row.get(c, "")) for c in ["Colour1", "Colour2", "Colour3"] if row.get(c, "")]
    colour_map = {
        "Red": "#c0392b", "Black": "#1a1a1a", "White": "#f0f0f0",
        "Blue": "#2980b9", "Gold": "#f1c40f", "Yellow": "#f1c40f",
        "Green": "#27ae60", "Dark Green": "#1a5e2b", "Teal": "#16a085",
        "Navy": "#1a237e", "Orange": "#e67e22", "Purple": "#8e44ad",
        "Grey": "#7f8c8d", "Silver": "#bdc3c7", "Bronze": "#cd7f32",
    }
    colour_chips = "".join([
        f'<span style="display:inline-block;width:14px;height:14px;border-radius:3px;'
        f'background:{colour_map.get(c,"#888")};border:1px solid #333;margin-right:3px;'
        f'vertical-align:middle" title="{c}"></span>'
        for c in colours if c
    ])

    # Team logo
    team_abbr = ""
    for abbr, meta in TEAM_META.items():
        # if meta["name"].lower() in team.lower() or abbr.lower() in team.lower():
        if meta["name"].lower() == team.lower():
            team_abbr = abbr
            break
    logo_html = "<div></div>"
    if team_abbr:
        logo_url = fetch_team_logo(team_abbr)
        logo_html = f'<img src="{logo_url}" width="36" style="vertical-align:middle;margin-right:8px">'

    # Jersey images
    img_paths = get_jersey_image_paths(jersey_id, base_img_path) if jersey_id != "?" else []

    markdown = f"""
    <div style="background:#0d1f35;border:1px solid #1e3a5a;border-radius:10px;padding:16px;margin-bottom:12px">
        <div style="display:flex;align-items:center;margin-bottom:8px">
            {logo_html}
            <div>
                <span style="font-family:'Bebas Neue',sans-serif;font-size:1.3rem;color:#c8a84b;letter-spacing:2px">
                    {"#" + str(int(number)) + " " if str(number).strip() not in ["","nan"] else ""}{player if player else team}
                </span>
                <span style="color:#8899aa;font-size:0.8rem;margin-left:8px">{team} · {league}</span>
            </div>
        </div>
        <div style="color:#ccd6e0;font-size:0.82rem;line-height:1.7">
            <b>ID:</b> J_{int(jersey_id):03d} &nbsp;|&nbsp;
            <b>Brand:</b> {brand} {make} &nbsp;|&nbsp;
            <b>Model:</b> {model} &nbsp;|&nbsp;
            <b>Size:</b> {size}<br>
            <b>Colours:</b> {colour_chips} {", ".join(colours)}<br>
            {"<b>Cost:</b> $" + f"{price:.2f}" + " CAD &nbsp;|&nbsp;" if pd.notna(price) else ""}
            {"<b>Ordered:</b> " + order_dt.strftime("%b %d, %Y") if pd.notna(order_dt) else ""}
        </div>
    </div>
    """
    # st.code(markdown, language="HTML", line_numbers=True)
    st.markdown(markdown, unsafe_allow_html=True)

    # Jersey photos
    if img_paths:
        if len(img_paths) > 3:
            lst_cols_to_make = [1] + [8 for _ in range(3)] + [1]
            # st.write(img_paths)
        else:
            lst_cols_to_make = [1 for _ in range(min(len(img_paths), 3))]
            
        with st.expander(f"{len(img_paths)} Jersey Images:", expanded=False):
            cols_img = st.columns(lst_cols_to_make)
            k_images_start: str = f"key_images_start_{k_jersey}"
            i_images_start = st.session_state.setdefault(k_images_start, 0)
            # st.write(f"{len(img_paths)=}, {i_images_start=}, {k_images_start=}")
            if len(img_paths) > 3:
                with cols_img[0]:
                    if st.button("<", key=f"prev_image_{k_jersey}", disabled=i_images_start==0):
                        st.session_state.update({k_images_start: max(0, i_images_start - 1)})
                        st.rerun()
                    if st.button("|<", key=f"first_image_{k_jersey}", disabled=i_images_start==0):
                        st.session_state.update({k_images_start: 0})
                        st.rerun()
                with cols_img[4]:
                    if st.button("\>", key=f"next_image_{k_jersey}", disabled=i_images_start==(len(img_paths)-3)):
                        st.session_state.update({k_images_start: max(0, i_images_start + 1)})
                        st.rerun()
                    if st.button("\>|", key=f"last_image_{k_jersey}", disabled=i_images_start==(len(img_paths)-3)):
                        st.session_state.update({k_images_start: len(img_paths)-3})
                        st.rerun()
            for i, p in enumerate(img_paths[i_images_start: i_images_start + 3]):
                with cols_img[i + int(bool(len(img_paths) > 3))]:
                    try:
                        st.image(p, use_container_width=True, caption=f"{i_images_start+i+1} / {len(img_paths)} -- '{p}'")
                    except Exception:
                        st.caption(f"📷 {p.split('/')[-1].split(chr(92))[-1]}")
    else:
        st.caption("📷 No local images found for this jersey.")

    # Player data
    if show_player_data and pd.notna(nhl_id) and league in ("NHL", "PWHL"):
        nhl_id_int = int(nhl_id)
        player_data = fetch_nhl_player(nhl_id_int)
        if player_data:
            render_player_panel(player_data, league)


def render_player_panel(pd_data: dict, league: str):
    """Render player bio and stats panel."""
    headshot = pd_data.get("headshot", "")
    name     = pd_data.get("name", "").strip()
    birth    = pd_data.get("birthDate", "")
    city     = pd_data.get("birthCity", "")
    country  = pd_data.get("birthCountry", "")
    stats    = pd_data.get("stats", {})
    bio_text = pd_data.get("bio", "")

    # Age calculation
    age_str = ""
    try:
        bd = datetime.strptime(birth, "%Y-%m-%d")
        age = (datetime.now() - bd).days // 365
        age_str = f"{age} years old"
    except Exception:
        age_str = ""

    col_hs, col_bio = st.columns([1, 4])
    with col_hs:
        if headshot:
            st.image(headshot, width=90)
    with col_bio:
        retired = pd_data.get("isRetired", False)
        badge = "🏒 Active" if not retired else "🎽 Retired"
        draft_info = ""
        if pd_data.get("draftYear"):
            draft_info = f"  |  Drafted {pd_data['draftYear']} Rd {pd_data.get('draftRound','')} #{pd_data.get('draftPick','')} by {pd_data.get('draftTeam','')}"

        st.markdown(f"""
        <div style="background:#081420;border-left:3px solid #c8a84b;padding:10px 14px;border-radius:0 6px 6px 0;margin-bottom:6px">
            <div style="font-family:'Bebas Neue',sans-serif;font-size:1.1rem;color:#c8a84b">{name} <span style="font-size:0.75rem;color:#8899aa">{badge}</span></div>
            <div style="color:#aabbcc;font-size:0.8rem">
                {pd_data.get('position','').upper()} · {pd_data.get('shoots','')} · 
                {str(pd_data.get('heightFeet',''))}\'{str(pd_data.get('heightInches',''))}\" · 
                {pd_data.get('weightPounds','')} lbs
            </div>
            <div style="color:#8899aa;font-size:0.78rem;margin-top:2px">
                📍 {city}{", " + country if country else ""} · 🎂 {birth} ({age_str}){draft_info}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Career stats
    if stats:
        pos = pd_data.get("position", "G").upper()
        if pos == "G":
            stat_items = [
                ("GP", stats.get("gamesPlayed", "—")),
                ("W",  stats.get("wins", "—")),
                ("L",  stats.get("losses", "—")),
                ("OTL",stats.get("otLosses", "—")),
                ("GAA",f"{stats.get('goalsAgainstAvg', 0):.2f}" if stats.get('goalsAgainstAvg') else "—"),
                ("SV%",f"{stats.get('savePctg', 0):.3f}" if stats.get('savePctg') else "—"),
                ("SO", stats.get("shutouts", "—")),
            ]
        else:
            stat_items = [
                ("GP",  stats.get("gamesPlayed", "—")),
                ("G",   stats.get("goals", "—")),
                ("A",   stats.get("assists", "—")),
                ("PTS", stats.get("points", "—")),
                ("+/-", stats.get("plusMinus", "—")),
                ("PIM", stats.get("pim", "—")),
                ("PPG", stats.get("powerPlayGoals", "—")),
                ("SHG", stats.get("shorthandedGoals", "—")),
            ]
        cols_s = st.columns(len(stat_items))
        for i, (label, val) in enumerate(stat_items):
            with cols_s[i]:
                st.markdown(f"""
                <div style="text-align:center;background:#0a1828;border:1px solid #1e3a5a;border-radius:5px;padding:5px 3px">
                    <div style="font-family:'Bebas Neue';font-size:1.2rem;color:#c8a84b">{val}</div>
                    <div style="font-size:0.65rem;color:#8899aa">{label}</div>
                </div>
                """, unsafe_allow_html=True)

    # Bio blurb
    if bio_text and len(bio_text) > 20:
        with st.expander("📖 Player Bio"):
            st.markdown(f'<div style="color:#aabbcc;font-size:0.82rem;line-height:1.6">{bio_text}</div>', unsafe_allow_html=True)


def to_string(
    row: pd.Series | dict,
    inc_team: Optional[bool] = None,
    inc_brand: Optional[bool] = None,
    inc_make: Optional[bool] = None,
    inc_model: Optional[bool] = None,
    inc_num: Optional[bool] = None,
    inc_fname: Optional[bool] = None,
    inc_lname: Optional[bool] = None,
    inc_size: Optional[bool] = None
) -> str:
    res = []
    if inc_team is None:
        inc_team = True
    if inc_brand is None:
        inc_brand = True
    if inc_make is None:
        inc_make = True
    if inc_model is None:
        inc_model = True
    
    is_blank: bool = pd.isna(row["Number"])

    if inc_num is None:
        inc_num = not is_blank
    if inc_fname is None:
        inc_fname = not is_blank
    if inc_lname is None:
        inc_lname = not is_blank

    if inc_size is None:
        inc_size = True

    team = row["Team"]
    brand = row["Brand"]
    make = row["Make"]
    model = row["Model"]
    number = row["Number"]
    player_first = row["PlayerFirst"]
    player_last = row["PlayerLast"]
    size = row["Size"]

    if inc_team and bool(team):
        res.append(team)
    if inc_brand and bool(brand):
        res.append(brand)
    if inc_make and bool(make):
        res.append(make)
    if inc_model and bool(model):
        res.append(model)
    if inc_num and bool(number):
        res.append(f"#{number}")
    if inc_fname and bool(player_first):
        res.append(player_first)
    if inc_lname and bool(player_last):
        res.append(player_last)
    if inc_size and bool(size):
        res.append(size)
    return " ".join(map(str, res))


def page_jersey_collection(df_jerseys: pd.DataFrame, base_img_path: str):
    """Full Jersey Collection page."""
    
    if st.session_state.get("user") is None:

        if "user" not in st.session_state:
            st.session_state.user = None
            
        show_login_register()
        st.stop()
    elif st.session_state.get("user", "").lower() != "avery":
        st.info("You do not currently have permission to view this screen.")
        st.stop()
    
    st.markdown('<div class="section-header">🧥 JERSEY COLLECTION</div>', unsafe_allow_html=True)
    
    # st.write("df_jerseys")
    # st.dataframe(df_jerseys)
    # st.write("'" + ("', '".join(df_jerseys["PlayerName"].values)) + "'")

    active = df_jerseys[df_jerseys.get("Cancelled", pd.Series([False]*len(df_jerseys))).fillna(False) != True].copy()
    for c in ["Order", "Receive", "Open"]:
        col = f"{c}Date"
        active[col] = active[col].dt.date
    
    # st.write("active")
    # st.dataframe(active)
    # st.write("'" + ("', '".join(active["PlayerName"].values)) + "'")
    
    active["ImagePaths"] = active["ID"].apply(lambda id_: get_jersey_image_paths(id_, base_img_path))
    
    st.write(f"active")
    st.write(active)
    
    total_jerseys = len(active)
    total_value   = active["PriceF"].sum() if "PriceF" in active.columns else 0
    with_player   = (~active["PlayerName"].str.strip().isin(["nan", "none", ""])).sum()
    blank_jerseys = total_jerseys - with_player
    # with_images   = sum(1 for _, r in active.iterrows() if get_jersey_image_paths(r.get("ID", -1), base_img_path))
    # need_images = active.loc[bool(len(get_jersey_image_paths(active.get("ID", -1), base_img_path)))]
    # need_images = active.loc[len(np.where(get_jersey_image_paths(active.get("ID", -1), base_img_path)) > 0)]
    # need_images = active.loc[(pd.isna(active["ImagePaths"])) | (len(active["ImagePaths"]) == 0)]
    need_images = active.loc[active["ImagePaths"].map(len) == 0]
    st.write(f"need_images")
    st.write(need_images)
    with_images   = len(active) - len(need_images)
    missing_price = len(active) - len(active[active["PriceF"] > 0])

    # Top KPIs
    k1, k2, k3, k4, k5, k6 = st.columns(6)
    k1.metric("Total Jerseys", total_jerseys)
    k2.metric("Collection Value", f"${total_value:,.0f} CAD" if total_value > 0 else "—")
    k3.metric("Player Jerseys", with_player)
    k4.metric("Blank Jerseys", blank_jerseys)
    k5.metric("With Photos", with_images)
    k6.metric("Missing Price", missing_price)

    st.markdown("---")
    
    options_pills_jersey_collection_mode = [
        "📊 Collection Stats",
        "🔍 Browse Jerseys",
        "📅 Timeline",
        "💰 Cost Analysis",
        "Checklist"
    ]
    k_pills_jersey_collection_mode: str = "key_pills_jersey_collection_mode"
    st.session_state.setdefault(k_pills_jersey_collection_mode, 0)
    pills_jersey_collection_mode = pills(
        label="Mode",
        options=options_pills_jersey_collection_mode,
        key=k_pills_jersey_collection_mode,
        index=0,
        label_visibility="hidden"
    )

    # ══════════════════════════════════════════════
    # TAB 1: COLLECTION STATS
    # ══════════════════════════════════════════════
    if pills_jersey_collection_mode == options_pills_jersey_collection_mode[0]:
        # 📊 Collection Stats
        st.markdown('<div class="section-header" style="font-size:1.2rem">COLLECTION STATISTICS</div>', unsafe_allow_html=True)

        col_l, col_r = st.columns(2)

        # By League
        with col_l:
            if "League" in active.columns:
                league_cnt = active["League"].value_counts().reset_index()
                league_cnt.columns = ["League", "Count"]
                fig_league = px.pie(
                    league_cnt, names="League", values="Count",
                    title="By League", hole=0.5,
                    color_discrete_sequence=px.colors.qualitative.Set2
                )
                fig_league.update_layout(**DARK_THEME, height=300, margin=dict(l=10,r=10,t=40,b=10))
                st.plotly_chart(fig_league, use_container_width=True)

        # By Brand
        with col_r:
            if "Brand" in active.columns:
                brand_cnt = active["Brand"].fillna("Unknown").value_counts().reset_index()
                brand_cnt.columns = ["Brand", "Count"]
                fig_brand = px.bar(
                    brand_cnt, x="Count", y="Brand", orientation="h",
                    title="By Brand / Manufacturer",
                    color="Count", color_continuous_scale=[[0, ICE_BLUE], [1, GOLD]],
                    text="Count"
                )
                fig_brand.update_traces(textposition="outside")
                fig_brand.update_layout(**DARK_THEME, coloraxis_showscale=False,
                                        height=300, margin=dict(l=10,r=10,t=40,b=10))
                st.plotly_chart(fig_brand, use_container_width=True)

        col_l2, col_r2 = st.columns(2)

        # By Team
        with col_l2:
            if "Team" in active.columns:
                team_cnt = active["Team"].fillna("Unknown").value_counts().head(20).reset_index()
                team_cnt.columns = ["Team", "Count"]
                fig_team = px.bar(
                    team_cnt, x="Count", y="Team", orientation="h",
                    title="Top Teams in Collection",
                    color="Count", color_continuous_scale=[[0, RED], [0.5, GOLD], [1, GREEN]],
                    text="Count"
                )
                fig_team.update_traces(textposition="outside")
                fig_team.update_layout(**DARK_THEME, coloraxis_showscale=False,
                                       height=max(300, len(team_cnt)*28 + 60))
                st.plotly_chart(fig_team, use_container_width=True)

        # By Jersey Type / Model
        with col_r2:
            if "Model" in active.columns:
                model_cnt = active["Model"].fillna("Unknown").value_counts().reset_index()
                model_cnt.columns = ["Model", "Count"]
                fig_model = px.pie(
                    model_cnt, names="Model", values="Count",
                    title="By Jersey Model / Type", hole=0.45,
                    color_discrete_sequence=px.colors.qualitative.Plotly
                )
                fig_model.update_layout(**DARK_THEME, height=350, margin=dict(l=10,r=10,t=40,b=10))
                st.plotly_chart(fig_model, use_container_width=True)

        col_l3, col_r3 = st.columns(2)

        # By Make (PrimeGreen, Blue-Line etc)
        with col_l3:
            if "Make" in active.columns:
                make_cnt = active["Make"].fillna("Unknown").value_counts().reset_index()
                make_cnt.columns = ["Make", "Count"]
                fig_make = px.bar(
                    make_cnt, x="Make", y="Count",
                    title="By Make / Tier",
                    color="Count", color_continuous_scale=[[0, ICE_BLUE], [1, GOLD]],
                    text="Count"
                )
                fig_make.update_traces(textposition="outside")
                fig_make.update_layout(**DARK_THEME, coloraxis_showscale=False, height=320)
                st.plotly_chart(fig_make, use_container_width=True)

        # By Supplier
        with col_r3:
            if "Supplier" in active.columns:
                sup_cnt = active["Supplier"].fillna("Unknown").value_counts().head(15).reset_index()
                sup_cnt.columns = ["Supplier", "Count"]
                fig_sup = px.bar(
                    sup_cnt, x="Count", y="Supplier", orientation="h",
                    title="By Supplier / Store",
                    color="Count", color_continuous_scale=[[0, "#8e44ad"], [1, GOLD]],
                    text="Count"
                )
                fig_sup.update_traces(textposition="outside")
                fig_sup.update_layout(**DARK_THEME, coloraxis_showscale=False,
                                      height=max(280, len(sup_cnt)*30 + 60))
                st.plotly_chart(fig_sup, use_container_width=True)

        # By Nationality of player
        if "Nationality" in active.columns:
            nat_cnt = active["Nationality"].dropna().value_counts().reset_index()
            nat_cnt.columns = ["Nationality", "Count"]
            fig_nat = px.bar(
                nat_cnt, x="Nationality", y="Count",
                title="Player Nationality in Collection",
                color="Count", color_continuous_scale=[[0, ICE_BLUE], [1, GOLD]],
                text="Count"
            )
            fig_nat.update_traces(textposition="outside")
            fig_nat.update_layout(**DARK_THEME, coloraxis_showscale=False, height=320)
            st.plotly_chart(fig_nat, use_container_width=True)

        # By Position
        if "Position" in active.columns:
            pos_cnt = active["Position"].dropna().value_counts().reset_index()
            pos_cnt.columns = ["Position", "Count"]
            fig_pos = px.pie(
                pos_cnt, names="Position", values="Count",
                title="Player Positions in Collection", hole=0.45,
                color_discrete_sequence=[GOLD, ICE_BLUE, GREEN, RED]
            )
            fig_pos.update_layout(**DARK_THEME, height=300)
            st.plotly_chart(fig_pos, use_container_width=True)

        # Size distribution
        if "Size" in active.columns:
            size_cnt = active["Size"].fillna("Unknown").astype(str).value_counts().reset_index()
            size_cnt.columns = ["Size", "Count"]
            fig_size = px.bar(
                size_cnt.sort_values("Count", ascending=False), x="Size", y="Count",
                title="Jersey Size Distribution",
                color="Count",
                color_continuous_scale=[[0, ICE_BLUE], [1, GOLD]],
                text="Count"
            )
            fig_size.update_xaxes(type="category")
            fig_size.update_traces(textposition="outside")
            fig_size.update_layout(**DARK_THEME, coloraxis_showscale=False, height=300)
            st.plotly_chart(fig_size, use_container_width=True)
            
        cols_names = st.columns(3)
        active_player = active.copy()
        active_player = active_player[~pd.isna(active_player["PlayerLast"]) & (active_player["PlayerLast"].str not in [None, ""])]
        for i, col in enumerate(["PlayerLast", "PlayerFirst", "Number"]):
            with cols_names[i]:
                lname_cnt = active_player[col].fillna("Unknown").value_counts().reset_index()
                lname_cnt.columns = [col, "Count"]
                fig_lname = px.bar(
                    lname_cnt, x="Count", y=col, orientation="h",
                    title=f"By {col}",
                    color="Count", color_continuous_scale=[[0, "#8e44ad"], [1, GOLD]],
                    text="Count"
                )
                fig_lname.update_traces(textposition="outside")
                fig_lname.update_layout(**DARK_THEME, coloraxis_showscale=False,
                                        height=max(280, len(lname_cnt)*30 + 60))
                st.plotly_chart(fig_lname, use_container_width=True)
    
        active_letters = pd.DataFrame(dict(zip([chr(i) for i in range(97, 97+26)], [[0] for i in range(26)])))
        active_letters[[".", " ", "-", "'"]] = [0, 0, 0, 0]
        for i, row in active_player.iterrows():
            for c in row["PlayerLast"].lower():
                active_letters.at[0, c] += 1
        active_letters = active_letters.T.reset_index()
        # # lname_cnt = active_letters[].fillna("Unknown").value_counts().head(15).reset_index()
        active_letters.columns = ["Letter", "Count"]
        fig_lname = px.bar(
            active_letters, x="Count", y="Letter", orientation="h",
            title=f"By Letter",
            color="Count", color_continuous_scale=[[0, "#8e44ad"], [1, GOLD]],
            text="Count"
        )
        fig_lname.update_traces(textposition="outside")
        fig_lname.update_layout(**DARK_THEME, coloraxis_showscale=False,
                                height=max(280, len(active_letters)*30 + 60))
        st.plotly_chart(fig_lname, use_container_width=True)

    # ══════════════════════════════════════════════
    # TAB 2: BROWSE JERSEYS
    # ══════════════════════════════════════════════
    elif pills_jersey_collection_mode == options_pills_jersey_collection_mode[1]:
        # 🔍 Browse Jerseys
        st.markdown('<div class="section-header" style="font-size:1.2rem">BROWSE & SEARCH</div>', unsafe_allow_html=True)

        # Filters
        fc1, fc2, fc3, fc4 = st.columns(4)
        with fc1:
            leagues_avail = sorted(active["League"].dropna().unique()) if "League" in active.columns else []
            sel_league = st.multiselect("League", leagues_avail, default=leagues_avail)
        with fc2:
            teams_avail = sorted(active["Team"].dropna().unique()) if "Team" in active.columns else []
            sel_team = st.multiselect("Team", teams_avail, default=[])
        with fc3:
            brands_avail = sorted(active["Brand"].dropna().unique()) if "Brand" in active.columns else []
            sel_brand = st.multiselect("Brand", brands_avail, default=[])
        with fc4:
            player_search = st.text_input("Search player name", "")

        fc5, fc6, fc7 = st.columns(3)
        has_player_filter = fc5.checkbox("Has player name", value=False)
        show_player_info  = fc6.checkbox("Load player data from NHL API", value=True,
                                        help="Fetches live data — may be slow for many jerseys")
        has_image_filter = fc7.checkbox("Has image(s)", value=False)

        # Apply filters
        filtered = active.copy()
        if sel_league:
            filtered = filtered[filtered["League"].isin(sel_league)]
        if sel_team:
            filtered = filtered[filtered["Team"].isin(sel_team)]
        if sel_brand:
            filtered = filtered[filtered["Brand"].isin(sel_brand)]
        if has_player_filter:
            filtered = filtered[filtered["PlayerName"].notna()]
        if player_search:
            filtered = filtered[
                filtered["PlayerName"].fillna("").str.lower().str.contains(player_search.lower())
            ]
        if has_image_filter:
            filtered = filtered[filtered["ImagePaths"].map(len) != 0]

        st.caption(f"Showing {len(filtered)} of {total_jerseys} jerseys")

        # Sort
        sort_col, sort_dir = st.columns([3, 1])
        with sort_col:
            sort_by = st.selectbox("Sort by", ["OrderDate", "PriceF", "Team", "PlayerLast", "League", "ID"], index=0)
        with sort_dir:
            asc = st.selectbox("Direction", ["Desc", "Asc"], index=0) == "Asc"

        if sort_by in filtered.columns:
            filtered = filtered.sort_values(sort_by, ascending=asc, na_position="last")

        # st.write(f"filtered")
        # st.write(filtered)
        # print(f"filtered")
        # print(filtered)
        
        cols_paginataion = st.columns([0.65, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05])
        k_page: str = "page_number"
        cards_per_page = 3
        n_pages = int(math.ceil(filtered.shape[0] / cards_per_page))
        page_num = st.session_state.setdefault(k_page, 0)
        with cols_paginataion[1]:
            if st.button("|<"):
                st.session_state.update({k_page: 0})
                st.rerun()
        with cols_paginataion[2]:
            if st.button(f"-{cards_per_page} <"):
                st.session_state.update({k_page: max(0, page_num - cards_per_page)})
                st.rerun()
        with cols_paginataion[3]:
            if st.button("<"):
                st.session_state.update({k_page: max(0, page_num - 1)})
                st.rerun()
        with cols_paginataion[4]:
            st.write(f"{page_num + 1} / {n_pages}")
        with cols_paginataion[5]:
            if st.button("\>"):
                st.session_state.update({k_page: min(n_pages - 1, page_num + 1)})
                st.rerun()
        with cols_paginataion[6]:
            if st.button(f"\> {cards_per_page}"):
                st.session_state.update({k_page: min(n_pages - 1, page_num + cards_per_page)})
                st.rerun()
        with cols_paginataion[7]:
            if st.button("\>|"):
                st.session_state.update({k_page: n_pages - 1})
                st.rerun()
        i_a = cards_per_page * page_num
        i_b = (cards_per_page * (page_num + 1)) - 1
        
        filtered = filtered[i_a: i_b + 1]
        
        # st.write(f"{page_num=}, {i_a=}, {i_b=}, {filtered.shape=}")

        # Render jersey cards
        for _, row in filtered.head(cards_per_page).iterrows():
            with st.container():
                # st.write(f"row")
                # st.write(row)
                # print(f"row")
                # print(row)
                render_jersey_card(row, base_img_path, show_player_data=show_player_info)
                st.markdown("---")

    # ══════════════════════════════════════════════
    # TAB 3: TIMELINE
    # ══════════════════════════════════════════════
    # with tab_timeline:
    elif pills_jersey_collection_mode == options_pills_jersey_collection_mode[2]:
        # 📅 Timeline
        st.markdown('<div class="section-header" style="font-size:1.2rem">ACQUISITION TIMELINE</div>', unsafe_allow_html=True)
        
        active_timeline = active.rename(columns={
            "ID": "JerseyID",
            "Brand": "BrandName",
            "Make": "JerseyMake"
        })
        active_timeline["Colours"] = active_timeline.apply(
            lambda r:
                ", ".join([c for c in r[["Colour1", "Colour2", "Colour3"]] if str(c).lower().strip() not in ["none", "nan", ""]])
            , axis=1
        )
        cols_timeline_order_open = ["OrderDate", "OpenDate", "JerseyID"]
        # st.write("active_timeline")
        # st.write(active_timeline)
        df_timeline_order_open = active_timeline[cols_timeline_order_open]
        # st.dataframe(df_timeline_order_open)
        # df_timeline_order_receive["Event"] = df_timeline_order_receive.apply(lambda row: print(f"{row=}"))
        # df_timeline_order_receive["Event"] = df_timeline_order_receive.apply(lambda row: print(f"{row=}"))
        df_timeline_order_open = df_timeline_order_open.rename(
            columns={"OrderDate": "Start Date", "OpenDate": "End Date"})

        df_timeline_order_open['Start Date'] = pd.to_datetime(df_timeline_order_open['Start Date'])
        df_timeline_order_open["Category"] = df_timeline_order_open.apply(lambda row: "Yet To Open" if pd.isna(row["End Date"]) else "Opened", axis=1)
        df_timeline_order_open['End Date'] = pd.to_datetime(df_timeline_order_open['End Date']).fillna(pd.Timestamp.now())
        df_timeline_order_open["DDiff"] = df_timeline_order_open.apply(lambda row: (row["End Date"] - row["Start Date"]).days, axis=1)
        df_timeline_order_open["Event"] = df_timeline_order_open.apply(
            lambda row:
                ", ".join(map(str, active_timeline.loc[
                        active_timeline["JerseyID"] == row["JerseyID"],
                    ["Number", "PlayerFirst", "PlayerLast", "Team", "BrandName", "JerseyMake", "Colours"]
                    ].iloc[0].values)) + " Dates between: " + str(row["DDiff"]),
            axis=1
        )
        del df_timeline_order_open["JerseyID"]
        df_timeline_order_open.sort_values(
            by=["End Date", "DDiff"],
            inplace=True
        )

        # Create a Gantt-like timeline using Plotly
        fig_timeline_order_open = px.timeline(
            df_timeline_order_open,
            x_start='Start Date',
            x_end='End Date',
            y='Event',
            title='Time Between Order to Open date',
            color='Category',
            color_discrete_map={
                'Yet To Open': 'red',
                'Medium': 'orange',
                'Opened': 'green'
            }
        )

        # Update layout to make it more readable
        fig_timeline_order_open.update_layout(xaxis_title="Date", yaxis_title="Order Date to Open Date", height=1500)

        # Display in Streamlit
        st.plotly_chart(fig_timeline_order_open)

        timeline_df = active.dropna(subset=["OrderDate"]).copy()
        timeline_df["Label"] = timeline_df.apply(
            lambda r: (
                f"#{int(r['Number'])} " if str(r.get("Number","")).strip() not in ["","nan"] else ""
            ) + (r.get("PlayerName") or r.get("Team","?")) + f" ({r.get('Team','?')})",
            axis=1
        )
        timeline_df = timeline_df.sort_values("OrderDate")

        # Gantt-style timeline: Order → Receive → Open
        fig_gantt = go.Figure()
        colours_gantt = [GOLD, ICE_BLUE, GREEN, RED, "#e67e22", "#9b59b6", "#1abc9c"]

        for i, (_, row) in enumerate(timeline_df.iterrows()):
            colour = colours_gantt[i % len(colours_gantt)]
            label  = row["Label"]
            od     = row.get("OrderDate")
            rd     = row.get("ReceiveDate")
            opd    = row.get("OpenDate")
            price  = row.get("PriceF")
            hover  = (
                f"<b>{label}</b><br>"
                f"Ordered: {od.strftime('%b %d, %Y') if pd.notna(od) else '—'}<br>"
                f"Received: {rd.strftime('%b %d, %Y') if pd.notna(rd) else '—'}<br>"
                f"Opened: {opd.strftime('%b %d, %Y') if pd.notna(opd) else '—'}<br>"
                f"Cost: {'$' + f'{price:.0f}' + ' CAD' if pd.notna(price) else '—'}"
            )

            # Order → Receive bar
            if pd.notna(od) and pd.notna(rd):
                fig_gantt.add_trace(go.Bar(
                    name="Order→Receive" if i == 0 else "",
                    y=[label],
                    x=[(rd - od).days],
                    base=[od],
                    orientation="h",
                    marker_color=colour,
                    opacity=0.85,
                    hovertemplate=hover + "<extra>Order→Receive</extra>",
                    showlegend=(i == 0),
                ))

            # Receive → Open bar (if both exist)
            if pd.notna(rd) and pd.notna(opd) and opd > rd:
                fig_gantt.add_trace(go.Bar(
                    name="Receive→Open" if i == 0 else "",
                    y=[label],
                    x=[(opd - rd).days],
                    base=[rd],
                    orientation="h",
                    marker_color=colour,
                    opacity=0.35,
                    hovertemplate=hover + "<extra>Receive→Open</extra>",
                    showlegend=(i == 0),
                ))

            # Point markers for key events
            for event_date, marker_sym, event_label in [
                (od,  "circle",          "Ordered"),
                (rd,  "diamond",         "Received"),
                (opd, "star",            "Opened"),
            ]:
                if pd.notna(event_date):
                    fig_gantt.add_trace(go.Scatter(
                        x=[event_date], y=[label],
                        mode="markers",
                        marker=dict(symbol=marker_sym, size=9, color=colour,
                                    line=dict(width=1, color="#fff")),
                        hovertemplate=f"<b>{label}</b><br>{event_label}: {event_date.strftime('%b %d, %Y')}<extra></extra>",
                        showlegend=False
                    ))

        fig_gantt.update_layout(
            **DARK_THEME,
            barmode="overlay",
            title="Jersey Acquisition Timeline  ●=Ordered  ◆=Received  ★=Opened",
            xaxis_title="Date",
            # xaxis=dict(type="date", gridcolor="#1e3a5a", linecolor="#1e3a5a"),
            # yaxis=dict(gridcolor="#1e3a5a", linecolor="#1e3a5a", autorange="reversed"),
            height=max(400, len(timeline_df) * 32 + 80),
            legend=dict(orientation="h", yanchor="bottom", y=1.01),
            margin=dict(l=20, r=20, t=60, b=20),
        )
        st.plotly_chart(fig_gantt, use_container_width=True)

        # Days to receive + days to open distributions
        col_dtr, col_dto = st.columns(2)
        with col_dtr:
            dtr = active["DaysToReceive"].dropna() if "DaysToReceive" in active.columns else pd.Series([], dtype=float)
            if len(dtr) > 0:
                fig_dtr = px.histogram(
                    dtr, nbins=15, title="Days: Order → Receive",
                    color_discrete_sequence=[ICE_BLUE],
                    labels={"value": "Days", "count": "Jerseys"}
                )
                fig_dtr.update_layout(**DARK_THEME, height=280)
                st.plotly_chart(fig_dtr, use_container_width=True)
                st.metric("Avg Days to Receive", f"{dtr.mean():.1f}")

        with col_dto:
            dto = active["DaysToOpen"].dropna() if "DaysToOpen" in active.columns else pd.Series([], dtype=float)
            if len(dto) > 0:
                fig_dto = px.histogram(
                    dto, nbins=15, title="Days: Receive → Open",
                    color_discrete_sequence=[GREEN],
                    labels={"value": "Days", "count": "Jerseys"}
                )
                fig_dto.update_layout(**DARK_THEME, height=280)
                st.plotly_chart(fig_dto, use_container_width=True)
                st.metric("Avg Days to Open", f"{dto.mean():.1f}")

        # Orders by month bar
        if "OrderMonth" in active.columns:
            mo_cnt = active.groupby("OrderMonth").size().reset_index(name="Jerseys")
            mo_cnt = mo_cnt.sort_values("OrderMonth")
            fig_mo = px.bar(
                mo_cnt, x="OrderMonth", y="Jerseys",
                title="Jerseys Ordered by Month",
                color="Jerseys", color_continuous_scale=[[0, ICE_BLUE], [1, GOLD]],
                text="Jerseys"
            )
            fig_mo.update_traces(textposition="outside")
            fig_mo.update_layout(**DARK_THEME, coloraxis_showscale=False,
                                  xaxis_tickangle=-45, height=340)
            st.plotly_chart(fig_mo, use_container_width=True)
    
    # ══════════════════════════════════════════════
    # TAB 5: Checklist
    # ══════════════════════════════════════════════
    # with tab_cost:
    elif pills_jersey_collection_mode == options_pills_jersey_collection_mode[4]:
        checklist = active.copy()
        for i in range(10):
            checklist["Model"] = checklist["Model"].apply(lambda m: m.replace(str(i), "").strip())
        display_df(
            checklist,
            "checklist"
        )
        cols_bm = ["Team", "Model"]
        checklist_by_model = checklist.groupby(
            cols_bm
        ).agg("count").reset_index().rename(columns={"ID":"Count"})
        display_df(
            checklist_by_model,
            "checklist_by_model"
        )
        checklist_by_model_b = checklist_by_model.pivot(
            index=["Team"],
            columns=["Model"]
        )["Count"]
        cols_model = checklist_by_model_b.columns.tolist()
        cols_model.remove("Away")
        cols_model.remove("Home")
        cols_model = ["Home", "Away"] + cols_model
        display_df(
            checklist_by_model_b[cols_model],
            "Model Checklist by Team"
        )

    # ══════════════════════════════════════════════
    # TAB 4: COST ANALYSIS
    # ══════════════════════════════════════════════
    # with tab_cost:
    # if pills_jersey_collection_mode == options_pills_jersey_collection_mode[3]:
    else:
        # 💰 Cost Analysis
        st.markdown('<div class="section-header" style="font-size:1.2rem">COST ANALYSIS</div>', unsafe_allow_html=True)

        all_known = active.copy()
        n_all_jerseys = len(all_known)
        priced = active.dropna(subset=["PriceF"]).copy()
        priced.sort_values("ID", ascending=False, inplace=True)
        priced = priced[priced["PriceF"] > 0]
        n_priced_jerseys = len(priced)
        
        first_date = active["OrderDate"].min()
        last_date = active["OrderDate"].max()
        today = datetime.now().date()
        n_days = (today - first_date).days
        
        sum_priced = priced['PriceF'].sum()
        mean_priced = priced['PriceF'].mean()
        sum_priced_extrapolated = ((mean_priced * (n_all_jerseys - n_priced_jerseys)) + sum_priced)
        spent_per_day = sum_priced_extrapolated / n_days
        jerseys_per_day = len(active) / n_days
        days_since_last_order = (today - last_date).days
        est_savings_since_last_order = days_since_last_order * spent_per_day
        
        t_c_patches = len(priced[priced["CPatch"] == 1])
        t_a_patches = len(priced[priced["APatch"] == 1])

        if len(priced) == 0:
            st.info("No pricing data available yet.")
        else:
            # Summary KPIs
            ck1, ck2, ck3, ck4, ck5, ck6 = st.columns(6)
            
            loc_cur = " CAD"
            ck1.metric("Total Spent", f"${sum_priced:,.2f}{loc_cur}")
            ck2.metric("Total Spent (Extrapolated)", f"${sum_priced_extrapolated:,.2f}{loc_cur}")
            ck3.metric("Avg per Jersey", f"${mean_priced:,.0f}{loc_cur}")
            ck4.metric("Most Expensive", f"${priced['PriceF'].max():,.2f}{loc_cur}")
            ck5.metric("Least Expensive", f"${priced['PriceF'].min():,.2f}{loc_cur}")
            ck6.metric("Jerseys with Price", len(priced))
            
            ck1.metric("Total Days Collecting:", n_days)
            ck2.metric("Total Spent per Day:", f"${spent_per_day:,.2f}{loc_cur}")
            ck3.metric("Jersey per Day:", f"{jerseys_per_day:,.2f}")
            ck4.metric("Days Between Jersey Order:", f"{1/jerseys_per_day:,.2f}")
            ck5.metric("Days Since Last Order:", days_since_last_order)
            ck6.metric("Est. Savings Since Last Order:", f"${est_savings_since_last_order:,.2f}{loc_cur}")
            
            ck1.metric("First Date:", f"{first_date}")
            ck2.metric("Last Date:", f"{last_date}")
            ck3.metric("# C Patches:", t_c_patches)
            ck4.metric("# A Patches:", t_a_patches)
            
            # Cumulative spend over time
            st.write("priced")
            st.write(priced)

            priced_plot = pd.concat([
                priced.copy(),
                pd.DataFrame({
                    "OrderDate": [datetime.now().date()],
                    "PriceF": [0],
                    "PlayerName": [""],
                    "Team": [""]
                })
            ])

            priced_sorted = priced_plot.dropna(subset=["OrderDate"]).sort_values("OrderDate").copy()

            if len(priced_sorted) > 0:
                priced_sorted["CumulativeSpend"] = priced_sorted["PriceF"].cumsum()
                priced_sorted["Label"] = priced_sorted.apply(
                    lambda r: (r.get("PlayerName") or r.get("Team", "?")) + f" (${r['PriceF']:.0f})",
                    axis=1
                )

                # Build extrapolated series from all jerseys, not just priced ones
                extrapolated = active.dropna(subset=["OrderDate"]).sort_values("OrderDate").copy()
                extrapolated["PriceF_Extrapolated"] = extrapolated["PriceF"].fillna(mean_priced)
                extrapolated["PriceF_Extrapolated"] = extrapolated["PriceF"].replace(0, mean_priced)
                extrapolated["PriceF_Extrapolated"] = extrapolated["PriceF"].replace(-1, mean_priced)
                extrapolated["CumulativeSpendExtrapolated"] = extrapolated["PriceF_Extrapolated"].cumsum()
                extrapolated["Label"] = extrapolated.apply(
                    lambda r: (
                        (r.get("PlayerName") or r.get("Team", "?"))
                        + (
                            f" (${r['PriceF']:.0f})"
                            if pd.notna(r.get("PriceF"))
                            else f" (est. ${mean_priced:.0f})"
                        )
                    ),
                    axis=1
                )

                # Append today to extrapolated series too
                extrapolated = pd.concat([
                    extrapolated,
                    pd.DataFrame({
                        "OrderDate": [datetime.now().date()],
                        "PriceF": [0],
                        "PriceF_Extrapolated": [0],
                        "CumulativeSpendExtrapolated": [sum_priced_extrapolated],
                        "PlayerName": [""],
                        "Team": [""],
                        "Label": ["Today"]
                    })
                ]).sort_values("OrderDate").reset_index(drop=True)

                fig_cum = make_subplots(specs=[[{"secondary_y": False}]])

                # Actual cumulative spend
                fig_cum.add_trace(
                    go.Scatter(
                        x=priced_sorted["OrderDate"],
                        y=priced_sorted["CumulativeSpend"],
                        name="Actual Cumulative Spend",
                        mode="lines+markers",
                        line=dict(color=GOLD, width=2),
                        marker=dict(size=8, color=GOLD),
                        text=priced_sorted["Label"],
                        hovertemplate="<b>%{text}</b><br>Date: %{x|%b %d, %Y}<br>Cumulative: $%{y:,.0f} CAD<extra></extra>",
                        fill="tozeroy",
                        fillcolor="rgba(200,168,75,0.08)"
                    )
                )

                # Actual trendline
                if len(priced_sorted) > 1:
                    x_actual = priced_sorted["OrderDate"].map(lambda d: 1 + (d - datetime(1, 1, 1).date()).days).to_numpy().reshape(-1, 1)
                    y_actual = priced_sorted["CumulativeSpend"].to_numpy()

                    regr_actual = LinearRegression()
                    regr_actual.fit(x_actual, y_actual)
                    fit_actual = regr_actual.predict(x_actual)

                    fig_cum.add_trace(
                        go.Scatter(
                            x=priced_sorted["OrderDate"],
                            y=fit_actual,
                            name="Actual Trend",
                            mode="lines",
                            line=dict(dash="dash", width=2, color="white"),
                            hovertemplate="Actual Trend: $%{y:,.0f} CAD<extra></extra>"
                        )
                    )

                # Extrapolated cumulative spend
                fig_cum.add_trace(
                    go.Scatter(
                        x=extrapolated["OrderDate"],
                        y=extrapolated["CumulativeSpendExtrapolated"],
                        name="Extrapolated Cumulative Spend",
                        mode="lines+markers",
                        line=dict(width=2, dash="dot"),
                        marker=dict(size=7),
                        text=extrapolated["Label"],
                        hovertemplate="<b>%{text}</b><br>Date: %{x|%b %d, %Y}<br>Extrapolated Cumulative: $%{y:,.0f} CAD<extra></extra>"
                    )
                )

                # Extrapolated trendline
                if len(extrapolated) > 1:
                    x_ex = extrapolated["OrderDate"].map(lambda d: 1 + (d - datetime(1, 1, 1).date()).days).to_numpy().reshape(-1, 1)
                    y_ex = extrapolated["CumulativeSpendExtrapolated"].to_numpy()

                    regr_ex = LinearRegression()
                    regr_ex.fit(x_ex, y_ex)
                    fit_ex = regr_ex.predict(x_ex)

                    fig_cum.add_trace(
                        go.Scatter(
                            x=extrapolated["OrderDate"],
                            y=fit_ex,
                            name="Extrapolated Trend",
                            mode="lines",
                            line=dict(dash="dash", width=2),
                            hovertemplate="Extrapolated Trend: $%{y:,.0f} CAD<extra></extra>"
                        )
                    )

                fig_cum.update_layout(
                    **DARK_THEME,
                    title="Cumulative Collection Spend Over Time",
                    xaxis_title="Order Date",
                    yaxis_title="Cumulative Spend (CAD $)",
                    height=420
                )

                st.plotly_chart(fig_cum, use_container_width=True)

            # Cost by team
            cost_team = priced.groupby("Team")["PriceF"].agg(["sum","mean","count"]).reset_index()
            cost_team.columns = ["Team","Total","Average","Count"]
            cost_team = cost_team.sort_values("Total", ascending=True)

            col_ct1, col_ct2 = st.columns(2)
            with col_ct1:
                fig_ct = px.bar(
                    cost_team, x="Total", y="Team", orientation="h",
                    title="Total Spend by Team",
                    color="Total", color_continuous_scale=[[0, ICE_BLUE], [1, GOLD]],
                    text=cost_team["Total"].apply(lambda x: f"${x:,.0f}")
                )
                fig_ct.update_traces(textposition="outside")
                fig_ct.update_layout(**DARK_THEME, coloraxis_showscale=False,
                                     height=max(280, len(cost_team)*28 + 60))
                st.plotly_chart(fig_ct, use_container_width=True)

            with col_ct2:
                fig_ca = px.bar(
                    cost_team.sort_values("Average", ascending=True),
                    x="Average", y="Team", orientation="h",
                    title="Avg Cost per Jersey by Team",
                    color="Average", color_continuous_scale=[[0, "#27ae60"], [1, RED]],
                    text=cost_team.sort_values("Average", ascending=True)["Average"].apply(lambda x: f"${x:,.0f}")
                )
                fig_ca.update_traces(textposition="outside")
                fig_ca.update_layout(**DARK_THEME, coloraxis_showscale=False,
                                     height=max(280, len(cost_team)*28 + 60))
                st.plotly_chart(fig_ca, use_container_width=True)

            # Cost by brand & supplier
            col_cb1, col_cb2 = st.columns(2)
            with col_cb1:
                cost_brand = priced.groupby("Brand")["PriceF"].agg(["sum","mean"]).reset_index()
                cost_brand.columns = ["Brand","Total","Average"]
                fig_cb = px.bar(
                    cost_brand.sort_values("Total"),
                    x="Total", y="Brand", orientation="h",
                    title="Total Spend by Brand",
                    color="Average", color_continuous_scale=[[0, ICE_BLUE],[1, GOLD]],
                    text=cost_brand.sort_values("Total")["Total"].apply(lambda x: f"${x:,.0f}")
                )
                fig_cb.update_traces(textposition="outside")
                fig_cb.update_layout(**DARK_THEME, coloraxis_showscale=False, height=300)
                st.plotly_chart(fig_cb, use_container_width=True)

            with col_cb2:
                cost_sup = priced.groupby("Supplier")["PriceF"].sum().reset_index()
                cost_sup.columns = ["Supplier","Total"]
                cost_sup = cost_sup.sort_values("Total", ascending=False).head(10)
                fig_cs = px.pie(
                    cost_sup, names="Supplier", values="Total",
                    title="Spend Share by Supplier (Top 10)", hole=0.4,
                    color_discrete_sequence=px.colors.qualitative.Plotly
                )
                fig_cs.update_layout(**DARK_THEME, height=300)
                st.plotly_chart(fig_cs, use_container_width=True)

            # Discount analysis
            if "Discount" in priced.columns and "StickerPriceCDN" in priced.columns:
                disc = priced.dropna(subset=["Discount","StickerPriceCDN"]).copy()
                disc = disc[disc["Discount"] > 0]
                if len(disc) > 0:
                    disc["DiscountPct"] = disc["Discount"] / disc["StickerPriceCDN"] * 100
                    fig_disc = px.scatter(
                        disc,
                        x="OrderDate", y="StickerPriceCDN", size="Discount",
                        color="DiscountPct",
                        color_continuous_scale=[[0, ICE_BLUE],[0.5, GOLD],[1, GREEN]],
                        hover_data=["Team","PlayerName","Supplier","DiscountReason"],
                        title="Discounts Over Time (bubble = $ saved, colour = % off)",
                        labels={"StickerPriceCDN":"Sticker Price (CDN $)","OrderDate":"Order Date","DiscountPct":"% Off"}
                    )
                    fig_disc.update_layout(**DARK_THEME, height=380)
                    st.plotly_chart(fig_disc, use_container_width=True)

                    avg_saving = disc["Discount"].mean()
                    total_saving = disc["Discount"].sum()
                    st.info(f"💸 You saved an avg of **${avg_saving:.0f} CAD** per discounted jersey — **${total_saving:,.0f} CAD total** across {len(disc)} discounted purchases.")

            # Price distribution scatter
            priced_label = priced.copy()
            priced_label["Label"] = priced_label.apply(
                lambda r: (r.get("PlayerName") or r.get("Team","?")) + f"\n{r.get('Brand','')} {r.get('Model','')}",
                axis=1
            )
            fig_scatter = px.scatter(
                priced_label.dropna(subset=["OrderDate"]),
                x="OrderDate", y="PriceF",
                color="League" if "League" in priced_label.columns else None,
                size="PriceF",
                hover_name="Label",
                hover_data=["Team","Brand","Model","Supplier"],
                title="Jersey Prices Over Time",
                labels={"PriceF":"Price (CAD $)","OrderDate":"Order Date"}
            )
            fig_scatter.update_layout(**DARK_THEME, height=380)
            st.plotly_chart(fig_scatter, use_container_width=True)
    
        df_cost_per_day = active.copy()
        df_cost_per_day["PriceF"] = df_cost_per_day["PriceF"].replace(-1, mean_priced)
        df_cost_per_day["ToString"] = df_cost_per_day.apply(to_string, axis=1)
        df_cost_per_day.sort_values("ID", inplace=True)
        for c in ["Order", "Receive", "Open"]:
            col = f"{c}Date"
            c_name = f"DaysSince{c}"
            df_cost_per_day[c_name] = df_cost_per_day[col].apply(lambda d: (today - d).days if not pd.isna(d) else 0)
        
        df_cost_per_day["DollarsPerDay"] = df_cost_per_day["PriceF"] / df_cost_per_day["DaysSinceOrder"]
        df_cost_per_day["DollarsPerWeek"] = df_cost_per_day["DollarsPerDay"] * 7
        df_cost_per_day["DollarsPerMonth"] = df_cost_per_day["DollarsPerDay"] * (365 / 12)
        df_cost_per_day["DollarsPerDay_Tomorrow"] = df_cost_per_day["PriceF"] / (1 + df_cost_per_day["DaysSinceOrder"])
        df_cost_per_day["DollarsPerDay_DayAftermorrow"] = df_cost_per_day["PriceF"] / (2 + df_cost_per_day["DaysSinceOrder"])
        df_cost_per_day["DollarsPerDay_NextWeek"] = df_cost_per_day["PriceF"] / (7 + df_cost_per_day["DaysSinceOrder"])
        df_cost_per_day["DollarsPerDay_NextMonth"] = df_cost_per_day["PriceF"] / ((365.2425 / 12) + df_cost_per_day["DaysSinceOrder"])
        df_cost_per_day["DollarsPerDay_NextYear"] = df_cost_per_day["PriceF"] / (365.2425 + df_cost_per_day["DaysSinceOrder"])
        
        df_cpd = df_cost_per_day[[
            "ID", "ToString",
            "OrderDate", "ReceiveDate", "OpenDate", "PriceF",
            "DaysSinceOrder", "DaysSinceReceive", "DaysSinceOpen",
            "DollarsPerDay", "DollarsPerWeek", "DollarsPerMonth",
            "DollarsPerDay_Tomorrow", "DollarsPerDay_DayAftermorrow",
            "DollarsPerDay_NextWeek", "DollarsPerDay_NextMonth",
            "DollarsPerDay_NextYear"
        ]]
        dpd_column_config = {
            col: st.column_config.NumberColumn(label=f"DPD_{col.split('_')[-1]}", format="dollar", width="small") 
            for col in [
                "DollarsPerDay", "DollarsPerWeek", "DollarsPerMonth",
                "DollarsPerDay_Tomorrow", "DollarsPerDay_DayAftermorrow",
                "DollarsPerDay_NextWeek", "DollarsPerDay_NextMonth",
                "DollarsPerDay_NextYear"
            ]
        }
        df_cpd.sort_values("DollarsPerDay", ascending=False, inplace=True)
        display_df(
            df_cpd,
            "df_cost_per_day",
            column_config=dpd_column_config
        )
        df_cpd["Label"] = df_cpd["ToString"]
        df_cpd["DPDRatingColor"] = df_cpd["DollarsPerDay"] // 5
        fig_scatter = px.scatter(
            df_cpd.dropna(subset=["DaysSinceOrder"]),
            x="DaysSinceOrder", y="DollarsPerDay",
            color="DPDRatingColor",
            size="PriceF",
            hover_name="Label",
            hover_data=[
                "OrderDate", "ReceiveDate", "OpenDate", "PriceF",
                "DaysSinceOrder", "DaysSinceReceive", "DaysSinceOpen",
                "DollarsPerDay", "DollarsPerWeek", "DollarsPerMonth"
            ],
            title="Jersey Dollars Per Day Over Time",
            labels={"PriceF":"Price (CAD $)","DaysSinceOrder":"Days Since Order"},
            trendline="expanding"
        )
        fig_scatter.update_layout(**DARK_THEME, height=380)
        st.plotly_chart(fig_scatter, use_container_width=True)


# ─────────────────────────────────────────────────────────
# DATA LOADING & ENRICHMENT
# ─────────────────────────────────────────────────────────

# ─────────────────────────────────────────────────────────
# ENHANCED PREDICTION SCORING
# ─────────────────────────────────────────────────────────
def compute_enhanced_score(row) -> float:
    """
    NHL Prediction Score v3 — a composited heuristic across 5 dimensions.

    Max possible score: 1.00  (perfect in every dimension)
    Practical "good" score: ~0.65–0.80 (correct winner + close scores)

    Component breakdown (A+B+C+D = 1.00 on a perfect prediction):
    ┌──────────────────────────────────────────────────────┐
    │  A) Winner        — 0.55 pts  (base; most important) │
    │  B) Result type   — 0.10 pts  (REG / OT / SO match)  │
    │  C) Margin error  — 0.175 pts (spread closeness)     │
    │  D) Score error   — 0.175 pts (per-team goal delta)  │
    │  E) OT/SO credit  — ≤0.10 pts (wrong-winner bonus)   │
    └──────────────────────────────────────────────────────┘

    Design rationale vs the existing formulas:
    • GPS  gives 0.80 for correct winner — too binary; a 6-1 blowout
      and a 3-2 overtime thriller both score the same.
    • GPS2 adds OT partial credit but still ignores score quality.
    • v3 rewards *how* right you were: a correct winner AND a 1-goal
      margin error scores much higher than a correct winner with a
      6-goal margin error.  Incorrect predictions still earn partial
      credit when scores are close or OT was correctly anticipated.
    """
    try:
        correct_winner  = str(row.get("CorrectWinnerPrediction", "N")).strip().upper() in ("Y", "TRUE", "1")
        correct_away_sc = str(row.get("CorrectAwayScorePrediction", "N")).strip().upper() in ("Y", "TRUE", "1")
        correct_home_sc = str(row.get("CorrectHomeScorePrediction", "N")).strip().upper() in ("Y", "TRUE", "1")
        pred_result  = str(row.get("PredictedResult", "REG")).strip().upper()
        actual_result= str(row.get("ActualResult",   "REG")).strip().upper()

        pred_away  = float(row.get("PredictedAwayScore", 0) or 0)
        pred_home  = float(row.get("PredictedHomeScore", 0) or 0)
        act_away   = float(row.get("ActualAwayScore",   0) or 0)
        act_home   = float(row.get("ActualHomeScore",   0) or 0)

        # ── A) Winner (0.55) ─────────────────────────────────
        # Scaled to 0.55 so that components A+B+C+D sum to 1.00 on a perfect prediction.
        score_winner = 0.55 if correct_winner else 0.0

        # ── B) Result type (0.10) ─────────────────────────────
        # Exact match = 0.10.  OT/SO confusion (both extra time) = 0.06.
        # REG vs OT/SO or vice-versa = 0.
        if pred_result == actual_result:
            score_result = 0.10
        elif pred_result in ("OT", "SO") and actual_result in ("OT", "SO"):
            score_result = 0.06
        else:
            score_result = 0.0

        # ── C) Victory-margin error (0.175) ───────────────────
        # Margin = away_score − home_score.
        # Exponential decay: pts = 0.175 * exp(−|Δmargin| / 2)
        # Δmargin=0 → 0.175,  Δ=1 → 0.106,  Δ=2 → 0.064,  Δ=3 → 0.039
        pred_margin   = pred_away - pred_home
        actual_margin = act_away  - act_home
        delta_margin  = abs(pred_margin - actual_margin)
        score_margin  = 0.175 * np.exp(-delta_margin / 2.0)

        # ── D) Raw score error (0.175, split 0.0875 each side) ─
        # Exponential decay per team: pts = 0.0875 * exp(−|Δgoals| / 1.5)
        # Exact match → 0.0875,  off by 1 → 0.051,  off by 2 → 0.030
        away_goal_err = abs(pred_away - act_away)
        home_goal_err = abs(pred_home - act_home)
        score_goals = (
            0.0875 * np.exp(-away_goal_err / 1.5) +
            0.0875 * np.exp(-home_goal_err / 1.5)
        )

        # ── E) Near-miss OT/SO credit (up to 0.10) ────────────
        # Wrong winner BUT game went OT/SO AND prediction was OT/SO:
        # award up to 0.10 scaled by how close the final scores were.
        # (This component only fires on wrong-winner extra-time games,
        #  so A+B+C+D still sum to exactly 1.00 on a perfect prediction.)
        score_ot_credit = 0.0
        if not correct_winner and actual_result in ("OT", "SO") and pred_result in ("OT", "SO"):
            total_goal_err = away_goal_err + home_goal_err
            # Linear taper: 0 goal err → 0.10, ≥4 goal err → 0
            score_ot_credit = max(0.0, 0.10 * (1 - total_goal_err / 4.0))

        total = score_winner + score_result + score_margin + score_goals + score_ot_credit
        return round(min(total, 1.0), 4)

    except Exception:
        return 0.0


def apply_enhanced_scores(df: pd.DataFrame) -> pd.DataFrame:
    """Add EnhancedScore column to completed games."""
    mask = df["GameIsOver"] == True
    df.loc[mask, "EnhancedScore"] = df[mask].apply(compute_enhanced_score, axis=1)
    return df


def peek_rows(filepath: str) -> int:
    """If copy file was made manually, need to skip 1 row. If it was done by the sidebar button, none need to be skipped."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Could not find '{filepath}'")
    n = 3
    ext = str(filepath).lower()
    if ext.endswith(".xlsx") or ext.endswith(".xls"):
        df = pd.read_excel(filepath, nrows=n)
    else:
        df = pd.read_csv(filepath, encoding="utf-8-sig", nrows=n)
    cols = df.columns.tolist()
    read = [cols] + [list(df.iloc[i].values) for i in range(n)]
    for i, row in enumerate(read):
        vals = "".join(map(str, [v for v in row if (not pd.isna(v)) and bool(v)])).strip()
        if vals:
            return i
    raise ValueError(f"peek_rows could not determine hoe many rows to skip in '{filepath}'")
    

@st.cache_data
def load_data(filepath: str) -> pd.DataFrame:
    ext = str(filepath).lower()
    if ext.endswith(".xlsx") or ext.endswith(".xls"):
        df = pd.read_excel(filepath, skiprows=peek_rows(filepath))
    else:
        df = pd.read_csv(filepath, encoding="utf-8-sig")
    df.columns = df.columns.str.strip()

    # Drop the unnamed first column if it exists
    if df.columns[0] == "" or df.columns[0].startswith("Unnamed"):
        df = df.iloc[:, 1:]

    # Date parsing
    for col in ["GameDate", "PredictionDate"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    # Normalize Y/N/1/0 columns
    yn_cols = ["GameIsOver", "CorrectWinnerPrediction", "CorrectAwayScorePrediction",
               "CorrectHomeScorePrediction", "WatchedGame", "GameHasShutOut",
               "AwayWon", "HomeWon_", "InterConf", "InterDiv",
               "SameConfDiffDiv", "CrossConf", "CanadianTeamPlays",
               "OriginalSixPlays", "THG_TonyTiger", "THG_80sGame",
               "THG_Extermination", "THG_ChessMatch"]
    for col in yn_cols:
        if col in df.columns:
            df[col] = df[col].map(
                lambda x: str(x).strip().upper().replace(".0", "") in ["Y", "YES", "1", "TRUE"]
            )

    # Numeric
    for col in ["ActualAwayScore", "ActualHomeScore", "PredictedAwayScore", "PredictedHomeScore",
                "GamePredictionScore", "GamePredictionScore2", "NewPointsAway", "NewPointsHome",
                "GameCost", "AwayTeamPays", "HomeTeamPays"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Enrich with team metadata
    df["AwayConf"] = df["AwayTeam"].map(lambda t: TEAM_META.get(t, {}).get("conf", "Unknown"))
    df["HomeConf"] = df["HomeTeam"].map(lambda t: TEAM_META.get(t, {}).get("conf", "Unknown"))
    df["AwayDiv"]  = df["AwayTeam"].map(lambda t: TEAM_META.get(t, {}).get("div", "Unknown"))
    df["HomeDiv"]  = df["HomeTeam"].map(lambda t: TEAM_META.get(t, {}).get("div", "Unknown"))

    # Week/Month/DayOfWeek
    if "GameDate" in df.columns:
        df["Month"]     = df["GameDate"].dt.month_name()
        df["MonthNum"]  = df["GameDate"].dt.month
        df["Week"]      = df["GameDate"].dt.isocalendar().week.astype(int)
        df["DayOfWeek"] = df["GameDate"].dt.day_name()
        df["WeekStart"] = df["GameDate"].dt.to_period("W").apply(lambda p: p.start_time)

    # Back-to-back detection (same team plays on consecutive days)
    df = detect_back_to_back(df)

    # Road trip / homestand tracking
    df = detect_road_trips(df)

    # Won/lost last game
    df = detect_last_game_result(df)

    # Gauntlet detection
    df = detect_gauntlets(df)

    # Enhanced scoring
    df = apply_enhanced_scores(df)
    
    df = detect_rivals(df)
    
    
    return df


def detect_rivals(df: pd.DataFrame) -> pd.DataFrame:
    df["RivalGame"] = ""
    df["RivalReason"] = [[] for _ in range(df.shape[0])]
    
    all_teams = set(df["AwayTeam"].dropna()) | set(df["HomeTeam"].dropna())
    for team in all_teams:
        rival_data = TEAM_RIVALS.get(team, {})
        mask_away = df["AwayTeam"] == team
        mask_home = df["HomeTeam"] == team
        team_away_games = df[mask_away].copy()
        team_home_games = df[mask_home].copy()
        for rival_status in [
            "primary",
            "secondary",
            "historic",
            "modern"
        ]:
            rivals_list = rival_data.get(rival_status, [])
            df.loc[mask_away & team_away_games["HomeTeam"].isin(rivals_list), "RivalGame"] = rival_status
            df.loc[mask_away & team_away_games["HomeTeam"].isin(rivals_list), "RivalReason"] = df.loc[mask_away & team_away_games["HomeTeam"].isin(rivals_list)].apply(
                lambda r:
                    r["RivalReason"] + rival_data["reasons"][r["HomeTeam"]]
                , axis=1
            )
            df.loc[mask_home & team_home_games["AwayTeam"].isin(rivals_list), "RivalGame"] = rival_status
            df.loc[mask_home & team_home_games["AwayTeam"].isin(rivals_list), "RivalReason"] = df.loc[mask_home & team_home_games["AwayTeam"].isin(rivals_list)].apply(
                lambda r:
                    r["RivalReason"] + rival_data["reasons"][r["AwayTeam"]]
                , axis=1
            )
            
    df["RivalReason"] = df["RivalReason"].apply(lambda rr: ", ".join(list(set(rr))))
    
    return df


def detect_back_to_back(df: pd.DataFrame) -> pd.DataFrame:
    df = df.sort_values("GameDate").reset_index(drop=True)
    df["AwayB2B"] = False
    df["HomeB2B"] = False

    all_teams = set(df["AwayTeam"].dropna()) | set(df["HomeTeam"].dropna())
    for team in all_teams:
        mask_away = df["AwayTeam"] == team
        mask_home = df["HomeTeam"] == team
        team_games = df[mask_away | mask_home][["GameDate"]].copy()
        team_games = team_games.sort_values("GameDate")
        team_games["PrevDate"] = team_games["GameDate"].shift(1)
        team_games["IsB2B"] = (team_games["GameDate"] - team_games["PrevDate"]).dt.days == 1

        b2b_dates = set(team_games[team_games["IsB2B"]]["GameDate"])
        df.loc[mask_away & df["GameDate"].isin(b2b_dates), "AwayB2B"] = True
        df.loc[mask_home & df["GameDate"].isin(b2b_dates), "HomeB2B"] = True

    df["EitherB2B"] = df["AwayB2B"] | df["HomeB2B"]
    return df


def detect_road_trips(df: pd.DataFrame) -> pd.DataFrame:
    """Track consecutive away games (road trips) and home games (homestands) per team."""
    df = df.sort_values("GameDate").reset_index(drop=True)
    df["AwayRoadTripGame"] = 0  # which game in road trip (0 = not on road trip)
    df["HomeHomestandGame"] = 0

    all_teams = set(df["AwayTeam"].dropna()) | set(df["HomeTeam"].dropna())
    for team in all_teams:
        away_idx = df[df["AwayTeam"] == team].index.tolist()
        home_idx = df[df["HomeTeam"] == team].index.tolist()

        all_idx = sorted(away_idx + home_idx)
        streak_away = 0
        streak_home = 0
        for idx in all_idx:
            if idx in df.index:
                if df.loc[idx, "AwayTeam"] == team:
                    streak_away += 1
                    streak_home = 0
                    if streak_away >= 2:
                        # Mark this game as part of road trip
                        df.loc[idx, "AwayRoadTripGame"] = streak_away
                else:
                    streak_home += 1
                    streak_away = 0
                    if streak_home >= 2:
                        df.loc[idx, "HomeHomestandGame"] = streak_home

    df["OnRoadTrip"]  = df["AwayRoadTripGame"] >= 2
    df["OnHomeStand"] = df["HomeHomestandGame"] >= 2
    return df


def detect_last_game_result(df: pd.DataFrame) -> pd.DataFrame:
    """For each game, did the away/home team win or lose their last game?"""
    df = df.sort_values("GameDate").reset_index(drop=True)
    df["AwayWonLast"] = None
    df["HomeWonLast"] = None

    all_teams = set(df["AwayTeam"].dropna()) | set(df["HomeTeam"].dropna())
    for team in all_teams:
        mask_away = df["AwayTeam"] == team
        mask_home = df["HomeTeam"] == team
        combined = pd.concat([
            df[mask_away][["GameDate", "ActualWinner"]].assign(side="away", idx=df[mask_away].index),
            df[mask_home][["GameDate", "ActualWinner"]].assign(side="home", idx=df[mask_home].index),
        ]).sort_values("GameDate")

        combined["TeamWon"] = combined["ActualWinner"] == team
        combined["TeamWonLast"] = combined["TeamWon"].shift(1)

        for _, row in combined.iterrows():
            if pd.isna(row["TeamWonLast"]):
                continue
            if row["side"] == "away":
                df.loc[row["idx"], "AwayWonLast"] = row["TeamWonLast"]
            else:
                df.loc[row["idx"], "HomeWonLast"] = row["TeamWonLast"]

    return df


def detect_gauntlets(df: pd.DataFrame) -> pd.DataFrame:
    """Detect when away team is on a gauntlet swing."""
    df = df.sort_values("GameDate").reset_index(drop=True)
    df["GauntletName"] = ""

    all_teams = set(df["AwayTeam"].dropna())
    for team in all_teams:
        away_games = df[df["AwayTeam"] == team][["GameDate", "HomeTeam"]].sort_values("GameDate")

        # Sliding window: look for gauntlet patterns in consecutive away games
        if len(away_games) < 2:
            continue

        away_games = away_games.reset_index()

        for gauntlet_name, g_info in GAUNTLETS.items():
            g_teams = set(g_info["teams"])
            for i in range(len(away_games)):
                # Look up to len(g_teams) ahead
                window = away_games.iloc[i:i+len(g_teams)]
                opponents = set(window["HomeTeam"].values)
                # Check if at least 2 gauntlet teams are in consecutive away window
                overlap = opponents & g_teams
                if len(overlap) >= 2:
                    # Check dates are within 10 days
                    if len(window) > 1:
                        span = (window["GameDate"].max() - window["GameDate"].min()).days
                        if span <= 14:
                            idxs = window["index"].tolist()
                            for idx in idxs:
                                if df.loc[idx, "HomeTeam"] in g_teams:
                                    if df.loc[idx, "GauntletName"] == "":
                                        df.loc[idx, "GauntletName"] = gauntlet_name
                                    elif gauntlet_name not in df.loc[idx, "GauntletName"]:
                                        df.loc[idx, "GauntletName"] += f", {gauntlet_name}"
    return df


@st.cache_data
def fetch_team_logo(team_abbr: str) -> str:
    """Get NHL team logo URL from NHL API."""
    team_id = TEAM_META.get(team_abbr, {}).get("id")
    if team_id:
        return f"https://assets.nhle.com/logos/nhl/svg/{team_abbr}_dark.svg"
    return ""


@st.cache_data(ttl=60)
def fetch_game_landing(g_id) -> dict:
    """Load NHL game landing for given game ID"""
    try:
        url = f"https://api-web.nhle.com/v1/gamecenter/{g_id}/landing"
        return requests.get(url).json()
    except Exception:
        return {}

 
# ─── STEP 1 – paste these two functions near the other fetch_* helpers ────────
 
@st.cache_data(ttl=300)
def fetch_nhl_standings() -> list:
    """
    Fetch current NHL standings from the NHL web API.
    Returns a list of team-standing dicts, one per team.
    """
    try:
        url = "https://api-web.nhle.com/v1/standings/now"
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        return data.get("standings", [])
    except Exception as e:
        return []
 
 
@st.cache_data(ttl=300)
def fetch_nhl_team_schedule(team_abbr: str) -> list:
    """
    Fetch the remaining regular-season schedule for *team_abbr*.
    Returns a list of game dicts that have not yet been played.
    """
    try:
        # The NHL API supports a full-season schedule by team abbreviation
        url = f"https://api-web.nhle.com/v1/club-schedule-season/{team_abbr}/20252026"
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        games = resp.json().get("games", [])
        today_str = datetime.now().strftime("%Y-%m-%d")
        # Keep only games that are not yet final (gameState != OFF/FINAL/CRIT)
        remaining = [
            g for g in games
            if g.get("gameDate", "") >= today_str
            and g.get("gameState", "") not in ("OFF", "FINAL", "CRIT")
            and g.get("gameType", 2) == 2          # regular season only
        ]
        return remaining
    except Exception:
        return []


# ─────────────────────────────────────────────────────────
# PLOTTING HELPERS
# ─────────────────────────────────────────────────────────
DARK_THEME = dict(
    paper_bgcolor="#0a0e1a",
    plot_bgcolor="#0d1f35",
    font=dict(color="#ccd6e0", family="Inter"),
    xaxis=dict(gridcolor="#1e3a5a", linecolor="#1e3a5a"),
    yaxis=dict(gridcolor="#1e3a5a", linecolor="#1e3a5a"),
)


def accuracy_bar(group_col, label, df_completed):
    """Bar chart of prediction accuracy by a grouping column."""
    grouped = (
        df_completed.groupby(group_col)["CorrectWinnerPrediction"]
        .agg(["sum", "count"])
        .reset_index()
    )
    grouped.columns = [group_col, "Correct", "Total"]
    grouped["Accuracy"] = (grouped["Correct"] / grouped["Total"] * 100).round(1)
    grouped = grouped.sort_values("Accuracy", ascending=True)

    fig = px.bar(
        grouped, x="Accuracy", y=group_col, orientation="h",
        text="Accuracy", color="Accuracy",
        color_continuous_scale=[[0, RED], [0.5, "#f39c12"], [1, GREEN]],
        labels={"Accuracy": "Accuracy %", group_col: label},
        title=f"Prediction Accuracy by {label}",
        custom_data=["Correct", "Total"]
    )
    fig.update_traces(
        texttemplate="%{text:.1f}%", textposition="outside",
        hovertemplate=f"<b>%{{y}}</b><br>Accuracy: %{{x:.1f}}%<br>Correct: %{{customdata[0]}} / %{{customdata[1]}}<extra></extra>"
    )
    fig.update_layout(**DARK_THEME, coloraxis_showscale=False, height=max(300, len(grouped)*35 + 80))
    fig.update_traces(marker_line_width=0)
    return fig, grouped


def correct_incorrect_pie(correct_count, total_count):
    incorrect = total_count - correct_count
    fig = go.Figure(go.Pie(
        labels=["Correct ✓", "Incorrect ✗"],
        values=[correct_count, incorrect],
        hole=0.65,
        marker_colors=[GREEN, RED],
        textinfo="label+percent",
        hovertemplate="%{label}: %{value}<extra></extra>"
    ))
    fig.update_layout(
        **DARK_THEME,
        showlegend=False,
        annotations=[dict(
            text=f"<b>{correct_count/total_count*100:.1f}%</b>",
            x=0.5, y=0.5, font_size=24, font_color=GOLD, showarrow=False
        )],
        height=280,
        margin=dict(l=20, r=20, t=20, b=20)
    )
    return fig


def rolling_accuracy_chart(df_team, team_abbr):
    df_team = df_team.sort_values("GameDate").copy()
    df_team["CumCorrect"] = df_team["CorrectWinnerPrediction"].cumsum()
    df_team["CumTotal"] = range(1, len(df_team) + 1)
    df_team["CumAccuracy"] = df_team["CumCorrect"] / df_team["CumTotal"] * 100
    df_team["Roll7"] = (
        df_team["CorrectWinnerPrediction"]
        .rolling(7, min_periods=3)
        .mean() * 100
    )

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_team["GameDate"], y=df_team["CumAccuracy"],
        name="Cumulative Accuracy", line=dict(color=GOLD, width=2),
        mode="lines"
    ))
    fig.add_trace(go.Scatter(
        x=df_team["GameDate"], y=df_team["Roll7"],
        name="7-Game Rolling Avg", line=dict(color=ICE_BLUE, width=2, dash="dot"),
        mode="lines"
    ))
    fig.add_hline(y=50, line_dash="dash", line_color="#555", annotation_text="50%")
    fig.update_layout(
        **DARK_THEME,
        title=f"Prediction Accuracy Trend — {team_abbr}",
        xaxis_title="Game Date",
        yaxis_title="Accuracy %",
        yaxis_range=[0, 105],
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
        height=350
    )
    return fig


def game_by_game_scatter(df_team, team_abbr):
    df_team = df_team.sort_values("GameDate").copy()
    df_team["GameNum"] = range(1, len(df_team) + 1)
    df_team["Result"] = df_team["CorrectWinnerPrediction"].map({True: "Correct", False: "Incorrect"})
    df_team["Opponent"] = df_team.apply(
        lambda r: r["HomeTeam"] if r["AwayTeam"] == team_abbr else r["AwayTeam"], axis=1
    )
    df_team["Side"] = df_team.apply(
        lambda r: "Away" if r["AwayTeam"] == team_abbr else "Home", axis=1
    )

    fig = px.scatter(
        df_team, x="GameDate", y="GamePredictionScore",
        color="Result", symbol="Side",
        color_discrete_map={"Correct": GREEN, "Incorrect": RED},
        hover_data=["Opponent", "ActualResult", "PredictedResult"],
        title=f"Game-by-Game Prediction Quality — {team_abbr}",
        labels={"GamePredictionScore": "Prediction Score", "GameDate": "Date"}
    )
    fig.update_layout(**DARK_THEME, height=350)
    return fig


def compare_two_groups(df_completed, group_col, label):
    """Side-by-side comparison chart."""
    g = (
        df_completed.groupby(group_col)["CorrectWinnerPrediction"]
        .agg(["sum", "count"]).reset_index()
    )
    g.columns = [group_col, "Correct", "Total"]
    g["Incorrect"] = g["Total"] - g["Correct"]
    g["Accuracy"] = (g["Correct"] / g["Total"] * 100).round(1)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="Correct", x=g[group_col], y=g["Correct"],
        marker_color=GREEN, text=g["Accuracy"].apply(lambda x: f"{x}%"),
        textposition="outside"
    ))
    fig.add_trace(go.Bar(
        name="Incorrect", x=g[group_col], y=g["Incorrect"],
        marker_color=RED
    ))
    fig.update_layout(
        **DARK_THEME,
        barmode="stack",
        title=f"Correct vs Incorrect by {label}",
        xaxis_title=label,
        yaxis_title="Games",
        height=380,
        legend=dict(orientation="h", yanchor="bottom", y=1.02)
    )
    return fig


# ---------------------------------------
# Example assumptions
# df_toar columns include:
# TeamA, TeamB, Sweep, WasSwept
#
# TEAM_META contains:
# {
#   "ANA": {"name": "Anaheim Ducks", "logo": "path/or/url"},
#   ...
# }
# ---------------------------------------


def render_sweep_logo_table(
    df_toar: pd.DataFrame,
    team_meta: dict = TEAM_META,
    sort: str | Sequence[str] = ("SweepCount", "SweptByCount", "TiedCount", "NetCount", "TeamName"),
    ascending: bool | Sequence[bool] = (False, True, True, True),
):
    # Maps:
    # swept_map[A] = teams that A swept
    # swept_by_map[B] = teams that swept B
    # tied_map[A] = teams that A tied in season series
    swept_map = defaultdict(list)
    swept_by_map = defaultdict(list)
    tied_map = defaultdict(list)

    for _, row in df_toar.iterrows():
        a = row["TeamA"]
        b = row["TeamB"]

        if bool(row.get("Sweep", False)):
            swept_map[a].append(b)
            swept_by_map[b].append(a)

        if bool(row.get("WasSwept", False)):
            swept_map[b].append(a)
            swept_by_map[a].append(b)

        # Explicit tie flag preferred
        is_tied = bool(row.get("Tied", False))

        # Fallback inference if no explicit flag exists
        if not is_tied:
            w = row.get("W")
            l = row.get("L")
            gp = row.get("GP")
            if pd.notna(w) and pd.notna(l) and pd.notna(gp):
                # Common tied-season-series case
                if int(gp) > 0 and int(w) == int(l):
                    # Avoid classifying sweep rows as ties
                    if not bool(row.get("Sweep", False)) and not bool(row.get("WasSwept", False)):
                        is_tied = True

        if is_tied:
            tied_map[a].append(b)
            tied_map[b].append(a)

    teams = sorted(team_meta.keys())

    rows = []
    for team in teams:
        swept = sorted(set(swept_map.get(team, [])))
        swept_by = sorted(set(swept_by_map.get(team, [])))
        tied = sorted(set(tied_map.get(team, [])))

        rows.append({
            "Team": team,
            "TeamName": team_meta.get(team, {}).get("name", team),
            "TeamLogo": fetch_team_logo(team),
            "SweptTeams": swept,
            "SweepCount": len(swept),
            "SweptByTeams": swept_by,
            "SweptByCount": len(swept_by),
            "TiedTeams": tied,
            "TiedCount": len(tied),
            "NetSweepDiff": len(swept) - len(swept_by),
        })

    df_summary = pd.DataFrame(rows)

    allowed_sort_cols = [
        "SweepCount", "SweptByCount", "TiedCount",
        "NetSweepDiff", "TeamName"
    ]

    # Normalize sort input
    if isinstance(sort, str):
        sort_order = [sort] if sort in allowed_sort_cols else ["SweepCount"]
    else:
        sort_order = [s for s in sort if s in allowed_sort_cols]
        if not sort_order:
            sort_order = ["SweepCount", "SweptByCount", "TiedCount", "TeamName"]

    # Add stable fallback sorts if missing
    for fallback in ["SweepCount", "SweptByCount", "TiedCount", "TeamName"]:
        if fallback not in sort_order:
            sort_order.append(fallback)

    # Normalize ascending input
    if isinstance(ascending, bool):
        sort_asc = [ascending] * len(sort_order)
    else:
        asc_list = list(ascending)
        default_dir = {
            "SweepCount": False,
            "SweptByCount": True,
            "TiedCount": True,
            "NetSweepDiff": False,
            "TeamName": True
        }
        sort_asc = []
        for i, col in enumerate(sort_order):
            if i < len(asc_list):
                sort_asc.append(bool(asc_list[i]))
            else:
                sort_asc.append(default_dir.get(col, True))

    df_summary = df_summary.sort_values(
        sort_order,
        ascending=sort_asc,
        kind="stable"
    )

    def build_logo_strip(team_list):
        if not team_list:
            return '<span class="no-items">None</span>'

        return "".join(
            f"""
            <div class="opp-logo-wrap" title="{team_meta.get(opp, {}).get('name', opp)}">
                <img class="opp-logo" src="{fetch_team_logo(opp)}" loading="lazy">
            </div>
            """
            for opp in team_list
        )

    html = """
    <html>
    <style>
    body {
        margin: 0;
        background: transparent;
        color: white;
        font-family: sans-serif;
    }

    .table-scroll {
        width: 100%;
        overflow-x: auto;
        overflow-y: visible;
    }

    .sweep-table {
        min-width: 1850px;
        width: 100%;
        border-collapse: collapse;
        color: white;
        table-layout: auto;
    }

    .sweep-table th, .sweep-table td {
        border-bottom: 1px solid #1f3b5c;
        padding: 12px 10px;
        vertical-align: middle;
        text-align: left;
        white-space: nowrap;
    }

    .team-cell {
        display: flex;
        align-items: center;
        gap: 12px;
        white-space: nowrap;
    }

    .team-logo {
        width: 34px;
        height: 34px;
        object-fit: contain;
        flex-shrink: 0;
    }

    .opp-strip {
        display: flex;
        flex-wrap: nowrap;
        gap: 8px;
        align-items: center;
        min-height: 50px;
    }

    .opp-logo-wrap {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 42px;
        height: 42px;
        border-radius: 10px;
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        flex: 0 0 auto;
    }

    .opp-logo {
        width: 30px;
        height: 30px;
        object-fit: contain;
    }

    .no-items {
        opacity: 0.6;
        font-style: italic;
    }

    th.count-col, td.count-col {
        text-align: center;
        width: 84px;
    }

    th.opp-col, td.opp-col {
        min-width: 300px;
    }

    th.net-col, td.net-col {
        text-align: center;
        width: 100px;
    }
    </style>
    <body>
        <div class="table-scroll">
            <table class="sweep-table">
                <thead>
                    <tr>
                        <th>Team</th>
                        <th class="count-col">Sweeps</th>
                        <th class="opp-col">Opponents</th>
                        <th class="count-col">Swept By</th>
                        <th class="opp-col">Opponents</th>
                        <th class="count-col">Tied</th>
                        <th class="opp-col">Opponents</th>
                        <th class="net-col">Net</th>
                    </tr>
                </thead>
                <tbody>
    """

    for _, row in df_summary.iterrows():
        html += f"""
        <tr>
            <td>
                <div class="team-cell">
                    <img class="team-logo" src="{row['TeamLogo']}" loading="lazy">
                    <span>{row['TeamName']}</span>
                </div>
            </td>
            <td class="count-col">{row['SweepCount']}</td>
            <td class="opp-col">
                <div class="opp-strip">{build_logo_strip(row['SweptTeams'])}</div>
            </td>
            <td class="count-col">{row['SweptByCount']}</td>
            <td class="opp-col">
                <div class="opp-strip">{build_logo_strip(row['SweptByTeams'])}</div>
            </td>
            <td class="count-col">{row['TiedCount']}</td>
            <td class="opp-col">
                <div class="opp-strip">{build_logo_strip(row['TiedTeams'])}</div>
            </td>
            <td class="net-col">{row['NetSweepDiff']:+d}</td>
        </tr>
        """

    html += """
                </tbody>
            </table>
        </div>
    </body>
    </html>
    """

    table_height = min(3200, 90 + len(df_summary) * 64)
    components.html(html, height=table_height, scrolling=True)


# ─────────────────────────────────────────────────────────
# PREDICTION MODEL — enhanced with scores & result type
# ─────────────────────────────────────────────────────────
def build_predictions(df: pd.DataFrame) -> pd.DataFrame:
    """
    Predict future games using team-specific stats from completed games.
    Outputs: winner, win probabilities, predicted scores, result type, confidence.

    Methodology:
      1. Win probability — blends each team's contextual win rates
         (home/away, last-5 form, B2B penalty, OT tendency).
      2. Predicted scores — team's avg goals scored/allowed in context,
         with a small regression to the NHL mean (~3.0 gpg).
      3. Predicted result — if |predicted_margin| < 0.60 predict OT/SO
         (closer to 0 → SO, 0.3-0.6 → OT), else REG.
    """
    completed = df[df["GameIsOver"] == True].copy()
    future    = df[df["GameIsOver"] == False].copy()

    if len(future) == 0:
        return pd.DataFrame()

    NHL_AVG_GPG   = 3.05   # league avg goals per team per game (~6.1 total)
    HOME_BOOST    = 0.04   # home-ice advantage
    REGRESSION_W  = 0.25   # weight toward league mean for small samples

    # ── team-level stats from completed games ────────────────────────────
    def weighted_mean(series, league_mean, n_min=10):
        """Shrink estimate toward league mean for small samples."""
        n = len(series)
        w = min(n / n_min, 1.0) * (1 - REGRESSION_W)
        return w * series.mean() + (1 - w) * league_mean

    # Goals scored / allowed, split by home vs away
    away_gf = completed.groupby("AwayTeam")["ActualAwayScore"].apply(
        lambda s: weighted_mean(s, NHL_AVG_GPG))
    away_ga = completed.groupby("AwayTeam")["ActualHomeScore"].apply(
        lambda s: weighted_mean(s, NHL_AVG_GPG))
    home_gf = completed.groupby("HomeTeam")["ActualHomeScore"].apply(
        lambda s: weighted_mean(s, NHL_AVG_GPG))
    home_ga = completed.groupby("HomeTeam")["ActualAwayScore"].apply(
        lambda s: weighted_mean(s, NHL_AVG_GPG))

    # Win rates
    away_wr = completed.groupby("AwayTeam")["AwayWon"].mean()
    home_wr = completed.groupby("HomeTeam")["HomeWon_"].mean()

    # OT/SO tendency per team
    ot_rate = {}
    for team in set(completed["AwayTeam"]) | set(completed["HomeTeam"]):
        tm = completed[(completed["AwayTeam"]==team) | (completed["HomeTeam"]==team)]
        ot_rate[team] = (tm["ActualResult"].isin(["OT","SO"])).mean() if len(tm) > 0 else 0.23

    # Last-5 form (win rate in last 5 games per team)
    def last5_wr(team):
        tm = completed[(completed["AwayTeam"]==team) | (completed["HomeTeam"]==team)]
        tm = tm.sort_values("GameDate").tail(5)
        if len(tm) == 0:
            return 0.5
        wins = ((tm["AwayTeam"]==team) & tm["AwayWon"] |
                (tm["HomeTeam"]==team) & tm["HomeWon_"])
        return wins.mean()

    last5 = {t: last5_wr(t) for t in set(completed["AwayTeam"]) | set(completed["HomeTeam"])}

    results = []
    for _, row in future.iterrows():
        away = row["AwayTeam"]
        home = row["HomeTeam"]

        # ── win probability ─────────────────────────────────────────────
        aw_wr   = away_wr.get(away, 0.45)
        hw_wr   = home_wr.get(home, 0.50)
        aw_l5   = last5.get(away, 0.5)
        hw_l5   = last5.get(home, 0.5)

        # Blend: 50% season rate, 30% contextual (home/away), 20% last-5 form
        away_prob_raw = 0.50 * aw_wr + 0.30 * (1 - hw_wr) + 0.20 * aw_l5
        home_prob_raw = 0.50 * hw_wr + HOME_BOOST + 0.30 * (1 - aw_wr) + 0.20 * hw_l5

        # Back-to-back penalty (if data available)
        if row.get("AwayB2B", False):
            away_prob_raw *= 0.93
        if row.get("HomeB2B", False):
            home_prob_raw *= 0.93

        # Normalise to sum to 1
        total_p = away_prob_raw + home_prob_raw
        away_prob = away_prob_raw / total_p
        home_prob = home_prob_raw / total_p
        away_prob = max(0.10, min(0.90, away_prob))
        home_prob = 1 - away_prob

        # ── score prediction ────────────────────────────────────────────
        # Predicted goals = avg of (attacker's GF) and (defender's GA)
        away_gf_est = away_gf.get(away, NHL_AVG_GPG)
        away_ga_est = away_ga.get(away, NHL_AVG_GPG)
        home_gf_est = home_gf.get(home, NHL_AVG_GPG)
        home_ga_est = home_ga.get(home, NHL_AVG_GPG)

        pred_away_raw = (away_gf_est + home_ga_est) / 2
        pred_home_raw = (home_gf_est + away_ga_est) / 2

        # Nudge scores toward the predicted winner slightly
        margin_factor = abs(away_prob - home_prob)
        if away_prob > home_prob:
            pred_away_raw += 0.3 * margin_factor * 5
        else:
            pred_home_raw += 0.3 * margin_factor * 5

        # Round to nearest integer (NHL scores are whole numbers)
        pred_away_score = max(0, round(pred_away_raw))
        pred_home_score = max(0, round(pred_home_raw))

        # Avoid ties in regulation; break with OT/SO logic below
        if pred_away_score == pred_home_score:
            if away_prob >= home_prob:
                pred_away_score += 1
            else:
                pred_home_score += 1

        # ── result type prediction ──────────────────────────────────────
        # Use combined OT/SO tendency & margin closeness
        margin     = abs(away_prob - home_prob)
        avg_ot     = (ot_rate.get(away, 0.23) + ot_rate.get(home, 0.23)) / 2
        ot_thresh  = avg_ot * 1.3   # boost threshold when teams are well-matched

        if margin < 0.06 and avg_ot >= 0.20:
            pred_result = "SO"
        elif margin < ot_thresh:
            pred_result = "OT"
        else:
            pred_result = "REG"

        # Reflect OT/SO in scores: tighten gap to 1 or 0
        if pred_result in ("OT", "SO"):
            diff = abs(pred_away_score - pred_home_score)
            if diff > 1:
                if pred_away_score > pred_home_score:
                    pred_away_score = pred_home_score + 1
                else:
                    pred_home_score = pred_away_score + 1

        predicted_winner = away if away_prob > home_prob else home
        confidence       = max(away_prob, home_prob)

        results.append({
            "GameDate":           row["GameDate"],
            "AwayTeam":           away,
            "HomeTeam":           home,
            "PredictedWinner":    predicted_winner,
            "PredictedAwayScore": int(pred_away_score),
            "PredictedHomeScore": int(pred_home_score),
            "PredictedResult":    pred_result,
            "AwayWinProb":        round(away_prob * 100, 1),
            "HomeWinProb":        round(home_prob * 100, 1),
            "Confidence":         round(confidence * 100, 1),
            "GameID":             row.get("GameID", ""),
        })

    return pd.DataFrame(results)


@st.cache_data()
def load_index_html() -> str:
    # index_html = ""
    # with open("index.html", "r", encoding="utf-8-sig") as f:
    #     index_html = "".join(f.read())
    # return index_html
    return Path("index.html").read_text(encoding="utf-8")


def load_jersey_workbook():
    # Load jersey workbook
    try:
        return load_jersey_data(path_excel_jerseys)
    except FileNotFoundError:
        st.error(f"❌ Jersey workbook not found:\n\n`{path_excel_jerseys}`\n\nCheck the path at the top of the script.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"❌ Could not load jersey workbook: {e}")
        return pd.DataFrame()


def verify_scores(df):
    """Slow process to check every game landing against every game prediction in the prediction file."""
    game_ids = df["GameID"].tolist()
    st.write(game_ids)
    to_reconcile = []
    for g_id in game_ids:
        results = fetch_game_landing(g_id)
        if results:
            # all_results.append(results)
            df_game = df.loc[df["GameID"] == g_id]
            if not df_game.empty:
                ser_game = df_game.reset_index().iloc[0]
                
                my_away_name = ser_game["AwayTeam"]
                my_home_name = ser_game["HomeTeam"]
                my_away_score = ser_game["ActualAwayScore"]
                my_home_score = ser_game["ActualHomeScore"]
                my_result = ser_game["ActualResult"]
                
                away = results.get("awayTeam", {})
                home = results.get("homeTeam", {})
                away_name = away.get("abbrev", "")
                home_name = home.get("abbrev", "")
                away_score = int(away.get("score", "0"))
                home_score = int(home.get("score", "0"))
                game_result = results.get("periodDescriptor", {}).get("periodType", "REG")
                
                if any([
                    my_away_name != away_name,
                    my_home_name != home_name,
                    my_away_score != away_score,
                    my_home_score != home_score,
                    my_result != game_result,
                ]):
                    to_reconcile.append(dict(
                        g_id=g_id, away=away_name, home=home_name,
                        my_away_score=my_away_score, my_home_score=my_home_score,
                        away_score=away_score, home_score=home_score,
                        my_result=my_result, game_result=game_result
                    ))
        
        # time.sleep(0.08)
        
    return to_reconcile
        

@st.cache_data
def load_stanley_cup_jsons():
    d_a = json.load(open(path_stanley_cup_appearances, "r"))
    d_w = json.load(open(path_stanley_cup_wins, "r"))
    d_l = json.load(open(path_stanley_cup_losses, "r"))
    datas = {
        "appearances": d_a,
        "wins": d_w,
        "losses": d_l
    }
    for k, data in datas.items():
        for k_ in ["colour", "border_colour", "font_colour", "font_back_colour"]:
            # st.write(f"{k=}, {k_=}")
            # st.write(data["ENTITIES"])
            for t, t_data in data["ENTITIES"].items():
                t_data[k_] = Colour(t_data[k_]).hex_code
    return datas


def img_to_uri(path, abbr, path_image_dir=path_image_dir):
    
    # logo = fetch_team_logo(abbr)
    logo = ""
    
    if not logo:    
        path = Path(os.path.join(path_image_dir, path))
        if not path.exists():
            return None
        ext = path.suffix.lower().replace(".", "")
        mime = "png" if ext == "png" else "jpeg"
        with open(path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        return f"data:image/{mime};base64,{b64}"
    else:
        return logo


def page_clinching_scenarios():
    """
    Render the 🏆 Clinching Scenarios page.
 
    Playoff structure (32 teams, 16 qualify):
      • Top 3 from each division  → 12 automatic berths
      • Next 2 points-leaders from each conference (wild-cards) → 4 berths
    """
 
    # ── colour / theme helpers (already defined in main.py) ──────────────────
    GOLD_    = "#c8a84b"
    ICE_     = "#4ab3f4"
    GREEN_   = "#2ecc71"
    RED_     = "#e74c3c"
    BG_CARD  = "#0d1f35"
    BG_DARK  = "#0a0e1a"
    BORDER   = "#1e3a5a"
 
    # ── header ────────────────────────────────────────────────────────────────
    st.markdown('<div class="section-header">🏆 CLINCHING SCENARIOS</div>',
                unsafe_allow_html=True)
    st.caption(
        "Live standings + remaining schedule are pulled from the NHL API. "
        "Clinch numbers are exact (magic-number arithmetic). "
        "Playoff odds are estimated via Monte-Carlo simulation."
    )
 
    # ─── fetch standings ──────────────────────────────────────────────────────
    with st.spinner("Fetching live standings…"):
        raw_standings = fetch_nhl_standings()
 
    if not raw_standings:
        st.error("❌ Could not load NHL standings. The NHL API may be temporarily unavailable.")
        return
 
    # ─── parse standings into a DataFrame ─────────────────────────────────────
    rows = []
    for s in raw_standings:
        abbr = s.get("teamAbbrev", {}).get("default", "")
        meta = TEAM_META.get(abbr, {})
        # Conference / division come from the API but we fall back to TEAM_META
        conf = s.get("conferenceName", meta.get("conf", ""))
        div  = s.get("divisionName",  meta.get("div",  ""))
        rows.append({
            "Abbr":        abbr,
            "TeamName":    s.get("teamName", {}).get("default", meta.get("name", abbr)),
            "Conf":        conf,
            "Div":         div,
            "GP":          int(s.get("gamesPlayed",        0)),
            "W":           int(s.get("wins",               0)),
            "L":           int(s.get("losses",             0)),
            "OTL":         int(s.get("otLosses",           0)),
            "Pts":         int(s.get("points",             0)),
            "RW":          int(s.get("regulationWins",     0)),   # tie-break #2
            "ROW":         int(s.get("regulationPlusOtWins", s.get("row", 0))),  # tie-break #3
            "GF":          int(s.get("goalFor",            0)),
            "GA":          int(s.get("goalAgainst",        0)),
            "DIFF":        int(s.get("goalDifferential",   0)),
            # Points percentage (tie-break #1 proxy — fewer GP with same pts = better)
            "PtsPct":      float(s.get("pointPctg",        0.0)),
        })
    df_st = pd.DataFrame(rows)
 
    if df_st.empty:
        st.error("Standings data appears empty.")
        return
 
    TOTAL_GAMES = 82  # regular-season games per team
 
    df_st["GP_Remaining"] = TOTAL_GAMES - df_st["GP"]
    df_st["Max_Pts"]      = df_st["Pts"] + df_st["GP_Remaining"] * 2   # 2 pts per game
 
    # ── rank within division and conference ───────────────────────────────────
    TIE_BREAK_COLS = ["Pts", "PtsPct", "RW", "ROW", "W", "DIFF", "GF"]
 
    def rank_group(sub: pd.DataFrame) -> pd.Series:
        ranked = sub.sort_values(
            TIE_BREAK_COLS,
            ascending=[False, False, False, False, False, False, False]
        )
        return pd.Series(range(1, len(ranked) + 1), index=ranked.index)
 
    df_st["DivRank"]  = df_st.groupby("Div",  group_keys=False).apply(rank_group)
    df_st["ConfRank"] = df_st.groupby("Conf", group_keys=False).apply(rank_group)
 
    # Wild-card rank: 4th+ in conference, after removing the top-3 of each division
    def wc_rank(conf_df: pd.DataFrame) -> pd.Series:
        non_div_leaders = conf_df[conf_df["DivRank"] > 3].copy()
        wc = non_div_leaders.sort_values(
            TIE_BREAK_COLS,
            ascending=[False, False, False, False, False, False, False]
        )
        ranks = pd.Series(range(1, len(wc) + 1), index=wc.index)
        # Fill division leaders with 0 (already in via div spot)
        full = pd.Series(0, index=conf_df.index)
        full.update(ranks)
        return full
 
    df_st["WCRank"] = df_st.groupby("Conf", group_keys=False).apply(wc_rank)
 
    # ── current playoff picture ───────────────────────────────────────────────
    df_st["InPlayoffs"] = (df_st["DivRank"] <= 3) | (df_st["WCRank"].between(1, 2))
    df_st["PlayoffSpot"] = df_st.apply(
        lambda r:
            f"Div {r['DivRank']}" if r["DivRank"] <= 3
            else (f"WC{int(r['WCRank'])}" if r["WCRank"] in (1, 2) else "—"),
        axis=1
    )
 
    # ── helper: find the "bubble" team (first team out of playoffs) ───────────
    def get_cutoff_pts(conf: str) -> tuple:
        """
        Returns (last_wc_pts, first_out_pts) for the conference.
        The 'magic number' for teams IN the playoffs is relative to first_out.
        The 'magic number' for teams OUT is relative to last_wc.
        """
        conf_df = df_st[df_st["Conf"] == conf]
        in_df   = conf_df[conf_df["InPlayoffs"]].sort_values("Pts", ascending=False)
        out_df  = conf_df[~conf_df["InPlayoffs"]].sort_values("Pts", ascending=False)
        last_wc_pts   = in_df["Pts"].iloc[-1]  if len(in_df)  > 0 else 0
        first_out_pts = out_df["Pts"].iloc[0]  if len(out_df) > 0 else 0
        return last_wc_pts, first_out_pts
 
    # ── Monte-Carlo playoff odds ───────────────────────────────────────────────
    # We simulate the remainder of the season N times, assuming each team wins
    # each remaining game with probability proportional to their current PtsPct.
    # This is fast (vectorised) rather than game-by-game schedule traversal.
    N_SIM = 10_000
 
    @st.cache_data(ttl=300)
    def monte_carlo_odds(_df_st: pd.DataFrame, n_sim: int = N_SIM) -> pd.DataFrame:
        """
        Returns a DataFrame with columns [Abbr, P_DivTop3, P_WildCard, P_Playoffs].
        Simulation assigns remaining GP as Bernoulli wins, weighted by PtsPct.
        Ties are broken by adding a tiny uniform noise to points.
        """
        teams = _df_st.set_index("Abbr")
        abbrs = list(teams.index)
        n = len(abbrs)
 
        # Base probability of winning any given game (proxy = current PtsPct)
        p_win = teams["PtsPct"].clip(0.30, 0.75).values           # shape (n,)
        gp_rem = teams["GP_Remaining"].values.clip(0).astype(int) # shape (n,)
        cur_pts = teams["Pts"].values.astype(float)
        rw_base = teams["RW"].values.astype(float)
        row_base = teams["ROW"].values.astype(float)
        w_base   = teams["W"].values.astype(float)
        gf_base  = teams["GF"].values.astype(float)
        diff_base = teams["DIFF"].values.astype(float)
        conf_arr = teams["Conf"].values
        div_arr  = teams["Div"].values
 
        rng = np.random.default_rng(42)
        div_top3_count = np.zeros(n, dtype=float)
        wc_count       = np.zeros(n, dtype=float)
        playoff_count  = np.zeros(n, dtype=float)
 
        for _ in range(n_sim):
            # Simulate wins for remaining games (binomial)
            sim_wins     = rng.binomial(gp_rem, p_win)                    # (n,)
            # OT losses: ~25 % of losses can be OTL (2 pts = OT win, 1 pt = OTL)
            # Simplified: treat each remaining game as 2 pts if win, 1 pt if OTL (~20 %), 0 if reg loss
            sim_otl      = rng.binomial(gp_rem - sim_wins, 0.22)
            sim_pts      = cur_pts + 2 * sim_wins + sim_otl
            sim_rw       = rw_base + sim_wins * 0.58    # ~58 % of wins are in regulation (approximation)
            sim_row      = row_base + sim_wins * 0.88
            sim_w        = w_base  + sim_wins
            sim_gf       = gf_base + sim_wins * 2.9 + (gp_rem - sim_wins - sim_otl) * 1.8
            sim_diff     = diff_base + sim_wins * 1.1 - (gp_rem - sim_wins) * 1.1
            # Tiny noise for tie-breaking stability
            noise = rng.uniform(0, 1e-4, n)
            eff_pts = sim_pts + noise
 
            # Rank within each division (top-3 = automatic playoff)
            div_top3 = np.zeros(n, bool)
            for div in np.unique(div_arr):
                mask = div_arr == div
                idx  = np.where(mask)[0]
                # Sort by pts desc, then by other tie-break criteria (simplified to pts+noise here)
                sorted_idx = idx[np.argsort(-eff_pts[idx])]
                div_top3[sorted_idx[:3]] = True
 
            # Wild-card: top 2 non-div-top3 per conference
            wc = np.zeros(n, bool)
            for conf in np.unique(conf_arr):
                mask = (conf_arr == conf) & (~div_top3)
                idx  = np.where(mask)[0]
                sorted_idx = idx[np.argsort(-eff_pts[idx])]
                wc[sorted_idx[:2]] = True
 
            in_po = div_top3 | wc
            div_top3_count += div_top3
            wc_count       += wc & (~div_top3)
            playoff_count  += in_po
 
        result = pd.DataFrame({
            "Abbr":        abbrs,
            "P_DivTop3":   (div_top3_count / n_sim * 100).round(1),
            "P_WildCard":  (wc_count       / n_sim * 100).round(1),
            "P_Playoffs":  (playoff_count  / n_sim * 100).round(1),
        })
        return result
 
    with st.spinner("Running Monte-Carlo simulation (10 000 seasons)…"):
        df_odds = monte_carlo_odds(df_st)
 
    df_st = df_st.merge(df_odds, on="Abbr", how="left")
 
    # ═══════════════════════════════════════════════════════════════════════════
    # UI LAYOUT
    # ═══════════════════════════════════════════════════════════════════════════
 
    # ── Conference selector tabs ──────────────────────────────────────────────
    tab_east, tab_west, tab_team = st.tabs(["🔵 Eastern Conference", "🟠 Western Conference", "🔍 Team Deep-Dive"])
 
    def render_conference_table(conf: str):
        """Render a sortable standings + clinching table for one conference."""
        cdf = df_st[df_st["Conf"] == conf].copy()
        cdf = cdf.sort_values(TIE_BREAK_COLS, ascending=[False]*len(TIE_BREAK_COLS)).reset_index(drop=True)
 
        last_wc_pts, first_out_pts = get_cutoff_pts(conf)
 
        # ── magic numbers ──────────────────────────────────────────────────────
        # Magic number to clinch a playoff spot (wild-card):
        #   For teams currently IN: how many points before the first team OUT
        #   cannot catch them even if they win all remaining.
        #   MN = (team_pts + gp_remaining * 2) - first_out_max_pts + 1
        # Simpler classic formula:
        #   MN_clinch = max(0, first_out_max_pts - team_pts + 1)   ← points team needs or opponent loses
        # We display "x" meaning: team clinches when (own_pts + opponent_losses) >= MN
 
        def magic_number_vs_team(team_pts, team_gp_rem, rival_pts, rival_gp_rem):
            """
            Classic magic number: wins + rival losses needed.
            = (rival_pts + rival_gp_rem*2 + 1) - team_pts
            Negative → already clinched vs that rival.
            """
            return max(0, (rival_pts + rival_gp_rem * 2 + 1) - team_pts)
 
        # For each team, find the worst rival they need to clinch against
        # (the first team outside the playoff line in points)
        out_teams = cdf[~cdf["InPlayoffs"]].sort_values("Pts", ascending=False)
        in_teams  = cdf[ cdf["InPlayoffs"]].sort_values("Pts", ascending=True)
 
        # Clinch magic number (for teams in playoffs, vs first out)
        if not out_teams.empty:
            first_out = out_teams.iloc[0]
            cdf["MN_Clinch"] = cdf.apply(
                lambda r: magic_number_vs_team(
                    r["Pts"], r["GP_Remaining"],
                    first_out["Pts"], first_out["GP_Remaining"]
                ) if r["InPlayoffs"] else "—",
                axis=1
            )
        else:
            cdf["MN_Clinch"] = "✅"    # everyone is in
 
        # Elimination number (for teams OUT, vs last team in)
        if not in_teams.empty:
            last_in = in_teams.iloc[0]
            cdf["MN_Elim"] = cdf.apply(
                lambda r: magic_number_vs_team(
                    last_in["Pts"], last_in["GP_Remaining"],
                    r["Pts"], r["GP_Remaining"]
                ) if not r["InPlayoffs"] else "—",
                axis=1
            )
        else:
            cdf["MN_Elim"] = "—"
 
        # ── division sub-tables ────────────────────────────────────────────────
        divs = cdf["Div"].unique()
        for div in sorted(divs):
            st.markdown(f'<div class="section-header" style="font-size:1.1rem">{div} Division</div>',
                        unsafe_allow_html=True)
            ddf = cdf[cdf["Div"] == div].copy()
 
            # Build display rows
            display_rows = []
            for i, (_, r) in enumerate(ddf.iterrows(), 1):
                logo_url = fetch_team_logo(r["Abbr"])
                logo_html = f'<img src="{logo_url}" width="26" style="vertical-align:middle;margin-right:6px">' if logo_url else ""
 
                # Spot indicator
                if r["DivRank"] <= 3:
                    spot_badge = f'<span style="background:#0d3321;color:{GREEN_};border-radius:4px;padding:2px 7px;font-size:0.75rem;font-weight:700">Div {int(r["DivRank"])}</span>'
                elif r["WCRank"] in (1, 2):
                    spot_badge = f'<span style="background:#1a2e05;color:#a3e04a;border-radius:4px;padding:2px 7px;font-size:0.75rem;font-weight:700">WC{int(r["WCRank"])}</span>'
                else:
                    spot_badge = f'<span style="background:#2a0d0d;color:{RED_};border-radius:4px;padding:2px 7px;font-size:0.75rem;font-weight:700">OUT</span>'
 
                # Playoff probability bar
                pct = float(r.get("P_Playoffs", 0))
                bar_color = GREEN_ if pct >= 70 else (GOLD_ if pct >= 35 else RED_)
                prob_bar = (
                    f'<div style="background:#1e3a5a;border-radius:3px;height:8px;width:80px;display:inline-block;vertical-align:middle">'
                    f'<div style="background:{bar_color};width:{pct:.0f}%;height:100%;border-radius:3px"></div></div>'
                    f'&nbsp;<span style="font-size:0.8rem;color:{bar_color}">{pct:.0f}%</span>'
                )
 
                mn = r["MN_Clinch"]
                el = r["MN_Elim"]
                mn_str = (
                    '<span style="color:#2ecc71;font-weight:700">✅ CLINCHED</span>' if mn == 0
                    else (f'<span style="color:{GOLD_}">{mn}</span>' if isinstance(mn, int) else str(mn))
                )
                el_str = (
                    '<span style="color:#e74c3c;font-weight:700">❌ ELIMINATED</span>' if el == 0
                    else (f'<span style="color:{RED_}">{el}</span>' if isinstance(el, int) else str(el))
                )
 
                display_rows.append({
                    "": logo_html + f'<b style="color:#ccd6e0">{r["TeamName"]}</b>',
                    "Spot":   spot_badge,
                    "GP":     r["GP"],
                    "Pts":    f'<span style="color:{GOLD_};font-weight:700">{r["Pts"]}</span>',
                    "W-L-OTL": f'{r["W"]}-{r["L"]}-{r["OTL"]}',
                    "RW":     r["RW"],
                    "GP Left": r["GP_Remaining"],
                    "Max Pts": r["Max_Pts"],
                    "Magic#": mn_str,
                    "Elim#":  el_str,
                    "Playoff %": prob_bar,
                })
 
            display_df_obj = pd.DataFrame(display_rows)
            st.markdown(
                display_df_obj.to_html(escape=False, index=False),
                unsafe_allow_html=True
            )
            st.markdown("<br>", unsafe_allow_html=True)
 
        # ── Wild-Card picture ─────────────────────────────────────────────────
        st.markdown(f'<div class="section-header" style="font-size:1.1rem">Wild-Card Race — {conf}</div>',
                    unsafe_allow_html=True)
 
        # All teams sorted by points; mark who's in the WC slots
        wc_df = cdf.sort_values(TIE_BREAK_COLS, ascending=[False]*len(TIE_BREAK_COLS)).reset_index(drop=True)
        # Show only teams within 10 points of the last WC spot (to keep it focused)
        bubble_pts = last_wc_pts - 10
        wc_focus = wc_df[wc_df["Pts"] >= bubble_pts].copy()
 
        wc_rows = []
        for _, r in wc_focus.iterrows():
            spot = r["PlayoffSpot"]
            pts_diff = r["Pts"] - last_wc_pts
            diff_str = (
                f'+{pts_diff}' if pts_diff > 0
                else (f'{pts_diff}' if pts_diff < 0 else '—')
            )
            diff_color = GREEN_ if pts_diff >= 0 else RED_
            logo_url = fetch_team_logo(r["Abbr"])
            logo_html = f'<img src="{logo_url}" width="22" style="vertical-align:middle;margin-right:5px">' if logo_url else ""
 
            wc_rows.append({
                "Team":    logo_html + r["TeamName"],
                "Spot":    spot,
                "Pts":     r["Pts"],
                "GP":      r["GP"],
                "GP Left": r["GP_Remaining"],
                "Max Pts": r["Max_Pts"],
                "vs Bubble": f'<span style="color:{diff_color};font-weight:700">{diff_str}</span>',
                "PO%":     f'<b style="color:{GREEN_ if r["P_Playoffs"] >= 50 else RED_}">{r["P_Playoffs"]:.0f}%</b>',
            })
 
        if wc_rows:
            st.markdown(
                pd.DataFrame(wc_rows).to_html(escape=False, index=False),
                unsafe_allow_html=True
            )
 
    # ── TAB: Eastern Conference ───────────────────────────────────────────────
    with tab_east:
        render_conference_table("Eastern")
 
    # ── TAB: Western Conference ───────────────────────────────────────────────
    with tab_west:
        render_conference_table("Western")
 
    # ── TAB: Team Deep-Dive ───────────────────────────────────────────────────
    with tab_team:
        st.markdown('<div class="section-header" style="font-size:1.1rem">TEAM CLINCHING SCENARIOS</div>',
                    unsafe_allow_html=True)
 
        # Team selector
        sorted_teams = sorted(df_st["Abbr"].tolist())
        col_sel, col_empty = st.columns([1, 3])
        with col_sel:
            sel_abbr = st.selectbox(
                "Select team",
                sorted_teams,
                format_func=lambda a: f"{a} — {TEAM_META.get(a, {}).get('name', a)}"
            )
 
        team_row = df_st[df_st["Abbr"] == sel_abbr].iloc[0]
        conf     = team_row["Conf"]
        div      = team_row["Div"]
        conf_df  = df_st[df_st["Conf"] == conf].copy()
 
        logo_url = fetch_team_logo(sel_abbr)
        team_name = team_row["TeamName"]
 
        # ── Team header card ──────────────────────────────────────────────────
        spot      = team_row["PlayoffSpot"]
        in_po     = team_row["InPlayoffs"]
        div_rank  = int(team_row["DivRank"])
        wc_rank   = int(team_row["WCRank"]) if team_row["WCRank"] > 0 else None
        p_po      = float(team_row.get("P_Playoffs", 0))
        p_div     = float(team_row.get("P_DivTop3",  0))
        p_wc      = float(team_row.get("P_WildCard", 0))
 
        spot_color = GREEN_ if in_po else RED_
        spot_text  = spot if spot != "—" else "OUT"
 
        st.markdown(f"""
        <div style="background:{BG_CARD};border:1px solid {BORDER};border-left:5px solid {spot_color};
                    border-radius:10px;padding:20px 24px;margin-bottom:18px;display:flex;align-items:center;gap:18px">
            <img src="{logo_url}" width="72" style="object-fit:contain">
            <div style="flex:1">
                <div style="font-family:'Bebas Neue',sans-serif;font-size:2rem;color:{GOLD_};letter-spacing:3px">{team_name}</div>
                <div style="color:#8899aa;font-size:0.85rem">{conf} Conference · {div} Division</div>
            </div>
            <div style="text-align:right">
                <div style="font-family:'Bebas Neue',sans-serif;font-size:2.5rem;color:{GOLD_}">{int(team_row['Pts'])}</div>
                <div style="color:#8899aa;font-size:0.75rem;letter-spacing:1px">POINTS</div>
                <div style="margin-top:6px">
                    <span style="background:{'#0d3321' if in_po else '#2a0d0d'};color:{spot_color};
                                 border-radius:5px;padding:3px 12px;font-weight:700;font-size:0.9rem">
                        {spot_text}
                    </span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
 
        # ── Key metrics row ───────────────────────────────────────────────────
        m1, m2, m3, m4, m5, m6 = st.columns(6)
        m1.metric("GP", int(team_row["GP"]))
        m2.metric("W–L–OTL", f"{int(team_row['W'])}–{int(team_row['L'])}–{int(team_row['OTL'])}")
        m3.metric("Pts", int(team_row["Pts"]))
        m4.metric("GP Remaining", int(team_row["GP_Remaining"]))
        m5.metric("Max Pts", int(team_row["Max_Pts"]))
        m6.metric("Reg Wins (RW)", int(team_row["RW"]))
 
        # ── Playoff odds gauge ────────────────────────────────────────────────
        st.markdown("#### 🎲 Estimated Playoff Odds (Monte-Carlo · 10 000 simulations)")
        g1, g2, g3 = st.columns(3)
 
        def gauge_fig(value, title, color):
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=value,
                number={"suffix": "%", "font": {"color": GOLD_, "size": 36}},
                title={"text": title, "font": {"color": "#8899aa", "size": 13}},
                gauge={
                    "axis": {"range": [0, 100], "tickcolor": "#8899aa"},
                    "bar": {"color": color},
                    "bgcolor": BG_CARD,
                    "bordercolor": BORDER,
                    "steps": [
                        {"range": [0,  35], "color": "#2a0d0d"},
                        {"range": [35, 70], "color": "#2a2000"},
                        {"range": [70, 100],"color": "#0d3321"},
                    ],
                    "threshold": {
                        "line": {"color": GOLD_, "width": 3},
                        "thickness": 0.75,
                        "value": value
                    }
                }
            ))
            fig.update_layout(
                paper_bgcolor=BG_DARK, font_color="#ccd6e0",
                height=220, margin=dict(l=20, r=20, t=40, b=10)
            )
            return fig
 
        g1.plotly_chart(gauge_fig(p_po,  "Make Playoffs",   GREEN_ if p_po >= 70 else (GOLD_ if p_po >= 35 else RED_)), use_container_width=True)
        g2.plotly_chart(gauge_fig(p_div, "Win Div Top-3",   ICE_   if p_div >= 50 else GOLD_), use_container_width=True)
        g3.plotly_chart(gauge_fig(p_wc,  "Wild-Card Only",  GOLD_  if p_wc >= 30  else RED_),  use_container_width=True)
 
        # ── Magic / Elimination numbers ───────────────────────────────────────
        st.markdown("#### 🔢 Clinching & Elimination Numbers")
 
        # Re-compute for this team against every rival in the conference
        rival_rows = []
        for _, rival in conf_df.iterrows():
            if rival["Abbr"] == sel_abbr:
                continue
            # Magic number: points we need combined with rival losses
            mn = max(0, (rival["Pts"] + rival["GP_Remaining"] * 2 + 1) - team_row["Pts"])
            rel = rival["Pts"] - team_row["Pts"]  # positive = rival leads
 
            rival_rows.append({
                "rival_abbr":  rival["Abbr"],
                "rival_name":  rival["TeamName"],
                "rival_div":   rival["Div"],
                "rival_spot":  rival["PlayoffSpot"],
                "rival_pts":   int(rival["Pts"]),
                "rival_gp":    int(rival["GP"]),
                "rival_gpr":   int(rival["GP_Remaining"]),
                "rival_maxpts":int(rival["Max_Pts"]),
                "mn":          mn,
                "pts_diff":    rel,
                "in_playoffs": rival["InPlayoffs"],
            })
 
        rival_df = pd.DataFrame(rival_rows)
 
        if in_po:
            st.markdown(
                f"**{team_name}** is currently **in a playoff spot** ({spot}). "
                f"Their clinching number vs the first team out:"
            )
            out_rivals = rival_df[~rival_df["in_playoffs"]].sort_values("rival_pts", ascending=False)
            if not out_rivals.empty:
                first_out = out_rivals.iloc[0]
                mn_clinch = first_out["mn"]
                st.markdown(f"""
                <div style="background:{BG_CARD};border:2px solid {GREEN_};border-radius:8px;padding:16px;margin:10px 0">
                    <span style="font-family:'Bebas Neue',sans-serif;font-size:1.8rem;color:{GREEN_}">
                        Magic Number: {mn_clinch if mn_clinch > 0 else "✅ CLINCHED"}
                    </span><br>
                    <span style="color:#8899aa">
                        vs <b style="color:#ccd6e0">{first_out['rival_name']}</b>
                        ({int(first_out['rival_pts'])} pts, {int(first_out['rival_gpr'])} GP left).
                        Any combination of {team_name} wins + {first_out['rival_name']} losses/OTL
                        totalling <b style="color:{GREEN_}">{mn_clinch}</b> clinches a playoff berth.
                    </span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown(
                f"**{team_name}** is currently **outside a playoff spot**. "
                f"Their elimination number vs the last team in:"
            )
            in_rivals = rival_df[rival_df["in_playoffs"]].sort_values("rival_pts", ascending=True)
            if not in_rivals.empty:
                last_in = in_rivals.iloc[0]
                # Elim number: when is it mathematically impossible for this team to catch last_in?
                # = max_pts_for_this_team - last_in_max_pts + 1  (simplified)
                elim_n = max(0, (last_in["rival_pts"] + last_in["rival_gpr"] * 2 + 1) - team_row["Pts"])
                can_still_make_it = team_row["Max_Pts"] >= last_in["rival_pts"]
                if can_still_make_it:
                    st.markdown(f"""
                    <div style="background:{BG_CARD};border:2px solid {GOLD_};border-radius:8px;padding:16px;margin:10px 0">
                        <span style="font-family:'Bebas Neue',sans-serif;font-size:1.8rem;color:{GOLD_}">
                            Still Alive — Need {elim_n} pts OR rival losses
                        </span><br>
                        <span style="color:#8899aa">
                            Last team in: <b style="color:#ccd6e0">{last_in['rival_name']}</b>
                            ({int(last_in['rival_pts'])} pts, {int(last_in['rival_gpr'])} GP left).
                            {team_name} max pts: <b>{int(team_row['Max_Pts'])}</b>.
                        </span>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="background:#2a0d0d;border:2px solid {RED_};border-radius:8px;padding:16px;margin:10px 0">
                        <span style="font-family:'Bebas Neue',sans-serif;font-size:1.8rem;color:{RED_}">
                            ❌ MATHEMATICALLY ELIMINATED
                        </span><br>
                        <span style="color:#8899aa">
                            Max possible points ({int(team_row['Max_Pts'])}) cannot reach
                            <b style="color:#ccd6e0">{last_in['rival_name']}</b>'s current {int(last_in['rival_pts'])} pts.
                        </span>
                    </div>
                    """, unsafe_allow_html=True)
 
        # ── Scenario generator ────────────────────────────────────────────────
        st.markdown("#### 📋 Scenario Explorer")
        st.caption(
            "Adjust the sliders to model different outcomes for the remainder of the season. "
            "The standings update live based on your inputs."
        )
 
        gp_rem = int(team_row["GP_Remaining"])
        if gp_rem == 0:
            st.info("No games remaining — the season is over for this team.")
        else:
            sc1, sc2 = st.columns(2)
            with sc1:
                sim_wins_user = st.slider(
                    f"{sel_abbr} wins in remaining {gp_rem} games",
                    0, gp_rem, min(gp_rem, max(0, int(gp_rem * team_row["PtsPct"]))),
                    key="slider_wins"
                )
            with sc2:
                # OTL can only happen on losses
                max_otl = gp_rem - sim_wins_user
                sim_otl_user = st.slider(
                    f"of those losses, how many are OTL?",
                    0, max_otl, min(max_otl, max(0, int(max_otl * 0.22))),
                    key="slider_otl"
                )
 
            proj_pts = int(team_row["Pts"]) + sim_wins_user * 2 + sim_otl_user
            proj_rw  = int(team_row["RW"])  + int(sim_wins_user * 0.58)
 
            st.markdown(f"""
            <div style="background:{BG_CARD};border:1px solid {BORDER};border-radius:8px;padding:14px 20px;margin:12px 0;display:flex;gap:32px">
                <div><div style="color:{GOLD_};font-family:'Bebas Neue',sans-serif;font-size:1.6rem">{proj_pts}</div>
                     <div style="color:#8899aa;font-size:0.75rem;letter-spacing:1px">PROJECTED PTS</div></div>
                <div><div style="color:{ICE_};font-family:'Bebas Neue',sans-serif;font-size:1.6rem">{sim_wins_user}-{gp_rem - sim_wins_user - sim_otl_user}-{sim_otl_user}</div>
                     <div style="color:#8899aa;font-size:0.75rem;letter-spacing:1px">REMAINING W-L-OTL</div></div>
                <div><div style="color:{GREEN_};font-family:'Bebas Neue',sans-serif;font-size:1.6rem">{proj_rw}</div>
                     <div style="color:#8899aa;font-size:0.75rem;letter-spacing:1px">PROJECTED RW</div></div>
            </div>
            """, unsafe_allow_html=True)
 
            # Would this projected total put the team in the playoffs?
            # Compare against each conference rival's current pts (static)
            proj_conf = conf_df.copy()
            proj_conf.loc[proj_conf["Abbr"] == sel_abbr, "Pts"] = proj_pts
            proj_conf.loc[proj_conf["Abbr"] == sel_abbr, "RW"]  = proj_rw
            proj_conf = proj_conf.sort_values(
                ["Div", "Pts", "RW"], ascending=[True, False, False]
            )
 
            # Re-rank division
            proj_conf["SimDivRank"] = proj_conf.groupby("Div")["Pts"].rank(
                ascending=False, method="min"
            ).astype(int)
            proj_conf["SimInDiv"]   = proj_conf["SimDivRank"] <= 3
 
            # Wild-card
            proj_conf["SimWCRank"] = 0
            for c_ in ["Eastern", "Western"]:
                sub = proj_conf[(proj_conf["Conf"] == c_) & (~proj_conf["SimInDiv"])].copy()
                sub = sub.sort_values("Pts", ascending=False).reset_index()
                for rank_, idx_ in enumerate(sub["index"].tolist(), 1):
                    proj_conf.loc[idx_, "SimWCRank"] = rank_
 
            proj_conf["SimInPO"] = proj_conf["SimInDiv"] | proj_conf["SimWCRank"].between(1, 2)
 
            team_sim = proj_conf[proj_conf["Abbr"] == sel_abbr].iloc[0]
            sim_in = bool(team_sim["SimInPO"])
            sim_div_r = int(team_sim["SimDivRank"])
            sim_wc_r  = int(team_sim["SimWCRank"])
 
            if sim_in:
                sim_spot = f"Div {sim_div_r}" if sim_div_r <= 3 else f"WC{sim_wc_r}"
                st.success(f"✅ With this scenario, **{team_name}** QUALIFIES for the playoffs as **{sim_spot}**.")
            else:
                pts_needed = proj_conf[proj_conf["SimInPO"] & (proj_conf["Conf"] == conf)]["Pts"].min() - proj_pts
                st.error(f"❌ With this scenario, **{team_name}** misses the playoffs by ~**{max(0, pts_needed)} pts**.")
 
        # ── Remaining schedule snapshot ───────────────────────────────────────
        st.markdown("#### 📅 Remaining Schedule")
        with st.spinner(f"Fetching {sel_abbr} remaining schedule…"):
            remaining_games = fetch_nhl_team_schedule(sel_abbr)
 
        if remaining_games:
            sched_rows = []
            for g in remaining_games[:20]:   # cap at 20 for display
                gdate  = g.get("gameDate", "")
                away   = g.get("awayTeam",  {}).get("abbrev", "")
                home   = g.get("homeTeam",  {}).get("abbrev", "")
                is_home = home == sel_abbr
                opp    = away if is_home else home
                side   = "🏠 Home" if is_home else "✈️ Away"
                opp_pts = int(df_st[df_st["Abbr"] == opp]["Pts"].values[0]) if opp in df_st["Abbr"].values else "—"
                opp_po  = bool(df_st[df_st["Abbr"] == opp]["InPlayoffs"].values[0]) if opp in df_st["Abbr"].values else False
                opp_logo = fetch_team_logo(opp)
                opp_html = f'<img src="{opp_logo}" width="20" style="vertical-align:middle;margin-right:5px">{opp}' if opp_logo else opp
                sched_rows.append({
                    "Date":      gdate,
                    "H/A":       side,
                    "Opponent":  opp_html,
                    "Opp Pts":   opp_pts,
                    "Opp In PO": "🟢" if opp_po else "🔴",
                })
            if sched_rows:
                st.markdown(
                    pd.DataFrame(sched_rows).to_html(escape=False, index=False),
                    unsafe_allow_html=True
                )
        else:
            st.info("No remaining regular-season games found (or season is complete).")
 
        # ── Head-to-head vs bubble rivals ────────────────────────────────────
        st.markdown("#### ⚔️ Remaining Games vs Bubble Rivals")
        st.caption("Teams within 5 points of the wild-card cut-line in your conference.")
 
        if remaining_games:
            bubble_abbrs = set(
                conf_df[
                    (conf_df["Pts"] >= team_row["Pts"] - 5) & (conf_df["Abbr"] != sel_abbr)
                ]["Abbr"].tolist()
            )
            h2h_rows = []
            for g in remaining_games:
                away = g.get("awayTeam", {}).get("abbrev", "")
                home = g.get("homeTeam", {}).get("abbrev", "")
                opp  = away if home == sel_abbr else home
                if opp in bubble_abbrs:
                    is_home = home == sel_abbr
                    opp_logo = fetch_team_logo(opp)
                    opp_html = f'<img src="{opp_logo}" width="20" style="vertical-align:middle;margin-right:5px">{opp}' if opp_logo else opp
                    opp_pts  = int(df_st[df_st["Abbr"] == opp]["Pts"].values[0]) if opp in df_st["Abbr"].values else "—"
                    h2h_rows.append({
                        "Date":     g.get("gameDate",""),
                        "H/A":      "🏠 Home" if is_home else "✈️ Away",
                        "Rival":    opp_html,
                        "Rival Pts": opp_pts,
                        "Importance": "🔥 Critical" if abs(opp_pts - team_row["Pts"]) <= 4 else "⚠️ Key",
                    })
            if h2h_rows:
                st.markdown(
                    pd.DataFrame(h2h_rows).to_html(escape=False, index=False),
                    unsafe_allow_html=True
                )
                st.caption(
                    f"These are direct points-stealing opportunities — a win takes 2 pts away from a rival "
                    f"(you gain 2, they gain 0) for a net 2-pt swing."
                )
            else:
                st.info("No upcoming games vs bubble rivals found.")
 
    # ── Legend / methodology ──────────────────────────────────────────────────
    with st.expander("ℹ️ Methodology & Tie-Breaking Rules"):
        st.markdown("""
**Playoff qualification:**
- Top **3** teams from each division (Atlantic, Metropolitan, Central, Pacific) qualify automatically.
- The next **2** highest-points teams from each conference (Eastern / Western) qualify as Wild-Cards.
- 16 teams total qualify.
 
**Tie-Breaking Order (official NHL rules):**
1. Fewer games played (superior points percentage) — teams with a game in hand rank higher at equal points.
2. Greater Regulation Wins (RW) — wins in regulation time only.
3. Greater ROW (Regulation + Overtime Wins) — excludes Shootout wins.
4. Greater total Wins (W) — includes Shootout wins.
5. Points in head-to-head games among tied clubs.
6. Greater goal differential (GF − GA) for the full season.
7. Greater goals scored (GF) for the full season.
 
**Magic Number:**  
`MN = (Rival Max Pts + 1) − Own Current Pts`  
= the number of combined "own wins + rival losses/OTL" needed to guarantee finishing ahead of that rival.  
When MN = 0, the team has clinched ahead of that rival.
 
**Playoff Odds:**  
Estimated via Monte-Carlo simulation (10 000 random season completions). Each remaining game is modelled as a Bernoulli trial with win probability ≈ team's current points percentage (clipped to 30–75%). OT losses are assigned at ~22% of losses. Final standings in each simulation are re-ranked using points + tie-breaker noise; the fraction of simulations where a team makes the playoffs gives the estimated odds.
        """)


def normalize_record_key(val):
    if isinstance(val, tuple):
        return val
    if isinstance(val, str):
        s = val.strip().replace("(", "").replace(")", "").replace(" ", "")
        if "," in s:
            parts = tuple(int(x) for x in s.split(",") if x != "")
        else:
            parts = tuple(int(x) for x in s.split("-") if x != "")
        return parts
    return (0, 0, 0)


def make_step_colorscale_from_record_map(record_colour_map):
    """
    Build a discrete/stepped Plotly colorscale from TEAM_RECORD_COLOUR_MAP.
    Uses the integer rank 'i' for exact bucket coloring.
    """
    # only tuple keys, not the duplicated str keys
    tuple_items = [(k, v) for k, v in record_colour_map.items() if isinstance(k, tuple)]
    tuple_items = sorted(tuple_items, key=lambda kv: kv[1]["i"])

    max_i = max(v["i"] for _, v in tuple_items)
    if max_i == 0:
        return [[0.0, "#707070"], [1.0, "#707070"]], max_i

    colorscale = []
    for rec, meta in tuple_items:
        i = meta["i"]
        color = meta["color"]

        left = i / max_i
        right = i / max_i

        # make it stepped by duplicating edges
        prev_edge = max(0.0, (i - 1) / max_i)
        curr_edge = min(1.0, i / max_i)

        colorscale.append([prev_edge, color])
        colorscale.append([curr_edge, color])

    # ensure exact zero bucket exists for (0,0,0)
    if (0, 0, 0) in record_colour_map:
        zero_color = record_colour_map[(0, 0, 0)]["color"]
        colorscale.insert(0, [0.0, zero_color])

    # sort for safety
    colorscale = sorted(colorscale, key=lambda x: x[0])
    return colorscale, max_i


def build_team_order(df_records, team_meta, sort_mode, reverse=False):
    active_teams = [t for t in team_meta if team_meta[t].get("active", True)]

    if sort_mode == "Team":
        return sorted(active_teams, reverse=reverse)

    if sort_mode == "Conference":
        return sorted(
            active_teams,
            key=lambda t: (
                team_meta[t].get("conf", ""),
                team_meta[t].get("name", ""),
                t
            ),
            reverse=reverse
        )

    if sort_mode == "Division":
        return sorted(
            active_teams,
            key=lambda t: (
                team_meta[t].get("div", ""),
                team_meta[t].get("conf", ""),
                team_meta[t].get("name", ""),
                t
            ),
            reverse=reverse
        )

    if sort_mode == "Best to Worst Record":
        team_points = {t: 0 for t in active_teams}
        team_games = {t: 0 for t in active_teams}

        for _, r in df_records.iterrows():
            away = r["AwayTeam"]
            home = r["HomeTeam"]

            if away in team_points:
                team_points[away] += 2 * r.get("AwayWon", 0) + r.get("A_ETL", 0)
                team_games[away] += r.get("GameID", 0)

            if home in team_points:
                team_points[home] += 2 * r.get("HomeWon", 0) + r.get("H_ETL", 0)
                team_games[home] += r.get("GameID", 0)

        return sorted(
            active_teams,
            key=lambda t: (
                -(team_points[t] / max(team_games[t], 1)),
                -team_points[t],
                t
            ),
            reverse=reverse
        )

    return sorted(active_teams, reverse=reverse)


def render_team_record_heatmap_fast(
    df,
    x_team_order,
    y_team_order,
    record_colour_map=TEAM_RECORD_COLOUR_MAP,
    dark_theme=True,
    impossible_color="#707070"
):
    dff = df.copy()

    colorscale, max_i = make_step_colorscale_from_record_map(record_colour_map)

    x_idx = {team: i for i, team in enumerate(x_team_order)}
    y_idx = {team: i for i, team in enumerate(y_team_order)}

    n_rows = len(y_team_order)
    n_cols = len(x_team_order)

    z = np.full((n_rows, n_cols), np.nan, dtype=float)
    hover = np.full((n_rows, n_cols), "", dtype=object)
    
    res_df = pd.DataFrame(columns=["ID", "Scenario", "AwayTeam", "HomeTeam", "PCT", "PTS"])

    # Fill valid matchup values
    for idx, row in dff.iterrows():
        away = row["AwayTeam"]
        home = row["HomeTeam"]

        if home not in x_idx or away not in y_idx:
            continue

        rec = normalize_record_key(row["Record"])
        meta = record_colour_map.get(
            rec,
            record_colour_map.get(str(rec), record_colour_map[(0, 0, 0)])
        )

        i = y_idx[away]
        j = x_idx[home]

        z[i, j] = meta["i"]
        scenario = f"{away} vs {home}"
        hover[i, j] = (
            f"{scenario}"
            f"<br>Record: {rec}"
            f"<br>Points %: {meta['pct']:.3f}"
            f"<br>Score: {meta['score']}"
        )
        if away == home:
            res_df.loc[idx] = [None for _ in res_df.columns]
        else:
            res_df.loc[idx] = [row["GameID"], scenario, away, home, meta["pct"], meta["score"]]

    # Build impossible-cell mask
    impossible_mask = np.full((n_rows, n_cols), np.nan, dtype=float)

    for i, away in enumerate(y_team_order):
        for j, home in enumerate(x_team_order):
            if away == home:
                impossible_mask[i, j] = 1
                hover[i, j] = f"{away} vs {home}<br>Not Applicable"

    fig = go.Figure()

    # Base grey layer for impossible cells
    fig.add_trace(
        go.Heatmap(
            z=impossible_mask,
            x=x_team_order,
            y=y_team_order,
            colorscale=[
                [0.0, impossible_color],
                [1.0, impossible_color]
            ],
            showscale=False,
            hoverinfo="skip",
            xgap=1,
            ygap=1
        )
    )

    # Main record layer
    fig.add_trace(
        go.Heatmap(
            z=z,
            x=x_team_order,
            y=y_team_order,
            text=hover,
            hovertemplate="%{text}<extra></extra>",
            zmin=0,
            zmax=max_i,
            colorscale=colorscale,
            showscale=False,
            xgap=1,
            ygap=1,
            hoverongaps=False
        )
    )

    fig.update_layout(
        title="Team vs Team Record Heatmap",
        height=900,
        margin=dict(l=10, r=10, t=50, b=10),
        plot_bgcolor="#000814" if dark_theme else "white",
        paper_bgcolor="#000814" if dark_theme else "white",
        font=dict(color="white" if dark_theme else "black"),
        xaxis=dict(side="top"),
        yaxis=dict(autorange="reversed")
    )

    return fig, res_df


@st.cache_data
def load_hockey_pool_data():
    with open(path_hockey_pool_data, "r") as f:
        data = json.load(f)
    res = {}
    for k, v in data.items():
        res[k] = pd.DataFrame(v)
    return res


# def page_hockey_pool():
#     dfs: dict[str, pd.DataFrame] = load_hockey_pool_data()
#     for k, df in dfs.items():
#         display_df(df, title=k)
        
#     df_people: pd.DataFrame = dfs["people"]
#     df_pools: pd.DataFrame = dfs["pools"]
        
#     cols_pool_results = st.columns(len(df_pools))
    
#     lst_df_pool_e = []
    
#     for i, row in df_pools.iterrows():
#         with cols_pool_results[i]:
#             year = row["year"]
#             fee = row["fee"]
#             pct_prize = row["pctPrize"]
#             standings = row["standings"]
#             n_people = len(standings)
#             total_fees = fee * pct_prize * n_people
#             prizes = [total_fees * 0.5, total_fees * 0.35, total_fees * 0.15]
            
#             st.header(f"{year} playoffs")
#             for i, people_id in enumerate(standings):
#                 name = df_people[df_people["id"] == people_id].reset_index().loc[0, "name"]
#                 winnings = prizes[i] if i < len(prizes) else 0
#                 if winnings:
#                     st.write(f"{i + 1} - prize: $ {winnings:,.2f} - {name}")
#                 else:
#                     st.write(f"{i + 1} - {name}")
#                 lst_df_pool_e.append(pd.DataFrame([{
#                     "year": year,
#                     "fee": fee,
#                     "pctPrize": pct_prize,
#                     "totalPrizes": total_fees,
#                     "nPlayers": n_people,
#                     "place": i + 1,
#                     "winnings": winnings,
#                     "person": people_id
#                 }]))
               
#     df_pools_e = pd.concat(lst_df_pool_e, ignore_index=True)
#     display_df(df_pools_e, "df_pools_e")
    
#     df_people_e = df_people.copy()
#     df_people_e["best"] = None
#     df_people_e["worst"] = None
#     df_people_e["sum"] = None
#     df_people_e["inv"] = None
#     df_people_e["mean"] = None
#     df_people_e["lastYear"] = None
#     df_people_e["totalPayed"] = 0
#     df_people_e["timesPlayed"] = 0
#     df_people_e["totalWinnings"] = 0
#     for i, row in df_people.iterrows():
#         people_id = row["id"]
#         df_pools_person = df_pools_e[df_pools_e["person"] == people_id]
#         df_people_e.loc[i, "best"] = df_pools_person["place"].min()
#         df_people_e.loc[i, "worst"] = df_pools_person["place"].max()
#         df_people_e.loc[i, "sum"] = df_pools_person["place"].sum()
#         df_people_e.loc[i, "inv"] = df_pools_person["nPlayers"].sum() - df_pools_person["place"].sum()
#         df_people_e.loc[i, "mean"] = df_pools_person["place"].mean()
#         df_people_e.loc[i, "lastYear"] = df_pools_person["year"].max()
#         df_people_e.loc[i, "totalPayed"] = df_pools_person["fee"].sum()
#         df_people_e.loc[i, "timesPlayed"] = df_pools_person["place"].count()
#         df_people_e.loc[i, "totalWinnings"] = df_pools_person["winnings"].sum()
        
#     df_people_e["totalEarnings"] = df_people_e["totalWinnings"] - df_people_e["totalPayed"]
#     df_people_e["earningsPerYear"] = df_people_e["totalEarnings"] / df_people_e["timesPlayed"]
#     df_people_e["score"] = df_people_e["inv"] + (df_people_e["totalEarnings"] / 10)
#     # df_people_e.sort_values(["totalEarnings", "timesPlayed", "mean"], ascending=[False, False, True], inplace=True)
#     df_people_e.sort_values(["score"], ascending=[False], inplace=True)
#     display_df(df_people_e, "df_people_e")


@st.cache_data
def read_pool_sheet(path, debug=False):
    search_text_start_picks = ["East Fwd 1 (pick 1)", "East - Forward 1 (pick 1)", "West - Forward 1 (pick 1)"]
    found_start_picks = 0
    # 4 boxes per row, 3 rows per conference, 6 text rows per box (+1 header & only 4 in the team boxes). => 6 * (6+1) = 42 lines of text in 24 boxes (4 team boxes only have 4 lines +1 header)
    box_data = [
        {
            "name": None,
            "row": i // 4,
            "col": i % 4,
            "picks": [],
        }
        for i in range(24)
    ]
    # line_by_line_data = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            if debug:
                st.write(f"Page #{page.page_number}")
                # st.write(page.extract_text()[:15])
                # st.write(page.extract_text())
                st.write(page.find_table())
            table = page.find_table()
            if table:
                for i, data in enumerate(table.extract()):
                    if debug:
                        st.write(f"{i=}")
                        st.write(data)
                    for j, txt in enumerate(data):
                        if not found_start_picks:
                            for stsp in search_text_start_picks:
                                if stsp.lower() in str(txt).lower():
                                    found_start_picks = 1
                                    break
                        if found_start_picks and txt:
                            if debug:
                                st.write(f"{j=}, {found_start_picks=}")
                                st.write(txt)
                                st.write("'__' in txt: {txt.split('__')=}")
                            for k, txt_s in enumerate(txt.split("__")):
                                if debug:
                                    st.write(f"{k=}")
                                    st.write(txt_s)
                                if k == 0:
                                    box_data[found_start_picks - 1]["name"] = txt_s.strip()
                                else:
                                    # row = found_start_picks // 4
                                    # col = found_start_picks % 4
                                    tss = txt_s.split(":")
                                    ppg = tss[-1].strip()
                                    tss_t = "".join(tss[:-1]).strip()
                                    tss_ts = tss_t.split("(")
                                    val = "".join(tss_ts[:-1]).strip()
                                    team = tss_ts[-1].removesuffix(")").strip()
                                    box_data[found_start_picks - 1]["picks"].append({"pick": val, "team": team, "ppg": ppg})
                            found_start_picks += 1

    if debug:
        st.write("box_data")
        st.write(box_data)
    # box_data_2 = box_data.copy()
    datas = []
    for i, data in enumerate(box_data):
        name, row, col = data["name"], data["row"], data["col"]
        for j, pick in enumerate(data["picks"]):
            p_data = pick.copy()
            p_data.update(dict(name=name, row=row, col=col, box=i, pos=j))
            datas.append(p_data)
    
    df_sheet = pd.DataFrame(datas)
    if debug:
        st.write("datas")
        st.write(datas)
        display_df(df_sheet, "df_sheet")
    
    if not df_sheet.empty:
        df_sheet["conf"] = df_sheet["name"].apply(lambda n: "E" if set({"east", "atlantic", "metro", "metropolitan"}).intersection(set(n.lower().split(" "))) else "W")
        df_sheet["type"] = df_sheet["name"].apply(lambda n: "D" if "def" in n.lower() else ("T" if "seed" in n.lower() else "F"))
    if debug:
        display_df(df_sheet, "df_sheet")
    return df_sheet


def show_sheet(path: str, year: int, final: bool=True, style: Literal["radio", "selectbox", "counts", "results_best", "results_worst", "input"] = "radio"):
    
    if style in ["counts", "results_best", "results_worst"]:
        st.error(f"{style=} not supported yet")
        return
    
    radios: bool = style == "radio"
    num_type: bool = style in ["counts", "results_best", "results_worst", "input"]
    
    with st.container(border=True):
        df_sheet = read_pool_sheet(path)
        n_cols = 4
        n_boxes = df_sheet["box"].max() + 1
        selectboxes = []
        box_nums = {}
        
        def sb_key(i):
            return f"key_selectbox_poolbox_{i}"
        
        def sbi_key(i, j):
            return f"{sb_key(i)}_{j}"
        
        def name_fmt(pick_name, team, ppg):
            return f"{pick_name} ({team}): {ppg}"
        
        def sb_options(i):
            df_box = df_sheet[df_sheet["box"] == i].reset_index()
            return [""] + df_box.apply(lambda r: name_fmt(r["pick"], r["team"], r["ppg"]), axis=1).values.tolist()
        
        cols_menu = st.columns([0.15, 0.85])
        
        with cols_menu[0]:
            if st.button("Clear", key="key_poolsheet_btn_clear"):
                for i in range(n_boxes):
                    st.session_state.update({sb_key(i): None})
            if st.button("Clear East", key="key_poolsheet_btn_clear_east"):
                for i in range(n_boxes):
                    df_box = df_sheet[(df_sheet["conf"] == "E") & (df_sheet["box"] == i)]
                    if not df_box.empty:
                        st.session_state.update({sb_key(i): None})
            if st.button("Clear West", key="key_poolsheet_btn_clear_west"):
                for i in range(n_boxes):
                    df_box = df_sheet[(df_sheet["conf"] == "W") & (df_sheet["box"] == i)]
                    if not df_box.empty:
                        st.session_state.update({sb_key(i): None})
            if st.button("Clear Forwards", key="key_poolsheet_btn_clear_forwards"):
                for i in range(n_boxes):
                    df_box = df_sheet[(df_sheet["type"] == "F") & (df_sheet["box"] == i)]
                    if not df_box.empty:
                        st.session_state.update({sb_key(i): None})
            if st.button("Clear Defence", key="key_poolsheet_btn_clear_defence"):
                for i in range(n_boxes):
                    df_box = df_sheet[(df_sheet["type"] == "D") & (df_sheet["box"] == i)]
                    if not df_box.empty:
                        st.session_state.update({sb_key(i): None})
            if st.button("Clear Teams", key="key_poolsheet_btn_clear_teams"):
                for i in range(n_boxes):
                    df_box = df_sheet[(df_sheet["type"] == "T") & (df_sheet["box"] == i)]
                    if not df_box.empty:
                        st.session_state.update({sb_key(i): None})
            if st.button("Randomize", key="key_poolsheet_btn_randomize"):
                for i in range(n_boxes):
                    st.session_state.update({sb_key(i): random.choice(sb_options(i)[1:])})
            if st.button("Randomize East", key="key_poolsheet_btn_randomize_east"):
                for i in range(n_boxes):
                    df_box = df_sheet[(df_sheet["conf"] == "E") & (df_sheet["box"] == i)]
                    if not df_box.empty:
                        st.session_state.update({sb_key(i): random.choice(sb_options(i)[1:])})
            if st.button("Randomize West", key="key_poolsheet_btn_randomize_west"):
                for i in range(n_boxes):
                    df_box = df_sheet[(df_sheet["conf"] == "W") & (df_sheet["box"] == i)]
                    if not df_box.empty:
                        st.session_state.update({sb_key(i): random.choice(sb_options(i)[1:])})
            if st.button("Randomize Forwards", key="key_poolsheet_btn_randomize_forwards"):
                for i in range(n_boxes):
                    df_box = df_sheet[(df_sheet["type"] == "F") & (df_sheet["box"] == i)]
                    if not df_box.empty:
                        st.session_state.update({sb_key(i): random.choice(sb_options(i)[1:])})
            if st.button("Randomize Defence", key="key_poolsheet_btn_randomize_defence"):
                for i in range(n_boxes):
                    df_box = df_sheet[(df_sheet["type"] == "D") & (df_sheet["box"] == i)]
                    if not df_box.empty:
                        st.session_state.update({sb_key(i): random.choice(sb_options(i)[1:])})
            if st.button("Randomize Teams", key="key_poolsheet_btn_randomize_teams"):
                for i in range(n_boxes):
                    df_box = df_sheet[(df_sheet["type"] == "T") & (df_sheet["box"] == i)]
                    if not df_box.empty:
                        st.session_state.update({sb_key(i): random.choice(sb_options(i)[1:])})
            if st.button("Fill Remaining", key="key_poolsheet_btn_fill_remaining"):
                for i in range(n_boxes):
                    key = sb_key(i)
                    if not bool(st.session_state.get(key)):
                        st.session_state.update({key: random.choice(sb_options(i)[1:])})
            if st.button("Top PPG", key="key_poolsheet_btn_top_ppg"):
                for i in range(n_boxes):
                    key = sb_key(i)
                    df_box = df_sheet[df_sheet["box"] == i].reset_index()
                    df_box = df_box[~pd.isna(df_box["pick"])].sort_values("ppg", ascending=False)
                    pick, team, ppg = df_box.iloc[0][["pick", "team", "ppg"]].values
                    st.session_state.update({key: name_fmt(pick, team, ppg)})
            if st.button("Top PPG of Selected Teams", key="key_poolsheet_btn_top_ppg_sel_teams"):
                sel_box_nums = df_sheet[df_sheet["type"] == "T"]["box"].unique().tolist()
                sel_teams = [st.session_state.get(sb_key(i), "") for i in sel_box_nums]
                sel_teams = ["".join(("".join(s.split("(")[1]).split(":")[0]).removesuffix(")").lower() if s else "") for s in sel_teams]
                if not all(sel_teams):
                    st.warning(f"Choose a team from the 4 team selector boxes below, then hit save")
                # st.write("sel_box_nums")
                # st.write(sel_box_nums)
                # st.write("sel_teams")
                # st.write(sel_teams)                
                for i in range(n_boxes):
                    if i not in sel_box_nums:
                        key = sb_key(i)
                        df_box = df_sheet[df_sheet["box"] == i].reset_index()
                        df_box["sel_team"] = df_box["team"].apply(lambda t: 1 if t.lower() in sel_teams else 0)
                        df_box = df_box[~pd.isna(df_box["pick"])].sort_values(["sel_team", "ppg"], ascending=[False, False])
                        # display_df(df_box, f"df_box_{i=}")
                        pick, team, ppg = df_box.iloc[0][["pick", "team", "ppg"]].values
                        st.session_state.update({key: name_fmt(pick, team, ppg)})
            if style == "input":
                st.divider()            
                # if st.button("output", key="key_output_poolsheet", disabled=all(selectboxes)):
                if st.button("output", key="key_output_poolsheet"):
                    now = datetime.now()
                    f_name = f"poolsheet_{year}_{now:%Y%m%d%H%M%S}.json"
                    data = {"date": now}
                    # data.update({i: sb for i, sb in enumerate(selectboxes)})
                    data.update({i: [st.session_state.get(sbi_key(i, j)) for j, opt in enumerate(sb_options(i)[1:])] for i in range(n_boxes)})
                    data = jsonify(data, in_line=False)
                    st.write("data")
                    st.json(data)
                    with open(f_name, "w") as f:
                        json.dump(data, f)
        
        with cols_menu[1]:
            with st.form(border=False, key="key_poolsheet_form"):
                with st.container():
                    st.header(f"{year} Playoffs:")
                    st.caption("Final: " + (":white_check_mark:" if final else ":x:"))
                grid_conts = [st.container(horizontal=True) for i in range(n_boxes // n_cols)]
                for i in range(n_boxes):
                    df_box = df_sheet[df_sheet["box"] == i].reset_index()
                    name = df_box.loc[0, "name"]
                    options = sb_options(i)
                    key = sb_key(i)
                    with grid_conts[i // n_cols]:
                        with st.container(border=True):
                            valid = bool(st.session_state.get(key))
                            valid_lbl = ":white_check_mark:" if valid else ":x:"
                            if radios:
                                options = options[1:]
                                selectboxes.append(st.radio(label=f"{name} {valid_lbl}", options=options, key=key, index=None))
                            else:
                                if num_type:
                                    box_nums[i] = []
                                    for j, opt in enumerate(options[1:]):
                                        val = 0
                                        disabled = False
                                        box_nums[i].append(st.number_input(
                                            label=opt,
                                            min_value=0,
                                            max_value=50,
                                            value=val,
                                            disabled=disabled,
                                            key=sbi_key(i, j)
                                        ))
                                else:
                                    selectboxes.append(st.selectbox(label=f"{name} {valid_lbl}", options=options, key=key))
                        
                        
                st.write("box_nums")
                st.write(box_nums)
                if st.form_submit_button("submit", key="key_poolsheet_submit"):
                    valid = all(selectboxes)
                    st.write(f"Valid={valid}")
                                    
                # display_df(df_sheet)
    

def page_hockey_pool_test():
    sheet_paths = [[2023, "C:\\Users\\abrig\\Documents\\Coding_Practice\\Python\\Hockey pool\\2023\\boxpool-BWSPool2023 (2).pdf"]]
    st.write("sheet_paths")
    st.write(sheet_paths)
    df_combined = []
    for year, path in sheet_paths:
        df = read_pool_sheet(path, debug=year==2023)
        display_df(df, f"df_{year}")
        if not df.empty:
            df["year"] = year
            df_combined.append(df)
    
    df_combined = pd.concat(df_combined)
    display_df(df_combined, f"Combined")
            
    show_sheet(sheet_paths[0][1], 2023)
    
    
def page_hockey_pool():
    dfs: dict[str, pd.DataFrame] = load_hockey_pool_data()
    for k, df in dfs.items():
        display_df(df, title=k, show_shape="separate", border=True)
        
    df_people: pd.DataFrame = dfs["people"]
    df_pools: pd.DataFrame = dfs["pools"]
    df_years: pd.DataFrame = dfs["years"]
    
    
    sheet_paths = df_pools.groupby(["picksheet", "year", "final"]).agg("min").index.to_list()
    count_paths = df_pools.groupby(["pickCounts", "year", "final"]).agg("min").index.to_list()
    st.write("sheet_paths")
    st.write(sheet_paths)
    df_combined = []
    for path, year, final in sheet_paths:
        df = read_pool_sheet(path)
        # display_df(df, f"df_{year}")
        if not df.empty:
            df["year"] = year
            df_combined.append(df)
    
    df_combined = pd.concat(df_combined)
    display_df(df_combined, f"Combined")
    
    radio_pool_sheet_year = st.radio(
        label="Select a Pool Year:",
        options=df_years["year"].unique().tolist(),
        key="key_radio_pool_sheet_year",
        index=len(df_years["year"].unique()) - 1,
        horizontal=True
    )
    radio_pool_sheet_style = st.radio(
        label="Select a Pool Sheet Style:",
        options=["radio", "selectbox", "counts", "results_best", "results_worst", "input"],
        key="key_radio_pool_sheet_style",
        index=0,
        horizontal=True        
    )
    # st.write(*[sp for sp in sheet_paths if sp[1] == radio_pool_sheet_year][0])
    show_sheet(*[sp for sp in sheet_paths if sp[1] == radio_pool_sheet_year][0], style=radio_pool_sheet_style)
    
    
    hp_html = """
        <iframe marginheight="0" marginwidth="0"
            style="border: none;" frameborder="0"
            src="https://www.officepools.com/nhl/classic/auth/2025/playoff/MMPlayoffs2026/hockey"
            width="500" 
            height="500"
        ></iframe>
    """
    
    st.markdown(hp_html, unsafe_allow_html=True)
    
    
    
    
    df_people["norm"] = df_people["name"].apply(lambda n: no_specials(n, strict=True))
        
    cols_pool_results = st.columns(len(df_pools))
    
    lst_df_pool_e = []
    
    for i, row in df_pools.iterrows():
        with cols_pool_results[i]:
            year = row["year"]
            fee = row["fee"]
            pct_prize = row["pctPrize"]
            standings = row["standings"]
            final = row["final"]
            n_people = len(standings)
            total_fees = fee * pct_prize * n_people
            prizes = [total_fees * 0.5, total_fees * 0.35, total_fees * 0.15]
            
            st.header(f"{year} playoffs - {'FINAL' if final else 'ONGOING'}")
            for i, people_id in enumerate(standings):
                df_pool_people = df_people[df_people["id"] == people_id].reset_index()
                name = df_pool_people.loc[0, "name"]
                alias = df_pool_people.iloc[0].get("alias")
                if " " in name.strip():
                    name_a = name.split(" ")
                    name_a = f"{name_a[0].title()} {name_a[1][0].upper()}"
                else:
                    name_a = name
                alias = name_a if pd.isna(alias) else alias
                winnings = prizes[i] if i < len(prizes) else 0
                winnings = winnings if final else 0
                if winnings:
                    st.write(f"{i + 1} - prize: $ {winnings:,.2f} - {alias}")
                else:
                    st.write(f"{i + 1} - {alias}")
                norm = no_specials(name, strict=True)
                lst_df_pool_e.append(pd.DataFrame([{
                    "year": year,
                    "fee": fee,
                    "pctPrize": pct_prize,
                    "totalPrizes": total_fees,
                    "nPlayers": n_people,
                    "place": i + 1,
                    "winnings": winnings,
                    "person": people_id,
                    "norm": norm
                }]))
               
    df_pools_e = pd.concat(lst_df_pool_e, ignore_index=True)
    display_df(df_pools_e, "df_pools_e")
    
    df_people_e = df_people.copy()
    df_people_e["best"] = None
    df_people_e["worst"] = None
    df_people_e["sum"] = None
    df_people_e["inv"] = None
    df_people_e["mean"] = None
    df_people_e["lastYear"] = None
    df_people_e["totalPayed"] = 0
    df_people_e["timesPlayed"] = 0
    df_people_e["totalWinnings"] = 0
    for i, row in df_people.iterrows():
        # people_id = row["id"]
        # df_pools_person = df_pools_e[df_pools_e["person"] == people_id]
        people_norm = row["norm"]
        df_pools_person = df_pools_e[df_pools_e["norm"] == people_norm]
        df_people_e.loc[i, "best"] = df_pools_person["place"].min()
        df_people_e.loc[i, "worst"] = df_pools_person["place"].max()
        df_people_e.loc[i, "sum"] = df_pools_person["place"].sum()
        df_people_e.loc[i, "inv"] = df_pools_person["nPlayers"].sum() - df_pools_person["place"].sum()
        df_people_e.loc[i, "mean"] = df_pools_person["place"].mean()
        df_people_e.loc[i, "lastYear"] = df_pools_person["year"].max()
        df_people_e.loc[i, "totalPayed"] = df_pools_person["fee"].sum()
        df_people_e.loc[i, "timesPlayed"] = df_pools_person["place"].count()
        df_people_e.loc[i, "totalWinnings"] = df_pools_person["winnings"].sum()
        
    df_people_e["totalEarnings"] = df_people_e["totalWinnings"] - df_people_e["totalPayed"]
    df_people_e["earningsPerYear"] = df_people_e["totalEarnings"] / df_people_e["timesPlayed"]
    df_people_e["score"] = df_people_e["inv"] + (df_people_e["totalEarnings"] / 10)
    
    df_people_e["placementPct"] = 1 - ((df_people_e["mean"] - 1) / (df_people_e["timesPlayed"].replace(0, 1)))
    df_people_e["roi"] = df_people_e["totalWinnings"] / df_people_e["totalPayed"].replace(0, 1)

    # Final score (balanced)
    df_people_e["score"] = (
        df_people_e["placementPct"] * 0.6 +
        np.log1p(df_people_e["roi"]) * 0.4
    )
    
    total_players = df_people["id"].nunique()
    total_entries = len(df_pools_e)
    total_fees = df_pools_e["fee"].sum()
    total_winnings = df_pools_e["winnings"].sum()

    df_p_ret = df_pools_e.copy()
    df_p_ret["currID"] = df_p_ret["person"]
    display_df(df_p_ret, "df_p_ret A")
    df_p_ret["person"] = df_p_ret["person"].apply(lambda id_: no_specials(df_people[df_people["id"] == id_].reset_index().loc[0, "name"], strict=True).lower())
    display_df(df_people, "df_people")
    display_df(df_p_ret, "df_p_ret B")
    # df_p_ret["maxID"] = df_p_ret["person"].apply(lambda id_: df_people[df_people["id"] == id_, "id"].sort_values("id", ascending=False).reset_index().loc[0, "id"])
    df_p_ret["maxID"] = df_p_ret["person"].apply(lambda p: df_people[df_people["norm"].str.lower() == p.lower()]["id"].idxmax())
    # retention_rate = df_pools_e.groupby("person")["year"].nunique().mean() / df_pools["year"].nunique()
    display_df(df_p_ret, "df_p_ret FINAL")
    retention_rate = df_p_ret.groupby("person")["year"].nunique().mean() / df_pools["year"].nunique()
    

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Unique Players", total_players)
    col2.metric("Total Entries", total_entries)
    col3.metric("Total Fees Collected", f"${total_fees:,.2f}")
    col4.metric("Total Winnings Paid", f"${total_winnings:,.2f}")

    st.metric("Avg Retention Rate", f"{retention_rate:.2%}")
    
    best_player = df_people_e.sort_values("score", ascending=False).iloc[0]
    worst_player = df_people_e.sort_values("score", ascending=True).iloc[0]

    st.subheader("🏆 Best Performer")
    st.write(best_player[["name", "score", "totalEarnings", "mean"]])

    st.subheader("💀 Worst Performer")
    st.write(worst_player[["name", "score", "totalEarnings", "mean"]])
    
    df_prize_dist = df_pools_e[df_pools_e["winnings"] > 0]

    fig = px.pie(
        df_prize_dist,
        names="place",
        values="winnings",
        title="Prize Distribution by Placement"
    )

    st.plotly_chart(fig, use_container_width=True)
    
    df_top = df_people_e.sort_values("totalWinnings", ascending=False).head(15)

    fig_bar_winnings = px.bar(
        df_top,
        x="name",
        y="totalWinnings",
        title="Top Earners",
        text_auto=True
    )

    # st.plotly_chart(fig, use_container_width=True)
    
    fig_roi = px.bar(
        df_top,
        x="name",
        y="roi",
        title="ROI by Player"
    )

    # st.plotly_chart(fig, use_container_width=True)
    
    fig_scatter = px.scatter(
        df_people_e,
        x="placementPct",
        y="totalEarnings",
        size="timesPlayed",
        hover_name="name",
        title="Skill vs Profit (Bubble Size = Participation)"
    )

    # st.plotly_chart(fig, use_container_width=True)
    
    fig_hist = px.histogram(
        df_pools_e,
        x="place",
        nbins=20,
        title="Distribution of Placements"
    )

    # st.plotly_chart(fig, use_container_width=True)
    
    df_retention = df_pools_e.groupby("year")["person"].nunique().reset_index()

    fig_retention = px.line(
        df_retention,
        x="year",
        y="person",
        title="Players Per Year"
    )

    # st.plotly_chart(fig, use_container_width=True)
    
    df_people_e["wins"] = df_pools_e[df_pools_e["place"] == 1].groupby("person").size()
    df_people_e["wins"] = df_people_e["wins"].fillna(0)

    df_people_e["winRate"] = df_people_e["wins"] / df_people_e["timesPlayed"]
    
    df_people_e["podiums"] = df_pools_e[df_pools_e["place"] <= 3].groupby("person").size()
    df_people_e["podiums"] = df_people_e["podiums"].fillna(0)

    df_people_e["podiumRate"] = df_people_e["podiums"] / df_people_e["timesPlayed"]
    
    st.title("🏒 Hockey Pool Analytics Dashboard")
    
    # df_people_e.sort_values(["totalEarnings", "timesPlayed", "mean"], ascending=[False, False, True], inplace=True)
    df_people_e.sort_values(["score"], ascending=[False], inplace=True)
    display_df(df_people_e, "df_people_e")

    # KPIs
    # (metrics row)

    # Row 1
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_bar_winnings)
    with col2:
        st.plotly_chart(fig_roi)

    # Row 2
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_scatter)
    with col2:
        st.plotly_chart(fig_hist)

    # Row 3
    st.plotly_chart(fig_retention)
    
    curr_year = int(df_years["year"].max())
    last_year = int(df_years["year"].values.tolist()[-2])
    
    df_current = df_people_e[df_people_e["lastYear"] == curr_year]
    df_core = df_people_e[df_people_e["timesPlayed"] == len(df_years)]
    df_sub_core = df_people_e[df_people_e["timesPlayed"] == (len(df_years) - 1)]
    df_core_twice = df_people_e[df_people_e["timesPlayed"] == 2]
    df_core_once = df_people_e[df_people_e["timesPlayed"] == 1]
    df_new = df_current.loc[df_current.index.intersection(df_core_once.index)]
    df_recent_exits = df_people_e[df_people_e["lastYear"] == last_year]
    # df_recent_exits = df_recent_exits.loc[~df_current.index.intersection(df_recent_exits.index)]
    
    for df, title in [
        (df_current, f"This year's pool players for {curr_year} playoffs"),
        (df_new, f"New pool players for {curr_year} playoffs"),
        (df_recent_exits, f"Players that did not return from {last_year} playoffs"),
        (df_core, f"Core pool players for {len(df_years)} seasons"),
        (df_sub_core, f"Core pool players for all but 1 season"),
        (df_core_twice, f"Players who have played two seasons only"),
        (df_core_once, f"Players who have played only one season")
    ]:
        display_df(df, title, show_shape="below", border=True)
        


# ─────────────────────────────────────────────────────────
# MAIN APP
# ─────────────────────────────────────────────────────────
def main():
    # Header
    st.markdown("""
    <div class="nhl-header">
        <h1>🏒 NHL PREDICTION DASHBOARD</h1>
        <p>Analyze your game prediction performance across teams, divisions, conferences, and scheduling patterns</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Sidebar ─────────────────────────────────────────
    with st.sidebar:
        st.markdown("### 🗂️ Navigation")
        page = st.radio("", [
            "⚡ Scores",
            "📊 Overview & Accuracy",
            "👥 By Team",
            "🗓️ Trends Over Time",
            "🌍 Travel & Gauntlets",
            "🔮 Future Predictions",
            "🏆 Clinching Scenarios",
            "🧥 Jersey Collection",
            "Stanley Cup",
            "Explore API",
            "Hockey Pool",
        ], label_visibility="collapsed")
        st.markdown("---")
        st.caption(f"📂 `{path_excel_predictions.split(chr(92))[-1]}`")
        
        if st.button(
            "Update predictions copy"
        ):
            path_predictions_2526 = r"C:\Users\abrig\Documents\Coding_Practice\Python\Jerseys\NHLGamePredictions2526.xlsx"
            if os.path.exists(path_predictions_2526):
                try:
                    df_new = pd.read_excel(path_predictions_2526, skiprows=1)
                    df_new.to_excel(path_excel_predictions, index=False)
                    load_data.clear()
                except PermissionError:
                    print("Excel file is currently open.")

    # Load data
    # try:
    df = load_data(path_excel_predictions)
    # # except FileNotFoundError:
    #     # st.error(f"❌ Workbook not found:\n\n`{path_excel_predictions}`\n\nCheck the path at the top of the script.")
    #     # return
    # # except Exception as e:
    #     # st.error(f"❌ Could not load workbook: {e}")
    #     # return
    
    # # DataFrames to show days canadian teams play, and when all have a chance of winning.
    # display_df(df)
    # df_cad_games_1_team = df[
    #     (
    #         (df["HomeTeam"].isin(CANADIAN_TEAMS))
    #         & (~df["AwayTeam"].isin(CANADIAN_TEAMS))
    #     )
    #     | (
    #         (df["AwayTeam"].isin(CANADIAN_TEAMS))
    #         & (~df["HomeTeam"].isin(CANADIAN_TEAMS))
    #     )
    # ]
    # df_cad_games_2_team = df[
    #     (
    #         (df["HomeTeam"].isin(CANADIAN_TEAMS))
    #         & (df["AwayTeam"].isin(CANADIAN_TEAMS))
    #     )
    # ]
    # df_cad_games_either_team = df[
    #     (
    #         (df["HomeTeam"].isin(CANADIAN_TEAMS))
    #         | (df["AwayTeam"].isin(CANADIAN_TEAMS))
    #     )
    # ]
    # display_df(
    #     df_cad_games_1_team,
    #     "df_cad_games_1_team"
    # )
    # display_df(
    #     df_cad_games_2_team,
    #     "df_cad_games_2_team"
    # )
    # display_df(
    #     df_cad_games_either_team,
    #     "df_cad_games_either_team"
    # )
    # df_grouped = df_cad_games_1_team.groupby(
    #     by=["GameDate"]
    # ).agg("count")
    # df_grouped = df_grouped[df_grouped["PredictionDate"] >= 6]
    # display_df(
    #     df_grouped
    # )

    completed = df[df["GameIsOver"] == True].copy()
    future    = df[df["GameIsOver"] == False].copy()
    teams     = sorted(list(set(completed["AwayTeam"].dropna().unique().tolist() + completed["HomeTeam"].dropna().unique().tolist() + future["AwayTeam"].dropna().unique().tolist() + future["HomeTeam"].dropna().unique().tolist())))

    total      = len(completed)
    n_correct  = completed["CorrectWinnerPrediction"].sum()
    accuracy   = n_correct / total * 100 if total > 0 else 0
    
    if page == "Explore API":
        
        
        stats_base_a = "https://api.nhle.com/stats/rest/en"

        url_goalie_summary_a = (
            f'{stats_base_a}/goalie/summary'
            f'?isAggregate=false'
            f'&isGame=false'
            f'&start=0'
            f'&limit=50'
            f'&sort=[{{"property":"wins","direction":"DESC"}}]'
            f'&cayenneExp=seasonId=20252026 and gameTypeId=2'
        )
        st.write("url_goalie_summary_a")
        st.write(url_goalie_summary_a)

        url_skater_summary_a = (
            f'{stats_base_a}/skater/summary'
            f'?isAggregate=false'
            f'&isGame=false'
            f'&start=0'
            f'&limit=50'
            f'&sort=[{{"property":"wins","direction":"DESC"}}]'
            f'&cayenneExp=seasonId=20252026 and gameTypeId=2'
        )
        st.write("url_skater_summary_a")
        st.write(url_skater_summary_a)
        
        df_jerseys = load_jersey_workbook()
        
        if not df_jerseys.empty:
            
            lst_player_ids = df_jerseys["NHLID"].dropna().unique().tolist()
            if 0 in lst_player_ids:
                lst_player_ids.remove(0)
            lst_player_ids.sort()
            
            # playerID = data["playerID"]
            # teamAbbr = data["teamAbbr"]
            # date = data["date"]
            # season = data["season"]
            # gameType = data["gameType"]
            # gameID = data["gameID"]
            # draftYear = data["draftYear"]
            
            k_selectbox_player_id = "key_selectbox_player_id"
            st.session_state.setdefault(k_selectbox_player_id, 8471675)  # Sidney Crosby
            selectbox_player_id = st.selectbox(
                label="Player ID",
                options=lst_player_ids,
                key=k_selectbox_player_id,
                help="PlayerIDs list is sourced from Jersey Collection spreadsheet"
            )
            
            k_datepicker_date = "key_datepicker_date"
            st.session_state.setdefault(k_datepicker_date, datetime.now().date())  # Today
            datepicker_date = st.date_input(
                label="Date",
                key=k_datepicker_date
            )
            
            start_year = 1900
            lst_seasons = [f"{start_year+i}{start_year+i+1}" for i in range(2026-start_year)]
            lst_seasons.sort(reverse=True)
            k_selectbox_season = "key_selectbox_season"
            st.session_state.setdefault(k_selectbox_season, lst_seasons[0])  # Current season
            selectbox_season = st.selectbox(
                label="Season",
                options=lst_seasons,
                key=k_selectbox_season,
                help="Season of play. Seasons start in the Fall and end in Spring / Summer, spanning ~250 days over 2 calendar years."
            )
            
            lst_team_abbrs = list(TEAM_META.keys())
            k_selectbox_team = "key_selectbox_team"
            st.session_state.setdefault(k_selectbox_team, "PIT")  # Sidney Crosby's team
            lst_team_abbrs.sort()
            selectbox_team = st.selectbox(
                label="Team",
                options=lst_team_abbrs,
                key=k_selectbox_team
            )
            
            params = {
                "playerID": selectbox_player_id,
                "date": datepicker_date,
                "season": selectbox_season,
                "teamAbbr": selectbox_team,
            }
            
            df_contents_og = api_ref.contents(**params)
            df_contents = df_contents_og.copy()
            df_contents[["url", "key_order"]] = df_contents.apply(
                lambda r:
                    pd.Series([
                        r["url"].format(**r["data"]),
                        [{v: k_ for k_, v in r["data"].items()}[k] for k in r["order"]]
                    ])
                , axis=1
            )
            df_contents.drop(columns=["order", "data"], inplace=True)
            
            lst_sections = df_contents["section"].dropna().unique().tolist()
            lst_sections.sort()
            k_multiselect_sections = "key_multiselect_sections"
            st.session_state.setdefault(k_multiselect_sections, lst_sections)  # All
            selectbox_player_id = st.multiselect(
                label="Sections:",
                options=lst_sections,
                key=k_multiselect_sections
            )
            
            df_contents = df_contents[df_contents["section"].isin(selectbox_player_id)]
            
            k_sel_url = "key_sel_url"
            stdf_contents = st.dataframe(
                df_contents,
                selection_mode="single-row",
                on_select="rerun"
            )
            
            if not stdf_contents:
                stdf_contents = st.session_state.get(k_sel_url)
            
            if stdf_contents:
                df_sel_contents: pd.DataFrame = df_contents.iloc[stdf_contents.get("selection", {}).get("rows", [])]
                if not df_sel_contents.empty:
                    ser_sel_contents = df_sel_contents.reset_index().iloc[0]
                    sel_url = ser_sel_contents["url"]
                    section = ser_sel_contents["section"]
                    description = ser_sel_contents["description"]
                    is_image = str(sel_url).lower().strip().endswith(".png")
                    st.session_state.update({k_sel_url: stdf_contents})
                    result = None
                    cont_info = st.container(horizontal=True)
                    cols_info = st.columns(2)
                    try:
                        if not is_image:
                            result = requests.get(sel_url)
                            if result.status_code == 200:
                                result = result.json()
                            else:
                                st.write(f":red[Invalid HTML status code] {result.status_code=}")
                        else:
                            result = None
                        with cont_info:
                            # st.write(ser_sel_contents["section"])
                            # st.write(ser_sel_contents["description"])
                            st.metric(
                                ser_sel_contents["section"],
                                ser_sel_contents["description"]
                            )
                            st.link_button(label=sel_url, url=sel_url)
                            with st.container():
                                st.write("raw")
                                st.code(sel_url)
                            
                            proxy_prefix = "https://corsproxy.io/?url="
                            replace_chars = {
                                ":": "%3A",
                                "/": "%2F",
                                "?": "%3F",
                                "=": "%3D",
                                ",": "%2C",
                                "&": "%26",
                            }
                            sel_url_cors = f"{sel_url}"
                            for c, v in replace_chars.items():
                                sel_url_cors = sel_url_cors.replace(c, v)
                            sel_url_cors = f"{proxy_prefix}{sel_url_cors}"
                            with st.container():
                                st.write(f"cors")
                                st.code(sel_url_cors)
                        if not is_image:
                            with cols_info[1]:
                                k_checkbox_expand_actual = "key_checkbox_expand_actual"
                                checkbox_expand_actual = st.checkbox(
                                    "expand?",
                                    key=k_checkbox_expand_actual,
                                    value=False
                                )
                                st.subheader(f"Actual ({len(str(result))} characters)")
                                st.json(result, expanded=checkbox_expand_actual)
                    except Exception as e:
                        st.error(e)
                        raise e
                    with cols_info[0]:
                        st.write(df_contents_og[(df_contents_og["section"] == section) & (df_contents_og["description"] == description)].iloc[0])
                        if is_image:
                            st.image(sel_url, caption=sel_url)
                        else:
                            if result:
                                k_checkbox_expand_sampled = "key_checkbox_expand_sampled"
                                checkbox_expand_sampled = st.checkbox(
                                    "expand?",
                                    key=k_checkbox_expand_sampled,
                                    value=False
                                )
                                peek_results = peek_json(result)
                                st.subheader(f"Sampled ({len(str(peek_results))} characters)")
                                st.json(peek_results, expanded=checkbox_expand_sampled)
            
    # ── PAGE: Stanley Cup ───────────────────────────────────
    elif page == "Stanley Cup":
        
        datas = load_stanley_cup_jsons()
        data_appearances = datas["appearances"].copy()
        data_wins = datas["wins"].copy()
        data_losses = datas["losses"].copy()
        
        entities = data_appearances.pop("ENTITIES", {})

        rows = []
        first_season = list(data_appearances)[0]
        teams = list(data_appearances[first_season])
        data_appearances[int(first_season) - 1] = {t: 0 for t in teams}
        data_wins[int(first_season) - 1] = {t: 0 for t in teams}
        data_losses[int(first_season) - 1] = {t: 0 for t in teams}
        
        for season, season_data_a in data_appearances.items():
            season_data_w = data_wins[season]
            season_data_l = data_losses[season]
            for team, total in season_data_a.items():
                season_data_w_t = season_data_w[team]
                season_data_l_t = season_data_l[team]
                rows.append({
                    "Season": int(season),
                    "Team": team,
                    "Appearances": total,
                    "Wins": season_data_w_t,
                    "Losses": season_data_l_t
                })

        df = pd.DataFrame(rows)
        df.sort_values(by=["Season", "Team"], inplace=True)

        # Optional historical name cleanup
        df["Team"] = df["Team"].replace({
            "Chicago Black Hawks": "Chicago Blackhawks",
            "Mighty Ducks of Anaheim": "Anaheim Ducks",
        })

        # User choice of metric to animate
        metric = st.radio(
            "Animate by:",
            ["Appearances", "Wins", "Losses"],
            horizontal=True,
            index=0
        )

        top_n = st.slider("Top teams to display", 5, 20, 12)

        # Build label text for bars
        df["BarText"] = df.apply(
            lambda r: f"{r[metric]}  (W:{r['Wins']} L:{r['Losses']})",
            axis=1
        )

        # Keep top N teams per season based on chosen metric
        df_plot = (
            df.sort_values(["Season", metric], ascending=[True, False])
            .groupby("Season", group_keys=False)
            .head(top_n)
            .copy()
        )

        color_map = {
            team: meta.get("colour", "#888888")
            for team, meta in entities.items()
            if isinstance(meta, dict)
        }

        title_map = {
            "Appearances": "Stanley Cup Final Appearances by Team Over Time",
            "Wins": "Stanley Cup Wins by Team Over Time",
            "Losses": "Stanley Cup Final Losses by Team Over Time"
        }

        fig = px.bar(
            df_plot,
            x=metric,
            y="Team",
            animation_frame="Season",
            orientation="h",
            color="Team",
            color_discrete_map=color_map,
            text="BarText",
            range_x=[0, df[metric].max() + 1],
            title=title_map[metric],
            hover_data={
                "Appearances": True,
                "Wins": True,
                "Losses": True,
                "BarText": False
            }
        )

        fig.update_layout(
            height=700,
            showlegend=False,
            yaxis=dict(categoryorder="total ascending")
        )

        fig.update_traces(
            textposition="outside",
            cliponaxis=False,
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Season: %{frame}<br>"
                f"{metric}: %{{x}}<br>"
                "Wins: %{customdata[1]}<br>"
                "Losses: %{customdata[2]}<extra></extra>"
            )
        )
        
        logo_uri_map = {
            team: img_to_uri(meta.get("image_path", ""), meta.get("abbr", ""))
            for team, meta in entities.items()
            if isinstance(meta, dict)
        }
        
        for frame in fig.frames:
            season = int(frame.name)
            frame_df = (
                df_plot[df_plot["Season"] == season]
                .sort_values(metric, ascending=False)
                .head(top_n)
                .copy()
            )

            images = []
            for _, row in frame_df.iterrows():
                team = row["Team"]
                logo_uri = logo_uri_map.get(team)

                if not logo_uri:
                    continue

                images.append(dict(
                    source=logo_uri,
                    xref="x",
                    yref="y",
                    x=row[metric],
                    y=team,
                    sizex=max(df[metric].max() * 0.03, 0.6),
                    sizey=0.8,
                    xanchor="left",
                    yanchor="middle",
                    sizing="contain",
                    layer="above",
                    opacity=1
                ))

            frame.layout = dict(images=images)
        
        initial_season = df_plot["Season"].min()
        initial_df = (
            df_plot[df_plot["Season"] == initial_season]
            .sort_values(metric, ascending=False)
            .head(top_n)
            .copy()
        )

        fig.update_layout(
            images=[
                dict(
                    source=logo_uri_map[row["Team"]],
                    xref="x",
                    yref="y",
                    x=row[metric],
                    y=row["Team"],
                    sizex=max(df[metric].max() * 0.03, 0.6),
                    sizey=0.8,
                    xanchor="left",
                    yanchor="middle",
                    sizing="contain",
                    layer="above",
                    opacity=1
                )
                for _, row in initial_df.iterrows()
                if logo_uri_map.get(row["Team"])
            ]
        )

        st.plotly_chart(fig, use_container_width=True)
    
    # ── PAGE: Scores ───────────────────────────────────
    elif page == "⚡ Scores":
        st.markdown('<div class="section-header">Scores</div>', unsafe_allow_html=True)
        # index_html = load_index_html()
        # st.code(index_html, language="html", line_numbers=True)
        # st.markdown(index_html, unsafe_allow_html=True)
        # st.html("index.html")
        index_html = load_index_html()
        components.html(
            index_html,
            height=2400,
            scrolling=True,
        )
        st.subheader(f"Coming soon")
        if st.button(
            "Verify My Records?"
        ):
            game_ids = completed["GameID"].tolist()
            st.write(game_ids)
            to_reconcile = verify_scores(completed)
            st.write(to_reconcile)

    # ── PAGE: OVERVIEW ───────────────────────────────────
    elif page == "📊 Overview & Accuracy":
        st.markdown('<div class="section-header">OVERALL PERFORMANCE</div>', unsafe_allow_html=True)

        c1, c2, c3, c4, c5 = st.columns(5)
        with c1:
            st.metric("Total Games", f"{total}")
        with c2:
            st.metric("Correct", f"{int(n_correct)}")
        with c3:
            st.metric("Incorrect", f"{int(total - n_correct)}")
        with c4:
            st.metric("Win Rate", f"{accuracy:.1f}%")
        with c5:
            avg_score = completed["EnhancedScore"].mean() if "EnhancedScore" in completed.columns else completed["GamePredictionScore"].mean()
            st.metric("Avg Enhanced Score", f"{avg_score:.3f}" if not pd.isna(avg_score) else "N/A",
                      help="v3 heuristic: Winner(0.50) + ResultType(0.10) + MarginError(0.15) + ScoreError(0.15) + OT/SO credit(0.10)")

        # Score comparison section
        if "EnhancedScore" in completed.columns and "GamePredictionScore" in completed.columns:
            with st.expander("📐 Scoring System Comparison — GPS v1 vs v2 vs Enhanced v3", expanded=False):
                sc_cols = st.columns(3)
                gps1_avg = completed["GamePredictionScore"].mean()
                gps2_avg = completed["GamePredictionScore2"].mean() if "GamePredictionScore2" in completed.columns else None
                gps3_avg = completed["EnhancedScore"].mean()
                sc_cols[0].metric("GPS v1 Mean", f"{gps1_avg:.3f}", help="0.8×winner + 0.1×awayScore + 0.1×homeScore")
                if gps2_avg is not None:
                    sc_cols[1].metric("GPS v2 Mean", f"{gps2_avg:.3f}", help="v1 + OT/SO partial credit (0.85/0.95)")
                sc_cols[2].metric("Enhanced v3 Mean", f"{gps3_avg:.3f}", help="Winner(0.55) + ResultType(0.10) + MarginErr(0.175) + ScoreErr(0.175) + OT/SO bonus(≤0.10). Perfect = 1.00")

                score_compare_df = completed[["GameDate","AwayTeam","HomeTeam",
                    "CorrectWinnerPrediction","ActualResult","PredictedResult",
                    "GamePredictionScore","GamePredictionScore2","EnhancedScore"]].copy() \
                    if "GamePredictionScore2" in completed.columns \
                    else completed[["GameDate","AwayTeam","HomeTeam",
                    "CorrectWinnerPrediction","ActualResult","PredictedResult",
                    "GamePredictionScore","EnhancedScore"]].copy()
                score_compare_df["GameDate"] = score_compare_df["GameDate"].dt.strftime("%b %d")

                # Distribution comparison chart
                fig_sc = go.Figure()
                fig_sc.add_trace(go.Histogram(
                    x=completed["GamePredictionScore"], name="GPS v1",
                    opacity=0.65, marker_color=ICE_BLUE, nbinsx=20
                ))
                if "GamePredictionScore2" in completed.columns:
                    fig_sc.add_trace(go.Histogram(
                        x=completed["GamePredictionScore2"], name="GPS v2",
                        opacity=0.65, marker_color="#f39c12", nbinsx=20
                    ))
                fig_sc.add_trace(go.Histogram(
                    x=completed["EnhancedScore"], name="Enhanced v3",
                    opacity=0.65, marker_color=GREEN, nbinsx=20
                ))
                fig_sc.update_layout(
                    **DARK_THEME, barmode="overlay",
                    title="Score Distribution Comparison",
                    xaxis_title="Score (0–1.0)", yaxis_title="Games",
                    height=300,
                    legend=dict(orientation="h", yanchor="bottom", y=1.02)
                )
                st.plotly_chart(fig_sc, use_container_width=True)
                st.dataframe(score_compare_df.sort_values("GameDate", ascending=False), use_container_width=True)

        col_pie, col_info = st.columns([1, 2])
        with col_pie:
            st.plotly_chart(correct_incorrect_pie(int(n_correct), total), use_container_width=True)
        with col_info:
            st.markdown('<div class="section-header" style="font-size:1.1rem">QUICK FACTS</div>', unsafe_allow_html=True)
            if "WatchedGame" in completed.columns:
                watched = completed["WatchedGame"].sum()
                st.metric("Games Watched", f"{int(watched)} / {total}")
            if "GameHasShutOut" in completed.columns:
                shutouts = completed["GameHasShutOut"].sum()
                st.metric("Shutouts in Dataset", f"{int(shutouts)}")
            if "ActualResult" in completed.columns:
                ots = completed[completed["ActualResult"].isin(["OT", "SO"])].shape[0]
                st.metric("OT/SO Games", f"{int(ots)}")

        st.markdown('<div class="section-header">ACCURACY BY GROUPING</div>', unsafe_allow_html=True)

        grouping_options = {
            "Conference": "AwayConf",
            "Division (Away Team)": "AwayDiv",
            "Division (Home Team)": "HomeDiv",
            "Day of Week": "DayOfWeek",
            "Month": "Month",
            "Home Team": "HomeTeam",
            "Away Team": "AwayTeam",
            "Actual Result Type": "ActualResult",
        }

        col_g1, col_g2 = st.columns(2)
        with col_g1:
            g1 = st.selectbox("Group by (Chart 1)", list(grouping_options.keys()), index=0)
            fig, tbl = accuracy_bar(grouping_options[g1], g1, completed)
            st.plotly_chart(fig, use_container_width=True)
            with st.expander("View data table"):
                st.dataframe(tbl.sort_values("Accuracy", ascending=False), use_container_width=True)
        with col_g2:
            g2 = st.selectbox("Group by (Chart 2)", list(grouping_options.keys()), index=2)
            fig2, tbl2 = accuracy_bar(grouping_options[g2], g2, completed)
            st.plotly_chart(fig2, use_container_width=True)
            with st.expander("View data table"):
                st.dataframe(tbl2.sort_values("Accuracy", ascending=False), use_container_width=True)
        
        # Stacked comparison
        st.markdown('<div class="section-header">SIDE-BY-SIDE COMPARISON</div>', unsafe_allow_html=True)
        cmp_col = st.selectbox("Compare by", list(grouping_options.keys()), index=6)
        fig_cmp = compare_two_groups(completed, grouping_options[cmp_col], cmp_col)
        st.plotly_chart(fig_cmp, use_container_width=True)

        # Back-to-back accuracy
        st.markdown('<div class="section-header">BACK-TO-BACK PERFORMANCE</div>', unsafe_allow_html=True)
        b2b_df = completed.copy()
        b2b_df["Situation"] = "Standard"
        b2b_df.loc[b2b_df["AwayB2B"], "Situation"] = "Away B2B"
        b2b_df.loc[b2b_df["HomeB2B"], "Situation"] = "Home B2B"
        b2b_df.loc[b2b_df["AwayB2B"] & b2b_df["HomeB2B"], "Situation"] = "Both B2B"

        fig_b2b, _ = accuracy_bar("Situation", "Back-to-Back Situation", b2b_df)
        st.plotly_chart(fig_b2b, use_container_width=True)
        
        teams = df["AwayTeam"].dropna().unique().tolist()
        df_w = completed.copy()
        df_w["Teams"] = df_w.apply(lambda row: [row["AwayTeam"], row["HomeTeam"]], axis=1)
        df_w["HasExtraTime"] = df_w["ActualResult"].apply(lambda ar: ar in ["OT", "SO"])
        df_w = df_w[[
            "GameID",
            "Teams",
            "AwayTeam",
            "HomeTeam",
            "AwayWon",
            "HomeWon_",
            "HasExtraTime"
        ]]
        df_w.rename(
            columns={
                "HomeWon_": "HomeWon"
            },
            inplace=True
        )
        
        df_w["A_ETL"] = df_w.apply(lambda r: r["HomeWon"] and r["HasExtraTime"], axis=1)
        df_w["H_ETL"] = df_w.apply(lambda r: r["AwayWon"] and r["HasExtraTime"], axis=1)
        
        if st.toggle("Filter using test games?", value=False):
            # df_w = df_w[df_w["Teams"] == "CHI"]
            
            # def validate_matchups(*args):
            #     st.write(f"validate_matchups {args=}")
            #     df = de_matchups.copy()
            #     display_df(df, "a")
            #     df = st.session_state.get(k_df_matchups, pd.DataFrame()).copy()
            #     display_df(df, "b")
            #     de_data = st.session_state.get(k_stde_matchups, {})
            #     display_df(de_data, "c")
                
            #     edited_rows = de_data.get("edited_rows", {})
            #     added_rows = de_data.get("added_rows", [])
            #     deleted_rows = de_data.get("deleted_rows", [])
                
            #     team_count = {}
            #     for i, row in enumerate(added_rows):
            #         team1 = row.get("Team1")
            #         team2 = row.get("Team2")
            #         if team1 is not None:
            #             team_count.setdefault(team1, 0)
            #         if team2 is not None:
            #             team_count.setdefault(team2, 0)
            #         if (team1 is None) and (team2 is None):
            #             # bad
            #         elif team1 == team2:
            #             # bad
                    
            #         team_count[team1] += 1
            #         team_count[team2] += 1
            #         if team_count1[team1] > 1:             
            
            radio_and_or = st.radio("And / Or", options=["And", "Or"], index=1)
            
            k_df_matchups = "key_df_matchups"
            k_stde_matchups = "key_stde_matchups"
            df_matchups: pd.DataFrame = st.session_state.setdefault(
                k_df_matchups,
                pd.DataFrame({
                    "Team1": ["ANA", "ANA", "ANA", "ANA", "ANA", "NJD"],
                    "Team2": ["CGY", "UTA", "EDM", "LAK", "NSH", "MTL"]
                }))
            de_matchups = st.data_editor(
                df_matchups,
                column_config = {
                    "Team1": st.column_config.SelectboxColumn(
                        "Team1",
                        options=teams
                    ),
                    "Team2": st.column_config.SelectboxColumn(
                        "Team2",
                        options=teams
                    )
                },
                # on_change=validate_matchups,
                key=k_stde_matchups,
                num_rows="dynamic"
            )
            
            de_data = st.session_state.get(k_stde_matchups, {})
            
            # st.write("df_matchups")
            # st.write(df_matchups)
            # st.write("de_data")
            # st.write(de_data)
            dfc: pd.DataFrame = consolidate_df_edits(df_matchups, de_data)
            st.write("dfc")
            st.write(dfc)
            if not dfc.empty:
                filter_idxs = []
                for i, row in dfc.iterrows():
                    team1 = row.get("Team1")
                    team2 = row.get("Team2")
                    # st.write(f"{team1=}, {team2=}")
                    if pd.isna(team1):
                        team1 = team2 if not pd.isna(team2) else None
                        team2 = None
                    st.write(f"{team1=}, {team2=}")
                    if (not pd.isna(team1)) and pd.isna(team2):
                        # all matchups for this team
                        for j, team in enumerate(teams):
                            df_ww = df_w[
                                ((df_w["AwayTeam"] == team1) & (df_w["HomeTeam"] == team))
                                | ((df_w["AwayTeam"] == team) & (df_w["HomeTeam"] == team1))
                            ]
                            filter_idxs += df_ww.index.tolist()
                            
                    else:
                        # matchups between the two teams
                        df_ww = df_w[
                            ((df_w["AwayTeam"] == team1) & (df_w["HomeTeam"] == team2))
                            | ((df_w["AwayTeam"] == team2) & (df_w["HomeTeam"] == team1))
                        ]
                        window = df_ww.index.tolist()
                        if radio_and_or == "Or":
                            # st.write(f"window")
                            # st.write(window)
                            filter_idxs += window
                        else:
                            if not filter_idxs:
                                filter_idxs += window
                            else:
                                window = window
                                filter_idxs = list(set(filter_idxs).intersection(set(window)))
                df_w = df_w.loc[filter_idxs]
                
            st.write("filter_idxs")
            st.write(filter_idxs)
            
            # df_w = df_w[
            #     (
            #         (
            #             (df_w["AwayTeam"] == "CGY")
            #             & (df_w["HomeTeam"] == "ANA")
            #         ) | (
            #             (df_w["AwayTeam"] == "ANA")
            #             & (df_w["HomeTeam"] == "CGY")
            #         )
            #     ) |
            #     (
            #         (
            #             (df_w["AwayTeam"] == "UTA")
            #             & (df_w["HomeTeam"] == "ANA")
            #         ) | (
            #             (df_w["AwayTeam"] == "ANA")
            #             & (df_w["HomeTeam"] == "UTA")
            #         )
            #     ) |
            #     (
            #         (
            #             (df_w["AwayTeam"] == "EDM")
            #             & (df_w["HomeTeam"] == "ANA")
            #         ) | (
            #             (df_w["AwayTeam"] == "ANA")
            #             & (df_w["HomeTeam"] == "EDM")
            #         )
            #     ) |
            #     (
            #         (
            #             (df_w["AwayTeam"] == "LAK")
            #             & (df_w["HomeTeam"] == "ANA")
            #         ) | (
            #             (df_w["AwayTeam"] == "ANA")
            #             & (df_w["HomeTeam"] == "LAK")
            #         )
            #     ) |
            #     (
            #         (
            #             (df_w["AwayTeam"] == "MTL")
            #             & (df_w["HomeTeam"] == "NJD")
            #         ) | (
            #             (df_w["AwayTeam"] == "NJD")
            #             & (df_w["HomeTeam"] == "MTL")
            #         )
            #     ) |
            #     (
            #         (
            #             (df_w["AwayTeam"] == "ANA")
            #             & (df_w["HomeTeam"] == "NSH")
            #         ) | (
            #             (df_w["AwayTeam"] == "NSH")
            #             & (df_w["HomeTeam"] == "ANA")
            #         )
            #     )
            # ]
        
        df_w = df_w.groupby(
            ["AwayTeam", "HomeTeam"]
        ).agg({
            "GameID": "count",
            "AwayWon": "sum",
            "HomeWon": "sum",
            "HasExtraTime": "sum",
            "A_ETL": "sum",
            "H_ETL": "sum"
        }).reset_index()
        
        df_w["Record"] = ""
        covered = set()
        to_add = []
        with st.container(horizontal=False):
            for i, a_row in df_w.iterrows():
                # st.write(a_row)
                if i not in covered:
                    covered.add(i)
                else:
                    continue
                a, b = a_row["AwayTeam"], a_row["HomeTeam"]
                j_row_lst = df_w[(df_w["AwayTeam"] == b) & (df_w["HomeTeam"] == a)].index.tolist()
                if len(j_row_lst):
                    j = j_row_lst[0]
                    h_row = df_w.iloc[j]
                    covered.add(j)
                else:
                    h_row = {
                        "GameID": 0,
                        "AwayWon": False,
                        "HomeWon": False,
                        "A_ETL": 0,
                        "H_ETL": 0,
                    }
                    to_add.append(pd.DataFrame({
                        k: [v]
                        for k, v in {
                            "AwayTeam": b,
                            "HomeTeam": a,
                            "GameID": int(a_row["GameID"]),
                            "AwayWon": int(a_row["HomeWon"]),
                            "HomeWon": int(a_row["AwayWon"]),
                            "HasExtraTime": 0,
                            "A_ETL": int(a_row["H_ETL"]),
                            "H_ETL": int(a_row["A_ETL"]),
                            "Record": f"{(int(a_row['HomeWon']), int(a_row['AwayWon'] - a_row['H_ETL']), int(a_row['H_ETL']))}",
                        }.items()
                    }))
                
                a_gp = int(a_row["GameID"])
                h_gp = int(h_row["GameID"])
                t_gp = a_gp + h_gp
                
                a_aw = int(a_row["AwayWon"])
                a_hw = int(a_row["HomeWon"])
                h_aw = int(h_row["AwayWon"])
                h_hw = int(h_row["HomeWon"])
                a_w = a_aw + h_hw
                h_w = a_hw + h_aw
                
                a_et = int(a_row["A_ETL"] + h_row["H_ETL"])
                h_et = int(a_row["H_ETL"] + h_row["A_ETL"])
                
                a_l = t_gp - (a_w + a_et)
                h_l = t_gp - (h_w + h_et)
                
                away_record = (a_w, a_l, a_et)
                home_record = (h_w, h_l, h_et)
                
                # dd = dict(
                #     a=a,
                #     b=b,
                #     i=i,
                #     j=j,
                #     # covered=covered,             
                #     a_gp=a_gp,
                #     a_aw=a_aw,
                #     a_hw=a_hw,
                #     a_w=a_w,
                #     a_het=a_het,    
                #     h_gp=h_gp,
                #     h_aw=h_aw,
                #     h_hw=h_hw,
                #     h_w=h_w,
                #     h_het=h_het,   
                #     t_gp=t_gp,             
                #     a_et=a_et,    
                #     h_et=h_et,        
                #     a_l=a_l,
                #     h_l=h_l,
                #     away_record=away_record,
                #     home_record=home_record,
                # )
                # st.write(dd)
                # display_df(pd.DataFrame({k: [v] for k, v in dd.items()}))
                
                df_w.loc[i, "Record"] = str(away_record)
                df_w.loc[j, "Record"] = str(home_record)
        
        if to_add:
            df_ta = pd.concat(to_add) 
            df_w = pd.concat([df_w, df_ta], ignore_index=True)
        df_w.sort_values(["AwayTeam", "HomeTeam"], inplace=True)
        
        display_df(df_w, "df_w")
        
        df_w["colour"] = df_w["Record"].apply(lambda r: TEAM_RECORD_COLOUR_MAP[r]["color"])
        
        # with st.container(horizontal=True):
        cc1, cc2, cc3, cc4 = st.columns([3, 1, 3, 1])
        x_sort_mode = cc1.selectbox("Sort X axis by", ["Conference", "Division", "Team", "Best to Worst Record"], index=3)
        x_sort_rev = not cc2.toggle("Ascending?", key="x_sort_rev", value=True)
        y_sort_mode = cc3.selectbox("Sort Y axis by", ["Conference", "Division", "Team", "Best to Worst Record"], index=3)
        y_sort_rev = not cc4.toggle("Ascending?", key="y_sort_rev", value=True)

        x_team_order = build_team_order(df_w, TEAM_META, x_sort_mode, x_sort_rev)
        y_team_order = build_team_order(df_w, TEAM_META, y_sort_mode, y_sort_rev)

        fig, res_df = render_team_record_heatmap_fast(
            df=df_w,
            x_team_order=x_team_order,
            y_team_order=y_team_order,
            record_colour_map=TEAM_RECORD_COLOUR_MAP
        )

        st.plotly_chart(fig, use_container_width=True)
        
        df_w["Remaining"] = 0
        for i, row in future.iterrows():
            away = row["AwayTeam"]
            home = row["HomeTeam"]
            a_row = df_w[(df_w["AwayTeam"] == away) & (df_w["HomeTeam"] == home)]
            # b_row = df_w[(df_w["AwayTeam"] == home) & (df_w["HomeTeam"] == away)]
            if not a_row.empty:
                a_idx = a_row.index.tolist()[0]
                # b_idx = b_row.index.tolist()[0]
                df_w.loc[a_idx, "Remaining"] += 1
        
        df_toar = pd.DataFrame(
            columns=[
                "TeamA", "TeamB", "GP",
                "Away_W", "Home_W",
                "Away_ET", "Home_ETL",
                "Away_Record", "Home_Record",
                "Colour_A", "Colour_B",
                "GR", "W", "L", "OTL", "Record"
            ]
        )
        df_toar.rename(columns={"GameID" : "GP"}, inplace=True)    
        for i, row in df_w.iterrows():
            away = row["AwayTeam"]
            home = row["HomeTeam"]
            a_row = df_w[(df_w["AwayTeam"] == away) & (df_w["HomeTeam"] == home)]
            b_row = df_w[(df_w["AwayTeam"] == home) & (df_w["HomeTeam"] == away)]
            a_idx = a_row.index.tolist()[0]
            b_idx = b_row.index.tolist()[0]
            a_row = a_row.reset_index().iloc[0]
            b_row = b_row.reset_index().iloc[0]
            row_data = [
                away,
                home,
                int(a_row["GameID"] + b_row["GameID"]),  # GP
                int(a_row["AwayWon"] + b_row["HomeWon"]),  # Away_W
                int(a_row["HomeWon"] + b_row["AwayWon"]),  # Home_W
                int(a_row["A_ETL"] + b_row["H_ETL"]),  # Away_ET
                int(a_row["H_ETL"] + b_row["A_ETL"]),  # Home_ETL
                a_row["Record"],
                b_row["Record"],
                a_row["colour"],
                b_row["colour"],
                a_row["Remaining"] + b_row["Remaining"],  # GR
                int(a_row["AwayWon"] + b_row["HomeWon"]),  # W
                int((a_row["HomeWon"] - a_row["A_ETL"]) + (b_row["AwayWon"] - b_row["H_ETL"])),  # L
                int(a_row["A_ETL"] + b_row["H_ETL"]),  # OTL
                a_row["Record"],
            ]
            # if int(i) == 0:
            #     st.write(a_row)
            #     st.write(b_row)
            #     st.write(row_data)
            #     st.write(df_toar.columns.tolist())
            df_toar.loc[i] = row_data
            
        df_toar["PTS"] = df_toar.apply(lambda r: (2 * r["W"]) + r["OTL"], axis=1)
        df_toar["PCT"] = df_toar.apply(lambda r: ((r["PTS"] / r["GP"]) / 2) if r["GP"] != 0 else 0, axis=1)
        df_toar["MAX_PTS"] = df_toar.apply(lambda r: r["PTS"] + (2 * r["GR"]), axis=1)
        df_toar["Sweep"] = df_toar.apply(lambda r: (r["GR"] == 0) and (r["GP"] == r["W"]), axis=1)
        df_toar["WasSwept"] = df_toar.apply(lambda r: (r["GR"] == 0) and (r["PTS"] == 0), axis=1)
        
        with st.expander("View data table", expanded=False):
            display_df(
                df_w,
                "Data"
            )
            # display_df(
            #     res_df,
            #     "res_df"
            # )
        
        st.markdown('<div class="section-header">🧹 Season Sweeps</div>', unsafe_allow_html=True)
        num_sweeps = df_toar["Sweep"].sum()
        st.write(f"{num_sweeps} total sweeps this regular season")
        display_df(
            df_toar,
            "Team vs Team Records"
        )
        
        k_multiselect_sort_toar = "key_multiselect_sort_toar"
        # st.session_state.setdefault(k_multiselect_sort_toar, ["SweepCount", "SweptByCount", "TiedCount", "NetSweepDiff", "TeamName"])
        multiselect_sort_toar = sort_items(
            header="Sort Order",
            items=[
                {"header": "Sort Order", "items": ["SweepCount", "SweptByCount", "TiedCount", "NetSweepDiff", "TeamName"]},
                {"header": "Exclude", "items": []}
            ],
            multi_containers=True,
            key=k_multiselect_sort_toar
        )
        sort_asc_toar = False
        sort_items_use = multiselect_sort_toar[0]["items"]
        if sort_items:
            co_asc = st.columns(len(sort_items_use))
            sort_asc_toar = [
                co_asc[i].toggle(f"{sort} ASC", value=False, key=f"col_asc_sort_{i=}_{sort=}")
                for i, sort in enumerate(sort_items_use)
            ]
            
        render_sweep_logo_table(df_toar, sort=sort_items_use, ascending=sort_asc_toar)
            
        # df_zero_against = df_w[df_w[""]].groupby("AwayTeam")

    # ── PAGE: BY TEAM ────────────────────────────────────
    elif page == "👥 By Team":
        st.markdown('<div class="section-header">TEAM PERFORMANCE EXPLORER</div>', unsafe_allow_html=True)

        all_teams = sorted(set(completed["AwayTeam"].dropna()) | set(completed["HomeTeam"].dropna()))
        selected_team = st.selectbox("Select Team", all_teams)

        team_logo_url = fetch_team_logo(selected_team)
        team_name = TEAM_META.get(selected_team, {}).get("name", selected_team)

        col_logo, col_title = st.columns([1, 6])
        with col_logo:
            if team_logo_url:
                st.image(team_logo_url, width=80)
        with col_title:
            st.markdown(f"### {team_name} ({selected_team})")
            meta = TEAM_META.get(selected_team, {})
            st.caption(f"{meta.get('conf','?')} Conference · {meta.get('div','?')} Division")

        # Filter conditions
        st.markdown("#### 🔍 Filter Conditions")
        filter_cols = st.columns(3)
        filter_opts = {
            "Away Games Only": None,
            "Home Games Only": None,
            "Playing Back-to-Back": None,
            "On Road Trip": None,
            "On Home Stand": None,
            "Team Won Last Game": None,
            "Team Lost Last Game": None,
        }
        selected_filters = []
        for i, (label, _) in enumerate(filter_opts.items()):
            with filter_cols[i % 3]:
                if st.checkbox(label):
                    selected_filters.append(label)

        # Build team dataframe
        team_away = completed[completed["AwayTeam"] == selected_team].copy()
        team_home = completed[completed["HomeTeam"] == selected_team].copy()
        team_all  = pd.concat([team_away, team_home]).sort_values("GameDate").drop_duplicates()

        # Apply filters
        fdf = team_all.copy()
        for f in selected_filters:
            if f == "Away Games Only":
                fdf = fdf[fdf["AwayTeam"] == selected_team]
            elif f == "Home Games Only":
                fdf = fdf[fdf["HomeTeam"] == selected_team]
            elif f == "Playing Back-to-Back":
                fdf = fdf[
                    ((fdf["AwayTeam"] == selected_team) & fdf["AwayB2B"]) |
                    ((fdf["HomeTeam"] == selected_team) & fdf["HomeB2B"])
                ]
            elif f == "On Road Trip":
                fdf = fdf[(fdf["AwayTeam"] == selected_team) & fdf["OnRoadTrip"]]
            elif f == "On Home Stand":
                fdf = fdf[(fdf["HomeTeam"] == selected_team) & fdf["OnHomeStand"]]
            elif f == "Team Won Last Game":
                fdf = fdf[
                    ((fdf["AwayTeam"] == selected_team) & (fdf["AwayWonLast"] == True)) |
                    ((fdf["HomeTeam"] == selected_team) & (fdf["HomeWonLast"] == True))
                ]
            elif f == "Team Lost Last Game":
                fdf = fdf[
                    ((fdf["AwayTeam"] == selected_team) & (fdf["AwayWonLast"] == False)) |
                    ((fdf["HomeTeam"] == selected_team) & (fdf["HomeWonLast"] == False))
                ]

        n_t = len(fdf)
        n_c = fdf["CorrectWinnerPrediction"].sum() if n_t > 0 else 0

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Games (filtered)", n_t)
        m2.metric("Correct", int(n_c))
        m3.metric("Accuracy", f"{n_c/n_t*100:.1f}%" if n_t > 0 else "—")
        m4.metric("Home/Away Split", f"{len(fdf[fdf['HomeTeam']==selected_team])}H / {len(fdf[fdf['AwayTeam']==selected_team])}A")

        if n_t > 0:
            st.plotly_chart(rolling_accuracy_chart(fdf, selected_team), use_container_width=True)
            st.plotly_chart(game_by_game_scatter(fdf, selected_team), use_container_width=True)

            # Game-by-game table
            st.markdown("#### Game Log")
            display_cols = ["GameDate", "AwayTeam", "HomeTeam", "PredictedWinner", "ActualWinner",
                            "CorrectWinnerPrediction", "ActualResult", "GamePredictionScore"]
            display_cols = [c for c in display_cols if c in fdf.columns]
            log_df = fdf[display_cols].sort_values("GameDate", ascending=False).copy()
            log_df["CorrectWinnerPrediction"] = log_df["CorrectWinnerPrediction"].map(
                {True: "✅", False: "❌"}
            )
            st.dataframe(log_df, use_container_width=True, height=320)
        else:
            st.warning("No games match the selected filters.")

        # Home vs Away breakdown
        st.markdown('<div class="section-header">HOME VS AWAY BREAKDOWN</div>', unsafe_allow_html=True)
        col_hv, col_av = st.columns(2)

        for col_w, subset, label in [(col_hv, team_home, "Home"), (col_av, team_away, "Away")]:
            with col_w:
                n = len(subset)
                c = subset["CorrectWinnerPrediction"].sum() if n > 0 else 0
                st.metric(f"{label} Games", n)
                st.metric(f"{label} Accuracy", f"{c/n*100:.1f}%" if n > 0 else "—")
                if n > 0:
                    st.plotly_chart(correct_incorrect_pie(int(c), n), use_container_width=True)

    # ── PAGE: TRENDS OVER TIME ────────────────────────────
    elif page == "🗓️ Trends Over Time":
        st.markdown('<div class="section-header">PREDICTION TRENDS OVER TIME</div>', unsafe_allow_html=True)

        # Overall cumulative accuracy
        overall = completed.sort_values("GameDate").copy()
        overall["CumAcc"] = overall["CorrectWinnerPrediction"].expanding().mean() * 100
        overall["Roll14"] = overall["CorrectWinnerPrediction"].rolling(14, min_periods=5).mean() * 100

        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(
            x=overall["GameDate"], y=overall["CumAcc"],
            name="Cumulative Accuracy", line=dict(color=GOLD, width=2),
        ))
        fig_trend.add_trace(go.Scatter(
            x=overall["GameDate"], y=overall["Roll14"],
            name="14-Game Rolling Avg", line=dict(color=ICE_BLUE, width=2, dash="dot"),
        ))
        fig_trend.add_hline(y=50, line_dash="dash", line_color="#555", annotation_text="50%")
        fig_trend.update_layout(
            **DARK_THEME,
            title="Overall Prediction Accuracy Over Time",
            xaxis_title="Date", yaxis_title="Accuracy %",
            yaxis_range=[0, 105], height=380
        )
        st.plotly_chart(fig_trend, use_container_width=True)

        # By week
        st.markdown('<div class="section-header">WEEKLY BREAKDOWN</div>', unsafe_allow_html=True)
        weekly = (
            completed.groupby("WeekStart")["CorrectWinnerPrediction"]
            .agg(["sum", "count"]).reset_index()
        )
        weekly.columns = ["Week", "Correct", "Total"]
        weekly["Accuracy"] = weekly["Correct"] / weekly["Total"] * 100

        fig_wk = go.Figure()
        fig_wk.add_trace(go.Bar(
            x=weekly["Week"], y=weekly["Accuracy"],
            marker_color=[GREEN if a >= 50 else RED for a in weekly["Accuracy"]],
            text=weekly["Accuracy"].round(1), texttemplate="%{text:.1f}%",
            textposition="outside",
            hovertemplate="Week of %{x}<br>Accuracy: %{y:.1f}%<br>Games: %{customdata}<extra></extra>",
            customdata=weekly["Total"]
        ))
        fig_wk.add_hline(y=50, line_dash="dash", line_color="#888")
        fig_wk.update_layout(**DARK_THEME, title="Accuracy by Week", yaxis_range=[0, 110], height=380)
        st.plotly_chart(fig_wk, use_container_width=True)

        # By month
        st.markdown('<div class="section-header">MONTHLY BREAKDOWN</div>', unsafe_allow_html=True)
        monthly = (
            completed.groupby(["MonthNum", "Month"])["CorrectWinnerPrediction"]
            .agg(["sum", "count"]).reset_index().sort_values("MonthNum")
        )
        monthly.columns = ["MonthNum", "Month", "Correct", "Total"]
        monthly["Accuracy"] = monthly["Correct"] / monthly["Total"] * 100

        fig_mo = px.bar(
            monthly, x="Month", y="Accuracy",
            color="Accuracy",
            color_continuous_scale=[[0, RED], [0.5, "#f39c12"], [1, GREEN]],
            text=monthly["Accuracy"].round(1),
            title="Accuracy by Month"
        )
        fig_mo.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig_mo.update_layout(**DARK_THEME, coloraxis_showscale=False, yaxis_range=[0, 110], height=380)
        st.plotly_chart(fig_mo, use_container_width=True)

        # Day of week heatmap
        st.markdown('<div class="section-header">DAY OF WEEK HEATMAP</div>', unsafe_allow_html=True)
        dow_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        dow = (
            completed.groupby("DayOfWeek")["CorrectWinnerPrediction"]
            .agg(["sum", "count"]).reset_index()
        )
        dow.columns = ["Day", "Correct", "Total"]
        dow["Accuracy"] = dow["Correct"] / dow["Total"] * 100
        dow["Day"] = pd.Categorical(dow["Day"], categories=dow_order, ordered=True)
        dow = dow.sort_values("Day")

        fig_dow = px.bar(
            dow, x="Day", y="Accuracy",
            color="Accuracy",
            color_continuous_scale=[[0, RED], [0.5, "#f39c12"], [1, GREEN]],
            text=dow["Accuracy"].round(1),
            title="Accuracy by Day of Week",
            hover_data=["Correct", "Total"]
        )
        fig_dow.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig_dow.update_layout(**DARK_THEME, coloraxis_showscale=False, yaxis_range=[0, 110], height=360)
        st.plotly_chart(fig_dow, use_container_width=True)

    # ── PAGE: TRAVEL & GAUNTLETS ──────────────────────────
    elif page == "🌍 Travel & Gauntlets":
        st.markdown('<div class="section-header">TRAVEL PATTERNS & SCHEDULING GAUNTLETS</div>', unsafe_allow_html=True)

        st.markdown("""
        Scheduling gauntlets occur when an away team travels through a geographic cluster of opponents
        consecutively. Detect how well games are predicted during these grueling road swings.
        """)

        # Road trip performance
        st.markdown('<div class="section-header">ROAD TRIP PERFORMANCE</div>', unsafe_allow_html=True)

        rt_df = completed[completed["OnRoadTrip"]].copy()
        st_df = completed[~completed["OnRoadTrip"]].copy()

        col_rt1, col_rt2 = st.columns(2)
        with col_rt1:
            n_rt = len(rt_df)
            c_rt = rt_df["CorrectWinnerPrediction"].sum() if n_rt > 0 else 0
            st.metric("Road Trip Games", n_rt)
            st.metric("Road Trip Accuracy", f"{c_rt/n_rt*100:.1f}%" if n_rt > 0 else "—")
            if n_rt > 0:
                st.plotly_chart(correct_incorrect_pie(int(c_rt), n_rt), use_container_width=True)
        with col_rt2:
            n_st = len(st_df)
            c_st = st_df["CorrectWinnerPrediction"].sum() if n_st > 0 else 0
            st.metric("Standard Away Games", n_st)
            st.metric("Standard Away Accuracy", f"{c_st/n_st*100:.1f}%" if n_st > 0 else "—")
            if n_st > 0:
                st.plotly_chart(correct_incorrect_pie(int(c_st), n_st), use_container_width=True)

        # Gauntlet analysis
        st.markdown('<div class="section-header">GAUNTLET PERFORMANCE</div>', unsafe_allow_html=True)

        gauntlet_games = completed[completed["GauntletName"] != ""].copy()
        non_gauntlet   = completed[completed["GauntletName"] == ""].copy()

        if len(gauntlet_games) > 0:
            gauntlet_summary = (
                gauntlet_games.groupby("GauntletName")["CorrectWinnerPrediction"]
                .agg(["sum", "count"]).reset_index()
            )
            gauntlet_summary.columns = ["Gauntlet", "Correct", "Total"]
            gauntlet_summary["Accuracy"] = (gauntlet_summary["Correct"] / gauntlet_summary["Total"] * 100).round(1)

            fig_g = px.bar(
                gauntlet_summary.sort_values("Accuracy", ascending=True),
                x="Accuracy", y="Gauntlet", orientation="h",
                color="Accuracy",
                color_continuous_scale=[[0, RED], [0.5, "#f39c12"], [1, GREEN]],
                text="Accuracy",
                title="Prediction Accuracy During Gauntlet Swings",
                hover_data=["Correct", "Total"]
            )
            fig_g.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
            fig_g.update_layout(**DARK_THEME, coloraxis_showscale=False, height=400)
            st.plotly_chart(fig_g, use_container_width=True)

            for gauntlet_name, g_info in GAUNTLETS.items():
                g_games = gauntlet_games[gauntlet_games["GauntletName"].str.contains(gauntlet_name.split("🌴")[0].strip().split("🍁")[0].strip(), na=False)]
                if len(g_games) == 0:
                    continue
                n_g = len(g_games)
                c_g = g_games["CorrectWinnerPrediction"].sum()
                with st.expander(f"{gauntlet_name} — {n_g} games, {c_g/n_g*100:.0f}% accuracy"):
                    st.caption(g_info["desc"])
                    dcols = ["GameDate", "AwayTeam", "HomeTeam", "ActualWinner", "CorrectWinnerPrediction"]
                    dcols = [c for c in dcols if c in g_games.columns]
                    st.dataframe(g_games[dcols].sort_values("GameDate"), use_container_width=True)
        else:
            st.info("No gauntlet patterns detected in completed games yet. As the season progresses, patterns will emerge from consecutive away game groupings.")

        # Show gauntlet definitions
        st.markdown('<div class="section-header">GAUNTLET DEFINITIONS</div>', unsafe_allow_html=True)
        cols = st.columns(2)
        for i, (name, info) in enumerate(GAUNTLETS.items()):
            with cols[i % 2]:
                teams_str = " · ".join([
                    f'<img src="{fetch_team_logo(t)}" width="24" style="vertical-align:middle"> {t}'
                    for t in info["teams"]
                ])
                st.markdown(f"""
                <div class="gauntlet-card">
                    <div class="gauntlet-title">{name}</div>
                    <div style="color:#8899aa; font-size:0.85rem; margin-top:4px">{info["desc"]}</div>
                    <div style="margin-top:8px; font-size:0.8rem; color:#ccd6e0">{", ".join(info["teams"])}</div>
                </div>
                """, unsafe_allow_html=True)

    # ── PAGE: FUTURE PREDICTIONS ──────────────────────────
    elif page == "🔮 Future Predictions":
        st.markdown('<div class="section-header">FUTURE GAME PREDICTIONS</div>', unsafe_allow_html=True)

        pred_df = build_predictions(df)

        if len(pred_df) == 0:
            st.info("🎉 All games in your dataset have been completed! No future games to predict.")
            return

        st.markdown(f"Found **{len(pred_df)}** upcoming games to predict using statistical win rates from your dataset.")

        # Team win rate stats used for predictions
        completed_copy = completed.copy()
        away_stats = (
            completed_copy.groupby("AwayTeam")["AwayWon"]
            .agg(["mean", "count"]).reset_index()
        )
        away_stats.columns = ["Team", "AwayWinRate", "AwayGames"]
        home_stats = (
            completed_copy.groupby("HomeTeam")["HomeWon_"]
            .agg(["mean", "count"]).reset_index()
        )
        home_stats.columns = ["Team", "HomeWinRate", "HomeGames"]

        with st.expander("📈 Team Win Rate Statistics (basis for predictions)"):
            combined_stats = away_stats.merge(home_stats, on="Team", how="outer")
            combined_stats["OverallGames"] = combined_stats["AwayGames"].fillna(0) + combined_stats["HomeGames"].fillna(0)
            combined_stats["AwayWinRate"] = (combined_stats["AwayWinRate"] * 100).round(1)
            combined_stats["HomeWinRate"] = (combined_stats["HomeWinRate"] * 100).round(1)

            fig_stats = px.scatter(
                combined_stats.dropna(subset=["AwayWinRate", "HomeWinRate"]),
                x="AwayWinRate", y="HomeWinRate", text="Team",
                size="OverallGames", color="HomeWinRate",
                color_continuous_scale=[[0, RED], [0.5, "#f39c12"], [1, GREEN]],
                title="Team Away vs Home Win Rates",
                labels={"AwayWinRate": "Away Win Rate %", "HomeWinRate": "Home Win Rate %"}
            )
            fig_stats.update_traces(textposition="top center")
            fig_stats.update_layout(**DARK_THEME, coloraxis_showscale=False, height=450)
            st.plotly_chart(fig_stats, use_container_width=True)

        # Display predictions
        st.markdown('<div class="section-header">UPCOMING GAME PREDICTIONS</div>', unsafe_allow_html=True)

        filter_team = st.selectbox(
            "Filter by team (optional)",
            ["All Teams"] + sorted(set(pred_df["AwayTeam"]) | set(pred_df["HomeTeam"]))
        )

        display_pred = pred_df.copy()
        if filter_team != "All Teams":
            display_pred = display_pred[
                (display_pred["AwayTeam"] == filter_team) |
                (display_pred["HomeTeam"] == filter_team)
            ]

        display_pred["GameDate"] = pd.to_datetime(display_pred["GameDate"]).dt.strftime("%a %b %d")
        display_pred["Matchup"] = display_pred["AwayTeam"] + " @ " + display_pred["HomeTeam"]
        display_pred["Predicted Score"] = (
            display_pred["PredictedAwayScore"].astype(str) + " – " +
            display_pred["PredictedHomeScore"].astype(str)
        )
        display_pred["Win Probabilities"] = (
            display_pred["AwayTeam"] + ": " + display_pred["AwayWinProb"].astype(str) + "% | " +
            display_pred["HomeTeam"] + ": " + display_pred["HomeWinProb"].astype(str) + "%"
        )
        display_pred["Conf %"] = display_pred["Confidence"].astype(str) + "%"

        st.dataframe(
            display_pred[["GameDate", "Matchup", "PredictedWinner",
                          "Predicted Score", "PredictedResult",
                          "Win Probabilities", "Conf %"]],
            use_container_width=True
        )

        # Confidence distribution
        fig_conf = px.histogram(
            pred_df, x="Confidence", nbins=20,
            color_discrete_sequence=[GOLD],
            title="Distribution of Prediction Confidence",
            labels={"Confidence": "Confidence %", "count": "Games"}
        )
        fig_conf.update_layout(**DARK_THEME, height=300)
        st.plotly_chart(fig_conf, use_container_width=True)

        # Predicted winners summary
        winners = pred_df["PredictedWinner"].value_counts().reset_index()
        winners.columns = ["Team", "Predicted Wins"]

        col_pw1, col_pw2 = st.columns(2)
        with col_pw1:
            fig_pw = px.bar(
                winners.head(15), x="Predicted Wins", y="Team", orientation="h",
                color="Predicted Wins", color_continuous_scale=[[0, ICE_BLUE], [1, GOLD]],
                title="Teams with Most Predicted Wins (upcoming)"
            )
            fig_pw.update_layout(**DARK_THEME, coloraxis_showscale=False, height=420)
            st.plotly_chart(fig_pw, use_container_width=True)
        with col_pw2:
            st.markdown("**Top Confident Predictions**")
            top_conf = pred_df.nlargest(10, "Confidence")[
                ["GameDate", "AwayTeam", "HomeTeam", "PredictedWinner",
                 "PredictedAwayScore", "PredictedHomeScore", "PredictedResult", "Confidence"]
            ].copy()
            top_conf["Predicted Score"] = (
                top_conf["PredictedAwayScore"].astype(str) + " – " +
                top_conf["PredictedHomeScore"].astype(str)
            )
            top_conf = top_conf.drop(columns=["PredictedAwayScore","PredictedHomeScore"])
            top_conf["GameDate"] = pd.to_datetime(top_conf["GameDate"]).dt.strftime("%b %d")
            top_conf["Confidence"] = top_conf["Confidence"].astype(str) + "%"
            st.dataframe(top_conf, use_container_width=True, hide_index=True)
    
    # ── PAGE: CLINCHING SCENARIOS──────────────────────────
    elif page == "🏆 Clinching Scenarios":
        page_clinching_scenarios()

    # ── PAGE: JERSEY COLLECTION ───────────────────────────
    elif page == "🧥 Jersey Collection":
        
        df_jerseys = load_jersey_workbook()
        if not df_jerseys.empty:        
            page_jersey_collection(df_jerseys, path_jersey_images)
    
    # ── PAGE: Hockey Pool ──────────────────────────
    elif page == "Hockey Pool":
        page_hockey_pool()


if __name__ == "__main__":
    main()