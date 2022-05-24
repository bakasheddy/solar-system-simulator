import pygame
import math
pygame.init()
WIDTH, HEIGHT = 1100, 800
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('SOLAR SYSTEM SIMULATION')

SUN_COLOR = (253, 184, 19)
MECURY_COLOR = (231, 232, 236)
VENUS_COLOR = (139, 145, 161)
EARTH_COLOR = (10, 20, 116)
MARS_COLOR = (156, 46, 53)
JUPITER_COLOR = (180, 167, 158)
SATURN_COLOR = (250, 229, 191)
URANUS_COLOR = (175, 219, 245)
NEPTUNE_COLOR = (62, 102, 249)

FONT = pygame.font.SysFont('Ace', 19)

# objects


class Planets:
    ASTRO_UNIT = 149.6e6 * 1000
    G = 6.67428e-11
    SCALE = 250/ASTRO_UNIT  # 1AU = 100px
    TIMESTEP = 3600 * 24  # 1day of planet sim

    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.orbit = []
        self.sun = False

        self.x_velocity = 0
        self.y_velocity = 0
        self.distance_to_sun = 0

    # draws the object
    def draw(self, win):
        x = self.x * self.SCALE + WIDTH/2
        y = self.y * self.SCALE + HEIGHT/2

        if len(self.orbit) > 2:
            updated_points = []
            for points in self.orbit:
                x, y = points
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x, y))

            pygame.draw.lines(win, self.color, False, updated_points, 1)

        pygame.draw.circle(win, self.color, (x, y), self.radius)
        if not self.sun:
            distance_text = FONT.render(
                f'{round(self.distance_to_sun/ 1000, 1)}km', True, 'WHITE')
            win.blit(distance_text, (x - distance_text.get_width() /
                     2, y - distance_text.get_height()/2))

    # calsulates force of attraction using pythagoras theory
    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other.sun:
            self.distance_to_sun = distance
        force = self.G * self.mass * other.mass / distance**2
        theta = math.atan2(distance_y, distance_x)
        force_of_x_axis = math.cos(theta) * force
        force_of_y_axis = math.sin(theta) * force
        return force_of_x_axis, force_of_y_axis

    def update_position(self, planets):
        total_fx, total_fy = 0, 0
        for planet in planets:
            if self == planet:
                continue
            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy
        self.x_velocity += total_fx / self.mass * self.TIMESTEP
        self.y_velocity += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_velocity * self.TIMESTEP
        self.y += self.y_velocity * self.TIMESTEP
        self.orbit.append((self.x, self.y))


# event loop
def main():
    run = True
    clock = pygame.time.Clock()

    sun = Planets(0, 0, 35, SUN_COLOR, 1.98892 * 10**30)
    sun.sun = True
    mecury = Planets(0.387 * Planets.ASTRO_UNIT, 0,
                     8, MECURY_COLOR, 3.30 * 10**23)
    mecury.y_velocity = -47.4 * 1000
    venus = Planets(0.723 * Planets.ASTRO_UNIT, 0,
                    15, VENUS_COLOR,  4.8685 * 10**24)
    venus.y_velocity = -35.02 * 1000
    earth = Planets(-0.8 * Planets.ASTRO_UNIT, 0,
                    16, EARTH_COLOR, 5.9742 * 10**24)
    earth.y_velocity = 29.783 * 1000
    mars = Planets(-1.3 * Planets.ASTRO_UNIT, 0, 13, MARS_COLOR, 6.39 * 10**23)
    mars.y_velocity = 24.077 * 1000
    jupiter = Planets(1 * Planets.ASTRO_UNIT, 0, 25,
                      JUPITER_COLOR, 1.898 * 10**27)
    jupiter.y_velocity = -13.06 * 1000
    saturn = Planets(1.5 * Planets.ASTRO_UNIT, 0, 21,
                     SATURN_COLOR, 5.683 * 10**26)
    saturn.y_velocity = -9.68 * 1000
    uranus = Planets(-1.7 * Planets.ASTRO_UNIT, 0,
                     19, URANUS_COLOR, 8.681 * 10**25)
    uranus.y_velocity = 6.80 * 1000
    neptune = Planets(-2 * Planets.ASTRO_UNIT, 0, 18,
                      NEPTUNE_COLOR, 1.024 * 10**26)
    neptune.y_velocity = 5.43 * 1000
    planets = [sun,  mecury, venus, earth,
               mars, jupiter, saturn, uranus, neptune]

    while run:
        pygame.event.get()
        clock.tick(60)
        WINDOW.fill((0, 0, 0))
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                run = False

        for planet in planets:
            planet.update_position(planets)
            planet.draw(WINDOW)

        pygame.display.update()

    pygame.quit()


main()
