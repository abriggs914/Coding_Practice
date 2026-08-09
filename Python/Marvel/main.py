import re
import pandas as pd
import streamlit as st
import plotly.express as px

from streamlit_utility import display_df


st.set_page_config(layout="wide")


@st.cache_data
def load_imdb_list() -> pd.DataFrame:
        
    file = "imdb_list_20260802.txt"
    content = []

    with open(file, "r", encoding="utf8") as f:
        lines = f.readlines()
        
    c_lines = []
    for i, line in enumerate(lines):
        match = re.match(r"--->\d+.", line)
        if match:
            # new numbered item
            print(f"{line=}")
            title = "".join(line.split(".")[1:]).strip()
            if len(title) > 1:
                content.append({
                    "title": title,
                    "lines_0": i - 1
                })
                content[-1]["lines_1"] = i - 2
                c_lines = []
        elif content:
            c_lines.append(line)
            
            if line.lower().strip() == "pre-release info":
                continue
            
            if len(c_lines) == 1:
                # year, runtime, rating
                s_year = line[:4]
                
                try:
                    s_year_i = int(s_year)
                
                    r_line = line.removeprefix(s_year).strip()
                    print(f"A {r_line=}")
                    if r_line.startswith("-") or r_line.startswith("–"):
                        # continuing
                        r_line = r_line.removeprefix("-").removeprefix("–").strip()      
                        e_year = r_line[:4]
                        try:
                            e_year_i = int(e_year)
                            r_line = r_line.removeprefix(e_year)
                        except Exception as e:
                            e_year = None
                        print(f"B {e_year=}, {r_line=}")
                    else:
                        e_year = s_year
                        
                except Exception as e:
                    word = line.split(" ")[0]
                    r_line = line.removeprefix(word).strip()
                    if "expected" in word.lower():
                        month = r_line.split(" ")[0].strip()
                        r_line = r_line.removeprefix(month).strip()
                        day = r_line.split(" ")[0].removesuffix(",")
                        r_line = r_line.removeprefix(day).strip().removeprefix(",").strip()
                        s_year = e_year = r_line[:4]
                        r_line = r_line.removeprefix(s_year)
                
                runtime = r_line.split("m")[0]
                rnt = runtime.replace("h", "").replace(" ", "").strip()
                print(f"RUNTIME {r_line=}")
                try:
                    rnt_i = int(rnt)
                    runtime = runtime + "m"
                except Exception as e:
                    runtime = None
                    
                rating = None
                if r_line is not None:
                    r_line = r_line.removeprefix(str(runtime))
                    print(f"RATING {r_line=}")
                    
                    rating = r_line[:2]
                    if rating in ["14", "18"]:
                        rating = r_line[:3]
                    elif rating.lower() == "tv":
                        if r_line.lower().startswith("tv-"):
                            rating = r_line[:5]
                            r_line = r_line.removeprefix(rating)
                    elif rating.lower() == "no":
                        if r_line.lower().startswith("not rated"):
                            r_line = r_line.lower().removeprefix("not rated")
                            rating = "Not Rated"
                    elif rating.lower() == "pg":
                        pass
                    else:
                        rating = None
                    
                    r_line = r_line.removeprefix(f"{rating}").strip()
                    
                content[-1].update({
                    "s_year": s_year,
                    "e_year": e_year,
                    "runtime": runtime,
                    "rating": rating,
                    "score": r_line if r_line else None
                })
            
            elif len(c_lines) == 2:
                content[-1]["imdb"] = line.strip()
                
            elif len(c_lines) == 3:
                votes = line.strip().strip()
                if votes:
                    if votes.startswith("(") and votes.endswith(")"):
                        content[-1]["votes"] = votes
                    else:
                        content[-1]["desc"] = votes
                                    
            elif len(c_lines) == 5:
                if "desc" not in content[-1]:
                    content[-1]["desc"] = line.strip()
                else:
                    content[-1]["notes"] = line.strip()
                    
            elif len(c_lines) == 6:
                if "notes" not in content[-1]:
                    content[-1]["notes"] = line.strip()
                else:
                    content[-1]["timeline/release"] = line.strip()
                    
            elif len(c_lines) == 7:
                if "timeline/release" not in content[-1]:
                    content[-1]["timeline/release"] = line.strip()

    # for i, data in enumerate(content):
    #     title = data["title"]
    #     print(f"{title=}")
    #     print(f"\t{data}")
    # print(len(content))

    df = pd.DataFrame(content)
    df["imdb"] = df["imdb"].apply(lambda i: float(i) if ((not pd.isna(i)) and (i != "")) else 0)
    df["imdb"] = df["imdb"].astype(float)

    df["s_year"] = df["s_year"].astype(int)
    df["e_year"] = df["e_year"].apply(lambda e: int(e) if ((not pd.isna(e)) and (e != "")) else None)
    df["votes"] = df["votes"].fillna(0)
    df["votes"] = df["votes"].apply(lambda v: int(str(v).lower().replace("k", "000").replace("m", "000000").replace(".", "").removeprefix("(").removesuffix(")")))
    df["votes"] = df["votes"] / 1e6
    df = df.reset_index(names="order_chronological")
    df["minutes"] = df["runtime"].apply(lambda r: eval(("(" if ("h" in r.lower()) else "") + r.lower().replace("m","").replace("h","*60)").replace(" ", "+")) if ((not pd.isna(r)) and (r != "")) else None)
    df["d_years"] = df["e_year"] - df["s_year"]
    df.sort_values(["d_years", "s_year"], inplace=True)
    df = df.reset_index(drop=True).reset_index(names="order_release")
    return df


df = load_imdb_list()
display_df(df, "Entire Watch List")

df_titles = df[[
    "title",
    "order_release",
    "order_chronological",
    "s_year",
    "e_year",
    "votes",
    "runtime",
    "rating",
    "score",
    "imdb",
    "desc",
    "notes",
    "minutes",
]].groupby([
    "title",
]).agg({
    "order_release": "min",
    "order_chronological": "min",
    "s_year": "min",
    "e_year": "min",
    "votes": "min",
    "runtime": "min",
    "rating": "min",
    "score": "min",
    "imdb": "min",
    "desc": "min",
    "notes": "min",
    "minutes": "min",
})

display_df(
    df_titles,
    "Individual Titles"
)
df_titles["count"] = 1
df_score_by_year = df_titles.groupby([
    "s_year"
]).agg({
    "minutes": "mean",
    "imdb": "mean",
    "votes": "mean",
    "count": "sum"
})
df_score_by_year = df_score_by_year.reset_index(names="year")
with st.container(horizontal=True):
    display_df(
        df_score_by_year,
        "Scores By Year",
    )
    
    for c in ["minutes", "imdb", "votes", "count"]:
        fig = px.line(
            df_score_by_year,
            "year",
            c
        )
        with st.container(border=True):
            st.subheader(c.title())
            st.plotly_chart(fig)


fig = px.line(
    df_score_by_year,
    "year",
    y=["minutes", "imdb", "votes", "count"]
)
st.plotly_chart(fig)