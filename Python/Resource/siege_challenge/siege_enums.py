import enum


class GameMode(enum.Enum):
    CASUAL = "Casual"
    RANKED = "Ranked"


class TypeMode(enum.Enum):
    BOMB = "Bomb"
    SECURE = "Secure Area"
    HOSTAGE = "Hostage"


class PlayMode(enum.Enum):
    ATTACK = "Attack"
    DEFENCE = "Defence"
