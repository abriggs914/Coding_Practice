from utility import *


"""
	General JSON Writer class
	Version...............1.2
	Date...........2022-04-20
	Author.......Avery Briggs
"""


class JSONWriter:

    def __init__(self, output_file=None):
        self.output_file = output_file
        self.tab_depth = 0
        self.string = ""
        self.started = False
        self.items = {}

    def start(self):
        self.started = True
        self.ooj(use_tab=False)

    def stop(self):
        self.coj(next=False)

    def reset(self):
        self.tab_depth = 0
        self.string = ""
        self.started = False

    def save(self, file_name=None):
        if not self.started:
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

    def tdp(self):
        s = self.tab_depth * "\t"
        self.string += s
        return s

    def ooj(self, use_tab=True):
        self.tab_depth += 1
        if self.tab_depth not in self.items:
            self.items.update({self.tab_depth: []})
        s = ((self.tab_depth - 1) * "\t" if use_tab else "") + "{\n"
        self.string += s
        return s

    def coj(self, next=False):
        self.tab_depth -= 1
        s = "\n" + max(0, self.tab_depth) * "\t" + "}" + ("," if next else "")
        self.string += s
        return s

    def okey(self, k_name, new_line=True):
        s = ("\n" if new_line else "") + self.tdp() + f"\"{k_name}\": " + self.ooj(use_tab=False)
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
        s = "{t}\"{k}\": {x}{v}{x}{n}{l}".format(t=self.tdp(), k=k, v=v, n=',' if next else '', l='\n' if new_line else '', x=x)
        add_new = False
        add_tab = False
        # asdg = self.string[-1] == '\t'
        # print(f"EW: <{self.string[-1]}> ==NL: {(asdg)} ==T: {asdg}")
        if self.string.endswith("\n"):
            add_new = True
        if self.string.endswith("\t"):
            add_new = True
        adjust = not self.string.strip().endswith(",") and self.items[self.tab_depth]
        if adjust:
            self.string = self.string.strip() + ","
        if add_new and adjust:
            self.string = self.string.strip() + "\n"
        # if add_tab and adjust:
        #     self.string += "\t"
        self.string += s
        self.items[self.tab_depth].append((k, v))
        return s

    def wakv(self, k, *v, next=False, new_line=False):
        """Remember to properly pass 'next' and 'new_line' params to ensure valid JSON"""
        print(f"k: {k} <{type(k)}>, v: {v} <{type(v)}>")
        if not isinstance(k, list) and not isinstance(k, tuple):
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
    jw.wakv("key1", "Value1", "key2", "Value2")
    jw.wakv(["key3", "Value3", "key4", "Value4"])
    jw.stop()
    jw.save("demo")
    print(f"STR: <{jw.string}>")
    print(dict_print(jw.items, "Items"))


if __name__ == "__main__":
    test_1()
    test_2()
    test_3()
