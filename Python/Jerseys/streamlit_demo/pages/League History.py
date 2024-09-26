import datetime
from typing import Optional, Any

import requests
import streamlit as st
from streamlit.components import v1
from streamlit_javascript import st_javascript
import hydralit_components as hc


@st.cache_data(show_spinner=False)
def load_league_seasons() -> list[int]:
    try:
        return requests.get("https://api-web.nhle.com/v1/season").json()
    except requests.JSONDecodeError:
        return []


@st.cache_data(show_spinner=False)
def load_playoff_bracket_data(year: Optional[int] =None) -> dict[str: Any]:
    if year is None:
        n = datetime.datetime.now()
        year = n.year
        if n.month < 3:
            year -= 1
    try:
        return requests.get(f"https://api-web.nhle.com/v1/playoff-bracket/{year}").json()
    except requests.JSONDecodeError:
        return {}


def load_all_playoff_brackets() -> dict[int: dict[str: Any]]:
    results = {}
    for y in nhl_seasons_list:
        y0, y1 = divmod(y, 10000)
        results[y] = load_playoff_bracket_data(y1)
    return results


def streamlitImageClick(*args):
    print(f"streamlitImageClick {args=}")


with hc.HyLoader("Loading...", hc.Loaders.pulse_bars,):
    nhl_seasons_list: list[int] = load_league_seasons()
    playoff_bracket_data: dict[int: dict[str: Any]] = load_all_playoff_brackets()


top_bar = st.columns(1)
winners: dict[int: dict[str: int]] = st.session_state.setdefault("dict_winners", {})
teams: dict[int: Any] = st.session_state.setdefault("dict_teams", {})

not_winners = not bool(winners)
not_teams = not bool(teams)


for y in nhl_seasons_list:
    y0, y1 = divmod(y, 10000)
    s_title: str = f"{y0} - {y1}"
    st.write(f"# {s_title}")

    bracket_data: dict[str: Any] = playoff_bracket_data[y]
    bracket_logo: str = bracket_data.get("bracketLogo")
    bracket_logo_fr: str = bracket_data.get("bracketLogoFr")
    if bracket_logo:
        st.image(
            bracket_logo,
            caption=f"Bracket Logo {s_title}",
            use_column_width=True
        )
    series_data_list: list[dict[str: Any]] = bracket_data.get("series", [])
    if series_data_list:
        rounds_by_series: dict[int: list[int]] = {}
        for i, series_data in enumerate(series_data_list):
            playoff_round: int = series_data.get("playoffRound") - 1
            if playoff_round not in rounds_by_series:
                rounds_by_series[playoff_round] = []

            rounds_by_series[playoff_round].append(i)

        # print(f"{series_data_list[0]=}")
        # print(f"{rounds_by_series.keys()=}")
        # print(f"{rounds_by_series.values()=}")

        rounds_by_series_sort: list[tuple[int, list[int]]] = sorted([
            (pr, lst.copy()) for pr, lst in rounds_by_series.items()
        ], key=lambda tup: tup[0])
        # print(f"{rounds_by_series_sort[0]=}")
        # print(f"{rounds_by_series_sort[-1]=}")

        for pr, series_idxs in rounds_by_series_sort:

            # print(f"{rounds_by_series[pr]=}, {type(rounds_by_series[pr])=}")
            # print(f"{rounds_by_series[pr][1]=}, {type(rounds_by_series[pr][1])=}, {len(rounds_by_series[pr][1])=}")
            # print(f"{rounds_by_series[pr][1][0]=}, {type(rounds_by_series[pr][1][0])=}")
            # print(f"{series_data_list[pr]=}, {type(series_data_list[pr])=}")

            exp_round = st.expander(f"Round {pr}")
            n_games = sum([
                series_data_list[i].get("topSeedWins", 0)
                + series_data_list[i].get("bottomSeedWins", 0)
                for i in rounds_by_series[pr]
            ])

            for series_idx in series_idxs:
                series_data = series_data_list[series_idx]
                series_url: str = series_data.get("seriesUrl")
                series_title: str = series_data.get("seriesTitle")
                series_abbrev: str = series_data.get("seriesAbbrev")
                series_letter: str = series_data.get("seriesLetter")
                tst_rank: int = series_data.get("topSeedRank")
                tst_rank_abbrev: str = series_data.get("topSeedRankAbbrev")
                tst_wins: int = series_data.get("topSeedWins")
                lst_rank: int = series_data.get("bottomSeedRank")
                lst_rank_abbrev: str = series_data.get("bottomSeedRankAbbrev")
                lst_wins: int = series_data.get("bottomSeedWins")
                winning_team_id: int = series_data.get("winningTeamId")
                losing_team_id: int = series_data.get("losingTeamId")

                tst_data: dict[str: str] = series_data.get("topSeedTeam")
                lst_data: dict[str: str] = series_data.get("bottomSeedTeam")

                tst_id = tst_data.get("id")
                tst_abbrev = tst_data.get("abbrev")
                tst_name = tst_data.get("name", {}).get("default")
                tst_name_fr = tst_data.get("name", {}).get("fr")
                tst_common_name = tst_data.get("commonName", {}).get("default")
                tst_common_name_fr = tst_data.get("commonName", {}).get("fr")
                tst_place_name_prep = tst_data.get("placeNameWithPreposition", {}).get("default")
                tst_place_name_prep_fr = tst_data.get("placeNameWithPreposition", {}).get("fr")
                tst_logo = tst_data.get("logo")

                lst_id = lst_data.get("id")
                lst_abbrev = lst_data.get("abbrev")
                lst_name = lst_data.get("name", {}).get("default")
                lst_name_fr = lst_data.get("name", {}).get("fr")
                lst_common_name = lst_data.get("commonName", {}).get("default")
                lst_common_name_fr = lst_data.get("commonName", {}).get("fr")
                lst_place_name_prep = lst_data.get("placeNameWithPreposition", {}).get("default")
                lst_place_name_prep_fr = lst_data.get("placeNameWithPreposition", {}).get("fr")
                lst_logo = lst_data.get("logo")

                # tst_won_series = tst_wins > lst_wins
                tst_won_series = tst_id == winning_team_id
                if not_winners:
                    winners[y] = {
                        "winner_id": winning_team_id,
                        "loser_id": losing_team_id,
                        "round": pr,
                        "series_idx": series_idx,
                        "top_seed_won": tst_won_series,
                        "top_seed_id": tst_id,
                        "bottom_seed_id": lst_id
                    }
                if not_teams:
                    if winning_team_id not in teams:
                        teams[winning_team_id] = tst_data if tst_won_series else lst_data
                    if losing_team_id not in teams:
                        teams[losing_team_id] = tst_data if not tst_won_series else lst_data

                with exp_round:
                    cols = st.columns(3)
                    with cols[0]:
                        st.write(f"{tst_name}")
                        if tst_logo:
                            st.image(tst_logo, f"{tst_common_name} logo")
                    with cols[1]:
                        st.write(f"VS")
                        cols_rnd_results = st.columns(3)
                        # st.write(f"{tst_wins} - {lst_wins}")
                        with cols_rnd_results[0]:
                            # h = "# " if tst_won_series else "#### "
                            h = 24 if tst_won_series else 16
                            c = "#AECEFF" if tst_won_series else "#AEAEAE"
                            st.write(f"<p style='color:{c}; font-size:{h}px;'>{tst_wins}<p>", unsafe_allow_html=True)
                        with cols_rnd_results[1]:
                            st.write(f"-")
                        with cols_rnd_results[2]:
                            # st.write(f"{lst_wins}")
                            h = 24 if not tst_won_series else 16
                            c = "#AECEFF" if not tst_won_series else "#AEAEAE"
                            st.write(f"<p style='color:{c}; font-size:{h}px;'>{lst_wins}<p>", unsafe_allow_html=True)
                    with cols[2]:
                        st.write(f"{lst_name}")
                        if lst_logo:
                            st.image(lst_logo, f"{lst_common_name} logo")

                    st.write(f"{n_games} Total Games")
    else:
        st.write("Coming Soon!")

    st.divider()

with top_bar[0]:
    # for y, series_idx in winners:

    # Create the HTML container for horizontal scrolling
    # images_html = """
    #     <div style="display: flex; overflow-x: auto; white-space: nowrap;">
    # """

    # images_html = """
    #     <script>
    #         function imageClick(index) {
    #             // Pass the clicked image index to Streamlit via a custom JS function
    #             var streamlitClickEvent = new CustomEvent("streamlitImageClick", { detail: index });
    #             window.dispatchEvent(streamlitClickEvent);
    #         }
    #     </script>
    #     <div style="display: flex; overflow-x: auto; white-space: nowrap;">
    # """

    # images_html = """
    #     <script>
    #         function imageClick(index) {
    #             // Send the clicked image index to Streamlit
    #             return index;
    #         }
    #     </script>
    #     <div style="display: flex; overflow-x: auto; white-space: nowrap;">
    # """

    images_html = """
        <script>
            function imageClick(index) {
                // Send the clicked image index to Streamlit
                window.imageIndex = index;
                console.log(index);
                console.log(window);
                
                document.querySelector('button[type="submit"]').click();
            }
        </script>
        <div style="display: flex; overflow-x: auto; white-space: nowrap;">
    """

    for y, winner_data in winners.items():
        winner_id = winner_data.get("winner_id")
        loser_id = winner_data.get("loser_id")
        rnd = winner_data.get("round")
        series_idx = winner_data.get("series_idx")
        top_seed_won = winner_data.get("top_seed_won")
        top_seed_id = winner_data.get("top_seed_id")
        bottom_seed_id = winner_data.get("bottom_seed_id")

        series_data = playoff_bracket_data.get(y, {}).get("series", [])[series_idx]
        seed_key_w = "topSeedTeam" if top_seed_won else "bottomSeedTeam"
        seed_key_l = "topSeedTeam" if not top_seed_won else "bottomSeedTeam"

        image_url_w = series_data[seed_key_w]["logo"]
        caption_tn_w = series_data[seed_key_w].get("name", {}).get("default", "?")

        image_url_l = series_data[seed_key_l]["logo"]
        caption_tn_l = series_data[seed_key_l].get("name", {}).get("default", "?")

        caption_y = divmod(y, 10000)[1]
        fs = 18
        fs_l = fs - 2
        fg = "#FFFFFF"
        w_img, h_img = 100, 100

        # images_html += f'<img src="{image_url}" style="width:150px; height:150px; margin-right:10px;">'
        images_html += f'''
            <div style="text-align: center; margin-right: 15px;">
                <div onClick="imageClick({y})">
                    <div style="font-size: {fs}px; margin-top: 5px; color: {fg};">{caption_y}</div>
                    <div style="font-size: {fs}px; margin-top: 5px; color: {fg};">{caption_tn_w}</div>
                    <img src="{image_url_w}" style="width:{w_img}px; height:{h_img}px;">
                    <img src="{image_url_l}" style="width:{w_img}px; height:{h_img}px;">
                    <div style="font-size: {fs_l}px; margin-bottom: 5px; color: {fg};">{caption_tn_l}</div>
                </div>
            </div>
        '''
        # images_html += f'''
        #     <div style="text-align: center; margin-right: 15px;">
        #         <div style="font-size: {fs}px; margin-top: 5px; color: {fg};" onClick="imageClick({y})";>{caption_y}</div>
        #         <img src="{image_url}" style="width:150px; height:150px;" onClick="window.imageIndex = {y};">
        #         <div style="font-size: {fs}px; margin-bottom: 5px; color: {fg};" onClick="imageClick({y})";>{caption_tn}</div>
        #     </div>
        # '''

    images_html += "</div>"

    print(f"{images_html=}")

    with st.form(key='rerun_form'):
        rerun_button = st.form_submit_button(label="Click me to rerun")

    hyperlink_bar = st.components.v1.html(images_html, height=280, scrolling=True)

    # clicked_image_index = st.query_params.get("image_index", [None])[0]
    clicked_image_index = st.query_params.get("window.imageIndex", [None])[0]
    print(f"A {clicked_image_index=}")
    if clicked_image_index is not None:
        st.write(f"Clicked on image index: {clicked_image_index}")

    clicked_image_index = st_javascript("window.imageIndex", key="000")
    print(f"B {clicked_image_index=}")
    clicked_image_index = st_javascript("window.imageIndex", key="001")
    print(f"C {clicked_image_index=}")
    clicked_image_index = st_javascript("window.imageIndex || -1", key="002")
    print(f"D {clicked_image_index=}")
    if clicked_image_index != -1:
        st.write(f"Clicked on image index: {clicked_image_index}")

st.session_state.setdefault("dict_winners", winners)
st.session_state.setdefault("dict_teams", teams)
