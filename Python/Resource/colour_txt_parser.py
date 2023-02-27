from colour_utility import *
from utility import print_by_line

if __name__ == '__main__':

    # print(f"{COLOURS.keys()}")

    with open("colours.txt", "r") as f:
        text = f.read()
        lines = text.split("\n")

        names = []

        for line in lines:
            hex_code, name = line.split("\t")
            name = name.upper().replace('(W3C)', '').strip().replace(' ', '_')
            if name not in COLOURS:
                c = Colour(hex_code)
                print(f"{name} = {c.rgb_code}")
                names.append(name)
            # else:
            #     print(f"Skipped {name}")

        print_by_line(names)
        print(",\n".join([f"\"{n}\"" for n in names]))
