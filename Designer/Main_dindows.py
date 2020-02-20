import sys
from Designer.pixiv_downloader import *
from PyQt5.QtWidgets import QApplication, QMainWindow
from pixiv.printer import *
import time



if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = QMainWindow()
    ui = Ui_MainWindow(main_window)
    main_window.show()
    sys.exit(app.exec_())
