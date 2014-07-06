#! /usr/bin/env python3

import sys
import random
import logging
import configparser

from collections import namedtuple
from datetime import datetime

#DEBUG
from pprint import pprint as P


import pygame
from pygame.locals import *


CONFIG_FILE = './.config'

logger = logging.getLogger('main_logger')

#TODO:
    #There's no ExtendedInterpolation in config parser.
    #Maybe have to do some config preprocessing if only python 2.x found?!

try:
    config = configparser.SafeConfigParser(allow_no_value=True,
                           interpolation=configparser.ExtendedInterpolation())
    config.read(CONFIG_FILE)

except AttributeError as err:
    logger.warn("Extended Interpolation isn't supported in Python 2.x: {0}".format(err))
    config = configparser.SafeConfigParser(allow_no_value=True)
    config.read(CONFIG_FILE)

except configparser.ParsingError as err:
    logger.error('Could not parse {0}: {1}'.format(CONFIG_FILE, err))
    config = None

#TODO:
    # App have to recover defaults if something bad happened with CONFIG_FILE
    # For example:
    #default = generate(default_config)
    #dump(default)

DEBUG = config.getboolean("application", "debug")
if DEBUG:
    logger.setLevel(logging.DEBUG)


Point = namedtuple("Point", ["x", "y"])
#'start' and 'end' are Points
Line = namedtuple("Line", ["start", "end"])
#'direction' is a Point, 'coords' is a tuple of Points
Snake = namedtuple("Snake", ["direction"], ["coords"])

class _Field(object):
    """Field """
    def __init__(self, start_pos, end_pos, config):
        self._start_pos = start_pos
        self._end_pos = end_pos

        #Style
        self._cube_size = config.getint("field", "cube_size")
        self._cell_size = config.getint("field", "cell_size")
        self._line_size = config.getint("field", "line_size")
        
        self._item = self._cell_size + 2 * self._line_size
        
        #TEMP:
        self._max_matrix_x = self._end_pos.x // self._item
        self._max_matrix_y = self._end_pos.y // self._item
        
        self._grid_rtop = Point(self._end_pos.x - self._end_pos.x % self._item,
                                self._end_pos.y - self._end_pos.y % self._item)

        self._surface = None
     
        #Color
        header = namedtuple("t", ["section", "var"])
        get_color = lambda t: pygame.Color(*[int(c)
                                            for c in config.get(t.section, 
                                                                t.var).split(',')]) 
        
        self._head_color = get_color(header("field", "head_color"))
        self._tail_color = get_color(header("field", "tail_color"))
        self._line_color = get_color(header("field", "line_color"))
        del header
        del get_color

        #TODO:
            #Dynamic recalculating grid based on surface's size
            #Dynamic creating grid, rereading config on the fly

        #self._grid_f = self._greed_to_pixels() #dictionary { (grid_x, grid_y) : (left, top) }
    
        #TEMP:
        self._grid_px = self._generate_surface()


    def _generate_surface(self):
        grid_px = []
        
        for i in range(self._start_pos.x, self._grid_rtop.x, self._cell_size):
            grid_px.append(Line(Point(i, self._start_pos.y), 
                                Point(i, self._grid_rtop.y)))
        for i in range(self._start_pos.y, self._grid_rtop.y, self._cell_size):
            grid_px.append(Line(Point(self._start_pos.x, i),
                                Point(self._grid_rtop.x, i)))
        return grid_px[:]


    def _grid_to_pixels(point):
        """
        returns pygame rectangle coordinates in pixels
        
        Point(grid_x, grid_y) --> _grid_to_pixels --> (Point(x, y), width, height) 
        """
        pass
    
    
    def _draw_rect(rect, r_type):
        if r_type == 'head':
            pygame.draw.rect(self._surface, self._head_color, *rect)
        elif r_type == 'tail':
            pygame.draw.rect(self._surface, self._tail_color, *rect)
        elif r_type == 'food':
            pygame.draw.rect(self._surface, self._food_color, *rect)
        

    def draw(self, surface):
        for start_point, end_point in self._grid_px:
            pygame.draw.line(surface, self._line_color,
                             start_point, end_point,
                             self._line_size)
        

class App(object):
    """Main application class"""
    
    def __init__(self, config):
        self._width = config.getint("window", "width")
        self._height = config.getint("window", "height")
        self._FPS = config.getint("window", "FPS")
        
        pygame.init()
        self._fpsClock = pygame.time.Clock()
        
        self._window = pygame.display.set_mode((self._width, self._height))
        pygame.display.set_caption(config.get("window", "caption"))

        self._field = _Field(Point(0, 0), Point(self._width, self._height), config)
        #self._food = Point(

        #TODO:
        #field coordinate system
        #snake's start position - center of field
        #self._snake = [(self._field.x // 2, self._field.y // 2)] 

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and 
                                        event.key == K_ESCAPE):
                pygame.quit()
                sys.exit(0)

            else:
                print(event)

    
    def _update(self):
        #self._Field._update
        pass


    def _render(self):
        self._window.fill(pygame.Color(0, 0, 0, 1))
        
        #self._field_surface = self._field.get_surface()
        
        self._field.draw(self._window)
        pygame.display.update()
        self._fpsClock.tick(self._FPS)
        

    def start(self):
        while True:
            self._handle_events()
            self._update()
            self._render()


if __name__ == "__main__":
    app = App(config)
    sys.exit(app.start())
