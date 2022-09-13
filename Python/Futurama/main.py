import dataclasses
from dataclasses import dataclass


# https://stackoverflow.com/questions/61740748/python-dataclass-generate-hash-and-exclude-unsafe-fields
@dataclass(unsafe_hash=True)
class Person:
    name: str = dataclasses.field(hash=True)
    switches: set[object] = dataclasses.field(default_factory=set, compare=False, hash=False)

    def can_switch(self, person):
        return person not in self.switches

    def has_switched(self, person):
        return person in self.switches

    def switch(self, person):
        self.switches.add(person)

    def __copy__(self):
        p = Person(self.name)
        for sw in self.switches:
            p.switches.add(sw)
        return p

    def __repr__(self):
        return f"<Person {self.name}>"


@dataclass(unsafe_hash=True)
class Graph:
    names: list[str] = dataclasses.field(hash=False)
    people: dict[str: Person] = dataclasses.field(default_factory=dict, hash=False)
    switches: tuple[tuple[str, str]] = dataclasses.field(default_factory=tuple, hash=True)
    switch_board: dict[str: list[str]] = dataclasses.field(default_factory=dict, hash=False)
    involved: set[str] = dataclasses.field(default_factory=set, hash=False)

    def init(self):
        self.people = {n: {"obj": Person(n)} for n in names}
        self.switch_board = {p: [p] for p, p_obj in self.people.items()}
        print(f"{self.switch_board=}")
        return self

    def switch(self, from_person: str, to_person: str):
        assert from_person in self.people, f"Error to_person '{from_person}' not recognized in this graph."
        assert to_person in self.people, f"Error to_person '{to_person}' not recognized in this graph."
        if from_person not in self.involved:
            self.involved.add(from_person)
        if to_person not in self.involved:
            self.involved.add(to_person)
        from_person = self.people[from_person]["obj"]
        to_person = self.people[to_person]["obj"]
        if from_person.can_switch(to_person) and to_person.can_switch(from_person):
            from_person.switch(to_person)
            to_person.switch(from_person)
            self.switches = (*self.switches, (from_person.name, to_person.name))
            off = -1
            for person, person_obj in self.people.items():
                p_obj = person_obj["obj"]
                next = self.switch_board[person][-1]
                if p_obj == from_person:
                    next = self.switch_board[to_person.name][off]
                    print(f"\tEQUAL: {person=} == {from_person=}, {p_obj=}, {to_person=}, {next=}")
                    off -= 1
                if p_obj == to_person:
                    next = self.switch_board[from_person.name][off]
                    print(f"\tEQUAL: {person=} == {to_person=}, {p_obj=}, {from_person=}, {next=}")
                    off -= 1
                else:
                    print(f"NOT EQUAL: {person=}, {p_obj=}, {from_person=}, {to_person=}, {next=}")
                self.switch_board[person].append(next)
        ml = max([len(str(name)) for name in self.switch_board]) + 2
        sb = "\n\nbody |" + "|".join([f"{name.center(ml, ' ')}" for name in self.switch_board]) + "|"
        for i in range(len(self.switches)):
            sb += f"\n" + f"{i + 1}".rjust(5) + "|"
            for person, dat in self.switch_board.items():
                sb += f"{dat[i+1]}".rjust(ml) + "|"
        print(f"SWITCH\n\n[\nself.switch_board:{sb}\n]")

        ntsb = self.needs_to_swap_back()
        for person in ntsb:
            print(f"{self.switch_board[person][-1]} is in {person}'s body")

    def needs_to_swap_back(self):
        need_to_switch = []
        for person, lst in self.switch_board.items():
            if person != lst[-1]:
                need_to_switch.append(person)
        return need_to_switch

    def who_is_where(self):
        # body: mind
        return {

        }

    def show_switches(self):
        print(f"\n\nSwitches:")
        for name, person in self.people.items():
            p_obj = person["obj"]
            print(f"{name=}, {p_obj.switches=}")

    def __eq__(self, other):
        if not isinstance(other, Graph):
            raise TypeError(f"Comparison type must be a Graph, got {other}")
        a = self.needs_to_swap_back() == other.needs_to_swap_back()
        print(f"{a=}, {self.needs_to_swap_back()=}, {other.needs_to_swap_back()=}")
        b = False
        if a:
            b = self.involved == other.involved
            print(f"{b=}, {self.involved=}, {other.involved=}")
        return a and b

    def __copy__(self):
        g = Graph(self.names).init()

        new_switches = tuple()
        for sw in self.switches:
            a, b = sw
            new_switches = (*new_switches, (a, b))

        new_involved = set()
        for p in self.involved:
            new_involved.add(p)

        new_switch_board = dict()
        for p, lst in self.switch_board.items():
            for i, val, in enumerate(lst):
                if p not in new_switch_board:
                    new_switch_board[p] = []
                new_switch_board[p].append(val)

        g.switches = new_switches
        g.involved = new_involved
        g.switch_board = new_switch_board

        return g

    def gen_solution_tree(self, only_involved=True):
        ntsb = self.needs_to_swap_back()
        people = set(self.people)
        involved = self.involved
        result = []
        if only_involved:
            people = involved
        if ntsb:
            rev_pairs = set()
            # TODO this will be made into a helper function to calculate all possible swaps of a given graph.
            for person_a in ntsb:
                for person_b in people:
                    if person_a != person_b:
                        pa_obj = self.people[person_a]["obj"]
                        pb_obj = self.people[person_b]["obj"]
                        swap = (person_a, person_b)
                        swap_key = f"{person_a} -> {person_b}"
                        if pa_obj.can_switch(pb_obj) and swap_key not in rev_pairs:
                            result.append(swap)
                            rev_pairs.add(swap_key)
                            rev_pairs.add(f"{person_b} -> {person_a}")
        return result


def bfs(graph, start_vertex, target_value):
    path = [start_vertex]
    vertex_and_path = [start_vertex, path]
    bfs_queue = [vertex_and_path]
    visited = set()

    while bfs_queue:
        current_vertex, path = bfs_queue.pop(0)
        visited.add(current_vertex)

        for neighbor in graph[current_vertex]:
            if neighbor not in visited:
                if neighbor == target_value:
                    return path + [neighbor]

                else:
                    bfs_queue.append([neighbor, path + [neighbor]])


if __name__ == "__main__":
    print(f"hey")
    names = [
        fry := "Fry",
        leela := "Leela",
        zoid := "Zoidberg",
        prof := "Professor",
        amy := "Amy",
        must := "Mustache",
        afro := "Afro",
        bucket := "Mop Bucket",
        king := "King",
        bender := "Bender",
        hermes := "Hermes"
    ]

    graph = Graph(names).init()
    graph.switch(amy, prof)
    graph.switch(bender, amy)
    graph.switch(leela, prof)
    graph.switch(bucket, amy)
    graph.switch(fry, zoid)
    graph.switch(king, bucket)
    graph.switch(hermes, leela)

    # solution
    graph.switch(fry, must)
    graph.switch(zoid, afro)
    graph.switch(must, zoid)
    graph.switch(afro, fry)
    graph.switch(prof, must)
    graph.switch(bucket, afro)
    graph.switch(must, leela)
    graph.switch(afro, king)
    graph.switch(hermes, must)
    graph.switch(bender, afro)
    graph.switch(must, amy)
    graph.switch(afro, prof)
    graph.switch(must, bucket)

    print(f"{graph.needs_to_swap_back()=}")

    # graph2 = Graph(names).init()
    # graph2.switch(amy, prof)
    # graph2.switch(bender, amy)
    # graph2.switch(leela, prof)
    #
    # graph3 = Graph(names).init()
    # graph3.switch(amy, prof)
    # graph3.switch(bender, amy)
    # # graph3.switch(leela, prof)
    #
    # graph4 = graph.__copy__()
    #
    # graph.show_switches()
    # print(f"{graph=}")
    # print(f"{graph2=}")
    # print(f"{graph3=}")
    # print(f"{graph4=}")
    # print(f"{graph.needs_to_swap_back()=}")
    # print(f"{graph.gen_solution_tree()=}")
    # print(f"{hash(graph)=}")
    # print(f"{hash(graph2)=}")
    # print(f"{hash(graph3)=}")
    # print(f"{hash(graph4)=}")
    # print(f"{hash(graph) == hash(graph2)=}")
    # print(f"{hash(graph) == hash(graph3)=}")
    # print(f"{hash(graph2) == hash(graph3)=}")
    # print(f"{graph == graph3=}")
    # print(f"{graph == graph4=}")
