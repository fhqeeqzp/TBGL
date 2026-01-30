# coding:utf-8
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from qfluentwidgets import SettingCardGroup, OptionsSettingCard, ComboBoxSettingCard
from qfluentwidgets import FluentIcon as FIF

from ..common.config import cfg


class SettingInterface(QWidget):
    """ 设置界面类 """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName('SettingInterface')
        self.initUI()

    def initUI(self):
        # 创建垂直布局
        self.vBoxLayout = QVBoxLayout(self)
        
        # 标题
        self.titleLabel = QLabel('主题设置', self)
        self.titleLabel.setObjectName('titleLabel')
        
        # 创建设置卡片组
        self.settingGroup = SettingCardGroup('外观设置', self)
        
        # 主题设置卡片
        self.themeCard = OptionsSettingCard(
            cfg.themeMode,
            FIF.BRUSH,
            "应用主题",
            "设置应用的外观主题",
            texts=["浅色", "深色", "跟随系统"]
        )
        
        # DPI缩放设置卡片
        self.dpiCard = ComboBoxSettingCard(
            cfg.dpiScale,
            FIF.ZOOM,
            "DPI缩放",
            "调整应用的显示大小",
            texts=["自动", "100%", "125%", "150%", "175%", "200%"]
        )
        
        # 添加卡片到组
        self.settingGroup.addSettingCard(self.themeCard)
        self.settingGroup.addSettingCard(self.dpiCard)
        
        # 添加到布局
        self.vBoxLayout.addWidget(self.titleLabel)
        self.vBoxLayout.addWidget(self.settingGroup)
        self.vBoxLayout.addStretch()
