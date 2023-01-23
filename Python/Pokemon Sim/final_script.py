from full_pokedex import pokedex
from pokemon import Pokemon


#Dict[Union[str,  Any],  Union[Union[Tuple[List[str],  List[str],  List[Any]],  Tuple[List[str],  List[str],  List[str]]],  Any]]
type_effectiveness = {'fairy': (['poison', 'steel'], ['fight', 'dragon', 'dark'], []),
                      'steel': (['fire', 'fight', 'ground'], ['ice', 'rock', 'fairy'], []),
                      'dark': (['fight', 'bug', 'fairy'], ['psychic', 'ghost'], []),
                      'dragon': (['ice', 'dragon', 'fairy'], ['dragon'], ['fairy']),
                      'ghost': (['ghost', 'dragon'], ['psychic', 'ghost'], ['normal']),
                      'rock': (['water', 'grass', 'fight', 'ground', 'steel'], ['fire', 'ice', 'flying', 'bug'], []),
                      'bug': (['fire', 'flying', 'rock'], ['grass', 'psychic', 'dark'], []),
                      'psychic': (['bug', 'ghost', 'dark'], ['fight', 'poison'], ['dark']),
                      'flying': (['electric', 'ice', 'rock'], ['grass', 'fight', 'bug'], []),
                      'ground': (['water', 'grass', 'ice'], ['fire', 'electric', 'poison', 'rock', 'steel'], ['flying']),
                      'poison': (['ground', 'psychic'], ['grass', 'fairy'], ['steel']),
                      'fight': (['flying', 'psychic', 'fairy'], ['normal', 'ice', 'rock', 'dark', 'steel'], ['ghost']),
                      'ice': (['fire', 'fight', 'rock', 'steel'], ['grass', 'ground', 'flying', 'dragon'], []),
                      'grass': (['fire', 'ice', 'poison', 'flying', 'bug'], ['water', 'ground', 'rock'], []),
                      'electric': (['ground'], ['water', 'flying'], ['ground']),
                      'water': (['electric', 'grass'], ['fire', 'ground', 'rock'], []),
                      'fire': (['water', 'ground', 'rock'], ['grass', 'ice', 'bug', 'steel'], []),
                      'normal': (['fight'], [], ['ghost'])}


if __name__ == '__main__':

    print(type_effectiveness)
    print(type_effectiveness.get('fairy'))

    pokemon_list = []

    for i in range(len(pokedex)):
        num = (i+1)
        name = pokedex[i]['name']['english']
        types = pokedex[i]['type']
        stats = pokedex[i]['base']
        pokemon_list.append(Pokemon(num, name, types, stats))

    print(pokemon_list)
