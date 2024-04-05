import pygame
import random
import math as m

class Vector():
    def __init__(self, x, y, length, angle):
        self.pi = m.pi
        self.tau = m.pi * 2

        self.x = x
        self.y = y
        self.l = length
        self._d = 0
        self.h = 0
        self.lock = False
        self.a = degreesToRadians(angle)

        self.x1 = x
        self.y1 = y
        self.x2 = 0
        self.y2 = 0
        self.length = length
        self.angle = degreesToRadians(angle)

    #Length of the vector
    def __len__(self):
        return m.sqrt(abs(self.x1 - self.x2)**2 + abs(self.y1 - self.y2)**2)

    #Debug
    def __repr__(self):
        return (f"x1 = {self.x1};y1 = {self.y1};x2 = {self.x2};y2 = {self.y2};angle = {self.angle};length = {self.length};lock = {self.lock}")
    

    #Return vector scalar
    def __mul__(self, other):
        return (self.x2 - self.x1)*(other.x2 - other.x1)+(self.y2 - self.y1)*(other.y2 - other.y1)

    #True if vector equals vector/ Vector both coordinates equals other coordinate
    def __eq__(self, other):
        if type(other) == "class '__main__.Vector'":
            return (self.x1 == other.x1 and 
                    self.y1 == other.y1 and 
                    self.x2 == other.x2 and 
                    self.y2 == other.y2)
        else:
            return (self.x1 == other and 
                    self.y1 == other and 
                    self.x2 == other and 
                    self.y2 == other)

    #True if one of vector coordinates greater then other coordinate
    def __gt__(self, other):
        return (self.x1 > other or
                self.y1 > other or
                self.x2 > other or
                self.y2 > other)

    #True if one of vector coordinates less then other coordinate
    def __lt__(self, other):
        return (self.x1 < other or
                self.y1 < other or
                self.x2 < other or
                self.y2 < other)

    #Returns the max difference between two vectors coordinates
    def __sub__(self, other):
        return max(abs(self.x1 - other.x1), abs(self.y1 - other.y1))

    #Rotate vector
    def _rotate2D(self, l, a):
        return l*m.cos(a)+self.x1, l*m.sin(a)+self.y1

    #Move vector with count
    def moveVector(self, count):
        self.x1 , self.y1 = self._rotate2D(count, self.angle)
        self.x2 , self.y2 = self._rotate2D(self.length, self.angle)

    #Rotate vector by angle
    def rotateVector(self, angle):
        self.angle += degreesToRadians(angle)
        self.x2, self.y2 = self._rotate2D(self.length, self.angle)

    #Reset vector
    def reset(self):
        self.x1 = self.x
        self.y1 = self.y
        self.length = self.l
        self.angle = self.a
        self.x2, self.y2 = self._rotate2D(self.length, self.angle)

    
    #Proportional navigation
    def pn(self, vector, maneuverability):
        dx = self.x1 - vector.x1
        dy = self.y1 - vector.y1
        if self.lock:
            g = m.sqrt(dx**2+dy**2)
        else:
            g = 7000 + m.sqrt(dx**2+dy**2)
        dx = noise(dx, g)
        dy = noise(dy, g)
        angle = m.atan2(dy, dx)
        Dhor = angle - self._d
        self.h += Dhor
        self._d = angle
        self.angle = self.angle+cl(Dhor*maneuverability, -0.044, 0.044)
        self._rotate2D(self.length, self.angle)

    #Check point in field
    def checkInField(self, vector, sector, range):
        dx = self.x1 - vector.x1; dy = self.y1 - vector.y1
        angle = m.atan2(dy ,dx)
        localAngle = m.atan2((self.y1-self.y2),(self.x1-self.x2))

        if thr(angle, localAngle-degreesToRadians(sector), localAngle+degreesToRadians(sector)) and m.sqrt((vector.x1-self.x1)**2 + (vector.y1-self.y1)**2) < range:
            self.lock = True
        else:
            self.lock = False
        return

#Simulating radar noise
def noise(x, dist, gain = 5000):
    return x + random.randint(-dist//gain, dist//gain)

#Clamping number with range
def cl(x, xmin, xmax):
	return max(min(x, xmax), xmin)

#If number in range (Treshhold)
def thr(x, minx, maxx):
	if x > minx and x < maxx: return True
	return False

#Sign of number
def sgn(x):
    try: return abs(x)/x    
    except: return 1

#Convert degrees to radians
def degreesToRadians(deg):
    return deg * (m.pi/180)

#Draw path points
def draw_points(a, sc, tr = True):
    for i in range(len(a)-1):
        j = cl(i+1, 0, len(a)-1)
        pygame.draw.line(sc, (0, 0, 255), (a[i][0][0] , a[i][0][1]), (a[j][0][0], a[j][0][1]), 3)
        pygame.draw.line(sc, (255, 0, 0), (a[i][1][0] , a[i][1][1]), (a[j][1][0], a[j][1][1]), 3)
    if tr:
        for i in range((len(a)-1)//3):
            pygame.draw.line(sc, (200, 200, 200), (a[i*3][0][0] , a[i*3][0][1]), (a[i*3][1][0], a[i*3][1][1]), 3)
    return

#Rotate vector by a/d buttons
def rotation(x, maneuverability):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_d]:
        x.rotateVector(maneuverability)
    if keys[pygame.K_a]:
        x.rotateVector(-maneuverability)
    return x

#main function
def main():
    pi = m.pi
    tau = pi*2
    plane_random_turn_mode = False
    plane_maneuverability = 1
    plane_speed = 70
    rocket_maneuverability = 2.5
    rocket_speed = 140
    rocket_fov = 22.5
    rocket_range = 500
    w = 1000
    h = 1000
    fps = 75

    path = []
    t = 50; turn = 0; tt = 0

    pygame.init()
    sc = pygame.display.set_mode([w, h])
    clock = pygame.time.Clock()
    my_font = pygame.font.SysFont(None, 50)

    running = True
    #Initialising vectors
    rocket = Vector(0, 0, 20, 0)
    plane = Vector(w/2, h/2, 20, 0)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        #Random turn
        t += 1
        if t >= 50:
            t = 0
            turn = random.randint(-m.ceil(plane_maneuverability), m.ceil(plane_maneuverability))
        #Append path points array
        tt += 1
        if tt >= 15:
            path.append([[rocket.x1, rocket.y1],[plane.x1, plane.y1]])
            tt  = 0

        #Reset condition
        if (plane > 1000 or plane < 0) or thr(plane - rocket, 0, 5): plane.reset(); rocket.reset(); path = []


        sc.fill((0, 0, 0))
        clock.tick(fps)
        #Vector changing
        if plane_random_turn_mode:
            plane.rotateVector(turn)
        else:
            plane = rotation(plane, plane_maneuverability)
        rocket.pn(plane, rocket_maneuverability)
        plane.moveVector(plane_speed/fps)
        rocket.moveVector(rocket_speed/fps)
        rocket.checkInField(plane, rocket_fov, rocket_range)

        #Drawing scene
        draw_points(path, sc)
        pygame.draw.circle(sc, (255 ,0 , 0), (plane.x1, plane.y1), plane.length)
        pygame.draw.line(sc, (0, 0, 255), (plane.x1 , plane.y1 ), (plane.x2, plane.y2), 3)

        pygame.draw.circle(sc, (0 ,0 ,255), (rocket.x1, rocket.y1), rocket.length)
        pygame.draw.line(sc, (255, 0, 0), (rocket.x1 , rocket.y1), (rocket.x2, rocket.y2), 3)
        text_surface = my_font.render(f'', False, (0, 255, 0))
        #Draw rocket fov
        ang = degreesToRadians(rocket_fov)
        pygame.draw.line(sc, (0, 200, 0), (rocket.x1 , rocket.y1 ), (rocket_range*m.cos(rocket.angle+ang)+rocket.x1, rocket_range*m.sin(rocket.angle+ang)+rocket.y1), 3)
        pygame.draw.line(sc, (0, 200, 0), (rocket.x1 , rocket.y1 ), (rocket_range*m.cos(rocket.angle-ang)+rocket.x1, rocket_range*m.sin(rocket.angle-ang)+rocket.y1), 3)
        sc.blit(text_surface, (0,0))

        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    main()