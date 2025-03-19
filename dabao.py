from cx_Freeze import setup, Executable

# 需要的模块
packages = ['pygame', 'os', 'random']

# 需要的文件
include_files = [
    ('assets', 'assets'),  # 将整个 assets 文件夹打包
]

# 排除不需要的库和文件夹
excludes = ['tkinter', 'email', 'unittest', 'lib', 'share']  # 你可以根据实际情况排除更多不需要的模块

# 根据需要的不同操作系统设置 target name 和图标
base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

# 设置构建参数
executables = [
    Executable('main2.py', base=base, target_name='FlappyBird.exe', icon=r'C:\Users\crz\Desktop\4\assets\icon.png')  # 修正为 target_name
]

# 配置 cx_Freeze 打包设置
setup(
    name='FlappyBird',
    version='1.0',
    description='Your Application Description',
    options={
        'build_exe': {
            'packages': packages,  # 只包含需要的库
            'include_files': include_files,  # 额外的文件夹
            'excludes': excludes,  # 排除不需要的模块
        }
    },
    executables=executables
)
