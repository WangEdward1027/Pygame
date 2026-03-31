import pygame
import random
import sys
import math
import os

pygame.init()

CELL_SIZE = 30
ROWS = 21
COLS = 19
WIDTH = COLS * CELL_SIZE
HEIGHT = ROWS * CELL_SIZE + 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pac-Man Game')

BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
CYAN = (0, 255, 255)
PINK = (255, 184, 255)
ORANGE = (255, 184, 82)
DARK_BLUE = (0, 0, 139)

def get_chinese_font(size):
    font_names = [
        'Microsoft YaHei',
        'SimHei',
        'SimSun',
        'KaiTi',
        'FangSong',
        'Arial Unicode MS',
        'STHeiti',
        'Hiragino Sans GB',
        'WenQuanYi Micro Hei'
    ]
    
    for font_name in font_names:
        try:
            font = pygame.font.SysFont(font_name, size)
            test_surface = font.render('测试', True, WHITE)
            if test_surface.get_width() > 0:
                return font
        except:
            continue
    
    return pygame.font.Font(None, size)

WALL = 1
DOT = 2
EMPTY = 0
POWER_DOT = 3

maze = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,2,2,2,2,2,2,2,2,1,2,2,2,2,2,2,2,2,1],
    [1,3,1,1,2,1,1,1,2,1,2,1,1,1,2,1,1,3,1],
    [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
    [1,2,1,1,2,1,2,1,1,1,1,1,2,1,2,1,1,2,1],
    [1,2,2,2,2,1,2,2,2,1,2,2,2,1,2,2,2,2,1],
    [1,1,1,1,2,1,1,1,0,1,0,1,1,1,2,1,1,1,1],
    [0,0,0,1,2,1,0,0,0,0,0,0,0,1,2,1,0,0,0],
    [1,1,1,1,2,1,0,1,1,0,1,1,0,1,2,1,1,1,1],
    [0,0,0,0,2,0,0,1,0,0,0,1,0,0,2,0,0,0,0],
    [1,1,1,1,2,1,0,1,1,1,1,1,0,1,2,1,1,1,1],
    [0,0,0,1,2,1,0,0,0,0,0,0,0,1,2,1,0,0,0],
    [1,1,1,1,2,1,0,1,1,1,1,1,0,1,2,1,1,1,1],
    [1,2,2,2,2,2,2,2,2,1,2,2,2,2,2,2,2,2,1],
    [1,2,1,1,2,1,1,1,2,1,2,1,1,1,2,1,1,2,1],
    [1,3,2,1,2,2,2,2,2,0,2,2,2,2,2,1,2,3,1],
    [1,1,2,1,2,1,2,1,1,1,1,1,2,1,2,1,2,1,1],
    [1,2,2,2,2,1,2,2,2,1,2,2,2,1,2,2,2,2,1],
    [1,2,1,1,1,1,1,1,2,1,2,1,1,1,1,1,1,2,1],
    [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]

class Pacman:
    def __init__(self):
        self.x = 9
        self.y = 15
        self.direction = 'right'
        self.next_direction = 'right'
        self.mouth_open = True
        self.mouth_timer = 0
    
    def draw(self, screen):
        x = self.x * CELL_SIZE + CELL_SIZE // 2
        y = self.y * CELL_SIZE + CELL_SIZE // 2 + 60
        radius = CELL_SIZE // 2 - 2
        
        mouth_angle = 0.25 if self.mouth_open else 0.05
        
        direction_angles = {
            'right': 0,
            'down': math.pi / 2,
            'left': math.pi,
            'up': -math.pi / 2
        }
        
        base_angle = direction_angles[self.direction]
        
        start_angle = base_angle + mouth_angle
        end_angle = base_angle + 2 * math.pi - mouth_angle
        
        points = [(x, y)]
        num_points = 20
        for i in range(num_points + 1):
            angle = start_angle + (end_angle - start_angle) * i / num_points
            px = x + radius * math.cos(angle)
            py = y + radius * math.sin(angle)
            points.append((px, py))
        
        if len(points) > 2:
            pygame.draw.polygon(screen, YELLOW, points)
    
    def move(self, maze):
        self.mouth_timer += 1
        if self.mouth_timer >= 5:
            self.mouth_open = not self.mouth_open
            self.mouth_timer = 0
        
        directions = {
            'up': (0, -1),
            'down': (0, 1),
            'left': (-1, 0),
            'right': (1, 0)
        }
        
        dx, dy = directions[self.next_direction]
        new_x = self.x + dx
        new_y = self.y + dy
        
        if self.can_move(new_x, new_y, maze):
            self.direction = self.next_direction
            self.x = new_x
            self.y = new_y
            return True
        else:
            dx, dy = directions[self.direction]
            new_x = self.x + dx
            new_y = self.y + dy
            if self.can_move(new_x, new_y, maze):
                self.x = new_x
                self.y = new_y
                return True
        return False
    
    def can_move(self, x, y, maze):
        if x < 0 or x >= COLS or y < 0 or y >= ROWS:
            return False
        return maze[y][x] != WALL

class Ghost:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.direction = random.choice(['up', 'down', 'left', 'right'])
        self.scared = False
    
    def draw(self, screen):
        x = self.x * CELL_SIZE + CELL_SIZE // 2
        y = self.y * CELL_SIZE + CELL_SIZE // 2 + 60
        radius = CELL_SIZE // 2 - 2
        
        color = BLUE if self.scared else self.color
        
        pygame.draw.circle(screen, color, (x, y - 2), radius)
        
        pygame.draw.rect(screen, color, (x - radius, y - 2, radius * 2, radius))
        
        for i in range(3):
            wave_x = x - radius + i * (radius * 2 // 3)
            pygame.draw.circle(screen, color, (wave_x + radius // 3, y + radius - 4), radius // 3)
        
        pygame.draw.circle(screen, WHITE, (x - 4, y - 4), 4)
        pygame.draw.circle(screen, WHITE, (x + 4, y - 4), 4)
        
        eye_color = RED if self.scared else BLACK
        pygame.draw.circle(screen, eye_color, (x - 3, y - 3), 2)
        pygame.draw.circle(screen, eye_color, (x + 5, y - 3), 2)
    
    def move(self, maze):
        directions = {
            'up': (0, -1),
            'down': (0, 1),
            'left': (-1, 0),
            'right': (1, 0)
        }
        
        valid_directions = []
        for dir, (dx, dy) in directions.items():
            new_x = self.x + dx
            new_y = self.y + dy
            if self.can_move(new_x, new_y, maze):
                valid_directions.append(dir)
        
        if valid_directions:
            if random.random() < 0.7 and self.direction in valid_directions:
                dx, dy = directions[self.direction]
                self.x += dx
                self.y += dy
            else:
                self.direction = random.choice(valid_directions)
                dx, dy = directions[self.direction]
                self.x += dx
                self.y += dy
    
    def can_move(self, x, y, maze):
        if x < 0 or x >= COLS or y < 0 or y >= ROWS:
            return False
        return maze[y][x] != WALL

class Game:
    def __init__(self):
        self.pacman = Pacman()
        self.ghosts = [
            Ghost(9, 9, RED),
            Ghost(8, 9, CYAN),
            Ghost(10, 9, PINK),
            Ghost(9, 10, ORANGE)
        ]
        self.score = 0
        self.lives = 3
        self.game_over = False
        self.won = False
        self.power_mode = False
        self.power_timer = 0
        self.maze = [row[:] for row in maze]
        self.font = get_chinese_font(32)
        self.big_font = get_chinese_font(48)
        self.move_timer = 0
        self.ghost_timer = 0
    
    def draw_maze(self, screen):
        for row in range(ROWS):
            for col in range(COLS):
                x = col * CELL_SIZE
                y = row * CELL_SIZE + 60
                
                if self.maze[row][col] == WALL:
                    pygame.draw.rect(screen, BLUE, (x, y, CELL_SIZE, CELL_SIZE))
                    pygame.draw.rect(screen, DARK_BLUE, (x + 2, y + 2, CELL_SIZE - 4, CELL_SIZE - 4), 2)
                elif self.maze[row][col] == DOT:
                    pygame.draw.circle(screen, YELLOW, (x + CELL_SIZE // 2, y + CELL_SIZE // 2), 3)
                elif self.maze[row][col] == POWER_DOT:
                    pygame.draw.circle(screen, YELLOW, (x + CELL_SIZE // 2, y + CELL_SIZE // 2), 8)
    
    def draw_ui(self, screen):
        score_text = self.font.render(f'分数: {self.score}', True, WHITE)
        lives_text = self.font.render(f'生命: {self.lives}', True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (WIDTH - 120, 10))
        
        if self.game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(200)
            overlay.fill(BLACK)
            screen.blit(overlay, (0, 0))
            
            text = '你赢了!' if self.won else '游戏结束!'
            game_over_text = self.big_font.render(text, True, YELLOW if self.won else RED)
            text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30))
            screen.blit(game_over_text, text_rect)
            
            final_score_text = self.font.render(f'最终分数: {self.score}', True, WHITE)
            score_rect = final_score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
            screen.blit(final_score_text, score_rect)
            
            restart_text = self.font.render('按 R 重新开始', True, WHITE)
            restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 60))
            screen.blit(restart_text, restart_rect)
    
    def check_collisions(self):
        for ghost in self.ghosts:
            if ghost.x == self.pacman.x and ghost.y == self.pacman.y:
                if self.power_mode:
                    ghost.x = 9
                    ghost.y = 9
                    self.score += 200
                else:
                    self.lives -= 1
                    if self.lives <= 0:
                        self.game_over = True
                    else:
                        self.reset_positions()
    
    def reset_positions(self):
        self.pacman.x = 9
        self.pacman.y = 15
        self.pacman.direction = 'right'
        self.pacman.next_direction = 'right'
        
        for i, ghost in enumerate(self.ghosts):
            ghost.x = 9
            ghost.y = 9
    
    def check_win(self):
        for row in range(ROWS):
            for col in range(COLS):
                if self.maze[row][col] in [DOT, POWER_DOT]:
                    return False
        return True
    
    def update(self):
        if self.game_over:
            return
        
        self.move_timer += 1
        self.ghost_timer += 1
        
        if self.move_timer >= 8:
            self.pacman.move(self.maze)
            self.move_timer = 0
            
            if 0 <= self.pacman.x < COLS and 0 <= self.pacman.y < ROWS:
                if self.maze[self.pacman.y][self.pacman.x] == DOT:
                    self.maze[self.pacman.y][self.pacman.x] = EMPTY
                    self.score += 10
                elif self.maze[self.pacman.y][self.pacman.x] == POWER_DOT:
                    self.maze[self.pacman.y][self.pacman.x] = EMPTY
                    self.score += 50
                    self.power_mode = True
                    self.power_timer = 420
                    for ghost in self.ghosts:
                        ghost.scared = True
        
        if self.ghost_timer >= 12:
            for ghost in self.ghosts:
                ghost.move(self.maze)
            self.ghost_timer = 0
        
        if self.power_mode:
            self.power_timer -= 1
            if self.power_timer <= 0:
                self.power_mode = False
                for ghost in self.ghosts:
                    ghost.scared = False
        
        self.check_collisions()
        
        if self.check_win():
            self.game_over = True
            self.won = True
    
    def draw(self, screen):
        screen.fill(BLACK)
        self.draw_maze(screen)
        
        if 0 <= self.pacman.x < COLS and 0 <= self.pacman.y < ROWS:
            self.pacman.draw(screen)
        
        for ghost in self.ghosts:
            if 0 <= ghost.x < COLS and 0 <= ghost.y < ROWS:
                ghost.draw(screen)
        
        self.draw_ui(screen)
    
    def restart(self):
        self.__init__()

def main():
    clock = pygame.time.Clock()
    game = Game()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    game.pacman.next_direction = 'up'
                elif event.key == pygame.K_DOWN:
                    game.pacman.next_direction = 'down'
                elif event.key == pygame.K_LEFT:
                    game.pacman.next_direction = 'left'
                elif event.key == pygame.K_RIGHT:
                    game.pacman.next_direction = 'right'
                elif event.key == pygame.K_r:
                    game.restart()
        
        game.update()
        game.draw(screen)
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
