import pygame
from enum import Enum
from numpy import random


class Direction(Enum):
    LEFT = 'left'
    RIGHT = 'right'
    UP = 'up'
    DOWN = 'down'

class Color:
    RED = (255,0,0)
    GREEN = (0,255,0)
    BLUE = (0,0,255)
    WHITE = (255,255,255)
    YELLOW = (255,255,0)
    BLACK = (0,0,0)

class Screen:
    # WIDTH = int(1920/3)
    # HEIGHT = int(1080/3)
    WIDTH = 800
    HEIGHT = 600

    FRAME_RATE = 20
    EXIT = False
    TIME_SEC = 0

    def get_dimensions():
        return (Screen.WIDTH, Screen.HEIGHT)
    
class Images:
    images_warrior = None
    images_thug = None
    image_background = None

    def __init__(self):
        image_paths_warrior = self.get_image_paths(name='warrior', number_of_images=2)
        image_paths_thug = self.get_image_paths(name='warrior', number_of_images=2)
        # loading static images
        Images.images_warrior = self.load_sprite_images(image_paths_warrior, color_key=Color.BLACK)
        Images.images_thug = self.load_sprite_images(image_paths_thug, color_key=Color.BLACK)
        Images.image_background = self.load_background_image('res/background.jpg')

    def load_sprite_images(self, paths, color_key):
        images = {}
        for direction in (Direction.LEFT, Direction.RIGHT):
            images[direction] = []
            for path in paths[direction]:
                i = pygame.image.load(path).convert()
                i.set_colorkey(color_key)
                images[direction].append(i)
        return images
    
    def get_image_paths(self,name=None, number_of_images=None):
        paths = {}
        for direction in (Direction.LEFT, Direction.RIGHT):
            paths[direction] = [f'res/{name}_{direction.value}_{i}.png' for i in range(number_of_images)]
        return paths
    
    def load_background_image(self, path):
        return pygame.image.load(path)


    

class Being:
    width, height = None, None
    stepx, stepy = None, None
    directions = (Direction.LEFT, Direction.RIGHT, Direction.UP, Direction.DOWN)

    def __init__(self, image_path, mask_color=None):
        self.direction = random.choice(Being.directions[:2])
        self.frame = 0
        self.image = Images.images_warrior[self.direction][self.frame]
        rect = self.image.get_rect()
        Being.width, Being.height = rect.w, rect.h


    def get_position(self):
        return (self.posx, self.posy)
    
    def set_position(self, posx, posy):
        self.posx = posx
        self.posy = posy
    
    def move_left(self):
        self.image = Images.images_warrior[Direction.LEFT][self.frame]
        self.direction = Direction.LEFT
        self.posx -= self.stepx
        if self.posx < 0:
            self.posx = 0
            self.direction = Direction.RIGHT
        
        self.frame = (self.frame + 1) % 2
    
    def move_right(self):
        self.image = Images.images_warrior[Direction.RIGHT][self.frame]
        self.direction = Direction.RIGHT
        self.posx += self.stepx
        if self.posx + self.width > Screen.WIDTH:
            self.posx = Screen.WIDTH - self.width
            self.direction = Direction.LEFT
        
        self.frame = (self.frame + 1) % 2

    
    def move_up(self):
        self.posy -= self.stepy
        self.direction = Direction.UP
        if self.posy < 0:
            self.posy = 0
            self.direction = Direction.DOWN
    
    def move_down(self):
        self.posy += self.stepy
        self.direction = Direction.DOWN
        if self.posy + self.height > Screen.HEIGHT:
            self.posy = Screen.HEIGHT - self.height
            self.direction = Direction.UP
    

class Warrior(Being):
    
    def __init__(self):
        image_path = 'res/warrior1.png'
        super(Warrior, self).__init__(image_path=image_path, mask_color=Color.BLACK)
        self.set_position(0, Screen.HEIGHT - self.height)
        Warrior.stepx = 40
        Warrior.stepy = 40

class Thug(Being):
    count = 5
    prob_direction_change = 0.05
    stepx, stepy = 10, 10

    def __init__(self):
        image_path = 'res/warrior1.png'
        super(Thug, self).__init__(image_path=image_path, mask_color=Color.BLACK)
        # random start position
        self.set_position(
            random.randint(Warrior.width, high=Screen.WIDTH - self.width),
            random.randint(0, Screen.HEIGHT - self.height - Warrior.height)
        )

    
    def move(self):
        if Thug.prob_direction_change > random.rand():
            self.direction = random.choice(Thug.directions)        

        funcs = {
            Direction.LEFT : self.move_left,
            Direction.RIGHT : self.move_right,
            Direction.UP : self.move_up,
            Direction.DOWN : self.move_down,
        }

        selected_function = funcs[self.direction]
        selected_function()

class Hud:
    def __init__(self):
        # background
        self.width, self.height = (125, 25)
        self.color = Color.RED
        self.alpha = 256
        self.posx, self.posy = 0, 0
    
    def get_position(self):
        return (self.posx, self.posy)
    
    def render_surface(self, score=0):
        # background
        background_surface = pygame.Surface((self.width, self.height))
        background_surface.fill(self.color)
        background_surface.set_alpha(self.alpha)
        background_rect = background_surface.get_rect()
        # text object
        font_object = pygame.font.Font('freesansbold.ttf', 15)
        font_surface = font_object.render(f'Score: {score}', True, Color.BLACK)
        font_rect = font_surface.get_rect()
        font_rect.center = background_rect.center
        background_surface.blit(font_surface, font_rect)

        return background_surface







