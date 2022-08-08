

#	Class outlining a Game-State-Machine (GSM).
#	Version............1.4
#	Date........2022-08-03
#	Author....Avery Briggs


class GSM:

    def __init__(self, options, name=None, idx=None, max_cycles=None, allow_recycle=True):
        """Game State Machine. Simulates state switches for an object.
        Required:   options         -   list of states.
        Optional:   name            -   GSM name
                    idx             -   starting index for a state
                    max_cycles      -   maximum number of cycles allowed
                    allow_recycle   -   use this to allow for only a single cycle(Think generators)"""
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
        self.prev = self.calc_prev()

        self.max_cycles = -1
        if max_cycles is not None:
            if isinstance(max_cycles, bool) and max_cycles:
                # use this for 1 iteration
                self.max_cycles = 1
            elif isinstance(max_cycles, int):
                self.max_cycles = max_cycles

        self.callbacks = {}
        self.allow_recycle = allow_recycle

    def __iter__(self):
        """Generator of upcoming states. ONLY 1 CYCLE"""
        # return self.options[:self.idx] + self.options[self.idx:]
        for op in self.queue():
            yield op

    def calc_prev(self, idx=None):
        """Grab the index immediately before the given index, defaults to current index."""
        idx = self.idx if idx is None else idx
        # print(f"idx: {idx}, new: {(idx - 1) % len(self)}, t: {type(idx)}")
        return (idx - 1) % len(self)

    def __next__(self):
        """Call this like a generator would. Simulates 'walking' states and checks against max_cycles."""
        a = (self.idx - 1) % len(self)
        b = (self.prev + 0) % len(self)
        # print(f"name={self.name}, idx: <{self.idx}>, prev: <{self.prev}>, a={a}, b={b}")
        if a != b:
            # if this is true, then the state index was altered illegally.
            raise ValueError("STOP!!" + "\n" + str(self) + "\n" + "The state index was altered illegally.")
        self.idx += 1
        if self.idx >= len(self):
            self.cycles += 1
            self.restart()
            if not self.can_recycle():
                raise StopIteration(f"Error max cycles have been reached for this GSM object. cycles={self.cycles}")
            # if self.max_cycles >= 0:
            #     if self.cycles >= self.max_cycles:
            #         raise StopIteration(f"Error max cycles have been reached for this GSM object. cycles={self.cycles}")
        new_state = self.state()
        self.callback(new_state)
        # print(f"new_state: <{new_state}>, idx: <{self.idx}>, prev: <{self.prev}>")
        self.prev = self.calc_prev()  # call last to act as a check.
        return new_state

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
        """Viewing options cyclically, return the state opposite to the current. Use round_up to handle odd length state lists"""
        off = 0 if not round_up else len(self) % 2
        return self.options[(self.idx + ((len(self) // 2) + off)) % len(self)]

    def state(self, idx=None):
        """Return the state at a given index. If none given, defaults to own index."""
        return self.options[self.idx] if idx is None else self.options[idx]

    def peek(self, n_ahead=1):
        """Peek ahead to the nth state. Default next state."""
        return self.state((self.idx + n_ahead) % len(self))

    def set_state(self, idx):
        if idx in self.options:
            self.idx = self.options.index(idx)
            # print(f"UPDATE: {self.idx}")
            self.prev = self.calc_prev()
            print(self)
            # print(f"idf: {self.idx}, prev: {self.prev}")
            return
        else:
            if isinstance(idx, int) and not isinstance(idx, bool):
                if -1 < idx < len(self):
                    self.idx = idx
                    self.prev = self.calc_prev()
                    return
        raise ValueError(f"Error param idx is not recognized as a state or an index. idx={idx}, type={type(idx)}")
        # if isinstance(idx, int):
        #     # TODO this will cause a problem for keys that are also whole numbers. instead of by value this does by position
        #     if -1 < idx < len(self):
        #         self.idx = idx
        #         self.prev = self.calc_prev()
        #     else:
        #         raise ValueError(f"Error cannot set the state to index={idx}. Index out of range.")
        # else:
        #     if idx not in self.options:
        #         raise KeyError(f"Error key '{idx}' not a valid state for this machine.")
        #     state = idx
        #     self.idx = self.options.index(state)
        #     print(f"idx: {idx}, s.idx: {self.idx}")
        #     self.prev = self.calc_prev(self.idx)

    def add_state(self, state, idx=None):
        """Add a state. By default, appended, but can be altered using idx param."""
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
        self.prev = self.calc_prev()

    def remove_state(self, state):
        """Remove a state. Beware ValueError"""
        self.unbind_callback(state)
        if isinstance(self.options, list):
            self.options.remove(state)
        else:
            temp = list(self.options)
            temp.remove(state)
            self.options = tuple(temp)
        self.prev = self.calc_prev()

    def bind_callback(self, func, *args, state=None, all_states=False, **kwargs):
        """Add a callback to a given state """
        # print(f"func: {func}")
        # print(f"args: {args}")
        # print(f"kwargs: {kwargs}")
        state = state if state is not None else self.state()
        if state not in self.options:
            raise KeyError(f"Error unable to bind callback for state '{state}' as it is not a valid state of this GSM.")
        self.callbacks[state] = (func, args, kwargs)
        if all_states:
            for state_ in self.options:
                if state_ != state:
                    self.callbacks[state_] = (func, args, kwargs)

    def unbind_callback(self, state=None):
        """Unbind a callback for a given state, defaults to current state."""
        state = state if state is not None else self.state()
        if state not in self.options:
            raise KeyError(f"Error unable to unbind callback for state '{state}' as it is not a valid state of this GSM.")
        if state not in self.callbacks:
            print(f"No callbacks have been bound to state '{state}' yet.")
            return
        del self.callbacks[state]

    def callback(self, state=None):
        """Call the function associated with a given state, defaults to current state."""
        state = state if state is not None else self.state()
        if state in self.callbacks:
            func, args, kwargs = self.callbacks[state]
            func(*args, **kwargs)

    def restart(self):
        """Restart from idx=0, same cycle."""
        self.idx = 0

    def reset(self):
        """Reset from index=0 and cycle=0."""
        if not self.allow_recycle:
            raise StopIteration("Error this GSM is not allowed to recycle based on init param 'allow_recycle'.")
        self.restart()
        self.cycles = 0

    def can_recycle(self):
        """Can this GSM cycle again or will it raise a StopIteration."""
        return self.allow_recycle and (self.max_cycles < 0 or self.cycles < self.max_cycles - 1)

    def __repr__(self):
        a = f" name={self.name}," if self.name is not None else ""
        b = f", cycle_num/max_cycles={self.cycles} / {self.max_cycles}" if self.max_cycles >= 0 else ""
        r = (self.cycles * len(self)) + self.idx
        f = (self.max_cycles * len(self)) if len(self) != 0 and self.max_cycles != 0 else 1
        p = ("%.2f" % ((100 * r) / f)) + " %"
        c = f", #state_idx/ttl_states={r} / {f} = {p}" if b else ""
        return f"<GSM{a} state={self.state()}, options={self.queue()}{b}{c}>"


class BooleanGSM(GSM):

    # Binary switch

    def __init__(self, name=None, idx=None, max_cycles=None, t_first=True):
        super().__init__(options=[True, False] if t_first else [False, True], name=name, idx=idx, max_cycles=max_cycles)


class YesNoCancelGSM(GSM):

    # Triple state switch

    def __init__(self, name=None, idx=None, max_cycles=None):
        super().__init__(options=["Yes", "No", "Cancel"], name=name, idx=idx, max_cycles=max_cycles)


if __name__ == '__main__':

    def print_hello1():
        print("Hello World!")


    def print_hello2(arg1, arg2, arg3=4):
        print(f"Hello World! arg1={arg1} arg2={arg2} arg3={arg3}")


    # phone_number_guess.main()
    # orbiting_date_picker.main()
    gsma = GSM(options=list(range(100)), name="GSMA")
    gsm1 = GSM(options=list(range(100)), name="GSM1")
    gsm2 = BooleanGSM(name="GSM2")
    gsm3 = YesNoCancelGSM(name="GSM3")
    gsm4 = YesNoCancelGSM(max_cycles=True, name="GSM4")

    to_print = [
        # gsm3.opposite(round_up=True),
        gsm2.add_state("There"),
        gsm2.set_state("There")
        # gsm2.__next__(),
        # gsm4.__next__(),
        # gsm4.__next__(),
        # gsm4.can_recycle(),
        # # gsm2.bind_callback(print_hello1),
        # gsm2.__next__(),
        # # gsm2.bind_callback(print_hello2, 1, 4, arg3=5),
        # # gsm2.unbind_callback(state=True),
        # gsm2.bind_callback(print_hello2, -1, -4, arg3=-5, state=True),
        # gsm2.__next__(),
        # gsm2.__next__(),
        # gsm2.__next__(),
        # gsm2.__next__(),
        # gsm2.__next__(),
        # gsm2.__next__(),
        # gsm2.__next__(),
        # gsm2.remove_state(state=True),
        # gsm2.__next__(),
        # gsm2.__next__(),
        # gsm2.__next__(),
        # gsm2.__next__(),
        # gsm2.__next__(),
        # gsm2.__next__(),
        # gsm1,
        # gsm2,
        # gsm3,
        # gsm4,
        # list(gsm1),
        # list(gsm2),
        # list(gsm3),
        # list(gsm4)
        # # gsm4.__next__()
    ]

    for i, test in enumerate(to_print):
        print(f"i: {i}, test=<{test}>")
