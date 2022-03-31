from colour_utility import *
from utility import *
import pygame


N_OBJECTS = 0


def new_id():
    global N_OBJECTS
    N_OBJECTS += 1
    return N_OBJECTS


def pad_rect(rect, padding):
    return pygame.Rect(rect.x - padding, rect.y - padding, rect.w + (2 * padding), rect.h + (2 * padding))


class PObject:

    def __init__(
            self,
            x,
            y,
            rect=None,
            name=None,
            colour=RED,
            max_speed=15,
            x_change=0,  # initial x speed
            y_change=0,  # initial y speed
            x_acceleration=0,  # initial x acceleration
            y_acceleration=0,  # initial y acceleration
            x_acceleration_rate=1,  # rate of x acceleration
            y_acceleration_rate=1.5,  # rate of y acceleration
            x_de_acceleration_rate=0.9,  # rate of x friction
            y_de_acceleration_rate=0.9,  # rate of y friction
            x_gravity=0,
            y_gravity=0.9,
            width=20,
            height=20
    ):
        self._x = x
        self._y = y
        self._xy = x, y
        self._rect = rect
        self._width = width
        self._height = height
        self.x_change = x_change
        self.y_change = y_change
        self.x_acceleration = x_acceleration
        self.y_acceleration = y_acceleration
        self.obj_id = new_id()
        self.colour = colour
        self.name = name
        self.max_speed = max_speed
        self.x_acceleration_rate = x_acceleration_rate
        self.y_acceleration_rate = y_acceleration_rate
        self.x_de_acceleration_rate = x_de_acceleration_rate
        self.y_de_acceleration_rate = y_de_acceleration_rate
        self.x_gravity = x_gravity
        self.y_gravity = y_gravity
        self.proposed_move = None

        self.init(
            self.obj_id,
            x,
            y,
            rect=rect,
            name=name,
            colour=colour,
            max_speed=max_speed,
            x_acceleration_rate=x_acceleration_rate,  # rate of x acceleration
            y_acceleration_rate=y_acceleration_rate,  # rate of y acceleration
            x_de_acceleration_rate=x_de_acceleration_rate,  # rate of x friction
            y_de_acceleration_rate=y_de_acceleration_rate,  # rate of y friction
            x_gravity=x_gravity,
            y_gravity=y_gravity,
            width=width,
            height=height,
            proposed_move=self.proposed_move
        )

    def init(
            self,
            obj_id,
            x,
            y,
            rect=None,
            name=None,
            colour=RED,
            max_speed=15,
            x_change=0,  # inital x speed
            y_change=0,  # inital y speed
            x_acceleration=0,  # initial x acceleration
            y_acceleration=0,  # initial y acceleration
            x_acceleration_rate=1,  # rate of x acceleration
            y_acceleration_rate=1.5,  # rate of y acceleration
            x_de_acceleration_rate=0.9,  # rate of x friction
            y_de_acceleration_rate=0.9,  # rate of y friction
            x_gravity=0,
            y_gravity=0.9,
            width=20,
            height=20,
            proposed_move=None
    ):
        if rect is None:
            rect = pygame.Rect(0, 0, width, height)
            rect.center = x, y

        # ensure these match
        width, height = rect.w, rect.h

        # finally, set class attributes
        self.x = x
        self.y = y
        self.xy = x, y
        self.x_change = x_change
        self.y_change = y_change
        self.x_acceleration = x_acceleration
        self.y_acceleration = y_acceleration
        self.obj_id = obj_id
        self.rect = rect
        self.colour = colour
        self.name = name
        self.max_speed = max_speed
        self.x_acceleration_rate = x_acceleration_rate
        self.y_acceleration_rate = y_acceleration_rate
        self.x_de_acceleration_rate = x_de_acceleration_rate
        self.y_de_acceleration_rate = y_de_acceleration_rate
        self.x_gravity = x_gravity
        self.y_gravity = y_gravity
        self.width = width
        self.height = height
        self.proposed_move = proposed_move

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            # Set the acceleration value.
            if event.key == pygame.K_LEFT:
                self.x_acceleration = -self.x_acceleration_rate
            if event.key == pygame.K_RIGHT:
                self.x_acceleration = self.x_acceleration_rate
            if event.key == pygame.K_UP:
                self.y_acceleration = -self.y_acceleration_rate
            if event.key == pygame.K_DOWN:
                self.y_acceleration = self.y_acceleration_rate
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                self.x_acceleration = 0
            if event.key in (pygame.K_UP, pygame.K_DOWN):
                self.y_acceleration = 0

    def propose_move(self, event, bounds, move_data_in=None):
        if move_data_in:
            print(dict_print(move_data_in, "Move data in"))
        us = move_data_in is None
        x_acceleration = self.x_acceleration if us else move_data_in['x_acceleration']
        y_acceleration = self.y_acceleration if us else move_data_in['y_acceleration']
        if event is None:
            # print(f'no event type')
            pass
        elif event.type == pygame.KEYDOWN:
            # Set the acceleration value.
            if event.key == pygame.K_LEFT:
                x_acceleration = -self.x_acceleration_rate
            if event.key == pygame.K_RIGHT:
                x_acceleration = self.x_acceleration_rate
            if event.key == pygame.K_UP:
                y_acceleration = -self.y_acceleration_rate
            if event.key == pygame.K_DOWN:
                y_acceleration = self.y_acceleration_rate
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                x_acceleration = 0
            if event.key in (pygame.K_UP, pygame.K_DOWN):
                y_acceleration = 0

        x_change = (self.x_change if us else move_data_in['x_change']) + x_acceleration  # Accelerate.
        y_change = (self.y_change if us else move_data_in['y_change']) + y_acceleration  # Accelerate.
        if abs(x_change) >= self.max_speed:  # If max_speed is exceeded.
            # Normalize the x_change and multiply it with the max_speed.
            x_change = x_change / abs(x_change) * self.max_speed
        if abs(y_change) >= self.max_speed:  # If max_speed is exceeded.
            # Normalize the x_change and multiply it with the max_speed.
            y_change = y_change / abs(y_change) * self.max_speed

        # Decelerate if no key is pressed.
        if x_acceleration == 0:
            x_change *= self.x_de_acceleration_rate
        if y_acceleration == 0:
            y_change *= self.y_de_acceleration_rate

        # Add effect of gravity
        x_change += self.x_gravity
        y_change += self.y_gravity

        # Move the object
        x = self.x if us else move_data_in['x']
        y = self.y if us else move_data_in['y']
        x = clamp(bounds.left + (self.width / 2), x + x_change, bounds.right - (self.width / 2))  # Move the object.
        y = clamp(bounds.top + (self.height / 2), y + y_change, bounds.bottom - (self.height / 2))  # Move the object.

        rect = pygame.Rect(self.rect)
        print(f"pre-commit A rect: {rect}")
        rect.center = x, y
        print(f"pre-commit B rect: {rect}")
        move_data = {
            'x': x,
            'y': y,
            'x_change': x_change,
            'y_change': y_change,
            'x_acceleration': x_acceleration,
            'y_acceleration': y_acceleration,
            'rect': rect
        }
        self.proposed_move = move_data
        return move_data

    def move_commit(self):
        if self.proposed_move is None:
            # print("nothing to commit")
            return
            # raise ValueError("No move proposed to commit.")
        move_data = self.proposed_move
        self.x = move_data['x']
        self.y = move_data['y']
        self.x_change = move_data['x_change']
        self.y_change = move_data['y_change']
        self.x_acceleration = move_data['x_acceleration']
        self.y_acceleration = move_data['y_acceleration']
        self.rect = move_data['rect']
        print(dict_print(move_data, "Committing..."))
        self.proposed_move = None

    def check_collisions(self, other_objects):
        """Return T if this object is colliding with another."""
        # y_rest = self.resting_y(other_objects)
        # if y_rest:
        #     raise ValueError("RESTING Y")
        for other in other_objects:
            assert isinstance(other, PObject)
            # print(f"other: {other}")
            if self != other:
                if self.rect.colliderect(other.rect):
                    # print(f"self: {self} is colliding with other: {other}")
                    return True
        return False

    def resting_x(self, other_objects, inc=True, threshold=0):
        sorted_objects = [obj for obj in other_objects]
        sorted_objects.sort(key=lambda o: o.rect.x)
        rect = pad_rect(self.rect, threshold)
        # print(f"sorted: {sorted_objects}")
        # print(f"og: {other_objects}")
        for other in sorted_objects:
            if self != other:
                if inc:
                    # print(f"other.rect.top == rect.bottom: a:{other.rect.bottom}, b:{rect.top}, c:{other.rect.bottom == rect.top}")
                    if other.rect.right == rect.left:
                        if other.rect.top <= rect.centery <= other.rect.bottom:
                            print("resting to the right of something")
                            return True
                else:
                    if other.rect.left == rect.right:
                        if other.rect.top <= rect.centery <= other.rect.bottom:
                            print("resting the right of something")
                            return True
        return False

    def resting_y(self, other_objects, inc=True, threshold=0):
        sorted_objects = [obj for obj in other_objects]
        sorted_objects.sort(key=lambda o: o.rect.y)
        rect = pad_rect(self.rect, threshold)
        # print(f"sorted: {sorted_objects}")
        # print(f"og: {other_objects}")
        for other in sorted_objects:
            if self != other:
                if inc:
                    # print(f"other.rect.top == rect.bottom: a:{other.rect.bottom}, b:{rect.top}, c:{other.rect.bottom == rect.top}")
                    if other.rect.bottom == rect.top:
                        if other.rect.left <= rect.centerx <= other.rect.right:
                            print("resting underneath something")
                            return True
                else:
                    if other.rect.top == rect.bottom:
                        if other.rect.left <= rect.centerx <= other.rect.right:
                            print("resting on top of something")
                            return True
        return False

    def move(self, bounds):
        self.x_change += self.x_acceleration  # Accelerate.
        self.y_change += self.y_acceleration  # Accelerate.
        if abs(self.x_change) >= self.max_speed:  # If max_speed is exceeded.
            # Normalize the x_change and multiply it with the max_speed.
            self.x_change = self.x_change / abs(self.x_change) * self.max_speed
        if abs(self.y_change) >= self.max_speed:  # If max_speed is exceeded.
            # Normalize the x_change and multiply it with the max_speed.
            self.y_change = self.y_change / abs(self.y_change) * self.max_speed

        # Decelerate if no key is pressed.
        if self.x_acceleration == 0:
            self.x_change *= self.x_de_acceleration_rate
        if self.y_acceleration == 0:
            self.y_change *= self.y_de_acceleration_rate

        # Add effect of gravity
        self.x_change += self.x_gravity
        self.y_change += self.y_gravity

        # Move the object
        self.x = clamp(bounds.left + (self.width / 2), self.x + self.x_change, bounds.right - (self.width / 2))  # Move the object.
        self.y = clamp(bounds.top + (self.height / 2), self.y + self.y_change, bounds.bottom - (self.height / 2))  # Move the object.

        self.rect.center = self.x, self.y

    def draw(self, window):
        pygame.draw.rect(window, self.colour, self.rect)

    def get_x(self):
        return self._x

    def set_x(self, value):
        self._x = value
        if self._rect is not None and self.rect.centerx != self._x:
            self.rect.centerx = self._x

    def del_x(self):
        del self._x

    def get_y(self):
        return self._y

    def set_y(self, value):
        self._y = value
        if self._rect is not None and self.rect.centery != self._y:
            self.rect.centery = self._y

    def del_y(self):
        del self._y

    def get_xy(self):
        return self._xy

    def set_xy(self, value):
        self._xy = value
        if self._rect is not None and self.rect.center != self._xy:
            self.rect.center = self._xy

    def del_xy(self):
        del self._xy

    def get_width(self):
        return self._width

    def set_width(self, value):
        self._width = value
        if self._rect.width != self._width:
            self._rect.width = self._width

    def del_width(self):
        del self._width

    def get_height(self):
        return self._height

    def set_height(self, value):
        self._height = value
        if self._rect.height != self._height:
            self._rect.height = self._height

    def del_height(self):
        del self._height

    def get_rect(self):
        return self._rect

    def set_rect(self, value):
        self._rect = value
        if self._x != self._rect.centerx:
            self._x = self._rect.centerx
        if self._y != self._rect.centery:
            self._y = self._rect.centery
        if self._width != self._rect.width:
            self._width = self._rect.width
        if self._height != self._rect.height:
            self._height = self._rect.height

    def del_rect(self):
        del self._rect

    def __eq__(self, other):
        return isinstance(other, PObject) and self.obj_id == other.obj_id

    def __getitem__(self, item):
        d = {
            'x': self._x,
            'y': self._y,
            'xy': self._xy,
            'obj_id': self.obj_id,
            'rect': self._rect,
            'colour': self.colour,
            'name': self.name,
            'max_speed': self.max_speed,
            'x_acceleration_rate': self.x_acceleration_rate,
            'y_acceleration_rate': self.y_acceleration_rate,
            'x_de_acceleration_rate': self.x_de_acceleration_rate,
            'y_de_acceleration_rate': self.y_de_acceleration_rate,
            'x_gravity': self.x_gravity,
            'y_gravity': self.y_gravity,
            'width': self._width,
            'height': self._height
        }
        try:
            return d[item]
        except KeyError as e:
            message = f"key <{item}> not a member of PObject."

            # This one shows double error:
            # During handling of the above exception, another exception occurred:
            # raise KeyError(message)

            # https://stackoverflow.com/questions/52725278/during-handling-of-the-above-exception-another-exception-occurred
            raise KeyError(message) from None

    def __repr__(self):
        return f"<PObject id:{self.obj_id}, name:{self.name}, rect:{self._rect}>"

    x = property(get_x, set_x, del_x, 'X position of this object')
    y = property(get_y, set_y, del_y, 'Y position of this object')
    xy = property(get_xy, set_xy, del_xy, 'X and Y position of this object')
    rect = property(get_rect, set_rect, del_rect, 'pygame.Rect object representing the position of this object')
    width = property(get_width, set_width, del_width, 'Width of this object')
    height = property(get_height, set_height, del_height, 'Height of this object')


if __name__ == "__main__":
    pygame.init()
    WIDTH, HEIGHT = 750, 550
    WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
    CLOCK = pygame.time.Clock()
    FPS = 60

    FONT_DEFAULT = pygame.font.Font(None, 36)

    running = True

    p_objects = []
    po1 = PObject(52, 35)
    po2 = PObject(50, 150, colour=GREEN)
    p_objects.append(po1)
    p_objects.append(po2)
    # for i in range(10):
    #     p_objects.append(PObject(i * (30 + (2 * i)), 5 + (i * 15), colour=random_colour()))

    while running:
        CLOCK.tick(FPS)

        # reset window
        WINDOW.fill(BLACK)

        # handle events
        events = pygame.event.get()
        for p_obj in p_objects:
            # print(f"obj: {p_obj}")
            move_data = p_obj.propose_move(None, WINDOW.get_rect())
            if p_obj.check_collisions(p_objects):
                handled = False
                if p_obj.resting_y(p_objects) or p_obj.resting_y(p_objects, False):
                    old_rect = pygame.Rect(p_obj.proposed_move['rect'])
                    old_rect.center = p_obj.proposed_move['rect'].centerx, p_obj.rect.y
                    p_obj.proposed_move['rect'] = old_rect
                    p_obj.proposed_move['y'] = p_obj.rect.y
                    p_obj.proposed_move['y_change'] = 0
                    p_obj.proposed_move['y_acceleration'] = 0
                    handled = True
                    print("ADJUSTING A1")
                if p_obj.resting_x(p_objects) or p_obj.resting_x(p_objects, False):
                    old_rect = pygame.Rect(p_obj.proposed_move['rect'])
                    old_rect.center = p_obj.rect.x, p_obj.proposed_move['rect'].centery
                    p_obj.proposed_move['rect'] = old_rect
                    p_obj.proposed_move['x'] = p_obj.rect.x
                    p_obj.proposed_move['x_change'] = 0
                    p_obj.proposed_move['y_acceleration'] = 0
                    handled = True
                    print("ADJUSTING A2")
                if not handled:
                    p_obj.proposed_move = None
                # else:
                #     p_obj.proposed_move = None
                # raise ValueError("ADJUSTING A")
            # TODO check collisions
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                    break
                # print(f"event: {event}")
                move_data = p_obj.propose_move(event, WINDOW.get_rect(), move_data)
                print(dict_print(move_data, "Move Data Out"))
                if p_obj.check_collisions(p_objects):
                    handled = False
                    if p_obj.resting_y(p_objects) or p_obj.resting_y(p_objects, False):
                        # print("resting underneath something")
                        old_rect = pygame.Rect(p_obj.proposed_move['rect'])
                        old_rect.center = p_obj.proposed_move['rect'].centerx, p_obj.rect.y
                        p_obj.proposed_move['rect'] = old_rect
                        p_obj.proposed_move['y'] = p_obj.rect.y
                        p_obj.proposed_move['y_change'] = 0
                        p_obj.proposed_move['y_acceleration'] = 0
                        handled = True
                        print("ADJUSTING B")
                    if p_obj.resting_x(p_objects) or p_obj.resting_x(p_objects, False):
                        old_rect = pygame.Rect(p_obj.proposed_move['rect'])
                        old_rect.center = p_obj.rect.x, p_obj.proposed_move['rect'].centery
                        p_obj.proposed_move['rect'] = old_rect
                        p_obj.proposed_move['x'] = p_obj.rect.x
                        p_obj.proposed_move['x_change'] = 0
                        p_obj.proposed_move['y_acceleration'] = 0
                        handled = True
                        print("ADJUSTING B2")
                    if not handled:
                        p_obj.proposed_move = None
                    # else:
                    #     p_obj.proposed_move = None
                    # raise ValueError("ADJUSTING B")
                p_obj_x = move_data['x']
                p_obj_y = move_data['y']
                p_obj_x_change = move_data['x_change']
                p_obj_y_change = move_data['y_change']
                p_obj_x_acceleration = move_data['x_acceleration']
                p_obj_y_acceleration = move_data['y_acceleration']
                p_obj_rect = move_data['rect']

            p_obj.move_commit()
            p_obj.draw(WINDOW)

        # update the display
        pygame.display.update()

    # print(po1)
    # print(po1['x'])
    # # print(po1['xy'])
    # print(po1.__dict__)
    pygame.quit()
