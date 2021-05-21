class Element:

    def __init__(self, desc, clazz=None, id_n=None):
        self.desc = desc
        self.id_n = id_n
        self.clazz = clazz

        self.link_ref = None

    # txt can be another element object.
    def add_link(self, a):
        self.link_ref = a

    def get_link(self):
        if not self.link_ref:
            return ""
        link = self.link_ref
        return "<a href=\'" + link + "\'>", "</a>"


class Img(Element):

    def __init__(self, resource, clazz=None, id_n=None, style=None):
        super().__init__("IMAGE", clazz=clazz, id_n=id_n)
        self.resource = resource
        self.style = style
        self.tag_open = "<img"
        self.tag_close = ">"

    def __repr__(self):
        linked = self.get_link()
        op, cl = "", ""
        if linked:
            op, cl = linked
        return op + " ".join([
            self.tag_open,
            "" if not self.id_n else " id=" + self.id_n,
            "" if not self.clazz else " class=" + self.clazz,
            " src=" + self.resource,
            self.tag_close
        ]) + cl


class H1(Element):

    def __init__(self, txt, clazz=None, id_n=None, style=None):
        super().__init__("H1", clazz=clazz, id_n=id_n)
        self.txt = txt
        self.style = style
        self.tag_open = "<h1>"
        self.tag_close = "</h1>"

    def __repr__(self):
        linked = self.get_link()
        op, cl = "", ""
        if linked:
            op, cl = linked
        return op + " ".join([
            self.tag_open,
            "" if not self.id_n else " id=" + self.id_n,
            "" if not self.clazz else " class=" + self.clazz,
            self.txt,
            self.tag_close
        ]) + cl


class H2(Element):

    def __init__(self, txt, clazz=None, id_n=None, style=None):
        super().__init__("H2", clazz=clazz, id_n=id_n)
        self.txt = txt
        self.style = style
        self.tag_open = "<h2>"
        self.tag_close = "</h2>"

    def __repr__(self):
        linked = self.get_link()
        op, cl = "", ""
        if linked:
            op, cl = linked
        return op + " ".join([
            self.tag_open,
            "" if not self.id_n else " id=" + self.id_n,
            "" if not self.clazz else " class=" + self.clazz,
            self.txt,
            self.tag_close
        ]) + cl


class H3(Element):

    def __init__(self, txt, clazz=None, id_n=None, style=None):
        super().__init__("H3", clazz=clazz, id_n=id_n)
        self.txt = txt
        self.style = style
        self.tag_open = "<h3>"
        self.tag_close = "</h3>"

    def __repr__(self):
        linked = self.get_link()
        op, cl = "", ""
        if linked:
            op, cl = linked
        return op + " ".join([
            self.tag_open,
            "" if not self.id_n else " id=" + self.id_n,
            "" if not self.clazz else " class=" + self.clazz,
            self.txt,
            self.tag_close
        ]) + cl


class H4(Element):

    def __init__(self, txt, clazz=None, id_n=None, style=None):
        super().__init__("H4", clazz=clazz, id_n=id_n)
        self.txt = txt
        self.style = style
        self.tag_open = "<h4>"
        self.tag_close = "</h4>"

    def __repr__(self):
        linked = self.get_link()
        op, cl = "", ""
        if linked:
            op, cl = linked
        return op + " ".join([
            self.tag_open,
            "" if not self.id_n else " id=" + self.id_n,
            "" if not self.clazz else " class=" + self.clazz,
            self.txt,
            self.tag_close
        ]) + cl


class H5(Element):

    def __init__(self, txt, clazz=None, id_n=None, style=None):
        super().__init__("H5", clazz=clazz, id_n=id_n)
        self.txt = txt
        self.style = style
        self.tag_open = "<h5>"
        self.tag_close = "</h5>"

    def __repr__(self):
        linked = self.get_link()
        op, cl = "", ""
        if linked:
            op, cl = linked
        return op + " ".join([
            self.tag_open,
            "" if not self.id_n else " id=" + self.id_n,
            "" if not self.clazz else " class=" + self.clazz,
            self.txt,
            self.tag_close
        ]) + cl


class H6(Element):

    def __init__(self, txt, clazz=None, id_n=None, style=None):
        super().__init__("H6", clazz=clazz, id_n=id_n)
        self.txt = txt
        self.style = style
        self.tag_open = "<h6>"
        self.tag_close = "</h6>"

    def __repr__(self):
        linked = self.get_link()
        op, cl = "", ""
        if linked:
            op, cl = linked
        return op + " ".join([
            self.tag_open,
            "" if not self.id_n else " id=" + self.id_n,
            "" if not self.clazz else " class=" + self.clazz,
            self.txt,
            self.tag_close
        ]) + cl


class P(Element):

    def __init__(self, txt, clazz=None, id_n=None, style=None):
        super().__init__("P", clazz=clazz, id_n=id_n)
        self.txt = txt
        self.style = style
        self.tag_open = "<p>"
        self.tag_close = "</p>"

    def __repr__(self):
        linked = self.get_link()
        op, cl = "", ""
        if linked:
            op, cl = linked
        return op + " ".join([
            self.tag_open,
            "" if not self.id_n else " id=" + self.id_n,
            "" if not self.clazz else " class=" + self.clazz,
            self.txt,
            self.tag_close
        ]) + cl


# class A(Element):
#
#     def __init__(self, link, clazz=None, id_n=None, style=None):
#         super().__init__("P", clazz=clazz, id_n=id_n)
#         self.txt = txt
#         self.style = style
#         self.tag_open = "<p>"
#         self.tag_close = "</p>"
#
#     def __repr__(self):
#         return " ".join([
#             self.tag_open,
#             "" if not self.id_n else " id=" + self.id_n,
#             "" if not self.clazz else " class=" + self.clazz,
#             self.txt,
#             self.tag_close
#         ])
