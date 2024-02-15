# This file was created by: Chris Cozort

# import libraries and modules
import pygame as pg
from settings import *
from sprites import *
from random import randint
import sys

# Define game class...
class Game:
    # Define a special method to init the properties of said class...
    def __init__(self):
        # init pygame
        pg.init()
        # set size of screen and be the screen
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        # setting game clock 
        self.clock = pg.time.Clock()
        self.load_data()
    def load_data(self):
        pass
    # Create run method which runs the whole GAME
    def new(self):
        print("create new game...")
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.player1 = Player(self, 1, 1)
        for x in range(10, 20):
            Wall(self, x, 5)

    def run(self):
        # 
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()
    def quit(self):
         pg.quit()
         sys.exit()

    def update(self):
        self.all_sprites.update()
    
    def draw_grid(self):
         for x in range(0, WIDTH, TILESIZE):
              pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
         for y in range(0, HEIGHT, TILESIZE):
              pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
            self.screen.fill(BGCOLOR)
            self.draw_grid()
            self.all_sprites.draw(self.screen)
            pg.display.flip()

    def events(self):
         for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    self.player1.move(dx=-1)
                if event.key == pg.K_RIGHT:
                    self.player1.move(dx=1)
                if event.key == pg.K_UP:
                    self.player1.move(dy=-1)
                if event.key == pg.K_DOWN:
                    self.player1.move(dy=1)

# Instantiate the game... 
g = Game()
# use game method run to run
# g.show_start_screen()
while True:
    g.new()
    g.run()
    # g.show_go_screen()