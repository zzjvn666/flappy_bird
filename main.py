import pygame
import random
import os

# 初始化 Pygame
pygame.init()

# 游戏窗口设置
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 420
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# 加载背景和管道图片
try:
    background = pygame.image.load(r'assets\background.png').convert()
    # 缩放背景图片以适应屏幕大小
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    pipe = pygame.image.load(r'assets\pipe.png').convert_alpha()
    # 缩放管道图片到合适大小
    pipe = pygame.transform.scale(pipe, (52, 320))
    # 翻转管道图片以创建上管道
    top_pipe = pygame.transform.flip(pipe, False, True)
except FileNotFoundError:
    print("图片文件未找到，请检查路径和文件名。")
    pygame.quit()
    quit()

# 加载小鸟图片
bird_folder = 'assets/bird'
bird_images = []
try:
    for filename in os.listdir(bird_folder):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            bird_image = pygame.image.load(os.path.join(bird_folder, filename)).convert_alpha()
            # 缩放小鸟图片到合适大小
            bird_image = pygame.transform.scale(bird_image, (34, 24))
            bird_images.append(bird_image)
except FileNotFoundError:
    print("小鸟图片文件夹或文件未找到，请检查路径。")
    pygame.quit()
    quit()

bird_index = 0
bird = bird_images[bird_index]

# 小鸟属性
bird_x = 50
bird_y = 250
bird_vel_y = 0
gravity = 0.25
jump = -4

# 管道属性
pipe_width = 52
pipe_height = 320
pipe_gap = 150
# 存储所有管道的信息，每个元素是一个元组 (x, top_pipe_top_y)
pipes = []
# 初始创建一个管道对
pipes.append((450, random.randint(-250,-75)))
# 管道移动速度
pipe_vel_x = 2
# 控制管道出现频率，数值越小频率越高
pipe_spawn_frequency =50
pipe_spawn_counter = 0

# 计分系统
score = 0
font = pygame.font.Font(None, 36)

# 小鸟图片切换计时器
bird_frame_counter = 0
bird_frame_rate = 5  # 每 5 帧切换一次图片

# 游戏循环
clock = pygame.time.Clock()
running = True
while running:
    clock.tick(60)

    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_vel_y = jump

    # 更新小鸟位置
    bird_vel_y += gravity
    bird_y += bird_vel_y

    # 更新管道位置
    new_pipes = []
    for pipe_x, top_pipe_top_y in pipes:
        pipe_x -= pipe_vel_x
        if pipe_x + pipe_width > 0:
            new_pipes.append((pipe_x, top_pipe_top_y))
        # 计分逻辑：当小鸟飞过管道中间时得分
        if pipe_x + pipe_width < bird_x and (pipe_x + pipe_width + pipe_vel_x) >= bird_x:
            score += 1
    pipes = new_pipes

    # 控制管道出现频率
    pipe_spawn_counter += 1
    if pipe_spawn_counter >= pipe_spawn_frequency:
        pipe_spawn_counter = 0
        top_pipe_top_y = random.randint(-250,-150)
        pipes.append((SCREEN_WIDTH, top_pipe_top_y))
    # 随着得分增加，加快游戏速度和减少管道间距
    pipe_vel_x = 2  + score//10
    pipe_gap = max(100, 180 - (score // 10) * 10)

    # 碰撞检测
    bird_rect = bird.get_rect(topleft=(bird_x, bird_y))
    for pipe_x, top_pipe_top_y in pipes:
        top_pipe_rect = top_pipe.get_rect(topleft=(pipe_x, top_pipe_top_y))
        bottom_pipe_top_y = top_pipe_top_y + pipe_height + pipe_gap
        bottom_pipe_rect = pipe.get_rect(topleft=(pipe_x, bottom_pipe_top_y))
        if bird_rect.colliderect(top_pipe_rect) or bird_rect.colliderect(bottom_pipe_rect) or bird_y < 0 or bird_y > SCREEN_HEIGHT:
            running = False

    # 切换小鸟图片
    bird_frame_counter += 1
    if bird_frame_counter >= bird_frame_rate:
        bird_frame_counter = 0
        bird_index = (bird_index + 1) % len(bird_images)
        bird = bird_images[bird_index]

    # 绘制背景
    screen.blit(background, (0, 0))

    # 绘制管道
    for pipe_x, top_pipe_top_y in pipes:
        screen.blit(pipe, (pipe_x, top_pipe_top_y))
        bottom_pipe_top_y = top_pipe_top_y + pipe_height + pipe_gap
        screen.blit(pygame.transform.flip(pipe, False, True), (pipe_x, bottom_pipe_top_y))

    # 绘制小鸟
    screen.blit(bird, (bird_x, bird_y))

    # 绘制得分，显示在左上角
    score_text = font.render(str(score), True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    # 更新显示
    pygame.display.flip()

# 退出游戏
pygame.quit()