#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年12月3日
@author: Irony
@site: https://pyqt.site https://github.com/892768447
@email: 892768447@qq.com
@file: 重定向输出
@description: 
"""
from PyQt5.QtWidgets import QTextBrowser


__Author__ = 'Irony'
__Copyright__ = 'Copyright (c) 2019'
__Version__ = 1.0


class Window(QTextBrowser):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)

        # 记住原来的方法
        self._swrite = sys.stdout.write
        # 替换原来的方法
        sys.stdout.write = self.onWrite

        print('test')
        print('this is message')

    def onWrite(self, text):
        self._swrite(text)
        self.append(text)


if __name__ == '__main__':
    import sys
    import cgitb
    sys.excepthook = cgitb.enable(1, None, 5, '')
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())