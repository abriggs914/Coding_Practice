import pygame
import math

# Tech with Tim tutorial
# 2022-02-20
# https://www.youtube.com/watch?v=WTLPmUHTPqo

if __name__ == '__main__':
    pygame.init()

    WIDTH, HEIGHT = 1600, 1000
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Planet Simulation")

    FONT = pygame.font.SysFont("comicsans", 16)

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    YELLOW = (255, 255, 0)
    BLUE = (100, 149, 237)
    RED = (188, 39, 50)
    DARK_GREY = (80, 78, 81)

    class Planet:

        AU = 149.6e6 * 1000
        G = 6.67428e-11
        SCALE = 80 / AU  # 1 AU = 100 pixels
        TIMESTEP = 3600 * 24 * 1  # 1 day

        def __init__(self, x, y, radius, colour, mass):
            self.x = x
            self.y = y
            self.radius = radius
            self.colour = colour
            self.mass = mass

            self.orbit = []
            self.sun = False
            self.distance_to_sun = 0

            self.x_vel = 0
            self.y_vel = 0

        def draw(self, win):
            x = self.x * self.SCALE + WIDTH / 2
            y = self.y * self.SCALE + HEIGHT / 2

            if len(self.orbit) > 2:
                updated_points = []
                for point in self.orbit:
                    x_, y_ = point
                    x_ = x_ * self.SCALE + WIDTH / 2
                    y_ = y_ * self.SCALE + HEIGHT / 2
                    # if (x_, y_) not in updated_points:
                    updated_points.append((x_, y_))

                pygame.draw.lines(WIN, self.colour, False, updated_points[-100:], 2)

            pygame.draw.circle(win, self.colour, (x, y), self.radius)

            if not self.sun:
                distance_text = FONT.render(f"{round(self.distance_to_sun/1000, 1)}km", 1, WHITE)
                WIN.blit(distance_text, (x - distance_text.get_width() / 2, y - distance_text.get_height() / 2))

        def attraction(self, other):
            other_x, other_y = other.x, other.y
            distance_x = other_x - self.x
            distance_y = other_y - self.y
            distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

            if other.sun:
                self.distance_to_sun = distance

            force = self.G * self.mass * other.mass / distance ** 2
            theta = math.atan2(distance_y, distance_x)
            force_x = math.cos(theta) * force
            force_y = math.sin(theta) * force
            return force_x, force_y

        def update_position(self, planets):
            total_fx = total_fy = 0
            for planet in planets:
                if self == planet:
                    continue
                fx, fy = self.attraction(planet)
                total_fx += fx
                total_fy += fy

            self.x_vel += total_fx / self.mass * self.TIMESTEP
            self.y_vel += total_fy / self.mass * self.TIMESTEP

            self.x += self.x_vel * self.TIMESTEP
            self.y += self.y_vel * self.TIMESTEP
            self.orbit.append((self.x, self.y))

    run = True
    clock = pygame.time.Clock()

    sun = Planet(0, 0, 30, YELLOW, 1.98892 * 10**30)
    sun.sun = True

    mercury = Planet(0.387 * Planet.AU, 0, 8, DARK_GREY, 3.30 * 10**23)
    mercury.y_vel = 47.4 * 1000

    venus = Planet(0.723 * Planet.AU, 0, 14, WHITE, 4.8685 * 10**24)
    venus.y_vel = 35.02 * 1000

    earth = Planet(-1 * Planet.AU, 0, 16, BLUE, 5.9742 * 10**24)
    earth.y_vel = 29.783 * 1000

    mars = Planet(-1.524 * Planet.AU, 0, 12, RED, 6.39 * 10**23)
    mars.y_vel = 24.077 * 1000

    jupiter = Planet(5.2 * Planet.AU, 0, 22, RED, 1.9 * 10**27)
    jupiter.y_vel = 13.99 * 1000

    planets = [sun, venus, mercury, earth, mars, jupiter]

    while run:
        clock.tick(60)
        WIN.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)

        pygame.display.update()

    pygame.quit()


