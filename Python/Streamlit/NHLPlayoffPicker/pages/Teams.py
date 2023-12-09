# from NHLPlayoffPicker import main
# from NHLPlayoffPicker.main import league
import main
import streamlit as st


if __name__ == '__main__':
    # print(f"{league}")

    if (ss_k := "loaded_images") not in st.session_state:
        st.session_state[ss_k] = False

    if not st.session_state[ss_k]:
        main.load_image_logos()

    league = main.league

    st.write("Teams")
    st.divider()

    for conf, conf_data in league.items():
        cn = conf.title()
        st.write(f"{cn}")
        st.divider()
        for div, div_data in conf_data.items():
            dn = div.title()
            st.write(f"{dn}")
            st.divider()
            for team, team_data in div_data.items():
                tn = team.title()
                st.write(f"{tn}")
                # st.write(team_data)
                if team_data["logo"] is not None:
                    img = team_data["logo"]
                    masc = team_data["mascot"].title()
                    print(f"{tn=}, {masc=}, {img=}")
                    st.image(
                        img,
                        caption=f"{tn} {masc} logo",
                        output_format="PNG"
                    )
                else:
                    st.write(f"COULD NOT LOAD IMAGE")
