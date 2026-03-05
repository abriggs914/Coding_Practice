from utils.colour_utility import Colour


class NHLTeam:

    def __init__(self, t_data):

        self.t_data = t_data
        self.t_id: str = t_data.get("id")
        self.franchise_id: str = t_data.get("franchiseId")
        self.league_id: str = t_data.get("leagueId")
        self.full_name: str = t_data.get("fullName")
        self.raw_tri_code: str = t_data.get("rawTriCode")
        self.tri_code: str = t_data.get("triCode")
        self.url_logo: str = None
        self.record: str = None

    def st_card(
            self,
            show_record: bool = True,
            logo_width: int = 75,
            bg: Colour = Colour("#676767"),
            fg: Colour = Colour("#000000")
    ) -> str:
        left_to_right = True
        jc = "flex-start" if left_to_right else "flex-end"
        html = f"<div class='card_team_{self.t_id}, style='background-color: {bg.hex_code}; foreground-color: {fg.hex_code}; display: flex; justify-content: {jc}; align-items: center;'>"
        html += f"<img src='{self.url_logo}', width='{logo_width}'>"
        if show_record:
            html += f"<h6>{self.record}</h6>"
        html += "</div>"
        return html

    def __eq__(self, other):
        return self.t_id == other.t_id

    def __repr__(self):
        return f"{self.tri_code}"