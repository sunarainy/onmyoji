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
        self.debug = False
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
        # self.chllg_btn = (round(self.left + self.width * 0.695),
        #                   round(self.top + self.height * 0.67),
        #                   round(self.left + self.width * 0.785),
        #                   round(self.top + self.height * 0.73))
        self.chllg_btn = (round(self.left + self.width * 0.85),
                          round(self.top + self.height * 0.85),
                          round(self.left + self.width * 0.94),
                          round(self.top + self.height * 0.94))
        # 开始战斗按钮坐标
        self.fght_btn = (round(self.left + self.width * 0.92),
                         round(self.top + self.height * 0.85),
                         round(self.left + self.width * 0.98),
                         round(self.top + self.height * 0.94))
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
        # 战斗数据按钮坐标
        self.battle_data_button = (round(self.ltrb[0] + self.scaling_width * 0.05),
                                   round(self.ltrb[1] + self.scaling_height * 0.06),
                                   round(self.ltrb[0] + self.scaling_width * 0.07),
                                   round(self.ltrb[1] + self.scaling_height * 0.1))
        # 战斗数据按钮hash
        self.battle_data_button_hash = '33ff3bff7b9f7ff37fffe03f8e0f1c670073003bc61bc7038003003a08723c74'
        # 单刷界面判定采样坐标
        self.single_intf = (round(self.ltrb[0] + self.scaling_width * 0.45),
                            round(self.ltrb[1] + self.scaling_height * 0.1),
                            round(self.ltrb[0] + self.scaling_width * 0.58),
                            round(self.ltrb[1] + self.scaling_height * 0.18))
        self.single_hash = '000000000000000000186e1836387ebc7ebc7eb86ed897fc0000ffffffffffff'
        # 组队界面判定采样坐标#
        self.form_team_intf = (round(self.ltrb[0] + self.scaling_width * 0.07),
                               round(self.ltrb[1] + self.scaling_height * 0.03),
                               round(self.ltrb[0] + self.scaling_width * 0.18),
                               round(self.ltrb[1] + self.scaling_height * 0.08))
        # 组队界面判定hash
        self.form_team_hash = '000000000000479c67dc7fdc7fd877d87fdc7fdc7fdc7f5c7fdc7ffc2b380000'
        # 组队栏位1采样坐标
        self.form_team1 = (round(self.ltrb[0] + self.scaling_width * 0.08),
                           round(self.ltrb[1] + self.scaling_height * 0.28),
                           round(self.ltrb[0] + self.scaling_width * 0.11),
                           round(self.ltrb[1] + self.scaling_height * 0.38))
        # 组队栏位2采样坐标
        self.form_team2 = (round(self.ltrb[0] + self.scaling_width * 0.45),
                           round(self.ltrb[1] + self.scaling_height * 0.5),
                           round(self.ltrb[0] + self.scaling_width * 0.55),
                           round(self.ltrb[1] + self.scaling_height * 0.7))
        # 组队栏位3采样坐标
        self.form_team3 = (round(self.ltrb[0] + self.scaling_width * 0.8),
                           round(self.ltrb[1] + self.scaling_height * 0.5),
                           round(self.ltrb[0] + self.scaling_width * 0.9),
                           round(self.ltrb[1] + self.scaling_height * 0.7))
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
        self.form_team_blank_hash1 = '003f001fec3fec3f9b3fc13f003f243f3c3f383f363f313f007f007f807f807f'
        self.form_team_blank_hash2 = 'fff3fff8ffffffffffff1ff707f000a0000000000000ffff0000000000000000'
        self.form_team_blank_hash3 = 'fffffffffffffe1ff0040000efff001f000400000000ffffffff000000000000'

        self.form_team = [self.form_team1, self.form_team2, self.form_team3]
        self.form_team_blank_hash = [self.form_team_blank_hash1, self.form_team_blank_hash2, self.form_team_blank_hash3]

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

        # 满仓提示采样坐标
        self.fullrepo_intf = (round(self.ltrb[0] + self.scaling_width * 0.35),
                              round(self.ltrb[1] + self.scaling_height * 0.35),
                              round(self.ltrb[0] + self.scaling_width * 0.65),
                              round(self.ltrb[1] + self.scaling_height * 0.67))

        # 满仓提示hash
        self.fullrepo_hash = 'ffff0008000810960004ce7ef81ff81ffffff81ffbdffe5ffa5ff81ff81fffff'

        # 满仓确定按钮坐标
        self.fullrepo_confirm = (round(self.left + self.width * 0.5),
                                 round(self.top + self.height * 0.6))

        # 状态初始化
        self._running = 1

    def setdebug(self, debug):
        self.debug = debug

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
        hamming_value = sum(ch1 != ch2 for ch1, ch2 in zip(hash1, hash2))
        # print(hamming_value)
        if hamming_value <= n:
            result = True
        return result, hamming_value

    def move_curpos_test(self):
        self.move_curpos(self.fullrepo_confirm[0], self.fullrepo_confirm[1])
        catch_img = ImageGrab.grab(self.fullrepo_intf)
        catch_img.save('fullrepo_intf.jpg', 'jpeg')
        print(self.get_hash(catch_img))

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
            time.sleep(round(random.uniform(0.5, 1.0), 2))
            self.click_left_cur()
            return
        elif mode == '司机':
            # 检测是否进入组队界面
            while True:
                if not queue.empty():
                    self._running = queue.get()
                if self._running == 1:
                    catch_img = ImageGrab.grab(self.form_team_intf)
                    r1, r2 = self.hamming(self.get_hash(catch_img), self.form_team_hash, 30)
                    if self.debug:
                        print('%s:%s' % ('form_team_phase', r2))
                    if r1:
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
                    for i in range(1, 3):
                        print('inin')
                        print(self.form_team[i])
                        print(self.form_team_blank_hash[i])
                        print('in2in2')
                        catch_img = ImageGrab.grab(self.form_team[i])
                        # self.get_hash(catch_img)
                        r1, r2 = self.hamming(self.get_hash(catch_img), self.form_team_blank_hash[i], 10)
                        if self.debug:
                            print('%s:%s' % ('form_team_phase2', r2))
                        if not r1:
                            num = num + 1
                    if num == fight_num - 1:
                        break
                    time.sleep(0.5)
                elif self._running == 0:
                    return
            # 移动到开始战斗按钮并点击 每次移动在按钮范围内加入随机坐标位移
            xrandom = int(random.uniform(0, self.fght_btn[2] - self.fght_btn[0]))
            yrandom = int(random.uniform(0, self.fght_btn[3] - self.fght_btn[1]))
            self.move_curpos(self.fght_btn[0] + xrandom, self.fght_btn[1] + yrandom)
            time.sleep(round(random.uniform(0.5, 1.0), 2))
            self.click_left_cur(2)
        elif mode == '乘客':
            # 检测是否进入战斗状态
            while True:
                if not queue.empty():
                    self._running = queue.get()
                if self._running == 1:
                    catch_img = ImageGrab.grab(self.exit_btn)
                    r1, r2 = self.hamming(self.get_hash(catch_img), self.exit_btn_hash, 30)
                    if self.debug:
                        print('%s:%s' % ('form_team_phase', r2))
                    if r1:
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
                r1, r2 = self.hamming(self.get_hash(catch_img), self.exit_btn_hash, 30)
                if self.debug:
                    print('%s:%s' % ('wait_fight_finish_phase', r2))
                if r1:
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
        battle_buttun_is_appear = False
        for rounds in range(0, 20):
            if not queue.empty():
                self._running = queue.get()
            if self._running == 1:
                # 当出现战斗数据按钮时，则视为进入结算界面
                catch_img = ImageGrab.grab(self.battle_data_button)
                r1, r2 = self.hamming(self.get_hash(catch_img), self.battle_data_button_hash, 40)
                if self.debug:
                    print('%srounds%s:%s' % ('settle_phase1', rounds, r2))
                if r1:
                    battle_buttun_is_appear = True
                    # 在右侧边缘范围内随机移动鼠标位置，并随机点击1-3次
                    xrandom = int(random.uniform(0, self.blank_area[2] - self.blank_area[0]))
                    yrandom = int(random.uniform(0, self.blank_area[3] - self.blank_area[1]))
                    self.move_curpos(self.blank_area[0] + xrandom, self.blank_area[1] + yrandom)
                    self.click_left_cur(int(random.uniform(1, 3)))
                elif not r1:
                    if battle_buttun_is_appear:
                        time.sleep(0.5)
                        break
                    else:
                        catch_img = ImageGrab.grab(self.settle_area)
                        # catch_img.save('%s.jpg' % xx, 'jpeg')
                        r1, r2 = self.hamming(self.get_hash(catch_img), self.settle_area_hash, 40)
                        if self.debug:
                            print('%srounds%s:%s' % ('settle_phase1', rounds, r2))
                        if r1:
                            break
                        else:
                            # 在右侧边缘范围内随机移动鼠标位置，并随机点击1-3次
                            xrandom = int(random.uniform(0, self.blank_area[2] - self.blank_area[0]))
                            yrandom = int(random.uniform(0, self.blank_area[3] - self.blank_area[1]))
                            self.move_curpos(self.blank_area[0] + xrandom, self.blank_area[1] + yrandom)
                            self.click_left_cur(int(random.uniform(1, 3)))
            elif self._running == 0:
                break
            time.sleep(round(random.uniform(0.5, 1.0), 2))

    def settle_phase2(self, queue):
        """
        战斗结算阶段
        :param queue: 队列对象
        :return:
        """
        for rounds in range(0, 10):
            if not queue.empty():
                self._running = queue.get()
            if self._running == 1:
                # 当镜头旋转结束，出现结算达摩，则视为进入结算界面
                catch_img = ImageGrab.grab(self.settle_area)
                # catch_img.save('%s.jpg' % xx, 'jpeg')
                r1, r2 = self.hamming(self.get_hash(catch_img), self.settle_area_hash, 40)
                if self.debug:
                    print('%srounds%s:%s' % ('settle_phase1', rounds, r2))
                if r1:
                    break
                else:
                    # 在右侧边缘范围内随机移动鼠标位置，并随机点击1-3次
                    xrandom = int(random.uniform(0, self.blank_area[2] - self.blank_area[0]))
                    yrandom = int(random.uniform(0, self.blank_area[3] - self.blank_area[1]))
                    self.move_curpos(self.blank_area[0] + xrandom, self.blank_area[1] + yrandom)
                    self.click_left_cur(int(random.uniform(1, 3)))
            elif self._running == 0:
                break
            time.sleep(round(random.uniform(1, 1.5), 2))
        for rounds in range(0, 10):
            if not queue.empty():
                self._running = queue.get()
            if self._running == 1:
                catch_img = ImageGrab.grab(self.settle_area)
                # 当结算达摩消失时，视为结算结束
                r1, r2 = self.hamming(self.get_hash(catch_img), self.settle_area_hash, 40)
                if self.debug:
                    print('%srounds%s:%s' % ('settle_phase2', rounds, r2))
                if not r1:
                    break
                else:
                    # 在右侧边缘范围内随机移动鼠标位置，并随机点击1-3次，直到结算结束
                    xrandom = int(random.uniform(0, self.blank_area[2] - self.blank_area[0]))
                    yrandom = int(random.uniform(0, self.blank_area[3] - self.blank_area[1]))
                    self.move_curpos(self.blank_area[0] + xrandom, self.blank_area[1] + yrandom)
                    self.click_left_cur(int(random.uniform(1, 3)))
            elif self._running == 0:
                break
            time.sleep(round(random.uniform(0.5, 1.0), 2))

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
                r1, r2 = self.hamming(self.get_hash(catch_img), self.offer_hash, 30)
                if r1:
                    if offer_mode == "接受":
                        self.move_curpos(self.accept[0], self.accept[1])
                    elif offer_mode == "拒绝":
                        self.move_curpos(self.denied[0], self.denied[1])
                    self.click_left_cur()
                time.sleep(1.3)
            elif self._running == 0:
                return

    def check_fullrepo_alert(self, queue):
        """
        处理满仓提示
        :param queue: 队列对象
        :return:
        """
        while True:
            if not queue.empty():
                self._running = queue.get()
            if self._running == 1:
                catch_img = ImageGrab.grab(self.fullrepo_intf)
                r1, r2 = self.hamming(self.get_hash(catch_img), self.fullrepo_hash, 30)
                if r1:
                    self.move_curpos(self.fullrepo_confirm[0], self.fullrepo_confirm[1])
                    self.click_left_cur()
                time.sleep(1.3)
            elif self._running == 0:
                return
