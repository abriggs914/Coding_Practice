import datetime

import requests

HOST_NAME = f"https://api-web.nhle.com"


def get_calendar_schedule(date: datetime.date):
    url = f"{HOST_NAME}/v1/schedule-calendar/{date:%Y-%m-%d}"
    print(f"{url=}")
    # schedule keys
    # ['endDate', 'nextStartDate', 'previousStartDate', 'startDate', 'teams']
    # teams list keys
    # ['id', 'seasonId', 'commonName', 'abbrev', 'name', 'placeName', 'logo', 'darkLogo', 'isNhl', 'french']
    return requests.get(url).json()


def get_schedule(date: datetime.date):
    url = f"{HOST_NAME}/v1/schedule/{date:%Y-%m-%d}"
    print(f"{url=}")
    # schedule keys
    # ['nextStartDate', 'previousStartDate', 'gameWeek', 'oddsPartners', 'preSeasonStartDate', 'regularSeasonStartDate', 'regularSeasonEndDate', 'playoffEndDate', 'numberOfGames']
    # teams list keys
    # ['id', 'seasonId', 'commonName', 'abbrev', 'name', 'placeName', 'logo', 'darkLogo', 'isNhl', 'french']
    return requests.get(url).json()


def get_geolocation():
    url = "https://geolocation.onetrust.com/cookieconsentpub/v1/geo/location"
    return requests.get(url).json()


if __name__ == '__main__':
    today = datetime.datetime.today()
    games_today = get_calendar_schedule(today)
    print(f"{games_today=}")
