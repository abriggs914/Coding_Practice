class Vehicle:

    def __init__(self, id_no, name, pos, colour,
                 x_vel=0,
                 y_vel=0,
                 x_acc=0,
                 y_acc=0,
                 fuel_grade=None,
                 drill=None,
                 hull=None,
                 storage=None,
                 propeller=None,
                 fuel_tank=None,
                 text_symbol="V"
                 ):
        self.id_no = id_no
        self.name = name
        self.pos = pos
        self.colour = colour
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.x_acc = x_acc
        self.y_acc = y_acc
        self.fuel_grade = fuel_grade
        self.drill = drill
        self.hull = hull
        self.storage = storage
        self.propeller = propeller
        self.fuel_tank = fuel_tank
        self.text_symbol = text_symbol