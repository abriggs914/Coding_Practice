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
                spl_2 = [line.strip() for line in
                         op_data.replace("align=left| ", "\"").replace("â€“", "-").replace("]]", "]").replace("[[",
                                                                                                              "[").replace(
                             "'''", "\"").split("\n|")]
                # print(f"i: {i}, j: {j}")
                try:
                    spl_2 = spl_2[1:]
                    if i == 0 and j < 2:
                        print(f"SPL: {spl_2}")
                    opponent, series, occurrences, games_played, record, percentage = spl_2
                    print(f"Team {team_name} vs. {opponent}, gp: {games_played}")
                except ValueError as ve:
                    print(ve)
                    print(f"SPL: {spl_2}")
