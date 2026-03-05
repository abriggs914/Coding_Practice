import datetime
import numpy as np
import streamlit as st
from PIL import Image, ImageDraw
from typing import Optional
from sklearn.cluster import KMeans
from collections import Counter

from utils.colour_utility import Colour
from utils.datetime_utility import is_leap_year


def get_this_season_str() -> str:
    now = datetime.datetime.now()
    year = now.year
    month = now.month
    if month < 7 or 8 < month:
        return f"{year}{year+1}"
    else:
        return "off"


def f_season(season_str) -> str:
    ss = str(season_str)
    return f"{ss[:4]}-{ss[-4:]}"


def f_standing_record(w, l, so_otl) -> str:
    return f"{w}-{l}-{so_otl}"


def game_state_translate(game_state: str) -> tuple[str, Colour, Colour]:
    bg = Colour("#525252")
    fg = Colour("#FFFFFF")
    match game_state:
        case "FUT":
            bg = Colour("#52F252")
            fg = Colour("#0823FF")
            return "Upcoming", bg, fg
        case "OFF":
            bg = Colour("#9292F2")
            fg = Colour("#FF0000")
            return "Final", bg, fg
        case _:
            return game_state.title(), bg, fg


def quantize_image_colors(image_array, n_bins=10):
    """Reduce the number of colors via rounding to unify similar tones"""
    return (image_array // (256 // n_bins)) * (256 // n_bins)


def remove_background(image_array, bg_threshold=25):
    """Remove near-black background from pixels"""
    return image_array[
        (image_array[:, 0] > bg_threshold) |
        (image_array[:, 1] > bg_threshold) |
        (image_array[:, 2] > bg_threshold)
    ]


def merge_similar_clusters(cluster_centers, proportions, threshold=20):
    merged = []
    used = set()

    for i, center in enumerate(cluster_centers):
        if i in used:
            continue
        merged_color = center
        merged_prop = proportions[i]
        for j in range(i + 1, len(cluster_centers)):
            if j in used:
                continue
            dist = np.linalg.norm(center - cluster_centers[j])
            if dist < threshold:
                merged_color = (merged_color * merged_prop + cluster_centers[j] * proportions[j]) / (merged_prop + proportions[j])
                merged_prop += proportions[j]
                used.add(j)
        used.add(i)
        merged.append((merged_color, merged_prop))
    return merged


def get_color_at_position(gradient_img: Image.Image, position: float) -> str:
    """Sample the color from a horizontal gradient image at a given relative position (0–1)."""
    width = gradient_img.width
    x = min(int(position * width), width - 1)
    rgb = gradient_img.getpixel((x, 0))
    return '#{:02x}{:02x}{:02x}'.format(*rgb)


@st.cache_data
def extract_dominant_colours(image_path, num_colours=3, resize=True):
    image = Image.open(image_path)

    if resize:
        image = image.resize((300, 300))  # Speed up processing

    # Convert to numpy and reshape
    image_array = np.array(image)
    image_array = image_array.reshape((-1, 3))

    # Preprocess: remove background and quantize
    image_array = remove_background(image_array, bg_threshold=60)
    image_array = quantize_image_colors(image_array, n_bins=32)

    # KMeans clustering
    kmeans = KMeans(n_clusters=num_colours, random_state=42)
    labels = kmeans.fit_predict(image_array)
    counts = Counter(labels)

    total_pixels = sum(counts.values())
    center_colours = kmeans.cluster_centers_
    proportions = [counts[i] / total_pixels for i in range(len(center_colours))]

    # Merge similar clusters
    merged = merge_similar_clusters(center_colours, proportions, threshold=30)

    # Convert to hex + sort
    colours = []
    for rgb, prop in merged:
        hex_colour = '#{:02x}{:02x}{:02x}'.format(int(rgb[0]), int(rgb[1]), int(rgb[2]))
        colours.append((hex_colour, prop))

    colours.sort(key=lambda x: x[1], reverse=True)
    return colours


def generate_color_gradient(colour_data, width=600, height=50):
    """
    Create a horizontal color gradient bar from the dominant colors.
    :param colour_data: List of (hex_color, proportion)
    :param width: Total width of the image
    :param height: Height of the gradient bar
    :return: PIL Image object
    """
    gradient = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(gradient)

    current_x = 0
    for hex_color, proportion in colour_data:
        color_width = int(proportion * width)
        draw.rectangle([current_x, 0, current_x + color_width, height], fill=hex_color)
        current_x += color_width

    return gradient


def seconds_to_clock(seconds_left: int) -> str:
    t_sec: int = 20*60  # 20 minutes
    p_sec: float = 1 - (seconds_left / t_sec)
    # (hour : 1/2 hour) === (x : x + 12)
    clocks = [
        ("0100", "&#128336"),
        ("0130", "&#128348"),
        ("0200", "&#128337"),
        ("0230", "&#128349"),
        ("0300", "&#128338"),
        ("0330", "&#128350"),
        ("0400", "&#128339"),
        ("0430", "&#128351"),
        ("0500", "&#128340"),
        ("0530", "&#128352"),
        ("0600", "&#128341"),
        ("0630", "&#128353"),
        ("0700", "&#128342"),
        ("0730", "&#128354"),
        ("0800", "&#128343"),
        ("0830", "&#128355"),
        ("0900", "&#128344"),
        ("0930", "&#128356"),
        ("1000", "&#128345"),
        ("1030", "&#128357"),
        ("1100", "&#128346"),
        ("1130", "&#128358"),
        ("1200", "&#128347"),
        ("1230", "&#128359")
    ]
    # 24 segments
    p_sec: int = int(round(p_sec * len(clocks)))
    print(f"sl={seconds_left}, ts={t_sec}, ps={p_sec}, lc={len(clocks)}")
    if (p_sec == 0) or (p_sec == len(clocks)):
        # default show 1200
        return clocks[-2][1]
    return clocks[p_sec][1]


def date_to_this_year(date_in: datetime.date | datetime.datetime, to_year: Optional[int] = None) -> datetime.date | datetime.datetime:
    date_now = datetime.datetime.now() if to_year is None else datetime.datetime(to_year, 1, 1)
    leap_in = is_leap_year(date_in)
    leap_now = is_leap_year(date_now)
    if leap_in and not leap_now:
        if date_in.month == 2 and date_in.day == 29:
            date_in = date_in - datetime.timedelta(days=1)

    date_in = date_in.replace(year=date_now.year)
    return date_in