# -*-coding:utf-8-*-

import time
import datetime
import os
import random
import shelve
import platform
import threading
from queue import Queue
import win32api, win32gui, win32con, win32com.client
from ctypes import *
from PIL import ImageGrab, Image as PLI_Image, ImageTk
from tkinter import *
from tkinter import ttk
import tkinter.messagebox as messagebox
from tkinter.scrolledtext import ScrolledText


class GameController:
    def __init__(self, hwnd, release, scaling):
        # 获取游戏窗口坐标
        self.hwnd = hwnd
        self.left, self.top, self.right, self.bottom = win32gui.GetWindowRect(self.hwnd)
        # 获取游戏画面坐标
        if release == '10':
            self.right, self.bottom = win32gui.ClientToScreen(self.hwnd,
                                                              (self.right - self.left - 17,
                                                               self.bottom - self.top - 39))  # 神奇的游戏窗口
        else:
            self.right, self.bottom = win32gui.ClientToScreen(self.hwnd,
                                                              (self.right - self.left - 17,
                                                               self.bottom - self.top - 39 - 6))
        self.left, self.top = win32gui.ClientToScreen(self.hwnd, (0, 0))
        # 缩放后的游戏窗口坐标
        self.ltrb = list(map(lambda x: x * scaling, [self.left, self.top, self.right, self.bottom]))
        self.width = self.right - self.left
        self.high = self.bottom - self.top
        self.scaling_width = self.width * scaling
        self.scaling_high = self.high * scaling
        # 挑战按钮坐标
        self.chllg_btn = (round(self.left + self.width * 0.695),
                          round(self.top + self.high * 0.67),
                          round(self.left + self.width * 0.785),
                          round(self.top + self.high * 0.73))
        # 开始战斗按钮坐标
        self.fght_btn = (round(self.left + self.width * 0.75),
                         round(self.top + self.high * 0.82),
                         round(self.left + self.width * 0.87),
                         round(self.top + self.high * 0.88))
        # 退出战斗按钮采样坐标
        self.exit_btn = (round(self.ltrb[0] + self.scaling_width * 0.014),
                         round(self.ltrb[1] + self.scaling_high * 0.0245),
                         round(self.ltrb[0] + self.scaling_width * 0.0415),
                         round(self.ltrb[1] + self.scaling_high * 0.074))
        # 退出战斗按钮hash
        self.exit_btn_hash = '1ff83ffc3ffe3ffe007e001f001f019f079e1ffe7fff7ffe1ff8078001800000'
        # 结算判定区域采样坐标
        self.settle_area = (round(self.ltrb[0] + self.scaling_width * 0.42),
                            round(self.ltrb[1] + self.scaling_high * 0.82),
                            round(self.ltrb[0] + self.scaling_width * 0.58),
                            round(self.ltrb[1] + self.scaling_high * 0.86))
        # 结算判定区域hash
        self.settle_area_hash = '4f3f672f600fa01fb03ff03ff07df874f171d170c170c970c320c020c000c000'
        # 单刷界面判定采样坐标
        self.single_intf = (round(self.ltrb[0] + self.scaling_width * 0.45),
                            round(self.ltrb[1] + self.scaling_high * 0.1),
                            round(self.ltrb[0] + self.scaling_width * 0.58),
                            round(self.ltrb[1] + self.scaling_high * 0.18))
        self.single_hash = '000000000000000000186e1836387ebc7ebc7eb86ed897fc0000ffffffffffff'
        # 组队界面判定采样坐标#
        self.form_team_intf = (round(self.ltrb[0] + self.scaling_width * 0.12),
                               round(self.ltrb[1] + self.scaling_high * 0.8),
                               round(self.ltrb[0] + self.scaling_width * 0.24),
                               round(self.ltrb[1] + self.scaling_high * 0.88))
        # 组队界面判定hash
        self.form_team_hash = '7ffeffffffffffffcd33cd33c823c923cd93c901e577ffffffff7ffe00000000'
        # 组队栏位1采样坐标
        self.form_team1 = (round(self.ltrb[0] + self.scaling_width * 0.2),
                           round(self.ltrb[1] + self.scaling_high * 0.4),
                           round(self.ltrb[0] + self.scaling_width * 0.28),
                           round(self.ltrb[1] + self.scaling_high * 0.53))
        # 组队栏位2采样坐标
        self.form_team2 = (round(self.ltrb[0] + self.scaling_width * 0.46),
                           round(self.ltrb[1] + self.scaling_high * 0.4),
                           round(self.ltrb[0] + self.scaling_width * 0.54),
                           round(self.ltrb[1] + self.scaling_high * 0.53))
        # 组队栏位3采样坐标
        self.form_team3 = (round(self.ltrb[0] + self.scaling_width * 0.76),
                           round(self.ltrb[1] + self.scaling_high * 0.4),
                           round(self.ltrb[0] + self.scaling_width * 0.84),
                           round(self.ltrb[1] + self.scaling_high * 0.53))
        # 点击屏幕继续字样采样坐标
        self.notice_area = (round(self.ltrb[2] * 0.40),
                            round(self.ltrb[3] * 0.90),
                            round(self.ltrb[2] * 0.60),
                            round(self.ltrb[3] * 0.97))
        # 结算点击区域坐标
        self.blank_area = (round(self.left + self.width * 0.86),
                           round(self.top + self.high * 0.23),
                           round(self.left + self.width * 0.95),
                           round(self.top + self.high * 0.7))
        # 组队栏位为空时hash
        self.form_team_blank_hash = 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff'

        self._running = 1

    @staticmethod
    def click_left_cur(counts=1):
        for o in range(counts):
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
            time.sleep(0.1)

    @staticmethod
    def click_right_cur():
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP | win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)

    @staticmethod
    def move_curpos(x, y):
        windll.user32.SetCursorPos(x, y)

    @staticmethod
    def get_curpos():
        return win32gui.GetCursorPos()

    @staticmethod
    def get_hash(img):
        img = img.resize((16, 16), PLI_Image.ANTIALIAS).convert('L')
        avg = sum(list(img.getdata())) / 256  # 计算像素平均值
        s = ''.join(map(lambda x: '0' if x < avg else '1', img.getdata()))  # 每个像素进行比对,大于avg为1,反之为0
        return ''.join(map(lambda j: '%x' % int(s[j:j + 4], 2), range(0, 256, 4)))

    @staticmethod
    def hamming(hash1, hash2, n=20):
        result = False
        assert len(hash1) == len(hash2)
        # print(sum(ch1 != ch2 for ch1, ch2 in zip(hash1, hash2)))
        if sum(ch1 != ch2 for ch1, ch2 in zip(hash1, hash2)) <= n:
            result = True
        return result

    def form_team_phase(self, mode, fight_num, queue):
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
            self.click_left_cur()
        elif mode == '乘客':
            return

    def wait_fight_finish_phase(self, clear_time, queue):
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
                if not self.hamming(self.get_hash(catch_img), self.settle_area_hash, 20):
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


class Application(Frame):
    def __init__(self, master=None):
        self.warning = '【封号防止】\n' + \
                       '请尽量在自己的日常刷魂时间使用\n' + \
                       '请不要长时间连续使用，任何使你看起来明显违背人类正常作息规律的行为，很容易会被鬼使黑盯上\n' + \
                       '当你离开了常在城市，请不要使用，这会被认为是找了代练\n' + \
                       '点到为止，贪婪是万恶之源\n'
        self.label = r'阴阳师-网易游戏'
        # self.label = r'Foxmail'
        self.hwnd = self.check_hwnd(self.label)
        if not self.hwnd:
            messagebox.showinfo(title='提示', message='游戏没有运行')
            quit()
        self.shell = win32com.client.Dispatch("WScript.Shell")
        # self.shell.SendKeys('%')

        # 获取操作系统版本
        self.release = platform.platform().split('-')[1]
        if not self.info_get():
            self.scaling = 1
            self.clear_time = 35
        self.fight = None

        # 控件初始化
        Frame.__init__(self, master)
        self.pack()
        self.frame1 = Frame(self)
        self.frame1.pack()
        self.frame2 = Frame(self)
        self.frame2.pack()

        self.label_scaling = Label(self.frame1)
        self.var_scaling = StringVar(self.frame1)
        self.entry_scaling = Entry(self.frame1)

        self.button_scaling_explain = Button(self.frame1)

        self.label_mode = Label(self.frame1)
        self.var_mode = StringVar(self.frame1)
        self.listbox_mode = ttk.Combobox(self.frame1)

        self.button_mode_explain = Button(self.frame1)

        self.label_member = Label(self.frame1)
        self.var_member = IntVar()
        self.radio1 = Radiobutton(self.frame1)
        self.radio2 = Radiobutton(self.frame1)

        self.label_clear_time = Label(self.frame1)
        self.var_clear_time = StringVar(self.frame1)
        self.entry_clear_time = Entry(self.frame1)

        self.button_clear_time_explain = Button(self.frame1)

        self.entry_test = Entry(self.frame1)
        self.test_btn = Button(self.frame1)

        self.start_ctn = Button(self.frame2)
        self.stop_ctn = Button(self.frame2)

        self.info_box = ScrolledText(self.frame2)

        self.queue = Queue(maxsize=1)
        self._running = True
        self.create_main()

    @staticmethod
    def check_hwnd(label):
        # 获取游戏窗口句柄
        hwnd = win32gui.FindWindow(None, label)
        if hwnd:
            return hwnd
        else:
            print('游戏没有运行')
            return False

    @staticmethod
    def init_window_place(root, x, y):
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        root.resizable(False, False)
        root.update_idletasks()
        root.deiconify()
        width = root.winfo_width()
        height = root.winfo_height()
        size = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / x, (screenheight - height) / y)
        root.geometry(size)

    def jump_window(self):
        # 跳转到游戏窗口
        win32gui.SetForegroundWindow(self.hwnd)
        win32gui.PostMessage(self.hwnd, win32con.WM_SYSCOMMAND, win32con.SC_RESTORE, 0)

    def get_scaling(self):
        var = self.entry_scaling.get()
        try:
            var = float(var)
        except ValueError:
            messagebox.showinfo(title='提示', message='缩放倍率只能为数字')
            return False
        if var > 2:
            messagebox.showinfo(title='提示', message='缩放倍率过高')
            return False
        return var

    def get_clear_time(self):
        var = self.var_clear_time.get()
        try:
            var = float(var)
        except ValueError:
            messagebox.showinfo(title='提示', message='平均通关时间只能为数字')
            return False
        if var <= 5:
            messagebox.showinfo(title='提示', message='平均通关时间不能小于5')
            return False
        return var

    @staticmethod
    def time_format(second):
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

    def info_get(self):
        try:
            with shelve.open('mysetting.db') as data:
                setting_data = data['setting']
                self.scaling = setting_data['scaling']
                self.clear_time = setting_data['clear_time']
        except KeyError:
            return False
        return True

    def info_save(self):
        with shelve.open('mysetting.db') as data:
            setting_data = dict()
            setting_data['scaling'] = self.var_scaling.get()
            setting_data['clear_time'] = self.var_clear_time.get()
            data['setting'] = setting_data

    def turn_radio_on(self, *args):
        type(args)
        var = self.listbox_mode.get()
        if var == '司机':
            self.radio1.configure(state='active')
            self.radio2.configure(state='active')
        else:
            self.radio1.configure(state='disabled')
            self.radio2.configure(state='disabled')

    def fight_start(self):
        self.scaling = self.get_scaling()
        if not self.scaling:
            return False
        self.clear_time = self.get_clear_time()
        if not self.clear_time:
            return False
        self.info_save()
        self.fight = GameController(self.hwnd, self.release, self.scaling)
        thread1 = threading.Thread(target=self.fight_thread, name='fight_thread')
        # 将线程状态、队列内容置为1
        self._running = True
        if self.queue.empty():
            self.queue.put(1)
        else:
            self.queue.get()
            self.queue.put(1)
        self.start_ctn.configure(state='disabled')
        self.stop_ctn.configure(state='active')
        thread1.start()

    def fight_thread(self):
        self.jump_window()
        if not self.queue.empty():
            self.queue.get()
        self.info_box.mark_set('insert', END)
        self.info_box.insert('insert', str(self.warning) + '\n', 'RED')
        self.info_box.tag_config('RED', foreground='red')
        var = '[%s]挂机开始' % datetime.datetime.now().strftime("%H:%M:%S")
        self.info_box.mark_set('insert', END)
        self.info_box.insert('insert', str(var) + '\n')
        self.info_box.see(END)
        rounds = 0
        total_time = 0
        while True:
            if self._running == 1:
                fight_start_time = time.clock()
                self.fight.form_team_phase(self.listbox_mode.get(), self.var_member.get(), self.queue)
                self.fight.wait_fight_finish_phase(self.clear_time, self.queue)
                self.jump_window()
                self.fight.settle_phase(self.queue)
                if self._running == 1:
                    fight_end_time = time.clock()
                    fight_time = fight_end_time - fight_start_time
                    # time.sleep(0.5)
                    rounds = rounds + 1
                    total_time = total_time + fight_time
                    var = '第 %s 场 耗时：%s 共计：%s' % \
                          (rounds, self.time_format(fight_time), self.time_format(total_time))
                    self.info_box.mark_set('insert', END)
                    self.info_box.insert('insert', str(var) + '\n')
                    self.info_box.see(END)
                    time.sleep(random.uniform(1, 2))
            elif self._running == 0:
                return

    def fight_stop(self):
        # 将线程状态、队列内容置为0
        self._running = False
        self.queue.put(0)
        self.start_ctn.configure(state='active')
        self.stop_ctn.configure(state='disabled')
        var = '[%s]挂机结束。记得关御魂buff' % datetime.datetime.now().strftime("%H:%M:%S")
        self.info_box.mark_set('insert', END)
        self.info_box.insert('insert', str(var) + '\n')
        self.info_box.see(END)

    @staticmethod
    def resource_path(relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)

    def what_is_scaling_window(self):
        what_is_scaling = Toplevel(self)
        what_is_scaling.title('缩放倍率 - 不能自动获取，技术就是这么菜，不服憋着_(:3」∠)_')

        frame1 = Frame(what_is_scaling)
        frame1.pack()
        frame2 = Frame(what_is_scaling)
        frame2.pack()

        title = Label(frame1)
        title['text'] = '\n【 缩放倍率 】'
        title.pack()
        desc1 = Message(frame1)
        desc1['width'] = 600
        desc1['text'] = '\n缩放倍率是指Windows系统在不改变分辨率的情况下，将窗口和图标放大以达到更加舒适的显示效果的功能\n' + \
                        '\n在某些分辨率下，Windows会自动设置一个超过100%的倍率。请确定自己系统当前的缩放倍率设置，并填入缩放倍率一栏中\n' + \
                        '\n不正确的缩放倍率设置，会导致坐标计算不准\n' + \
                        '\n若设置的缩放倍率是100%，则填入1，若是125%，则填1.25，依次类推\n'
        desc1.pack()

        label_win10 = Label(frame2)
        label_win10['text'] = 'Windows 10'
        label_win10.grid(row=0, column=0)

        label_win7 = Label(frame2)
        label_win7['text'] = 'Windows 7'
        label_win7.grid(row=0, column=1)

        ipath = self.resource_path('image/win10.png')
        load = PLI_Image.open(ipath)
        load = load.resize(tuple(map(lambda x: int(x * 0.5), load.size)))
        render = ImageTk.PhotoImage(load)
        img_win10 = Label(frame2, image=render)
        img_win10.image = render
        img_win10.grid(row=1, column=0)

        ipath = self.resource_path('image/win7.png')
        load = PLI_Image.open(ipath)
        load = load.resize(tuple(map(lambda x: int(x * 0.5), load.size)))
        render = ImageTk.PhotoImage(load)
        img_win7 = Label(frame2, image=render)
        img_win7.image = render
        img_win7.grid(row=1, column=1)

        self.init_window_place(what_is_scaling, 1.3, 3)

    def when_click_start_window(self):
        when_click_start = Toplevel(self)
        when_click_start.title('模式说明')

        var = self.listbox_mode.get()
        if var == '单刷':
            title = Label(when_click_start)
            title['text'] = '\n【 单刷模式 】'
            title.pack()
            desc = Message(when_click_start)
            desc['text'] = '\n请把游戏调整至如图所示界面，再点START\n'
            desc['width'] = 300
            desc.pack()

            ipath = self.resource_path('image/single.png')
            load = PLI_Image.open(ipath)
            load = load.resize(tuple(map(lambda x: int(x * 0.7), load.size)))
            render = ImageTk.PhotoImage(load)
            img = Label(when_click_start, image=render)
            img.image = render
            img.pack()
        elif var == '乘客':
            title = Label(when_click_start)
            title['text'] = '\n【 乘客模式 】'
            title.pack()
            desc = Message(when_click_start)
            desc['text'] = '\n建议接受了司机的默认邀请，再点START\n' + \
                           '因为我不会在战斗里帮你点开始...不服憋着\n_(:3」∠)_\n'
            desc['width'] = 300
            desc.pack()

            ipath = self.resource_path('image/passenger_accept.png')
            load = PLI_Image.open(ipath)
            load = load.resize(tuple(map(lambda x: int(x * 0.7), load.size)))
            render = ImageTk.PhotoImage(load)
            img = Label(when_click_start, image=render)
            img.image = render
            img.pack()
        elif var == '司机':
            title = Label(when_click_start)
            title['text'] = '\n【 司机模式 】'
            title.pack()
            desc = Message(when_click_start)
            desc['text'] = '\n建议对乘客发出默认邀请，回到组队界面再点START\n' + \
                           '因为自动发出邀请这个功能没写...不服憋着\n_(:3」∠)_\n'
            desc['width'] = 300
            desc.pack()

            ipath = self.resource_path('image/driver_invite.png')
            load = PLI_Image.open(ipath)
            load = load.resize(tuple(map(lambda x: int(x * 0.5), load.size)))
            render = ImageTk.PhotoImage(load)
            img1 = Label(when_click_start, image=render)
            img1.image = render
            img1.pack()

            ipath = self.resource_path('image/driver_form.png')
            load = PLI_Image.open(ipath)
            load = load.resize(tuple(map(lambda x: int(x * 0.5), load.size)))
            render = ImageTk.PhotoImage(load)
            img2 = Label(when_click_start, image=render)
            img2.image = render
            img2.pack()

        self.init_window_place(when_click_start, 1.3, 3)

    def what_is_clear_time(self):
        what_is_clear = Toplevel(self)
        what_is_clear.title('平均通关时间说明')

        title = Label(what_is_clear)
        title['text'] = '\n【 平均通关时间 】'
        title.pack()
        desc = Message(what_is_clear)
        desc['text'] = '\n平均通关时间是指在游戏中，从按下开始战斗到进入结算奖励界面所经过的时间(秒)\n' + \
                       '\n程序会在经过指定的时间后，再开始检测游戏画面是否进入了结算界面\n' + \
                       '\n如果设置一个较短的时间也可以，不过设置一个合理的时间，能节省你CPU资源\n（其实也没占多少_(:3」∠)_\n'
        desc['width'] = 300
        desc.pack()
        self.init_window_place(what_is_clear, 1.3, 3)

    def create_main(self):
        self.label_scaling['text'] = '缩放倍率'
        self.var_scaling.set(self.scaling)
        self.entry_scaling['textvariable'] = self.var_scaling
        self.label_scaling.grid(row=0, column=0, sticky='E')
        self.entry_scaling.grid(row=0, column=1, sticky='W', columnspan=2)

        self.button_scaling_explain['text'] = '?'
        self.button_scaling_explain['command'] = self.what_is_scaling_window
        self.button_scaling_explain['relief'] = 'flat'
        self.button_scaling_explain.grid(row=0, column=2, sticky='E')

        self.label_mode['text'] = '模式'
        self.var_mode.set('单刷')
        self.listbox_mode['textvariable'] = self.var_mode
        self.listbox_mode['width'] = 10
        self.listbox_mode['values'] = ["单刷", "乘客", "司机"]
        self.listbox_mode.bind("<<ComboboxSelected>>", self.turn_radio_on)
        self.label_mode.grid(row=1, column=0, sticky='E')
        self.listbox_mode.grid(row=1, column=1, sticky='W')

        self.button_mode_explain['text'] = '?'
        self.button_mode_explain['command'] = self.when_click_start_window
        self.button_mode_explain['relief'] = 'flat'
        self.button_mode_explain.grid(row=1, column=2, sticky='W')

        self.var_member.set(2)
        self.label_member['text'] = '车队人数'
        self.label_member.grid(row=2, column=0, sticky='E')
        self.radio1['text'] = '2人'
        self.radio1['variable'] = self.var_member
        self.radio1['value'] = 2
        # self.radio1['command'] = self.test_val3
        self.radio1.grid(row=2, column=1, sticky='W')
        self.radio1.configure(state='disabled')

        self.radio2['text'] = '3人'
        self.radio2['variable'] = self.var_member
        self.radio2['value'] = 3
        # self.radio2['command'] = self.test_val3
        self.radio2.grid(row=2, column=2, sticky='W')
        self.radio2.configure(state='disabled')

        self.label_clear_time['text'] = '平均通关时间'
        self.var_clear_time.set(self.clear_time)
        self.entry_clear_time['textvariable'] = self.var_clear_time
        self.label_clear_time.grid(row=3, column=0, sticky='E')
        self.entry_clear_time.grid(row=3, column=1, sticky='W', columnspan=2)

        self.button_clear_time_explain['text'] = '?'
        self.button_clear_time_explain['command'] = self.what_is_clear_time
        self.button_clear_time_explain['relief'] = 'flat'
        self.button_clear_time_explain.grid(row=3, column=2, sticky='E')

        self.start_ctn['text'] = 'START'
        self.start_ctn['width'] = 10
        self.start_ctn['height'] = 2
        self.start_ctn['command'] = self.fight_start
        self.start_ctn['relief'] = 'groove'
        self.start_ctn.grid(row=0, column=0, sticky='E')

        self.stop_ctn['text'] = 'STOP'
        self.stop_ctn['width'] = 10
        self.stop_ctn['height'] = 2
        self.stop_ctn['command'] = self.fight_stop
        self.stop_ctn['relief'] = 'groove'
        self.stop_ctn.grid(row=0, column=1, sticky='W')
        self.stop_ctn.configure(state='disabled')

        self.info_box['width'] = 40
        self.info_box['height'] = 20
        self.info_box.grid(row=1, column=0, columnspan=2)
        self.info_box.see(END)
        var = '请授予此程序管理员权限运行，否则在游戏窗口内鼠标无法被控制'
        self.info_box.mark_set('insert', END)
        self.info_box.insert('insert', str(var) + '\n')
        self.info_box.see(END)


app = Application()
app.master.title('就你破势多')
app.init_window_place(app.master, 1.1, 4)
app.mainloop()
