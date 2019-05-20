class Pokemon:
    # Dict[Union[str,  Any],  Union[Union[Tuple[List[str],  List[str],  List[Any]],  Tuple[List[str],  List[str],  List[str]]],  Any]]
    type_effectiveness = {'fairy': (['poison', 'steel'], ['fighting', 'dragon', 'dark'], []),
                          'steel': (['fire', 'fighting', 'ground'], ['ice', 'rock', 'fairy'], []),
                          'dark': (['fighting', 'bug', 'fairy'], ['psychic', 'ghost'], []),
                          'dragon': (['ice', 'dragon', 'fairy'], ['dragon'], ['fairy']),
                          'ghost': (['ghost', 'dragon'], ['psychic', 'ghost'], ['normal']),
                          'rock': (
                          ['water', 'grass', 'fighting', 'ground', 'steel'], ['fire', 'ice', 'flying', 'bug'], []),
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

    def __init__(self, id_in, name_in, type_in, stats_in):
        self.id = id_in
        self.name = name_in
        self.types = type_in
        self.stats = stats_in

    def __repr__(self):
        line = 'ID#:\t' + str(self.id) + '\n\tName:\t' + str(self.name) + '\n\tTypes:\t' + str(self.types) + '\n'
        return line

    def get_str_atk(self):
        lst = []
        for typ in self.types:
            lst += self.type_effectiveness[typ.lower()][1]
        return lst

    def get_weak_def(self):
        lst = []
        for typ in self.types:
            lst += self.type_effectiveness[typ.lower()][0]
        return lst

    def get_no_effect(self):
        lst = []
        for typ in self.types:
            lst += self.type_effectiveness[typ.lower()][2]
        return lst

    # generic, doesn't consider what type the move is
    def versus_effectiveness(self, enemy_pokemon):
        effectiveness = 1
        #print(str(self) + ' vs:\n' + str(enemy_pokemon))
        a_strong_atk = self.get_str_atk()
        b_strong_def = enemy_pokemon.get_str_atk()
        a_no_effect = self.get_no_effect()
        #print('astrongattack',a_strong_atk)
        #print('bstrongdefense',b_strong_def)
        for type_b in enemy_pokemon.types:
            if type_b.lower() in a_no_effect:
                return 0
            if type_b.lower() in a_strong_atk:
                effectiveness *= 2
        for type_a in self.types:
            if type_a.lower() in b_strong_def:
                effectiveness /= 2
        #print('effectiveness',effectiveness)
        #print('\n')
        return effectiveness

    def move_effectiveness(self, move, enemy_pokemon):
        if move.lower() not in list(self.type_effectiveness.keys()):
            return "ERROR"
        effectiveness = 1
        #print(str(self) + ' vs:\n' + str(enemy_pokemon))
        a_strong_atk = self.type_effectiveness.get(move)[1]
        b_strong_def = enemy_pokemon.get_str_atk()
        a_no_effect = self.type_effectiveness.get(move)[2]
        #print('astrongattack',a_strong_atk)
        #print('bstrongdefense',b_strong_def)
        for type_b in enemy_pokemon.types:
            if type_b.lower() in a_no_effect:
                return 0
            if type_b.lower() in a_strong_atk:
                effectiveness *= 2
        #for type_a in self.types:
        if move.lower() in b_strong_def:
            effectiveness /= 2
        #print('effectiveness',effectiveness)
        #print('\n')
        return effectiveness

    def get_name(self):
        return self.name

    def get_id(self):
        return self.id

    def get_types(self):
        return self.types

    def get_stats(self):
        return self.stats