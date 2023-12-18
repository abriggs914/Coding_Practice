import datetime

import requests

HOST_NAME = f"https://api-web.nhle.com"


def query_url(url, do_print=False) -> dict | None:
    if do_print:
        print(f"{url=}")
    response = requests.get(url)
    response.raise_for_status()  # raises exception when not a 2xx response
    if response.status_code != 204:
        ct = response.headers["Content-Type"].lower()
        if ct.startswith("application/json"):
            return response.json()
        elif ct.startswith("text/javascript"):
            return eval(response.text.replace("jsonFeed(", "")[:-2])


def get_calendar_schedule(date: datetime.date, do_print=False) -> dict | None:
    url = f"{HOST_NAME}/v1/schedule-calendar/{date:%Y-%m-%d}"
    if do_print:
        print(f"{url=}")
    # schedule keys
    # ['endDate', 'nextStartDate', 'previousStartDate', 'startDate', 'teams']
    # teams list keys
    # ['id', 'seasonId', 'commonName', 'abbrev', 'name', 'placeName', 'logo', 'darkLogo', 'isNhl', 'french']
    return query_url(url)


def get_schedule(date: datetime.date, do_print=False) -> dict | None:
    """Get 1 week's schedule of games"""
    url = f"{HOST_NAME}/v1/schedule/{date:%Y-%m-%d}"
    if do_print:
        print(f"{url=}")
    # schedule keys
    # ['nextStartDate', 'previousStartDate', 'gameWeek', 'oddsPartners', 'preSeasonStartDate', 'regularSeasonStartDate', 'regularSeasonEndDate', 'playoffEndDate', 'numberOfGames']
    return query_url(url)


def get_geolocation(do_print=False) -> dict | None:
    url = "https://geolocation.onetrust.com/cookieconsentpub/v1/geo/location"
    if do_print:
        print(f"{url=}")
    return query_url(url)


def get_country(do_print=False) -> dict | None:
    url = f"{HOST_NAME}/v1/location"
    if do_print:
        print(f"{url=}")
    return query_url(url)


def get_score(date: datetime.date, do_print=False) -> dict | None:
    """Get scores for a particular date"""
    # score keys:
    # ['prevDate', 'currentDate', 'nextDate', 'gameWeek', 'oddsPartners', 'games']
    url = f"{HOST_NAME}/v1/score/{date:%Y-%m-%d}"
    if do_print:
        print(f"{url=}")
    return query_url(url)


def get_standings(date: datetime.date, do_print=False) -> dict | None:
    """Get standings up to a particular date"""
    # standings keys:
    # ['wildCardIndicator', 'standings']
    url = f"{HOST_NAME}/v1/standings/{date:%Y-%m-%d}"
    if do_print:
        print(f"{url=}")
    return query_url(url)


if __name__ == '__main__':
    today = datetime.datetime.today()
    games_today = get_calendar_schedule(today)
    print(f"{games_today=}")
