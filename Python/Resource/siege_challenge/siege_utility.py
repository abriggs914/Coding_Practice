from siege_challenge.siege_enums import *


def siege_acronym(val):

    db = {
        PlayMode.ATTACK: "ATK",
        PlayMode.DEFENCE: "DEF",
        GameMode.RANKED: "RNK"
        GameMode.CASUAL: "CAS",
        TypeMode.SECURE: "SEC",
        TypeMode.HOSTAGE: "HOS",
        TypeMode.BOMB: "BMB"
    }
    db_rev = {v: k for k, v in db.items()}

    if len(db) != len(db_rev):
        raise ValueError("Error all values must map 1:1 in the db. If a value does not have a unique key, then cannot perform reverse look-ups.")

    if val in db:
        return db[val]
    elif val in db_rev:
        return db_rev[val]
    else:
        raise ValueError(f"Unknown Siege value. Cannot find acronym for '{val}'")
