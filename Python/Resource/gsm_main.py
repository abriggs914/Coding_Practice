import phone_number_guess
# import orbiting_date_picker
from utility import *


# gsm_showing_dae_picker = (True, False), 0


#	Class outlining a Game-State-Machine (GSM).
#	Version............1.1
#	Date........2022-06-30
#	Author....Avery Briggs
from test_suite import TestSuite


class GSM:

    def __init__(self, options, name=None, idx=None, max_cycles=None):
        """Game State Machine. Simulates app_state switches for an object.
        Required:   options     -   list of states.
        Optional:   name        -   GSM name
                    idx         -   starting index for a app_state
                    max_cycles  -   maximum number of cycles allowed. (Think generators)"""
        if idx is None:
            idx = 0
        if not isinstance(idx, int) or (0 < idx < len(options)):
            raise TypeError("Error param 'idx' needs to be an integer corresponding to a list index.")

        if not isinstance(options, list) and not isinstance(options, tuple):
            raise TypeError("Error param 'options' needs to be an ordered iterable object. (supported: list, tuple)")
        if len(options) == 0:
            raise ValueError("Error param 'options' needs to have at least 1 element.")
        if max_cycles == 0:
            raise ValueError("Error you can not create a GSM that does not have at least 1 cycle")

        self.name = name
        self.idx = idx
        self.options = options
        self.cycles = 0

        self.max_cycles = -1
        if max_cycles is not None:
            if isinstance(max_cycles, bool) and max_cycles:
                # use this for 1 iteration
                self.max_cycles = 1
            elif isinstance(max_cycles, int):
                self.max_cycles = max_cycles

    def __iter__(self):
        """Generator of upcoming states. ONLY 1 CYCLE"""
        # return self.options[:self.idx] + self.options[self.idx:]
        for op in self.queue():
            yield op

    def __next__(self):
        """Call this like a generator would. Simulates 'walking' states and checks against max_cycles."""
        self.idx += 1
        if self.idx >= len(self):
            self.cycles += 1
            self.restart()
            if not self.can_recycle():
                raise StopIteration(f"Error max cycles have been reached for this GSM object. cycles={self.cycles}")
            # if self.max_cycles >= 0:
            #     if self.cycles >= self.max_cycles:
            #         raise StopIteration(f"Error max cycles have been reached for this GSM object. cycles={self.cycles}")
        return self.state()

    def __len__(self):
        """Return length of states list"""
        return len(self.options)

    def queue(self):
        """List of states in pending order, beginning with the current."""
        rest = self.options[self.idx:]
        if self.can_recycle():
            rest += self.options[:self.idx]
        return rest

    def opposite(self, round_up=False):
        """Viewing options cyclically, return the app_state opposite to the current. Use round_up to handle odd length app_state lists"""
        off = 0 if not round_up else len(self) % 2
        return self.options[(self.idx + ((len(self) // 2) + off)) % len(self)]

    def state(self, idx=None):
        """Return the app_state at a given index. If none given, defaults to own index."""
        return self.options[self.idx] if idx is None else self.options[idx]

    def peek(self, n_ahead=1):
        """Peek ahead to the nth app_state. Default next app_state."""
        return self.state((self.idx + n_ahead) % len(self))

    def add_state(self, state, idx=None):
        """Add a app_state. By default, appended, but can be altered using idx param."""
        if idx is None:
            if isinstance(self.options, list):
                self.options.append(state)
            else:
                self.options = (*self.options, state)
        else:
            if isinstance(self.options, list):
                self.options.insert(idx, state)
            else:
                self.options = (*self.options[:idx], state, self.options[idx:])

    def remove_state(self, state):
        """Remove a app_state. Beware ValueError"""
        if isinstance(self.options, list):
            self.options.remove(state)
        else:
            temp = list(self.options)
            temp.remove(state)
            self.options = tuple(temp)

    def restart(self):
        """Restart from idx=0, same cycle."""
        self.idx = 0

    def reset(self):
        """Reset from index=0 and cycle=0."""
        self.restart()
        self.cycles = 0

    def can_recycle(self):
        """Can this GSM cycle again or will it raise a StopIteration."""
        return self.max_cycles < 0 or self.cycles < self.max_cycles - 1

    def __repr__(self):
        a = f" name={self.name}," if self.name is not None else ""
        b = f", cycle_num/max_cycles={self.cycles} / {self.max_cycles}" if self.max_cycles >= 0 else ""
        r = (self.cycles * len(self)) + self.idx
        f = (self.max_cycles * len(self)) if len(self) != 0 and self.max_cycles != 0 else 1
        p = ("%.2f" % ((100 * r) / f)) + " %"
        c = f", #state_idx/ttl_states={r} / {f} = {p}" if b else ""
        return f"<GSM{a} app_state={self.state()}, options={self.queue()}{b}{c}>"


class BooleanGSM(GSM):

    # Binary switch

    def __init__(self, name=None, idx=None, max_cycles=None, t_first=True):
        super().__init__(options=[True, False] if t_first else [False, True], name=name, idx=idx, max_cycles=max_cycles)


class YesNoCancelGSM(GSM):

    # Triple app_state switch

    def __init__(self, name=None, idx=None, max_cycles=None):
        super().__init__(options=["Yes", "No", "Cancel"], name=name, idx=idx, max_cycles=max_cycles)



if __name__ == '__main__':
    # phone_number_guess.main()
    # orbiting_date_picker.main()
    # gsma = GSM(options=list(range(100)), name="GSM3")
    # gsm1 = GSM(options=list(range(100)))
    # gsm2 = BooleanGSM()
    # gsm3 = YesNoCancelGSM()
    # gsm4 = YesNoCancelGSM(max_cycles=True)
    #
    # to_print = [
    #     gsm3.opposite(round_up=True),
    #     gsm2.add_state("There"),
    #     gsm2.__next__(),
    #     gsm4.__next__(),
    #     gsm4.__next__(),
    #     gsm4.can_recycle(),
    #     gsm4.__next__()
    # ]
    #
    # for i, test in enumerate(to_print):
    #     print(f"i: {i}, test=<{test}>")

    def calc_bounds(center, width, height=None):
        assert (isinstance(center, list) or isinstance(center, tuple)) and len(center) == 2 and all([isnumber(x) for x in center]), f"Error param 'center' must be a tuple or list representing center coordinates (x, y). Got: {center}"
        assert isnumber(width), f"Error param 'width' must be a number. Got: {width}"
        if height is not None:
            assert isnumber(height), f"Error param 'height' if not omitted, must be a number. Got: {height}"
        w = width / 2
        h = w if height is None else (height / 2)
        return (
            center[0] - w,
            center[1] - h,
            center[0] + w,
            center[1] + h
        )

    print(f"res: {calc_bounds((0, 0), 10)}")
    print(f"res: {calc_bounds((0, 0), 10, 20)}")

    ts = TestSuite(test_func=calc_bounds)
    # ts.set_func(calc_bounds)
    ts.add_test("test1", [[(0, 0), 10], (-5, -5, 5, 5)])
    ts.add_test("test2", [[(0, 0), 10, 20], (-5, -10, 5, 10)])
    ts.add_test("test3", [[(None, 0), 10, 20], AssertionError])
    ts.execute()
