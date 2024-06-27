

class CA:
    def __init__(self):
        self.a = "ca_a"
        self.b = "ca_b"
        self.c = "ca_c"

class CB:

    class CC:
        def __init__(self):
            self.a = "cc_a"
            self.b = "cc_b"
            self.c = "cc_c"

            self.d = CB.a

    def __init__(self):
        self.a = "cb_a"
        self.b = "cb_b"
        self.c = "cb_c"


if __name__ == "__main__":
    ca = CA()
    cb = CB()

    print(f"{ca.__dict__=}")
    print(f"{cb.__dict__=}")
    print(f"{cb.CC.__dict__=}")
    cc = CB.CC()
    print(f"{cc.__dict__=}")
    print(f"{.a=}")
