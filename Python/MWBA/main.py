from utility import dict_print
from itertools import combinations

teams = {
    "Port City Fog": {
        "city": "Saint John",
        "province": "NB"
    },
    "Halifax Thunder": {
        "city": "Halifax",
        "province": "NS"
    },
    "Halifax Hornets": {
        "city": "Halifax",
        "province": "NS"
    },
    "Windsor Edge": {
        "city": "Windsor",
        "province": "NS"
    },
    "Moncton Mystics": {
        "city": "Moncton",
        "province": "NB"
    },
    "Fredericton Freeze": {
        "city": "Fredericton",
        "province": "NB"
    }
}


def n_games_rr(teams_dict, n_rr=1):
    n_teams = len(teams_dict) - 1
    # ab ac ad ae af
    #    bc bd be bf
    #       cd ce cf
    #          de df
    #             ef
    return n_rr * (((n_teams * (n_teams + 1))) // 2)


def read_html_table_values(file_name):
    try:
        with open(file_name, "r") as f:
            html = f.read()
            html = html.replace("\n", "")
            idx_1 = html.index("<tbody>")
            idx_2 = html.index("</tbody>")
            html_3 = html[idx_1: idx_2].strip().split("<td>")[1:]
         #    return [int(line.replace("</td>", "").replace("<tr>", "").replace("</tr>", "").strip()) for i, line in
         # enumerate([line for i, line in enumerate(html.replace("\n", "").split("<td>")[1:]) if i % 7 != 0])]
            return {html_3[i].replace("</td>", "").strip(): [int(line.replace("</tr>", "").replace("</td>", "").replace("<tr>", "").strip()) for line in html_3[i + 1: i + 7]] for i in range(0, len(html_3), 7)}
    except ValueError as ve:
        raise ValueError(f"ValueError: {ve}")
    except FileExistsError as fe:
        raise ValueError(f"FileExistsError: {fe}")
    except FileNotFoundError as fn:
        raise ValueError(f"FileNotFoundError: {fn}")
    except IndexError as ie:
        raise ValueError(f"IndexError: {ie}")
    except AttributeError as ae:
        raise ValueError(f"AttributeError: {ae}")
    except TypeError as te:
        raise ValueError(f"TypeError: {te}")

if __name__ == '__main__':
    print(dict_print(teams))
    n_rr = 2
    n_pts_win = 2
    n_games = n_games_rr(teams, n_rr=n_rr)
    max_pts = n_rr * n_pts_win * (len(teams) - 1)
    print(
        f"Number of games for a group of {len(teams)} teams in a round robin season\n playing {n_rr} game{'' if n_rr == 1 else 's'} each, is {n_games} game{'' if n_games == 1 else 's'}.\nMeaning that the best overall points record is {max_pts} point{'' if max_pts == 1 else 's'}")

    print(dict_print({i + 1: {"A": dat[0], "B": dat[1]} for i, dat in enumerate(n_rr * list(combinations(teams, 2)))}))

    html = """<tr>
                            <td>Halifax Thunder</td>
                            <td>2</td>
                            <td>2</td>
                            <td>0</td>
                            <td>156</td>
                            <td>121</td>
                            <td>4</td>
                        </tr>
                            <tr>
                            <td>Halifax Hornets</td>
                            <td>2</td>
                            <td>2</td>
                            <td>0</td>
                            <td>157</td>
                            <td>132</td>
                            <td>4</td>
                        </tr>
                        <tr>
                            <td>Windsor</td>
                            <td>2</td>
                            <td>1</td>
                            <td>1</td>
                            <td>137</td>
                            <td>137</td>
                            <td>2</td>
                        </tr>
                        <tr>
                            <td>Fredericton</td>
                            <td>2</td>
                            <td>1</td>
                            <td>1</td>
                            <td>134</td>
                            <td>137</td>
                            <td>2</td>
                        </tr>
                        <tr>
                            <td>Moncton</td>
                            <td>2</td>
                            <td>0</td>
                            <td>2</td>
                            <td>129</td>
                            <td>149</td>
                            <td>0</td>
                        </tr>
                        <tr>
                            <td>Port City</td>
                            <td>2</td>
                            <td>0</td>
                            <td>2</td>
                            <td>131</td>
                            <td>151</td>
                            <td>0</td>
                        </tr>"""
    html.replace("\n", "")
    html_3 = html.replace("\n", "").split("<td>")[1:]
    html_4 = [line for i, line in enumerate(html_3) if i % 7 != 0]
    html_5 = [int(line.replace("</td>", "").replace("<tr>", "").replace("</tr>", "").strip()) for i, line in enumerate(html_4)]
    html_6 = [int(line.replace("</td>", "").replace("<tr>", "").replace("</tr>", "").strip()) for i, line in enumerate([line for i, line in enumerate(html.replace("\n", "").split("<td>")[1:]) if i % 7 != 0])]
    print(dict_print({
        "html": html,
        "html_3": html_3,
        "html_4": html_4,
        "html_5": html_5,
        "html_6": html_6,
        "sum(5)": sum(html_5),
        "sum(6)": sum(html_6)
    }))
    print(dict_print(read_html_table_values("2022-05-19.html")))
    print(dict_print(read_html_table_values("2022-05-20.html")))
    print(read_html_table_values("2022-05-20.html"))
