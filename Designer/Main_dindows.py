# !/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from Designer.pixiv_downloader import *
from PyQt5.QtWidgets import QApplication, QMainWindow




def windows_main():
    app = QApplication(sys.argv)
    main_window = QMainWindow()
    ui = Ui_MainWindow(main_window)
    main_window.show()
    sys.exit(app.exec_())
