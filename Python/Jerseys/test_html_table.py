from pathlib import Path

import base64
import pandas as pd
from typing import Any, Optional

def create_html_table(
    df: pd.DataFrame,
    column_config: Optional[dict[str: Any]] = None
) -> str:
    """
    Create a custom HTML table with alternate row backgrounds.

    LAST UPDATED 2024-12-19 20:41

    Args:
        df (pd.DataFrame): The DataFrame to render as an HTML table.

    Returns:
        str: The HTML string representing the table.
    """
    # Initialize the HTML table with styles
    html = '<table style="border-collapse: collapse; width: 100%;">'

    valid_configs = {
        "image": {
            # "func": lambda img, img_width="100", img_height="100": f'<td style="border: 1px solid #ddd; padding: 8px;"><img src="{img}" alt="{img}" width="{img_width}" height="{img_height}"></td>',
            "func": lambda img, img_width="100",
                           img_height="100": f'<img src="{img}" alt="{img}" width="{img_width}" height="{img_height}">',
            "args": ["img_width", "img_height"]
        }
    }

    columns = df.columns

    if column_config is None:
        column_config = {}
    else:
        to_remove = []
        for col in column_config:
            if col not in columns:
                # to_remove.append(col)
                raise ValueError(f"Unrecognized column '{col}'.")
            else:
                config_type: str = column_config[col].get("config_type")
                if config_type is None:
                    raise ValueError(
                        f"You must specify how to configure column '{col}'. Include 'config_type' as a keyword and set to one of {' '.join(list(valid_configs))}")
                config_args: list[Any] | dict[str: Any] = column_config.get("args", [])
                v_args: list[str] = valid_configs[config_type]["args"]

                if isinstance(config_args, dict):
                    for k, v in config_args.items():
                        if k not in v_args:
                            raise ValueError(
                                f"unrecognized kwarg '{k}' for {config_type=}, expected one of {' '.join(v_args)}")

                # func = valid_configs[config_type]["func"]

                # l_args = len(v_args)
                # for i, kw in enumerate(column_config[col]):
                #     val = column_config[col][kw]
                #     if i > l_args:
                #         raise ValueError(f"Got too many arguments to configure this column type ({})")

        for col in to_remove:
            del column_config[col]

    # print(f"{df=}")

    # Add table headers
    html += '<thead style="background-color: #2f2f2f; font-weight: bold;">'
    html += '<tr>'
    for col in columns:
        html += f'<th style="border: 1px solid #ddd; padding: 8px;">{col}</th>'
    html += '</tr>'
    html += '</thead>'

    # Add table rows with alternate-row styling
    html += '<tbody>'
    for i, row in df.iterrows():
        # Determine row background color
        # print(f"{i=}, {list(row)=}")
        i: int = int(i)
        bg_color = '#4f4f4f' if i % 2 == 0 else '#9f9f9f'
        html += f'<tr style="background-color: {bg_color};">'
        for j, col in enumerate(columns):
            value = row[col]
            if col in column_config:
                config_type: str = column_config[col]["config_type"]
                func = valid_configs[config_type]["func"]
                args = column_config[col].get("args", [])
                if isinstance(args, dict):
                    value = func(value, **args)
                else:
                    value = func(value, *args)
            html += f'<td style="border: 1px solid #ddd; padding: 8px;">{value}</td>'
        html += '</tr>'
    html += '</tbody>'

    # Close the table
    html += '</table>'

    return html


def encode_image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return f"data:image/png;base64,{base64.b64encode(img_file.read()).decode()}"


if __name__ == '__main__':

    data = {
        "Team": {
            "0": r"C:\Users\abriggs\Documents\Coding_Practice\Resources\Flags\icons8-usa-96.png",
            "1": r"C:\Users\abriggs\Documents\Coding_Practice\Resources\Flags\icons8-finland-96.png",
            "2": r"C:\Users\abriggs\Documents\Coding_Practice\Resources\Flags\icons8-canada-96.png",
            "3": r"C:\Users\abriggs\Documents\Coding_Practice\Resources\Flags\icons8-latvia-96.png",
            "4": r"C:\Users\abriggs\Documents\Coding_Practice\Resources\Flags\icons8-germany-96.png"
        },
        "Name": {
            "0": "USA",
            "1": "FIN",
            "2": "CAN",
            "3": "LAT",
            "4": "GER"
        },
        "tc": {
            "0": 4,
            "1": 2,
            "2": 2,
            "3": 2,
            "4": 0
        },
        "pts": {
            "0": 12,
            "1": 6,
            "2": 6,
            "3": 6,
            "4": 0
        }
    }
    column_config_ex = {
        "Team": {
            "config_type": "image",
            "args": {
                "img_width": "200",
                "img_height": "200"
            }
        }
    }

    df = pd.DataFrame(data)
    # df["Team"] = df["Team"].apply(lambda p: Path(p).resolve().as_uri())
    df["Team"] = df["Team"].apply(encode_image_to_base64)

    html = create_html_table(
        df,
        column_config=column_config_ex
    )

    print(f"{html=}")
