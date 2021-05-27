# TODO: Convert all html creation code to list format. Main file-writer will split lists of contents and be able to
#  write nested elements more simply then the current string-only approach.

class Element:

    def __init__(self, desc, **kwargs):
        self.e__desc = desc
        for attr, val in kwargs.items():
            setattr(self, attr, val)
        self.e__link_ref = None
        self.e__children = []

    # txt can be another element object.
    def e__add_link(self, a):
        self.e__link_ref = a

    def e__get_link(self):
        if not self.e__link_ref:
            return ""
        link = self.e__link_ref
        return "<a href=\'" + link + "\'>", "</a>"

    def e__collect_kwargs(self):
        attrs = [attr for attr in dir(self) if not attr.startswith("__")]
        kwargs = {}
        for attr in attrs:
            if not attr.startswith("e__"):
                print("\t\tattr t: <{0}>:".format(type(getattr(self, attr))), attr)
                kwargs[attr] = getattr(self, attr)

        return " " + " ".join([k + "=\'" + str(v) + "\'" for k, v in kwargs.items()])

    def e__get_children(self):
        return self.e__children


class Img(Element):

    def __init__(self, resource, **kwargs):
        super().__init__("IMAGE", **kwargs)
        self.e__resource = resource
        self.e__tag_open = "<img"
        self.e__tag_close = ">"
        self.e__children = [" src=" + self.e__resource]

    def e__get_children(self):
        # children = [self.e__tag_open] + self.e__children + [self.e__collect_kwargs()] + [self.e__tag_close]
        linked = self.e__get_link()
        if linked:
            op, cl = linked
            # children = [op] + children + [cl]

        #     x = [self.e__tag_open] + self.e__children + [self.e__collect_kwargs()] + [self.e__tag_close]
        #     print('''{op}\n\t{eto} {kwargs} src={resource}{etc}\n{cl}'''.format(op=op, kwargs=self.e__collect_kwargs(), eto=self.e__tag_open, resource=self.e__resource, etc=self.e__tag_close, cl=cl))
        # return children
        s = str(self)
        spl = s.split("\n")
        tab_idxs = [i for i in range(len(s)) if s[i] == "\t"]
        t = tab_idxs.copy()
        tab_idxs = []
        i = 0
        while i < len(t):
            j = i
            c = 0
            while j < len(t) - 1 and t[j] == t[j - 1] + 1:
                j += 1
                c += 1
            tab_idxs.append((i, c))
            i += j + 1
        print("tab_idxs {}:".format(len(tab_idxs)), tab_idxs)
        print("t {}:".format(len(t)), t)
        print("spl {}:".format(len(spl)), spl)
        return []


        #     if i < len(tab_idxs) - 1:
        #         n = tab_idxs[i + 1]
        #
        #     i += 1
        # children = []
        # for line in spl:
        #     children.append([None for i in range()])


    def __repr__(self):
        linked = self.e__get_link()
        op, cl = "", ""
        if linked:
            op, cl = linked
        return '''{op}\n\t{eto} {kwargs} src={resource}{etc}\n{cl}'''.format(op=op, kwargs=self.e__collect_kwargs(), eto=self.e__tag_open, resource=self.e__resource, etc=self.e__tag_close, cl=cl)


class H1(Element):

    def __init__(self, txt, **kwargs):
        super().__init__("H1", **kwargs)
        self.e__txt = txt
        self.e__tag_open = "<h1>"
        self.e__tag_close = "</h1>"

    def __repr__(self):
        linked = self.e__get_link()
        op, cl = "", ""
        if linked:
            op, cl = linked
        return op + " ".join([
            self.e__tag_open[:-1],
            self.e__collect_kwargs(),
            self.e__tag_close[-1],
            self.e__txt,
            self.e__tag_close
        ]) + cl


class H2(Element):

    def __init__(self, txt, **kwargs):
        super().__init__("H2", **kwargs)
        self.txt = txt
        self.e__tag_open = "<h2>"
        self.e__tag_close = "</h2>"

    def __repr__(self):
        linked = self.e__get_link()
        op, cl = "", ""
        if linked:
            op, cl = linked
        return op + " ".join([
            self.e__tag_open[:-1],
            self.e__collect_kwargs(),
            self.e__tag_close[-1],
            self.txt,
            self.e__tag_close
        ]) + cl


class H3(Element):

    def __init__(self, txt, **kwargs):
        super().__init__("H3", **kwargs)
        self.e__txt = txt
        self.e__tag_open = "<h3>"
        self.e__tag_close = "</h3>"

    def __repr__(self):
        linked = self.e__get_link()
        op, cl = "", ""
        if linked:
            op, cl = linked
        return op + " ".join([
            self.e__tag_open[:-1],
            self.e__collect_kwargs(),
            self.e__tag_close[-1],
            self.e__txt,
            self.e__tag_close
        ]) + cl


class H4(Element):

    def __init__(self, txt, **kwargs):
        super().__init__("H4", **kwargs)
        self.e__txt = txt
        self.e__tag_open = "<h4>"
        self.e__tag_close = "</h4>"

    def __repr__(self):
        linked = self.e__get_link()
        op, cl = "", ""
        if linked:
            op, cl = linked
        return op + " ".join([
            self.e__tag_open[:-1],
            self.e__collect_kwargs(),
            self.e__tag_close[-1],
            self.e__txt,
            self.e__tag_close
        ]) + cl


class H5(Element):

    def __init__(self, txt, **kwargs):
        super().__init__("H5", **kwargs)
        self.e__txt = txt
        self.e__tag_open = "<h5>"
        self.e__tag_close = "</h5>"

    def __repr__(self):
        linked = self.e__get_link()
        op, cl = "", ""
        if linked:
            op, cl = linked
        return op + " ".join([
            self.e__tag_open[:-1],
            self.e__collect_kwargs(),
            self.e__tag_close[-1],
            self.e__txt,
            self.e__tag_close
        ]) + cl


class H6(Element):

    def __init__(self, txt, **kwargs):
        super().__init__("H6", **kwargs)
        self.e__txt = txt
        self.e__tag_open = "<h6>"
        self.e__tag_close = "</h6>"

    def __repr__(self):
        linked = self.e__get_link()
        op, cl = "", ""
        if linked:
            op, cl = linked
        return op + " ".join([
            self.e__tag_open[:-1],
            self.e__collect_kwargs(),
            self.e__tag_close[-1],
            self.e__txt,
            self.e__tag_close
        ]) + cl


class P(Element):

    def __init__(self, txt, **kwargs):
        super().__init__("P", **kwargs)
        self.e__txt = txt
        self.e__tag_open = "<p>"
        self.e__tag_close = "</p>"

    def __repr__(self):
        linked = self.e__get_link()
        op, cl = "", ""
        if linked:
            op, cl = linked
        return op + " ".join([
            self.e__tag_open[:-1],
            self.e__collect_kwargs(),
            self.e__tag_close[-1],
            self.e__txt,
            self.e__tag_close
        ]) + cl


class LI(Element):

    def __init__(self, val, **kwargs):
        super().__init__("LI", **kwargs)
        self.e__val = val
        self.e__tag_open = "<li>"
        self.e__tag_close = "</li>"

    def __repr__(self):
        linked = self.e__get_link()
        op, cl = "", ""
        if linked:
            op, cl = linked
        return op + " ".join([
            self.e__tag_open[:-1],
            self.e__collect_kwargs(),
            self.e__tag_close[-1],
            self.e__val,
            self.e__tag_close
        ]) + cl


class OL(Element):

    # def __init__(self, clazz=None, id_n=None, style=None):
    def __init__(self, **kwargs):
        # super().__init__("OL")
        super().__init__("OL", **kwargs)
        # self.style = style
        self.e__tag_open = "<ol>"
        self.e__tag_close = "</ol>"

        self.e__items = []

    def __add__(self, other, **kwargs):
        if isinstance(other, Element):
            self.e__items.append(other)
        else:
            self.e__items.append(LI(other, **kwargs))

    def e__add_item(self, item, **kwargs):
        self.__add__(item, **kwargs)

    def __sub__(self, other):
        try:
            self.e__items.remove(other)
        except ValueError:
            print("\"{0}\" not found in list.".format(other))

    def e__sub_item(self, item):
        self - item

    def __len__(self):
        return len(self.e__items)

    def e__sort(self):
        self.e__items.sort()

    def __reversed__(self):
        self.e__items.reverse()

    def e__clear(self):
        self.e__items.clear()

    def e__display_items(self):
        return "".join([str(item) for item in self.e__items])

    def __repr__(self):
        linked = self.e__get_link()
        op, cl = "", ""
        if linked:
            op, cl = linked

        # print(self.e__tag_open)
        # print("" if not self.id_n else " id=" + self.id_n)
        # print("self.clazz:", self.clazz)
        # print("" if not self.clazz else " class=" + self.clazz)
        # print(self.e__tag_close)
        return op + " ".join([
            self.e__tag_open[:-1],
            self.e__collect_kwargs(),
            self.e__tag_close[-1],
            # self.display_items(),
            self.e__tag_close
        ]) + cl


class UL(Element):

    # def __init__(self, clazz=None, id_n=None, style=None):
    def __init__(self, **kwargs):
        # super().__init__("OL")
        super().__init__("UL", **kwargs)
        # self.style = style
        self.e__tag_open = "<ul>"
        self.e__tag_close = "</ul>"

        self.e__items = []

    def __add__(self, other):
        self.e__items.append(LI(other))

    def e__add_item(self, item):
        self + item

    def __sub__(self, other):
        try:
            self.e__items.remove(other)
        except ValueError:
            print("\"{0}\" not found in list.".format(other))

    def e__sub_item(self, item):
        self - item

    def __len__(self):
        return len(self.e__items)

    def e__sort(self):
        self.e__items.sort()

    def __reversed__(self):
        self.e__items.reverse()

    def e__clear(self):
        self.e__items.clear()

    def e__display_items(self):
        return "".join([str(item) for item in self.e__items])

    def __repr__(self):
        linked = self.e__get_link()
        op, cl = "", ""
        if linked:
            op, cl = linked

        # print(self.e__tag_open)
        # print("" if not self.id_n else " id=" + self.id_n)
        # print("self.clazz:", self.clazz)
        # print("" if not self.clazz else " class=" + self.clazz)
        # print(self.e__tag_close)
        return op + " ".join([
            self.e__tag_open[:-1],
            self.e__collect_kwargs(),
            self.e__tag_close[-1],
            # self.display_items(),
            self.e__tag_close
        ]) + cl

# class A(Element):
#
#     def __init__(self, link, clazz=None, id_n=None, style=None):
#         super().__init__("P", clazz=clazz, id_n=id_n)
#         self.txt = txt
#         self.style = style
#         self.e__tag_open = "<p>"
#         self.e__tag_close = "</p>"
#
#     def __repr__(self):
#         return " ".join([
#             self.e__tag_open,
#             "" if not self.id_n else " id=" + self.id_n,
#             "" if not self.clazz else " class=" + self.clazz,
#             self.txt,
#             self.e__tag_close
#         ])
