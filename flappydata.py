import pygame
import random
import os
import sys
import time

# 初始化 Pygame
pygame.init()

# 游戏窗口设置
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 480
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# 设置窗口图标
def set_window_icon():
    try:
        icon = pygame.image.load(r'assets\icon.png').convert_alpha()
        pygame.display.set_icon(icon)
    except FileNotFoundError:
        print("窗口图标文件未找到，请检查路径和文件名。")

# 加载图片资源
def load_images():
    try:
        background = pygame.image.load(r'assets\background.png').convert()
        background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        pipe = pygame.image.load(r'assets\pipe.png').convert_alpha()
        pipe = pygame.transform.scale(pipe, (52, 320))
        top_pipe = pygame.transform.flip(pipe, False, True)
        return background, pipe, top_pipe
    except FileNotFoundError:
        print("图片文件未找到，请检查路径和文件名。")
        pygame.quit()
        sys.exit()

# 初始化游戏变量
def init_game_variables():
    global pipe_width, pipe_height, pipe_gap, pipes, pipe_vel_x, pipe_spawn_frequency, pipe_spawn_counter, score, font
    pipe_width = 52
    pipe_height = 320
    pipe_gap = 150
    pipes = []
    pipes.append((450, random.randint(-250, -150)))
    pipe_vel_x = 2
    pipe_spawn_frequency = 50
    pipe_spawn_counter = 0
    score = 0
    font = pygame.font.Font("assets/POWER_UP.ttf", 36)

# 游戏结束后的循环
def game_over_screen():
    global pipes, score, pipe_spawn_counter, pipe_gap, pipe_vel_x
    game_over_font = pygame.font.Font("assets/POWER_UP.ttf", 128)
    continue_font = pygame.font.Font("assets/POWER_UP.ttf", 24)
    game_over_text = game_over_font.render("YOU DEAD", True, (255, 255, 255))
    continue_text = continue_font.render("Press Space To Restart", True, (255, 255, 255))
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
    screen.blit(continue_text, (SCREEN_WIDTH // 2 - continue_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False
                    init_game_variables()

# 绘制管道
def draw_pipes(pipes):
    for pipe_x, top_pipe_top_y in pipes:
        screen.blit(pipe, (pipe_x, top_pipe_top_y + pipe_height + pipe_gap))
        screen.blit(top_pipe, (pipe_x, top_pipe_top_y))

# 主游戏循环
def main_game():
    global pipes, score, pipe_spawn_counter, pipe_gap, pipe_vel_x
    clock = pygame.time.Clock()
    running = True
    img_count = 0
    last_save_time = time.time()
    os.makedirs('imgs', exist_ok=True)
    with open('pos.txt', 'w') as f:
        pass

    while running:
        clock.tick(120)
        current_time = time.time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # 更新管道位置
        new_pipes = []
        for pipe_x, top_pipe_top_y in pipes:
            pipe_x -= pipe_vel_x
            if pipe_x + pipe_width > 0:
                new_pipes.append((pipe_x, top_pipe_top_y))
            if pipe_x + pipe_width < SCREEN_WIDTH // 2 and (pipe_x + pipe_width + pipe_vel_x) >= SCREEN_WIDTH // 2:
                score += 1
        pipes = new_pipes

        # 控制管道出现频率
        pipe_spawn_counter += 1
        if pipe_spawn_counter >= pipe_spawn_frequency:
            pipe_spawn_counter = 0
            top_pipe_top_y = random.randint(-250, -150)
            pipes.append((SCREEN_WIDTH, top_pipe_top_y))

        # 随着得分增加调整速度和管道间距
        pipe_vel_x = min(4,2 + score // 10)
        pipe_gap = max(100, 180 - (score // 10) * 10)

        # 碰撞检测（这里因为没有小鸟，可根据实际需求调整或移除）
        for pipe_x, top_pipe_top_y in pipes:
            top_pipe_rect = top_pipe.get_rect(topleft=(pipe_x, top_pipe_top_y))
            bottom_pipe_top_y = top_pipe_top_y + pipe_height + pipe_gap
            bottom_pipe_rect = pipe.get_rect(topleft=(pipe_x, bottom_pipe_top_y))
            # 可根据需要添加更合适的碰撞结束条件
            if len(pipes) > 0 and (top_pipe_rect.right < 0 or bottom_pipe_rect.right < 0):
                running = False

        # 绘制背景
        screen.blit(background, (0, 0))

        # 绘制管道
        draw_pipes(pipes)

        # 绘制得分
        score_text = font.render(str(score), True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        # 计算并标记最左侧管道中间位置
        if pipes:
            pipe_x, top_pipe_top_y = pipes[0]
            mid_x = pipe_x + pipe_width // 2
            # 上管道底端 y 坐标
            top_pipe_bottom_y = top_pipe_top_y + pipe_height
            # 下管道顶端 y 坐标
            bottom_pipe_top_y = top_pipe_top_y + pipe_height + pipe_gap
            mid_y = (top_pipe_bottom_y + bottom_pipe_top_y) // 2
            # pygame.draw.circle(screen, (255, 0, 0), (mid_x, mid_y), 5)  # 绘制红色圆点标记

            # 保存位置信息到文件
            if current_time - last_save_time >= 0.1:
                img_path = os.path.join('imgs', f'img_{img_count}.png')
                pygame.image.save(screen, img_path)
                with open('pos.txt', 'a') as f:
                    f.write(f'{mid_y}\n')
                img_count += 1
                last_save_time = current_time

        # 更新显示
        pygame.display.flip()

    # 显示游戏结束界面
    game_over_screen()

# 设置窗口图标
set_window_icon()
# 加载图片资源
background, pipe, top_pipe = load_images()
# 启动游戏
init_game_variables()
while True:
    main_game()