class Person :
    
    def __init__(self, name, nickname=None, family=None) :
        self.name = name
        self.nickname = nickname
        
    def format_name(self) :
        names = self.name.split(" ")
        if self.nickname is None :
            return self.name
        else :
            return " ".join([self.nickname] + [names[i] for i in range(1, len(names))])
        
    def __repr__(self) :
        return self.format_name()
        # names = format_name()
        # if 
        # if self != self.to_buy_for :
            # return self.name + " got " + str(self.to_buy_for)
        
    def got(self, person) :
        self.to_buy_for = person
        
mum = Person("Monica Dugan", "Mum")
carol = Person("Carol Pelkey")
alden = Person("Alden Pelkey")
kyle = Person("Kyle Pelkey")
tiffany = Person("Tiffany Pelkey")
cary_ann = Person("Cary Ann Pelkey")
florence = Person("Florence Dugan")
susan = Person("Susan Briggs")
gus = Person("Augustine Briggs", "Gus")
avery = Person("Avery Briggs")
kristen = Person("Kristen Briggs")
emily = Person("Emily Briggs")
hayley = Person("Hayley Briggs")
louise = Person("Louise Bettle")
fred = Person("Fred Bettle")
alex = Person("Alex Bettle")
justin = Person("Justin Bettle")
olivia = Person("Olivia Bettle")
nathan = Person("Nathan Bettle")
barbara = Person("Barbara Dugan", "Barb")
brian = Person("Brian Dugan")
kelly = Person("Kelly Dugan")
lauryn = Person("Lauryn Dugan")
steve = Person("Steve Dugan")
dan = Person("Danny Dugan", "Dan")
sarah = Person("Sarah Dugan")
jacob = Person("Jacob Dugan")
annie = Person("Annie Dugan")
lorraine = Person("Lorraine Pickard")
clarence = Person("Clarence Pickard")
sabrina = Person("Sabrina Pickard")

        
mum.got(fred)
carol.got(olivia)
alden.got(kelly)
kyle.got(gus)
tiffany.got(mum)
cary_ann.got(jacob)
florence.got(steve)
susan.got(cary_ann)
gus.got(clarence)
avery.got(justin)
kristen.got(tiffany)
emily.got(sarah)
hayley.got(annie)
louise.got(emily)
fred.got(avery)
alex.got(carol)
justin.got(barbara)
olivia.got(lauryn)
nathan.got(dan)
barbara.got(kristen)
brian.got(susan)
kelly.got(nathan)
lauryn.got(florence)
steve.got(lorraine)
dan.got(sabrina)
sarah.got(alden)
jacob.got(kyle)
annie.got(brian)
lorraine.got(louise)
clarence.got(hayley)
sabrina.got(alex)

do_it = True
to_cover = [mum,
            carol,
            alden,
            kyle,
            tiffany,
            cary_ann,
            florence,
            susan,
            gus,
            avery,
            kristen,
            emily,
            hayley,
            louise,
            fred,
            alex,
            justin,
            olivia,
            nathan,
            barbara,
            brian,
            kelly,
            lauryn,
            steve,
            dan,
            sarah,
            jacob,
            annie,
            lorraine,
            clarence,
            sabrina]
covered = []
current = mum
p = current
num_loops = 1

while True :
    print(p)
    covered.append(p)
    n_p = p.to_buy_for
    to_cover.remove(p)
    if n_p in covered :
        if len(to_cover) < 1 :
            break
        else :
            print("\n\n\tNew circle\n\n")
            p = to_cover[0]
            num_loops += 1
    else :
        p = n_p
        
# print("\n\tcovered:\n" + str(covered))
# print("\n\tto_cover:\n" + str(to_cover))
        
# print(mum)
print("\nNum loops: " + str(num_loops))
        