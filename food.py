import pygame
import random
from settings import *

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = FOOD_COLOR
        self.glow_color = (255, 200, 100)  
        self.glow_size = 0
        self.glow_direction = 1
        self.randomize_position()
        
    def randomize_position(self):
        """Случайное размещение еды на поле"""
        x = random.randint(0, (SCREEN_WIDTH - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
        y = random.randint(0, (SCREEN_HEIGHT - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
        self.position = (x, y)
        
    def update(self):
        """Обновление анимации свечения"""
        self.glow_size += self.glow_direction * 0.5
        if self.glow_size > 5 or self.glow_size < 0:
            self.glow_direction *= -1
        
    def draw(self, surface):
        """Отрисовка еды с эффектом свечения"""
        self.update()
        
        x, y = self.position
        

        for i in range(3):
            glow_radius = GRID_SIZE // 2 + int(self.glow_size) + i * 2
            glow_surface = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
            alpha = 50 - i * 15
            pygame.draw.circle(glow_surface, (*self.glow_color, alpha), 
                             (glow_radius, glow_radius), glow_radius)
            surface.blit(glow_surface, (x + GRID_SIZE//2 - glow_radius, 
                                       y + GRID_SIZE//2 - glow_radius))
        

        rect = pygame.Rect((x + 2, y + 2), (GRID_SIZE - 4, GRID_SIZE - 4))
        pygame.draw.rect(surface, self.color, rect, border_radius=8)
        

        inner_rect = pygame.Rect((x + 6, y + 6), (GRID_SIZE - 12, GRID_SIZE - 12))
        pygame.draw.rect(surface, (255, 255, 200), inner_rect, border_radius=4)