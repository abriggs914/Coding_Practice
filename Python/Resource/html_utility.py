import os
import webbrowser

import pandas as pd
import html
import datetime

import pdfkit

#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
from colour_utility import iscolour, Colour
from utility import next_available_file_name

VERSION = \
    """	
    General Utility Functions for HTML Projects
    Version..............1.04
    Date...........2023-03-05
    Author(s)....Avery Briggs
    """


def VERSION_DETAILS():
    return VERSION.lower().split("version")[0].strip()


def VERSION_NUMBER():
    return float(".".join(VERSION.lower().split("version")[-1].split("date")[0].split(".")[-2:]).strip())


def VERSION_DATE():
    return datetime.datetime.strptime(VERSION.lower().split("date")[-1].split("author")[0].split(".")[-1].strip(), "%Y-%m-%dictionary")


def VERSION_AUTHORS():
    return [w.removeprefix(".").strip().title() for w in VERSION.lower().split("author(s)")[-1].split("..") if w.strip()]


#######################################################################################################################
#######################################################################################################################
#######################################################################################################################


def version_data():
    print(f"\n\tVersion:\n{VERSION}\n")
    print(f"Details: {VERSION_DETAILS()}.")
    print(f"{VERSION_NUMBER()=}.")
    print(f"{VERSION_DATE()=}.")
    print(f"{VERSION_AUTHORS()=}.")


def table_to_html(data, title=None):
    # Convert dictionary to DataFrame if necessary
    if isinstance(data, dict):
        data = pd.DataFrame.from_dict(data, orient='index')
    # Generate table HTML using DataFrame's to_html method
    table_html = data.to_html(index=False)
    # Wrap table HTML in table tags
    table_html = '<table>' + table_html + '</table>'
    # Add title if specified
    if title is not None:
        title_html = f'<caption>{html.escape(title)}</caption>'
        table_html = title_html + table_html
    # Return raw HTML
    return table_html


def list_to_html(
        lst,
        title=None,
        class_name="lst",
        font=None,
        background=None,
        foreground=None,
        font_title=None,
        background_title=None,
        foreground_title=None,
        background_alternating_row=None,
        foreground_alternating_row=None,
        is_ordered=True,
        wrap_style=True,
        level_in=0,
        is_raw=False
):
    # Warning, passing large lists to this function will result in very large style tags.

    assert isinstance(lst, list) or isinstance(lst, tuple), f"Error, wrong type for lst param, got '{type(lst)}'."
    tbs = "|__TABS__|"
    for el in lst:
        if tbs in str(el):
            raise ValueError(f"Error, keyword not allowed in list contents.")

    # validation lambdas, assert parameter matches an expected type or types.
    _list = lambda thing: isinstance(thing, list)
    _tuple = lambda thing: isinstance(thing, tuple)
    _dict = lambda thing: isinstance(thing, dict)
    _str = lambda thing: isinstance(thing, str)
    _ds_y = lambda thing: any([fun(thing) for fun in [_dict, _str]])
    _ltds_y = lambda thing: any([fun(thing) for fun in [_list, _tuple, _dict, _str]])

    # define tags for re-use
    cn = html.escape(class_name)
    t_tag = "h2"
    l_tag = "ol" if is_ordered else "ul"

    css_selectors = {}
    level = level_in
    ck_key = lambda key: css_selectors.update({key: []}) if key not in css_selectors else None
    ck_val = lambda key, val: css_selectors[key].append(val)
    replace_t = lambda key: ("\t" * level, key.replace(tbs, ""))
    replace_j = lambda key: "".join(replace_t(key))

    # open style tag
    style = replace_j(f"{tbs}<style>\n" if wrap_style else f"{tbs}")
    level += 1

    # handle root font
    if font is not None:

        # assert known parameter type.
        assert _ltds_y(font), "Error, invalid type for param 'font'."
        if isinstance(font, tuple) or isinstance(font, list):
            font_family, font_size = font
        elif isinstance(font, dict):
            font_family, font_size = font.get("font-family", None), int(font.get("font-size", 0))
        else:
            font_family = font.split("font-family:")[-1].split(";")[0].strip()
            font_size = int(font.split("font-size:")[-1].split(";")[0].strip())

        # validate font vars
        assert isinstance(font_family, str) and isinstance(font_size, int)

        # Add to selectors apply to div, title, list, and list items.
        for key in [f"{tbs}{l_tag}.{cn}", f"{tbs}div.{cn}", f"{tbs}{t_tag}.{cn}", f"{tbs}li.{cn}"]:
            ck_key(key)
            ck_val(key, f"{tbs}font-family:\"{font_family}\"")
            ck_val(key, f"{tbs}font-size:{font_size}px")

    # handle root background
    if background is not None:

        # assert known parameter type.
        assert _ltds_y(background), "Error, invalid type for param 'background'."
        if isinstance(background, tuple) or isinstance(background, list):
            # level = 1
            colours = []
            for i, col in enumerate(background):
                assert iscolour(col), f"Error, colour '{col}' not recognized."
                colours.append(col)
        elif isinstance(background, dict):
            colours = [background.get("background", None)]
        else:
            colours = [background.lower().split("background:")[-1].split(";")[0].strip()]

        # validate colours list
        for i, col in enumerate(colours):
            assert col is not None, f"Error invalid colour: \"{col}\"."
            colours[i] = Colour(col)

        # Add to selectors
        for i, item in enumerate(lst):
            c = colours[i % len(colours)]

            # apply for each row
            key = f"{tbs}li.{cn}:nth-child({i + 1})"
            ck_key(key)
            ck_val(key, f"{tbs}background:{c.hex_code}")

            # these tags will only need to be applied once. this ensures they will at least be the last colour.
            for key in [f"{tbs}div.{cn}", f"{tbs}{t_tag}.{cn}", f"{tbs}{l_tag}.{cn}", f"{tbs}li.{cn}"]:
                ck_key(key)
                ck_val(key, f"{tbs}background:{c.hex_code}")

    # handle root foreground
    if foreground is not None:

        # assert known parameter type.
        assert _ltds_y(foreground), "Error, invalid type for param 'foreground'."
        if isinstance(foreground, tuple) or isinstance(foreground, list):
            # level = 1
            colours = []
            for i, col in enumerate(foreground):
                assert iscolour(col), f"Error, colour '{col}' not recognized."
                colours.append(col)
        elif isinstance(foreground, dict):
            colours = [foreground.get("color", None)]
        else:
            colours = [foreground.lower().split("color:")[-1].split(";")[0].strip()]

        # validate colours list
        for i, col in enumerate(colours):
            assert col is not None, f"Error invalid colour: \"{col}\"."
            colours[i] = Colour(col)

        # Add to selectors
        for i, item in enumerate(lst):
            c = colours[i % len(colours)]

            # apply for each row
            key = f"{tbs}li.{cn}:nth-child({i + 1})"
            ck_key(key)
            ck_val(key, f"{tbs}color:{c.hex_code}")

            # these tags will only need to be applied once. this ensures they will at least be the last colour.
            for key in [f"{tbs}div.{cn}", f"{tbs}{t_tag}.{cn}", f"{tbs}{l_tag}.{cn}", f"{tbs}li.{cn}"]:
                ck_key(key)
                ck_val(key, f"{tbs}color:{c.hex_code}")

    # handle title font
    if font_title is not None:

        # assert known parameter type.
        assert _ltds_y(font_title), "Error, invalid type for param 'font_title'."
        if isinstance(font_title, tuple) or isinstance(font_title, list):
            font_family, font_size = font_title
        elif isinstance(font_title, dict):
            font_family, font_size = font_title.get("font-family", None), int(font_title.get("font-size", 0))
        else:
            font_family = font_title.lower().split("font-family:")[-1].split(";")[0].strip()
            font_size = int(font_title.lower().split("font-size:")[-1].split(";")[0].strip())

        # validate font vars
        assert isinstance(font_family, str) and isinstance(font_size, int)

        # Add to selectors
        key = f"{tbs}{t_tag}.{cn}"
        ck_key(key)
        ck_val(key, f"{tbs}font-family:\"{font_family}\"")
        ck_val(key, f"{tbs}font-size:{font_size}px")

    # handle title background
    if background_title is not None:

        # assert known parameter type.
        assert _ds_y(background_title), "Error, invalid type for param 'background_title'."
        if isinstance(background_title, dict):
            colour = background_title.get("background", None)
        else:
            colour = background_title.lower().split("background:")[-1].split(";")[0].strip()

        # validate colours list
        assert iscolour(colour), f"Error invalid colour: \"{colour}\"."
        colour = Colour(colour)

        # Add to selectors
        key = f"{tbs}{t_tag}.{cn}"
        ck_key(key)
        ck_val(key, f"{tbs}background:{colour.hex_code}")

    # handle title foreground
    if foreground_title is not None:

        # assert known parameter type.
        assert _ds_y(foreground_title), "Error, invalid type for param 'foreground_title'."
        if isinstance(foreground_title, dict):
            colour = foreground_title.get("background", None)
        else:
            colour = foreground_title.lower().split("color:")[-1].split(";")[0].strip()

        # validate colours list
        assert iscolour(colour), f"Error invalid colour: \"{colour}\"."
        colour = Colour(colour)

        # Add to selectors
        key = f"{tbs}{t_tag}.{cn}"
        ck_key(key)
        ck_val(key, f"{tbs}color:{colour.hex_code}")

    # handle alternating row backgrounds
    if background_alternating_row is not None:

        # assert known parameter type.
        assert _list(background_alternating_row), "Error, invalid type for param 'background_alternating_row'."
        colours = [Colour(col) for col in background_alternating_row]

        for i, item in enumerate(lst):
            c = colours[i % len(colours)]

            # apply for each row
            key = f"{tbs}li.{cn}:nth-child({i + 1})"
            ck_key(key)
            ck_val(key, f"{tbs}background:{c.hex_code}")

    # handle alternating row foregrounds
    if foreground_alternating_row is not None:

        # assert known parameter type.
        assert _list(foreground_alternating_row), "Error, invalid type for param 'foreground_alternating_row'."
        colours = [Colour(col) for col in foreground_alternating_row]

        for i, item in enumerate(lst):
            c = colours[i % len(colours)]

            # apply for each row
            key = f"{tbs}li.{cn}:nth-child({i + 1})"
            ck_key(key)
            ck_val(key, f"{tbs}color:{c.hex_code}")

        # # Add to selectors
        # key = f"{tbs}li.{cn}"
        # ck_key(key)
        # ck_val(key, f"{tbs}font-family:\"{font_family}\"")
        # ck_val(key, f"{tbs}font-size:{font_size}px")

    # add all styles together
    for key, style_list in css_selectors.items():
        t1, k = replace_t(key)
        style += f"{t1}{k} {{\n"
        t1 += "\t"

        # iterate the list in reverse, ensure that the last definition for a style is the one that is used.
        known = {}
        for i in range(len(style_list) -1, -1, -1):
            sty = style_list[i]
            styl, val = sty.split(":")
            if styl not in known:
                known[styl] = sty
            # else:
            #     print(f"skipped {i=}, {sty=}")

        for styl in known.values():
            t2, s = replace_t(styl)
            style += f"{t1}{s};\n"

        t1 = t1[:-1]
        style += f"{t1}}}\n"

    # close style tag
    level -= 1
    style += replace_j(f"{tbs}</style>" if wrap_style else "")

    list_tag = f"<{l_tag} class=\"{cn}\">"
    for el in lst:
        list_tag += f"<li class=\"{cn}\">{el}</li>"
    list_tag += f"</{l_tag}>"

    # Generate the title html
    title_html = f"<{t_tag} class=\"{cn}\">{title}</{t_tag}>" if title else ""
    body_html = f"<div class=\"{cn}\">\n\t{title_html}\n\t{list_tag}\n</div>"

    if is_raw:
        style = style.replace("\n", "").replace("\t", "")
        body_html = body_html.replace("\n", "").replace("\t", "")

    return style, body_html


def html_to_pdf(
        html_file,
        pdf_file_out=None,
        do_open=True,
        do_quit=False,
        options=None,
        avoid_overwrite=True,
        wkhtmltopdf_path=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
):

    # No wkhtmltopdf, no go.
    assert isinstance(wkhtmltopdf_path, str) and wkhtmltopdf_path.endswith(
        ".exe"), f"Error, invalid exe file path given: '{wkhtmltopdf_path}'."
    if not os.path.exists(wkhtmltopdf_path):
        msg = f"Error, please install wkhtmltopdf before continuing."
        loc = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
        lnk = r"https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox-0.12.6-1.msvc2015-win64.exe"
        brd = f"=" * 120
        msg = f"\n\n{brd}\n\n{msg}\nPreferred location:\n\t{loc}\nWindows 64-bit link (~100 Mb):\n\t{lnk}\n\nThis package must be installed to use this function.\n\n{brd}\n\n"
        if not do_quit:
            raise FileNotFoundError(msg)
        else:
            print(msg)
            quit()

    assert isinstance(html_file, str) and html_file.endswith(
        ".html"), f"Error, invalid html file path given: '{html_file}'."
    if options is None:
        options = {
            "page-size": "letter",
            "orientation": "portrait",
            'margin-top': '0.5in',
            'margin-right': '0.5in',
            'margin-bottom': '0.5in',
            'margin-left': '0.5in',
            'encoding': "UTF-8"
        }
    if pdf_file_out is None:
        pdf_file_out = html_file.removesuffix(".html") + ".pdf"
    else:
        assert isinstance(pdf_file_out, str) and pdf_file_out.endswith(".pdf"), f"Error, invalid pdf file path given: '{pdf_file_out}'."

    if avoid_overwrite:
        pdf_file_out = next_available_file_name(pdf_file_out)

    # print(f"HTML file: {html_file}")
    # print(f"PDF file : {pdf_file_out}")

    # else:
    #     try:
    #         config = pdfkit.configuration()
    #     except OSError:
    #         # not present in path
    #         print(f"Error, wkhtmltopdf not found in path either. Please install before continuing")
    #         quit()

    config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)
    pdfkit.from_file(html_file, pdf_file_out, configuration=config, options=options)

    # from weasyprint import HTML
    # HTML(file_out).write_pdf(pdf_file_out)

    if do_open:
        webbrowser.open(pdf_file_out)

    return pdf_file_out


def test_list_to_html_2():
    lst = ["Cat", "dog", "Bicycle", "Umbrella", "Potato", "Goose"]
    # lst = list(range(-500, 60))
    result_style, result_html = list_to_html(
        lst=lst,
        title='Sample List',
        # font=('Courier', 22),
        font={"font-family":"Courier", "font-size": 22},
        # font="font-family:Courier, font-size: 22",
        # background=("orange", "red"),
        # background="red",
        background=("orange", "white"),
        foreground=("#0d0d0d", "#1212CC"),
        # font_title=("Comic Sans", 12),
        background_title="background: limegreen;",
        foreground_title="#101010;",
        is_raw=False
    )

    print(f"my_attempt:\n{result_style}\n{result_html}")


if __name__ == '__main__':
    version_data()
    # test_list_to_html_2()
