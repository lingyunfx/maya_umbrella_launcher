import sys
from PySide2 import QtWidgets, QtCore
import dayu_widgets as dy
from dayu_widgets.qt import MPixmap, MIcon


from maya_umbrella_launcher.common_widgets import CommonWidget, CommonDialog
from maya_umbrella_launcher.maya import get_installed_maya_versions
from maya_umbrella_launcher import constant as const
from maya_umbrella_launcher.filesystem import get_maya_module_folder


class MainUI(CommonWidget):

    def __init__(self, parent=None):
        super(MainUI, self).__init__(parent=parent)

        # data
        self.language = 'en'
        self.maya_versions = get_installed_maya_versions()

        # widgets
        self.line_tab = dy.MLineTabWidget(alignment=QtCore.Qt.AlignLeft, parent=self)
        self.launcher_tab = LauncherWidget(parent=self)
        self.installer_tab = InstallerWidget(parent=self)
        self.help_bt = dy.MToolButton().svg(r'./resource/help.svg').icon_only().small()
        self.setting_bt = dy.MToolButton().svg(r'./resource/settings.svg').icon_only().small()
        self.translate_bt = dy.MToolButton().svg(r'./resource/translate.svg').icon_only().small()
        self.theme_bt = dy.MToolButton().svg(r'./resource/dark.svg').icon_only().small()
        self.div = dy.MDivider()

        # init ui
        self.init_ui()
        self.adjust_ui()
        self.connect_command()
        self.set_data()
        self.translate_ui()

    def init_ui(self):
        self.line_tab.add_tab(self.launcher_tab, '.')
        self.line_tab.add_tab(self.installer_tab, '.')

        self.add_widgets_h_line(dy.MLabel('Maya Umbrella Launcher').h2().secondary())
        self.add_widgets_v_line(self.line_tab)
        self.add_widgets_v_line(self.div)
        self.add_widgets_h_line(self.translate_bt, self.theme_bt, self.setting_bt, self.help_bt, side='right')

        self.setLayout(self.main_layout)

    def adjust_ui(self):
        self.line_tab.tool_button_group.set_dayu_checked(0)
        self.setWindowTitle(const.WINDOW_TITLE)
        self.setWindowIcon(MIcon(r'./resource/app_umbrella.ico'))

        self.resize(800, 600)

        theme = dy.MTheme(theme='dark')
        theme.apply(self)

    def connect_command(self):
        self.setting_bt.clicked.connect(self.show_setting_dialog)
        self.translate_bt.clicked.connect(self.translate_ui)

    def set_data(self):
        self.launcher_tab.version_cb.addItems(sorted(self.maya_versions))
        self.installer_tab.version_cb.addItems(sorted(self.maya_versions))

    def show_setting_dialog(self):
        dialog = SettingDialog(language=self.language,
                               parent=self)
        dialog.exec_()

    def translate_ui(self):
        self.language = 'cn' if self.language == 'en' else 'en'
        lang = self.language

        self.launcher_tab.maya_bt.setText(const.LAUNCH_BUTTON[lang])
        self.launcher_tab_bt.setText(const.LAUNCH_TAB[lang])
        self.launcher_tab.description_label.setText(const.LAUNCHER_DESC[lang])
        self.launcher_tab.version_label.setText(const.VERSION_LABEL[lang])

        self.installer_tab_bt.setText(const.INSTALL_TAB[lang])
        self.installer_tab.description_label.setText(const.INSTALL_DESC[lang])
        self.installer_tab.version_label.setText(const.VERSION_LABEL[lang])
        self.installer_tab.mod_label.setText(const.MOD_LABEL[lang])
        self.installer_tab.install_bt.setText(const.INSTALL_BUTTON[lang])
        self.installer_tab.remove_bt.setText(const.REMOVE_BUTTON[lang])

    @property
    def launcher_tab_bt(self):
        return self.line_tab.tool_button_group.get_button_group().button(0)

    @property
    def installer_tab_bt(self):
        return self.line_tab.tool_button_group.get_button_group().button(1)


class LauncherWidget(CommonWidget):

    def __init__(self, parent=None):
        super(LauncherWidget, self).__init__(parent=parent)

        # widgets
        self.description_label = dy.MLabel().code()
        self.version_label = dy.MLabel()
        self.maya_bt = dy.MPushButton()
        self.version_cb = dy.MComboBox()

        # init ui
        self.init_ui()
        self.adjust_ui()

    def init_ui(self):
        self.add_widgets_v_line(self.description_label)
        self.add_widgets_h_line(self.version_label, self.version_cb, self.maya_bt)
        self.setLayout(self.main_layout)

    def adjust_ui(self):
        self.version_label.setFixedWidth(100)
        self.maya_bt.setIcon(MPixmap('app-maya.png'))
        self.version_cb.setMaximumWidth(200)


class InstallerWidget(CommonWidget):

    def __init__(self, parent=None):
        super(InstallerWidget, self).__init__(parent=parent)

        # widgets
        self.version_label = dy.MLabel()
        self.mod_label = dy.MLabel()
        self.description_label = dy.MLabel().code()
        self.version_cb = dy.MComboBox().small()
        self.mod_folder_line = dy.MLineEdit().small()
        self.install_bt = dy.MPushButton().small()
        self.remove_bt = dy.MPushButton().small()

        # init ui
        self.init_ui()
        self.adjust_ui()
        self.connect_command()

    def init_ui(self):
        self.add_widgets_v_line(self.description_label)
        self.add_widgets_h_line(self.version_label, self.version_cb)
        self.add_widgets_h_line(self.mod_label, self.mod_folder_line)
        self.add_widgets_h_line(self.install_bt, self.remove_bt)

        self.setLayout(self.main_layout)

    def adjust_ui(self):
        self.mod_folder_line.setReadOnly(True)

    def connect_command(self):
        self.version_cb.currentTextChanged.connect(self.version_cb_changed)

    def version_cb_changed(self, version_number):
        if version_number:
            self.mod_folder_line.setText(get_maya_module_folder(version_number))


class SettingDialog(CommonDialog):

    def __init__(self, language, parent=None):
        super(SettingDialog, self).__init__(parent=parent)

        # data
        self.language = language

        # widget
        self.setting_title = dy.MLabel().h2().secondary()
        self.plug_folder_label = dy.MLabel()
        self.plug_version_label = dy.MLabel('')
        self.plug_folder_line = dy.MLineEdit().folder().small()
        self.plug_version_cb = dy.MComboBox().small()
        self.download_bt = dy.MPushButton().small()
        self.check_update_bt = dy.MPushButton().small()

        self.init_ui()
        self.adjust_ui()
        self.translate_ui()

    def init_ui(self):
        self.add_widgets_h_line(self.setting_title)
        self.add_widgets_h_line(self.plug_folder_label, self.plug_folder_line, self.download_bt)
        self.add_widgets_h_line(self.plug_version_label, self.plug_version_cb, self.check_update_bt)

        self.setLayout(self.main_layout)

    def adjust_ui(self):
        self.resize(600, 180)
        self.setWindowTitle('Settings Dialog')

    def translate_ui(self):
        self.setting_title.setText(const.SETTING_TITLE_LABEL[self.language])
        self.plug_folder_label.setText(const.PLUGIN_FOLDER_LABEL[self.language])
        self.plug_version_label.setText(const.PLUGIN_VERSION_LABEL[self.language])
        self.download_bt.setText(const.DOWNLOAD_BUTTON[self.language])
        self.check_update_bt.setText(const.CHECK_UPDATE_BUTTON[self.language])


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ui = MainUI()
    ui.show()
    app.exec_()
