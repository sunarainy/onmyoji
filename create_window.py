# -*-coding:utf-8-*-

"""
创建windows界面
响应各控件功能
"""

import time
import random
import shelve
import threading
from queue import Queue
import win32gui
import win32con
import ctypes
# import win32com.client
import ctypes.wintypes
import psutil
import win32process
from PIL import Image as PLI_Image, ImageTk
from tkinter import *
from tkinter import ttk
import tkinter.messagebox as messagebox
from tkinter.scrolledtext import ScrolledText
from game_controller import GameController
from utilities import *


class Application(Frame):
    def __init__(self, master=None):
        """
        控件初始化
        :param master:
        """
        self.debug = False
        self.warning = '【封号防止】\n' + \
                       '请尽量在自己的日常刷魂时间使用\n' + \
                       '请不要长时间连续使用，任何使你看起来明显违背人类正常作息规律的行为，很容易会被鬼使黑盯上\n' + \
                       '当你离开了常在城市，请不要使用，这会被认为是找了代练\n' + \
                       '点到为止，贪婪是万恶之源\n'
        self.label = r'阴阳师-网易游戏'
        self.hwnd = None
        self.shell = None
        if not self.info_get():
            self.scaling = 1
            self.clear_time = 35
            self.delay_time = 1
        self.fight = None
        self.timing_value = None

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

        self.label_delay_time = Label(self.frame1)
        self.var_delay_time = StringVar(self.frame1)
        self.entry_delay_time = Entry(self.frame1)

        self.button_delay_time_explain = Button(self.frame1)

        self.label_offer = Label(self.frame1)
        self.var_offer_mode = StringVar(self.frame1)
        self.listbox_offer_mode = ttk.Combobox(self.frame1)

        self.label_timing_mode = Label(self.frame1)
        self.var_timing_mode = StringVar(self.frame1)
        self.listbox_timing_mode = ttk.Combobox(self.frame1)

        self.var_timing_value = StringVar(self.frame1)
        self.entry_timing_value = Entry(self.frame1)

        self.label_done_action_mode = Label(self.frame1)
        self.var_done_action_mode = StringVar(self.frame1)
        self.listbox_done_action_mode = ttk.Combobox(self.frame1)

        self.entry_test = Entry(self.frame1)
        self.test_btn = Button(self.frame1)

        self.start_ctn = Button(self.frame2)
        self.stop_ctn = Button(self.frame2)

        self.info_box = ScrolledText(self.frame2)

        self.queue = Queue(maxsize=1)
        self._running = 0
        self.create_main()

        hot_key = threading.Thread(target=self.hotkey_thread, name='hotkey_thread')
        hot_key.setDaemon(True)
        hot_key.start()

    def setdebug(self, debug):
        self.debug = debug

    @staticmethod
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

    # @staticmethod
    def check_hwnd(self, label):
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
        if len(self.get_hwnds(p)) > 0:
            hwnd = self.get_hwnds(p)[0]
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

    @staticmethod
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

    def jump_window(self):
        """
        使游戏窗口到最顶层
        :return:
        """
        win32gui.SetForegroundWindow(self.hwnd)
        win32gui.PostMessage(self.hwnd, win32con.WM_SYSCOMMAND, win32con.SC_RESTORE, 0)

    def get_scaling(self):
        """
        校验windows缩放倍率输入值
        :return: 校验通过则返回浮点型数字，否则返回False
        """
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
        """
        校验平均通关时间输入值
        :return: 校验通过则返回浮点型数字，否则返回False
        """
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

    def get_delay_time(self):
        """
        校验平均通关时间输入值
        :return: 校验通过则返回浮点型数字，否则返回False
        """
        var = self.var_delay_time.get()
        try:
            var = float(var)
        except ValueError:
            messagebox.showinfo(title='提示', message='战斗后等待时间只能为数字')
            return False
        if var <= 0:
            messagebox.showinfo(title='提示', message='战斗后等待时间不能小于0')
            return False
        return var

    def get_timimg(self):
        """
        校验预定结束输入值
        :return: 校验通过则返回浮点型数字，否则返回False
        """
        if self.listbox_timing_mode.get() == '无' or \
           self.listbox_timing_mode.get() == '超鬼王模式1' or \
           self.listbox_timing_mode.get() == '超鬼王模式2':
            return True
        var = self.var_timing_value.get()
        try:
            var = float(var)
        except ValueError:
            messagebox.showinfo(title='提示', message='预定结束只能填入数字')
            return False
        if var < 1:
            messagebox.showinfo(title='提示', message='数字过小，无法执行')
            return False
        return var

    @staticmethod
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

    def info_get(self):
        """
        读取存储文件
        :return:
        """
        try:
            with shelve.open('mysetting.db') as data:
                setting_data = data['setting']
                self.scaling = setting_data['scaling']
                self.clear_time = setting_data['clear_time']
                self.delay_time = setting_data['delay_time']
        except KeyError:
            return False
        return True

    def info_save(self):
        """
        存储设置
        :return:
        """
        with shelve.open('mysetting.db') as data:
            setting_data = dict()
            setting_data['scaling'] = self.var_scaling.get()
            setting_data['clear_time'] = self.var_clear_time.get()
            setting_data['delay_time'] = self.var_delay_time.get()
            data['setting'] = setting_data

    def turn_radio_on(self, *args):
        """
        根据条件激活相应控件
        :param args:
        :return:
        """
        type(args)
        var = self.listbox_mode.get()
        if var == '司机':
            self.radio1.configure(state='active')
            self.radio2.configure(state='active')
        else:
            self.radio1.configure(state='disabled')
            self.radio2.configure(state='disabled')

    def turn_entry_on(self, *args):
        """
        根据条件激活相应控件
        :param args:
        :return:
        """
        type(args)
        var = self.listbox_timing_mode.get()
        if var == '定时[分钟]' or var == '场数':
            self.entry_timing_value.configure(state='normal')
            self.listbox_done_action_mode.configure(state='normal')
            self.var_done_action_mode.set('关闭游戏窗口')
        elif var == '超鬼王模式1':
            self.entry_timing_value.configure(state='disabled')
            self.listbox_done_action_mode.configure(state='normal')
            self.var_done_action_mode.set('仅停止挂机')
            content = '\n超鬼王模式1：\n仅自己发现的鬼王\n'
            self.info_box.mark_set('insert', END)
            self.info_box.insert('insert', str(content) + '\n')
            self.info_box.see(END)
        elif var == '超鬼王模式2':
            self.entry_timing_value.configure(state='disabled')
            self.listbox_done_action_mode.configure(state='normal')
            self.var_done_action_mode.set('仅停止挂机')
            content = '\n超鬼王模式2：\n自己发现的鬼王或好友邀请的鬼王\n'
            self.info_box.mark_set('insert', END)
            self.info_box.insert('insert', str(content) + '\n')
            self.info_box.see(END)
        else:
            self.entry_timing_value.configure(state='disabled')
            self.var_done_action_mode.set('')
            self.listbox_done_action_mode.configure(state='disabled')

    def turn_all_widget_off(self):
        self.entry_scaling.configure(state='disabled')
        self.entry_clear_time.configure(state='disabled')
        self.entry_delay_time.configure(state='disabled')
        self.entry_timing_value.configure(state='disabled')
        self.listbox_mode.configure(state='disabled')
        self.listbox_offer_mode.configure(state='disabled')
        self.listbox_timing_mode.configure(state='disabled')
        self.listbox_done_action_mode.configure(state='disabled')

    def turn_all_widget_on(self):
        self.entry_scaling.configure(state='normal')
        self.entry_clear_time.configure(state='normal')
        self.entry_delay_time.configure(state='normal')
        self.entry_timing_value.configure(state='normal')
        self.listbox_mode.configure(state='normal')
        self.listbox_offer_mode.configure(state='normal')
        self.listbox_timing_mode.configure(state='normal')
        self.listbox_done_action_mode.configure(state='normal')

    def fight_start(self):
        """
        START按钮响应流程
        :return:
        """
        self.scaling = self.get_scaling()
        if not self.scaling:
            return False
        self.clear_time = self.get_clear_time()
        if not self.clear_time:
            return False
        self.delay_time = self.get_delay_time()
        if not self.delay_time:
            return False
        self.timing_value = self.get_timimg()
        if not self.timing_value:
            return False
        self.info_save()

        # 获取游戏窗口句柄
        self.hwnd = self.check_hwnd(self.label)
        if not self.hwnd:
            messagebox.showinfo(title='提示', message='游戏没有运行')
            return False
        # self.shell = win32com.client.Dispatch("WScript.Shell")
        # self.shell.SendKeys('%')

        self.jump_window()
        time.sleep(0.5)
        self.fight = GameController(self.hwnd, self.scaling)
        if self.debug:
            self.fight.setdebug(True)
        threads = []
        thread1 = threading.Thread(target=self.fight_thread, name='fight_thread')
        threads.append(thread1)
        thread2 = threading.Thread(target=self.offer_thread, name='offer_thread')
        threads.append(thread2)
        thread3 = threading.Thread(target=self.fullrepo_thread, name='fullrepo_thread')
        threads.append(thread3)
        if self.listbox_timing_mode.get() == '超鬼王模式1' or self.listbox_timing_mode.get() == '超鬼王模式2':
            thread4 = threading.Thread(target=self.boss_monitoring_thread, name='boss_thread')
            threads.append(thread4)
        # 将线程状态、队列内容置为1
        self._running = 1
        if self.queue.empty():
            self.queue.put(1)
        else:
            self.queue.get()
            self.queue.put(1)
        self.start_ctn.configure(state='disabled')
        self.stop_ctn.configure(state='active')
        for thread in threads:
            thread.setDaemon(True)
            thread.start()

    def fight_stop(self):
        """
        STOP按钮响应流程
        :return:
        """
        # 将线程状态、队列内容置为0
        self._running = 0
        self.queue.put(0)
        self.start_ctn.configure(state='active')
        self.stop_ctn.configure(state='disabled')
        self.turn_all_widget_on()
        var = '[%s]挂机结束。记得关御魂buff' % datetime.datetime.now().strftime("%H:%M:%S")
        self.info_box.mark_set('insert', END)
        self.info_box.insert('insert', str(var) + '\n')
        self.info_box.see(END)
        if self.debug:
            logging('STOP指令-----------------')
        if len(sys.argv) == 1 or (len(sys.argv) > 1 and sys.argv[1] != 'debug'):
            self.setdebug(False)

    def fight_thread(self):
        """
        战斗控制线程，并输出相关信息
        :return:
        """
        self.jump_window()
        if not self.queue.empty():
            self.queue.get()
        self.info_box.mark_set('insert', END)
        self.info_box.insert('insert', str(self.warning) + '\n', 'RED')
        self.info_box.tag_config('RED', foreground='red')
        var = '[%s]挂机开始。按Ctrl + F1可以停止挂机' % datetime.datetime.now().strftime("%H:%M:%S")
        if self.debug:
            var = var + '\n当前以debug模式运行，在当前目录下将生成debug.log'
        self.turn_all_widget_off()
        self.info_box.mark_set('insert', END)
        self.info_box.insert('insert', str(var) + '\n')
        self.info_box.see(END)
        rounds = 0
        total_time = 0
        beginning_time = int(time.time())
        while True:
            if self._running == 1:
                fight_start_time = time.time()
                self.fight.form_team_phase(self.listbox_mode.get(), self.var_member.get(), self.queue)
                self.fight.wait_fight_finish_phase(self.listbox_mode.get(), self.clear_time, self.queue)
                self.jump_window()
                self.fight.settle_phase(self.queue)
                if self._running == 1:
                    fight_end_time = int(time.time())
                    fight_time = fight_end_time - fight_start_time
                    rounds = rounds + 1
                    total_time = total_time + fight_time
                    elapsed_time = fight_end_time - beginning_time
                    var = '第 %s 场 耗时：%s 共计：%s' % \
                          (rounds, self.time_format(fight_time), self.time_format(elapsed_time))
                    self.info_box.mark_set('insert', END)
                    self.info_box.insert('insert', str(var) + '\n')
                    self.info_box.see(END)
                    if self.debug:
                        logging('------------------------')
                    # 检查是否到达预定结束场数或时间
                    if (self.listbox_timing_mode.get() == '场数' and rounds >= self.timing_value) or \
                       (self.listbox_timing_mode.get() == '定时[分钟]' and elapsed_time / 60 >= self.timing_value):
                        if self.listbox_done_action_mode.get() == '关闭游戏窗口':
                            win32gui.PostMessage(self.hwnd, win32con.WM_CLOSE, 0, 0)
                            time.sleep(1)
                            lebel_exit = '退出游戏'
                            hwnd_exit = self.check_hwnd(lebel_exit)
                            win32gui.PostMessage(hwnd_exit, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
                            win32gui.PostMessage(hwnd_exit, win32con.WM_KEYUP, win32con.VK_RETURN, 0)
                            var = '已到达预定目标，游戏窗口已关闭。下线15分钟后buff自动关闭'
                        elif self.listbox_done_action_mode.get() == '仅停止挂机':
                            var = '已到达预定目标，挂机已停止。'
                        self.fight_stop()
                        self.info_box.mark_set('insert', END)
                        self.info_box.insert('insert', str(var) + '\n')
                        self.info_box.see(END)
                    random.uniform(1, 2)
                    delay_time = int(self.delay_time) + random.uniform(0.2, 0.5)
                    time.sleep(delay_time)
            elif self._running == 0:
                return

    def offer_thread(self):
        """
        悬赏协助控制线程
        :return:
        """
        while True:
            if self._running == 1:
                self.fight.check_offer(self.listbox_offer_mode.get(), self.queue)
            elif self._running == 0:
                return

    def fullrepo_thread(self):
        """
        点击满仓提示控制线程
        :return:
        """
        while True:
            if self._running == 1:
                self.fight.check_fullrepo_alert(self.queue)
            elif self._running == 0:
                return

    def hotkey_thread(self):
        """
        快捷键监听线程
        :return:
        """
        user32 = ctypes.windll.user32
        byref = ctypes.byref
        user32.RegisterHotKey(None, 10001, win32con.MOD_CONTROL, win32con.VK_F1)
        user32.RegisterHotKey(None, 10002, win32con.MOD_CONTROL, win32con.VK_F2)

        try:
            msg = ctypes.wintypes.MSG()
            while user32.GetMessageA(byref(msg), None, 0, 0) != 0:
                if msg.message == win32con.WM_HOTKEY:
                    if self._running == 1 and msg.wParam == 10001:
                        self.fight_stop()
                    elif self._running == 0 and msg.wParam == 10002:
                        self.setdebug(True)
                        self.fight_start()
                user32.TranslateMessage(byref(msg))
                user32.DispatchMessageA(byref(msg))
        finally:
            user32.UnregisterHotKey(None, 10001)
            user32.UnregisterHotKey(None, 10002)

    def boss_monitoring_thread(self):
        """
        点击发现超鬼王提示控制线程
        :return: 
        """""
        mode = None
        if self.listbox_timing_mode.get() == '超鬼王模式1':
            mode = 1
        elif self.listbox_timing_mode.get() == '超鬼王模式2':
            mode = 2
        logging('mode:%s' % mode)
        while True:
            if self._running == 1:
                self.fight.click_boss_notice(mode, self.queue)
                self.fight_stop()
                time.sleep(3)
                audio_play()
                messagebox.showinfo('就你鬼王多', '发现超鬼王啦！还不快冲鸭！')
                audio_stop()
                return
            elif self._running == 0:
                return

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

        ipath = resource_path('image/win10.png')
        load = PLI_Image.open(ipath)
        load = load.resize(tuple(map(lambda x: int(x * 0.5), load.size)))
        render = ImageTk.PhotoImage(load)
        img_win10 = Label(frame2, image=render)
        img_win10.image = render
        img_win10.grid(row=1, column=0)

        ipath = resource_path('image/win7.png')
        load = PLI_Image.open(ipath)
        load = load.resize(tuple(map(lambda x: int(x * 0.5), load.size)))
        render = ImageTk.PhotoImage(load)
        img_win7 = Label(frame2, image=render)
        img_win7.image = render
        img_win7.grid(row=1, column=1)

        self.init_window_position(what_is_scaling, 1.3, 3)

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

            ipath = resource_path('image/single.png')
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

            ipath = resource_path('image/passenger_accept.png')
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

            ipath = resource_path('image/driver_invite.png')
            load = PLI_Image.open(ipath)
            load = load.resize(tuple(map(lambda x: int(x * 0.5), load.size)))
            render = ImageTk.PhotoImage(load)
            img1 = Label(when_click_start, image=render)
            img1.image = render
            img1.pack()

            ipath = resource_path('image/driver_form.png')
            load = PLI_Image.open(ipath)
            load = load.resize(tuple(map(lambda x: int(x * 0.5), load.size)))
            render = ImageTk.PhotoImage(load)
            img2 = Label(when_click_start, image=render)
            img2.image = render
            img2.pack()

        self.init_window_position(when_click_start, 1.3, 3)

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
        self.init_window_position(what_is_clear, 1.3, 3)

    def what_is_delay_time(self):
        what_is_delay = Toplevel(self)
        what_is_delay.title('战斗后等待时间说明')

        title = Label(what_is_delay)
        title['text'] = '\n【 战斗后等待时间 】'
        title.pack()
        desc = Message(what_is_delay)
        desc['text'] = '\n战斗后等待时间是指，在下一次战斗开始前强制等待的时间(秒)\n' + \
                       '\n填入的时间还会加上一个300毫秒以内的随机时间\n'
        desc['width'] = 300
        desc.pack()
        self.init_window_position(what_is_delay, 1.3, 3)

    def create_main(self):
        """
        窗体、控件绘制
        :return:
        """
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

        self.label_delay_time['text'] = '战斗结束后等待时间'
        self.var_delay_time.set(self.delay_time)
        self.entry_delay_time['textvariable'] = self.var_delay_time
        self.label_delay_time.grid(row=4, column=0, sticky='E')
        self.entry_delay_time.grid(row=4, column=1, sticky='W', columnspan=2)

        self.button_delay_time_explain['text'] = '?'
        self.button_delay_time_explain['command'] = self.what_is_delay_time
        self.button_delay_time_explain['relief'] = 'flat'
        self.button_delay_time_explain.grid(row=4, column=2, sticky='E')

        self.label_offer['text'] = '好友发来悬赏'
        self.var_offer_mode.set('接受')
        self.listbox_offer_mode['textvariable'] = self.var_offer_mode
        self.listbox_offer_mode['width'] = 10
        self.listbox_offer_mode['values'] = ["接受", "拒绝"]
        # self.listbox_offer_mode.bind("<<ComboboxSelected>>", self.turn_entry_on)
        self.label_offer.grid(row=5, column=0, sticky='E')
        self.listbox_offer_mode.grid(row=5, column=1, sticky='W')

        self.label_timing_mode['text'] = '预定结束'
        self.var_timing_mode.set('无')
        self.listbox_timing_mode['textvariable'] = self.var_timing_mode
        self.listbox_timing_mode['width'] = 10
        self.listbox_timing_mode['values'] = ["无", "定时[分钟]", "场数", "超鬼王模式1", "超鬼王模式2"]
        self.listbox_timing_mode.bind("<<ComboboxSelected>>", self.turn_entry_on)
        self.label_timing_mode.grid(row=6, column=0, sticky='E')
        self.listbox_timing_mode.grid(row=6, column=1, sticky='W')

        self.var_timing_value.set('')
        self.entry_timing_value['textvariable'] = self.var_timing_value
        self.entry_timing_value['width'] = 5
        self.entry_timing_value.configure(state='disabled')
        self.entry_timing_value.grid(row=6, column=2, sticky='W')

        self.label_done_action_mode['text'] = '预定结束后动作'
        self.var_done_action_mode.set('')
        self.listbox_done_action_mode['textvariable'] = self.var_done_action_mode
        self.listbox_done_action_mode['width'] = 10
        self.listbox_done_action_mode.configure(state='disabled')
        self.listbox_done_action_mode['values'] = ["关闭游戏窗口", "仅停止挂机"]
        # self.listbox_done_action_mode.bind("<<ComboboxSelected>>", self.turn_entry_on)
        self.label_done_action_mode.grid(row=7, column=0, sticky='E')
        self.listbox_done_action_mode.grid(row=7, column=1, sticky='W')

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
        var = 'Build 20200226'
        self.info_box.mark_set('insert', END)
        self.info_box.insert('insert', str(var) + '\n')
        self.info_box.see(END)
        var = '请授予此程序管理员权限运行，否则在游戏窗口内鼠标无法被控制'
        self.info_box.mark_set('insert', END)
        self.info_box.insert('insert', str(var) + '\n')
        self.info_box.see(END)
