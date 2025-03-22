import pygame
import time
import random
import os

# 初始化pygame
pygame.init()

# 游戏窗口尺寸
window_width = 600
window_height = 400
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("贪吃蛇游戏")

# 颜色定义
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
light_green = (144, 238, 144)
dark_green = (34, 139, 34)
blue = (50, 153, 213)

# 基本参数
snake_block = 15
snake_speed = 15

# 背景图路径
bg_path = "/mnt/data/image.png"  # 这里修改为你的图片路径

# 默认背景颜色
background = blue  # 如果未加载图片，则使用蓝色背景

# 尝试加载背景图像
try:
    if os.path.exists(bg_path):
        background = pygame.image.load(bg_path)
        background = pygame.transform.scale(background, (window_width, window_height))  # 调整大小
    else:
        raise FileNotFoundError(f"未找到图片文件: {bg_path}")
except Exception as e:
    print(f"错误: {e}，使用默认蓝色背景。")

# 字体定义
score_font = pygame.font.SysFont("comicsansms", 40)
msg_font = pygame.font.SysFont("impact", 50)

# 显示分数（右上角，黑色）
def Your_score(score):
    value = score_font.render(f"Score: {score}", True, black)
    window.blit(value, [window_width - value.get_width() - 20, 20])

# 显示Game Over消息，分为两行显示
def message_centered(msg1, msg2, color):
    text1 = msg_font.render(msg1, True, color)
    text2 = msg_font.render(msg2, True, color)

    # 计算两行消息的显示位置
    text1_rect = text1.get_rect(center=(window_width // 2, window_height // 3))
    text2_rect = text2.get_rect(center=(window_width // 2, window_height // 2 + 40))

    window.blit(text1, text1_rect)
    window.blit(text2, text2_rect)

# 画蛇（尾到头，最后一个是蛇头）
def draw_snake(snake_block, snake_list):
    for i, pos in enumerate(snake_list):
        color = dark_green if i == len(snake_list) - 1 else light_green
        pygame.draw.rect(window, color, [pos[0], pos[1], snake_block, snake_block])

# 画食物（圆形）
def draw_food(x, y):
    pygame.draw.circle(window, yellow, (x + snake_block // 2, y + snake_block // 2), snake_block // 2)

# 蛇是否吃到食物（精确碰撞）
def check_food_collision(x1, y1, fx, fy):
    return abs(x1 - fx) < snake_block and abs(y1 - fy) < snake_block

# 游戏开始界面
def game_start_screen():
    window.fill(blue)
    message_centered("Press Any Key to Start", " ", white)
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                waiting = False

# 游戏主循环
def gameLoop():
    game_over = False
    game_close = False
    game_paused = False

    # 初始蛇的位置和方向
    x1 = window_width / 2
    y1 = window_height / 2
    x1_change = 0
    y1_change = 0

    snake_list = []
    snake_length = 1

    foodx = round(random.randrange(0, window_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, window_height - snake_block) / 10.0) * 10.0

    while not game_over:
        while game_close:
            window.fill(blue)
            message_centered("Game Over!", "Press Q to Quit or C to Restart", red)
            Your_score(snake_length - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        # 暂停功能
        if game_paused:
            window.fill(blue)
            message_centered("Paused!", "Press P to Resume", red)
            Your_score(snake_length - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:  # 按 P 键继续游戏
                        game_paused = False
                    elif event.key == pygame.K_q:
                        game_over = True
                        game_close = False

        # 处理所有键盘事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and not game_paused:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and not game_paused:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP and not game_paused:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN and not game_paused:
                    y1_change = snake_block
                    x1_change = 0
                elif event.key == pygame.K_p:  # 按 P 键暂停游戏
                    game_paused = True

        # 暂停时蛇不再移动，方向不变
        if game_paused:
            x1_change = 0
            y1_change = 0

        # 判断是否撞到墙壁
        if x1 >= window_width or x1 < 0 or y1 >= window_height or y1 < 0:
            game_close = True

        # 更新蛇的位置
        x1 += x1_change
        y1 += y1_change

        # 如果背景是图片，使用blit，否则直接填充颜色
        if isinstance(background, pygame.Surface):
            window.blit(background, (0, 0))  # 保证背景图在最底层
        else:
            window.fill(background)  # 如果是颜色背景，直接填充颜色

        draw_food(foodx, foody)  # 食物绘制

        # 更新蛇身
        head = [x1, y1]
        snake_list.append(head)
        if len(snake_list) > snake_length:
            del snake_list[0]

        # 如果蛇的头部碰到自己的身体
        for segment in snake_list[:-1]:
            if segment == head:
                game_close = True

        draw_snake(snake_block, snake_list)
        Your_score(snake_length - 1)
        pygame.display.update()

        # 吃到食物
        if check_food_collision(x1, y1, foodx, foody):
            foodx = round(random.randrange(0, window_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, window_height - snake_block) / 10.0) * 10.0
            snake_length += 1

        pygame.time.Clock().tick(snake_speed)

    pygame.quit()
    quit()

# 启动游戏前的开始界面
game_start_screen()

# 启动游戏
gameLoop()
