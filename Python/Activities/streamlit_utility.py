import math
import html
import base64
import datetime
import mimetypes
import pandas as pd
from PIL import Image
import streamlit as st
from pathlib import Path
from streamlit_js_eval import streamlit_js_eval
from typing import Literal, Optional, Iterable, Any
from streamlit.runtime.state import (
    WidgetArgs,
    WidgetCallback
)
from pandas.api.types import (
    is_numeric_dtype,
    is_datetime64_any_dtype,
    is_timedelta64_dtype,
    is_bool_dtype,
)

from colour_utility import Colour

#######################################################################################################################
#######################################################################################################################
#######################################################################################################################

VERSION = \
    """    
        Streamlit utility functions
        Version..............1.19
        Date...........2026-06-25
        Author(s)....Avery Briggs
        """


def VERSION_DETAILS():
    return VERSION.lower().split("version")[0].strip()


def VERSION_NUMBER():
    return float(".".join(VERSION.lower().split("version")[-1].split("today")[0].split(".")[-2:]).strip())


def VERSION_DATE():
    return datetime.datetime.strptime(VERSION.lower().split("today")[-1].split("author")[0].split(".")[-1].strip(),
                                      "%Y-%m-%d")


def VERSION_AUTHORS():
    return [w.removeprefix(".").strip().title() for w in VERSION.lower().split("author(s)")[-1].split("..") if
            w.strip()]


#######################################################################################################################
#######################################################################################################################
#######################################################################################################################


def aligned_text(
        txt: str,
        tag_style: Literal["h1", "h2", "h3", "h4", "h5", "h6", "p", "span"] = "h1",
        h_align: Literal["left", "center", "right"] = "center",
        colour: str = "#FFFFFF",
        line_height: int = 1
) -> str:
    """
        Return formatted HTML, and in-line CSS to h_align a given text in a container.
        Use with streamlit's markdown function and with 'unsafe_allow_html' set to True.
        See coloured_text() for streamlined-colour-only functionality.
        """
    return f"<{tag_style} style='line-height: {line_height}; text-align: {h_align}; color: {colour};'>{txt}</{tag_style}>"


def hide_image_fullscreen_buttons():
    """
        Remove ALL fullscreen buttons for images created using streamlit's image function.
        https://discuss.streamlit.io/t/hide-fullscreen-option-when-displaying-images-using-st-image/19792
        """
    hide_img_fs = '''
        <style>
        button[title="View fullscreen"]{
                visibility: hidden;}
        </style>
        '''
    st.markdown(hide_img_fs, unsafe_allow_html=True)

    hide_img_fs


def center_fullscreen_images():
    """
        Center an image when in fullscreen browsing mode
        https://discuss.streamlit.io/t/how-can-i-center-a-picture/30995/3
        """
    st.markdown(
        """
        <style>
                button[title^=Exit]+div [path_data-testid=stImage]{
                        text-align: center;
                        display: block;
                        margin-left: auto;
                        margin-right: auto;
                        width: 100%;
                }
        </style>
        """, unsafe_allow_html=True
    )


def coloured_text(
        text: str,
        colour: str | Colour = "#000000",
        html_tags: str = "span",
        call: bool = False,
        style_only: bool = False
) -> str:
    """
        Return an HTML string of text styled with a colour.
        See aligned_text() for more functionality

        :param text: Text to be rendered.
        :param colour: Text foreground colour.
        :param html_tags: The HTML text tag you want to display the text with. Wide-open and not fully tested. stick to common text elements (headers, paragraphs, etc...)
        :param call: If True the result will immediately be displayed by calling st.markdown. Not recommended if you want to place your text within another element or container.
        :param style_only: If True return the formatted HTML style string.
        :return: Formatted HTML string.
        """
    style = f"style='color:{Colour(colour).hex_code};'"
    html_ = f"<{html_tags}{' ' + style}'>{text}</{html_tags}>"
    if call:
        st.markdown(html_, unsafe_allow_html=True)
    if style_only:
        return style
    return html_


def rerun():
    # https://discuss.streamlit.io/t/is-it-possible-to-create-a-button-to-reset-relaod-the-whole-dashboard/6615/3
    import pyautogui
    pyautogui.hotkey("ctrl", "F5")


def screen_dimensions() -> tuple[Optional[int], Optional[int]]:
    """
        Use JavaScript to retrieve the screen's Width and Height as integers.
        :return: (Width, Height) as an integer tuple. May return None.
        """
    return (
        streamlit_js_eval(js_expressions='parent.innerWidth', key='SCR_W'),
        streamlit_js_eval(js_expressions='parent.innerHeight', key='SCR_H')
    )


def divider_header(
    text: str,
    boxed: bool = True,
    line_color: str = "#d0d0d0",
    text_color: str = "inherit",
    background_color: str = "#757575",
    margin: str = "1rem 0",
    font_size: str = "0.95rem",
    font_weight: int = 500,
):
    safe_text = html.escape(str(text))

    box_css = (
        f"padding: 0.15rem 0.75rem; "
        f"border: 1px solid {line_color}; "
        f"border-radius: 0.25rem;"
        if boxed
        else "padding: 0 0.65rem;"
    )

    html_string = f"""
    <div style="display:flex; align-items:center; width:100%; margin:{margin};">
        <div style="flex:1; height:1px; background:{line_color};"></div>
        <span style="color:{text_color}; background:{background_color}; font-size:{font_size}; font-weight:{font_weight}; white-space:nowrap; {box_css}">
            {safe_text}
        </span>
        <div style="flex:1; height:1px; background:{line_color};"></div>
    </div>
    """

    st.markdown(html_string, unsafe_allow_html=True)
    # st.code(html_string, language="html", line_numbers=True)
    
    
def is_time_series(s: pd.Series) -> bool:
    s2 = s.dropna()
    return not s2.empty and s2.map(lambda x: isinstance(x, datetime.time)).all()


def mean_time(s: pd.Series):
    s2 = s.dropna()
    seconds = s2.map(lambda t: t.hour * 3600 + t.minute * 60 + t.second + t.microsecond / 1_000_000)
    avg = seconds.mean()

    h = int(avg // 3600) % 24
    m = int((avg % 3600) // 60)
    sec = int(avg % 60)

    return datetime.time(h, m, sec)


def can_aggregate(s: pd.Series, agg: str) -> bool:
    numeric_aggs = {"sum", "mean", "median", "std", "var", "sem", "prod", "skew"}
    order_aggs = {"min", "max", "first", "last"}
    count_aggs = {"count", "size", "nunique"}
    bool_aggs = {"any", "all"}

    if agg in count_aggs:
        return True

    if agg in bool_aggs:
        return is_bool_dtype(s) or s.dropna().map(lambda x: isinstance(x, bool)).all()

    if agg in order_aggs:
        return True

    if agg in numeric_aggs:
        return (
            is_numeric_dtype(s)
            or is_datetime64_any_dtype(s)
            or is_timedelta64_dtype(s)
            or is_time_series(s)
        )

    return False


def safe_aggregate(s: pd.Series, agg: str):
    if not can_aggregate(s, agg):
        return None

    if agg == "mean" and is_time_series(s):
        return mean_time(s)

    try:
        return s.aggregate(agg)
    except Exception:
        return None


def display_df(
    df: pd.DataFrame | pd.Series,
    title: Optional[str] = None,
    hide_index: Optional[str | bool] = "if_int",
    show_shape: Literal[True, False, "separate", "below"] = True,
    fail_safe: Optional[Any] = True,
    warn_fail_safe: Optional[Any] = True,
    border: Optional[bool] = None,
    debug: bool = False,

    # params for st.dataframe 20250325
    width: int | str = "stretch",
    height: int | str = "auto",
    use_container_width: bool = False,
    column_order: Optional[Iterable[str]] = None,
    column_config: Optional[dict] = None,
    key: Any = None,
    on_select: Literal["ignore", "rerun"] | Any = "ignore",
    selection_mode: Any = "multi-row",
    editor: bool = False,
    num_rows: Literal["fixed", "dynamic", "add", "delete"] = "fixed",
    disabled: bool | Iterable[str | int] = False,
    on_change: Optional[WidgetCallback] = None,
    args: Optional[WidgetArgs] = None,
 
     # params for st.dataframe 20260514
    selection_default: Optional[dict] = None,
    row_height: Optional[int] = None,
    placeholder: Optional[str] = None,
    
    totals: Any = None,
):
    border = bool(border) or (bool(totals) and (border is None))
    with st.container(border=border):
        try:
            title = title if title else ""
            sub_title = ""
            shape = df.shape
            if show_shape:
                if isinstance(show_shape, bool):
                    # st.write(f"{len(shape)=}")
                    title = f"{title} " + (f"({shape[0]} Rows x {shape[1]} Cols)" if len(shape) > 1 else (f"({len(df)} Rows x 1 Col)" if isinstance(df, pd.Series) else "")).strip()
                else:
                    sub_title = f"({shape[0]} Rows x {shape[1]} Cols)" if len(shape) > 1 else (f"({len(df)} Rows x 1 Col)" if isinstance(df, pd.Series) else "")
        
            if title:
                st.write(title)
            if sub_title and (show_shape != "below"):
                st.caption(sub_title)

            if (not editor) and (hide_index == "if_int"):
                hide_index = str(df.index.dtype).lower() == "int64"
            elif editor and (hide_index == "if_int"):
                hide_index = None
            
            if debug:
                
                de_defaults = dict(
                    width = "stretch",
                    height = "auto",
                    use_container_width = None,
                    hide_index = None,
                    column_order = None,
                    column_config = None,
                    num_rows = "fixed",
                    disabled = False,
                    key = None,
                    on_change = None,
                    args = None,
                    row_height = None,
                    placeholder = None,
                )
                
                kwargs = dict(
                    title=title,
                    hide_index=hide_index,
                    show_shape=show_shape,
                    fail_safe=fail_safe,
                    border=border,

                    # params for st.dataframe 20250325
                    width=width,
                    height=height,
                    use_container_width=use_container_width,
                    column_order=column_order,
                    column_config=column_config,
                    key=key,
                    on_select=on_select,
                    selection_mode=selection_mode,
                    editor=editor,
                    num_rows=num_rows,
                    disabled=disabled,
                    on_change=on_change,
                    args=args,
                
                    # params for st.dataframe 20260514
                    selection_default=selection_default,
                    row_height=row_height,
                    placeholder=placeholder,
                )
                st.write("kwargs")
                st.write(kwargs)
                st.write("de_defaults")
                st.write(de_defaults)
                # in_valid = {k: [kwargs[k], de_defaults[k]] for k, v in de_defaults.items() if de_defaults[k] != kwargs[k]}
                in_valid = {k: (kwargs[k] if k in kwargs else v) for k, v in de_defaults.items()}
                st.write("valid:")
                st.write(not in_valid)
                if in_valid:
                    st.write("INVALID:")
                    st.write(in_valid)
                    
            if debug:
                xxx = dict(
                    data=df,
                    hide_index=hide_index,
                    width=width,
                    height=height,
                    use_container_width=use_container_width,
                    column_order=column_order,
                    column_config=column_config,
                    key=key,
                    num_rows=num_rows,
                    on_change=on_change,
                    row_height=row_height,
                    placeholder=placeholder,
                    args=args,
                    disabled=disabled,)
                st.write(f"xxx")
                st.write(xxx)

            if editor:
                if debug:
                    st.write(f"DE {title=}, {hide_index=}")
                    st.write("columns")
                    st.write(df.columns.tolist())
                stdf = st.data_editor(
                    data=df,
                    hide_index=hide_index,
                    width=width,
                    height=height,
                    use_container_width=use_container_width,
                    column_order=column_order,
                    column_config=column_config,
                    key=key,
                    num_rows=num_rows,
                    on_change=on_change,
                    row_height=row_height,
                    placeholder=placeholder,
                    args=args,
                    disabled=disabled,
                )
            else:
                if debug:
                    st.write(f"DF {title=}, {hide_index=}")
                    st.write("columns")
                    st.write(df.columns.tolist())
                stdf = st.dataframe(
                    data=df,
                    hide_index=hide_index,
                    width=width,
                    height=height,
                    use_container_width=use_container_width,
                    column_order=column_order,
                    column_config=column_config,
                    key=key,
                    on_select=on_select,
                    selection_mode=selection_mode,
                    selection_default=selection_default,
                    row_height=row_height,
                    placeholder=placeholder,
                )
            if sub_title and (show_shape == "below"):
                st.markdown(
                    f"""
                    <div style="
                        width: 100%;
                        text-align: right;
                        color: rgba(128, 128, 128, 0.9);
                        font-size: 0.8rem;
                        margin-top: -0.35rem;
                        padding-top: 0;
                    ">
                        {sub_title}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
            if totals is not None:
                valid_agg = [
                    "sum", "mean", "median", "min", "max", "count",
                    "size", "std", "var", "sem", "prod", "first",
                    "last", "nunique", "any", "all", "skew",
                ]
                t_vals = {}
                aggs_used = []
                if isinstance(totals, dict):
                    for c, v_ in totals.items():
                        if c not in df.columns:
                            raise KeyError(f"column '{c}' in 'totals' was not found in the dataframe columns.")
                        if isinstance(v_, (list, tuple)):
                            t_vals[c] = []
                            for v in v_:
                                if v not in valid_agg:
                                    raise ValueError(f"aggregate '{v}' in 'totals' is not recognized as a valid aggregate function.")
                                t_vals[c].append(v)
                                if v not in aggs_used:
                                    aggs_used.append(v)
                        else:
                            t_vals[c] = [v_]
                            if v_ not in aggs_used:
                                aggs_used.append(v_)
                            
                elif isinstance(totals, (list, tuple)):
                    for c in df.columns:
                        t_vals[c] = []
                        for v in totals:
                            if v not in valid_agg:
                                raise ValueError(f"aggregate '{v}' in 'totals' is not recognized as a valid aggregate function.")
                            t_vals[c].append(v)
                            if v not in aggs_used:
                                aggs_used.append(v)
                            
                elif isinstance(totals, str):
                    if totals not in valid_agg:
                        raise ValueError(f"aggregate '{totals}' is not recognized as a valid aggregate function.")
                    for c in df.columns:
                        t_vals[c] = [totals]
                        if totals not in aggs_used:
                            aggs_used.append(totals)
                
                if t_vals:
                    # st.write(df.describe())
                    df_t = pd.DataFrame([[None] * len(df.columns.tolist()) for _ in range(len(aggs_used))], index=aggs_used, columns=df.columns)
                    for c in df.columns:
                        for i, a in enumerate(t_vals.get(c, [])):
                            # st.write(f"{c=}, {i=}, {a=}") 
                            s = df[c].dropna()
                            if a == "mean" and len(s) and s.map(lambda x: isinstance(x, datetime.time)).all():
                                df_t.loc[a, c] = mean_time(s)
                            else:
                                df_t.loc[a, c] = safe_aggregate(df[c], a)
                    
                    divider_header("Totals:", font_size="1.12rem")
                    display_df(df_t, show_shape=False)
                        
        except Exception as e:
            if isinstance(fail_safe, bool):
                fail_safe = st.write if fail_safe else None
            if fail_safe is not None:
                if warn_fail_safe:
                    st.warning("display_df fail-safe evoked.")
                stdf = None
                if callable(fail_safe):
                    try:
                        fail_safe(df)
                    except:
                        pass
                else:
                    st.write(df)
            else:
                raise e
    
    return stdf


def consolidate_df_edits(df: pd.DataFrame, editor_data: dict) -> pd.DataFrame:
    """Use with a data_editor to quickly retrieve a copy of the data currently modeled in the editor."""
    edited_rows = editor_data.get("edited_rows", {})
    added_rows = editor_data.get("added_rows", [])
    deleted_rows = editor_data.get("deleted_rows", [])

    dff = df.copy()
    for idx, changes in edited_rows.items():
        for col, val in changes.items():
            dff.loc[idx, col] = val
            
    for idx in deleted_rows:
        dff.drop(index=deleted_rows, inplace=True)

    if added_rows:
        dff = pd.concat([dff, pd.DataFrame(added_rows)], ignore_index=True)
        
    return dff


@st.cache_data(ttl=None, show_spinner=True)
def load_pdf_binary(pdf_file):
    with open(pdf_file, "rb") as f:
        return f.read()
    

@st.cache_data(show_spinner=False)
def split_frame(input_df: pd.DataFrame, rows: int):
    if input_df.shape[0] <= rows:
        return [input_df]
    # st.write(f"{rows=}")
    df = [input_df.reset_index(drop=True).loc[i : i + rows - 1, :] for i in range(0, input_df.shape[0] + rows, rows)]
    return df


def display_df_paginated(
    df: pd.DataFrame | pd.Series,
    title: Optional[str] = None,
    hide_index: str | bool = "if_int",
    show_shape: bool = True,
    batch_size_options: list[int] = (25, 50, 100),

    # params for st.dataframe 20250325
    width: int | None = None,
    height: int | None = None,
    use_container_width: bool = False,
    column_order: Iterable[str] | None = None,
    column_config: Any | None = None,
    key: Any | None = None,
    on_select: Literal["ignore", "rerun"] | Any = "ignore",
    selection_mode: Any = "multi-row",
    editor: bool = False,
    num_rows: Literal["fixed", "dynamic", "add", "delete"] = "fixed",
    disabled: bool | Iterable[str | int] = False,
    on_change: WidgetCallback | None = None,
    args: WidgetArgs | None = None,
 
     # params for st.dataframe 20260514
    selection_default: dict | None = None,
    row_height: int | None = None,
    placeholder: str | None = None,
    
    debug: bool = False
):
    
    if key is None:
        # sub_widget_keys = f"stdf_paginated_{datetime.datetime.now():%Y%m%d%%H%M%S}"
        msg = f"You must pass a key for a paginated dataframe widget. Otherwise sub-widgets won't have state-persistence."
        st.error(msg)
        raise ValueError(msg)
    else:
        sub_widget_keys = key

    top_menu = st.columns(3)
    with top_menu[0]:
        sort = st.radio(
            label="Sort Data",
            options=["Yes", "No"],
            horizontal=1,
            index=1,
            key=f"{sub_widget_keys}_radio_sort_col"
        )
    if sort == "Yes":
        with top_menu[1]:
            sort_field = st.selectbox("Sort By", options=df.columns)
        with top_menu[2]:
            sort_direction = st.radio(
                label="Direction",
                options=["⬆️", "⬇️"],
                horizontal=True,
                key=f"{sub_widget_keys}_radio_sort_dir"
            )
        df.sort_values(
            by=sort_field,
            ascending=sort_direction == "⬆️",
            ignore_index=True,
            inplace=True
        )
    pagination = st.container()

    bottom_menu = st.columns((4, 1, 1))
    with bottom_menu[2]:
        batch_size = st.selectbox(
            label="Page Size",
            options=batch_size_options,
            key=f"{sub_widget_keys}_selectbox_batch_size"
        )
    with bottom_menu[1]:
        total_pages = (
            math.ceil(len(df) / batch_size) if int(len(df) / batch_size) > 0 else 1
        )
        current_page = st.number_input(
            label="Page",
            min_value=1,
            max_value=total_pages,
            step=1,
            key=f"{sub_widget_keys}_number_input_pages"
        )
    with bottom_menu[0]:
        st.markdown(f"Page **{current_page}** of **{total_pages}** ")
        st.markdown(f"**{df.shape[0]}** total records")

    pages = split_frame(df, batch_size)
    # st.write(f"{len(pages)=}")
    # st.write(f"{[len(p) for p in pages]=}")
    # st.write(f"{batch_size=}")
    with pagination:
        return display_df(
            df=pages[current_page - 1].reset_index(drop=True) if pages else pd.DataFrame(data=[{"data": None}]),
            title=title,
            hide_index=hide_index,
            show_shape=show_shape,

            width=width,
            height=height,
            use_container_width=use_container_width,
            column_order=column_order,
            column_config=column_config,
            key=key,
            on_select=on_select,
            selection_mode=selection_mode,
            editor=editor,
   
            selection_default=selection_default,
            row_height=row_height,
            placeholder=placeholder,
            debug=debug
        )  
  

def in_streamlit() -> bool:
    """Detect whether there is an active Streamlit script context"""
    try:
            from streamlit.runtime.scriptrunner import get_script_run_ctx
            return get_script_run_ctx() is not None
    except Exception:
            return False


def get_selected_rows(df: pd.DataFrame, stdf, cols=None, n=1, id_mode: bool = False, debug: bool = False) -> Any:
    cols_in = cols.copy() if isinstance(cols, (list, tuple, dict)) else ([cols] if isinstance(cols, (int, str)) else cols)
    cols_og = {col: col.lower().strip() for col in (df.columns if cols is None else (cols if isinstance(cols, (list, tuple, type(pd.DataFrame(data={"data": []}).columns))) else [cols]))}
    cols = list(cols_og.values())
    if debug:
        st.write(f"stdf")
        st.write(stdf)
        st.write(f"A {cols=}")
        st.write(f"A {cols_og=}")
        st.write(f"A {cols_in=}")
        # st.write(f"{type(df.columns)=}")
    if (isinstance(stdf, pd.DataFrame) and (not stdf.empty)) or stdf:
        cols_to_check = [
            "selection",
            "selected",
            "included",
            "include",
            "+"
        ]
        stdf_columns = stdf.columns if isinstance(stdf, (pd.DataFrame, pd.Series)) else stdf.get("columns", [])
        cols_to_check_found = [col for col in cols_to_check if col in stdf_columns]
        if bool([col for col in cols_to_check if col in (df.columns if hasattr(df, "columns") else dict(df))]):
            if debug:
                st.write("--A")
            st.write("cols_to_check_found")
            st.write(cols_to_check_found)
            for col in cols_to_check_found:
                stdf = stdf[stdf[col] == True].reset_index()
            if id_mode:
                idxs = stdf.index.to_list()
                if (n == 1) and idxs:
                    return idxs[0]
                else:
                    return idxs
            else:
                return stdf.iloc[0] if n == 1 else stdf
        # st.write(f"B {cols=}")
        # st.write(f"{df.columns=}")
        # st.write(f"{stdf.keys()=}")
        if stdf["selection"]:
            if stdf["selection"]["rows"]:
                if n == 1:
                    if debug:
                        st.write("--B")
                    try:
                        if len(cols_in) == 1:
                            if id_mode:
                                return stdf["selection"]["rows"][0]
                            else:
                                return df.reset_index().loc[stdf["selection"]["rows"][0]][cols_in[0]]
                        else:
                            return df.reset_index().loc[stdf["selection"]["rows"][0], cols_in]
                    except KeyError as ke:
                        if not cols_in:
                            raise KeyError(f"Try setting explicit column names for param 'cols': " + str(ke))
                        else:
                            raise ke
                else:
                    if debug:
                        st.write("--C")
                    if n is None:
                        n = len(stdf["selection"]["rows"])
                    if id_mode:
                        return stdf["selection"]["rows"][:n]
                    return df.reset_index().rename(columns=cols_og).loc[stdf["selection"]["rows"][:n], cols].rename(columns={v: k for k, v in cols_og.items()})
    return pd.DataFrame()


def local_image_to_data_url(path: str | Path) -> str | None:
    if not path:
        return
    
    path = Path(path)

    if not path.exists():
        return

    mime_type, _ = mimetypes.guess_type(path)
    mime_type = mime_type or "image/png"

    data = base64.b64encode(path.read_bytes()).decode("utf-8")
    return f"data:{mime_type};base64,{data}"


@st.cache_data(show_spinner=False)
def local_image_thumbnail_data_url(
    path: str,
    max_size: tuple[int, int] | int = (96, 96),
    quality: int = 70,
) -> str | None:
    
    if not path:
        return
    
    path = Path(path)

    if not path.exists():
        return None
    
    if isinstance(max_size, int):
        max_size = (max_size, max_size)

    img = Image.open(path)
    img.thumbnail(max_size)

    thumb_path = Path(st.session_state.get("_thumb_dir", ".thumb_cache"))
    thumb_path.mkdir(exist_ok=True)

    out_path = thumb_path / f"{path.stem}_thumb.webp"
    img.save(out_path, format="WEBP", quality=quality)

    data = base64.b64encode(out_path.read_bytes()).decode("utf-8")
    return f"data:image/webp;base64,{data}"


if __name__ == '__main__':
    st.set_page_config(layout="wide")

    text = "Hello World"
    st.markdown(aligned_text(text, colour="#569072", tag_style="h6", line_height=50), unsafe_allow_html=True)
