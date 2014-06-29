#! /usr/bin/env python3

import sys
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


def check_constraints(func):
    def wrapper(*args, **kwargs):
        res = func()
        return res
    return wrapper

class Snake(object):
    def __init__(self, start_grid_x, start_grid_y):
        self._x = start_grid_x
        self._y = start_grid_y

    def _move_segment_up(self):
        pass
    def _move_segment_down(self):
        pass
    def _move_segment_left(self):
        pass
    def _move_segment_right(self):
        pass

class _Field(object):
    """Field """
    def __init__(self, start_x, start_y, end_x, end_y, config):
        self._start_x = start_x
        self._start_y = start_y
        self._end_x = end_x
        self._end_y = end_y

        #Style
        self._cell_w = config.getint("field", "cell_w")
        self._cell_h = config.getint("field", "cell_h")
        self._border_ext = config.getint("field", "border_ext")
        self._border_int = config.getint("field", "border_int")

        #Color
        header = namedtuple("t", ["section", "var"])
        get_color = lambda t: pygame.Color(*[int(c) for c in config.get(t.section, t.var).split(',')]) 
        
        self._head_color = get_color(header("field", "head_color"))
        self._tail_color = get_color(header("field", "tail_color"))
        self._border_ext_color = get_color(header("field", "border_ext_color"))
        self._border_int_color = get_color(header("field", "border_int_color"))
        del header
        del get_color

        offset = self._border_ext + 2*self._border_int + self._cell_w

        #TODO:
            #Dynamic recalculating grid based on surface's size
            #Dynamic creating grid, rereading config on the fly
        #REFACTOR:
        offset_ext = self._border_ext + 2*self._border_int + self._cell_w

        self._borders_ext = {(x, self._start_y): (x, self._end_y) for x in range(self._start_x, self._end_x, offset_ext)}
        self._borders_ext.update({(self._start_x, y): (self._end_x, y) for y in range(self._start_y, self._end_y, offset_ext)}) 
        
    def draw(self, surface):
        
        for start_point, end_point in self._borders_ext.items():
            pygame.draw.line(surface, self._border_ext_color,
                             start_point, end_point,
                             self._border_ext)

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

        self._field = _Field(0, 0, self._width, self._height, config)

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and 
                                        event.key == K_ESCAPE):
                pygame.quit()
                sys.exit(0)
            else:
                print(event)

    
    def _update(self):
        pass


    def _render(self):
        self._window.fill(pygame.Color(0, 0, 0, 1))
        self._field.draw(self._window)
        pygame.display.update()
        self._fpsClock.tick(self._FPS)
        

    def exec_(self):
        while True:
            self._handle_events()
            self._update()
            self._render()
        return 0

if __name__ == "__main__":
    app = App(config)
    sys.exit(app.exec_())
