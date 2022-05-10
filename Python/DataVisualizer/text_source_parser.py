if __name__ == "__main__":

    file_names = [
        r"./Text Source/calgary_flames.txt"
    ]

    for i, file_name in enumerate(file_names):
        with open(file_name, "r") as f:
            raw_str = f.read()
            spl_1 = raw_str.split("|-")
            team_name = spl_1[0].split("==")[1]
            for j, op_data in enumerate(spl_1[2:]):
                spl_2 = op_data.split("\n|")
                # print(f"i: {i}, j: {j}")
                try:
                    blank, opponent, series, occurrences, games_played, record, percentage = spl_2
                    print(f"Team {team_name} vs. {opponent}, gp: {games_played}")
                except ValueError as ve:
                    print(ve)


