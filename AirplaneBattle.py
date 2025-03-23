import pygame
import random

# 初始化 Pygame
pygame.init()

# 窗口大小
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# 载入背景图片
background = pygame.image.load("./background.png")
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))  #让屏幕大小和背景图片大小一致

# 载入游戏音乐
pygame.mixer.init()
#pygame.mixer.music.load("bgm.mp3")
#pygame.mixer.music.play(-1)  # 无限循环播放

# 颜色
WHITE = (255, 255, 255)

# 载入字体
#font = pygame.font.Font("font.ttf", 24)
font = pygame.font.SysFont(None, 24)  # 默认字体
#large_font = pygame.font.Font("font.ttf", 48)
large_font = pygame.font.Font(None, 48)

# 玩家类
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("./player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80)
        self.speed = 5
        self.hp = 3
        self.score = 0
        self.bullets = pygame.sprite.Group()
        self.super_bullets = pygame.sprite.Group()
        self.shoot_delay = 300                    #普通子弹发射间隔(ms)
        self.last_shot = pygame.time.get_ticks()  #普通子弹上次射击时间
        self.super_shoot_delay = 500   #大招冷却时间0.5秒
        self.last_super_shot = 0       #记录上次大招发射时间

    def update(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += self.speed

        # 发射普通子弹
        now = pygame.time.get_ticks()
        if keys[pygame.K_SPACE] and now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.top)
            self.bullets.add(bullet)

        # 按B键 发射大招（0.5秒冷却）
        if self.score >= 10 and keys[pygame.K_b] and now - self.last_super_shot > self.super_shoot_delay:
            self.last_super_shot = now  # 记录大招发射时间
            bullet = SuperBullet(self.rect.centerx, self.rect.top)
            self.super_bullets.add(bullet)
            self.score -= 10  # 每次使用大招消耗 10 分

# 玩家普通子弹类
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("./bullet.png")
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = -8

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

# 玩家大招子弹类
class SuperBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("./super_bullet.png")
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = -12

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

# 敌机类
class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_type):
        super().__init__()
        self.enemy_type = enemy_type
        self.image = pygame.image.load(f"enemy_{enemy_type}.png")
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-150, -50)
        self.speed = random.randint(5-enemy_type, 6-enemy_type)  #敌机飞行速度
        self.hp = enemy_type * 1      #敌机生命值 =  等级 * 1
        self.bullets = pygame.sprite.Group()
        self.shoot_delay = random.randint(1000, 3000)
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

        # 随机发射子弹
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = EnemyBullet(self.rect.centerx, self.rect.bottom)
            self.bullets.add(bullet)

# 敌机子弹类
class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("./enemy_bullet.png")
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 5

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

# 游戏主循环
def game_loop():
    running = True
    clock = pygame.time.Clock()
    player = Player()
    enemies = pygame.sprite.Group()
    enemy_spawn_delay = 1000
    last_spawn = pygame.time.get_ticks()

    while running:
        clock.tick(60)
        screen.blit(background, (0, 0))

        # 事件处理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        player.update(keys)

        # 生成敌机
        now = pygame.time.get_ticks()
        if now - last_spawn > enemy_spawn_delay:
            last_spawn = now
            enemy = Enemy(random.randint(1, 4))
            enemies.add(enemy)

        # 更新元素
        player.bullets.update()
        player.super_bullets.update()
        enemies.update()
        for enemy in enemies:
            enemy.bullets.update()

        # 碰撞检测：普通子弹
        for bullet in player.bullets:
            hit_enemies = pygame.sprite.spritecollide(bullet, enemies, False)
            for enemy in hit_enemies:
                enemy.hp -= 1
                bullet.kill()
                if enemy.hp <= 0:
                    enemy.kill()
                    player.score += 10

        # 碰撞检测：超级子弹（大招），秒杀所有碰撞的敌机
        for super_bullet in player.super_bullets:
            hit_enemies = pygame.sprite.spritecollide(super_bullet, enemies, True)  # True 表示敌机直接消失
            if hit_enemies:
                super_bullet.kill()  # 大招击中敌人后自己消失
                player.score += len(hit_enemies) * 10  # 每杀一个敌机加 10 分

        # 绘制
        screen.blit(player.image, player.rect)
        player.bullets.draw(screen)
        player.super_bullets.draw(screen)
        enemies.draw(screen)
        for enemy in enemies:
            enemy.bullets.draw(screen)

        # 显示得分
        score_text = font.render(f"Score: {player.score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()

    pygame.quit()

# 运行游戏
game_loop()
