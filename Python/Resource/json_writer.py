import json

from utility import *
from test_suite import *

"""
	General JSON Writer class
	Version...............1.7
	Date...........2022-04-25
	Author.......Avery Briggs
"""


class JSONWriter:

    class StateException(Exception):
        def __init__(self, message):
            pass

    class StateGSM:

        # started = False
        # writing_obj = False
        # writing_arr = False
        # stopped = False

        def __init__(self):

            # self.started = JSONWriter.StateGSM.started
            # self.writing_obj = JSONWriter.StateGSM.writing_obj
            # self.writing_arr = JSONWriter.StateGSM.writing_arr
            # self.stopped = JSONWriter.StateGSM.stopped

            self.started = False
            self.writing_obj = []
            self.writing_arr = []
            self.stopped = False

        def start(self):
            if self.started:
                raise JSONWriter.StateException("Error can't start this JSON file because it is already started")
            if self.stopped:
                raise JSONWriter.StateException("Error can't start this JSON file because it has already been stopped")
            self.started = True

        def stop(self):
            if not self.started:
                raise JSONWriter.StateException("Error can't stop this JSON file because it hasn't been started yet")
            if self.stopped:
                raise JSONWriter.StateException("Error can't stop this JSON file because it has already been stopped")
            self.stopped = True

        def start_obj(self):
            if not self.started:
                raise JSONWriter.StateException(
                    "Error can't start an object in this JSON file because it hasn't been started yet")
            if self.stopped:
                raise JSONWriter.StateException(
                    "Error can't start writing an object because this JSON file has already been stopped")
            self.writing_obj.append(True)

        def stop_obj(self):
            if not self.started:
                raise JSONWriter.StateException(
                    "Error can't stop writing an object in this JSON file because it hasn't been started yet")
            if self.stopped:
                raise JSONWriter.StateException(
                    "Error can't stop writing an object because this JSON file has already been stopped")
            if not self.writing_obj:
                raise JSONWriter.StateException(
                    "Error can't stop writing an object because this JSON file has already been stopped")
            self.writing_obj.pop()

        def start_arr(self):
            if not self.started:
                raise JSONWriter.StateException(
                    "Error can't start an object in this JSON file because it hasn't started yet")
            if self.stopped:
                raise JSONWriter.StateException(
                    "Error can't start writing an array because this JSON file has already been stopped")
            print(f"START ARR A: {self.writing_arr}")
            self.writing_arr.append(True)
            print(f"START ARR B: {self.writing_arr}")

        def stop_arr(self):
            if not self.started:
                raise JSONWriter.StateException(
                    "Error can't stop an array in this JSON file because it hasn't started yet")
            if self.stopped:
                raise JSONWriter.StateException(
                    "Error can't start writing an array because this JSON file has already been stopped")
            if not self.writing_arr:
                raise JSONWriter.StateException(
                    "Error can't stop writing an array because this JSON file has already been stopped")
            print(f"STOP ARR A: {self.writing_arr}")
            self.writing_arr.pop()
            print(f"STOP ARR B: {self.writing_arr}")

        def reset(self):
            self.started = False
            self.stopped = False
            self.writing_obj = []
            self.writing_arr = []

    def __init__(self, output_file=None, start_obj=False, start_arr=False, safe=False):
        self.state = self.StateGSM()
        self.tab = "    "
        self.output_file = output_file
        self.tab_depth = 0
        self._string = ""
        # self.started = False, None, False  # has started, writing object, has stopped
        self._safe = safe
        self.items = {}
        if start_obj:
            self.start()
            self.ooj()
        elif start_arr:
            self.start()
            self.ooj()

    def get_string(self):
        return self._string

    def get_safe(self):
        return self._safe

    def set_string(self, value):
        # if not self.started[0]:
        # safe_leave = False
        # if self.safe:
        #     if not self.app_state.started:
        #         print("WARNING wrinting has begun in safe game_mode without calling \'start()\' on this file.")
        #         typ = type(value)
        #         obj = False
        #         single = True
        #         if typ in [int, float, str, bool]:
        #             obj = False
        #         elif typ in [dict]:
        #             obj = True
        #         if single:
        #             if obj:
        #                 self.wel(value)
        #             else:
        #                 self.
        #         self.start(obj=obj)
        #
        # if safe_leave:
        #     return

        if not self.state.started:
            raise self.StateException(
                "\n\tCannot begin writing to this json file because it has not been \'started\' yet.\n\tYou must call \'start()\' before values can be written.")
        if not self.state.writing_obj and not self.state.writing_arr:
            raise self.StateException(
                "\n\tCannot write to this json file because either an object or an array must be opened first.")
        self._string = value

    def set_safe(self, value):
        if self._safe is not None:
            raise self.StateException("Error cannot alter \'safe\' game_mode after creation.")
        self._safe = value

    def del_string(self):
        del self._string

    def del_safe(self):
        del self._safe

    def size(self):
        """Return text dimensions (rows x cols)"""
        return text_size(self.string)

    def test_valid_json(self):
        try:
            json.loads(self.string)
            return True
        except json.JSONDecodeError:
            return False

    def start(self, obj=True):
        # self.started = True, obj, False
        self.state.start()
        if obj:
            # self.app_state.start_obj()
            self.ooj(use_tab=False)
        else:
            # self.app_state.start_arr()
            self.oar(use_tab=False)
        return self

    def stop(self):
        # if self.app_state.started:
        #     raise self.StateException("Cannot stop, writing has not started yet")
        while self.state.writing_arr or self.state.writing_obj:
            if self.state.writing_obj:
                self.coj(next=False)
            if self.state.writing_arr:
                self.car(next=False)
        # self.started = *self.started[:2], True
        self.state.stop()
        return self

    def reset(self):
        self.tab_depth = 0
        self.string = ""
        # self.started = False, None, False
        self.state.reset()

    def save(self, file_name=None):
        # if not self.started[0]:
        if not self.state.started:
            raise self.StateException(
                "\n\tCannot save this json file because nothing has been written to it.\n\tYou must call \'start()\' and \'stop()\' to enable writing and saving.")
        # elif not self.started[2]:
        elif not self.state.stopped:
            # allow saving without calling close first. This will do it for you.
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
        return self

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
        self.state.start_obj()
        self.tab_depth += 1
        # if self.tab_depth not in self.items:
        #     # self.items.update({self.tab_depth: {}})
        #     x = ""
        # else:
        #     x = ",\n"
        x = ""
        # s = ((self.tab_depth - 1) * "\t" if use_tab else "") + "{\n"
        s = ((self.tab_depth - 1) * self.tab if use_tab else "") + x + "{\n"
        self.string += s
        # self.started = self
        return self

    def coj(self, next=False):
        # # if not self.started[0]:
        # if not self.app_state.started:
        #     raise self.StateException("Cannot close object in file that has not been started first.")
        # # if not self.started[1]:
        # if not self.app_state.writing_obj:
        #     raise self("Cannot close object that has not been opened first.")
        self.tab_depth -= 1
        # s = "\n" + max(0, self.tab_depth) * "\t" + "}" + ("," if next else "")
        s = "\n" + max(0, self.tab_depth) * self.tab + "}" + ("," if next else "")
        self.string += s
        self.state.stop_obj()
        return self

    def oar(self, use_tab=True):
        self.state.start_arr()
        self.tab_depth += 1
        # if self.app_state.writing_arr or self.app_state.writing_obj:
        #     self.string += ",\n"
        # if self.tab_depth not in self.items:
        #     self.items.update({self.tab_depth: {}})
        # s = ((self.tab_depth - 1) * "\t" if use_tab else "") + "{\n"
        s = ((self.tab_depth - 1) * self.tab if use_tab else "") + "[\n"
        self.string += s
        return self

    def car(self, next=False):
        self.tab_depth -= 1
        # s = "\n" + max(0, self.tab_depth) * "\t" + "}" + ("," if next else "")
        s = "\n" + max(0, self.tab_depth) * self.tab + "]" + ("," if next else "")
        self.string += s
        self.state.stop_arr()
        return self

    def okey(self, k_name, new_line=True):
        s = ("\n" if new_line else "") + self.tdp(write=False) + f"\"{k_name}\": "
        self.ooj(use_tab=False)
        self.string += s
        return self

    def ckey(self, next=False):
        self.tdp()
        self.coj(next=next)
        # self.string += s
        return self

    def wkv(self, k, v, next=False, new_line=False, new_obj=False):
        """Remember to properly pass 'next' and 'new_line' params to ensure valid JSON"""
        if new_obj:
            self.ooj()
        print(f"TD: {self.tab_depth}")
        x = "\"" if isinstance(v, str) else ""
        if v == "null":
            x = ""
        if isinstance(v, bool):
            if v:
                v = "true"
            else:
                v = "false"

        s = ""
        print("\'f\': <{}>".format(k))
        print("CALC S: <{}>".format(s))
        # s = "{t}\"{k}\": {x}{v}{x}{n}{l}".format(t="@", k=k, v=v, n=',' if next else '', l='\n' if new_line else '', x=x)
        add_new = False
        add_tab = False
        # asdg = self.string[-1] == '\t'
        # print(f"EW: <{self.string[-1]}> ==NL: {(asdg)} ==T: {asdg}")
        add_new = True
        skip_comma = False
        # if self.string.endswith("\n"):
        if self.string.endswith(self.tab):
            add_new = True
            add_tab = True
        elif self.string.strip().endswith("{") or self.string.strip().endswith("["):
            skip_comma = True
        # adjust = not bool(self.string.strip().endswith(",")) and bool(self.items[self.tab_depth])
        adjust = not bool(self.string.strip().endswith(","))
        print("adjusted: {}, an: {}, at: {}".format(adjust, add_new, add_tab))
        if adjust:
            self.string = self.string.strip() + ("," if not skip_comma else "")
        if add_new and adjust:
            self.string = self.string.strip() + "\n"
        if add_tab and adjust:
            self.string += self.tab

        self.string += "{t}\"{k}\": ".format(t=self.tdp(write=False), k=k)
        if isinstance(v, dict):
            self.woj(v, nested=True)
            self.string += "{n}{l}".format(n=',' if next else '', l='\n' if new_line else '')
        elif isinstance(v, list) or isinstance(v, tuple):
            self.war(v, nested=True)
            self.string += "{n}{l}".format(n=',' if next else '', l='\n' if new_line else '')
        else:
            s = "{x}{v}{x}{n}{l}".format(v=v, n=',' if next else '', l='\n' if new_line else '', x=x)
            self.string += s
        # self.items[self.tab_depth].append((k, v))
        self.record(k, v)
        if new_obj:
            self.coj()
        return self

    def wakv(self, k, *v, new_obj=False):
        # """Remember to properly pass 'next' and 'new_line' params to ensure valid JSON"""
        if new_obj:
            self.ooj()
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
        # s = ""
        for i, even_odd in enumerate(zip(evens, odds)):
            even, odd = even_odd
            self.wkv(even, odd, next=i != (l - 1), new_line=i != (l - 1))
            # print(f"i != (l - 1): i: {i}, l: {l}, r: {i != (l - 1)}, s: <{s}>")
        # self.string += s
        if new_obj:
            self.coj()
        return self
        # x = "\"" if isinstance(v, str) else ""
        # if v == "null":
        #     x = ""
        # s = "{t}\"{k}\": {x}{v}{x}{n}{l}".format(t=self.tdp(), k=k, v=v, n=',' if next else '', l='\n' if new_line else '', x=x)
        # self.string += s
        # return s

    def wel(self, el, next=False, new_line=False, new_arr=False):
        if new_arr:
            self.oar()
        not_str = False
        if el is None:
            el = "null"
            not_str = True
        elif isinstance(el, bool):
            if el:
                el = "true"
            else:
                el = "false"
            not_str = True
        s = ""

        # s = "{t}\"{k}\": {x}{v}{x}{n}{l}".format(t="@", k=k, v=v, n=',' if next else '', l='\n' if new_line else '', x=x)
        # add_new = False
        add_tab = False
        # asdg = self.string[-1] == '\t'
        # print(f"EW: <{self.string[-1]}> ==NL: {(asdg)} ==T: {asdg}")
        add_new = True
        skip_comma = False
        # if self.string.endswith("\n"):
        #     add_new = True
        if self.string.endswith(self.tab):
            add_new = True
            add_tab = True
        elif self.string.strip().endswith("{") or self.string.strip().endswith("["):
            skip_comma = True
        # adjust = not bool(self.string.strip().endswith(",")) and bool(self.items[self.tab_depth])
        adjust = not bool(self.string.strip().endswith(","))
        print("adjusted: {}, an: {}, at: {}".format(adjust, add_new, add_tab))
        if adjust:
            self.string = self.string.strip() + ("," if not skip_comma else "")
        if add_new and adjust:
            self.string = self.string.strip() + "\n"
        if add_tab and adjust:
            self.string += self.tab

        if isinstance(el, dict) and el:
            self.woj(el)
        elif (isinstance(el, list) or isinstance(el, tuple)) and el:
            self.war(el)
        else:
            # next = next if not (self.string.strip().endswith("{") or self.string.strip().endswith("[")) else False
            s = "{t}{x}{e}{x}{c}{n}".format(t=self.tdp(write=False), e=el, c=", " if next else "",
                                            n="\n" if new_line else "",
                                            x="\"" if isinstance(el, str) and not not_str else "")
        self.string += s
        if new_arr:
            self.car()
        return self

    def war(self, a, nested=False):
        if isinstance(a, tuple):
            a = list(a)
        if not isinstance(a, list):
            raise TypeError("Param \'a\' must be either a list or a tuple, got: \'{}\'".format(type(a)))
        self.oar(use_tab=not nested)
        # s = ""
        for i, el in enumerate(a):
            x = i != len(a) - 1
            # s += self.wel(el, next=x, new_line=x)
            self.wel(el, next=x, new_line=x)
        self.car()
        # s = str()
        # self.string += s
        return self

    def woj(self, o, nested=False):
        if not isinstance(o, dict):
            raise TypeError("Param \'a\' must be either a dict, got: \'{}\'".format(type(o)))
        self.ooj(use_tab=not nested)
        # s = ""
        for i, kv in enumerate(o.items()):
            k, v = kv
            x = i != len(o) - 1
            # s += self.wel(el, next=x, new_line=x)
            self.wkv(k, v, next=x, new_line=x)
        self.coj()
        # s = str()
        # self.string += s
        return self

    def record(self, k, v, depth=None):
        d = self.tab_depth if depth is None else depth
        # if k in self.items[dictionary]:
        #     raise KeyError("This k=\'{}\' cannot be duplicated within the same nesting.")
        # self.items[dictionary][k] = v

    string = property(get_string, set_string, del_string)
    safe = property(get_safe, set_safe, del_safe)

    def __repr__(self):
        return self.string


def test_1():
    jw = JSONWriter().start().ooj().coj().stop().save("demo")
    print(f"STR: <{jw.string}>")
    print(f"STR: <" + jw.string + ">")
    return jw.string


def test_2():
    jw = JSONWriter()
    jw.start()
    jw.wkv("key1", "value1", new_obj=True)
    jw.stop()
    jw.save("demo")
    print(f"STR: <{jw.string}>")
    return jw.string


def test_3():
    jw = JSONWriter()
    jw.start()
    jw.ooj()
    jw.wakv("key1", "Value1", "key2", "Value2")  # passing multiple keys + values
    jw.wakv(["key3", "Value3", "key4", "Value4"])  # passing list of multiple keys + values
    # jw.wakv({"key5": "Value5", "key6": "Value6"})  # passing dict of multiple keys + values
    # jw.wakv(["5", "Value5", "6", "Value6"], ["a", "b"])  # multiple lists of multiple keys + values
    # jw.wakv({"key5": "Value5", "key6": "Value6"}, ["a", "b"])  # ensure this doesnt work
    jw.coj()
    jw.stop()
    jw.save("demo")
    print(f"STR: <{jw.string}>")
    print(dict_print(jw.items, "Items"))
    return jw.string


def test_4():
    jw = JSONWriter()
    jw.start()
    jw.ooj()
    jw.wakv("key1", "Value1", "key2", "Value2")  # passing multiple keys + values
    jw.wakv(["key3", False, "key4", True])  # passing list of multiple keys + values
    jw.wakv(["key5", 18, "key6", 19.2])  # passing list of multiple keys + values
    # jw.okey("List")
    jw.ckey()
    # jw.wakv({"key5": "Value5", "key6": "Value6"})  # passing dict of multiple keys + values
    # jw.wakv(["5", "Value5", "6", "Value6"], ["a", "b"])  # multiple lists of multiple keys + values
    # jw.wakv({"key5": "Value5", "key6": "Value6"}, ["a", "b"])  # ensure this doesnt work
    jw.stop()
    jw.save("demo")
    print(f"STR: <{jw.string}>")
    print(dict_print(jw.items, "Items"))
    return jw.string


def test_5():
    jw = JSONWriter()
    jw.start()
    jw.war([1, 2, "three", """four""", 5.5])
    # jw.stop()
    jw.save("demo")
    print(f"STR: <{jw.string}>")
    print(dict_print(jw.items, "Items"))
    return jw.string


def test_6():
    jw = JSONWriter()
    jw.start().war([1, 2, "eight", """nine""", "none", None, "true", True, {}, [], 5.5]).save("demo")
    print(f"STR: <{jw.string}>")
    print(dict_print(jw.items, "Items"))
    return jw.string


def test_7():
    jw = JSONWriter()
    # jw.app_state.start()
    # jw.app_state.start()
    jw.start().war([1, 2, "three", """four""", 5.5]).save("demo")
    print(f"STR: <{jw.string}>")
    print(dict_print(jw.items, "Items"))
    return jw.string


def test_8():
    jw = JSONWriter()
    jw.start().war([
        1,
        2,
        "eight",
        """nine""",
        "none",
        None,
        "true",
        True,
        {
            "first": "1st",
            "second": 2,
            "third": 3.5,
            "fourth": False,
            "nested_dict": {
                1: "one",
                2: "two",
                3: "three"
            },
            "nested_list": [
                1,
                "one",
                2,
                "two",
                3,
                "three"
            ]
        },
        [
            16,
            17,
            18,
            19,
            10,
            False,
            "False",
            8.5,
            None,
            "none",
            []
        ],
        5.5]
    ).save("demo")
    print(f"STR: <{jw.string}>")
    print(dict_print(jw.items, "Items"))
    print(f"size: {jw.size()}")
    return jw.string


def test_9():
    jw = JSONWriter()
    jw.start().war([
        1,
        2,
        "eight",
        """nine""",
        "none",
        None,
        "true",
        True,
        {
            "first": "1st",
            "second": 2,
            "third": 3.5,
            "fourth": False,
            "nested_dict": {
                1: "one",
                2: "two",
                3: "three"
            },
            "nested_list": [
                1,
                "one",
                2,
                "two",
                3,
                "three"
            ]
        },
        [
            16,
            17,
            18,
            19,
            10,
            False,
            "False",
            8.5,
            None,
            "none",
            []
        ],
        5.5]
    ).save("demo")
    print(f"STR: <{jw.string}>")
    print(dict_print(jw.items, "Items"))
    print(f"size: {jw.size()}")
    return jw.string


def test_10():
    jw = JSONWriter()
    jw.start()
    jw.wel("hello", new_arr=True)
    jw.save("demo")
    print(f"STR: <{jw.string}>")
    print(dict_print(jw.items, "Items"))
    print(f"size: {jw.size()}")
    return jw.string


def test_11():
    jw = JSONWriter()
    jw.start()
    jw.ooj()
    jw.wakv("key1", "Value1", "key2", "Value2")  # passing multiple keys + values
    jw.wakv(["key3", "Value3", "key4", "Value4"])  # passing list of multiple keys + values
    # jw.wakv({"key5": "Value5", "key6": "Value6"})  # passing dict of multiple keys + values
    # jw.wakv(["5", "Value5", "6", "Value6"], ["a", "b"])  # multiple lists of multiple keys + values
    # jw.wakv({"key5": "Value5", "key6": "Value6"}, ["a", "b"])  # ensure this doesnt work
    jw.coj()
    # jw.oar()
    # jw.wel(1)
    # jw.wel(2)
    # jw.car()
    jw.stop()
    jw.save("demo")
    print(f"STR: <{jw.string}>")
    print(dict_print(jw.items, "Items"))
    return jw.string


if __name__ == "__main__":

    def valid_json(test_fn):
        string = test_fn()
        try:
            json.loads(string)
            return True
        except json.JSONDecodeError:
            return False

    TS = TestSuite(valid_json)
    # TS.add_test("test1", [[test_1], True])
    # TS.add_test("test2", [[test_2], True])
    # TS.add_test("test3", [[test_3], True])
    # TS.add_test("test4", [[test_4], True])
    # TS.add_test("test5", [[test_5], True])
    # TS.add_test("test6", [[test_6], True])
    # TS.add_test("test7", [[test_7], True])
    # TS.add_test("test8", [[test_8], True])
    # TS.add_test("test9", [[test_9], True])
    # TS.add_test("test10", [[test_10], True])
    TS.add_test("test11", [[test_11], True])
    TS.execute_log()

# from utility import *
#
# """
# 	General JSON Writer class
# 	Version...............1.4
# 	Date...........2022-04-22
# 	Author.......Avery Briggs
# """
#
#
# class JSONWriter:
#
#     def __init__(self, output_file=None):
#         self.tab = "    "
#         self.output_file = output_file
#         self.tab_depth = 0
#         self._string = ""
#         self.started = False, None, False  # has started, writing object, has stopped
#         self.items = {}
#
#     def get_string(self):
#         return self._string
#
#     def set_string(self, value):
#         if not self.started[0]:
#             raise ValueError(
#                 "\n\tCannot begin writing to this json file because it has not been \'started\' yet.\n\tYou must call \'start()\' before values can be written.")
#         self._string = value
#
#     def del_string(self):
#         del self._string
#
#     def start(self, obj=True):
#         self.started = True, obj, False
#         if obj:
#             self.ooj(use_tab=False)
#         else:
#             self.oar(use_tab=False)
#
#     def stop(self):
#         if not self.started[0]:
#             raise ValueError("Cannot stop, writing has not started yet")
#         if self.started[1]:
#             self.coj(next=False)
#         else:
#             self.car(next=False)
#         self.started = *self.started[:2], True
#
#     def reset(self):
#         self.tab_depth = 0
#         self.string = ""
#         self.started = False, None, False
#
#     def save(self, file_name=None):
#         if not self.started[0]:
#             raise ValueError("\n\tCannot save this json file because nothing has been written to it.\n\tYou must call \'start()\' and \'stop()\' to enable writing and saving.")
#         elif not self.started[2]:
#             # allow saving without calling close first. This will do it for you.
#             self.stop()
#         if self.output_file is not None or file_name is not None:
#             fn = self.output_file if self.output_file is not None else file_name
#             if "." not in fn:
#                 fn = fn + ".json"
#             try:
#                 with open(fn, "w") as f:
#                     f.write(self.string)
#             except FileNotFoundError:
#                 raise FileNotFoundError("File not Found error")
#         else:
#             raise FileExistsError("Cannot create a file without a name.")
#
#     def tdp(self, depth=None, write=True):
#         # s = self.tab_depth * "\t"
#         s = (self.tab_depth if depth is None else depth) * self.tab
#         print(f"A: <{self.string}>")
#         print(f"TDP s: <{s}>, td: {(self.tab_depth if depth is None else depth)}")
#         if write:
#             self.string += s
#         print(f"B: <{self.string}>")
#         return s
#
#     def ooj(self, use_tab=True):
#         self.tab_depth += 1
#         if self.tab_depth not in self.items:
#             self.items.update({self.tab_depth: {}})
#             x = ""
#         else:
#             x = ",\n"
#         # s = ((self.tab_depth - 1) * "\t" if use_tab else "") + "{\n"
#         s = ((self.tab_depth - 1) * self.tab if use_tab else "") + x + "{\n"
#         self.string += s
#         return s
#
#     def coj(self, next=False):
#         self.tab_depth -= 1
#         # s = "\n" + max(0, self.tab_depth) * "\t" + "}" + ("," if next else "")
#         s = "\n" + max(0, self.tab_depth) * self.tab + "}" + ("," if next else "")
#         self.string += s
#         return s
#
#     def oar(self, use_tab=True):
#         self.tab_depth += 1
#         if self.tab_depth not in self.items:
#             self.items.update({self.tab_depth: {}})
#         # s = ((self.tab_depth - 1) * "\t" if use_tab else "") + "{\n"
#         s = ((self.tab_depth - 1) * self.tab if use_tab else "") + "[\n"
#         self.string += s
#         return s
#
#     def car(self, next=False):
#         self.tab_depth -= 1
#         # s = "\n" + max(0, self.tab_depth) * "\t" + "}" + ("," if next else "")
#         s = "\n" + max(0, self.tab_depth) * self.tab + "]" + ("," if next else "")
#         self.string += s
#         return s
#
#     def okey(self, k_name, new_line=True):
#         s = ("\n" if new_line else "") + self.tdp(write=False) + f"\"{k_name}\": " + self.ooj(use_tab=False)
#         self.string += s
#         return s
#
#     def ckey(self, next=False):
#         s = self.tdp() + self.coj(next=next)
#         self.string += s
#         return s
#
#     def wkv(self, k, v, next=False, new_line=False):
#         """Remember to properly pass 'next' and 'new_line' params to ensure valid JSON"""
#         print(f"TD: {self.tab_depth}")
#         x = "\"" if isinstance(v, str) else ""
#         if v == "null":
#             x = ""
#         if isinstance(v, bool):
#             if v:
#                 v = "true"
#             else:
#                 v = "false"
#         print("\'f\': <{}>".format(k))
#         s = "{t}\"{k}\": {x}{v}{x}{n}{l}".format(t=self.tdp(depth=1, write=False), k=k, v=v, n=',' if next else '',
#                                                  l='\n' if new_line else '', x=x)
#         print("CALC S: <{}>".format(s))
#         # s = "{t}\"{k}\": {x}{v}{x}{n}{l}".format(t="@", k=k, v=v, n=',' if next else '', l='\n' if new_line else '', x=x)
#         add_new = False
#         add_tab = False
#         # asdg = self.string[-1] == '\t'
#         # print(f"EW: <{self.string[-1]}> ==NL: {(asdg)} ==T: {asdg}")
#         add_new = True
#         # if self.string.endswith("\n"):
#         if self.string.endswith(self.tab):
#             add_new = True
#             add_tab = True
#         adjust = not bool(self.string.strip().endswith(",")) and bool(self.items[self.tab_depth])
#         print("adjusted: {}, an: {}, at: {}".format(adjust, add_new, add_tab))
#         if adjust:
#             self.string = self.string.strip() + ","
#         if add_new and adjust:
#             self.string = self.string.strip() + "\n"
#         if add_tab and adjust:
#             self.string += self.tab
#         self.string += s
#         self.record(k, v)
#         # self.items[self.tab_depth].append((k, v))
#         return s
#
#     def wakv(self, k, *v):
#         # """Remember to properly pass 'next' and 'new_line' params to ensure valid JSON"""
#         print(f"k: {k} <{type(k)}>, v: {v} <{type(v)}>")
#         if isinstance(k, dict):
#             if len(v) != 0:
#                 raise ValueError("Parameter \'v\' must be omitted when passing a dict for parameter \'k\'.")
#             else:
#                 r = []
#                 for kk, kv in k.items():
#                     r.append(kk)
#                     r.append(kv)
#                 k = r
#         elif not isinstance(k, list) and not isinstance(k, tuple):
#             k = [k]
#         v = list(v)
#         lst = k + v
#         evens = [v for i, v in enumerate(lst) if i % 2 == 0]
#         odds = [v for i, v in enumerate(lst) if i % 2 == 1]
#         l = len(lst) // 2
#         print(f"l: {l}")
#         s = ""
#         for i, even_odd in enumerate(zip(evens, odds)):
#             even, odd = even_odd
#             s += self.wkv(even, odd, next=i != (l - 1), new_line=i != (l - 1))
#             print(f"i != (l - 1): i: {i}, l: {l}, r: {i != (l - 1)}, s: <{s}>")
#         return s
#         # x = "\"" if isinstance(v, str) else ""
#         # if v == "null":
#         #     x = ""
#         # s = "{t}\"{k}\": {x}{v}{x}{n}{l}".format(t=self.tdp(), k=k, v=v, n=',' if next else '', l='\n' if new_line else '', x=x)
#         # self.string += s
#         # return s
#
#     def wel(self, el, next=False, new_line=True):
#         s = "{t}{x}{e}{x}{c}{n}".format(t=self.tdp(depth=1), e=el, c=", " if next else "", n="\n" if new_line else "",
#                                         x="\"" if isinstance(el, str) else "")
#         self.string += s
#         return s
#
#     def war(self, a):
#         if isinstance(a, tuple):
#             a = list(a)
#         if not isinstance(a, list):
#             raise TypeError("Param \'a\' must be either a list or a tuple, got: \'{}\'".format(type(a)))
#         self.oar()
#         s = ""
#         for i, el in enumerate(a):
#             x = i != len(a) - 1
#             s += self.wel(el, next=x, new_line=x)
#         self.car()
#         # s = str()
#         # self.string += s
#         return s
#
#     def woj(self, o):
#         pass
#
#     def record(self, k, v, depth=None):
#         dictionary = self.tab_depth if depth is None else depth
#         if k in self.items[dictionary]:
#             raise KeyError("This k=\'{}\' cannot be duplicated within the same nesting.")
#         self.items[dictionary][k] = v
#
#     string = property(get_string, set_string, del_string)
#
#
# def test_1():
#     jw = JSONWriter()
#     jw.start()
#     jw.stop()
#     jw.save("demo")
#     print(f"STR: <{jw.string}>")
#     print(f"STR: <" + jw.string + ">")
#
#
# def test_2():
#     jw = JSONWriter()
#     jw.start()
#     jw.wkv("key1", "value1")
#     jw.stop()
#     jw.save("demo")
#     print(f"STR: <{jw.string}>")
#
#
# def test_3():
#     jw = JSONWriter()
#     jw.start()
#     jw.wakv("key1", "Value1", "key2", "Value2")  # passing multiple keys + values
#     jw.wakv(["key3", "Value3", "key4", "Value4"])  # passing list of multiple keys + values
#     # jw.wakv({"key5": "Value5", "key6": "Value6"})  # passing dict of multiple keys + values
#     # jw.wakv(["5", "Value5", "6", "Value6"], ["a", "b"])  # multiple lists of multiple keys + values
#     # jw.wakv({"key5": "Value5", "key6": "Value6"}, ["a", "b"])  # ensure this doesnt work
#     jw.stop()
#     jw.save("demo")
#     print(f"STR: <{jw.string}>")
#     print(dict_print(jw.items, "Items"))
#
#
# def test_4():
#     jw = JSONWriter()
#     jw.start()
#     jw.wakv("key1", "Value1", "key2", "Value2")  # passing multiple keys + values
#     jw.wakv(["key3", False, "key4", True])  # passing list of multiple keys + values
#     jw.wakv(["key5", 18, "key6", 19.2])  # passing list of multiple keys + values
#     # jw.okey("List")
#     jw.ckey()
#     # jw.wakv({"key5": "Value5", "key6": "Value6"})  # passing dict of multiple keys + values
#     # jw.wakv(["5", "Value5", "6", "Value6"], ["a", "b"])  # multiple lists of multiple keys + values
#     # jw.wakv({"key5": "Value5", "key6": "Value6"}, ["a", "b"])  # ensure this doesnt work
#     jw.stop()
#     jw.save("demo")
#     print(f"STR: <{jw.string}>")
#     print(dict_print(jw.items, "Items"))
#
#
# def test_5():
#     jw = JSONWriter()
#     jw.start(obj=False)
#     jw.war([1, 2, "three", """four""", 5.5])
#     # jw.stop()
#     jw.save("demo")
#     print(f"STR: <{jw.string}>")
#     print(dict_print(jw.items, "Items"))
#
#
# if __name__ == "__main__":
#     # test_1()
#     # test_2()
#     # test_3()
#     test_4()
#     # test_5()
