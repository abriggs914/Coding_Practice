from full_pokedex import pokedex
from pokemon import Pokemon

#Dict[Union[str,  Any],  Union[Union[Tuple[List[str],  List[str],  List[Any]],  Tuple[List[str],  List[str],  List[str]]],  Any]]
type_effectiveness = {'fairy': (['poison', 'steel'], ['fighting', 'dragon', 'dark'], []),
                      'steel': (['fire', 'fighting', 'ground'], ['ice', 'rock', 'fairy'], []),
                      'dark': (['fighting', 'bug', 'fairy'], ['psychic', 'ghost'], []),
                      'dragon': (['ice', 'dragon', 'fairy'], ['dragon'], ['fairy']),
                      'ghost': (['ghost', 'dragon'], ['psychic', 'ghost'], ['normal']),
                      'rock': (['water', 'grass', 'fighting', 'ground', 'steel'], ['fire', 'ice', 'flying', 'bug'], []),
                      'bug': (['fire', 'flying', 'rock'], ['grass', 'psychic', 'dark'], []),
                      'psychic': (['bug', 'ghost', 'dark'], ['fighting', 'poison'], ['dark']),
                      'flying': (['electric', 'ice', 'rock'], ['grass', 'fighting', 'bug'], []),
                      'ground': (['water', 'grass', 'ice'], ['fire', 'electric', 'poison', 'rock', 'steel'], ['flying']),
                      'poison': (['ground', 'psychic'], ['grass', 'fairy'], ['steel']),
                      'fighting': (['flying', 'psychic', 'fairy'], ['normal', 'ice', 'rock', 'dark', 'steel'], ['ghost']),
                      'ice': (['fire', 'fighting', 'rock', 'steel'], ['grass', 'ground', 'flying', 'dragon'], []),
                      'grass': (['fire', 'ice', 'poison', 'flying', 'bug'], ['water', 'ground', 'rock'], []),
                      'electric': (['ground'], ['water', 'flying'], ['ground']),
                      'water': (['electric', 'grass'], ['fire', 'ground', 'rock'], []),
                      'fire': (['water', 'ground', 'rock'], ['grass', 'ice', 'bug', 'steel'], []),
                      'normal': (['fighting'], [], ['ghost'])}

print(type_effectiveness)
print(type_effectiveness.get('fairy'))

pokedex_temp = {'id':[],
                'name':[],
                'types':[]}

pokemon_list = []

for i in range(len(pokedex)):
    pokedex_temp['id'].append((i+1))
    pokedex_temp['name'].append(pokedex[i]['name']['english'])
    pokedex_temp['types'].append(pokedex[i]['type'])
    pokemon_list.append(Pokemon((i+1), pokedex[i]['name']['english'], pokedex[i]['type'], pokedex[i]['base']))
    print(pokemon_list[i])

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



