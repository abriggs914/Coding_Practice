import tkinter
from typing import List, Union, Tuple
from tkhtmlview import HTMLLabel
from html_utility import *


def list_to_html__(items: Union[List[str], List[Tuple[str, str]]], title: str = None, is_ordered: bool = True, style: dict = None, inject_style: bool = False) -> Tuple[str, str]:
    # Generate the list items
    items_html = ""
    for item in items:
        # If each item is a tuple, format it as key-value pair
        if isinstance(item, tuple):
            key, value = item
            item_html = f"<li><strong>{key}: </strong>{value}</li>"
        # Otherwise, format it as a simple list item
        else:
            item_html = f"<li>{item}</li>"
        items_html += item_html

    # Determine the list type
    list_type = "ol" if is_ordered else "ul"

    # Generate the list html
    list_html = f"<{list_type}>{items_html}</{list_type}>"

    # Generate the title html
    title_html = f"<h2>{title}</h2>" if title else ""

    # Generate the style html
    style_html = ""
    if style:
        # Check for number styling keys and apply them to the list
        if "number_background" in style:
            style_html += f"{list_type} {{background-color: {style['number_background']};}}"
        if "number_foreground" in style:
            style_html += f"{list_type} {{color: {style['number_foreground']};}}"
        if "number_font" in style:
            font = f"{style['number_font'][0]}, {style['number_font'][1]}px"
            if len(style['number_font']) > 2:
                font += f", {style['number_font'][2]}"
            style_html += f"{list_type} {{font-family: {font};}}"

        # Check for alternate row styling keys and apply them to the list items
        if "alternate_row_background" in style or "alternate_row_foreground" in style:
            items_style_html = ""
            for i, item in enumerate(items):
                bg_key = "alternate_row_background" if i % 2 == 0 else "background"
                fg_key = "alternate_row_foreground" if i % 2 == 0 else "foreground"
                bg_color = style[bg_key][i % len(style[bg_key])] if bg_key in style else ""
                fg_color = style[fg_key][i % len(style[fg_key])] if fg_key in style else ""
                font = f"{style['font'][0]}, {style['font'][1]}px"
                if len(style['font']) > 2:
                    font += f", {style['font'][2]}"
                item_style_html = f"{list_type} li:nth-child({i+1}) {{background-color: {bg_color}; color: {fg_color}; font-family: {font};}}"
                items_style_html += item_style_html
            style_html += items_style_html

    # Generate the full html
    html = f"{title_html}{list_html}"

    # Determine where to inject the style
    if inject_style:
        html = f"<head><style>{style_html}</style></head>{html}"
    else:
        html = f"<style>{style_html}</style>{html}"

    return html, style_html


# def list_to_html(data, title=None, is_ordered=False, style=None, inject_style=False):
#     if style is None:
#         style = {}
#
#     html_str = ""
#
#     if title is not None:
#         html_str += f"<h3 style='{_get_style_str(style, 'title')}'>{title}</h3>"
#
#     if is_ordered:
#         html_str += f"<ol style='{_get_style_str(style, 'list')}'>"
#     else:
#         html_str += f"<ul style='{_get_style_str(style, 'list')}'>"
#
#     for i, item in enumerate(data):
#         html_str += f"<li style='{_get_style_str(style, 'list_item')}'>"
#         if 'number_background' in style:
#             html_str += f"<span style='{_get_style_str(style, 'number')}'>{i + 1}</span>"
#         html_str += f"<span style='{_get_style_str(style, 'list_item_content')}'>{item}</span>"
#         html_str += "</li>"
#
#     if is_ordered:
#         html_str += "</ol>"
#     else:
#         html_str += "</ul>"
#
#     style_str = ""
#     if inject_style:
#         style_str += f"ol, ul {{{_get_style_str(style, 'list')}}}\n"
#         style_str += f"li {{{_get_style_str(style, 'list_item')}}}\n"
#         style_str += f"li span {{{_get_style_str(style, 'list_item_content')}}}\n"
#         style_str += f"li span:first-child {{{_get_style_str(style, 'number')}}}\n"
#     else:
#         style_str += f"<style>ol, ul {{{_get_style_str(style, 'list')}}} li {{{_get_style_str(style, 'list_item')}}} li span {{{_get_style_str(style, 'list_item_content')}}} li span:first-child {{{_get_style_str(style, 'number')}}}</style>"
#
#     return html_str, style_str
#
#
# def _get_style_str(style, key):
#     style_str = ""
#
#     if key in style:
#         if key == 'list':
#             style_str += f"background-color: {style[key]};"
#         elif key == 'title':
#             style_str += f"color: {style[key]};"
#         elif key == 'list_item':
#             if 'alternate_row_background' in style and isinstance(style['alternate_row_background'], list):
#                 alt_index = i % len(style['alternate_row_background'])
#                 style_str += f"background-color: {style['alternate_row_background'][alt_index]};"
#             else:
#                 style_str += f"background-color:


# def list_to_html(data, title=None, is_ordered=True, style=None, inject_style=False):
#     # Determine list tag based on is_ordered parameter
#     list_tag = 'ol' if is_ordered else 'ul'
#     # Generate list items HTML
#     items_html = ''
#     for i, item in enumerate(data):
#         # Determine row background and foreground colors
#         if style is not None and 'alternate_row_background' in style and 'alternate_row_foreground' in style:
#             alt_row_bg = style['alternate_row_background']
#             alt_row_fg = style['alternate_row_foreground']
#             bg_colour = alt_row_bg[i % len(alt_row_bg)]
#             fg_colour = alt_row_fg[i % len(alt_row_fg)]
#         else:
#             bg_colour = ''
#             fg_colour = ''
#         # Generate item HTML with background and foreground styling
#         item_html = f'<li style="background-color:{bg_colour};color:{fg_colour}">{html.escape(str(item))}</li>'
#         items_html += item_html
#     # Wrap list items HTML in list tags
#     list_html = f'<{list_tag}>{items_html}</{list_tag}>'
#     # Add title if specified
#     if title is not None:
#         # Determine title background and foreground colors
#         if style is not None and ('background_title' in style or 'foreground_title' in style):
#             bg_colour = style.get('background_title', '')
#             fg_colour = style.get('foreground_title', '')
#             title_style = f'style="background-color:{bg_colour};color:{fg_colour}"'
#         else:
#             title_style = ''
#         title_html = f'<h2 {title_style}>{html.escape(title)}</h2>'
#         list_html = title_html + list_html
#     # Generate styles string
#     if style is not None:
#         styles = []
#         if 'background' in style:
#             styles.append(f'background-color:{style["background"]}')
#         if 'foreground' in style:
#             styles.append(f'color:{style["foreground"]}')
#         if 'font' in style:
#             font_family, font_size, font_weight = style['font']
#             styles.append(f'font-family:{font_family};font-size:{font_size}px;font-weight:{font_weight}')
#         style_str = ' '.join(styles)
#         if inject_style:
#             style_str = f'<style>{list_tag} {{ {style_str} }}</style>'
#     else:
#         style_str = ''
#     # Return raw HTML and styles string
#     return list_html, style_str


# def list_to_html(data, title=None, is_ordered=True, style=None, inject_style=False):
#     # Determine list tag based on is_ordered parameter
#     list_tag = 'ol' if is_ordered else 'ul'
#     # Generate list items HTML
#     items_html = ''
#     for i, item in enumerate(data):
#         item_html = f'<li>{html.escape(str(item))}</li>'
#         if style is not None:
#             # Add alternating row styles if necessary
#             if 'alternate_row_background' in style or 'alternate_row_foreground' in style:
#                 alt_bg, alt_fg = None, None
#                 if 'alternate_row_background' in style:
#                     alt_bg = style['alternate_row_background'][i % len(style['alternate_row_background'])]
#                 if 'alternate_row_foreground' in style:
#                     alt_fg = style['alternate_row_foreground'][i % len(style['alternate_row_foreground'])]
#                 item_html = f'<li style="background-color:{alt_bg}; color:{alt_fg}">{html.escape(str(item))}</li>'
#             # Apply background and foreground styles if necessary
#             if 'background' in style or 'foreground' in style:
#                 bg = style.get('background', None)
#                 fg = style.get('foreground', None)
#                 item_html = f'<li style="background-color:{bg}; color:{fg}">{html.escape(str(item))}</li>'
#         items_html += item_html
#     # Wrap list items HTML in list tags
#     list_html = f'<{list_tag}>{items_html}</{list_tag}>'
#     if style is None:
#         style = {}
#     # Add title if specified
#     if title is not None:
#         title_html = f'<h2 style="background-color:{style.get("background_title", "")}; color:{style.get("foreground_title", "")}; font-family:{style.get("font_title", ("", "", ""))[0]}; font-size:{style.get("font_title", ("", "", ""))[1]}px; font-weight:{style.get("font_title", ("", "", ""))[2]}">{html.escape(title)}</h2>'
#         list_html = title_html + list_html
#     # Generate style string if necessary
#     style_str = ''
#     if style is not None:
#         style_str += f'list-style: {list_tag};\n'
#         if 'font' in style:
#             font_family, font_size, font_weight = style['font']
#             style_str += f'font-family: {font_family}; font-size: {font_size}px; font-weight: {font_weight};\n'
#     # Generate style string for alternating row colors if necessary
#     if 'alternate_row_background' in style or 'alternate_row_foreground' in style:
#         alt_bg = ','.join(style.get('alternate_row_background', []))
#         alt_fg = ','.join(style.get('alternate_row_foreground', []))
#         style_str += f'{list_tag} li:nth-child(even) {{background-color: {alt_bg}; color: {alt_fg};}}\n'
#         style_str += f'{list_tag} li:nth-child(odd) {{background-color: {style.get("background", "")}; color: {style.get("foreground", "")};}}\n'
#     # Return raw HTML and style string
#     if inject_style:
#         style_str = f'<style type="text/css">\n{style_str}</style>\n'
#         return list_html, style_str
#     else:
#         return list_html, style_str.strip()



# def list_to_html(items, title=None, is_ordered=True):
#     # Determine which tag to use based on is_ordered parameter
#     tag = 'ol' if is_ordered else 'ul'
#     # Generate list items HTML
#     items_html = ''.join(f'<li>{html.escape(str(item))}</li>' for item in items)
#     # Wrap list items HTML in list tag
#     list_html = f'<{tag}>{items_html}</{tag}>'
#     # Add title if specified
#     if title is not None:
#         title_html = f'<h3>{html.escape(title)}</h3>'
#         list_html = title_html + list_html
#     # Return raw HTML
#     return list_html


def test_html_view():

    # Create the tkinter application
    app = tkinter.Tk()
    app.title("HTML Renderer")

    # Define the HTML content to render
    html_content = """
    <html>
        <body>
            <h1>Hello, Tkinter!</h1>
            <p>This is a <strong>simple</strong> HTML document rendered in a Tkinter application.</p>
            <ul>
                <li>Item 1</li>
                <li>Item 2</li>
                <li>Item 3</li>
            </ul>
        </body>
    </html>
    """

    # Create an HTMLLabel widget to display the HTML content
    html_label = HTMLLabel(app, html=html_content)
    html_label.pack(fill=tkinter.BOTH, expand=True)

    # Run the tkinter main loop
    app.mainloop()


def test_table_to_html():
    # Example usage with dictionary input and title
    data = {
        'Name': {'Alice': 25, 'Bob': 30},
        'Gender': {'Alice': 'Female', 'Bob': 'Male'}
    }
    html_output = table_to_html(data, title='Example Table')
    print(html_output)

    # Example usage with DataFrame input and no title
    data = pd.DataFrame({
        'Name': ['Alice', 'Bob'],
        'Age': [25, 30],
        'Gender': ['Female', 'Male']
    })
    html_output = table_to_html(data)
    print(html_output)


def test_list_to_html():
    # Example usage with list input and title
    items = ['Apple', 'Banana', 'Cherry']
    html_output = list_to_html__(items, title='Fruits')
    print(html_output)

    # Example usage with tuple input and no title
    items = ('Monday', 'Tuesday', 'Wednesday')
    html_output, style_output = list_to_html__(items, is_ordered=True)
    print(html_output)

    app = tkinter.Tk()
    app.geometry(f"600x600")
    html_label = HTMLLabel(app, html=html_output)
    html_label.pack(fill=tkinter.BOTH, expand=True)
    app.mainloop()

    # style = {
    #     "background": (19, 198, 66),
    #     "foreground": "#FF6677",
    #     "background_title": "#000000",
    #     "foreground_title": (180, 255, 140),
    #     # "alternate_row_background": ["green", "red", "blue"],
    #     # "alternate_row_foreground": ["red", "blue", "green"],
    #     "alternate_row_background": ["black", "white"],
    #     "alternate_row_foreground": ["white", "blacK"],
    #     "font": ("Arial", 16, "Bold"),
    #     "font_title": ("Arial", 20)
    # }

    style = {
        "background": (19, 198, 66),
        "foreground": "#FF6677",
        "background_title": "#000000",
        "foreground_title": (255, 255, 255),
        "alternate_row_background": ["black", "red", "white"],
        "alternate_row_foreground": ["red", "white", "black"],
        "font": ("Arial", 16, "Bold"),
        "font_title": ("Arial", 20),
        "number_background": "yellow",
        "number_foreground": "black",
        "number_font": ("Arial", 12, "Italic")
    }

    html_str, style_str = list_to_html__(range(-2, 6), is_ordered=True, title="Here is my title!", style=style,
                                         inject_style=False)
    print(f"{html_str=}")
    print(f"{style_str=}")


def new_html_util():
    tag_left = "<"
    tag_right = ">"
    html_tags = ['a', 'abbr', 'acronym', 'address', 'applet', 'area', 'article', 'aside', 'audio', 'b', 'base',
                 'basefont', 'bdi', 'bdo', 'blockquote', 'body', 'br', 'button', 'canvas', 'caption', 'center', 'cite',
                 'code', 'col', 'colgroup', 'data', 'datalist', 'dd', 'del', 'details', 'dfn', 'dialog', 'dir', 'div',
                 'dl', 'dt', 'em', 'embed', 'fieldset', 'figcaption', 'figure', 'font', 'footer', 'form', 'frame',
                 'frameset', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'head', 'header', 'hr', 'html', 'i', 'iframe', 'img',
                 'input', 'ins', 'kbd', 'label', 'legend', 'li', 'link', 'main', 'map', 'mark', 'meta', 'meter', 'nav',
                 'noframes', 'noscript', 'object', 'ol', 'optgroup', 'option', 'output', 'p', 'param', 'picture', 'pre',
                 'progress', 'q', 'rp', 'rt', 'ruby', 's', 'samp', 'script', 'section', 'select', 'small', 'source',
                 'span', 'strike', 'strong', 'style', 'sub', 'summary', 'sup', 'svg', 'table', 'tbody', 'td',
                 'template', 'textarea', 'tfoot', 'th', 'thead', 'time', 'title', 'tr', 'track', 'tt', 'u', 'ul', 'var',
                 'video', 'wbr']

    # def style_to_tag(style_dict):
    #     """
    #     Generates an HTML style tag from a dictionary of CSS properties.
    #
    #     Args:
    #         style_dict (dict): A dictionary containing CSS properties and their values.
    #
    #     Returns:
    #         str: The HTML style tag.
    #     """
    #     try:
    #         background = style_dict.get("background", "")
    #         foreground = style_dict.get("foreground", "")
    #         background_title = style_dict.get("background_title", background)
    #         foreground_title = style_dict.get("foreground_title", foreground)
    #         number_background = style_dict.get("number_background", background)
    #         number_foreground = style_dict.get("number_foreground", foreground)
    #         font = style_dict.get("font", "")
    #         font_title = style_dict.get("font_title", font)
    #         number_font = style_dict.get("number_font", font)
    #         alternate_row_background = style_dict.get("alternate_row_background", "")
    #         alternate_row_foreground = style_dict.get("alternate_row_foreground", "")
    #
    #         if alternate_row_background and isinstance(alternate_row_background, list):
    #             num_colors = len(alternate_row_background)
    #             if num_colors > 1:
    #                 alternate_row_background = "linear-gradient(to bottom, " + ", ".join(
    #                     alternate_row_background) + ")"
    #             elif num_colors == 1:
    #                 background = foreground = alternate_row_background[0]
    #
    #         if alternate_row_foreground and isinstance(alternate_row_foreground, list):
    #             num_colors = len(alternate_row_foreground)
    #             if num_colors > 1:
    #                 foreground_list = [alternate_row_foreground[i % num_colors]
    #                                    for i in range(0, 100, 2)]
    #             elif num_colors == 1:
    #                 foreground = background = alternate_row_foreground[0]
    #
    #         style_str = f"background:{background};\nforeground:{foreground};\nfont:{font};\n"
    #         style_str += f"background-title:{background_title};\nforeground-title:{foreground_title};\nfont-title:{font_title};\n"
    #         style_str += f"number-background:{number_background};\nnumber-foreground:{number_foreground};\nnumber-font:{number_font};\n"
    #         if alternate_row_background:
    #             style_str += f"alternate-background: {alternate_row_background};\n"
    #         if alternate_row_foreground:
    #             style_str += f"alternate-foreground: {' '.join(foreground_list)};\n"
    #
    #         return f"<style>\n{style_str}</style>"
    #     except KeyError:
    #         return ""

    def style_dict_to_tag(style_dict):
        if not isinstance(style_dict, dict):
            return ''

        style_str = ''
        try:
            background = style_dict.get('background')
            foreground = style_dict.get('foreground')
            font = style_dict.get('font')

            if background:
                style_str += f'background: {background};'
            if foreground:
                style_str += f'color: {foreground};'
            if font:
                font_family, font_size, font_weight = font
                style_str += f'font-family: {font_family}; font-size: {font_size}px; font-weight: {font_weight};'

            if 'background_title' in style_dict:
                style_str += f'title{{background: {style_dict["background_title"]};}}'
            if 'foreground_title' in style_dict:
                style_str += f'title{{color: {style_dict["foreground_title"]};}}'

            if 'number_background' in style_dict:
                style_str += f'ol{{background: {style_dict["number_background"]};}}'
            if 'number_foreground' in style_dict:
                style_str += f'ol{{color: {style_dict["number_foreground"]};}}'
            if 'number_font' in style_dict:
                font_family, font_size, font_weight = style_dict['number_font']
                style_str += f'ol{{font-family: {font_family}; font-size: {font_size}px; font-weight: {font_weight};}}'

            if 'alternate_row_background' in style_dict:
                alt_bg = ','.join(style_dict['alternate_row_background'])
                style_str += f'li:nth-child(even){{background: {alt_bg};}}'
            if 'alternate_row_foreground' in style_dict:
                alt_fg = ','.join(style_dict['alternate_row_foreground'])
                style_str += f'li:nth-child(even){{color: {alt_fg};}}'
        except KeyError:
            return ''

        style_str = ';\n'.join(style_str.split(';'))
        return f"<style>{style_str}</style>"



    style = {
        "background": (19, 198, 66),
        "foreground": "#FF6677",
        "background_title": "#000000",
        "foreground_title": (255, 255, 255),
        "alternate_row_background": ["black", "red", "white"],
        "alternate_row_foreground": ["red", "white", "black"],
        "font": ("Arial", 16, "Bold"),
        "font_title": ("Arial", 20),
        "number_background": "green",
        "number_foreground": "black",
        "number_font": ("Arial", 12, "Italic")
    }

    print(f"\n\tstyle_to_tag(style)\n{style_dict_to_tag(style)}")


def t3():
    def list_style(lst, background, foreground=None, is_ordered=True):
        bg_style = ""
        fg_style = ""
        if isinstance(background, list):
            bg_style = "background-color: {};".format(background[0])
            if len(background) > 1:
                bg_style += "background-image: repeating-linear-gradient(to bottom, "
                for i in range(len(background)):
                    bg_style += "{}, {} {}%, ".format(background[i], background[i], 100 / len(background))
                bg_style = bg_style[:-2] + ");"
        else:
            bg_style = "background-color: {};".format(background)

        if foreground is not None:
            if isinstance(foreground, list):
                fg_style = "color: {};".format(foreground[0])
                if len(foreground) > 1:
                    fg_style += "background-image: repeating-linear-gradient(to bottom, "
                    for i in range(len(foreground)):
                        fg_style += "{}, {} {}%, ".format(foreground[i], foreground[i], 100 / len(foreground))
                    fg_style = fg_style[:-2] + ");"
            else:
                fg_style = "color: {};".format(foreground)

        style_tag = "<style>"
        style_tag += "ol, ul {padding-left: 0; list-style-type: none;}"
        style_tag += "ol li:before, ul li:before {content: counter(item); counter-increment: item;}"
        style_tag += "ol {" + bg_style + fg_style + "}"
        style_tag += "ul {" + bg_style + fg_style + "}"
        style_tag += "</style>"

        list_tag = "<ol>" if is_ordered else "<ul>"
        for i in range(len(lst)):
            list_tag += "<li>{}</li>".format(lst[i])
        list_tag += "</ol>" if is_ordered else "</ul>"

        return list_tag, style_tag

    lst = ['item1', 'item2', 'item3', 'item4', 'item5', 'item6', 'item7']
    colour_1 = ['#FFC300', '#FF5733', '#C70039', '#900C3F']
    colour_2 = ['#00FFC3', '#33FF57', '#39C700', '#3F900C']
    is_ordered = True

    list_tag, style_tag = list_style(lst, background=colour_1, foreground=colour_2, is_ordered=True)
    print(list_tag)
    print(style_tag)

#
# def my_attempt(
#         lst,
#         title=None,
#         class_name="lst",
#         font=None,
#         background=None,
#         foreground=None,
#         font_title=None,
#         background_title=None,
#         foreground_title=None,
#         font_marker=None,
#         background_marker=None,
#         foreground_marker=None,
#         font_alternating_row=None,
#         background_alternating_row=None,
#         foreground_alternating_row=None,
#         is_ordered=True
# ):
#
#     # validation lambdas, assert parameter matches an expected type or types.
#     _list = lambda thing: isinstance(thing, list)
#     _tuple = lambda thing: isinstance(thing, tuple)
#     _dict = lambda thing: isinstance(thing, dict)
#     _str = lambda thing: isinstance(thing, str)
#     _ltds_y = lambda thing: any([fun(thing) for fun in [_list, _tuple, _dict, _str]])
#
#     # define tags for re-use
#     _l = "_line"
#     _a = "_args"
#     cn = html.escape(class_name)
#     l_tag = "ol" if is_ordered else "ul"
#
#     # style_tags = {
#     #     l_tag: {},
#     #     f".{cn}": {}
#     # }
#
#     css_selectors = {
#         "font": {
#             _l: 0,
#             "font-family": {
#                 _l: 0,
#                 _a: []
#             },
#             "font-size": 1
#         },
#         "background": {
#             _l: 0,
#             "background": 0
#         },
#         "foreground": {
#             _l: 0,
#             "color": 0
#         }
#     }
#
#     # Generate the title html
#     title_html = f"<h2>{title}</h2>" if title else ""
#
#     # open style tag
#     style = "<style>\n"
#     level = 1
#     tabs = level * "\t"
#
#     # handle root font
#     if font is not None:
#
#         # assert known parameter type.
#         assert _ltds_y(font), "Error, invalid type for param 'font'."
#         if isinstance(font, tuple) or isinstance(font, list):
#             font_family, font_size = font
#         elif isinstance(font, dict):
#             font_family, font_size = font.get("font-family", None), int(font.get("font-size", 0))
#         else:
#             font_family = font.split("font-family:")[-1].split(";")[0].strip()
#             font_size = int(font.split("font-size:")[-1].split(";")[0].strip())
#
#         # validate font vars
#         assert isinstance(font_family, str) and isinstance(font_size, int)
#
#         # add to style
#         style += f"{tabs}{l_tag}.{cn} {{\n"
#         level += 1
#         tabs = level * "\t"
#         style += f"{tabs}font-family:{font_family};\n"
#         style += f"{tabs}font-size:{font_size}px;\n"
#         level -= 1
#         tabs = level * "\t"
#         style += f"{tabs}}}\n"
#     else:
#         raise TypeError("A Error here")
#
#     # handle root background
#     if background is not None:
#
#         # assert known parameter type.
#         assert _ltds_y(background), "Error, invalid type for param 'background'."
#         if isinstance(background, tuple) or isinstance(background, list):
#             level = 1
#             tabs = level * "\t"
#             colours = []
#             for i, col in enumerate(background):
#                 assert iscolour(col), f"Error, colour '{col}' not recognized."
#                 colours.append(col)
#         elif isinstance(background, dict):
#             colours = [background.get("background", None)]
#         else:
#             colours = [background.split("background:")[-1].split(";")[0].strip()]
#
#         # validate colours list
#         for i, col in enumerate(colours):
#             assert col is not None, f"Error invalid colour: \"{col}\"."
#             colours[i] = Colour(col)
#
#         # add to style
#         for i, item in enumerate(lst):
#             c = colours[i % len(colours)]
#             style += f"{tabs}li.{cn}:nth-child({i+1})"
#             level += 1
#             tabs = level * "\t"
#             style += f" {{\n{tabs}background:{c.hex_code};{tabs}\n"
#             level -= 1
#             tabs = level * "\t"
#             style += f"{tabs}}}\n"
#     else:
#         raise TypeError("B Error here")
#
#     # close style tag
#     level -= 1
#     tabs = level * "\t"
#     style += f"{tabs}</style>"
#
#     list_tag = f"<{l_tag} class=\"{cn}\">"
#     for i in range(len(lst)):
#         list_tag += f"<li class=\"{cn}\">{lst[i]}</li>"
#     list_tag += f"</{l_tag}>"
#
#     return f"{title_html}\n{style}\n{list_tag}"


def test_list_to_html_1():
    lst = ["Cat", "dog", "Bicycle", "Umbrella", "Potato", "Goose"]
    # lst = list(range(-500, 60))
    result_style, result_html = my_attempt(
        lst=lst,
        title='my_title_goes_here',
        # font=('Courier', 22),
        font={"font-family":"Courier", "font-size": 22},
        # font="font-family:Courier, font-size: 22",
        # background=("orange", "red"),
        background="red",
        # # background=("orange", "red")
        foreground=("#0d0d0d", "#1212CC"),
        # font_title=("Comic Sans", 12),
        # background_title="background: limegreen;",
        # foreground_title="#101010;"
    )

    print(f"my_attempt:\n{result_style}\n{result_html}")



if __name__ == '__main__':

    # test_table_to_html()
    # test_list_to_html()
    # test_html_view()
    # new_html_util()
    # t3()

    # test_list_to_html_1()
    test_list_to_html_2()