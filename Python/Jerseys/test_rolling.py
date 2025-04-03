from dataframe_utility import *


if __name__ == "__main__":
    cols = ["T", "W", "L", "OTL", "SOL"]
    df = random_df(
        n_rows=82,
        n_columns=cols,
        defaults={
            "W": list(range(2)),
            "L": list(range(2)),
            "OTL": list(range(2)),
            "SOL": list(range(2)),
            "T": "str"
        }
    )

    for col in cols[1:]:
        df[f"{col}_l10"] = df.rolling(
            window=10,
            on=col
        )[col].sum()

    df.fillna(0, inplace=True)

    for col in df.columns[1:]:
        df[col] = df[col].astype(int)

    df["R_l10"] = df.apply(
        lambda row:
            f"{row['W_l10']}-{row['L_l10']}-{row['OTL_l10']+row['SOL_l10']}"
        , axis=1
    )

    print(df)
