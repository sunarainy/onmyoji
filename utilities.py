# -*-coding:utf-8-*-

"""
公共函数
"""

import sys
import os
import datetime
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


if __name__ == '__main__':
    audio_play()
    os.system("pause")
