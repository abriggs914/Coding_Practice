import pandas as pd
import os
import json
import datetime

from utils.colour_utility import Colour
from resources.resource import PATH_FOLDER_JERSEY_COLLECTION


class NHLJerseyCollection:
    def __init__(self, excel_path: str, colour_edits_save_file: str = None):
        self.df_jc_data: pd.DataFrame = pd.read_excel(excel_path)
        self.df_jc_data = self.df_jc_data.loc[~pd.isna(self.df_jc_data["ID"])]
        self.df_jc_data["ID"] = self.df_jc_data["ID"].astype(int)
        self.df_jc_data.sort_values(by="ID", ascending=True, inplace=True)

        date_cols = [
            "OrderDate",
            "ReceiveDate",
            "OpenDate",
            "DOB"
        ]
        for col in date_cols:
            self.df_jc_data[col] = pd.to_datetime(self.df_jc_data[col])

        int_cols = ["ID", "NHLID"]
        for col in int_cols:
            self.df_jc_data[col] = self.df_jc_data[col].apply(lambda x: f"{int(x):.0f}" if not pd.isna(x) else None)

        def nz(val, default=None):
            if pd.isnull(val):
                return default
            if pd.isna(val):
                return default
            return val

        self.df_jc_data["PriceCalc"] = self.df_jc_data.apply(
            lambda row:
                ((nz(row["ExchangeRate"], 1) * (row["StickerPriceUS"] + nz(row["Shipping"], 0) + nz(row["Tax"], 0)))
                + nz(row["Duty"], 0) - nz(row["Discount"], 0)) if not pd.isna(row["StickerPriceUS"]) else (
                    ((row["StickerPriceCDN"] + nz(row["Duty"], 0) + nz(row["Shipping"], 0) + nz(row["Tax"], 0)) - nz(row["Discount"], 0)) if not pd.isna(row["StickerPriceCDN"]) else None
                ), axis=1)
            # iif(
                # not isnull(jerseys.stickerpriceus),
                # (
                #         (
                #                 jerseys.exchangerate * (
                #                 Jerseys.StickerPriceus + iif(isnull(Jerseys.Shipping), 0, Jerseys.Shipping) + iif(
                #             isnull(jerseys.tax), 0, jerseys.tax)
                #         )
                #         ) + iif(isnull(Jerseys.Duty), 0, Jerseys.Duty) - iif(isnull(jerseys.discount), 0,
                #                                                              jerseys.discount)
                # ),
                # iif(
                #     not isnull(jerseys.stickerpricecdn),
                #     (
                #             (
                #                     Jerseys.StickerPriceCDN + iif(isnull(Jerseys.Duty), 0, Jerseys.Duty) + iif(
                #                 isnull(Jerseys.Shipping), 0, Jerseys.Shipping) + iif(isnull(jerseys.tax), 0,
                #                                                                      jerseys.tax)
                #             ) - iif(isnull(jerseys.discount), 0, jerseys.discount)
                #     ),
                #     -1
                # )
        #     )
        #     axis=1
        # )

        if colour_edits_save_file is not None:
            self.correct_colours(colour_edits_save_file)

        self.df_jerseys: pd.DataFrame = self.df_jc_data.loc[
            ~self.df_jc_data["Cancelled"]
        ]
        self.df_cancelled_jerseys: pd.DataFrame = self.df_jc_data.loc[
            self.df_jc_data["Cancelled"]
        ]

        self.first_date: datetime.date = self.df_jerseys["OrderDate"].min().date()
        self.last_date: datetime.date = self.df_jerseys["OrderDate"].max().date()

        self.jerseys: dict[int: Jersey] = {}
        for i, row in self.df_jerseys.iterrows():
            j_id = row["ID"]
            league: str = row["League"]
            is_nhl: bool = league == "NHL"
            if is_nhl:
                self.jerseys[j_id] = NHLJersey(row)
            else:
                self.jerseys[j_id] = Jersey(row)

        self.df_jerseys["JerseyToString"] = self.df_jerseys.apply(lambda row: self.jerseys[row["ID"]].to_string(), axis=1)

    def __repr__(self):
        return f"NHLJerseyCollection: {self.df_jerseys.shape[0]} jerseys between {self.first_date} and {self.last_date}"

    def correct_colours(self, colour_edits_save_file):
        print(f"correct_colours")
        if os.path.exists(os.path.join(os.getcwd(), colour_edits_save_file)):
            print(f"found file")
            with open(colour_edits_save_file, "r") as f:
                colour_edits: dict[str: list[str]] = json.load(f)
            for j_id, lst_colours in colour_edits.items():
                print(f"{j_id=}")
                df_id = self.df_jc_data.loc[self.df_jc_data["ID"] == int(j_id)]
                print(df_id)
                if not df_id.empty:
                    for i, row in df_id.iterrows():
                        for j, col in enumerate(lst_colours):
                            self.df_jc_data.loc[i, f"Colour{j+1}"] = col


class Jersey:
    def __init__(self, j_data: dict | pd.Series):
        self.j_data: dict = j_data if isinstance(j_data, dict) else j_data.to_dict()
        self.j_id: int = j_data["ID"]
        self.image_folder: str = os.path.join(PATH_FOLDER_JERSEY_COLLECTION, f"J_{('000' + str(self.j_id))[-3:]}")
        if not os.path.exists(self.image_folder):
            self.image_folder = ""
            self.n_images: int = 0
        else:
            self.n_images: int = len(os.listdir(self.image_folder))

        self.cancelled: bool = j_data.get("Cancelled", False)
        self.league: str = j_data.get("League", "NHL")
        self.team: str = j_data.get("Team")
        self.tournament: str = j_data.get("Tournament")
        self.conference: str = j_data.get("Conference")
        self.division: str = j_data.get("Division")
        self.c_patch: bool = j_data.get("CPatch")
        self.a_patch: bool = j_data.get("APatch")
        self.number: int = None if pd.isna(j_data.get("Number")) else int(j_data.get("Number"))
        self.player_first: str = None if pd.isna(j_data.get("PlayerFirst")) else j_data.get("PlayerFirst")
        self.player_last: str = None if pd.isna(j_data.get("PlayerLast")) else j_data.get("PlayerLast")
        self.colour_1: str = j_data.get("Colour1")
        self.colour_2: str = j_data.get("Colour2")
        self.colour_3: str = j_data.get("Colour3")
        self.order_date: datetime.date = j_data.get("OrderDate").date()
        self.receive_date: datetime.date = j_data.get("ReceiveDate").date()
        self.open_date: datetime.date = j_data.get("OpenDate").date()
        self.manufacture_date: str = j_data.get("ManufactureDate")
        self.brand: str = None if pd.isna(j_data.get("Brand")) else j_data.get("Brand")
        self.make: str = None if pd.isna(j_data.get("Make")) else j_data.get("Make")
        self.model: str = None if pd.isna(j_data.get("Model")) else j_data.get("Model")
        self.size: str = j_data.get("Size")
        self.supplier: str = j_data.get("Supplier")
        self.us_sale: bool = j_data.get("USSale", False)
        self.exchange_rate: float = j_data.get("ExchangeRate")
        self.sticker_price_cdn: float = j_data.get("StickerPriceCDN")
        self.sticker_price_us: float = j_data.get("USStickerPriceUS")
        self.duty: float = j_data.get("Duty")
        self.shipping: float = j_data.get("Shipping")
        self.discount: float = j_data.get("Discount")
        self.discount_reason: str = j_data.get("DiscountReason")
        self.tax: float = j_data.get("Tax")
        self.price_c: float = j_data.get("PriceC")
        self.price_m: float = j_data.get("PriceM")
        self.nhl_id: str = j_data.get("NHLID")
        self.position: str = j_data.get("Position")
        self.nationality: str = j_data.get("Nationality")
        self.dob: datetime.date = j_data.get("DOB")
        self.retire_date: str = j_data.get("RetireDate")
        self.first_season: str = j_data.get("FirstSeason")
        self.last_season: str = j_data.get("LastSeason")
        self.nhl_uniform_link: str = j_data.get("NHLUniformLink")
        self.notes: str = j_data.get("Notes")

        if self.j_id is None:
            raise ValueError(f"{self.j_id} cannot be None")

    def get_colours(self):
        return list(map(Colour, [c for c in [self.colour_1, self.colour_2, self.colour_3] if not pd.isna(c)]))

    def is_blank(self) -> bool:
        return (self.number is None) and (self.player_last is None)

    def to_string(
            self,
            inc_team: bool = None,
            inc_brand: bool = None,
            inc_make: bool = None,
            inc_model: bool = None,
            inc_num: bool = None,
            inc_fname: bool = None,
            inc_lname: bool = None,
            inc_size: bool = None
    ) -> str:
        res = []
        if inc_team is None:
            inc_team = True
        if inc_brand is None:
            inc_brand = True
        if inc_make is None:
            inc_make = True
        if inc_model is None:
            inc_model = True

        if inc_num is None:
            inc_num = not self.is_blank()
        if inc_fname is None:
            inc_fname = not self.is_blank()
        if inc_lname is None:
            inc_lname = not self.is_blank()

        if inc_size is None:
            inc_size = True

        if inc_team and bool(self.team):
            res.append(self.team)
        if inc_brand and bool(self.brand):
            res.append(self.brand)
        if inc_make and bool(self.make):
            res.append(self.make)
        if inc_model and bool(self.model):
            res.append(self.model)
        if inc_num and bool(self.number):
            res.append(f"#{self.number}")
        if inc_fname and bool(self.player_first):
            res.append(self.player_first)
        if inc_lname and bool(self.player_last):
            res.append(self.player_last)
        if inc_size and bool(self.size):
            res.append(self.size)
        return " ".join(map(str, res))

    def __repr__(self) -> str:
        return self.to_string()


class NHLJersey(Jersey):
    def __init__(self, j_data: dict | pd.Series):
        super().__init__(j_data)


class IIHFJersey(Jersey):
    def __init__(self, j_data: dict | pd.Series):
        super().__init__(j_data)


class PWHLJersey(Jersey):
    def __init__(self, j_data: dict | pd.Series):
        super().__init__(j_data)


class QMJHLJersey(Jersey):
    def __init__(self, j_data: dict | pd.Series):
        super().__init__(j_data)