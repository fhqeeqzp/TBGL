# coding: utf-8
from PyQt6.QtCore import QSize, QRect
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QStyleFactory

from qfluentwidgets import (NavigationItemPosition, MessageBox, FluentWindow,
                            SystemThemeListener)
from qfluentwidgets import FluentIcon as FIF

from .setting_interface import SettingInterface
from ..common.config import cfg


class MainWindow(FluentWindow):

    def __init__(self):
        super().__init__()
        self.initWindow()

        # create system theme listener
        self.themeListener = SystemThemeListener(self)

        # create sub interface
        self.settingInterface = SettingInterface(self)

        self.connectSignalToSlot()

        # add items to navigation interface
        self.initNavigation()

        # start theme listener
        self.themeListener.start()

    def connectSignalToSlot(self):
        pass

    def initNavigation(self):
        # add only setting interface to navigation
        self.addSubInterface(
            self.settingInterface, FIF.SETTING, self.tr('Settings'), NavigationItemPosition.SCROLL)

    def initWindow(self):
        self.resize(960, 780)
        self.setMinimumWidth(760)
        self.setWindowIcon(QIcon())
        self.setWindowTitle('主题设置演示')

        self.setMicaEffectEnabled(cfg.get(cfg.micaEnabled))

        # center the window on desktop
        screen = QApplication.primaryScreen()
        screen_geometry = screen.geometry()
        w, h = screen_geometry.width(), screen_geometry.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)
        self.show()

    def resizeEvent(self, e):
        super().resizeEvent(e)

    def closeEvent(self, e):
        self.themeListener.terminate()
        self.themeListener.deleteLater()
        super().closeEvent(e)
