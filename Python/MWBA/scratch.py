from utility import print_by_line


fredericton_freeze_raw = """
4. Megan Arseneault (Lakehead, UNB)
5. Rahshida Atkinson (UToronto)
6. Leah Bowers (UNB)
7. Bailey Black (UNB)
8. Katie Daley (UNB)
9. Robbi Daley (Dalhousie, Saint Mary’s)
10. Ashley Bawn (St. Thomas)
11. Katie McAffee (Acadia, UNB)*
12. Nicole Esson (UNB)
14. Grace Simpson (UNB)
15. Eva Tumwine (UNB)
21. Torrie Janes (Saint Mary’s, Mount Allison)*
31. Mackenzie Legere (Mount Allison)
35. Katelyn Mangold (UNB)
44. Kylee Speedy (UNB)*
51. Emily MacLeod (Acadia, UNB)
55. Jill Durling (UNB)"""

moncton_mystics_raw = """
2. Maddy Daley (Crandall)
3. Anne-Marie Poitras (Montmorency)
4. Kelsey McLaughlin (Saint Mary’s)
5. Lindy MacDonald (St. Thomas, Holland College)
6. Maddie Greatorex (Mount Allison)*
7. Kelly Vass (St. Thomas, Crandall)
9. Jenna Jones (UPEI)
10. Maddy Maillet (Dalhousie)*
12. Shannon Youden (Saint Mary’s)
14. Erika Traikor (Acadia)
13. Sarah West ()
15. Emile Turmel (Ste-Foy)
16. Abby Miller (Mount Allison)*"""

port_city_fog_raw = """
2. Emily Shiels()
4. Abby Ring-Dineen (UNBSJ)*
5. Courtney Thompson (Dalhousie)
6. Bailey Henderson (UNBSJ)*
7. Rachel Farwell (Toronto Metropolitan)*
8. Megan Stewart (York)
9. Reese Baxendale (UPEI)
10. Emily Briggs (Crandall)*
11. Janelle Haddad (Bishop’s)
12. Lauren Fleming (UPEI)
13. Lauren Harris (UPEI)*
14. Kaylee Kilpatrick (New Hampshire, Weiderstadt)
15. Emily Thomas ()
16. Amelia Mitchell (Mount Allison)*
21. Emily Fitzpatrick (UNBSJ)"""

windsor_edge_raw = """
3. Jodi Whyte (UOttawa)
4. Sydney Foran (McGill)*
5. Jessica Miller (St. FX)
7. Cassandra McCormick (MEBL)
8. Meghan Keoughan (Crandall)
9. Tiffany Reynolds (Lakehead)
10. Karissa Kajorinne (Algoma, Lakehead)
11. Chelsea Slawter-Wright (Dalhousie)
12. Lisa Edwards (Holland College)
13. Emily MacNeil (Bishop’s)
14. Karla Yepez (UPEI)
15. Christina Garon (MEBL)
16. Anna von Maltzahan (Dalhousie)
17. Carolina Del Santo (UPEI)"""

halifax_hornets_raw = """
5 Jaylnn Skier (Cape Breton)
6. Alaina McMillan (Saint Mary’s)*
7. Chanel Smith (Acadia)
8. Jayla Verney (Holland College)
9. Aliyah Fraser (St. FX)
10. Katherine Khorovets (Mount St. Vincent)*
12. Alisha McNeil (Mount St. Vincent)*
13. Arianna Macias (Saint Mary’s)
14. Lucina Beaumont (Saint Mary’s)*
15. Katherine Follis (UOttawa)
20. Cailin Crosby (Dalhousie)
21. Clara Gascoigne (Saint Mary’s)*
22. Madison Munro (Cape Breton)
23. Leah Martin (Dalhousie)
24. Hannah Brown (Cape Breton)
25. Jasmine Parent (Acadia)"""

halifax_thunder_raw = """
1. Ellen Hatt (Acadia)
2. Haley McDonald (Acadia, Germany)
3. Gemma Bullard (Queen’s)
4. Leslie Hawco (Memorial)
5. Justine Colley-Leger (Saint Mary’s)
7. Vanessa Pickard (St. FX, McMaster)
8. Katherine Quackenbush (Memorial)
9. Jayda Veinot (Acadia)*
10. Melina Collins (St. FX)*
11. Abby Duinker (Acadia)
13. Marley Curwin (UNB)*
14. Grace Wade (UNB)
15. Laura Langille (Saint Mary’s)
22. Elizabeth Beals-Iseyemi (Acadia)*"""


teams_list = [
    "Fredericton Freeze",
    "Port City Fog",
    "Moncton Mystics",
    "Windsor Edge",
    "Halifax Hornets",
    "Halifax Thunder"
]


def collect_affiliations(raw, rec=False):
    if isinstance(raw, list):
        ttls = set()
        for r in raw:
            ttls = ttls.union(collect_affiliations(r, rec=True))
        affiliations = list(ttls)
        affiliations.sort()
        return affiliations
    else:
        y = [l for l in raw.split("\n") if l]
        ga = lambda p: [l.strip() for l in p.replace('*', '').replace(')', '').split('(')[1].split(',')]
        affiliations = set()
        lst = [ga(p) for p in y]
        for l in lst:
            for a in l:
                if a:
                    affiliations.add(a)
        affiliations.add('')
        if not rec:
            affiliations = list(affiliations)
            affiliations.sort()
        return affiliations


def collect_sql_players(raw):
    if not isinstance(raw, dict):
        raise TypeError(f"Param 'raw' needs to be a dict, got: {type(raw)}")
    affiliations = collect_affiliations(list(raw.values()))
    print(f"RAW A <{raw}>")
    for k, v in raw.items():
        print(f"v: <{v}>")
        if isinstance(v, str):
            raw[k] = v.split("\n")
        # for r in raw[k]:
        #     if all([isinstance(r, str) for r in raw]):
        #         for i, r in enumerate(raw[k]):
        #             raw[k][i] = r.split("\n")

    # if all([isinstance(r, str) for r in raw]):
    #     for i, r in enumerate(raw):
    #         raw[i] = r.split("\n")
    print(f"RAW B <{raw}>")
    result = ""
    for team_key, roster in raw.items():
        for player in roster:
            if not player:
                continue
            print(f"p: {player}")
            name = " ".join(player.split(' ')[1:3])
            affiliation = player.replace('*', '').replace(')', '').split('(')[1].split(',')[-1].strip()
            affiliations_ar = ";".join([str(affiliations.index(a.strip()) + 1) for a in player.replace('*', '').replace(')', '').split('(')[1].split(',')])
            team = teams_list.index(team_key) + 1
            teams_ar = f"{teams_list.index(team_key) + 1}"
            number = int(player.split(' ')[0].replace(".", ""))
            numbers_ar = f"{int(player.split(' ')[0].replace('.', ''))}"
            result += "('{NAME}', {AFFILIATION}, '{AFFILIATIONSAR}', {TEAM}, '{TEAMSAR}', 1, {NUMBER}, '{NUMBERSAR}'),\n".format(
                NAME=name,
                AFFILIATION=affiliations.index(affiliation),
                AFFILIATIONSAR=affiliations_ar,
                TEAM=team,
                TEAMSAR=teams_ar,
                NUMBER=number,
                NUMBERSAR=numbers_ar
            )
    return result[:-2]


if __name__ == "__main__":
    raw = [
        fredericton_freeze_raw,
        port_city_fog_raw,
        moncton_mystics_raw,
        windsor_edge_raw,
        halifax_hornets_raw,
        halifax_thunder_raw
    ]
    affiliations = collect_affiliations(raw)
    print(f"result: {affiliations}")
    print_by_line(affiliations)

    print("Roster:")
    players = collect_sql_players(dict(zip(teams_list, raw)))
    print(players)
