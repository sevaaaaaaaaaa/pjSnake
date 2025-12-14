import pygame
from settings import *

class Snake:
    def __init__(self):
        self.reset()
        
    def reset(self):
        """Сброс змеи в начальное состояние"""
        self.length = 3
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.score = 0
        self.food_collected = 0
        self.consecutive_food = 0
        
    def get_head_position(self):
        """Получить позицию головы змеи"""
        return self.positions[0]
    
    def update_direction(self, direction):
        """Обновить направление движения"""
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.direction = direction
    
    def move(self):
        """Движение змеи"""
        head = self.get_head_position()
        x, y = self.direction
        new_x = head[0] + (x * GRID_SIZE)
        new_y = head[1] + (y * GRID_SIZE)
        new_position = (new_x, new_y)
        
        if (new_x < 0 or new_x >= SCREEN_WIDTH or 
            new_y < 0 or new_y >= SCREEN_HEIGHT):
            return False
        
        if new_position in self.positions[1:]:
            return False
        
        self.positions.insert(0, new_position)
        
        if len(self.positions) > self.length:
            self.positions.pop()
            
        return True
    
    def grow(self):
        """Увеличить длину змеи"""
        self.length += 1
        self.food_collected += 1
        self.consecutive_food += 1
        
        self.score += 10
        
        if self.consecutive_food % 5 == 0:
            self.score += 50
    
    def draw(self, surface):
        """Отрисовка змеи с новым стилем"""
        for i, p in enumerate(self.positions):
            if i == 0:
                color = SNAKE_COLOR
                size = GRID_SIZE
                pos = p
            else:
                fade = max(0.3, 1.0 - (i / self.length) * 0.7)
                color = tuple(int(c * fade) for c in SNAKE_COLOR)
                size = GRID_SIZE - 2
                pos = (p[0] + 1, p[1] + 1)
            
            rect = pygame.Rect(pos, (size, size))
            pygame.draw.rect(surface, color, rect, border_radius=5)

            if i == 0:
                eye_size = GRID_SIZE // 5
                eye_offset = GRID_SIZE // 3
                
                if self.direction == RIGHT:
                    eye_pos1 = (p[0] + GRID_SIZE - eye_offset, p[1] + eye_offset)
                    eye_pos2 = (p[0] + GRID_SIZE - eye_offset, p[1] + GRID_SIZE - eye_offset)
                elif self.direction == LEFT:
                    eye_pos1 = (p[0] + eye_offset, p[1] + eye_offset)
                    eye_pos2 = (p[0] + eye_offset, p[1] + GRID_SIZE - eye_offset)
                elif self.direction == UP:
                    eye_pos1 = (p[0] + eye_offset, p[1] + eye_offset)
                    eye_pos2 = (p[0] + GRID_SIZE - eye_offset, p[1] + eye_offset)
                else:  
                    eye_pos1 = (p[0] + eye_offset, p[1] + GRID_SIZE - eye_offset)
                    eye_pos2 = (p[0] + GRID_SIZE - eye_offset, p[1] + GRID_SIZE - eye_offset)
                
                pygame.draw.circle(surface, (0, 0, 0), eye_pos1, eye_size)
                pygame.draw.circle(surface, (0, 0, 0), eye_pos2, eye_size)