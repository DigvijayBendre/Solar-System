import pygame
import math
pygame.init()

WIDTH, HEIGHT = 1200, 900
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Solar System")

######################################################
RED = (188, 39, 50)
PINK = (255, 192, 203)
WHITE = (255, 255, 255)
DEEPGREEN = (0, 128, 0)
LIGHTGREEN = (192, 255, 63)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
VIOLET = (128, 0, 255)
BROWN = (150, 75, 0)
DARK_GREY = (80, 78, 81)
SPACE_GREY = (52, 61, 70)

######################################################

FONT = pygame.font.SysFont("comicsans", 16)
class Planet:

    ######################################################


    AU = 149.6e6 * 1000                  # 1 AU = 1.496e11 meters 
    G = 6.67428e-11                      # Gravitational Constant
    SCALE = 120/AU                       
    TIMESTEP = 3600*24                   # Actual Revolution time across the Sun will take Years
                                         # to finish a cycle. So TIMESTEP would reduce that time a by Lot

    ######################################################
    '''
                    FUNCTIONS TO BE DECLARED
    1. Variables Initializer = Distance from the Sun, , Radius, Color, Mass
    2. 
    3. 
    4. 
    5. 

    '''

    ######################################################
    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.sun = False 
        self.distance_to_sun = 0
        self.orbit = []

        self.x_vel = 0
        self.y_vel = 0            # by moving in x and y direction simultaneously we are able to make a circle

    def draw(self, win):
        x = self.x * self.SCALE + WIDTH/2
        y = self.y * self.SCALE + HEIGHT/2

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x, y))

            pygame.draw.lines(win, self.color, False, updated_points, 2)

        pygame.draw.circle(win, self.color, (x,y), self.radius)

        if not self.sun:
            distance_text = FONT.render(f"{round(self.distance_to_sun/1000, 1)}km", 1, WHITE)
            mercury_name = FONT.render("Mercury", 1, BROWN)
            venus_name = FONT.render("Venus", 1, DEEPGREEN)
            earth_name = FONT.render("Earth", 1, WHITE)
            mars_name = FONT.render("Mars", 1, RED)
            jupiter_name = FONT.render("Jupiter", 1, YELLOW)
            saturn_name = FONT.render("Saturn", 1, PINK)
            uranus_name = FONT.render("Uranus", 1, BLUE)
            neptune_name = FONT.render("Neptune", 1, LIGHTGREEN)
            pluto_name = FONT.render("Pluto", 1, VIOLET)
          
          # win.blit(distance_text, (x - distance_text.get_width()/2, y - distance_text.get_height()/2))
            win.blit(distance_text, (x , y))

            win.blit(mercury_name, (20 , 20))
            win.blit(venus_name, (20 , 40))
            win.blit(earth_name, (20 , 60))
            win.blit(mars_name, (20 , 80))
            win.blit(jupiter_name, (20 , 100))
            win.blit(saturn_name, (20 , 120))
            win.blit(uranus_name, (20 , 140))
            win.blit(neptune_name, (20 ,160))
            win.blit(pluto_name, (20 , 180))


    def attraction(self, other): 
        # F = GMm/r^2
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other.sun:
            self.distance_to_sun = distance

        force = self.G * self.mass * other.mass / distance**2
        theta = math.atan2(distance_y, distance_x)  #atan2 calcs arctangent of y/x while atan does so for x
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

        self.x_vel += total_fx / self.mass * self.TIMESTEP      # accelaration = force / mass
        self.y_vel += total_fy / self.mass * self.TIMESTEP      
        
        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))

  

def main():
    run = True
    clock = pygame.time.Clock()         #not implementing this will run the simulation at the speed of your pc
    

    sun = Planet(0,0, 30, YELLOW, 1.98892 * 10**30)
    sun.sun = True   #saying that the planet is a sun

    mercury = Planet(0.387 * Planet.AU, 0, 8, BROWN, 3.3 * 10**23)
    mercury.y_vel = 47.4 * 1000

    venus = Planet(0.723 * Planet.AU, 0, 14, DEEPGREEN, 4.8685 * 10**24)
    venus.y_vel = -35.02 * 1000

    earth = Planet(-1 * Planet.AU, 0, 16, WHITE, 5.9742 * 10**24) #-1 so earth is on left of sun
    earth.y_vel = 29.783 * 1000   #km per sec * 1000 = met per sec

    mars = Planet(-1.524 * Planet.AU, 0, 12, RED, 6.39 * 10**23) 
    mars.y_vel = 24.077 * 1000

    jupiter = Planet(5.203 * Planet.AU, 0, 14, YELLOW, 1.898 * 10**27)
    jupiter.y_vel = 13.1 * 1000

    saturn = Planet(9.539 * Planet.AU, 0, 14, PINK, 5.683 * 10**26)
    saturn.y_vel = 9.7 * 1000

    uranus = Planet(19.18 * Planet.AU, 0, 14, BLUE, 8.681 * 10**25)
    uranus.y_vel = -6.8 * 1000

    neptune = Planet(30.06 * Planet.AU, 0, 14, LIGHTGREEN, 1.024 * 10**26)
    neptune.y_vel = 5.4 * 1000
    
    pluto =   Planet(39.53 * Planet.AU, 0, 14, VIOLET, 1.29 * 10**22)
    pluto.y_vel = 4.67 * 1000

    planets = [sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune, pluto]
    # Planets after Mars are too far away thus they won't normally be visible
    # But to make them visible change the Scale at Line 32 to 12/AU
    # Of Course changing the scale would cause the nearer planets to overlap

    while run:
        clock.tick(60) #max frame rate set to 60fps
        WIN.fill((0,0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)

        pygame.display.update()

    pygame.quit()
main()

