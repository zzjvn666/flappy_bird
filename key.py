
import win32gui

def find_window(title):
    """
    根据窗口标题查找窗口句柄
    """
    hwnd = win32gui.FindWindow(None, title)
    if hwnd == 0:
        print(f"未找到窗口: {title}")
        return None
    return hwnd

import time
from pynput.keyboard import Controller, Key




def main():
    # 设置目标窗口标题
    target_window_title = "Flappy Bird"
    keyboard = Controller()
    # 查找目标窗口
    hwnd = find_window(target_window_title)
    if not hwnd:
        return

    try:
        print(f"开始向窗口 '{target_window_title}' 模拟按键...")
        start_time = time.time()

        while True:
            elapsed_time = time.time() - start_time

            # 每隔1秒按下 'W'
            if int(elapsed_time) % 1 == 0:
                keyboard.press('w')
                time.sleep(0.05)  # 按住时间
                keyboard.release('w')
                print(f"[{time.strftime('%H:%M:%S')}] 按下 W 键")
                time.sleep(0.1)  # 防止重复触发

            # 每隔2秒按下 'S'
            if int(elapsed_time) % 2 == 0:
                keyboard.press('s')
                time.sleep(0.05)  # 按住时间
                keyboard.release('s')
                print(f"[{time.strftime('%H:%M:%S')}] 按下 S 键")
                time.sleep(0.1)  # 防止重复触发
    except KeyboardInterrupt:
        print("模拟结束！")


if __name__ == "__main__":
    main()
