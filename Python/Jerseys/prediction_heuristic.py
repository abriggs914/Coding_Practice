import pandas as pd
from itertools import permutations


def h1(
        correct_winner: bool,
        correct_away_score: bool,
        correct_home_score: bool,
        correct_away_shutout: bool,
        correct_home_shutout: bool,
        correct_reg_finish: bool,
        correct_ot_finish: bool,
        correct_so_finish: bool
        # ,
        # score_scheme: dict[str: dict[str: float]] = None
) -> float:

    # if score_scheme is None:
    #     score_scheme = {
    #         "+": {
    #             "correct_winner": 3/4
    #         },
    #         "-": {},
    #         "+/-": {}
    #     }
    sc_score = 1/8
    sc_shut_out = 1/10
    sc_reg = 1/10
    sc_ot = 3/20
    sc_so = 1/5

    score = 0
    score += correct_winner * (3/4)
    score += correct_away_score * sc_score
    score += correct_home_score * sc_score
    score += correct_away_shutout * sc_shut_out
    score += correct_home_shutout * sc_shut_out
    # score += (not correct_away_shutout) * -sc_shut_out
    # score += (not correct_home_shutout) * -sc_shut_out
    score += correct_reg_finish * sc_reg
    score += correct_ot_finish * sc_ot
    score += correct_so_finish * sc_so
    # return min(1, max(0, score))
    return score


def score_to_text(
        correct_winner: bool,
        correct_away_score: bool,
        correct_home_score: bool,
        correct_away_shutout: bool,
        correct_home_shutout: bool,
        correct_reg_finish: bool,
        correct_ot_finish: bool,
        correct_so_finish: bool
):
    msg = ""
    msg += ("" if correct_winner else "in") + "correct winner, "
    if correct_reg_finish + correct_ot_finish + correct_so_finish > 0:
        msg += "correctly in " + ("REG" if correct_reg_finish else ("OT" if correct_ot_finish else "SO"))
    else:
        msg += "incorrect result"
    msg += ", "
    msg += ("" if correct_away_score else "in") + "correct AwayScore, "
    msg += ("" if correct_away_shutout else "in") + "correct AwayShutOut, "
    msg += ("" if correct_home_score else "in") + "correct HomeScore, "
    msg += ("" if correct_home_shutout else "in") + "correct HomeShutOut"

    return msg


# predicted a shutout and was correct - good
# predicted a winner, but they lost AND were shutout - very bad
# predicted an OT finish and was correct - good
# predicted an OT finish and was SO instead - okay
# predicted a SO finish and was OT instead - okay


if __name__ == '__main__':

    cols = ["Winner", "AwayScore", "AwayShutOut", "HomeScore", "HomeShutOut", "REGResult", "OTResult", "SOResult"]
    vals = []

    start = 0
    # print(f"end={2**(len(cols) + 1)}")
    while start < (2 ** (len(cols) + 1)):
        b_code = (("0" * (len(cols) + 1)) + bin(start).removeprefix("0b"))[-len(cols):]
        # adjust the last 3 columns since you can only have 1 of the 3 true at a time.
        if b_code[-3] == "1":
            b_code = b_code[:-2] + "00"
        elif b_code[-2] == "1":
            b_code = b_code[:-1] + "0"

        vals.append(list(map(int, b_code)))
        start += 1
        # print(f"{start=}, {vals[-1]=}")

    df = pd.DataFrame(columns=cols, data=vals)
    df = df.loc[
        (df["AwayShutOut"] * df["HomeShutOut"] != 1)
        # & ((df["AwayScore"] == 0) & (df["AwayShutOut"] != 1))
        # & ((df["HomeScore"] == 0) & (df["HomeShutOut"] != 1))
    ].reset_index(drop=True)
    df["Score"] = df.apply(lambda row: h1(*row), axis=1)

    print(f"df=")
    for i, row in df.iterrows():
        if i == 0:
            row_ = "|" + " |".join(map(lambda v: (f"     {''.join([w[0].upper() for w in v if ord(w) < 91])}")[-5:], cols + ["Score"])) + "|"
            i_ = f"   {i}"[-3:]
            print(f"{i_=}, {row_=}")
        row_ = "|" + " |".join(map(lambda v: ("     " + str(round(v, 2)))[-5:], row.values.tolist())) + "| " + score_to_text(*row[:-1])
        i_ = f"   {i}"[-3:]
        print(f"{i_=}, {row_=}")
    print(f"{df['Score'].mean()=}")
    print(f"{df['Score'].min()=}")
    print(f"{df['Score'].max()=}")
