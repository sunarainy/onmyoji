# -*-coding:utf-8-*-

import sys
import os
from ctypes import *


def create_app(title, version):
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
    from create_window import Application
    from utilities import init_window_position
    app = Application()
    app.master.title(title)
    app.setversion(version)
    app.create_main()
    init_window_position(app.master, 1.1, 4)
    # 隐藏console窗口
    try:
        para = sys.argv[1]
    except IndexError:
        para = False
    if para == 'debug':
        app.setdebug(True)
    else:
        whnd = windll.kernel32.GetConsoleWindow()
        if whnd:
            windll.user32.ShowWindow(whnd, 0)
            windll.kernel32.CloseHandle(whnd)

    return app


myapp = create_app('就你破势多', '20200228')
myapp.mainloop()
