# -*-coding:utf-8-*-

"""
对游戏不同阶段的响应动作
"""

import time
import random
import win32api, win32gui, win32con
from ctypes import *
from PIL import ImageGrab, Image as PLI_Image


class GameController:
    def __init__(self, hwnd, scaling):
        """
        对游戏数据进行初始化
        :param hwnd: 游戏窗口句柄
        :param scaling: Windows窗口缩放倍率
        """
        # 获取游戏窗口坐标
        self.hwnd = hwnd
        self.left, self.top, self.right, self.bottom = win32gui.GetWindowRect(self.hwnd)
        self.client_rect = win32gui.GetClientRect(self.hwnd)
        self.width = self.client_rect[2]
        self.height = self.client_rect[3]
        # 获取游戏画面坐标
        self.left, self.top = win32gui.ClientToScreen(self.hwnd, (0, 0))
        self.right, self.bottom = win32gui.ClientToScreen(self.hwnd, (self.width, self.height))
        # 缩放后的游戏窗口坐标
        self.ltrb = list(map(lambda x: x * scaling, [self.left, self.top, self.right, self.bottom]))
        self.scaling_width = self.width * scaling
        self.scaling_height = self.height * scaling
        # 挑战按钮坐标
        self.chllg_btn = (round(self.left + self.width * 0.695),
                          round(self.top + self.height * 0.67),
                          round(self.left + self.width * 0.785),
                          round(self.top + self.height * 0.73))
        # 开始战斗按钮坐标
        self.fght_btn = (round(self.left + self.width * 0.75),
                         round(self.top + self.height * 0.82),
                         round(self.left + self.width * 0.87),
                         round(self.top + self.height * 0.88))
        # 退出战斗按钮采样坐标
        self.exit_btn = (round(self.ltrb[0] + self.scaling_width * 0.014),
                         round(self.ltrb[1] + self.scaling_height * 0.0245),
                         round(self.ltrb[0] + self.scaling_width * 0.0415),
                         round(self.ltrb[1] + self.scaling_height * 0.074))
        # 退出战斗按钮hash
        self.exit_btn_hash = '1ff83ffc3ffe3ffe007e001f001f019f079e1ffe7fff7ffe1ff8078001800000'
        # 结算判定区域采样坐标
        self.settle_area = (round(self.ltrb[0] + self.scaling_width * 0.42),
                            round(self.ltrb[1] + self.scaling_height * 0.82),
                            round(self.ltrb[0] + self.scaling_width * 0.58),
                            round(self.ltrb[1] + self.scaling_height * 0.86))
        # 结算判定区域hash
        self.settle_area_hash = '4f3f672f600fa01fb03ff03ff07df874f171d170c170c970c320c020c000c000'
        # 单刷界面判定采样坐标
        self.single_intf = (round(self.ltrb[0] + self.scaling_width * 0.45),
                            round(self.ltrb[1] + self.scaling_height * 0.1),
                            round(self.ltrb[0] + self.scaling_width * 0.58),
                            round(self.ltrb[1] + self.scaling_height * 0.18))
        self.single_hash = '000000000000000000186e1836387ebc7ebc7eb86ed897fc0000ffffffffffff'
        # 组队界面判定采样坐标#
        self.form_team_intf = (round(self.ltrb[0] + self.scaling_width * 0.12),
                               round(self.ltrb[1] + self.scaling_height * 0.8),
                               round(self.ltrb[0] + self.scaling_width * 0.24),
                               round(self.ltrb[1] + self.scaling_height * 0.88))
        # 组队界面判定hash
        self.form_team_hash = '7ffeffffffffffffcd33cd33c823c923cd93c901e577ffffffff7ffe00000000'
        # 组队栏位1采样坐标
        self.form_team1 = (round(self.ltrb[0] + self.scaling_width * 0.2),
                           round(self.ltrb[1] + self.scaling_height * 0.4),
                           round(self.ltrb[0] + self.scaling_width * 0.28),
                           round(self.ltrb[1] + self.scaling_height * 0.53))
        # 组队栏位2采样坐标
        self.form_team2 = (round(self.ltrb[0] + self.scaling_width * 0.46),
                           round(self.ltrb[1] + self.scaling_height * 0.4),
                           round(self.ltrb[0] + self.scaling_width * 0.54),
                           round(self.ltrb[1] + self.scaling_height * 0.53))
        # 组队栏位3采样坐标
        self.form_team3 = (round(self.ltrb[0] + self.scaling_width * 0.76),
                           round(self.ltrb[1] + self.scaling_height * 0.4),
                           round(self.ltrb[0] + self.scaling_width * 0.84),
                           round(self.ltrb[1] + self.scaling_height * 0.53))
        # 点击屏幕继续字样采样坐标
        self.notice_area = (round(self.ltrb[2] * 0.40),
                            round(self.ltrb[3] * 0.90),
                            round(self.ltrb[2] * 0.60),
                            round(self.ltrb[3] * 0.97))
        # 结算点击区域坐标
        self.blank_area = (round(self.left + self.width * 0.89),
                           round(self.top + self.height * 0.23),
                           round(self.left + self.width * 0.95),
                           round(self.top + self.height * 0.7))
        # 组队栏位为空时hash
        self.form_team_blank_hash = 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff'

        # 悬赏界面采样坐标
        self.offer_intf = (round(self.ltrb[0] + self.scaling_width * 0.4),
                           round(self.ltrb[1] + self.scaling_height * 0.2),
                           round(self.ltrb[0] + self.scaling_width * 0.6),
                           round(self.ltrb[1] + self.scaling_height * 0.28))
        # 悬赏界面hash
        self.offer_hash = 'ffffffffffff3fff35fde004200020000004040420100064247037f7ffffffff'
        # 悬赏接受按钮坐标
        self.accept = (round(self.left + self.width * 0.66),
                       round(self.top + self.height * 0.6))
        # 悬赏拒绝按钮坐标
        self.denied = (round(self.left + self.width * 0.66),
                       round(self.top + self.height * 0.74))

        # 状态初始化
        self._running = 1

    @staticmethod
    def click_left_cur(counts=1):
        """
        鼠标左击指定次数
        :param counts: 鼠标点击次数
        """
        for o in range(counts):
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
            time.sleep(0.1)

    @staticmethod
    def click_right_cur():
        """
        鼠标右击
        """
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP | win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)

    @staticmethod
    def move_curpos(x, y):
        """
        鼠标移动到指定坐标
        :param x: 横轴移动量
        :param y: 竖轴移动量
        """
        windll.user32.SetCursorPos(x, y)

    @staticmethod
    def get_curpos():
        """
        显示鼠标当前坐标
        :return: 返回坐标touple
        """
        return win32gui.GetCursorPos()

    @staticmethod
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

    @staticmethod
    def hamming(hash1, hash2, n=20):
        """
        对2个hash值进行汉明距离计算，并与指定宽松度对比
        :param hash1:
        :param hash2:
        :param n: 宽松度
        :return: 2个hash值是否在宽松范围内，返回boolean数据类型
        """
        result = False
        assert len(hash1) == len(hash2)
        # print(sum(ch1 != ch2 for ch1, ch2 in zip(hash1, hash2)))
        if sum(ch1 != ch2 for ch1, ch2 in zip(hash1, hash2)) <= n:
            result = True
        return result

    def move_curpos_test(self):
        self.move_curpos(self.blank_area[0], self.blank_area[1])

    def form_team_phase(self, mode, fight_num, queue):
        """
        组队阶段控制方法
        :param mode: 组队模式
        :param fight_num: 车队人数
        :param queue: 队列对象
        :return:
        """
        if mode == '单刷':
            # 移动到挑战按钮并点击 每次移动在按钮范围内加入随机坐标位移
            xrandom = int(random.uniform(0, self.chllg_btn[2] - self.chllg_btn[0]))
            yrandom = int(random.uniform(0, self.chllg_btn[3] - self.chllg_btn[1]))
            self.move_curpos(self.chllg_btn[0] + xrandom, self.chllg_btn[1] + yrandom)
            time.sleep(0.5)
            self.click_left_cur()
            return
        elif mode == '司机':
            # 检测是否进入组队界面
            while True:
                if not queue.empty():
                    self._running = queue.get()
                if self._running == 1:
                    catch_img = ImageGrab.grab(self.form_team_intf)
                    if self.hamming(self.get_hash(catch_img), self.form_team_hash, 30):
                        break
                    time.sleep(0.5)
                elif self._running == 0:
                    return
            # 检测队伍人数，符合预期再点开始战斗
            while True:
                if not queue.empty():
                    self._running = queue.get()
                if self._running == 1:
                    num = 0
                    for i in [self.form_team1, self.form_team2, self.form_team3]:
                        catch_img = ImageGrab.grab(i)
                        # self.get_hash(catch_img)
                        if not self.hamming(self.get_hash(catch_img), self.form_team_blank_hash, 10):
                            num = num + 1
                    if num == fight_num:
                        break
                    time.sleep(0.5)
                elif self._running == 0:
                    return
            # 移动到开始战斗按钮并点击 每次移动在按钮范围内加入随机坐标位移
            xrandom = int(random.uniform(0, self.fght_btn[2] - self.fght_btn[0]))
            yrandom = int(random.uniform(0, self.fght_btn[3] - self.fght_btn[1]))
            self.move_curpos(self.fght_btn[0] + xrandom, self.fght_btn[1] + yrandom)
            time.sleep(0.5)
            self.click_left_cur(2)
        elif mode == '乘客':
            # 检测是否进入战斗状态
            while True:
                if not queue.empty():
                    self._running = queue.get()
                if self._running == 1:
                    catch_img = ImageGrab.grab(self.exit_btn)
                    if self.hamming(self.get_hash(catch_img), self.exit_btn_hash, 30):
                        break
                    time.sleep(0.5)
                elif self._running == 0:
                    return

    def wait_fight_finish_phase(self, mode, clear_time, queue):
        """
        等待战斗结束阶段
        :param mode: 组队模式
        :param clear_time: 平均通关时间
        :param queue: 队列对象
        :return:
        """
        if mode == '乘客':
            clear_time = clear_time - 3
        t = 0
        while t < clear_time:
            if not queue.empty():
                self._running = queue.get()
            if self._running == 1:
                time.sleep(1)
                t = t + 1
                # print(t)
            elif self._running == 0:
                break
        while True:
            if not queue.empty():
                self._running = queue.get()
            if self._running == 1:
                catch_img = ImageGrab.grab(self.exit_btn)
                # catch_img.save('fight.jpg', 'jpeg')
                # 当退出战斗按钮消失时，视为战斗结束
                if self.hamming(self.get_hash(catch_img), self.exit_btn_hash, 30):
                    pass
                else:
                    break
            elif self._running == 0:
                return
            time.sleep(0.5)

    def settle_phase(self, queue):
        """
        战斗结算阶段
        :param queue: 队列对象
        :return:
        """
        for xx in range(0, 10):
            if not queue.empty():
                self._running = queue.get()
            if self._running == 1:
                # 当镜头旋转结束，出现结算达摩，则视为进入结算界面
                catch_img = ImageGrab.grab(self.settle_area)
                # catch_img.save('%s.jpg' % xx, 'jpeg')
                if self.hamming(self.get_hash(catch_img), self.settle_area_hash, 20):
                    break
                else:
                    # 在右侧边缘范围内随机移动鼠标位置，并随机点击1-3次
                    xrandom = int(random.uniform(0, self.blank_area[2] - self.blank_area[0]))
                    yrandom = int(random.uniform(0, self.blank_area[3] - self.blank_area[1]))
                    self.move_curpos(self.blank_area[0] + xrandom, self.blank_area[1] + yrandom)
                    self.click_left_cur(int(random.uniform(1, 3)))
            elif self._running == 0:
                break
            time.sleep(0.5)
        for xx in range(0, 10):
            if not queue.empty():
                self._running = queue.get()
            if self._running == 1:
                catch_img = ImageGrab.grab(self.settle_area)
                # 当结算达摩消失时，视为结算结束
                if not self.hamming(self.get_hash(catch_img), self.settle_area_hash, 30):
                    break
                else:
                    # 在右侧边缘范围内随机移动鼠标位置，并随机点击1-3次，直到结算结束
                    xrandom = int(random.uniform(0, self.blank_area[2] - self.blank_area[0]))
                    yrandom = int(random.uniform(0, self.blank_area[3] - self.blank_area[1]))
                    self.move_curpos(self.blank_area[0] + xrandom, self.blank_area[1] + yrandom)
                    self.click_left_cur(int(random.uniform(1, 3)))
            elif self._running == 0:
                break
            time.sleep(0.5)
        # 防止判定失误再补一次点击
        xrandom = int(random.uniform(0, self.blank_area[2] - self.blank_area[0]))
        yrandom = int(random.uniform(0, self.blank_area[3] - self.blank_area[1]))
        self.move_curpos(self.blank_area[0] + xrandom, self.blank_area[1] + yrandom)
        self.click_left_cur(int(random.uniform(1, 3)))

    def check_offer(self, offer_mode, queue):
        """
        处理悬赏协助询问
        :param offer_mode: 悬赏协助处理模式
        :param queue: 队列对象
        :return:
        """
        while True:
            if not queue.empty():
                self._running = queue.get()
            if self._running == 1:
                catch_img = ImageGrab.grab(self.offer_intf)
                if self.hamming(self.get_hash(catch_img), self.offer_hash, 30):
                    if offer_mode == "接受":
                        self.move_curpos(self.accept[0], self.accept[1])
                    elif offer_mode == "拒绝":
                        self.move_curpos(self.denied[0], self.denied[1])
                    self.click_left_cur()
                time.sleep(1.3)
            elif self._running == 0:
                return
