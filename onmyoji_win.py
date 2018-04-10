# -*-coding:utf-8-*-

import sys
from ctypes import *
from create_window import Application

app = Application()
# 隐藏console窗口
try:
    para = sys.argv[1]
except IndexError:
    para = False
if para == 'test':
    pass
else:
    whnd = windll.kernel32.GetConsoleWindow()
    if whnd:
        windll.user32.ShowWindow(whnd, 0)
        windll.kernel32.CloseHandle(whnd)
app.master.title('就你破势多')
app.init_window_place(app.master, 1.1, 4)
app.mainloop()
