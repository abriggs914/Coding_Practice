import datetime

from siege_challenge.siege_enums import GameMode, TypeMode, PlayMode
from siege_challenge.siege_map import Map, MapLocation


class Round:

    def __init__(self, number: int, play_mode: PlayMode, location: MapLocation):
        self.play_mode = play_mode
        self.number = number  # use zero-index
        self.location = location

    def __repr__(self):
        pm = siege_acronym(self.play_mode)
        return f"<Round #{self.number} {pm} '{self.location.name}'>"


class Game:

    def __init__(self, game_map: Map, game_mode: GameMode, type_mode: TypeMode, date=None):
        self.game_map = game_map
        self.game_mode = game_mode
        self.type_mode = type_mode
        self.date = date if (date is not None and isinstance(date, datetime.datetime)) else datetime.datetime.now()
