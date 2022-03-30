from colour_utility import *
from utility import *
import pygame

#	General main loop structure for pygame.
#	Version............1.0
#	Date........2022-03-11
#	Author....Avery Briggs


class PObject:

    def __init__(
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
            height=20
    ):
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

        self.init(
            obj_id,
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
            height=height)

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
            height=20):
        if rect is None:
            rect = pygame.Rect(x, y, width, height)

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

    def __getitem__(self, item):
        d = {
            'x': self.x,
            'y': self.y,
            'xy': self.xy,
            'obj_id': self.obj_id,
            'rect': self.rect,
            'colour': self.colour,
            'name': self.name,
            'max_speed': self.max_speed,
            'x_acceleration_rate': self.x_acceleration_rate,
            'y_acceleration_rate': self.y_acceleration_rate,
            'x_de_acceleration_rate': self.x_de_acceleration_rate,
            'y_de_acceleration_rate': self.y_de_acceleration_rate,
            'x_gravity': self.x_gravity,
            'y_gravity': self.y_gravity,
            'width': self.width,
            'height': self.height
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

    # def __dict__(self):
    #     return {
    #         'x': self.x,
    #         'y': self.y,
    #         'xy': self.xy,
    #         'obj_id': self.obj_id,
    #         'rect': self.rect,
    #         'colour': self.colour,
    #         'name': self.name,
    #         'max_speed': self.max_speed,
    #         'x_acceleration_rate': self.x_acceleration_rate,
    #         'y_acceleration_rate': self.y_acceleration_rate,
    #         'x_de_acceleration_rate': self.x_de_acceleration_rate,
    #         'y_de_acceleration_rate': self.y_de_acceleration_rate,
    #         'x_gravity': self.x_gravity,
    #         'y_gravity': self.y_gravity,
    #         'width': self.width,
    #         'height': self.height
    #     }




if __name__ == "__main__":
    pygame.init()
    WIDTH, HEIGHT = 750, 550
    WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
    CLOCK = pygame.time.Clock()
    FPS = 60

    FONT_DEFAULT = pygame.font.Font(None, 36)

    running = True

    # working vars
    x, y = WIDTH / 2, HEIGHT / 2
    x_change = 0
    y_change = 0
    x_acceleration = 0
    y_acceleration = 0

    # constants (unless changed...)
    max_speed = 15
    x_acceleration_rate = 1  # rate of x acceleration
    y_acceleration_rate = 1.5  # rate of y acceleration
    x_de_acceleration_rate = 0.9  # rate of x friction
    y_de_acceleration_rate = 0.9  # rate of y friction
    x_gravity = 0
    y_gravity = 0.9
    m_width, m_height = 20, 40
    rect = pygame.Rect(0, 0, m_width, m_height)
    rect.center = x, y

    po1 = PObject('0001', 50, 50, height=100)

    while running:
        CLOCK.tick(FPS)

        # reset window
        WINDOW.fill(BLACK)

        # # begin drawing
        # text_surface = FONT_DEFAULT.render("Demo Text", True, GREEN_4, GRAY_27)
        # text_rect = text_surface.get_rect()
        # text_rect.center = WINDOW.get_rect().center
        # WINDOW.blit(text_surface, text_rect)

        # handle events
        for event in pygame.event.get():
            po1.handle_event(event)
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.KEYDOWN:
                # Set the acceleration value.
                if event.key == pygame.K_LEFT:
                    x_acceleration = -x_acceleration_rate
                if event.key == pygame.K_RIGHT:
                    x_acceleration = x_acceleration_rate
                if event.key == pygame.K_UP:
                    y_acceleration = -y_acceleration_rate
                if event.key == pygame.K_DOWN:
                    y_acceleration = y_acceleration_rate
            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    x_acceleration = 0
                if event.key in (pygame.K_UP, pygame.K_DOWN):
                    y_acceleration = 0

        x_change += x_acceleration  # Accelerate.
        y_change += y_acceleration  # Accelerate.
        if abs(x_change) >= max_speed:  # If max_speed is exceeded.
            # Normalize the x_change and multiply it with the max_speed.
            x_change = x_change / abs(x_change) * max_speed
        if abs(y_change) >= max_speed:  # If max_speed is exceeded.
            # Normalize the x_change and multiply it with the max_speed.
            y_change = y_change / abs(y_change) * max_speed

        # Decelerate if no key is pressed.
        if x_acceleration == 0:
            x_change *= x_de_acceleration_rate
        if y_acceleration == 0:
            y_change *= y_de_acceleration_rate

        # Add effect of gravity
        x_change += x_gravity
        y_change += y_gravity

        # Move the object
        win_rect = WINDOW.get_rect()
        x = clamp(win_rect.left + (m_width / 2), x + x_change, win_rect.right - (m_width / 2))  # Move the object.
        y = clamp(win_rect.top + (m_height / 2), y + y_change, win_rect.bottom - (m_height / 2))  # Move the object.

        rect.center = x, y
        pygame.draw.rect(WINDOW, (0, 120, 250), rect)
        po1.move(WINDOW.get_rect())
        po1.draw(WINDOW)

        # update the display
        # draw everything
        # pygame.display.flip()
        # draw everything, or pass a surface or shape to update only that portion.
        pygame.display.update()

    # print(po1)
    # print(po1['x'])
    # # print(po1['xy'])
    # print(po1.__dict__)
    pygame.quit()
