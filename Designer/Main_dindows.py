import sys
from Designer.pixiv_downloader import *
from PyQt5.QtWidgets import QApplication,QMainWindow

def main_window_display():
    app = QApplication(sys.argv)
    main_window = QMainWindow()
    Ui_MainWindow(main_window)
    main_window.show()
    sys.exit(app.exec_())

main_window_display()