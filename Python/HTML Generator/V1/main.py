# Python program to dynamically create html files.

import webbrowser
import os
from Element import *


class HTMLFile:

    def __init__(self, name, title=None):
        self.name = name
        self.title = title
        self.currently_saved = False
        self.f_name = name + ".html" if not name.endswith(".html") else name

        self.lines = {
            "top": [],
            "head": [],
            "body": [],
            "script": [],
            "link": [],
            "foot": [],
            "bottom": []
        }

        self.gen_header()

    def set_section(self, section, lines):
        self.currently_saved = False
        if self.lines[section]:
            self.lines[section].append(lines)
        else:
            self.lines[section] = lines if isinstance(lines, list) else [lines]

    def tag(self, section):
        sections = {
            "top": ["<!DOCTYPE html>", "<html>"],
            "head": ["<head>", "</head>"],
            "body": ["<body>", "</body>"],
            "script": ["<script>", "</script>"],
            "link": ["<link", ">"],
            "meta": ["<meta", ">"],
            "style": ["<style", "</style>"],
            "foot": ["<footer>", "</footer>"],
            "bottom": ["</html>"]
        }
        return sections[section]

    def gen_header(self):
        if self.title:
            lst = self.lines["head"]
            self.set_section("head", lst[:1] + ["<title>", self.title, "</title>"] + lst[-1:])

    def save(self):
        n_tabs = 0
        with open(self.f_name, "w") as f:
            for section, lines in self.lines.items():
                if not lines and section not in ["top", "bottom"]:
                    continue
                print("section:", section)
                n_lines = self.tag(section)
                og = n_lines.copy()
                h = len(n_lines) // 2
                n_lines = n_lines[:h if len(n_lines) > 1 else 1] + lines + n_lines[
                                                                           h if len(n_lines) % 2 == 0 else h + 1:]
                print("lines:", lines, "n_lines:", og, "n_lines:", n_lines)
                for lst in n_lines:
                    if isinstance(lst, OL) or isinstance(lst, UL):
                        tag_close = lst.e__tag_close
                        tag_open = lst.e__tag_open
                        lst = [str(lst)[: -tag_close.index(tag_open[-1])]] + lst.e__items + [tag_close]
                    if not isinstance(lst, list):
                        lst = [lst]
                    for line in lst:
                        print("isinstance(line, Element):", isinstance(line, OL))

                        elem = isinstance(line, Element)
                        print("isinstance(line, Element):", isinstance(line, OL))
                        if elem:
                            line = str(line)
                        print("line:", line)
                        if line[0] == "<":
                            if line[1] == "/":
                                n_tabs -= 1
                        f.write("".join(["\t" for i in range(n_tabs)]) + line + "\n")
                        if line[0] == "<":
                            if line[1] == "/":
                                pass
                            else:
                                n_tabs += 1
                        n_tabs += -1 if elem else 0
            self.currently_saved = True
        # n_tabs = 0
        # with open(self.f_name, "w") as f:
        #     for section, lines in self.lines.items():
        #         if not lines and section not in ["top", "bottom"]:
        #             continue
        #         print("section:", section)
        #         n_lines = self.tag(section)
        #         og = n_lines.copy()
        #         h = len(n_lines) // 2
        #         n_lines = n_lines[:h if len(n_lines) > 1 else 1] + lines + n_lines[h if len(n_lines) % 2 == 0 else h + 1:]
        #         print("lines:", lines, "n_lines:", og, "n_lines:", n_lines)
        #         special_cases = ["ol", "ul"]
        #         scc = 0
        #         for line in n_lines:
        #             sline = str(line)
        #             # t = scc
        #             # for i in range(t):
        #             #     n_tabs -= 1
        #             #     scc -= 1
        #             ci = -1
        #             try:
        #                 ci = sline.index(">")
        #             except ValueError:
        #                 pass
        #
        #             si = -1
        #             try:
        #                 si = sline.index(" ")
        #             except ValueError:
        #                 pass
        #             si = si if si >= 0 else float("inf")
        #             ci = ci if ci >= 0 else float("inf")
        #             idx = min(si, ci)
        #             print("ci:", ci, "si:", si, "idx:", idx)
        #             if idx < 0 or (si == ci == -1):
        #                 raise ValueError("line does not contain \">\" or \" \".\n\tInspect line: \"{0}\".".format(sline))
        #
        #             elem = isinstance(sline, Element)
        #             if elem:
        #                 sline = str(sline)
        #             # print("\tline:", sline, "\n\tsline[1: idx]:", sline[1: idx], "\n\tsline[1: idx] in special_cases:", (sline[1: idx] in special_cases))
        #             if sline[0] == "<":
        #                 if sline[1] == "/":
        #                     n_tabs -= 1
        #                 # elif sline[1: idx] in special_cases:
        #                 #     n_tabs += 1
        #                 #     scc += 1
        #             f.write("".join(["\t" for i in range(n_tabs)]) + sline + "\n")
        #             if sline[0] == "<":
        #                 if sline[1] == "/" or sline[1: idx] in special_cases:
        #                     pass
        #                 else:
        #                     n_tabs += 1
        #             n_tabs += -1 if elem else 0
        #     self.currently_saved = True

    def open(self):
        if self.f_name in os.listdir():
            webbrowser.open(self.f_name)

    def add_image(self, section, src, **kwargs):
        elem = Img(src, **kwargs)
        self.set_section(section, elem)
        return elem

    def add_h1(self, section, txt, **kwargs):
        elem = H1(txt, **kwargs)
        self.set_section(section, elem)
        return elem

    def add_h2(self, section, txt, **kwargs):
        elem = H2(txt, **kwargs)
        self.set_section(section, elem)
        return elem

    def add_h3(self, section, txt, **kwargs):
        elem = H3(txt, **kwargs)
        self.set_section(section, elem)
        return elem

    def add_h4(self, section, txt, **kwargs):
        elem = H4(txt, **kwargs)
        self.set_section(section, elem)
        return elem

    def add_h5(self, section, txt, **kwargs):
        elem = H5(txt, **kwargs)
        self.set_section(section, elem)
        return elem

    def add_h6(self, section, txt, **kwargs):
        elem = H6(txt, **kwargs)
        self.set_section(section, elem)
        return elem

    def add_p(self, section, txt, **kwargs):
        elem = P(txt, **kwargs)
        self.set_section(section, elem)
        return elem

    def add_a(self, elem, link):
        elem.e__add_link(link)
        return elem

    def add_ol(self, section, **kwargs):
        elem = OL(**kwargs)
        self.set_section(section, elem)
        return elem

    def add_ul(self, section, **kwargs):
        elem = UL(**kwargs)
        self.set_section(section, elem)
        return elem


if __name__ == "__main__":
    html = HTMLFile("html_1", title="Sample HTML file 1")
    # html.add_h1("head", "HEADER Hello World!! - 1")
    # footer_h1 = html.add_h1("foot", "FOOTER Hello World!! - 1")
    # html.add_h1("body", "Hello World!! - 1", style="color:red")
    # html.add_h2("body", "Hello World!! - 2", style="color:orange padding=45px")
    # html.add_h3("body", "Hello World!! - 3", style="color:yellow")
    # html.add_h4("body", "Hello World!! - 4", style="color:blue")
    # html.add_h5("body", "Hello World!! - 5", style="color:indigo")
    # html.add_h6("body", "Hello World!! - 6", style="color:violet")
    # html.add_p("body", "This is a paragraph tag\n does it work with line breaks? let's find out!")
    # logo = html.add_image("body", "https://www.bwstrailers.com/wp-content/uploads/2020/11/BWS-Chrome-Final-WO-Manufacturing.png")
    # ord_lst = html.add_ol("body", start=10)
    # ord_lst + 15
    # ord_lst + 16
    # ord_lst + 17
    # ord_lst + 25
    uord_lst = html.add_ul("head", style="color:lime; font-weight=1800; font-size=60px")
    uord_lst + 15
    uord_lst + 16
    uord_lst + LI(17, style="color:yellow; font-weight=1800; font-size=60p")
    uord_lst + 25



    # html.add_a(logo, "https://www.youtube.com/")  #  *OR*  logo.add_link("https://www.youtube.com/")
    # footer_h1.e__add_link("https://www.cbc.ca")

    # alt="BWS Manufacturing" srcset="https://www.bwstrailers.com/wp-content/uploads/2020/11/BWS-Chrome-Final-WO-Manufacturing.png 1x, https://www.bwstrailers.com/wp-content/uploads/2020/11/BWS-Chrome-Final-WO-Manufacturing.png 2x" >


    html.save()
    html.open()
