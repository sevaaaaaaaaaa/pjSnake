import pygame
import sys
from snake import Snake
from food import Food
from sounds import SoundManager
from settings import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Neon Snake')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 32)
        self.big_font = pygame.font.Font(None, 64)
        self.title_font = pygame.font.Font(None, 80)
        
        self.snake = Snake()
        self.food = Food()
        self.sound_manager = SoundManager()
        self.difficulty = "medium"
        self.game_state = "menu"
        self.running = True
        self.high_score = 0
        
    def draw_grid(self):
        """Отрисовка сетки"""
        for x in range(0, SCREEN_WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, GRID_LINE_COLOR, 
                           (x, 0), (x, SCREEN_HEIGHT), 1)
        for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, GRID_LINE_COLOR, 
                           (0, y), (SCREEN_WIDTH, y), 1)
    
    def handle_events(self):
        """Обработка событий"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()
                
            elif event.type == pygame.KEYDOWN:
                if self.game_state == "playing":
                    if event.key in [pygame.K_UP, pygame.K_w]:
                        self.snake.update_direction(UP)
                    elif event.key in [pygame.K_DOWN, pygame.K_s]:
                        self.snake.update_direction(DOWN)
                    elif event.key in [pygame.K_LEFT, pygame.K_a]:
                        self.snake.update_direction(LEFT)
                    elif event.key in [pygame.K_RIGHT, pygame.K_d]:
                        self.snake.update_direction(RIGHT)
                    elif event.key == pygame.K_ESCAPE:
                        self.show_menu()
                        
                elif self.game_state == "menu":
                    if event.key == pygame.K_1:
                        self.difficulty = "easy"
                        self.start_game()
                    elif event.key == pygame.K_2:
                        self.difficulty = "medium"
                        self.start_game()
                    elif event.key == pygame.K_3:
                        self.difficulty = "hard"
                        self.start_game()
                    elif event.key == pygame.K_ESCAPE:
                        self.running = False
                        
                elif self.game_state == "game_over":
                    if event.key == pygame.K_SPACE:
                        self.start_game()
                    elif event.key == pygame.K_ESCAPE:
                        self.show_menu()
    
    def start_game(self):
        """Начало новой игры"""
        self.snake.reset()
        self.food.randomize_position()
        self.game_state = "playing"
        
    def show_menu(self):
        """Показать меню"""
        self.game_state = "menu"
        
    def update(self):
        """Обновление состояния игры"""
        if self.game_state != "playing":
            return
            
        if not self.snake.move():
            self.game_over()
            return
            
        if self.snake.get_head_position() == self.food.position:
            self.snake.grow()
            self.food.randomize_position()
            
            while self.food.position in self.snake.positions:
                self.food.randomize_position()
        
    def game_over(self):
        """Завершение игры"""
        self.game_state = "game_over"
        self.high_score = max(self.high_score, self.snake.score)
        
    def get_game_speed(self):
        """Получить скорость игры"""
        return DIFFICULTY[self.difficulty]
        
    def draw_menu(self):
        """Отрисовка меню с новым стилем"""
        self.screen.fill(BACKGROUND_COLOR)
        self.draw_grid()
        
        # Полупрозрачный фон для текста
        text_bg = pygame.Surface((600, 400), pygame.SRCALPHA)
        text_bg.fill((0, 0, 0, 150))
        self.screen.blit(text_bg, (SCREEN_WIDTH//2 - 300, 150))
        
        # Заголовок с тенью
        title_shadow = self.title_font.render('NEON SNAKE', True, (0, 0, 0))
        title = self.title_font.render('NEON SNAKE', True, SNAKE_COLOR)
        self.screen.blit(title_shadow, (SCREEN_WIDTH//2 - title.get_width()//2 + 3, 183))
        self.screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 180))
        
        # Опции меню
        options = [
            '1 - ЛЕГКИЙ УРОВЕНЬ',
            '2 - СРЕДНИЙ УРОВЕНЬ',
            '3 - СЛОЖНЫЙ УРОВЕНЬ',
            'ESC - ВЫХОД'
        ]
        
        for i, option in enumerate(options):
            text = self.font.render(option, True, TEXT_COLOR)
            self.screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, 280 + i * 50))
        
        # Рисуем маленькую змейку для демонстрации
        demo_positions = [(SCREEN_WIDTH//2 + 100, 300), 
                         (SCREEN_WIDTH//2 + 75, 300), 
                         (SCREEN_WIDTH//2 + 50, 300)]
        for pos in demo_positions:
            rect = pygame.Rect(pos, (GRID_SIZE-2, GRID_SIZE-2))
            pygame.draw.rect(self.screen, SNAKE_COLOR, rect, border_radius=5)
        
    def draw_playing(self):
        """Отрисовка игрового процесса"""
        self.screen.fill(BACKGROUND_COLOR)
        self.draw_grid()
        self.snake.draw(self.screen)
        self.food.draw(self.screen)
        
        # Панель статистики
        stats_bg = pygame.Surface((200, 90), pygame.SRCALPHA)
        stats_bg.fill((0, 0, 0, 100))
        self.screen.blit(stats_bg, (10, 10))
        
        score_text = self.font.render(f'СЧЕТ: {self.snake.score}', True, TEXT_COLOR)
        diff_text = self.font.render(f'УРОВЕНЬ: {self.difficulty.upper()}', True, TEXT_COLOR)
        length_text = self.font.render(f'ДЛИНА: {self.snake.length}', True, TEXT_COLOR)
        
        self.screen.blit(score_text, (20, 20))
        self.screen.blit(diff_text, (20, 50))
        self.screen.blit(length_text, (20, 80))
        
    def draw_game_over(self):
        """Отрисовка экрана завершения игры"""
        self.screen.fill(BACKGROUND_COLOR)
        self.draw_grid()
        
        # Полупрозрачный фон
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))
        
        # Текст "ИГРА ОКОНЧЕНА"
        game_over_shadow = self.big_font.render('ИГРА ОКОНЧЕНА', True, (0, 0, 0))
        game_over = self.big_font.render('ИГРА ОКОНЧЕНА', True, GAME_OVER_COLOR)
        self.screen.blit(game_over_shadow, (SCREEN_WIDTH//2 - game_over.get_width()//2 + 3, 203))
        self.screen.blit(game_over, (SCREEN_WIDTH//2 - game_over.get_width()//2, 200))
        
        # Статистика
        score = self.font.render(f'Ваш счет: {self.snake.score}', True, TEXT_COLOR)
        high_score = self.font.render(f'Рекорд: {self.high_score}', True, TEXT_COLOR)
        restart = self.font.render('ПРОБЕЛ - Новая игра', True, TEXT_COLOR)
        menu = self.font.render('ESC - Меню', True, TEXT_COLOR)
        
        self.screen.blit(score, (SCREEN_WIDTH//2 - score.get_width()//2, 280))
        self.screen.blit(high_score, (SCREEN_WIDTH//2 - high_score.get_width()//2, 320))
        self.screen.blit(restart, (SCREEN_WIDTH//2 - restart.get_width()//2, 380))
        self.screen.blit(menu, (SCREEN_WIDTH//2 - menu.get_width()//2, 420))
        
    def draw(self):
        """Отрисовка игры"""
        if self.game_state == "menu":
            self.draw_menu()
        elif self.game_state == "playing":
            self.draw_playing()
        elif self.game_state == "game_over":
            self.draw_game_over()
            
        pygame.display.flip()
        
    def run(self):
        """Главный игровой цикл"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.get_game_speed())