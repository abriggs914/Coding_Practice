class Vehicle:

    state_falling = "falling"
    state_hovering = "hovering"

    def __init__(self, id_no, name, rect, colour,
                 x_vel=0,
                 y_vel=0,
                 x_vel_max=None,
                 y_vel_max=None,
                 x_acc=0,
                 y_acc=0,
                 x_acc_d=None,
                 y_acc_d=None,
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
        self.rect = rect
        self.colour = colour
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.x_vel_max = x_vel_max if x_vel_max is not None else x_vel + 5
        self.y_vel_max = y_vel_max if y_vel_max is not None else y_vel + 5
        self.x_acc = x_acc
        self.y_acc = y_acc
        self.x_acc_d = x_acc_d if x_acc_d is not None else 0.95
        self.y_acc_d = y_acc_d if y_acc_d is not None else 0.95
        self.fuel_grade = fuel_grade
        self.drill = drill
        self.hull = hull
        self.storage = storage
        self.propeller = propeller
        self.fuel_tank = fuel_tank
        self.text_symbol = text_symbol

        self.state = self.state_falling

    def set_hovering(self):
        self.state = self.state_hovering

    def set_falling(self):
        self.state = self.state_falling
