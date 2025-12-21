import pygame
import random
from settings import *

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = FOOD_COLOR
        self.randomize_position()
        
    def randomize_position(self):
        x = random.randint(0, (SCREEN_WIDTH - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
        y = random.randint(0, (SCREEN_HEIGHT - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
        self.position = (x, y)
        
    def draw(self, surface):
        x, y = self.position
        
        rect = pygame.Rect((x + 2, y + 2), (GRID_SIZE - 4, GRID_SIZE - 4))
        pygame.draw.rect(surface, self.color, rect, border_radius=6)
