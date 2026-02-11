import math
import pygame
import random
from colour import Color
import copy
red = Color("green")
colors = list(red.range_to(Color("red"),101))
class Player:
    ORIGIN = (0,0)
    THROW_SPEED = 29
    POS_SPEED = 8
    def __init__(self,label,side,eligible,x,y):
        self.offense =side
        self.pos = label
        self.radius = 0 if not eligible else 1
        self.qb = label == 'QB'
        self.coords = (x,y)

    def radiusCalc(self):
        dist = math.dist(self.coords,(507,569))
        
        time = dist/self.THROW_SPEED
        self.radius = time*self.POS_SPEED
    def move(self,orders):
        order = orders.pop()
        self.coords = (order)
        self.radiusCalc()
        if orders:
            self.move(orders)
    



def wr_coverage_percent(r_wr, r_db, d):
    # No overlap
    if d >= r_wr + r_db:
        return 0.0

    # DB fully covers WR
    if d <= abs(r_db - r_wr) and r_db >= r_wr:
        return 100.0

    # Partial overlap
    part1 = r_wr**2 * math.acos(
        (d**2 + r_wr**2 - r_db**2) / (2 * d * r_wr)
    )
    part2 = r_db**2 * math.acos(
        (d**2 + r_db**2 - r_wr**2) / (2 * d * r_db)
    )
    part3 = 0.5 * math.sqrt(
        (-d + r_wr + r_db) *
        ( d + r_wr - r_db) *
        ( d - r_wr + r_db) *
        ( d + r_wr + r_db)
    )

    overlap = part1 + part2 - part3

    return 100 * overlap / (math.pi * r_wr**2)
COLOR = (255, 100, 98)        
SURFACE_COLOR = (167, 255, 100) 
WIDTH = 500
HEIGHT = 500

class Sprite(pygame.sprite.Sprite):
    THROW_SPEED = 29
    POS_SPEED = 8
    ZONE_CENTERS= {}
    ZONE_CENTERS['Deep Half Left'] = (40,40)
    

    def __init__(self, color, height, width, layer=0, shape=0,text="DB"):
        super().__init__()
        self.shape = shape
        self.color = color
        self.width = width
        self.height = height
        self.radius = 25
        self._layer = layer
        self.font = pygame.font.SysFont("Arial", 12)
        self.textSurf = self.font.render(text, 1, BLACK)
        self._redraw()
        self.rect = self.image.get_rect()
        W = self.textSurf.get_width()
        H = self.textSurf.get_height()
        self.image.blit(self.textSurf, [width/2 - W/2, height/2 - H/2])
        self.pos = pygame.math.Vector2(self.rect.center)
        self.dragging = False
        self.speed = 80

    def _redraw(self):
        if self.shape == 0:  # square
            self.image = pygame.Surface((self.width, self.height))
            self.image.fill(SURFACE_COLOR)
            self.image.set_colorkey(COLOR)
            pygame.draw.rect(
                self.image, self.color,
                pygame.Rect(0, 0, self.width, self.height)
            )
        else:  # circle
            size = int(self.radius * 2)
            self.image = pygame.Surface((size, size), pygame.SRCALPHA)
            color = colors[0]
            pygame.draw.circle(
                self.image,
                (int(color.red   * 255),int(color.green * 255),int(color.blue  * 255), 120),
                (self.radius, self.radius),
                self.radius
            )

    def changeSize(self):
        # distance from origin
        coords = self.rect.center
        dist = math.dist(coords, (507, 569))

        time = dist / self.THROW_SPEED
        self.radius = max(1, int(time * self.POS_SPEED))

        # preserve center
        center = self.rect.center

        # redraw and reset rect
        self._redraw()
        self.rect = self.image.get_rect(center=center)

    def collision(self,player):

        size = int(self.radius * 2)
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        color = colors[int(wr_coverage_percent(self.radius,player.radius,math.dist(self.rect.center,player.rect.center)))]
        
        pygame.draw.circle(
                self.image,
                (int(color.red   * 255),int(color.green * 255),int(color.blue  * 255), 120),
                (self.radius, self.radius),
                self.radius
            )
    def wr_coverage_percent(r_wr, r_db, d):
    # No overlap
        if d >= r_wr + r_db:
            return 0.0

        # DB fully covers WR
        if d <= abs(r_db - r_wr) and r_db >= r_wr:
            return 100.0

        # Partial overlap
        part1 = r_wr**2 * math.acos(
            (d**2 + r_wr**2 - r_db**2) / (2 * d * r_wr)
        )
        part2 = r_db**2 * math.acos(
            (d**2 + r_db**2 - r_wr**2) / (2 * d * r_db)
        )
        part3 = 0.5 * math.sqrt(
            (-d + r_wr + r_db) *
            ( d + r_wr - r_db) *
            ( d - r_wr + r_db) *
            ( d + r_wr + r_db)
        )

        overlap = part1 + part2 - part3

        return 100 * overlap / (math.pi * r_wr**2)
    def movement(self,zone,time):
        if zone == "Left Deep Half":
            x_goal = 212
            y_goal = 168
            self.action((x_goal,y_goal),time)
        elif zone == "Right Deep Half":
            x_goal = 805
            y_goal = 170
            self.action((x_goal,y_goal),time)
        elif zone == "Left Curl Flat":
            x_goal = 905
            y_goal = 365
            self.action((x_goal,y_goal),time)
        elif zone == "Right Curl Flat":
            x_goal = 0
            y_goal = 365
            self.action((x_goal,y_goal),time)
        elif zone == "Left Cloud Flat":
            x_goal = 120
            y_goal = 315
            self.action((x_goal,y_goal),time)
        elif zone == "Right Cloud Flat":
            x_goal = 885
            y_goal = 315
            self.action((x_goal,y_goal),time)
        elif zone == "Left Hook":
            x_goal = 305
            y_goal = 325
            self.action((x_goal,y_goal),time)
        elif zone == "Right Hook":
            x_goal = 725
            y_goal = 325
            self.action((x_goal,y_goal),time)
        elif zone == "Middle Third":
            x_goal = 510
            y_goal = 165
            self.action((x_goal,y_goal),time)
        elif zone == "Middle Read":
            x_goal = 510
            y_goal = 250
            self.action((x_goal,y_goal),time)
        elif zone == "Left Curl":
            x_goal = 405
            y_goal = 325
            self.action((x_goal,y_goal),time)
        elif zone == "Right Curl":
            x_goal = 625
            y_goal = 325
            self.action((x_goal,y_goal),time)
    def action(self,target,dt):
        target = pygame.math.Vector2(target)

        direction = target - self.pos
        distance = direction.length()

        if distance == 0:
            return  # already there

        direction.normalize_ip()

        step = self.speed * (dt / 1000)

        if step >= distance:
            self.pos = target
        else:
            self.pos += direction * step

        self.rect.center = self.pos
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            
            if self.rect.collidepoint(event.pos):
                self.dragging = True

                # Store offset so sprite doesn't jump
                mouse_x, mouse_y = event.pos
                self.offset_x = self.rect.x - mouse_x
                self.offset_y = self.rect.y - mouse_y

        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False

        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                mouse_x, mouse_y = event.pos
                self.rect.x = mouse_x + self.offset_x
                self.rect.y = mouse_y + self.offset_y

class GridSprite(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        size = 20
 
        
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.rect(self.image, WHITE, self.image.get_rect(), 1)
        self.rect = self.image.get_rect(topleft=(x, y))

    def redraw(self,color):
        rect = pygame.Rect(self.x, self.y, 20, 20)
        pygame.draw.rect(win, color, rect, 1)
class StartSprite(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        size = 200
 
        
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.rect(self.image, WHITE, self.image.get_rect(), 0)
        self.rect = self.image.get_rect(topleft=(420, 600))
        font = pygame.font.SysFont(None, 48)  # default font, size 48
        text_surface = font.render("START", True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.image.get_rect().center)
        self.image.blit(text_surface, text_rect)

   
    def handle_event(self, event):
            if event.type == pygame.MOUSEBUTTONDOWN:
                return True
            return False

import pygame
pygame.init()
pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 30)
# Source - https://stackoverflow.com/a/61007670
# Posted by theshubhagrwl, modified by community. See post 'Timeline' for change history
# Retrieved 2026-01-31, License - CC BY-SA 4.0

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
WINDOW_HEIGHT = 880
WINDOW_WIDTH = 1240


# Source - https://stackoverflow.com/a/20842987
# Posted by Bartlomiej Lewandowski, modified by community. See post 'Timeline' for change history
# Retrieved 2026-02-11, License - CC BY-SA 4.0

text_surface = my_font.render('Some Text', True, (255, 255, 255))

global win, CLOCK
   

CLOCK = pygame.time.Clock()
ms = 0
interval = 1
visited = {}
colors2 = {}
blockSize = 10 #Set the size of the grid block
for x in range(-200, WINDOW_WIDTH, blockSize):
    for y in range(-200, WINDOW_HEIGHT, blockSize):
        visited[(x,y)] = {}
        colors2[(x,y)] = BLACK    

grid_sprites = pygame.sprite.Group()
def drawGrid(last=False):
    if last:
        blockSize = 10 #Set the size of the grid block
        for x in range(0, WINDOW_WIDTH, blockSize):
            for y in range(0, WINDOW_HEIGHT, blockSize):
                rect = pygame.Rect(x, y, blockSize, blockSize)
                pygame.draw.rect(win, colors2[(x,y)], rect, 0)
        return

    blockSize = 10 #Set the size of the grid block
    for x in range(0, WINDOW_WIDTH, blockSize):
        for y in range(0, WINDOW_HEIGHT, blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            #pygame.draw.rect(win, WHITE, rect, 0)

def circle_rect_overlap(cx, cy, r, rx, ry, size):
    # closest point on rect to circle center
    closest_x = max(rx, min(cx, rx + size))
    closest_y = max(ry, min(cy, ry + size))

    dx = cx - closest_x
    dy = cy - closest_y

    return dx*dx + dy*dy <= r*r

def gridColor(sprite,time):
    cx, cy = sprite.rect.center
    r = sprite.radius
    CELL = 10
    min_x = int((cx - r) // CELL)
    max_x = int((cx + r) // CELL)
    min_y = int((cy - r) // CELL)
    max_y = int((cy + r) // CELL)
    overlapping_cells = []
    
    for gx in range(min_x, max_x + 1):
        for gy in range(min_y, max_y + 1):
            rx = gx * CELL
            ry = gy * CELL

            if circle_rect_overlap(cx, cy, r, rx, ry, CELL):
                overlapping_cells.append((gx*10, gy*10))
    
    for i in overlapping_cells:
        
        if time in visited:
            visited[i][time] += 1
        else:
            visited[i][time] = 1
colorMapDict = {}      
def colorMap(time):
    return colorMapDict[time]
def loadMaps():
    temp_dict = {}
    time = 500
    while time < 2100:
        temp_dict[time] = copy.deepcopy(colors2)
        summation = 0
        for i in times_dict.keys():
            if abs(i-time) <= 100:
                summation += times_dict[i]
        for i in visited:
            colorval = 0
            for key in visited[i].keys():
                if abs(key-time) <= 100:
                    colorval+=visited[i][key]
            temp_dict[time][i] = (min(255,int(colorval*3/summation*255)),0,0)
        time += 100
    return temp_dict


    


bg = pygame.image.load("unnamed.png")

win = pygame.display.set_mode((1040, 880))
bg = pygame.transform.scale(bg, (1040, 880))

win.fill(BLACK)
pygame.display.set_caption("Moving rectangle")
layers = pygame.sprite.LayeredUpdates()
x = 200
y = 200
width = 20
height = 20
vel = 5
circle_surf = pygame.Surface((50, 50), pygame.SRCALPHA)
loop = 0
total_time = 1
times_dict = {}
positions = {}
positions['FS']= {}
positions['SS'] = {}
positions['CB1'] = {}
positions['CB2'] = {}
positions['LB1'] = {}
positions['LB2'] = {}
positions['LB3'] = {}
positions['FS']['X'] = 355
positions['FS']['Y'] = 210
positions['SS']['X'] = 660
positions['SS']['Y'] = 210
positions['CB1']['X'] = 185
positions['CB1']['Y'] = 370
positions['CB2']['X'] = 815
positions['CB2']['Y'] = 370
positions['LB1']['X'] = 665
positions['LB1']['Y'] = 370
positions['LB2']['X'] = 415
positions['LB2']['Y'] = 350
positions['LB3']['X'] = 540
positions['LB3']['Y'] = 370

while loop < 100:
    start_group = pygame.sprite.Group()
    center_sprites_list = pygame.sprite.Group()
    defense_sprites_list = pygame.sprite.Group()
    layers.empty()
    defense_sprites_list.empty()
    rand = random.randint(0,3)
    #object_ = Sprite("Red", 30, 30,1,text="USER")
    dt1 = Sprite("Red", 30, 30,1,text="DT")
    dt2 = Sprite("Red", 30, 30,1,text="DT")
    dt3 = Sprite("Red", 30, 30,1,text="DT")
    dt4 = Sprite("Red", 30, 30,1,text="DT")
    dt1.rect.x = 550
    dt1.rect.y = 450
    dt2.rect.x = 450
    dt2.rect.y = 450
    dt3.rect.x = 400
    dt3.rect.y = 450
    dt4.rect.x = 600
    dt4.rect.y = 450
    layers.add(dt1)
    layers.add(dt2)
    layers.add(dt3)
    layers.add(dt4)
    #object2 = Sprite("blue", 30, 30,0,1)
    start = StartSprite()
    start_group.add(start)
    """object_.rect.x = 200  
    object_.rect.y = 300
    object2.rect.x = 200  
    object2.rect.y = 300"""

    """layers.add(object_)
    layers.add(object2)"""

    object3 = Sprite("Red", 30, 30,1,text="FS")
    object4 = Sprite("blue", 30, 30,0,1)

    object3.rect.x = positions['FS']['X'] 
    object3.rect.y = positions['FS']['Y']
    object4.rect.x = 200  
    object4.rect.y = 300
    object3.pos = pygame.math.Vector2(object3.rect.center)  
    layers.add(object3)
    layers.add(object4)
    center_sprites_list.add(object3)
    defense_sprites_list.add(object4)
    object5 = Sprite("Red", 30, 30,1,text="SS")
    object6 = Sprite("blue", 30, 30,0,1)

    object5.rect.x = 660  
    object5.rect.y = 210
    object6.rect.x = 300  
    object6.rect.y = 300
    object5.pos = pygame.math.Vector2(object5.rect.center)  
    layers.add(object5)
    layers.add(object6)
    center_sprites_list.add(object5)
    defense_sprites_list.add(object6)
    cb1 = Sprite("Red", 30, 30,1,text="CB1")
    cb1_rad = Sprite("blue", 30, 30,0,1)

    cb1.rect.x = 185 
    cb1.rect.y = 370
    cb1_rad.rect.x = 300  
    cb1_rad.rect.y = 300
    cb1.pos = pygame.math.Vector2(cb1.rect.center)  
    
    layers.add(cb1)
    layers.add(cb1_rad)
    center_sprites_list.add(cb1)
    defense_sprites_list.add(cb1_rad)
    cb2 = Sprite("Red", 30, 30,1,text="CB2")
    cb2_rad = Sprite("blue", 30, 30,0,1)

    cb2.rect.x = 815  
    cb2.rect.y = 370
    cb2_rad.rect.x = 300  
    cb2_rad.rect.y = 300
    cb2.pos = pygame.math.Vector2(cb2.rect.center)  
    layers.add(cb2)
    layers.add(cb2_rad)
    center_sprites_list.add(cb2)
    defense_sprites_list.add(cb2_rad)
    lb1 = Sprite("Red", 30, 30,1,text="LB1")
    lb1_rad = Sprite("blue", 30, 30,0,1)

    lb1.rect.x = 665 
    lb1.rect.y = 370
    lb1_rad.rect.x = 300  
    lb1_rad.rect.y = 300
    lb1.pos = pygame.math.Vector2(lb1.rect.center)   
    layers.add(lb1)
    layers.add(lb1_rad)
    center_sprites_list.add(lb1)
    defense_sprites_list.add(lb1_rad)
    lb2 = Sprite("Red", 30, 30,1,text="LB2")
    lb2_rad = Sprite("blue", 30, 30,0,1)

    lb2.rect.x = 415
    lb2.rect.y = 350
    lb2_rad.rect.x = 300  
    lb2_rad.rect.y = 300
    lb2.pos = pygame.math.Vector2(lb2.rect.center)   

    layers.add(lb2)
    layers.add(lb2_rad)
    center_sprites_list.add(lb2)
    defense_sprites_list.add(lb2_rad)
    lb3 = Sprite("Red", 30, 30,1,text="LB3")
    lb3_rad = Sprite("blue", 30, 30,0,1)

    lb3.rect.x = 540  
    lb3.rect.y = 370
    lb3_rad.rect.x = 300  
    lb3_rad.rect.y = 300
    lb3.pos = pygame.math.Vector2(lb3.rect.center)   

    layers.add(lb3)
    layers.add(lb3_rad)
    center_sprites_list.add(lb3)
    defense_sprites_list.add(lb3_rad)
    object3.rect.x = positions['FS']['X'] 
    object3.rect.y = positions['FS']['Y'] 
    object5.rect.x = positions['SS']['X'] 
    object5.rect.y = positions['SS']['Y'] 
    cb1.rect.x =                        positions['CB1']['X'] 
    cb1.rect.y =                         positions['CB1']['Y'] 
    lb1.rect.x  =                     positions['LB1']['X'] 
    lb1.rect.y =                      positions['LB1']['Y'] 
    cb2.rect.x=    positions['CB2']['X']
    cb2.rect.y = positions['CB2']['Y']
    lb2.rect.x =  positions['LB2']['X']
    lb2.rect.y=                       positions['LB2']['Y'] 
    lb3.rect.x =  positions['LB3']['X']
    lb3.rect.y=                       positions['LB3']['Y']                    
    first = True
    while loop == 0 and first:
        run = True
        while run:
            win.blit(bg,(0,0))
            drawGrid()
            start_group.draw(win)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                
               
                            
                #object_.handle_event(event)
                object3.handle_event(event)
                object5.handle_event(event)
                cb1.handle_event(event)
                cb2.handle_event(event)
                lb1.handle_event(event)
                lb2.handle_event(event)
                lb3.handle_event(event)
                if event.type == pygame.MOUSEBUTTONDOWN:
        
                    if start.rect.collidepoint(event.pos):
                        run = False
                        first = False
                        positions['FS']['X'] = object3.rect.x
                        positions['FS']['Y'] = object3.rect.y
                        positions['SS']['X'] = object5.rect.x
                        positions['SS']['Y'] = object5.rect.y
                        positions['CB1']['X'] = cb1.rect.x
                        positions['CB1']['Y'] = cb1.rect.y
                        positions['LB1']['X'] = lb1.rect.x
                        positions['LB1']['Y'] = lb1.rect.y
                        positions['CB2']['X'] = cb2.rect.x
                        positions['CB2']['Y'] = cb2.rect.y
                        positions['LB2']['X'] = lb2.rect.x
                        positions['LB2']['Y'] = lb2.rect.y
                        positions['LB3']['X'] = lb3.rect.x
                        positions['LB3']['Y'] = lb3.rect.y
                        break
            layers.draw(win)
            pygame.display.update()
    ms = 0
    run = True
    while run:
        pygame.time.delay(10)
        CLOCK.tick()
        interval = CLOCK.get_time()
        ms += interval
        total_time += interval

        win.blit(bg,(0,0))
        drawGrid()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            #object_.handle_event(event)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and x > 0:
            x -= vel
        if keys[pygame.K_RIGHT]:
            x += vel
        if keys[pygame.K_UP] and y > 0:
            y -= vel
        if keys[pygame.K_DOWN]:
            y += vel
        
        
        
       
        
        #object2.rect.center = object_.rect.center
        
        if rand == 0:
            object4.rect.center = object3.rect.center
            object6.rect.center = object5.rect.center
            cb1_rad.rect.center = cb1.rect.center
            cb2_rad.rect.center = cb2.rect.center
            lb1_rad.rect.center = lb1.rect.center
            lb2_rad.rect.center = lb2.rect.center
            lb3_rad.rect.center = lb3.rect.center
            #object2.changeSize()
            object3.movement("Right Curl Flat",interval)
            object5.movement("Left Curl Flat",interval)
            cb1.movement("Left Deep Half",interval)
            cb1_rad.changeSize()
            cb2.movement("Right Deep Half",interval)
            cb2_rad.changeSize()
            lb1.movement("Right Hook",interval)
            lb1_rad.changeSize()
            lb2.movement("Left Hook",interval)
            lb2_rad.changeSize()
            lb3.movement("Middle Third",interval)
            lb3_rad.changeSize()
            object4.changeSize()
            object6.changeSize()
        elif rand == 1:
            object4.rect.center = object3.rect.center
            object6.rect.center = object5.rect.center
            cb1_rad.rect.center = cb1.rect.center
            cb2_rad.rect.center = cb2.rect.center
            lb1_rad.rect.center = lb1.rect.center
            lb2_rad.rect.center = lb2.rect.center
            lb3_rad.rect.center = lb3.rect.center
            #object2.changeSize()
            object3.movement("Left Deep Half",interval)
            object5.movement("Right Deep Half",interval)
            cb1.movement("Left Cloud Flat",interval)
            cb1_rad.changeSize()
            cb2.movement("Right Cloud Flat",interval)
            cb2_rad.changeSize()
            lb1.movement("Right Curl",interval)
            lb1_rad.changeSize()
            lb2.movement("Left Curl",interval)
            lb2_rad.changeSize()
            lb3.movement("Middle Read",interval)
            lb3_rad.changeSize()
            object4.changeSize()
            object6.changeSize()
        elif rand == 2:

            object4.rect.center = object3.rect.center
            object6.rect.center = object5.rect.center
            cb1_rad.rect.center = cb1.rect.center
            cb2_rad.rect.center = cb2.rect.center
            lb1_rad.rect.center = lb1.rect.center
            lb2_rad.rect.center = lb2.rect.center
            lb3_rad.rect.center = lb3.rect.center
            #object2.changeSize()
            object3.movement("Right Curl Flat",interval)
            object5.movement("Middle Third",interval)
            cb1.movement("Left Deep Half",interval)
            cb1_rad.changeSize()
            cb2.movement("Right Deep Half",interval)
            cb2_rad.changeSize()
            lb1.movement("Left Curl Flat",interval)
            lb1_rad.changeSize()
            lb2.movement("Left Curl",interval)
            lb2_rad.changeSize()
            lb3.movement("Right Curl",interval)
            lb3_rad.changeSize()
            object4.changeSize()
            object6.changeSize()
        elif rand == 3:
            object4.rect.center = object3.rect.center
            object6.rect.center = object5.rect.center
            cb1_rad.rect.center = cb1.rect.center
            cb2_rad.rect.center = cb2.rect.center
            lb1_rad.rect.center = lb1.rect.center
            lb2_rad.rect.center = lb2.rect.center
            lb3_rad.rect.center = lb3.rect.center
            #object2.changeSize()
            object3.movement("Left Deep Half",interval)
            object5.movement("Middle Third",interval)
            cb1.movement("Left Cloud Flat",interval)
            cb1_rad.changeSize()
            cb2.movement("Right Deep Half",interval)
            cb2_rad.changeSize()
            lb1.movement("Left Curl Flat",interval)
            lb1_rad.changeSize()
            lb2.movement("Left Hook",interval)
            lb2_rad.changeSize()
            lb3.movement("Right Curl",interval)
            lb3_rad.changeSize()
            object4.changeSize()
            object6.changeSize()
        elif rand == 4:
            object4.rect.center = object3.rect.center
            object6.rect.center = object5.rect.center
            cb1_rad.rect.center = cb1.rect.center
            cb2_rad.rect.center = cb2.rect.center
            lb1_rad.rect.center = lb1.rect.center
            lb2_rad.rect.center = lb2.rect.center
            lb3_rad.rect.center = lb3.rect.center
            #object2.changeSize()
            object3.movement("Left Deep Half",interval)
            object5.movement("Right Deep Half",interval)
            cb1.movement("Left Cloud Flat",interval)
            cb1_rad.changeSize()
            cb2.movement("Right Cloud Flat",interval)
            cb2_rad.changeSize()
            lb1.movement("Right Hook",interval)
            lb1_rad.changeSize()
            lb2.movement("Left Hook",interval)
            lb2_rad.changeSize()
            lb3.movement("Middle Read",interval)
            lb3_rad.changeSize()
            object4.changeSize()
            object6.changeSize()
        
            
        """if pygame.sprite.collide_circle(object2, object4):
            #object2.collision(object4)
            pass"""
        """candidates = pygame.sprite.spritecollide( object2,grid_sprites,False)   
        for i in candidates:
            if pygame.sprite.collide_circle(object2, i):
                i.redraw(WHITE)"""

        win.blit(circle_surf, (x-10 , y-10 ))

        
        for i in defense_sprites_list:
            gridColor(i,ms)
        layers.draw(win)
        pygame.display.update()
        if ms in times_dict:
            times_dict[ms] += 1
        else:
            times_dict[ms] = 1
        if ms > 2100:
            
            run = False
            
    loop += 1
colorMapDict = loadMaps()
page = 500
run = True
colors2 = colorMap(500)
while run:
    pygame.time.delay(10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    CLOCK.tick()
    
    interval = CLOCK.get_time()
    layers.empty()
    defense_sprites_list.empty()
    for keys,values in colors2.items():
        if values[0] > 255:
            print(keys,values)
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
            page = max(500,page-100)
            colors2 = colorMap(page)
    if keys[pygame.K_RIGHT]:
            page=min(page+100,2000)
            colors2 = colorMap(page)
    
    

    
    text_surface = my_font.render(f'Time(ms): {page}', True, (255, 255, 255))
    drawGrid(last=True)
    pygame.draw.line(
    win,              
    (255, 255, 255),  
    (0, 500),         
    (1040, 500),      
    3                
)
    pygame.draw.line(
    win,              
    (255, 255, 255),  
    (0, 300),         
    (1040, 300),      
    3                
)
    pygame.draw.line(
    win,              
    (255, 255, 255),  
    (0, 100),         
    (1040, 100),      
    3                
)

    win.blit(text_surface, (0,0))
    pygame.display.update()
        
