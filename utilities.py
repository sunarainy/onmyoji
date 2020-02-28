# -*-coding:utf-8-*-

"""
公共函数
"""

import sys
import os
import datetime
import time
import win32api
import win32gui
import win32con
import win32process
import psutil
from ctypes import windll
from PIL import Image as PLI_Image
import pygame as pg


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


def mypath():
    """
    判断是程序是以py格式运行还是exe格式运行，返回当前绝对路径
    :return: absolute path
    """
    if os.path.splitext(sys.argv[0])[1] == '.py':
        mp = os.path.dirname(sys.argv[0])
    else:
        mp = os.path.dirname(sys.executable)
    return mp


def logging(content):
    """
    日志记录
    :param content:记录内容
    """
    print(content)
    filename = mypath() + '/debug.log'
    now = datetime.datetime.now().strftime("%H:%M:%S")
    record = ('[%s]' + content) % now
    with open(filename, 'a') as f:
        f.write(record + '\n')


def audio_play():
    """
    播放音频
    :return:
    """
    custom_music_file = mypath() + '/fuckboss.mp3'
    if not os.path.exists(custom_music_file):
        custom_music_file = 'senbonzakura.mid'
    pg.mixer.init()
    pg.mixer.music.load(resource_path(custom_music_file))
    pg.mixer.music.play(loops=-1)  # 循环播放


def audio_stop():
    """
    停止音频
    :return:
    """
    if pg.mixer:
        if pg.mixer.music.get_busy():
            pg.mixer.music.stop()


def click_left_cur(counts=1):
    """
    鼠标左击指定次数
    :param counts: 鼠标点击次数
    """
    for o in range(counts):
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        time.sleep(0.1)


def click_right_cur():
    """
    鼠标右击
    """
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP | win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)


def move_curpos(x, y):
    """
    鼠标移动到指定坐标
    :param x: 横轴移动量
    :param y: 竖轴移动量
    """
    windll.user32.SetCursorPos(x, y)


def get_curpos():
    """
    显示鼠标当前坐标
    :return: 返回坐标touple
    """
    return win32gui.GetCursorPos()


def get_hash(img):
    """
    对图像缩放至16*16灰度，计算平均hash值
    :param img: 图片对象
    :return: hash值
    """
    img = img.resize((16, 16), PLI_Image.ANTIALIAS).convert('L')
    avg = sum(list(img.getdata())) / 256  # 计算像素平均值
    s = ''.join(map(lambda x: '0' if x < avg else '1', img.getdata()))  # 每个像素进行比对,大于avg为1,反之为0
    return ''.join(map(lambda j: '%x' % int(s[j:j + 4], 2), range(0, 256, 4)))


def hamming(hash1, hash2, n=20):
    """
    对2个hash值进行汉明距离计算，并与指定长度对比
    :param hash1:
    :param hash2:
    :param n: 长度
    :return: 2个hash值是否在长度范围内，返回boolean数据类型
    """
    result = False
    assert len(hash1) == len(hash2)
    hamming_value = sum(ch1 != ch2 for ch1, ch2 in zip(hash1, hash2))
    # print(hamming_value)
    if hamming_value <= n:
        result = True
    return result, hamming_value


def get_hwnds(pid):
    """
    return a list of window handlers based on it process id
    :param pid: process id
    :return: list of hwnds
    """

    def callback(hwnd, hwnds):
        if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
            _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
            if found_pid == pid:
                hwnds.append(hwnd)
        return True

    hwnd_list = []
    win32gui.EnumWindows(callback, hwnd_list)
    return hwnd_list


def check_hwnd(label=r'阴阳师-网易游戏'):
    """
    获取游戏窗口句柄
    :param label: 游戏窗口title
    :return: 游戏窗口存在则返回句柄对象，不存在则返回False
    """
    # hwnd = win32gui.FindWindow(None, label)
    # return hwnd
    print(label)
    process = psutil.process_iter()
    p = None
    for i in process:
        if i.name() == 'onmyoji.exe':
            p = i.pid
    if len(get_hwnds(p)) > 0:
        hwnd = get_hwnds(p)[0]
    else:
        hwnd = None
    if hwnd:
        return hwnd
    else:
        hwnd = win32gui.FindWindow(None, label)
        if hwnd:
            return hwnd
        else:
            print('游戏没有运行')
            return False


def jump_window(hwnd):
    """
    使游戏窗口到最顶层
    :return:
    """
    win32gui.SetForegroundWindow(hwnd)
    win32gui.PostMessage(hwnd, win32con.WM_SYSCOMMAND, win32con.SC_RESTORE, 0)


def init_window_position(root, x, y):
    """
    初始化窗口位置
    :param root: 顶层窗体
    :param x: 横轴分母
    :param y: 竖轴分母
    :return:
    """
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    root.resizable(False, False)
    root.update_idletasks()
    root.deiconify()
    width = root.winfo_width()
    height = root.winfo_height()
    size = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / x, (screenheight - height) / y)
    root.geometry(size)


def time_format(second):
    """
    时间数值格式化
    :param second: 总秒数
    :return: 时间大于60秒则返回00:00:00格式
    """
    try:
        second = int(second)
    except ValueError:
        return second
    if second > 60:
        m, s = divmod(second, 60)
        h, m = divmod(m, 60)
        return ':'.join((str(h).zfill(2), str(m).zfill(2), str(s).zfill(2)))
    else:
        return second


if __name__ == '__main__':
    audio_play()
    os.system("pause")
