from pixiv.network_speed import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QProgressBar, QPushButton, QFileDialog
import sys
import threading as Thread
from pixiv.printer import *
from main import *
import inspect
import ctypes


def _async_raise(tid, exctype):
    """用于强制结束线程的函数"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)


class Worker(QtCore.QThread):
    valueChanged = QtCore.pyqtSignal(str)  # 值变化信号

    def run(self):
        while True:
            speed = speed_test()
            self.valueChanged.emit(speed)


class Ui_MainWindow(object):

    def __init__(self, MainWindow):
        super(Ui_MainWindow, self).__init__()
        self.setupUi(MainWindow)
        self.main_process()
        self._swrite = sys.stdout.write
        # 替换原来print的方法
        sys.stdout.write = self.onWrite

    def onWrite(self, mystr):
        '''
        重建print函数
        Mypstr：是待显示的字符串
        '''
        self.text_show.insertHtml(str(mystr))  # 在指定的区域显示提示信息
        self.text_show.append('')
        sys.stdout.flush()
        self.cursor = self.text_show.textCursor()
        self.text_show.moveCursor(self.cursor.End)  # 光标移到最后，这样就会自动显示出来
        QtWidgets.QApplication.processEvents()  # 一定加上这个功能，不然有卡顿

    def setupUi(self, MainWindow):

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(487, 375)
        MainWindow.setMinimumSize(QtCore.QSize(487, 375))
        MainWindow.setMaximumSize(QtCore.QSize(487, 375))
        MainWindow.setBaseSize(QtCore.QSize(487, 375))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Designer/pixiv_icon.png"), QtGui.QIcon.Normal)
        MainWindow.setWindowIcon(icon)
        MainWindow.setToolTipDuration(0)
        MainWindow.setStyleSheet("")
        MainWindow.setInputMethodHints(QtCore.Qt.ImhNone)
        MainWindow.setToolButtonStyle(QtCore.Qt.ToolButtonFollowStyle)
        MainWindow.setAnimated(False)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        MainWindow.setDockNestingEnabled(False)
        MainWindow.setDockOptions(QtWidgets.QMainWindow.AllowTabbedDocks | QtWidgets.QMainWindow.GroupedDragging)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.start = QtWidgets.QPushButton(self.centralwidget)
        self.start.setGeometry(QtCore.QRect(384, 60, 91, 51))
        self.start.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.start.setAutoDefault(True)
        self.start.setObjectName("start")
        self.select_list = QtWidgets.QComboBox(self.centralwidget)
        self.select_list.setGeometry(QtCore.QRect(90, 20, 91, 22))
        self.select_list.setObjectName("select_list")
        self.select_list.addItem("")
        self.select_list.addItem("")
        self.select_list.addItem("")
        self.keywords_input = QtWidgets.QLineEdit(self.centralwidget)
        self.keywords_input.setGeometry(QtCore.QRect(190, 20, 81, 21))
        self.keywords_input.setObjectName("keywords_input")
        self.text_show = QtWidgets.QTextBrowser(self.centralwidget)
        self.text_show.setGeometry(QtCore.QRect(20, 130, 451, 201))
        self.text_show.setAutoFillBackground(True)
        self.text_show.setObjectName("text_show")
        self.max_number = QtWidgets.QSpinBox(self.centralwidget)
        self.max_number.setGeometry(QtCore.QRect(90, 60, 51, 22))
        self.max_number.setMinimum(0)
        self.max_number.setMaximum(1000000)
        self.max_number.setProperty("value", 200)
        self.max_number.setObjectName("max_number")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 20, 51, 21))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(30, 60, 51, 20))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(150, 60, 81, 20))
        self.label_3.setObjectName("label_3")
        self.min_like = QtWidgets.QSpinBox(self.centralwidget)
        self.min_like.setGeometry(QtCore.QRect(230, 60, 51, 22))
        self.min_like.setMinimum(0)
        self.min_like.setMaximum(1000000)
        self.min_like.setObjectName("min_like")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(30, 100, 54, 12))
        self.label_4.setObjectName("label_4")
        self.path = QtWidgets.QLineEdit(self.centralwidget)
        self.path.setGeometry(QtCore.QRect(90, 100, 221, 20))
        self.path.setObjectName("path")
        self.path_buttom = QtWidgets.QPushButton(self.centralwidget)
        self.path_buttom.setGeometry(QtCore.QRect(320, 100, 41, 20))
        self.path_buttom.setChecked(False)
        self.path_buttom.setObjectName("path_buttom")
        self.for_single_dir = QtWidgets.QCheckBox(self.centralwidget)
        self.for_single_dir.setGeometry(QtCore.QRect(300, 20, 151, 20))
        self.for_single_dir.setObjectName("for_single_dir")
        self.download_speed = QtWidgets.QLabel(self.centralwidget)
        self.download_speed.setGeometry(QtCore.QRect(400, 335, 71, 21))
        self.download_speed.setObjectName("download_speed")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(290, 60, 41, 20))
        self.label_5.setObjectName("label_5")
        self.thread_number = QtWidgets.QSpinBox(self.centralwidget)
        self.thread_number.setGeometry(QtCore.QRect(330, 60, 42, 22))
        self.thread_number.setMinimum(1)
        self.thread_number.setMaximum(5000)
        self.thread_number.setSingleStep(1)
        self.thread_number.setProperty("value", 5)
        self.thread_number.setObjectName("thread_number")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.path_buttom, self.start)
        MainWindow.setTabOrder(self.start, self.min_like)
        MainWindow.setTabOrder(self.min_like, self.keywords_input)
        MainWindow.setTabOrder(self.keywords_input, self.select_list)
        MainWindow.setTabOrder(self.select_list, self.max_number)
        MainWindow.setTabOrder(self.max_number, self.path)
        MainWindow.setTabOrder(self.path, self.text_show)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Pixiv_Downloader"))
        self.start.setText(_translate("MainWindow", "开始爬取"))
        self.select_list.setItemText(0, _translate("MainWindow", "画师id"))
        self.select_list.setItemText(1, _translate("MainWindow", "搜索结果"))
        self.select_list.setItemText(2, _translate("MainWindow", "每日排名"))
        self.label.setText(_translate("MainWindow", "爬取目标:"))
        self.label_2.setText(_translate("MainWindow", "限制数量:"))
        self.label_3.setText(_translate("MainWindow", "最少喜爱人数:"))
        self.label_4.setText(_translate("MainWindow", "储存路径:"))
        self.path.setText(_translate("MainWindow", "默认为程序所在目录"))
        self.path_buttom.setText(_translate("MainWindow", "..."))
        self.for_single_dir.setText(_translate("MainWindow", "为画册建立单独文件夹"))
        self.download_speed.setText(_translate("MainWindow", "网络速度"))
        self.label_5.setText(_translate("MainWindow", "线程数"))

    def main_process(self):
        '''主入口'''
        self.net_spped()  # 网络测速初始化
        self.select_list.currentIndexChanged.connect(self.hide)
        self.start.clicked.connect(self.spider)  # 爬取按钮
        self.path_buttom.clicked.connect(self.explore)

    def hide(self):
        '''若选择排名获取，则无需关键字栏'''
        select_words = self.select_list.currentText()
        if select_words == '每日排名':
            self.keywords_input.hide()
        else:
            self.keywords_input.show()

    def net_spped(self):
        '''网络信号事件'''
        self._threads = Worker()
        self._threads.valueChanged.connect(self.set)
        self._threads.start()  # 开启网络测速线程

    def set(self, str):
        self.download_speed.setText(str)

    def explore(self):
        '''选择保存目录事件'''
        directory = QFileDialog.getExistingDirectory(None, "选择文件夹", "/")
        self.path.setText(directory + '\\')

    def spider(self):
        '''爬虫启动项'''
        if self.start.text() == '开始爬取':
            self.start.setText('结束爬取')
            select_words = self.select_list.currentText()
            limits = int(self.max_number.text())
            single_dir = bool(self.for_single_dir.checkState())
            key_word = self.keywords_input.text()
            like = int(self.min_like.text())
            path = self.path.text()
            if path == '默认为程序所在目录':
                path = ''
            thread_numbers = int(self.thread_number.text())
            if select_words == '画师id':
                try:
                    self.T1 = Thread.Thread(target=pix_id, args=(key_word, limits, like, path, single_dir, thread_numbers))
                    self.T1.start()
                except  Exception as e:
                    print(e)
            elif select_words == '搜索结果':
                self.T1 = Thread.Thread(target=pix_search, args=(key_word, limits, like, path, single_dir, thread_numbers))
                try:
                    self.T1.start()
                except  Exception as e:
                    print(e)
            elif select_words == '每日排名':
                try:
                    self.T1 = Thread.Thread(target=pix_rank, args=(limits, like, path, single_dir, thread_numbers))
                    self.T1.start()
                except  Exception as e:
                    print(e)

        elif self.start.text() == '结束爬取':
            try:
                self.start.setText('开始爬取')
                stop_thread(self.T1)
                printer('已结束主线程，正在等待其余分支线程完成',color='red',style=1)
            except:
                pass
