from utility import *

"""
	General JSON Writer class
	Version...............1.2
	Date...........2022-04-20
	Author.......Avery Briggs
"""


class JSONWriter:

    def __init__(self, output_file=None):
        self.tab = "    "
        self.output_file = output_file
        self.tab_depth = 0
        self._string = ""
        self.started = False, None
        self.items = {}

    def get_string(self):
        return self._string

    def set_string(self, value):
        if not self.started[0]:
            raise ValueError(
                "Cannot begin writing to this json file because it has not been \'started\' yet.\nYou must call \'start()\' before values canbe written.")
        self._string = value

    def del_string(self):
        del self._string

    def start(self, obj=True):
        self.started = True, obj
        if obj:
            self.ooj(use_tab=False)
        else:
            self.oar(use_tab=False)

    def stop(self):
        if not self.started[0]:
            raise ValueError("Cannot stop, writing has not started yet")
        if self.started[1]:
            self.coj(next=False)
        else:
            self.car(next=False)

    def reset(self):
        self.tab_depth = 0
        self.string = ""
        self.started = False, None

    def save(self, file_name=None):
        if not self.started[0]:
            self.start()
            self.stop()
        if self.output_file is not None or file_name is not None:
            fn = self.output_file if self.output_file is not None else file_name
            if "." not in fn:
                fn = fn + ".json"
            try:
                with open(fn, "w") as f:
                    f.write(self.string)
            except FileNotFoundError:
                raise FileNotFoundError("File not Found error")
        else:
            raise FileExistsError("Cannot create a file without a name.")

    def tdp(self, depth=None, write=True):
        # s = self.tab_depth * "\t"
        s = (self.tab_depth if depth is None else depth) * self.tab
        print(f"A: <{self.string}>")
        print(f"TDP s: <{s}>, td: {(self.tab_depth if depth is None else depth)}")
        if write:
            self.string += s
        print(f"B: <{self.string}>")
        return s

    def ooj(self, use_tab=True):
        self.tab_depth += 1
        if self.tab_depth not in self.items:
            self.items.update({self.tab_depth: {}})
        # s = ((self.tab_depth - 1) * "\t" if use_tab else "") + "{\n"
        s = ((self.tab_depth - 1) * self.tab if use_tab else "") + "{\n"
        self.string += s
        return s

    def coj(self, next=False):
        self.tab_depth -= 1
        # s = "\n" + max(0, self.tab_depth) * "\t" + "}" + ("," if next else "")
        s = "\n" + max(0, self.tab_depth) * self.tab + "}" + ("," if next else "")
        self.string += s
        return s

    def oar(self, use_tab=True):
        self.tab_depth += 1
        if self.tab_depth not in self.items:
            self.items.update({self.tab_depth: {}})
        # s = ((self.tab_depth - 1) * "\t" if use_tab else "") + "{\n"
        s = ((self.tab_depth - 1) * self.tab if use_tab else "") + "[\n"
        self.string += s
        return s

    def car(self, next=False):
        self.tab_depth -= 1
        # s = "\n" + max(0, self.tab_depth) * "\t" + "}" + ("," if next else "")
        s = "\n" + max(0, self.tab_depth) * self.tab + "]" + ("," if next else "")
        self.string += s
        return s

    def okey(self, k_name, new_line=True):
        s = ("\n" if new_line else "") + self.tdp(write=False) + f"\"{k_name}\": " + self.ooj(use_tab=False)
        self.string += s
        return s

    def ckey(self, next=False):
        s = self.tdp() + self.coj(next=next)
        self.string += s
        return s

    def wkv(self, k, v, next=False, new_line=False):
        """Remember to properly pass 'next' and 'new_line' params to ensure valid JSON"""
        print(f"TD: {self.tab_depth}")
        x = "\"" if isinstance(v, str) else ""
        if v == "null":
            x = ""
        if isinstance(v, bool):
            if v:
                v = "true"
            else:
                v = "false"
        print("\'f\': <{}>".format(k))
        s = "{t}\"{k}\": {x}{v}{x}{n}{l}".format(t=self.tdp(depth=1, write=False), k=k, v=v, n=',' if next else '',
                                                 l='\n' if new_line else '', x=x)
        print("CALC S: <{}>".format(s))
        # s = "{t}\"{k}\": {x}{v}{x}{n}{l}".format(t="@", k=k, v=v, n=',' if next else '', l='\n' if new_line else '', x=x)
        add_new = False
        add_tab = False
        # asdg = self.string[-1] == '\t'
        # print(f"EW: <{self.string[-1]}> ==NL: {(asdg)} ==T: {asdg}")
        if self.string.endswith("\n"):
            add_new = True
        if self.string.endswith(self.tab):
            add_new = True
            add_tab = True
        adjust = not self.string.strip().endswith(",") and self.items[self.tab_depth]
        print("adjust: {}".format(adjust))
        if adjust:
            self.string = self.string.strip() + ","
        if add_new and adjust:
            self.string = self.string.strip() + "\n"
        if add_tab and adjust:
            self.string += self.tab
        self.string += s
        self.record(k, v)
        # self.items[self.tab_depth].append((k, v))
        return s

    def wakv(self, k, *v):
        # """Remember to properly pass 'next' and 'new_line' params to ensure valid JSON"""
        print(f"k: {k} <{type(k)}>, v: {v} <{type(v)}>")
        if isinstance(k, dict):
            if len(v) != 0:
                raise ValueError("Parameter \'v\' must be omitted when passing a dict for parameter \'k\'.")
            else:
                r = []
                for kk, kv in k.items():
                    r.append(kk)
                    r.append(kv)
                k = r
        elif not isinstance(k, list) and not isinstance(k, tuple):
            k = [k]
        v = list(v)
        lst = k + v
        evens = [v for i, v in enumerate(lst) if i % 2 == 0]
        odds = [v for i, v in enumerate(lst) if i % 2 == 1]
        l = len(lst) // 2
        print(f"l: {l}")
        s = ""
        for i, even_odd in enumerate(zip(evens, odds)):
            even, odd = even_odd
            s += self.wkv(even, odd, next=i != (l - 1), new_line=i != (l - 1))
            print(f"i != (l - 1): i: {i}, l: {l}, r: {i != (l - 1)}, s: <{s}>")
        return s
        # x = "\"" if isinstance(v, str) else ""
        # if v == "null":
        #     x = ""
        # s = "{t}\"{k}\": {x}{v}{x}{n}{l}".format(t=self.tdp(), k=k, v=v, n=',' if next else '', l='\n' if new_line else '', x=x)
        # self.string += s
        # return s

    def wel(self, el, next=False, new_line=True):
        s = "{t}{x}{e}{x}{c}{n}".format(t=self.tdp(depth=1), e=el, c=", " if next else "", n="\n" if new_line else "",
                                        x="\"" if isinstance(el, str) else "")
        self.string += s
        return s

    def war(self, a):
        if isinstance(a, tuple):
            a = list(a)
        if not isinstance(a, list):
            raise TypeError("Param \'a\' must be either a list or a tuple, got: \'{}\'".format(type(a)))
        self.oar()
        for i, el in enumerate(a):
            x = i != len(a) - 1
            self.wel(el, next=x, new_line=x)
        self.car()
        s = str()
        self.string += s
        return s

    def woj(self, o):
        pass

    def record(self, k, v, depth=None):
        d = self.tab_depth if depth is None else depth
        if k in self.items[d]:
            raise KeyError("This k=\'{}\' cannot be duplicated within the same nesting.")
        self.items[d][k] = v

    string = property(get_string, set_string, del_string)


def test_1():
    jw = JSONWriter()
    jw.start()
    jw.stop()
    jw.save("demo")
    print(f"STR: <{jw.string}>")


def test_2():
    jw = JSONWriter()
    jw.start()
    jw.wkv("key1", "value1")
    jw.stop()
    jw.save("demo")
    print(f"STR: <{jw.string}>")


def test_3():
    jw = JSONWriter()
    jw.start()
    jw.wakv("key1", "Value1", "key2", "Value2")  # passing multiple keys + values
    jw.wakv(["key3", "Value3", "key4", "Value4"])  # passing list of multiple keys + values
    jw.wakv({"key5": "Value5", "key6": "Value6"})  # passing dict of multiple keys + values
    jw.wakv(["5", "Value5", "6", "Value6"], ["a", "b"])  # multiple lists of multiple keys + values
    # jw.wakv({"key5": "Value5", "key6": "Value6"}, ["a", "b"])  # ensure this doesnt work
    jw.stop()
    jw.save("demo")
    print(f"STR: <{jw.string}>")
    print(dict_print(jw.items, "Items"))


def test_4():
    jw = JSONWriter()
    jw.start()
    jw.wakv("key1", "Value1", "key2", "Value2")  # passing multiple keys + values
    jw.wakv(["key3", False, "key4", True])  # passing list of multiple keys + values
    jw.wakv(["key5", 18, "key6", 19.2])  # passing list of multiple keys + values
    jw.okey("List")
    jw.ckey()
    # jw.wakv({"key5": "Value5", "key6": "Value6"})  # passing dict of multiple keys + values
    # jw.wakv(["5", "Value5", "6", "Value6"], ["a", "b"])  # multiple lists of multiple keys + values
    # jw.wakv({"key5": "Value5", "key6": "Value6"}, ["a", "b"])  # ensure this doesnt work
    jw.stop()
    jw.save("demo")
    print(f"STR: <{jw.string}>")
    print(dict_print(jw.items, "Items"))


def test_5():
    jw = JSONWriter()
    jw.start(obj=False)
    jw.war([1, 2, "three", """four""", 5.5])
    jw.stop()
    jw.save("demo")
    print(f"STR: <{jw.string}>")
    print(dict_print(jw.items, "Items"))


if __name__ == "__main__":
    # test_1()
    # test_2()
    test_3()
    # test_4()
    # test_5()