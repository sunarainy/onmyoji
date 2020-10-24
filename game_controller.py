# -*-coding:utf-8-*-

"""
定义识别对象
对游戏不同阶段的响应动作
"""

import time
import random
import win32gui
from PIL import ImageGrab
from utilities import logging, click_left_cur, move_curpos, get_hash, hamming, get_resolution


class ResolutionGetError(Exception):
    pass


class OnmyojiObjectBase:
    def __init__(self, hwnd, scaling):
        """
        对游戏数据进行初始化
        :param
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
        self.scaling_left = self.ltrb[0]
        self.scaling_top = self.ltrb[1]
        self.scaling_width = self.width * scaling
        self.scaling_height = self.height * scaling

        self._attribute()

    def _attribute(self):
        self.click_area = None  # tuple类型
        self.button = None      # tuple类型
        self.scan_area = None   # tuple类型
        self.hash = None        # str类型
        self.hashes = None      # tuple类型

    def simple_click(self):
        """简单点击"""
        move_curpos(self.button[0][0], self.button[0][1])
        click_left_cur()

    def custom_click(self, index):
        """根据选择点击相应按钮"""
        move_curpos(self.button[index][0], self.button[index][1])
        click_left_cur()

    def area_click(self, n=1):
        """区域范围内随机点击"""
        xrandom = int(random.uniform(0, self.click_area[2] - self.click_area[0]))
        yrandom = int(random.uniform(0, self.click_area[3] - self.click_area[1]))
        move_curpos(self.click_area[0] + xrandom, self.click_area[1] + yrandom)
        time.sleep(round(random.uniform(0.5, 1.0), 2))
        click_left_cur(n)


class ExitDisplay(OnmyojiObjectBase):
    """退出按钮判定区域对象"""
    def _attribute(self):
        self.scan_area = (round(self.scaling_left + self.scaling_width * 0.014),
                          round(self.scaling_top + self.scaling_height * 0.0245),
                          round(self.scaling_left + self.scaling_width * 0.0415),
                          round(self.scaling_top + self.scaling_height * 0.074))
        self.hash = '1ff83ffc3ffe3ffe007e001f001f019f079e1ffe7fff7ffe1ff8078001800000'


class RewardDisplay(OnmyojiObjectBase):
    """奖励显示判定区域对象"""
    def _attribute(self):
        self.click_area = (round(self.left + self.width * 0.89),
                           round(self.top + self.height * 0.23),
                           round(self.left + self.width * 0.95),
                           round(self.top + self.height * 0.7))
        self.scan_area = (round(self.scaling_left + self.scaling_width * 0.42),
                          round(self.scaling_top + self.scaling_height * 0.82),
                          round(self.scaling_left + self.scaling_width * 0.58),
                          round(self.scaling_top + self.scaling_height * 0.86))
        self.hash = '4f3f672f600fa01fb03ff03ff07df874f171d170c170c970c320c020c000c000'


class BattleDataDisplay(OnmyojiObjectBase):
    """战斗数据显示判定区域对象"""
    def _attribute(self):
        self.scan_area = (round(self.scaling_left + self.scaling_width * 0.05),
                          round(self.scaling_top + self.scaling_height * 0.06),
                          round(self.scaling_left + self.scaling_width * 0.07),
                          round(self.scaling_top + self.scaling_height * 0.1))
        self.hash = '33ff3bff7b9f7ff37fffe03f8e0f1c670073003bc61bc7038003003a08723c74'


class SinglePlayerDisplay(OnmyojiObjectBase):
    """单刷判定区域对象"""
    def _attribute(self):
        self.click_area = (round(self.left + self.width * 0.85),
                           round(self.top + self.height * 0.85),
                           round(self.left + self.width * 0.94),
                           round(self.top + self.height * 0.94))
        self.scan_area = (round(self.scaling_left + self.scaling_width * 0.45),
                          round(self.scaling_top + self.scaling_height * 0.1),
                          round(self.scaling_left + self.scaling_width * 0.58),
                          round(self.scaling_top + self.scaling_height * 0.18))
        self.hash = '000000000000000000186e1836387ebc7ebc7eb86ed897fc0000ffffffffffff'


class FormTeamDisplay(OnmyojiObjectBase):
    """组队界面判定区域对象"""
    def _attribute(self):
        self.scan_area = (round(self.scaling_left + self.scaling_width * 0.07),
                          round(self.scaling_top + self.scaling_height * 0.03),
                          round(self.scaling_left + self.scaling_width * 0.18),
                          round(self.scaling_top + self.scaling_height * 0.08))
        self.hash = '000000000000479c67dc7fdc7fd877d87fdc7fdc7fdc7f5c7fdc7ffc2b380000'


class MultiplayerDisplay(OnmyojiObjectBase):
    """组队人数判定区域对象"""
    def _attribute(self):
        self.click_area = (round(self.left + self.width * 0.92),
                           round(self.top + self.height * 0.85),
                           round(self.left + self.width * 0.98),
                           round(self.top + self.height * 0.94))
        self.scan_area = (
            (round(self.scaling_left + self.scaling_width * 0.08),
             round(self.scaling_top + self.scaling_height * 0.28),
             round(self.scaling_left + self.scaling_width * 0.11),
             round(self.scaling_top + self.scaling_height * 0.38)),
            (round(self.scaling_left + self.scaling_width * 0.45),
             round(self.scaling_top + self.scaling_height * 0.5),
             round(self.scaling_left + self.scaling_width * 0.55),
             round(self.scaling_top + self.scaling_height * 0.7)),
            (round(self.scaling_left + self.scaling_width * 0.8),
             round(self.scaling_top + self.scaling_height * 0.5),
             round(self.scaling_left + self.scaling_width * 0.9),
             round(self.scaling_top + self.scaling_height * 0.7))
        )
        self.hashes = (
            '003f001fec3fec3f9b3fc13f003f243f3c3f383f363f313f007f007f807f807f',
            'fff3fff8ffffffffffff1ff707f000a0000000000000ffff0000000000000000',
            'fffffffffffffe1ff0040000efff001f000400000000ffffffff000000000000'
        )


class OfferDisplay(OnmyojiObjectBase):
    """悬赏界面判定区域对象"""
    def _attribute(self):
        self.scan_area = (round(self.scaling_left + self.scaling_width * 0.4),
                          round(self.scaling_top + self.scaling_height * 0.2),
                          round(self.scaling_left + self.scaling_width * 0.6),
                          round(self.scaling_top + self.scaling_height * 0.28))
        self.hash = 'ffffffffffff3fff35fde004200020000004040420100064247037f7ffffffff'
        self.button = (
            (round(self.left + self.width * 0.66), round(self.top + self.height * 0.6)),  # 接受按钮
            (round(self.left + self.width * 0.66), round(self.top + self.height * 0.74))  # 拒绝按钮
        )


class FullRepoDisplay(OnmyojiObjectBase):
    """满仓提示界面判定区域对象"""
    def _attribute(self):
        self.scan_area = (round(self.scaling_left + self.scaling_width * 0.35),
                          round(self.scaling_top + self.scaling_height * 0.35),
                          round(self.scaling_left + self.scaling_width * 0.65),
                          round(self.scaling_top + self.scaling_height * 0.67))
        self.hash = 'ffff0008000810960004ce7ef81ff81ffffff81ffbdffe5ffa5ff81ff81fffff'
        self.button = (
            (round(self.left + self.width * 0.5), round(self.top + self.height * 0.6)),
        )


class BossMessageisplay(OnmyojiObjectBase):
    """超鬼王提示界面判定区域对象"""
    def _attribute(self):
        self.scan_area = (round(self.scaling_left + self.scaling_width * 0.03),
                          round(self.scaling_top + self.scaling_height * 0.379),
                          round(self.scaling_left + self.scaling_width * 0.11),
                          round(self.scaling_top + self.scaling_height * 0.422))
        self.hash = [
            '031803380331033502190608074e07ff07ff07ff07ff07ff0fff0fff0fff1fff',
            '03ff03ff03bf073f07370731073107330731071107310f310f150e590fff1fff'
        ]
        self.button = (
            (round(self.left + self.width * 0.1), round(self.top + self.height * 0.37)),
        )


class GameController:
    def __init__(self, hwnd):
        """
        对游戏数据进行初始化
        :param hwnd: 游戏窗口句柄
        """
        self.debug = False

        # 获取缩放比例
        self.resolution = get_resolution()
        if not self.resolution:
            raise ResolutionGetError
        scaling = self.resolution['scaling']

        self.exitobj = ExitDisplay(hwnd, scaling)
        self.rewardobj = RewardDisplay(hwnd, scaling)
        self.battledataobj = BattleDataDisplay(hwnd, scaling)
        self.singleobj = SinglePlayerDisplay(hwnd, scaling)
        self.mutipleobj = MultiplayerDisplay(hwnd, scaling)
        self.formteamobj = FormTeamDisplay(hwnd, scaling)
        self.offerobj = OfferDisplay(hwnd, scaling)
        self.fullrepobj = FullRepoDisplay(hwnd, scaling)
        self.bossobj = BossMessageisplay(hwnd, scaling)

        # 运行状态状态初始化
        self._running = 1

    def setdebug(self, debug):
        self.debug = debug

    def form_team_phase(self, mode, player_amount, queue):
        """
        组队阶段控制方法
        :param mode: 组队模式
        :param player_amount: 车队人数
        :param queue: 队列对象
        :return:
        """
        if mode == '单刷':
            # 移动到挑战按钮并点击 每次移动在按钮范围内加入随机坐标位移
            if self.debug:
                logging('[%s]%s' % ('form_team_phase', mode))
            self.singleobj.area_click()
            return
        elif mode == '司机':
            # 检测是否进入组队界面
            while True:
                if not queue.empty():
                    self._running = queue.get()
                if self._running == 1:
                    catch_img = ImageGrab.grab(self.formteamobj.scan_area)
                    img_hash = get_hash(catch_img)
                    r1, r2 = hamming(img_hash, self.formteamobj.hash, 30)
                    if self.debug:
                        logging('[%s]%s %s:%s:%s' % ('form_team_phase1', mode, img_hash, r1, r2))
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
                        catch_img = ImageGrab.grab(self.mutipleobj.scan_area[i])
                        img_hash = get_hash(catch_img)
                        r1, r2 = hamming(img_hash, self.mutipleobj.hashes[i], 10)
                        if self.debug:
                            logging('[%s]%s 乘客%s %s:%s:%s' % ('form_team_phase2', num, mode, img_hash, r1, r2))
                        if not r1:
                            num = num + 1
                    if num == player_amount - 1:
                        break
                    time.sleep(0.5)
                elif self._running == 0:
                    return
            # 移动到开始战斗按钮并点击 每次移动在按钮范围内加入随机坐标位移
            self.mutipleobj.area_click(2)
        elif mode == '乘客':
            # 检测是否进入战斗状态
            while True:
                if not queue.empty():
                    self._running = queue.get()
                if self._running == 1:
                    catch_img = ImageGrab.grab(self.exitobj.scan_area)
                    img_hash = get_hash(catch_img)
                    r1, r2 = hamming(img_hash, self.exitobj.hash, 30)
                    if self.debug:
                        logging('[%s]%s %s:%s:%s' % ('form_team_phase', mode, img_hash, r1, r2))
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
            elif self._running == 0:
                break
        while True:
            if not queue.empty():
                self._running = queue.get()
            if self._running == 1:
                catch_img = ImageGrab.grab(self.exitobj.scan_area)
                img_hash = get_hash(catch_img)
                # 当退出战斗按钮消失时，视为战斗结束
                r1, r2 = hamming(img_hash, self.exitobj.hash, 30)
                if self.debug:
                    logging('[%s]%s %s:%s:%s' % ('wait_fight_finish_phase', mode, img_hash, r1, r2))
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
        for battle_round in range(0, 20):
            if not queue.empty():
                self._running = queue.get()
            if self._running == 1:
                # 当出现战斗数据按钮时，则视为进入结算界面
                catch_img = ImageGrab.grab(self.battledataobj.scan_area)
                img_hash = get_hash(catch_img)
                r1, r2 = hamming(img_hash, self.battledataobj.hash, 40)
                if self.debug:
                    logging('[%s]round%s %s:%s:%s' % ('settle_phase', battle_round, img_hash, r1, r2))
                if r1:
                    battle_buttun_is_appear = True
                    # 在右侧边缘范围内随机移动鼠标位置，并随机点击1-3次
                    self.rewardobj.area_click(int(random.uniform(1, 3)))
                elif not r1:
                    if battle_buttun_is_appear:
                        time.sleep(2)
                        break
                    else:
                        self.special_settle_phase()
                        break
            elif self._running == 0:
                break
            time.sleep(round(random.uniform(0.5, 1.0), 2))

    def special_settle_phase(self):
        """
        没有战斗数据按钮的结算流程
        :return:
        """
        for battle_round in range(0, 10):
            # 当镜头旋转结束，出现结算达摩，则视为进入结算界面
            catch_img = ImageGrab.grab(self.rewardobj.scan_area)
            img_hash = get_hash(catch_img)
            r1, r2 = hamming(img_hash, self.rewardobj.hash, 40)
            if self.debug:
                logging('[%s]round%s %s:%s:%s' % ('special_settle_phase1', battle_round, img_hash, r1, r2))
            if r1:
                break
            else:
                # 在右侧边缘范围内随机移动鼠标位置，并随机点击1-3次
                self.rewardobj.area_click(int(random.uniform(1, 3)))
            time.sleep(round(random.uniform(0.5, 1.0), 2))
        for battle_round in range(0, 10):
            catch_img = ImageGrab.grab(self.rewardobj.scan_area)
            img_hash = get_hash(catch_img)
            # 当结算达摩消失时，视为结算结束
            r1, r2 = hamming(img_hash, self.rewardobj.hash, 40)
            if self.debug:
                logging('[%s]round%s %s:%s:%s' % ('special_settle_phase2', battle_round, img_hash, r1, r2))
            if not r1:
                break
            else:
                # 在右侧边缘范围内随机移动鼠标位置，并随机点击1-3次，直到结算结束
                self.rewardobj.area_click(int(random.uniform(1, 3)))
            time.sleep(round(random.uniform(0.5, 1.0), 2))

    def check_offer(self, mode, queue):
        """
        处理悬赏协助询问
        :param mode: 悬赏协助处理模式  1:接受 2：拒绝
        :param queue: 队列对象
        :return:
        """
        while True:
            if not queue.empty():
                self._running = queue.get()
            if self._running == 1:
                catch_img = ImageGrab.grab(self.offerobj.scan_area)
                r1, r2 = hamming(get_hash(catch_img), self.offerobj.hash, 30)
                if r1:
                    if mode == 1:
                        self.offerobj.custom_click(0)
                    elif mode == 2:
                        self.offerobj.custom_click(1)
                    click_left_cur()
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
                catch_img = ImageGrab.grab(self.fullrepobj.scan_area)
                r1, r2 = hamming(get_hash(catch_img), self.fullrepobj.hash, 30)
                if r1:
                    self.fullrepobj.custom_click(0)
                time.sleep(1.3)
            elif self._running == 0:
                return

    def click_boss_notice(self, mode, queue):
        """
        点击发现超鬼王提示
        :param mode: 1：超鬼王模式1-仅自己发现的鬼王 2：超鬼王模式2-自己发现的鬼王或好友邀请的鬼王
        :param queue: 队列对象
        :return:
        """
        num = 1
        while True:
            if not queue.empty():
                self._running = queue.get()
            if self._running == 1:
                catch_img = ImageGrab.grab(self.bossobj.scan_area)
                img_hash = get_hash(catch_img)
                num += 1
                r1 = False
                if mode == 1:
                    r1, r2 = hamming(img_hash, self.bossobj.hash[0], 15)
                    if self.debug:
                        logging('%s boss %s:%s:%s' % (num, img_hash, r1, r2))
                elif mode == 2:
                    r11, r21 = hamming(img_hash, self.bossobj.hash[0], 15)
                    r21, r22 = hamming(img_hash, self.bossobj.hash[1], 15)
                    if r11 or r21:
                        r1 = True
                if r1:
                    queue.put(0)
                    self.bossobj.custom_click(0)
                    return
                time.sleep(1)
            elif self._running == 0:
                return
