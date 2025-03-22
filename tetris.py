import pygame
import random

# 初始化 Pygame
pygame.init()

# 定义常量
WIDTH = 300
HEIGHT = 600
BLOCK_SIZE = 30
GRID_WIDTH = WIDTH // BLOCK_SIZE
GRID_HEIGHT = HEIGHT // BLOCK_SIZE

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)

# 定义方块形状
SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1, 1], [0, 0, 1]]
]

COLORS = [CYAN, YELLOW, MAGENTA, GREEN, RED, BLUE, ORANGE]

# 创建游戏窗口
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("俄罗斯方块")

# 初始化网格
grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]


# 生成新方块
def new_piece():
    shape = random.choice(SHAPES)
    color = random.choice(COLORS)
    x = GRID_WIDTH // 2 - len(shape[0]) // 2
    y = 0
    return shape, color, x, y


# 检查方块是否可以移动到指定位置
def can_move(shape, x, y):
    for i in range(len(shape)):
        for j in range(len(shape[0])):
            if shape[i][j]:
                new_x = x + j
                new_y = y + i
                if new_x < 0 or new_x >= GRID_WIDTH or new_y >= GRID_HEIGHT or (
                        new_y >= 0 and grid[new_y][new_x]):
                    return False
    return True


# 将方块固定到网格上
def fix_piece(shape, color, x, y):
    for i in range(len(shape)):
        for j in range(len(shape[0])):
            if shape[i][j]:
                grid[y + i][x + j] = color


# 检查并消除满行
def clear_lines():
    full_lines = []
    for i in range(GRID_HEIGHT):
        if all(grid[i]):
            full_lines.append(i)
    for line in full_lines:
        del grid[line]
        grid.insert(0, [0] * GRID_WIDTH)
    return len(full_lines)


# 绘制网格
def draw_grid():
    for i in range(GRID_HEIGHT):
        for j in range(GRID_WIDTH):
            if grid[i][j]:
                pygame.draw.rect(screen, grid[i][j],
                                 (j * BLOCK_SIZE, i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(screen, BLACK,
                                 (j * BLOCK_SIZE, i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)


# 绘制方块
def draw_piece(shape, color, x, y):
    for i in range(len(shape)):
        for j in range(len(shape[0])):
            if shape[i][j]:
                pygame.draw.rect(screen, color,
                                 ((x + j) * BLOCK_SIZE, (y + i) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(screen, BLACK,
                                 ((x + j) * BLOCK_SIZE, (y + i) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)


# 主游戏循环
clock = pygame.time.Clock()
shape, color, x, y = new_piece()
fall_time = 0
fall_speed = 0.3
score = 0

running = True
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if can_move(shape, x - 1, y):
                    x -= 1
            elif event.key == pygame.K_RIGHT:
                if can_move(shape, x + 1, y):
                    x += 1
            elif event.key == pygame.K_DOWN:
                if can_move(shape, x, y + 1):
                    y += 1
            elif event.key == pygame.K_UP:
                rotated_shape = list(map(list, zip(*reversed(shape))))
                if can_move(rotated_shape, x, y):
                    shape = rotated_shape

    fall_time += clock.get_rawtime()
    clock.tick()

    if fall_time / 1000 >= fall_speed:
        if can_move(shape, x, y + 1):
            y += 1
        else:
            fix_piece(shape, color, x, y)
            score += clear_lines()
            shape, color, x, y = new_piece()
            if not can_move(shape, x, y):
                running = False
        fall_time = 0

    draw_grid()
    draw_piece(shape, color, x, y)

    # 显示分数
    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {score}", 1, WHITE)
    screen.blit(text, (10, 10))

    pygame.display.flip()

pygame.quit()
