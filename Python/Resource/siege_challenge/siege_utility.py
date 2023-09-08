from siege_enums import *


def siege_acronym(val):

    match val:
        case PlayMode.ATTACK:
            return "ATK"
        case PlayMode.DEFENCE:
            return "DEF"
        case GameMode.RANKED:
            return "RNK"
        case GameMode.CASUAL:
            return "CAS"
        case _:
            raise ValueError(f"Unknown Siege value. Cannot find acronym for '{val}'")
