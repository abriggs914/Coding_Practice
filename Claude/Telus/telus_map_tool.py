"""
TELUS Maps Analyst – Interactive Study Aid
==========================================
Run locally:
    pip install streamlit folium streamlit-folium geopy
    streamlit run telus_map_tool.py

No API key required — blurb generation runs entirely on local rule logic.
"""

import math
import urllib.parse
import streamlit as st
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

# ─── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="TELUS Maps Study Aid",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Inter:wght@400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    code, .mono { font-family: 'DM Mono', monospace; }
    .stApp { background: #0a0f1e; color: #e2e8f0; }
    section[data-testid="stSidebar"] { background: #0d1424 !important; border-right: 1px solid #1a2540; }
    h1, h2, h3 { color: #f1f5f9 !important; }
    .block-container { padding-top: 1.5rem; }

    /* Cards */
    .card {
        background: #111827;
        border: 1px solid #1e293b;
        border-radius: 10px;
        padding: 16px 18px;
        margin-bottom: 14px;
    }
    .card-title {
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #475569;
        margin-bottom: 8px;
    }

    /* Tags */
    .tag {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.06em;
        margin-right: 6px;
        margin-bottom: 4px;
    }
    .tag-blue  { background: #1e3a5f33; color: #60a5fa; border: 1px solid #1e3a5f; }
    .tag-green { background: #14532d33; color: #4ade80; border: 1px solid #14532d; }
    .tag-red   { background: #7f1d1d33; color: #f87171; border: 1px solid #7f1d1d; }
    .tag-amber { background: #78350f33; color: #fbbf24; border: 1px solid #78350f; }
    .tag-purple{ background: #312e8133; color: #a5b4fc; border: 1px solid #312e81; }

    /* Link buttons */
    .link-btn {
        display: inline-block;
        padding: 5px 13px;
        border-radius: 6px;
        background: #1e293b;
        border: 1px solid #2a3650;
        color: #94a3b8 !important;
        font-size: 12px;
        font-weight: 600;
        text-decoration: none !important;
        margin-right: 6px;
        margin-bottom: 6px;
        transition: background 0.15s;
    }
    .link-btn:hover { background: #2a3650; color: #e2e8f0 !important; }
    .link-btn-primary { background: #1e3a5f; border-color: #2563eb; color: #60a5fa !important; }
    .link-btn-warn    { background: #1c0a0a; border-color: #dc2626; color: #f87171 !important; }
    .link-btn-green   { background: #052e16; border-color: #16a34a; color: #4ade80 !important; }

    /* Distance pill */
    .dist-good   { color: #4ade80; font-weight: 700; }
    .dist-warn   { color: #fbbf24; font-weight: 700; }
    .dist-bad    { color: #f87171; font-weight: 700; }

    /* Context blurb */
    .blurb-box {
        background: #090e1c;
        border: 1px solid #1e3a5f;
        border-radius: 8px;
        padding: 14px 16px;
        font-size: 13px;
        line-height: 1.7;
        color: #93c5fd;
        white-space: pre-wrap;
        font-family: 'DM Mono', monospace;
    }
    .warn-box {
        background: #1c0a0a;
        border: 1px solid #7f1d1d;
        border-radius: 8px;
        padding: 10px 14px;
        font-size: 13px;
        color: #fca5a5;
        margin-bottom: 8px;
    }
</style>
""", unsafe_allow_html=True)

# ─── Geocoder ─────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def geocode_address(address: str):
    """Return (lat, lon, display_name) or None."""
    try:
        geolocator = Nominatim(user_agent="telus_maps_study_aid_v1")
        loc = geolocator.geocode(address, timeout=8)
        if loc:
            return loc.latitude, loc.longitude, loc.address
    except GeocoderTimedOut:
        pass
    return None

def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1))*math.cos(math.radians(lat2))*math.sin(dlon/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

def km_to_miles(km):
    return km * 0.621371

# ─── Known chain locator URLs ─────────────────────────────────────────────────
CHAIN_LOCATORS = {
    # Fast food
    "mcdonald's": "https://www.mcdonalds.com/us/en-us/restaurant-locator.html",
    "mcdonalds":  "https://www.mcdonalds.com/us/en-us/restaurant-locator.html",
    "burger king":"https://www.burgerking.com/store-locator",
    "kfc":        "https://www.kfc.com/find-a-kfc",
    "taco bell":  "https://www.tacobell.com/find-a-taco-bell",
    "wendy's":    "https://www.wendys.com/restaurant-locator",
    "wendys":     "https://www.wendys.com/restaurant-locator",
    "subway":     "https://www.subway.com/en-US/FindASubway",
    "chick-fil-a":"https://www.chick-fil-a.com/locations",
    "chickfila":  "https://www.chick-fil-a.com/locations",
    "chick fil a":"https://www.chick-fil-a.com/locations",
    "whataburger":"https://whataburger.com/locations",
    "popeyes":    "https://www.popeyes.com/store-locator",
    "five guys":  "https://www.fiveguys.com/locations",
    "in-n-out":   "https://www.in-n-out.com/locations",
    "in n out":   "https://www.in-n-out.com/locations",
    "sonic":      "https://www.sonicdrivein.com/locations",
    "dairy queen":"https://www.dairyqueen.com/en-us/locator/",
    "jack in the box": "https://www.jackinthebox.com/locations",
    "hardee's":   "https://www.hardees.com/locations",
    "hardees":    "https://www.hardees.com/locations",
    "carl's jr":  "https://www.carlsjr.com/locations",
    "carls jr":   "https://www.carlsjr.com/locations",
    "arbys":      "https://arbys.com/locations",
    "arby's":     "https://arbys.com/locations",
    "panera":     "https://www.panerabread.com/en-us/cafe-locator.html",
    "panera bread":"https://www.panerabread.com/en-us/cafe-locator.html",
    "chipotle":   "https://www.chipotle.com/order",
    "domino's":   "https://www.dominos.com/en/pages/locator/",
    "dominos":    "https://www.dominos.com/en/pages/locator/",
    "pizza hut":  "https://www.pizzahut.com/locator",
    "papa john's":"https://www.papajohns.com/order/store-finder",
    "papa johns": "https://www.papajohns.com/order/store-finder",
    "little caesars": "https://littlecaesars.com/en-us/store-locator/",
    "dunkin":     "https://www.dunkindonuts.com/en/locations",
    "dunkin donuts": "https://www.dunkindonuts.com/en/locations",
    "starbucks":  "https://www.starbucks.com/store-locator",
    "tim hortons":"https://www.timhortons.com/store-locator",
    "panda express": "https://www.pandaexpress.com/locations",
    "raising cane's": "https://www.raisingcanes.com/locations",
    "wingstop":   "https://www.wingstop.com/order",
    "freddy's":   "https://www.freddysusa.com/locations/",
    "freddys":    "https://www.freddysusa.com/locations/",

    # Retail
    "walmart":    "https://www.walmart.com/store/finder",
    "target":     "https://www.target.com/store-locator/find-stores",
    "costco":     "https://www.costco.com/warehouse-locations",
    "home depot": "https://www.homedepot.com/l/storelocator",
    "lowe's":     "https://www.lowes.com/store",
    "lowes":      "https://www.lowes.com/store",
    "best buy":   "https://www.bestbuy.com/site/store-locator/store-finder",
    "walgreens":  "https://www.walgreens.com/storelocator/find.jsp",
    "cvs":        "https://www.cvs.com/store-locator/landing",
    "rite aid":   "https://www.riteaid.com/locations",
    "dollar tree":"https://www.dollartree.com/locations/index",
    "dollar general": "https://www.dollargeneral.com/store-directory",
    "family dollar": "https://stores.familydollar.com/",
    "tj maxx":    "https://tjmaxx.tjx.com/store-locator",
    "marshalls":  "https://www.marshalls.com/us/store/index.jsp",
    "ross":       "https://www.rossstores.com/store-finder",
    "whole foods":"https://www.wholefoodsmarket.com/stores",
    "trader joe's": "https://www.traderjoes.com/home/stores",
    "trader joes":"https://www.traderjoes.com/home/stores",
    "aldi":       "https://stores.aldi.us/",
    "kroger":     "https://www.kroger.com/stores/search",
    "safeway":    "https://www.safeway.com/stores/grocery-stores-near-me.html",
    "publix":     "https://www.publix.com/locations",
    "meijer":     "https://www.meijer.com/shopping/store-locator.html",
    "sam's club": "https://www.samsclub.com/club-finder",

    # Fuel / Convenience
    "shell":      "https://www.shell.com/motorists/shell-station-locator.html",
    "chevron":    "https://www.chevronwithtechron.com/en_us/home/find-a-station.html",
    "bp":         "https://www.bp.com/en_us/united-states/home/find-a-gas-station.html",
    "exxon":      "https://www.exxon.com/en/find-station",
    "mobil":      "https://www.mobil.com/en/find-station",
    "7-eleven":   "https://www.7-eleven.com/en/store-locator",
    "7 eleven":   "https://www.7-eleven.com/en/store-locator",
    "circle k":   "https://www.circlek.com/find-a-store",
    "speedway":   "https://www.speedway.com/storelocator",

    # Hotels
    "marriott":   "https://www.marriott.com/find-hotels/findHotels.mi",
    "hilton":     "https://www.hilton.com/en/locations/",
    "holiday inn":"https://www.ihg.com/holidayinn/hotels/us/en/find-hotels/hotel/list",
    "hampton inn":"https://www.hilton.com/en/hampton/",
    "hyatt":      "https://www.hyatt.com/find-a-hotel",
    "best western": "https://www.bestwestern.com/en_US/find-a-hotel.html",
    "motel 6":    "https://www.motel6.com/en/home/find-a-motel.html",

    # Banks
    "chase":      "https://locator.chase.com/",
    "bank of america": "https://www.bankofamerica.com/banking-centers-atms/",
    "wells fargo":"https://www.wellsfargo.com/locator/",
    "citibank":   "https://online.citi.com/US/JRS/portal/template.do?ID=ATMBranchLocator",
    "td bank":    "https://www.td.com/us/en/personal-banking/locations/",
    "us bank":    "https://www.usbank.com/bank-accounts/locations.html",

    # Others
    "ups store":  "https://www.theupsstore.com/tools/find-a-store",
    "fedex":      "https://local.fedex.com/",
    "usps":       "https://tools.usps.com/find-location.htm",
    "planet fitness": "https://www.planetfitness.com/gyms",
    "la fitness": "https://www.lafitness.com/pages/clublocator.aspx",
    "anytime fitness": "https://www.anytimefitness.com/gyms/",
    "autozone":   "https://www.autozone.com/locations",
    "o'reilly":   "https://www.oreillyauto.com/store-locator",
    "oreilly":    "https://www.oreillyauto.com/store-locator",
    "advance auto parts": "https://shop.advanceautoparts.com/o/store-locator",
    "jiffy lube": "https://www.jiffylube.com/locations",
    "valvoline":  "https://www.vioc.com/locations",

    # Transit / Transport
    "amtrak":     "https://www.amtrak.com/find-a-station",
    "greyhound":  "https://www.greyhound.com/en/locations",
}

CLASSIFICATION_KEYWORDS = {
    "pizza":        ["pizza", "italian", "pasta"],
    "burger":       ["burger", "fast food", "american food"],
    "mexican":      ["mexican", "taco", "burrito", "tex-mex"],
    "chinese":      ["chinese", "asian", "dim sum"],
    "gas station":  ["gas", "fuel", "petrol", "station", "shell", "chevron", "bp", "exxon"],
    "grocery":      ["grocery", "supermarket", "food store", "market"],
    "pharmacy":     ["pharmacy", "drug store", "walgreens", "cvs", "rite aid"],
    "hotel":        ["hotel", "motel", "inn", "lodging", "marriott", "hilton"],
    "bank":         ["bank", "atm", "financial", "chase", "wells fargo"],
    "airport":      ["airport", "terminal", "aviation", "airfield"],
    "mall":         ["mall", "shopping center", "plaza", "outlet"],
    "hospital":     ["hospital", "medical center", "health", "clinic"],
    "transit":      ["station", "transit", "subway", "metro", "bus terminal", "train"],
}

def detect_classification_issue(query: str, classification: str) -> str | None:
    """Return warning string if classification seems inconsistent with query."""
    q_lower = query.lower()
    c_lower = classification.lower()
    for cat, keywords in CLASSIFICATION_KEYWORDS.items():
        # Does classification match a category?
        if any(k in c_lower for k in keywords):
            # Does the query strongly imply a different category?
            for other_cat, other_kw in CLASSIFICATION_KEYWORDS.items():
                if other_cat != cat and any(k in q_lower for k in other_kw):
                    return f"Query suggests **{other_cat}** but classification is **{cat}** — possible mismatch (Section 6.3.2)"
    return None

def get_chain_locator(query: str) -> tuple[str | None, bool]:
    """Return (url, found) for the query chain."""
    q = query.lower().strip()
    # Try exact match first
    if q in CHAIN_LOCATORS:
        return CHAIN_LOCATORS[q], True
    # Try substring match
    for key, url in CHAIN_LOCATORS.items():
        if key in q or q in key:
            return url, True
    # Build a Google search fallback
    encoded = urllib.parse.quote(f"{query} store locator official site")
    return f"https://www.google.com/search?q={encoded}", False

def google_maps_link(lat: float, lon: float, label: str = "") -> str:
    return f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"

def google_maps_address_link(address: str) -> str:
    return f"https://www.google.com/maps/search/?api=1&query={urllib.parse.quote(address)}"

def usps_link(address: str) -> str:
    """Return USPS address verification tool URL (pre-filled where possible)."""
    return "https://tools.usps.com/zip-code-lookup.htm?byaddress"

# ─── Claude context blurb ─────────────────────────────────────────────────────

# ─── Rule-based blurb engine ──────────────────────────────────────────────────

DEMOTION_LABELS = {0: "Excellent", 1: "Good", 2: "Acceptable", 3: "Bad"}

def _demotion_to_label(n: int) -> str:
    if n <= 0: return "Excellent"
    if n == 1: return "Good"
    if n == 2: return "Acceptable"
    return "Bad"

def _address_diff_type(result_addr: str, official_addr: str) -> str | None:
    """
    Compare result address vs official address and return the sub-type of
    the first detected difference, or None if they match (case-insensitive,
    ignoring punctuation differences).
    """
    def norm(s):
        return " ".join(s.lower().replace(",", " ").replace(".", " ").split())

    r = norm(result_addr)
    o = norm(official_addr)
    if r == o:
        return None

    r_tokens = r.split()
    o_tokens = o.split()

    DIRECTIONS = {"n","s","e","w","ne","nw","se","sw","north","south","east","west"}
    STREET_TYPES = {"st","street","rd","road","ave","avenue","blvd","boulevard",
                    "dr","drive","ln","lane","ct","court","pl","place","way","cir","circle"}
    UNIT_WORDS   = {"suite","ste","unit","apt","#","floor","fl","building","bldg"}

    # Check if first token (street number) differs
    if r_tokens and o_tokens and r_tokens[0] != o_tokens[0]:
        if r_tokens[0].isdigit() or o_tokens[0].isdigit():
            return "Street Number"

    # Check for unit/apt presence in one but not the other
    r_has_unit = any(t in UNIT_WORDS for t in r_tokens)
    o_has_unit = any(t in UNIT_WORDS for t in o_tokens)
    if r_has_unit != o_has_unit:
        return "Unit/Apt"

    # Check for direction or street-type difference
    r_dirs = {t for t in r_tokens if t in DIRECTIONS}
    o_dirs = {t for t in o_tokens if t in DIRECTIONS}
    if r_dirs != o_dirs:
        return "Street Name"

    r_types = {t for t in r_tokens if t in STREET_TYPES}
    o_types = {t for t in o_tokens if t in STREET_TYPES}
    if r_types != o_types:
        return "Street Name"

    # Generic fallback
    return "Street Name"

def generate_blurb_local(params: dict) -> str:
    """
    Rule-based exam comment blurb generator.
    Returns a multi-section string in TELUS exam bracket format.
    """
    query       = params.get("query", "").strip()
    qtype       = params.get("query_type", "Chain Business")
    vp_status   = params.get("viewport_status", "Fresh")
    user_inside = params.get("user_inside_vp", None)   # True/False/None
    is_closed   = params.get("is_closed", False)
    demotion    = params.get("demotion", 0)             # int, computed from distances
    few_results = params.get("few_results", False)
    result_name = params.get("result_name", "").strip()
    result_addr = params.get("result_address", "").strip()
    result_cls  = params.get("classification", "").strip()
    official_name = params.get("official_name", "").strip()
    official_addr = params.get("official_address", "").strip()
    addr_does_not_exist = params.get("addr_does_not_exist", False)
    notes       = params.get("notes", "").strip()
    nearby_modifier = params.get("nearby_modifier", False)
    loc_modifier    = params.get("loc_modifier", False)   # chain + city/state modifier

    sections = []

    # ── 1. RELEVANCE ──────────────────────────────────────────────────────────
    rel_lines = []

    # Address queries (Specific / Non-specific / Non-existing)
    if qtype == "Specific Address":
        rel_lines.append(
            f"[Relevance- Navigational] The queried address points to a single location that can be "
            f"verified with the USPS. The result matches the queried address. According to Section 10.1, "
            f"Specific Address, when the query is an address and the user explicitly states their location "
            f"intent by including a locality, this is an explicit location query and the user's viewport "
            f"and location are irrelevant. The query refers to a unique location, so a result for this "
            f"exact location should be rated Navigational."
        )
    elif qtype == "Non-Specific Address":
        rel_lines.append(
            f"[Relevance- Acceptable] The query is for a non-specific or incomplete address "
            f"(missing street number or locality). According to Section 10.1, Specific Address — "
            f"example: 'Sugarloaf Key St.' — when the result is the queried street without a street "
            f"number, the relevance rating is Acceptable."
        )
    elif qtype == "Non-Existing Address":
        rel_lines.append(
            f"[Relevance- Excellent] The query is an address that does not exist. According to "
            f"Section 10.3, Query Address Does Not Exist, when research shows the full query address "
            f"does not exist and the result is the same address as the query address, the relevance "
            f"rating is Excellent. A Navigational rating cannot be applied to an address which does "
            f"not exist."
        )

    # Category query
    elif qtype == "Category Query":
        rel_label = _demotion_to_label(demotion)
        sub = " - Distance/Prominence Issue" if demotion > 0 else ""
        cls_lower = result_cls.lower()
        # Is result a sub-business inside the category target?
        cat_terms = ["mall", "shopping center", "plaza", "airport", "terminal",
                     "park", "complex", "center", "hospital"]
        possible_sub = any(t in query.lower() for t in cat_terms)
        if possible_sub and result_cls and not any(t in cls_lower for t in cat_terms):
            rel_lines.append(
                f"[Relevance- Bad - User Intent] This is a category query for a {query}. "
                f"The result is a {result_name}, located inside {query}, but users will have no way "
                f"of knowing this simply from looking at the result. This result does not satisfy "
                f"user intent and should be rated Bad. See the Sephora example in Section 10.7.8, "
                f"Clear Categories."
            )
        else:
            rel_lines.append(
                f"[Relevance- {rel_label}{sub}] This is a category query for a {query}. "
                f"The result matches the category query intent and is within the fresh viewport. "
                f"For more details on rating Category queries, see Section 10.7."
                + (f" This result fits the primary intent and is within the FVP; no demotion is required." if demotion == 0
                   else f" A -{demotion} demotion is applied for distance.")
            )

    # Locality query
    elif qtype == "Locality Query":
        cls_lower = result_cls.lower()
        transit_terms = ["station", "airport", "terminal", "transit", "subway", "metro", "train", "bus"]
        is_transit = any(t in cls_lower for t in transit_terms) or any(t in result_name.lower() for t in transit_terms)
        if is_transit:
            rel_label = _demotion_to_label(demotion)
            rel_lines.append(
                f"[Relevance- {rel_label} - User Intent] The query is for {query}, a locality. "
                f"The result is a transit POI associated with the queried locality, satisfying a "
                f"secondary transit intent. Per Section 5.14, Unexpected Results — see the "
                f"[san francisco] example — transit results within the queried locality qualify "
                f"for secondary intent."
                + (f" A -{demotion} demotion is applied for distance." if demotion > 0 else "")
            )
        else:
            rel_lines.append(
                f"[Relevance- Bad - User Intent] The query is for {query}, a locality. "
                f"The result is a POI located within or near the city; however, it does not fulfil "
                f"the secondary intent of the query, as it is neither internationally prominent nor "
                f"a transit POI. Per Section 5.14, Unexpected Results — see the [soho] example — "
                f"the Relevance rating should be Bad - User Intent Issue."
            )

    # Transit query
    elif qtype == "Transit Query":
        if demotion == 0:
            rel_lines.append(
                f"[Relevance- Navigational] The query is for {query}, a transit POI. "
                f"Research confirms there is only one station with a name that exactly matches "
                f"the query. As a singular, exact match, this result qualifies for a Navigational "
                f"rating. Per Section 5.16.1, Transit Queries — see the [Stockport Station] example."
            )
        elif demotion == 1:
            rel_lines.append(
                f"[Relevance- Good] The query is for {query}, a transit POI. Per Section 5.16.1, "
                f"Transit Queries — similar to the [Stockport Station] example — this station falls "
                f"just outside the requested locality in a neighbouring locality. It still provides "
                f"a relevant choice for the user. A -1 demotion is applied for distance."
            )
        elif demotion == 2:
            rel_lines.append(
                f"[Relevance- Acceptable] The query is for {query}, a transit POI. Per Section 5.16.1, "
                f"Transit Queries, this station is outside the requested locality. The fewer choices "
                f"available, the farther results can be and still be relevant. A -2 demotion is applied."
            )
        else:
            rel_lines.append(
                f"[Relevance- Excellent] The query is for {query}, a transit POI. Per Section 5.16.1, "
                f"when there is no station that perfectly matches the query name, each station within "
                f"the requested locality is Excellent. This result falls within the locality and "
                f"matches the intent."
            )

    # Chain + location modifier
    elif qtype == "Chain + Location Modifier":
        rel_label = _demotion_to_label(demotion)
        sub = " - Distance/Prominence Issue" if demotion > 0 else ""
        rel_lines.append(
            f"[Relevance- {rel_label}{sub}] The query is for a chain business with a general "
            f"location modifier. Per Section 10.6.3, Chain Business with Location Modifier, "
            f"user and viewport location should be ignored; results are expected within the "
            f"specified location modifier."
            + (f" This result is within the modifier; no demotion is required." if demotion == 0
               else f" This result is outside the specified location modifier. A -{demotion} demotion is applied for distance.")
        )

    # Service-level mismatch
    elif notes and any(kw in notes.lower() for kw in ["mismatch", "different brand", "competitor", "wrong brand"]):
        rel_lines.append(
            f"[Relevance- Bad - User Intent] Per Section 5.18, Service-Level Mismatch — "
            f"see the Burger King / McDonald's example — when the query is for a specific branded "
            f"POI, results are only expected to match that specific brand. Other brands offering "
            f"similar services are considered irrelevant. The result is a different brand than "
            f"the queried business."
        )

    # Default: Chain Business (with or without nearby modifier)
    else:
        rel_label = _demotion_to_label(demotion)
        sub = " - Distance/Prominence Issue" if demotion > 0 else ""
        rel_label_full = f"{rel_label}{sub}"

        if nearby_modifier:
            loc_rule = (
                f"According to Section 2.3.1 of the guidelines on Explicit Location, if the query "
                f"contains words like 'near me' or 'nearest,' the user's location — not the viewport "
                f"— should be considered the explicit location intent."
            )
        elif vp_status == "Stale":
            loc_rule = (
                f"The viewport is STALE. According to Section 2.3.2 of the guidelines on Implicit "
                f"Location, when the viewport is stale, consider only the user location as the "
                f"location intent."
            )
        elif user_inside is True:
            loc_rule = (
                f"The user is located inside the fresh viewport (FVP). According to Section 2.3.2 "
                f"of the guidelines on Implicit Location, when the user is inside the FVP, take "
                f"the user location as the location intent."
            )
        elif user_inside is False:
            loc_rule = (
                f"The user is located outside the fresh viewport (FVP). According to Section 2.3.2 "
                f"of the guidelines on Implicit Location, when the user is outside the FVP, results "
                f"are expected to be in or near the viewport area. All relevant results within the "
                f"viewport are eligible for an Excellent rating."
            )
        else:
            loc_rule = "The viewport and user location context applies per Section 2.3.2."

        if is_closed:
            closed_note = (
                f" Research shows this result is no longer operational. If you select the "
                f"\"Business/POI is closed or does not exist\" checkbox, you must still evaluate "
                f"the result Relevance as if the business/POI were operational. Avoid automatically "
                f"assigning a Bad rating. Refer to Section 4.2.2: Rating Relevance of "
                f"Closed/Non-existing Business/POI for guidance."
            )
        else:
            closed_note = ""

        if demotion == 0:
            demotion_note = " This result fits the primary intent and is within the FVP; no demotion is required."
        else:
            few_note = (
                f" Review Sections 5.7 and 5.8, Few Possible Results — leniency on distance is "
                f"acceptable when there are only a few possible results for the query in the area."
                if few_results else ""
            )
            demotion_note = (
                f" While this result fits the primary intent, research indicates that there is/are "
                f"closer {query} location(s) in the area. Therefore, a -{demotion} demotion is applied."
                f"{few_note}"
            )

        rel_lines.append(
            f"[Relevance- {rel_label_full}] The query is for {query}, a chain business. "
            f"{loc_rule}{demotion_note}{closed_note}"
        )

    sections.append("\n".join(rel_lines))

    # ── 2. NAME ───────────────────────────────────────────────────────────────
    # Skip Name/Address entirely for closed POIs
    if is_closed:
        sections.append(
            "[Name- N/A] Per Section 4.2.2, when the \"Business/POI is closed or does not exist\" "
            "checkbox is selected, Name, Address, and Pin do not need to be rated."
        )
    elif qtype in ("Specific Address", "Non-Specific Address", "Non-Existing Address", "Locality Query"):
        sections.append(
            "[Name- N/A] Per Section 6.1, Name Not Applicable (n/a), the N/A rating should be used "
            "for all address-type results, including residential addresses, streets, localities, and so on."
        )
    else:
        # Classification mismatch?
        cls_issue = detect_classification_issue(query, result_cls) if result_cls else None
        if cls_issue:
            sections.append(
                f"[Name- Incorrect - Incorrect Category] The business name matches the official "
                f"website; however, the classification \"{result_cls}\" does not accurately represent "
                f"this business. Per Section 6.3.2, Incorrect Category, when the business name is "
                f"correct but the category is not, the Name Accuracy is Incorrect."
            )
        elif official_name and official_name.lower() != result_name.lower():
            sections.append(
                f"[Name- Incorrect] The result name \"{result_name}\" does not match the name on "
                f"the official website (\"{official_name}\"). Per Section 6.2, the name must match "
                f"the official source."
            )
        else:
            sections.append(
                f"[Name- Correct] The name matches the name on the official website, and the "
                f"classification is correct."
            )

    # ── 3. ADDRESS ────────────────────────────────────────────────────────────
    if is_closed:
        pass  # already handled in Name block above; skip adding a duplicate
    elif qtype == "Non-Existing Address":
        sections.append(
            "[Address- Incorrect - Address Does Not Exist] The result address cannot be verified "
            "through street-level imagery, web-based resources, or the official postal service "
            "address verification tool. When attempting to confirm the address on USPS, it fails "
            "verification because the queried street number does not correspond to an existing "
            "address on the given street. Per Section 7.2, Address Does Not Exist."
        )
    elif qtype in ("Non-Specific Address",):
        sections.append(
            "[Address- Correct] The result address is accurate — the street is valid and exists "
            "within the specified locality. This can be verified through the USPS address tool."
        )
    elif qtype == "Transit Query":
        sections.append(
            f"[Address- Correct] Transit stations are POIs for which a full street address is not "
            f"required, even if one exists on the official website. The minimum required component "
            f"is the correct locality. Per Section 8.3.2.1, Minimum Address Component — see the "
            f"[Quincy Station] example."
        )
    elif addr_does_not_exist:
        sections.append(
            "[Address- Incorrect - Address Does Not Exist] The result address cannot be verified "
            "via the official postal service address verification tool or web-based resources. "
            "Per Section 7.2, Address Does Not Exist and the Country Specific Guidelines."
        )
    elif official_addr and official_addr.strip():
        diff_type = _address_diff_type(result_addr, official_addr)
        if diff_type is None:
            sections.append(
                f"[Address- Correct] The result address matches the official website "
                f"({official_addr})."
            )
        elif diff_type == "Street Number":
            sections.append(
                f"[Address- Incorrect - Street Number] The result address does not match the "
                f"official website. The street number listed ({result_addr.split()[0] if result_addr else '?'}) "
                f"is incorrect. Correct: {official_addr}. Per Section 7.1.1, Street Number."
            )
        elif diff_type == "Street Name":
            sections.append(
                f"[Address- Incorrect - Street Name] The listed address does not match the official "
                f"address. The result address street name or direction differs from the official "
                f"website ({official_addr}). USPS confirms the correct form. "
                f"Per Section 7.1.3, Street Name, subsection Street Directions and Types."
            )
        elif diff_type == "Unit/Apt":
            sections.append(
                f"[Address- Incorrect - Unit/Apt] The address does not match the official website. "
                f"The result address is missing or has an incorrect unit/suite number. "
                f"Correct: {official_addr}. Per Section 7.1.2, Unit/Apt."
            )
        else:
            sections.append(
                f"[Address- Incorrect] The result address does not match the official website. "
                f"Correct: {official_addr}."
            )
    else:
        sections.append(
            "[Address- Correct] The result address matches the official website."
        )

    # ── 4. PIN (placeholder — no map available) ───────────────────────────────
    if not is_closed and qtype not in ("Non-Existing Address",):
        sections.append(
            "[Pin- See map] Pin accuracy must be verified against street-level and aerial imagery. "
            "Per Section 9.4, Single Rooftop: pin on correct rooftop = Perfect; on same parcel = "
            "Approximate; adjacent same-block property = Next Door; wrong block or across street = Wrong."
        )
    elif qtype == "Non-Existing Address":
        sections.append(
            "[Pin- Can't Verify] Per Section 10.3, when an address does not exist, the Pin Accuracy "
            "is rated Can't Verify. There is no exact position for the pin to be placed."
        )

    # ── 5. Extra notes ────────────────────────────────────────────────────────
    if notes:
        sections.append(f"[Notes] {notes}")

    return "\n\n".join(sections)

# ─── Helper: resolve location input ──────────────────────────────────────────
def resolve_location(label: str, use_address: bool, address_val: str, lat_val, lon_val):
    """Returns (lat, lon, display) or (None, None, error_msg)."""
    if use_address and address_val.strip():
        with st.spinner(f"Geocoding {label}…"):
            result = geocode_address(address_val.strip())
        if result:
            return result[0], result[1], result[2]
        else:
            return None, None, f"Could not geocode: {address_val}"
    elif not use_address and lat_val is not None and lon_val is not None:
        return float(lat_val), float(lon_val), f"{lat_val:.6f}, {lon_val:.6f}"
    return None, None, "Not set"

# ─── Sidebar inputs ───────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🗺️ TELUS Maps Study Aid")
    st.divider()
    st.markdown("### 🔍 Query")
    query = st.text_input("Search query", placeholder="e.g. Taco Bell, Shell, mall")
    query_type = st.selectbox("Query type", [
        "Chain Business",
        "Chain + Nearby Modifier",
        "Chain + Location Modifier",
        "Category Query",
        "Specific Address",
        "Non-Specific Address",
        "Non-Existing Address",
        "Locality Query",
        "Transit Query",
    ])

    st.divider()
    st.markdown("### 📺 Viewport")
    viewport_status = st.radio("Viewport freshness", ["Fresh", "Stale"], horizontal=True)
    vp_mode = st.toggle("Enter viewport center as address", key="vp_mode")
    if vp_mode:
        vp_address = st.text_input("Viewport center address", key="vp_addr")
        vp_lat, vp_lon = None, None
    else:
        vp_address = ""
        c1, c2 = st.columns(2)
        vp_lat = c1.number_input("VP Lat", value=None, format="%.6f", key="vp_lat")
        vp_lon = c2.number_input("VP Lon", value=None, format="%.6f", key="vp_lon")

    st.divider()
    st.markdown("### 👤 User Location")
    user_mode = st.toggle("Enter user location as address", key="user_mode")
    if user_mode:
        user_address = st.text_input("User address", key="user_addr")
        user_lat, user_lon = None, None
    else:
        user_address = ""
        c1, c2 = st.columns(2)
        user_lat = c1.number_input("User Lat", value=None, format="%.6f", key="user_lat")
        user_lon = c2.number_input("User Lon", value=None, format="%.6f", key="user_lon")

    st.divider()
    st.markdown("### 📍 Result Pin(s)")
    num_results = st.number_input("Number of results", min_value=1, max_value=6, value=1, step=1)

    result_pins = []
    for i in range(int(num_results)):
        with st.expander(f"Result {i+1}", expanded=(i == 0)):
            r_name = st.text_input("Result name", key=f"r_name_{i}", placeholder="e.g. Taco Bell")
            r_addr = st.text_input("Result address (shown)", key=f"r_addr_{i}", placeholder="e.g. 123 Main St")
            r_class = st.text_input("Classification", key=f"r_class_{i}", placeholder="e.g. Fast Food Restaurant")
            r_mode = st.toggle("Enter as address", key=f"r_mode_{i}")
            if r_mode:
                r_geocode_addr = st.text_input("Geocode address", key=f"r_gc_{i}")
                r_lat, r_lon = None, None
            else:
                r_geocode_addr = ""
                cc1, cc2 = st.columns(2)
                r_lat = cc1.number_input("Lat", value=None, format="%.6f", key=f"r_lat_{i}")
                r_lon = cc2.number_input("Lon", value=None, format="%.6f", key=f"r_lon_{i}")
            r_closed = st.checkbox("Closed / does not exist", key=f"r_closed_{i}")
            r_official_name = st.text_input("Name on official site", key=f"r_oname_{i}", placeholder="Leave blank if same")
            r_official_addr = st.text_input("Address on official site", key=f"r_oaddr_{i}", placeholder="Leave blank if same")
            result_pins.append({
                "name": r_name, "address": r_addr, "classification": r_class,
                "mode": r_mode, "geocode_addr": r_geocode_addr,
                "lat": r_lat, "lon": r_lon,
                "closed": r_closed,
                "official_name": r_official_name,
                "official_address": r_official_addr,
            })

    st.divider()
    st.markdown("### 🧠 Blurb Parameters")

    user_inside_vp = st.radio(
        "User position relative to viewport",
        ["Inside FVP", "Outside FVP", "N/A (stale or explicit)"],
        horizontal=False,
    )
    user_inside_map = {"Inside FVP": True, "Outside FVP": False, "N/A (stale or explicit)": None}

    nearby_modifier = st.checkbox("Query contains 'nearby / near me / nearest'")
    loc_modifier    = st.checkbox("Query has a general location modifier (e.g. 'Walmart Tomball TX')")
    few_results     = st.checkbox("Few real-world results exist in the area (leniency applies)")
    addr_dne        = st.checkbox("Address does not exist per USPS")
    demotion        = st.number_input("Distance demotion (-0 / -1 / -2 / -3)", min_value=0, max_value=3, value=0, step=1)

    st.divider()
    st.markdown("### 📝 Extra Notes")
    extra_notes = st.text_area(
        "Additional notes (service mismatch, competitor, other flags)",
        placeholder="e.g. result is a competitor brand; 2 closer locations found on official site",
        height=80,
    )

    st.divider()
    generate_btn = st.button("⚡ Generate Context Blurb", type="primary", use_container_width=True)
    render_btn   = st.button("🗺️ Render Map", use_container_width=True)

# ─── Resolve all coordinates ──────────────────────────────────────────────────
resolved_vp   = resolve_location("viewport",      vp_mode,   vp_address,   vp_lat,   vp_lon)
resolved_user = resolve_location("user",           user_mode, user_address, user_lat, user_lon)

resolved_results = []
for i, r in enumerate(result_pins):
    lat, lon, disp = resolve_location(
        f"result {i+1}", r["mode"], r["geocode_addr"], r["lat"], r["lon"]
    )
    resolved_results.append({**r, "resolved_lat": lat, "resolved_lon": lon, "resolved_disp": disp})

# ─── Main content ─────────────────────────────────────────────────────────────
st.markdown("## 🗺️ TELUS Maps Analyst — Study Aid")

# ── Query / scenario header ──
if query:
    col_q, col_vp, col_qt = st.columns([2, 1, 1])
    with col_q:
        st.markdown(f"""
        <div class='card'>
            <div class='card-title'>Query</div>
            <span style='font-size:20px;font-weight:700;color:#f1f5f9'>"{query}"</span>
        </div>""", unsafe_allow_html=True)
    with col_vp:
        vp_color = "tag-green" if viewport_status == "Fresh" else "tag-amber"
        st.markdown(f"""
        <div class='card'>
            <div class='card-title'>Viewport</div>
            <span class='tag {vp_color}'>{viewport_status}</span>
        </div>""", unsafe_allow_html=True)
    with col_qt:
        st.markdown(f"""
        <div class='card'>
            <div class='card-title'>Query Type</div>
            <span class='tag tag-purple'>{query_type}</span>
        </div>""", unsafe_allow_html=True)

# ── Classification check ──
for i, r in enumerate(result_pins):
    if r["classification"] and query:
        issue = detect_classification_issue(query, r["classification"])
        if issue:
            st.markdown(f"<div class='warn-box'>⚠ Result {i+1} — {issue}</div>", unsafe_allow_html=True)

# ── Chain locator link ──
if query:
    locator_url, found = get_chain_locator(query)
    if found:
        st.markdown(f"""
        <div class='card'>
            <div class='card-title'>Official Chain Locator</div>
            <a href='{locator_url}' target='_blank' class='link-btn link-btn-primary'>
                🔗 {query.title()} — Official Store Locator
            </a>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class='card'>
            <div class='card-title'>Chain Locator — Not in database</div>
            <span style='font-size:12px;color:#64748b;margin-right:8px'>No direct URL found for "{query}".</span>
            <a href='{locator_url}' target='_blank' class='link-btn link-btn-warn'>
                🔍 Google Search: {query} store locator
            </a>
        </div>""", unsafe_allow_html=True)

# ── Map ──
map_col, info_col = st.columns([3, 2])

with map_col:
    st.markdown("### Map")

    # Determine map center
    center = [39.5, -98.35]  # US center default
    zoom = 4
    if resolved_vp[0] is not None:
        center = [resolved_vp[0], resolved_vp[1]]
        zoom = 11
    elif resolved_user[0] is not None:
        center = [resolved_user[0], resolved_user[1]]
        zoom = 12

    m = folium.Map(location=center, zoom_start=zoom, tiles="CartoDB dark_matter")

    # Viewport center marker (blue square)
    if resolved_vp[0] is not None:
        vp_color_map = "#3b82f6" if viewport_status == "Fresh" else "#f59e0b"
        folium.Marker(
            [resolved_vp[0], resolved_vp[1]],
            popup=f"Viewport Center<br>{resolved_vp[2]}",
            tooltip="📺 Viewport Center",
            icon=folium.Icon(color="blue" if viewport_status == "Fresh" else "orange",
                             icon="tv", prefix="fa")
        ).add_to(m)

    # User marker (green person)
    if resolved_user[0] is not None:
        folium.Marker(
            [resolved_user[0], resolved_user[1]],
            popup=f"User<br>{resolved_user[2]}",
            tooltip="👤 User Location",
            icon=folium.Icon(color="green", icon="user", prefix="fa")
        ).add_to(m)

    # Result pins
    pin_colors = ["red", "purple", "darkred", "cadetblue", "darkblue", "pink"]
    for i, r in enumerate(resolved_results):
        if r["resolved_lat"] is not None:
            popup_html = f"""
            <b>{r['name'] or f'Result {i+1}'}</b><br>
            {r['address'] or ''}<br>
            <i>{r['classification'] or ''}</i>
            {'<br><b style="color:red">⚠ CLOSED</b>' if r['closed'] else ''}
            """
            folium.Marker(
                [r["resolved_lat"], r["resolved_lon"]],
                popup=folium.Popup(popup_html, max_width=200),
                tooltip=f"📍 Result {i+1}: {r['name'] or 'unnamed'}",
                icon=folium.Icon(color=pin_colors[i % len(pin_colors)],
                                 icon="map-marker", prefix="fa")
            ).add_to(m)
            # Line from user to result
            if resolved_user[0] is not None:
                folium.PolyLine(
                    [[resolved_user[0], resolved_user[1]],
                     [r["resolved_lat"], r["resolved_lon"]]],
                    color=("#ef4444" if i == 0 else "#a78bfa"),
                    weight=1.5, opacity=0.5, dash_array="5"
                ).add_to(m)

    st_folium(m, width=None, height=480, returned_objects=[])

with info_col:
    st.markdown("### Distances & Links")

    # ── Distances ──
    for i, r in enumerate(resolved_results):
        with st.expander(f"📍 Result {i+1}: {r['name'] or 'Unnamed'}", expanded=True):
            if r["resolved_lat"] is not None:

                # Distance: user → result
                if resolved_user[0] is not None:
                    d_km  = haversine_km(resolved_user[0], resolved_user[1],
                                         r["resolved_lat"], r["resolved_lon"])
                    d_mi  = km_to_miles(d_km)
                    color_class = "dist-good" if d_mi < 2 else "dist-warn" if d_mi < 10 else "dist-bad"
                    st.markdown(f"**User → Result:** <span class='{color_class}'>{d_mi:.2f} mi ({d_km:.2f} km)</span>",
                                unsafe_allow_html=True)

                # Distance: viewport → result
                if resolved_vp[0] is not None:
                    dv_km = haversine_km(resolved_vp[0], resolved_vp[1],
                                         r["resolved_lat"], r["resolved_lon"])
                    dv_mi = km_to_miles(dv_km)
                    color_class = "dist-good" if dv_mi < 5 else "dist-warn" if dv_mi < 20 else "dist-bad"
                    st.markdown(f"**VP → Result:** <span class='{color_class}'>{dv_mi:.2f} mi ({dv_km:.2f} km)</span>",
                                unsafe_allow_html=True)

                # Closed badge
                if r["closed"]:
                    st.markdown("<span class='tag tag-red'>⚠ CLOSED / NON-EXISTENT</span>", unsafe_allow_html=True)

                # Classification check
                if r["classification"] and query:
                    issue = detect_classification_issue(query, r["classification"])
                    if issue:
                        st.markdown(f"<span class='tag tag-amber'>⚠ Classification mismatch</span>", unsafe_allow_html=True)

                # Official name/address diff
                if r["official_name"] and r["official_name"].strip() and r["official_name"].lower() != (r["name"] or "").lower():
                    st.markdown(f"**Name diff:** `{r['name']}` → official: `{r['official_name']}`")
                if r["official_address"] and r["official_address"].strip() and r["official_address"].lower() != (r["address"] or "").lower():
                    st.markdown(f"**Address diff:** `{r['address']}` → official: `{r['official_address']}`")

                st.divider()

                # Quick links
                gm_url = google_maps_link(r["resolved_lat"], r["resolved_lon"])
                usps_url = usps_link(r["address"] or "")

                st.markdown(f"""
                <a href='{gm_url}' target='_blank' class='link-btn link-btn-primary'>📍 Google Maps</a>
                <a href='{usps_url}' target='_blank' class='link-btn link-btn-green'>📮 USPS Verify</a>
                """, unsafe_allow_html=True)

                if r["address"]:
                    addr_gm = google_maps_address_link(r["address"])
                    st.markdown(f"<a href='{addr_gm}' target='_blank' class='link-btn'>🔍 Address in Maps</a>",
                                unsafe_allow_html=True)
            else:
                st.caption(f"No coordinates set. {r['resolved_disp']}")

    # ── User/VP quick links ──
    st.markdown("### Location Links")
    if resolved_user[0] is not None:
        st.markdown(f"<a href='{google_maps_link(resolved_user[0], resolved_user[1])}' target='_blank' class='link-btn'>👤 User in Maps</a>", unsafe_allow_html=True)
    if resolved_vp[0] is not None:
        st.markdown(f"<a href='{google_maps_link(resolved_vp[0], resolved_vp[1])}' target='_blank' class='link-btn'>📺 Viewport in Maps</a>", unsafe_allow_html=True)

# ── Distance summary if multiple results ──
if len([r for r in resolved_results if r["resolved_lat"]]) > 1 and resolved_user[0] is not None:
    st.markdown("### 📊 Distance Summary (User → Results, sorted)")
    distances = []
    for i, r in enumerate(resolved_results):
        if r["resolved_lat"] is not None:
            d_mi = km_to_miles(haversine_km(resolved_user[0], resolved_user[1],
                                             r["resolved_lat"], r["resolved_lon"]))
            distances.append((i+1, r["name"] or f"Result {i+1}", d_mi))
    distances.sort(key=lambda x: x[2])
    for rank, (ri, name, d) in enumerate(distances):
        color = "#22c55e" if rank == 0 else "#f59e0b" if rank == 1 else "#f87171"
        penalty = "" if rank == 0 else f" → -{rank} demotion suggested"
        st.markdown(
            f"<span style='color:{color}'>#{rank+1}</span> &nbsp; **Result {ri}** ({name}) — "
            f"<span style='color:{color}'>{d:.2f} mi</span>"
            f"<span style='color:#64748b;font-size:12px'>{penalty}</span>",
            unsafe_allow_html=True
        )

# ── Context Blurb ──
st.markdown("---")
st.markdown("### 📋 Context Blurb")

if generate_btn:
    if not query:
        st.error("Please enter a search query in the sidebar.")
    else:
        r0 = resolved_results[0] if resolved_results else {}
        params = {
            "query":            query,
            "query_type":       query_type,
            "viewport_status":  viewport_status,
            "user_inside_vp":   user_inside_map.get(user_inside_vp),
            "nearby_modifier":  nearby_modifier,
            "loc_modifier":     loc_modifier,
            "few_results":      few_results,
            "addr_does_not_exist": addr_dne,
            "demotion":         int(demotion),
            "result_name":      r0.get("name", ""),
            "result_address":   r0.get("address", ""),
            "classification":   r0.get("classification", ""),
            "is_closed":        r0.get("closed", False),
            "official_name":    r0.get("official_name", ""),
            "official_address": r0.get("official_address", ""),
            "notes":            extra_notes,
        }
        blurb = generate_blurb_local(params)
        st.session_state["blurb"] = blurb

if "blurb" in st.session_state and st.session_state["blurb"]:
    st.markdown(
        f"<div class='blurb-box'>{st.session_state['blurb']}</div>",
        unsafe_allow_html=True,
    )
    st.caption("Select all text in the box above to copy it.")
else:
    st.markdown(
        "<div style='color:#4b5563;font-size:13px'>Fill in the sidebar fields and click "
        "<b>⚡ Generate Context Blurb</b>.</div>",
        unsafe_allow_html=True,
    )

# ─── Footer ──────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style='font-size:11px;color:#374151;text-align:center'>
TELUS Maps Study Aid · For exam preparation use only ·
<a href='https://tools.usps.com/zip-code-lookup.htm?byaddress' target='_blank' style='color:#475569'>USPS Address Verify</a> ·
<a href='https://maps.google.com' target='_blank' style='color:#475569'>Google Maps</a>
</div>
""", unsafe_allow_html=True)
