import pygame
import random
import os
import sys
# 初始化 Pygame
pygame.init()

# 游戏窗口设置
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 420
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")
# 设置窗口图标
try:
    icon = pygame.image.load(r'assets\icon.png').convert_alpha()  # 加载图标文件
    pygame.display.set_icon(icon)  # 设置窗口图标
except FileNotFoundError:
    print("窗口图标文件未找到，请检查路径和文件名。")
# 加载背景和管道图片
try:
    background = pygame.image.load(r'assets\background.png').convert()
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    pipe = pygame.image.load(r'assets\pipe.png').convert_alpha()
    pipe = pygame.transform.scale(pipe, (52, 320))
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
            bird_image = pygame.transform.scale(bird_image, (34, 24))
            bird_images.append(bird_image)
except FileNotFoundError:
    print("小鸟图片文件夹或文件未找到，请检查路径。")
    pygame.quit()
    quit()

# 小鸟属性初始化
bird_index = 0
bird = bird_images[bird_index]
bird_x = 50
bird_y = 250
bird_speed = 2  # 控制小鸟上下移动的速度

# 管道属性初始化
pipe_width = 52
pipe_height = 320
pipe_gap = 150
pipes = []
pipes.append((450, random.randint(-250, -150)))
pipe_vel_x = 2
pipe_spawn_frequency = 50
pipe_spawn_counter = 0

# 计分系统
score = 0
font = pygame.font.Font("assets/POWER_UP.ttf", 36)

# 小鸟图片切换计时器
bird_frame_counter = 0
bird_frame_rate = 5  # 每 5 帧切换一次图片


# 游戏结束后的循环
def game_over_screen():
    global bird_x, bird_y, bird_vel_y, pipes, score, pipe_spawn_counter, pipe_gap, pipe_vel_x

    game_over_font = pygame.font.Font("assets/POWER_UP.ttf", 128)
    continue_font = pygame.font.Font("assets/POWER_UP.ttf", 24)
    # 渲染文本
    game_over_text = game_over_font.render("YOU DEAD", True, (255, 255, 255))
    continue_text = continue_font.render("Press Space To Restart", True, (255, 255, 255))
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
    screen.blit(continue_text, (SCREEN_WIDTH // 2 - continue_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
    pygame.display.flip()

    # 等待空格按下
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:  # 只在按键事件中检查按下的键
                if event.key == pygame.K_SPACE:  # 按下空格键继续游戏
                    waiting = False
    # 重置游戏属性
    bird_x = 50
    bird_y = 250
    bird_vel_y = 0
    pipes = [(450, random.randint(-250, -75))]
    score = 0
    pipe_spawn_counter = 0
    pipe_gap = 150
    pipe_vel_x = 2


def main_game():
    global bird_index, bird, bird_y, bird_vel_y, pipes, score, pipe_spawn_counter, pipe_gap, pipe_vel_x, bird_frame_counter  # 添加 bird_frame_counter

    clock = pygame.time.Clock()
    running = True
    move_up = False  # 控制是否向上移动
    move_down = False  # 控制是否向下移动

    while running:
        clock.tick(60)

        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:  # 按下 W 键让小鸟上移
                    move_up = True
                if event.key == pygame.K_s:  # 按下 S 键让小鸟下移
                    move_down = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:  # 松开 W 键停止上移
                    move_up = False
                if event.key == pygame.K_s:  # 松开 S 键停止下移
                    move_down = False

        # 更新小鸟位置
        if move_up:
            bird_y -= bird_speed  # 向上移动
        if move_down:
            bird_y += bird_speed  # 向下移动

        # 更新管道位置
        new_pipes = []
        for pipe_x, top_pipe_top_y in pipes:
            pipe_x -= pipe_vel_x
            if pipe_x + pipe_width > 0:
                new_pipes.append((pipe_x, top_pipe_top_y))
            if pipe_x + pipe_width < bird_x and (pipe_x + pipe_width + pipe_vel_x) >= bird_x:
                score += 1
        pipes = new_pipes

        # 控制管道出现频率
        pipe_spawn_counter += 1
        if pipe_spawn_counter >= pipe_spawn_frequency:
            pipe_spawn_counter = 0
            top_pipe_top_y = random.randint(-250, -150)
            pipes.append((SCREEN_WIDTH, top_pipe_top_y))

        # 随着得分增加调整速度和管道间距
        pipe_vel_x = 2 + score // 10
        pipe_gap = max(100, 150 - (score // 10) * 10)

        # 碰撞检测
        bird_rect = bird.get_rect(topleft=(bird_x, bird_y))
        for pipe_x, top_pipe_top_y in pipes:
            top_pipe_rect = top_pipe.get_rect(topleft=(pipe_x, top_pipe_top_y))
            bottom_pipe_top_y = top_pipe_top_y + pipe_height + pipe_gap
            bottom_pipe_rect = pipe.get_rect(topleft=(pipe_x, bottom_pipe_top_y))
            if bird_rect.colliderect(top_pipe_rect) or bird_rect.colliderect(bottom_pipe_rect) or bird_y < 0 or bird_y > SCREEN_HEIGHT:
                running = False

        # 切换小鸟图片
        bird_frame_counter += 1  # 在全局变量上递增
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

        # 绘制得分
        score_text = font.render(str(score), True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        # 更新显示
        pygame.display.flip()

    # 显示游戏结束界面
    game_over_screen()



# 启动游戏
while True:
    main_game()
