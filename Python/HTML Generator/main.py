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
                n_lines = n_lines[:h if len(n_lines) > 1 else 1] + lines + n_lines[h if len(n_lines) % 2 == 0 else h + 1:]
                print("lines:", lines, "n_lines:", og, "n_lines:", n_lines)
                for line in n_lines:
                    elem = isinstance(line, Element)
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

    def open(self):
        if self.f_name in os.listdir():
            webbrowser.open(self.f_name)

    def add_image(self, section, src, **kwargs):
        elem = Img(src, kwargs)
        self.set_section(section, elem)
        return elem

    def add_h1(self, section, txt, **kwargs):
        elem = H1(txt, kwargs)
        self.set_section(section, elem)
        return elem

    def add_h2(self, section, txt, **kwargs):
        elem = H2(txt, kwargs)
        self.set_section(section, elem)
        return elem

    def add_h3(self, section, txt, **kwargs):
        elem = H3(txt, kwargs)
        self.set_section(section, elem)
        return elem

    def add_h4(self, section, txt, **kwargs):
        elem = H4(txt, kwargs)
        self.set_section(section, elem)
        return elem

    def add_h5(self, section, txt, **kwargs):
        elem = H5(txt, kwargs)
        self.set_section(section, elem)
        return elem

    def add_h6(self, section, txt, **kwargs):
        elem = H6(txt, kwargs)
        self.set_section(section, elem)
        return elem

    def add_p(self, section, txt, **kwargs):
        elem = P(txt, kwargs)
        self.set_section(section, elem)
        return elem

    def add_a(self, elem, link):
        elem.add_link(link)
        return elem


if __name__ == "__main__":
    html = HTMLFile("html_1", title="Sample HTML file 1")
    html.add_h1("head", "HEADER Hello World!! - 1")
    footer_h1 = html.add_h1("foot", "FOOTER Hello World!! - 1")
    html.add_h1("body", "Hello World!! - 1")
    html.add_h2("body", "Hello World!! - 2")
    html.add_h3("body", "Hello World!! - 3")
    html.add_h4("body", "Hello World!! - 4")
    html.add_h5("body", "Hello World!! - 5")
    html.add_h6("body", "Hello World!! - 6")
    html.add_p("body", "This is a paragraph tag\n does it work with line breaks? let's find out!")
    logo = html.add_image("body", "https://www.bwstrailers.com/wp-content/uploads/2020/11/BWS-Chrome-Final-WO-Manufacturing.png")
    html.add_a(logo, "https://www.youtube.com/")  #  *OR*  logo.add_link("https://www.youtube.com/")
    footer_h1.add_link("https://www.cbc.ca")

    # alt="BWS Manufacturing" srcset="https://www.bwstrailers.com/wp-content/uploads/2020/11/BWS-Chrome-Final-WO-Manufacturing.png 1x, https://www.bwstrailers.com/wp-content/uploads/2020/11/BWS-Chrome-Final-WO-Manufacturing.png 2x" >


    html.save()
    html.open()
