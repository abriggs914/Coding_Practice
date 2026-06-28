
import json
import os
import datetime
from typing import Any
import requests
import dataclasses

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from streamlit_utility import display_df, display_df_paginated


def attr_map(obj: Any, data: dict):
    for k, v in data.items():
        if isinstance(v, (bool, str, int, float, list)):
            setattr(obj, k, v)
        elif isinstance(v, dict):
            for k_, v_ in v.items():
                setattr(obj, f"{k}_{k_}", v_)
            

@dataclasses.dataclass
class Pokedex:
    def __init__(self, data):
        self.data = data
        self.name = data.get("name")
        self.id = data.get("id")
        self.pokemon_entries = {p_dat.get("entry_number"): p_dat.get("pokemon_species", {}).get("name") for p_dat in data.get("pokemon_entries", {})}
        self.df = pd.DataFrame([
            {
                "number": p["entry_number"],
                "name": p["pokemon_species"]["name"],
                "url": p["pokemon_species"]["url"]
            }
            for p in self.data.get("pokemon_entries", [])
        ])
        combined = False
        
    def __add__(self, other):
        a_data = self.data.copy()
        for k in list(a_data.keys()):
            a_data[f"{k}_0"] = a_data[k]
            del a_data[k]
        b_data = other.data.copy()
        for k in list(b_data.keys()):
            b_data[f"{k}_0"] = b_data[k]
            del b_data[k]
        a_data.update(b_data)
        
        a_name, b_name = self.name, other.name
        a_id, b_id = self.id, other.id
        a_df, b_df = self.df.copy(), other.df.copy()
        
        a_pe = self.pokemon_entries.copy()
        b_pe = other.pokemon_entries.copy()
        a_pe.update(b_pe)
        
        a_df["pokedex"] = a_id
        b_df["pokedex"] = b_id
        
        df = pd.concat([a_df, b_df], ignore_index=True)
        
        d = Pokedex({})
        d.name = f"Dex({a_name} + {b_name})"
        d.id = f"Dex({a_id} + {b_id})"
        d.data = a_data
        d.df = df.copy()
        d.combined = True
        return d


@dataclasses.dataclass
class Generation:
    def __init__(self, data):
        self.data = data
        self.name = [d["name"] for d in data["names"] if d["language"]["name"] == "en"][0]
        self.pokemon_species = data["pokemon_species"]
        
        
@dataclasses.dataclass
class Type:
    def __init__(self, data):
        self.data = data
        # st.write(data)
        self.double_damage_from = data["damage_relations"]["double_damage_from"]
        self.double_damage_to = data["damage_relations"]["double_damage_to"]
        self.half_damage_from = data["damage_relations"]["half_damage_from"]
        self.half_damage_to = data["damage_relations"]["half_damage_to"]
        self.no_damage_from = data["damage_relations"]["no_damage_from"]
        self.no_damage_to = data["damage_relations"]["no_damage_to"]
        self.game_indices = data["game_indices"]
        self.damage_class = data.get("move_damage_class")
        if self.damage_class:
            self.damage_class = self.damage_class.get("name", data["move_damage_class"])
        self.name = data["name"]
        self.moves = data["moves"]
        self.pokemon = data["pokemon"]
        self.sprites = data["sprites"]
        self.first_name_icon = self.get_first_sprite("name", "first")
        self.last_name_icon = self.get_first_sprite("name", "last")
        self.first_symbol_icon = self.get_first_sprite("symbol", "first")
        self.last_symbol_icon = self.get_first_sprite("symbol", "last")

    def get_first_sprite(self, mode, pos):
        # st.divider()
        # st.write(f"{mode=}, {pos=}")
        keys = list(self.sprites.keys())
        def gn(gen_str):
            # st.write(f"{gen_str=}, {'-' in gen_str}")
            return ROMAN.index(gen_str.split("-")[-1]) + 1
        def get_sprite(gen_data):
            # st.write(f"{gen_data=}")
            games_lst = list(self.sprites[gen_data].keys())
            # st.write("games_lst")
            # st.write(games_lst)
            # st.write(self.sprites[gen_data])
            if mode == "first":
                return self.sprites[gen_data][games_lst[0]]["name_icon" if (mode == "name") else "symbol_icon"]
            else:
                return self.sprites[gen_data][games_lst[-1]]["name_icon" if (mode == "name") else "symbol_icon"]
            
        gens = [(g, gn(g)) for g in self.sprites]
        gens.sort(key=lambda t: t[1])
        # st.write(gens)
        # st.write("gens[0]")
        # st.write(gens[0 if (pos == "first") else -1][0])
        return get_sprite(gens[0 if (pos == "first") else -1][0])
    
    def get_generation_sprite(self, generation: str, game: str = None, mode: str = "name"):
        if game is None:
            games_lst = list(self.sprites[generation].keys()) 
        else:
            games_lst = [game]
        return self.sprites[generation][games_lst[0]][f"{'name' if mode == 'name' else 'symbol'}_icon"]
    
    def __repr__(self) -> str:
        return f"Type({self.name})"


@dataclasses.dataclass
class PokemonSpecies:
    def __init__(self, p_data):
        self.p_data = p_data
        attr_map(self, p_data)


@dataclasses.dataclass
class Pokemon:
    def __init__(self, p_data):
        data = {
            "id": p_data["id"],
            "name": p_data["name"],
            "types": [t["type"]["name"] for t in p_data["types"]],
            "sprite": p_data["sprites"]["front_default"],
            "official_artwork": p_data["sprites"]["other"]["official-artwork"]["front_default"],
        }
        self.raw = p_data
        self.data = data
        self.id = data["id"]
        self.name = data["name"]
        self.types = data["types"]
        self.sprite = data["sprite"]
        self.artwork = data["official_artwork"]
        # st.write(p_data)
        
    def card(self):
        with st.container(horizontal=True):
            st.image(self.artwork, self.name)
            with st.container():
                # st.write(self.types)
                # tm = " ".join([TYPE_IMAGES[t] for t in self.types])
                # st.write(tm)
                # img = [t for t in types if t.name in self.types]
                for t in self.types:
                    t_: Type = types.get(t)
                    if t_ is not None:
                        img = t_.last_name_icon
                        st.image(img)
                    else:
                        st.write(t) 
                        
    def __eq__(self, other):
        return all([self.name == other.name, self.id == other.id])
    
    def __repr__(self) -> str:
        return f"Pokemon(#{self.id}, {self.name})"


@dataclasses.dataclass
class Game:
    def __init__(self, data):
        self.data = data
        self.generation = data["generation"]["name"]
        self.move_learn_methods = data["move_learn_methods"]
        self.name = data["name"]
        self.order = data["order"]
        self.pokedexes = [d["name"] for d in data["pokedexes"]]
        self.regions = [d["name"] for d in data["regions"]]
        self.versions = [d["name"] for d in data["versions"]]
        
    def get_pokedex(self):
        for i, dat in enumerate(self.pokedexes):
            dex = Pokedex(get_json(self.data["pokedexes"][i]["url"]))
            return dex
        
        
    def __repr__(self):
        return f"Game(#{self.order}, {self.name})"


@st.cache_data
def load_data(sheet=0):
    dfs = pd.read_excel("data.xlsx", header=None, sheet_name=None)
    sheets = list(dfs)
    df = dfs[sheets[sheet]]
    df.columns = ["A"]
    vals = df["A"].values.tolist()
    res = []
    i = 0
    for i, v in enumerate(vals):
        if any([pd.isna(v), v in [0, 1]]):
            res.append(v)
    if i < len(vals):
        lv = vals[i]
        valid = lv == len(res)
    if not valid:
        st.error("Number of pokemon found does not match total rows")
    return res


ROMAN = ["i", "ii", "iii", "iv", "v", "vi", "vii", "viii", "ix", "x"]
BASE = "https://pokeapi.co/api/v2"
TYPE_IMAGES = {
    "electric": ":zap:",
    "fire": ":fire:",
    "water": ":droplet:",
    "ice": ":snowflake:",
    "poison": ":biohazard:",
    "fighting": ":anger:",
    "dragon": ":dragon_face:"
}
DEFAULT_GAME = "brilliant-diamond-shining-pearl"
LINK_POKEBALL = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/items/poke-ball.png"

def get_json(url):
    r = requests.get(url, timeout=20)
    # st.write(f"{datetime.datetime.now():%y-%m-%d %H:%M:%S} {url=}")
    r.raise_for_status()
    return r.json()


def get_pokemon_id(name_or_id):
    pids = st.session_state.setdefault("k_pids", {})
    for name, id_ in pids.items():
        if (id_ == name_or_id) or (name == name_or_id):
            return id_


@st.cache_data
def get_pokemon(name_or_id):
    id_ = get_pokemon_id(name_or_id)
    if id_ is None:
        p = Pokemon(get_json(f"{BASE}/pokemon/{name_or_id}"))
    else:
        p = Pokemon(get_json(f"{BASE}/pokemon/{id_}"))
        
    try:
        id_, name = p.id, p.name
        pids = st.session_state.setdefault("k_pids", {})
        pids.setdefault[name] = id_
        st.session_state.update({"k_pids": pids})
    except Exception as e:
        pass
    
    return p


@st.cache_data
def get_pokemon_species(name_or_id):
    id_ = get_pokemon_id(name_or_id)
    if id_ is None:
        p = PokemonSpecies(get_json(f"{BASE}/pokemon-species/{name_or_id}"))
    else:
        p = PokemonSpecies(get_json(f"{BASE}/pokemon-species/{id_}"))
        
    try:
        id_, name = p.id, p.name
        pids = st.session_state.setdefault("k_pids", {})
        pids.setdefault[name] = id_
        st.session_state.update({"k_pids": pids})
    except Exception as e:
        pass
    
    return p


@st.cache_data
def get_species(name_or_id):
    return get_json(f"{BASE}/pokemon-species/{name_or_id}")


@st.cache_data
def get_evolution_chain(name_or_id):
    species = get_species(name_or_id)
    return get_json(species["evolution_chain"]["url"])


@st.cache_data
def get_generation(gen_id):
    return get_json(f"{BASE}/generation/{gen_id}")


@st.cache_data
def get_pokedex(pokedex_id=1):
    """By default pokedex 1 includes ALL known pokemon from ALL generations."""
    return Pokedex(get_json(f"{BASE}/pokedex/{pokedex_id}"))


@st.cache_data
def get_type(type_id):
    return get_json(f"{BASE}/type/{type_id}")


@st.cache_data
def get_game(type_id):
    return get_json(f"{BASE}/version-group/{type_id}")


@st.cache_data
def gather_types():
    types = {}
    with st.container(horizontal=True):
        for i in range(1, 40):
            # st.write(f"{i=}, {len(types)=}")
            try:
                t = get_type(i)
                if t:
                    t = Type(t)
                    # if t.name:
                    types[t.name] = t
                    # # st.write(f"Name={t.name}")
                    # img = t.last_name_icon
                    # if img:
                    #     st.image(img, width=200)
            except Exception as e:
                pass
                # if i > 0:
                #     st.error(e)
                #     raise e            
    return types


@st.cache_data
def gather_games():
    games = {}
    with st.container(horizontal=True):
        for i in range(1, 50):
            st.write(f"{i=}, {len(games)=}")
            try:
                g = get_game(i)
                if g:
                    g = Game(g)
                    # if t.name:
                    games[g.name] = g
                    st.write(f"Name={g.name}")
                    # img = t.last_name_icon
                    # if img:
                    #     st.image(img, width=200)
            except Exception as e:
                pass
                # if i > 0:
                #     st.error(e)
                #     raise e            
    return games

# t18 = get_type(18)
# t18 = Type(t18)
# st.write(t18.name)
# st.write(t18)

# national_dex = get_pokedex()
# display_df(national_dex.df, "National")

# dexes = {}
# for i in range(5, 1, -1):
#     dexes[i] = get_pokedex(i)
#     display_df(dexes[i].df, f"Dex{i}")
    
# d2 = dexes[2]
# d3 = dexes[3]
# st.write(d2.name)
# st.write(d3.name)

# d23 = d2 + d3
# df23 = d23.df
# df23.sort_values("name", inplace=True)
# st.write(d23.name)
# display_df(df23, f"Dex23")

# st.stop()

# =====================================================================================
# =====================================================================================
# =====================================================================================

pika = get_pokemon("pikachu")
st.set_page_config(layout="wide", page_icon=pika.artwork, page_title="Pokedex")

# Pokemon Shining Pearl Dex Data
radio_sheet = st.radio("Sheet #", [0, 1, 2])
data = load_data(sheet=radio_sheet)
ids_missed = [i+1 for i, v in enumerate(data) if pd.isna(v)]
ids_seen = [i+1 for i, v in enumerate(data) if v == 0]
ids_caught = [i+1 for i, v in enumerate(data) if v == 1]
ids_all = sorted(ids_missed + ids_seen + ids_caught)
df_pies = []
with st.container(horizontal=True):
    for n, lst in [
        ("All", data),
        ("Missed", ids_missed),
        ("Seen", ids_seen),
        ("Caught", ids_caught),
    ]:
        with st.container():
            if n == "All":
                st.metric(n, len(lst), height=120)
            else:
                p_all = len(lst) / len(data)
                p_all = f"{p_all*100:.2f} %"
                st.metric(n, len(lst), delta=p_all, delta_arrow="off", height=120)
                df_pies.append(pd.DataFrame([{"category": n, "val": len(lst)}]))
                
            with st.container(height=400, border=False):
                with st.expander("data"):
                    st.write(lst)

df_pies = pd.concat(df_pies, ignore_index=True)
display_df(df_pies, f"{DEFAULT_GAME} DF")

# =====================================================================================
# =====================================================================================
# =====================================================================================

games = gather_games()
types: dict[str: Type] = gather_types()

st.write(games)
st.write(types)

k_selectbox_game = "key_selectbox_game"
st.session_state.setdefault(k_selectbox_game, DEFAULT_GAME)
selectbox_game = st.selectbox(
    label="Game:",
    options=sorted(list(games.keys()), key=lambda g: games[g].order),
    key=k_selectbox_game
)

if selectbox_game:
    sel_game: Game = [games[g] for g in games if g == selectbox_game][0]
    sel_generation = sel_game.generation
    pokedex = sel_game.get_pokedex()
    national_pokedex = get_pokedex()
    st.write(sel_game)
    st.write(sel_generation)
    display_df(pokedex.df, f"{sel_game.name} Pokedex")
    display_df(national_pokedex.df, f"National Pokedex")
    
    df_pokemon = national_pokedex.df.copy()
    df_pokemon = df_pokemon[df_pokemon["number"].isin(ids_all)]
    df_pokemon = df_pokemon.merge(
        pokedex.df,
        on="name",
        suffixes=["_national", ""],
        how="left"
    )
    df_pokemon["missed"] = df_pokemon["number_national"].isin(ids_missed)
    df_pokemon["seen"] = df_pokemon["number_national"].isin(ids_seen)
    df_pokemon["caught"] = df_pokemon["number_national"].isin(ids_caught)
    df_pokemon["artwork"] = ""
    df_pokemon["type1"] = ""
    df_pokemon["type2"] = ""
    df_pokemon["evolvefrom"] = ""
    df_pokemon["evolveto"] = ""
    df_pokemon["evolvefrom_art"] = ""
    df_pokemon["evolveto_art"] = ""
    display_df(df_pokemon, f"National Pokedex")
    
    with st.spinner("Loading Pokemon", show_time=True):
        for i, row in df_pokemon.copy().iterrows():
            p = get_pokemon(row["number_national"])
            ps = get_pokemon_species(row["number_national"])
            # st.write(ps)
            art = p.artwork
            ev_f = getattr(ps, "evolves_from_species_name", "")
            ev_t = ""
            ev_fa = get_pokemon(ev_f).artwork if ev_f else ""
            ev_ta = ""
            ts = p.types
            df_pokemon.loc[i, ["artwork", "evolvefrom", "evolvefrom_art", "evolveto", "evolveto_art"]] = [art, ev_f, ev_fa, ev_t, ev_ta]
            for t, c in zip(ts, ["type1", "type2"]):
                # if i < 3:
                #     st.write(f"{t=}, {c=}")
                t_: Type = types.get(t)
                # if i < 3:
                #     st.write(f"{t_.name=}")
                if t_ is not None:
                    df_pokemon.loc[i, c] = t_.last_name_icon
                    
    chains = {}
    chain_strs = {}
    ids_to_render = dict(zip(df_pokemon["number_national"], [1] * len(df_pokemon)))
    for i, row in df_pokemon.copy().iterrows():
        p1 = get_pokemon(row["number_national"])
        df_ev_to = df_pokemon[df_pokemon["evolvefrom"] == p1.name].reset_index()
        # display_df(df_ev_to, f"{i=}, {p1=}")
        if df_ev_to.empty:
            chains[p1.id] = []
        chain_strs[p1.id] = f"{p1.name.title()}"
        while not df_ev_to.empty:
            p2 = get_pokemon(df_ev_to.iloc[0]["number_national"])
            ids_to_render[p2.id] = 0
            chain_strs[p1.id] += f" -> {p2.name.title()}"
            if p1.id not in chains:
                chains[p1.id] = [p2.id]
            else:
                chains[p1.id].append(p2.id)
            df_ev_to2 = df_pokemon[df_pokemon["evolvefrom"] == p2.name].reset_index()
            if not df_ev_to2.empty:
                df_ev_to = pd.concat([df_ev_to, df_ev_to2])
            df_ev_to = df_ev_to[1:]
        # if i > 2:
        #     break

    i = 0
    img_width = 80
    # ev_col_p = 0.5
    radio_layout = st.radio("Layout:", ["Rows", "Compact"], 1)
    radio_show = st.radio("Filter:", ["All", "Caught", "Seen", "Seen + Missed", "Missed"], 1)
    
    def check_skip(id_, evolve=False):
        return any([
            (radio_show == "Caught") and (data[id_ - 1] != 1),
            (radio_show == "Seen") and (pd.isna(data[id_ - 1])),
            (radio_show == "Seen + Missed") and (data[id_ - 1] != 0),
            (radio_show == "Missed") and (not pd.isna(data[id_ - 1]))
        ]) or (False if evolve else (not ids_to_render[id_]))
    
    # def check_skip(id_, evolve=False):
    #     a = (radio_show == "Caught") and (data[id_ - 1] != 1)
    #     b = (radio_show == "Seen") and (pd.isna(data[id_ - 1]))
    #     c = (radio_show == "Seen + Missed") and (data[id_ - 1] == 0)
    #     d = (radio_show == "Missed") and (not pd.isna(data[id_ - 1]))
    #     e = (not ids_to_render[id_])
    #     if id_ in [19, 20]:
    #         st.write(f"{id_}, {evolve=}, {a=}, {b=}, {c=}, {d=}, {e=}")
    
    with st.container(horizontal=radio_layout=="Compact"):
        for p_name_src, p_chain in chains.items():
            p1 = get_pokemon(p_name_src)
            # if check_skip(p1.id):
            #     continue
            # st.write(f"{img_width=}, {len(p_chain)=}, {int(img_width * (max(1, len(p_chain)) * 3))=}")
            with st.container(border=True, width=int(img_width * (max(1.4, len(p_chain)) * 3.2))):
                st.subheader(chain_strs[p1.id], text_alignment="center")
                
                with st.container(horizontal=True, horizontal_alignment="center"): 
                    if not check_skip(p2.id):
                        with st.container(horizontal_alignment="center"):
                            st.image(p1.artwork, width=img_width)
                            cols_cap = st.columns([0.25, 0.75])
                            if data[p1.id - 1] == 1:
                                cols_cap[0].image(LINK_POKEBALL, width=int(img_width / 3.5))
                            cols_cap[1].caption(f"#{p1.id} - {p1.name}")
                        
                    if not len(p_chain):
                        continue
                    for j, p_evolve in enumerate(p_chain):
                        with st.container(width=img_width // 3, horizontal_alignment="center"):
                            with st.container(height=int(img_width // 10), width=1, border=False):
                                pass
                            st.subheader(f"->", text_alignment="center")
                        p2 = get_pokemon(p_evolve)
                        cols_cap = st.columns([0.25, 0.75])
                        if not check_skip(p2.id, evolve=True):
                            if data[p2.id - 1] == 1:
                                cols_cap[0].image(LINK_POKEBALL, width=int(img_width / 3.5))
                            cols_cap[1].image(p2.artwork, f"#{p2.id} - {p2.name}", width=img_width)
                        if j == (len(p_chain) - 1):
                            break
        i += 1
        # if i >= 5:
        #     break
            
    st.stop()
            
    
    df_pokemon.rename(columns={"number_national": "#"}, inplace=True)
    st.write(df_pokemon.columns.tolist())
    # display_df_paginated(
    #     df_pokemon[["#", "artwork", "name", "type1", "type2", "seen", "caught"]],
    #     "Pokemon",
    #     column_config={
    #         "artwork": st.column_config.ImageColumn("artwork", width=80),
    #         "type1": st.column_config.ImageColumn("type1", width=80),
    #         "type2": st.column_config.ImageColumn("type2", width=120),
    #     },
    #     row_height=80,
    #     key="key_here",
    #     width=1800,
    #     height=750,
    #     debug=False
    # )
    
    # a, b = "<___", ""
    display_df(df_pokemon)
    
    df_pokemon["type3"] = df_pokemon.apply(lambda r: f'<div><img src="{r["type1"]}">' + ("" if r["type2"] == "" else f'<br><img src="{r["type2"]}">') + "</div>", axis=1)
    for col in ["artwork", "type1", "type2", "evolvefrom_art", "evolveto_art"]:
        df_pokemon[col] = df_pokemon[col].apply(lambda a: f'<img src="{a}">' if a is not None else "")    
    df_pokemon["type"] = df_pokemon["type3"]
    
    html = df_pokemon[["#", "artwork", "name", "type", "seen", "caught", "evolvefrom_art"]].to_html(index=False)
    display_df(df_pokemon)
    html = html.replace("&lt;", "<").replace("&gt;", ">")
    st.markdown(
        html,
        unsafe_allow_html=True
    )
        
    st.stop()
    
    with st.container(horizontal=True):
        for k, t in types.items():
            # st.write(k)
            # img = t.last_name_icon
            img = t.get_generation_sprite(sel_generation)
            if img:
                st.image(img)
    
    st.write(pokedex)
    # st.write(pokedex.df)
    
    k_selectbox_pokemon = "key_selectbox_pokemon"
    st.session_state.setdefault(k_selectbox_pokemon, DEFAULT_GAME)
    selectbox_pokemon = st.selectbox(
        label="Pokemon:",
        options=pokedex.pokemon_entries.values(),
        key=k_selectbox_pokemon
    )
    
    if selectbox_pokemon:
        p = get_pokemon(selectbox_pokemon)
        p.card()

st.stop()


with st.container(horizontal=True):
    with st.container(border=True):
        fig = px.pie(
            df_pies,
            names="category",
            values="val"
        )
        st.subheader("All Pokemon", text_alignment="center")
        st.plotly_chart(fig)
        
    with st.container(border=True):
        fig = px.pie(
            df_pies[df_pies["category"] != "Missed"],
            names="category",
            values="val"
        )
        st.subheader("Seen Pokemon Only", text_alignment="center")
        st.plotly_chart(fig)
        

st.divider()
st.header("Browse")
# p = get_pokemon("luxray")
selectbox_pokemon = st.selectbox("Browse a Pokemon", ids_all)
if selectbox_pokemon is not None:
    p = get_pokemon(selectbox_pokemon)

    # st.write(p)

    # data = {
    #     "id": p["id"],
    #     "name": p["name"],
    #     "types": [t["type"]["name"] for t in p["types"]],
    #     "sprite": p["sprites"]["front_default"],
    #     "official_artwork": p["sprites"]["other"]["official-artwork"]["front_default"],
    # }

    p.card()
    st.write(p.data)
    st.write(p.raw)

    evo = get_evolution_chain("luxray")
    st.write(evo["chain"])

    gen1 = Generation(get_generation(1))
    st.write(list(gen1.data.keys()))
    st.write(gen1.pokemon_species)
    # gen2 = get_generation(2)
    # gen3 = get_generation(3)
    # gen4 = get_generation(4)
    # all_gens = gen1.copy()
    # all_gens.update(gen2)
    # all_gens.update(gen3)
    # all_gens.update(gen4)
    # # st.write(all_gens[0])
    # g = [(p["name"], p["id"]) for p in all_gens["pokemon_species"]]
    # g.sort(key=lambda t: t[1])
    # pokemon_names = [p[0] for p in g]
    # st.write("pokemon_names")
    # st.write(pokemon_names)