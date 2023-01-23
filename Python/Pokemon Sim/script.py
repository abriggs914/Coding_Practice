from full_pokedex import pokedex
from pokemon import Pokemon
import pandas as pd
import random

# Dict[Union[str,  Any],  Union[Union[Tuple[List[str],  List[str],  List[Any]],  Tuple[List[str],  List[str],  List[str]]],  Any]]
# List of all types stored as a dictionary. Each type contains a tuple of three lists:
# 1st list ideals strong damage to the key type
# 2nd list is dealt strong damage by the key type
# 3rd list is dealt no damage from the key type
type_effectiveness = {'fairy': (['poison', 'steel'], ['fighting', 'dragon', 'dark'], []),
                      'steel': (['fire', 'fighting', 'ground'], ['ice', 'rock', 'fairy'], []),
                      'dark': (['fighting', 'bug', 'fairy'], ['psychic', 'ghost'], []),
                      'dragon': (['ice', 'dragon', 'fairy'], ['dragon'], ['fairy']),
                      'ghost': (['ghost', 'dragon'], ['psychic', 'ghost'], ['normal']),
                      'rock': (['water', 'grass', 'fighting', 'ground', 'steel'], ['fire', 'ice', 'flying', 'bug'], []),
                      'bug': (['fire', 'flying', 'rock'], ['grass', 'psychic', 'dark'], []),
                      'psychic': (['bug', 'ghost', 'dark'], ['fighting', 'poison'], ['dark']),
                      'flying': (['electric', 'ice', 'rock'], ['grass', 'fighting', 'bug'], []),
                      'ground': (
                      ['water', 'grass', 'ice'], ['fire', 'electric', 'poison', 'rock', 'steel'], ['flying']),
                      'poison': (['ground', 'psychic'], ['grass', 'fairy'], ['steel']),
                      'fighting': (
                      ['flying', 'psychic', 'fairy'], ['normal', 'ice', 'rock', 'dark', 'steel'], ['ghost']),
                      'ice': (['fire', 'fighting', 'rock', 'steel'], ['grass', 'ground', 'flying', 'dragon'], []),
                      'grass': (['fire', 'ice', 'poison', 'flying', 'bug'], ['water', 'ground', 'rock'], []),
                      'electric': (['ground'], ['water', 'flying'], ['ground']),
                      'water': (['electric', 'grass'], ['fire', 'ground', 'rock'], []),
                      'fire': (['water', 'ground', 'rock'], ['grass', 'ice', 'bug', 'steel'], []),
                      'normal': (['fighting'], [], ['ghost'])}


pokedex_temp = {'iid': [],
                'name': [],
                'types': []}


pokemon_list = []


for i in range(len(pokedex)):
    pokedex_temp['iid'].append((i + 1))
    pokedex_temp['name'].append(pokedex[i]['name']['english'])
    pokedex_temp['types'].append(pokedex[i]['type'])
    pokemon_list.append(Pokemon((i + 1), pokedex[i]['name']['english'], pokedex[i]['type'], pokedex[i]['base']))
    # print(pokemon_list[i])


types_list_dataframe = pd.read_csv('types_list.csv')
types_list = list(types_list_dataframe['identifier'])

moves_list_dataframe = pd.read_csv('moves_list.csv')
moves_list_dataframe_coloumns = list(moves_list_dataframe.columns)


def look_up_type_index(types):
    for i in range(len(types_list)):
        if types == types_list[i]:
            return i + 1


def get_elemental_moves(types):
    possible_moves = {}
    moves = list(moves_list_dataframe.apply(lambda x: x.identifier, axis=1))
    move_types = list(moves_list_dataframe.apply(lambda x: x.type_id, axis=1))
    for typ in types:
        possible_moves[typ] = []
        type_index = look_up_type_index(typ)
        for i in range(len(move_types)):
            if move_types[i] == type_index:
                possible_moves[typ].append(moves[i])
    return possible_moves


def look_up_pokemon_name(name):
    for pokemon in pokemon_list:
        if pokemon.get_name().lower() == name.lower():
            return pokemon
    raise ValueError


def look_up_pokemon_id(id):
    for pokemon in pokemon_list:
        if pokemon.get_id() == id:
            return pokemon
    raise ValueError


def look_up_pokemon(identifier):
    if type(identifier) is str:
        print('look-up name')
        return look_up_pokemon_name(identifier)
    elif type(identifier) is int:
        return look_up_pokemon_id(identifier)
        print('look-up iid number')
    else:
        raise ValueError


def gen_random_team():
    team = []
    for i in range(6):
        j = random.randint(1, len(pokemon_list))
        team.append(pokemon_list[j - 1])
    return team


def pick_best_team_attacker(team, enemy_pokemon):
    # print('team:' + str(team) + '\n\tVS\n' + str(enemy_pokemon))
    effectiveness_scores = []
    for pokemon in team:
        effectiveness_scores.append(pokemon.versus_effectiveness(enemy_pokemon))
    best_score_index = effectiveness_scores.index(max(effectiveness_scores))
    return team[best_score_index]


def pick_worst_team_attacker(team, enemy_pokemon):
    # print('team:' + str(team) + '\n\tVS\n' + str(enemy_pokemon))
    effectiveness_scores = []
    for pokemon in team:
        effectiveness_scores.append(pokemon.versus_effectiveness(enemy_pokemon))
    best_score_index = effectiveness_scores.index(min(effectiveness_scores))
    return team[best_score_index]


def pick_best_team_defender(team, enemy_pokemon):
    # print('team:' + str(team) + '\n\tVS\n' + str(enemy_pokemon))
    effectiveness_scores = []
    for pokemon in team:
        effectiveness_scores.append(enemy_pokemon.versus_effectiveness(pokemon))
    best_score_index = effectiveness_scores.index(min(effectiveness_scores))
    return team[best_score_index]


def pick_worst_team_defender(team, enemy_pokemon):
    # print('team:' + str(team) + '\n\tVS\n' + str(enemy_pokemon))
    effectiveness_scores = []
    for pokemon in team:
        effectiveness_scores.append(enemy_pokemon.versus_effectiveness(pokemon))
    best_score_index = effectiveness_scores.index(max(effectiveness_scores))
    return team[best_score_index]


if __name__ == '__main__':



    print(type_effectiveness)
    print(type_effectiveness.get('fairy'))



    print(pokemon_list[0].versus_effectiveness(pokemon_list[1]) == 1)
    print(pokemon_list[3].versus_effectiveness(pokemon_list[1]) == 2)
    print(pokemon_list[3].versus_effectiveness(pokemon_list[46]) == 4)
    print(pokemon_list[24].versus_effectiveness(pokemon_list[26]) == 0)
    print(pokemon_list[235].versus_effectiveness(pokemon_list[176]) == 0.5)

    print(pokemon_list[238].move_effectiveness('electric', pokemon_list[1]) == 1)
    print(pokemon_list[0].move_effectiveness('grass', pokemon_list[1]) == 0.5)
    print(pokemon_list[3].move_effectiveness('fire', pokemon_list[1]) == 2)
    print(pokemon_list[3].move_effectiveness('fire', pokemon_list[46]) == 4)
    print(pokemon_list[24].move_effectiveness('electric', pokemon_list[26]) == 0)
    print(pokemon_list[235].move_effectiveness('fighting', pokemon_list[176]) == 0.5)

    print(types_list_dataframe)
    print(types_list)

    print(moves_list_dataframe_coloumns)





    print(get_elemental_moves(['fire', 'water']))
    print(look_up_pokemon('pikachu'))
    print(look_up_pokemon(15))
    # print(look_up_pokemon(None))

    team = gen_random_team()
    enemy_pokemon = look_up_pokemon(random.randint(0, len(pokemon_list) - 1))
    print('team:' + str(team) + '\n\tVS\n' + str(enemy_pokemon))
    print('pick_best_team_attacker',pick_best_team_attacker(team, enemy_pokemon))
    print('pick_best_team_defender',pick_best_team_defender(team, enemy_pokemon))
    print('pick_worst_team_attacker',pick_worst_team_attacker(team, enemy_pokemon))
    print('pick_worst_team_defender',pick_worst_team_defender(team, enemy_pokemon))
