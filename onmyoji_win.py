# -*-coding:utf-8-*-

import sys
import os


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

    return app


myapp = create_app('就你破势多', '20210531')
myapp.mainloop()
