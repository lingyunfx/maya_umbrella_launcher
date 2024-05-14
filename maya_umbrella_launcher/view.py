import sys

from PySide2 import QtWidgets, QtCore
import dayu_widgets as dy
from dayu_widgets.qt import MPixmap, MIcon

from maya_umbrella_launcher import constant as const
from maya_umbrella_launcher import translator as tr
from maya_umbrella_launcher.filesystem import get_installed_maya_versions, get_maya_module_folder
from maya_umbrella_launcher.common_widgets import (CommonWidget, CommonDialog, question_box, show_message,
                                                   show_center_messages)
from maya_umbrella_launcher.core import (get_plugin_folder, set_plugin_folder, get_versions, get_plugin_latest_version,
                                         download_plugin, get_maya_app_path, launch_maya, get_python_path_env,
                                         install_to_maya, uninstall_from_maya)


class MainUI(CommonWidget):

    def __init__(self, parent=None):
        super(MainUI, self).__init__(parent=parent)

        # data
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
        QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)

        self.resize(800, 600)

        theme = dy.MTheme(theme='dark')
        theme.apply(self)

    def connect_command(self):
        self.setting_bt.clicked.connect(self.show_setting_dialog)
        self.translate_bt.clicked.connect(self.switch_language)

    def set_data(self):
        self.launcher_tab.version_cb.addItems(sorted(self.maya_versions))
        self.installer_tab.version_cb.addItems(sorted(self.maya_versions))
        self.translate_ui()

    @staticmethod
    def show_setting_dialog():
        dialog = SettingDialog()
        theme = dy.MTheme(theme='dark')
        theme.apply(dialog)
        dialog.exec_()

    def switch_language(self):
        current_language = tr.get_language()
        tr.set_language('cn' if current_language == 'en' else 'en')
        self.translate_ui()

    def translate_ui(self):

        self.launcher_tab.launch_bt.setText(tr.launch_bt.text)
        self.launcher_tab_bt.setText(tr.launch_tab.text)
        self.launcher_tab.description_label.setText(tr.launcher_desc.text)
        self.launcher_tab.version_label.setText(tr.version_label.text)

        self.installer_tab_bt.setText(tr.install_tab.text)
        self.installer_tab.description_label.setText(tr.install_desc.text)
        self.installer_tab.version_label.setText(tr.version_label.text)
        self.installer_tab.mod_label.setText(tr.mod_label.text)
        self.installer_tab.install_bt.setText(tr.install_bt.text)
        self.installer_tab.remove_bt.setText(tr.remove_bt.text)

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
        self.launch_bt = dy.MPushButton()
        self.version_cb = dy.MComboBox()

        # init ui
        self.init_ui()
        self.adjust_ui()
        self.connect_command()

    def init_ui(self):
        self.add_widgets_v_line(self.description_label)
        self.add_widgets_h_line(self.version_label, self.version_cb, self.launch_bt)
        self.setLayout(self.main_layout)

    def adjust_ui(self):
        self.version_label.setFixedWidth(100)
        self.launch_bt.setIcon(MPixmap('app-maya.png'))
        self.version_cb.setMaximumWidth(200)

    def connect_command(self):
        self.launch_bt.clicked.connect(self.launch_bt_clicked)

    def launch_bt_clicked(self):
        maya_version = self.version_cb.currentText()
        if not maya_version:
            return

        maya_path = get_maya_app_path(maya_version)
        if not maya_path:
            return show_message(text=tr.unable_found_maya.text.format(maya_version),
                                typ='error',
                                parent=self)

        envs = get_python_path_env()
        if not envs:
            return show_message(text=tr.unable_found_script.text,
                                typ='error',
                                parent=self
                                )

        launch_maya(maya_path, envs)


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
        self.install_bt.clicked.connect(self.install_bt_clicked)
        self.remove_bt.clicked.connect(self.remove_bt_clicked)
        self.version_cb.currentTextChanged.connect(self.version_cb_changed)

    def version_cb_changed(self, version_number):
        if version_number:
            self.mod_folder_line.setText(get_maya_module_folder(version_number))

    def install_bt_clicked(self):
        maya_version = self.version_cb.currentText()
        if not maya_version:
            return

        if install_to_maya(maya_version):
            show_message(text=tr.install_success.text, typ='success', parent=self)
        else:
            show_message(text=tr.unable_found_script.text, typ='error', parent=self)

    def remove_bt_clicked(self):
        maya_version = self.version_cb.currentText()
        if not maya_version:
            return

        uninstall_from_maya(maya_version)
        show_message(text=tr.uninstall_success.text, typ='success', parent=self)


class SettingDialog(CommonDialog):

    def __init__(self, parent=None):
        super(SettingDialog, self).__init__(parent=parent)

        # widget
        self.loading_msg = None
        self.setting_title = dy.MLabel().h2().secondary()
        self.plugin_label = dy.MLabel()
        self.version_label = dy.MLabel()
        self.folder_line = dy.MLineEdit().folder().small()
        self.version_cb = dy.MComboBox().small()
        self.download_bt = dy.MPushButton().small()
        self.check_bt = dy.MPushButton().small()

        # init ui
        self.init_ui()
        self.adjust_ui()
        self.translate_ui()
        self.set_data()
        self.connect_command()

    def init_ui(self):
        self.add_widgets_h_line(self.setting_title)
        self.add_widgets_h_line(self.plugin_label, self.folder_line, self.download_bt)
        self.add_widgets_h_line(self.version_label, self.version_cb, self.check_bt)

        self.setLayout(self.main_layout)

    def adjust_ui(self):
        self.resize(600, 180)
        self.setWindowTitle('Settings Dialog')

    def set_data(self):
        plugin_folder = get_plugin_folder()
        if plugin_folder:
            self.plugin_folder = plugin_folder
            self.versions = get_versions(plugin_folder)

    def connect_command(self):
        self.folder_line.textChanged.connect(self.folder_line_changed)
        self.check_bt.clicked.connect(self.check_bt_clicked)
        self.download_bt.clicked.connect(self.download_bt_clicked)

    def folder_line_changed(self):
        set_plugin_folder(self.plugin_folder)
        self.versions = get_versions(self.plugin_folder)

    def download_bt_clicked(self):

        self.loading_msg = dy.MToast.loading(tr.downloading.text, parent=self)
        self.disable_dialog(is_disable=True)
        task = DownloadTask(parent=self)
        task.is_success_sig.connect(self.msg_slot_finished)
        task.start()

    def check_bt_clicked(self):
        current_latest_version = max(self.versions) if self.versions else 'v0.0.0'
        latest_version = get_plugin_latest_version()
        if latest_version > current_latest_version:
            if question_box(text=tr.is_download_new_version.text.format(latest_version), parent=self):
                self.download_bt_clicked()
                return
        else:
            show_message(text=tr.already_latest_version.text, parent=self)

    def translate_ui(self):
        self.setting_title.setText(tr.setting_title_label.text)
        self.plugin_label.setText(tr.plugin_folder_label.text)
        self.version_label.setText(tr.plugin_version_label.text)
        self.download_bt.setText(tr.download_bt.text)
        self.check_bt.setText(tr.check_update_bt.text)

    def msg_slot_finished(self, is_success):
        self.disable_dialog(is_disable=False)
        self.loading_msg.close()
        if is_success:
            self.set_data()
            show_center_messages(text=tr.download_success.text, typ='success', parent=self)
        else:
            show_center_messages(text=tr.download_failed.text, typ='warning', parent=self)

    def disable_dialog(self, is_disable=True):
        self.download_bt.setEnabled(not is_disable)
        self.check_bt.setEnabled(not is_disable)
        self.folder_line.setEnabled(not is_disable)
        self.version_cb.setEnabled(not is_disable)

    @staticmethod
    def download_plugin():
        return download_plugin()

    @property
    def plugin_folder(self):
        return self.folder_line.text()

    @plugin_folder.setter
    def plugin_folder(self, value):
        self.folder_line.setText(value)

    @property
    def versions(self):
        return [self.version_cb.itemText(i) for i in range(self.version_cb.count())]

    @versions.setter
    def versions(self, versions):
        self.version_cb.clear()
        if versions:
            self.version_cb.addItems(sorted(versions, reverse=True))


class DownloadTask(QtCore.QThread):

    is_success_sig = QtCore.Signal(bool)

    def __init__(self, parent=None):
        super(DownloadTask, self).__init__(parent=parent)

    def run(self):
        if download_plugin():
            self.is_success_sig.emit(True)
        else:
            self.is_success_sig.emit(False)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ui = MainUI()
    ui.show()
    app.exec_()
