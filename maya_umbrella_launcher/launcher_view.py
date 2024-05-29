import os.path
import sys

import dayu_widgets as dy
from PySide2 import QtWidgets, QtCore
from dayu_widgets.qt import MPixmap, MIcon

import maya_umbrella_launcher.constant as const
import maya_umbrella_launcher.translator as tr
from maya_umbrella_launcher.common_widgets import CommonWidget, CommonDialog, question_box, show_message
from maya_umbrella_launcher.filesystem import MayaSystem
from maya_umbrella_launcher.core import PluginManager, PluginInstaller, UserSetting


class MainUI(CommonWidget):

    def __init__(self, parent=None):
        super(MainUI, self).__init__(parent=parent)

        # data
        self.maya_versions = MayaSystem.get_installed_maya_versions()

        # widgets
        self.line_tab = dy.MLineTabWidget(alignment=QtCore.Qt.AlignLeft, parent=self)
        self.launcher_tab = LauncherWidget(parent=self)
        self.installer_tab = InstallerWidget(parent=self)
        self.help_bt = dy.MToolButton().svg(r'../resource/help.svg').icon_only().small()
        self.setting_bt = dy.MToolButton().svg(r'../resource/settings.svg').icon_only().small()
        self.translate_bt = dy.MToolButton().svg(r'../resource/translate.svg').icon_only().small()
        self.theme_bt = dy.MToolButton().svg(r'../resource/dark.svg').icon_only().small()
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
        self.setWindowIcon(MIcon(r'../resource/app_umbrella.ico'))
        QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)

        main_window_size = UserSetting.get('main_window_size')
        if not main_window_size:
            self.resize(520, 400)
        else:
            self.resize(*main_window_size)

        theme = dy.MTheme(theme=self.current_theme)
        theme.apply(self)
        theme.apply(self.installer_tab.version_cb)
        theme.apply(self.launcher_tab.version_cb)

    def connect_command(self):
        self.setting_bt.clicked.connect(self.show_setting_dialog)
        self.translate_bt.clicked.connect(self.switch_language)
        self.theme_bt.clicked.connect(self.switch_theme)

    def set_data(self):
        self.launcher_tab.version_cb.addItems(sorted(self.maya_versions))
        self.installer_tab.version_cb.addItems(sorted(self.maya_versions))
        self.translate_ui()

    def show_setting_dialog(self):
        dialog = SettingDialog()
        theme = dy.MTheme(theme=self.current_theme)
        theme.apply(dialog)
        theme.apply(dialog.version_cb)
        dialog.exec_()

    def switch_language(self):
        current_language = tr.get_language()
        tr.set_language('cn' if current_language == 'en' else 'en')
        self.translate_ui()

    def switch_theme(self):
        new_theme = 'dark' if self.current_theme == 'light' else 'light'
        theme = dy.MTheme(theme=new_theme)
        theme.apply(self)
        theme.apply(self.installer_tab.version_cb)
        theme.apply(self.launcher_tab.version_cb)
        self.current_theme = new_theme

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

    @property
    def current_theme(self):
        theme = UserSetting.get('theme', default='dark')
        return theme

    @current_theme.setter
    def current_theme(self, value):
        UserSetting.set('theme', value)

    def closeEvent(self, event):
        size = self.size()
        UserSetting.set('main_window_size', (size.width(), size.height()))


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
        self.version_label.setFixedWidth(60)
        self.launch_bt.setIcon(MPixmap('app-maya.png'))
        self.version_cb.setMaximumWidth(200)

    def connect_command(self):
        self.launch_bt.clicked.connect(self.launch_bt_clicked)

    def launch_bt_clicked(self):
        maya_version = self.version_cb.currentText()
        if not maya_version:
            return

        maya_path = MayaSystem.get_maya_app_path(maya_version)
        if not maya_path:
            return show_message(text=tr.unable_found_maya.text.format(maya_version),
                                typ='error',
                                parent=self)

        envs = PluginManager.get_python_path_env()
        if not envs:
            return show_message(text=tr.unable_found_script.text,
                                typ='error',
                                parent=self
                                )

        MayaSystem.launch_maya(maya_path, envs)


class InstallerWidget(CommonWidget):

    def __init__(self, parent=None):
        super(InstallerWidget, self).__init__(parent=parent)

        # widgets
        self.version_label = dy.MLabel()
        self.mod_label = dy.MLabel()
        self.description_label = dy.MLabel().code()
        self.version_cb = dy.MComboBox().small()
        self.mod_file_line = dy.MLineEdit().small()
        self.install_bt = dy.MPushButton().small()
        self.remove_bt = dy.MPushButton().small()
        self.status_label = dy.MLabel().strong()

        # init ui
        self.init_ui()
        self.adjust_ui()
        self.connect_command()

    def init_ui(self):
        self.add_widgets_v_line(self.description_label)
        self.add_widgets_h_line(self.version_label, self.version_cb, self.status_label)
        self.add_widgets_h_line(self.mod_label, self.mod_file_line)
        self.add_widgets_h_line(self.install_bt, self.remove_bt)

        self.setLayout(self.main_layout)

    def adjust_ui(self):
        self.mod_file_line.setReadOnly(True)

    def connect_command(self):
        self.install_bt.clicked.connect(self.install_bt_clicked)
        self.remove_bt.clicked.connect(self.remove_bt_clicked)
        self.version_cb.currentTextChanged.connect(self.version_cb_changed)

    def version_cb_changed(self, version_number):
        if version_number:
            mod_folder = MayaSystem.get_maya_module_folder(version_number)
            mod_file = os.path.join(mod_folder, 'maya_umbrella.mod')
            self.mod_file_line.setText(mod_file)
            self.update_install_status()

    def install_bt_clicked(self):
        maya_version = self.version_cb.currentText()
        if not maya_version:
            return

        if PluginInstaller.install(maya_version):
            show_message(text=tr.install_success.text, typ='success', parent=self)
        else:
            show_message(text=tr.install_failed.text, typ='error', parent=self)
        self.update_install_status()

    def remove_bt_clicked(self):
        maya_version = self.version_cb.currentText()
        if not maya_version:
            return

        PluginInstaller.uninstall(maya_version)
        show_message(text=tr.uninstall_success.text, typ='success', parent=self)
        self.update_install_status()

    def update_install_status(self):
        mod_file = self.mod_file_line.text()
        if os.path.isfile(mod_file):
            self.status_label.setText(tr.already_installed_status.text)
            self.status_label.set_dayu_type(dy.MLabel.WarningType)
        else:
            self.status_label.setText(tr.not_installed_status.text)
            self.status_label.set_dayu_type(dy.MLabel.DangerType)


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
        self.proxy_ckb = dy.MCheckBox()
        self.proxy_line = dy.MLineEdit().small()

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
        self.add_widgets_h_line(self.proxy_ckb, self.proxy_line)

        self.setLayout(self.main_layout)

    def adjust_ui(self):
        # 恢复窗口大小
        setting_window_size = UserSetting.get('setting_window_size')
        if not setting_window_size:
            self.resize(450, 160)
        else:
            self.resize(*setting_window_size)

        self.setWindowTitle('Settings Dialog')

    def set_data(self):
        plugin_folder = UserSetting.get('plugin_folder')
        if plugin_folder:
            self.plugin_folder = plugin_folder
            self.versions = PluginManager.get_local_version_list(plugin_folder)

        proxy_on = UserSetting.get('proxy_on', default='')
        self.proxy_ckb.setChecked(bool(proxy_on))
        self.proxy_line.setEnabled(bool(proxy_on))
        self.proxy_url = UserSetting.get('proxy_url', default='')
        self.proxy_line.setPlaceholderText('Example: http://127.0.0.1:8889')

    def connect_command(self):
        self.folder_line.textChanged.connect(self.folder_line_changed)
        self.check_bt.clicked.connect(self.check_bt_clicked)
        self.download_bt.clicked.connect(self.download_bt_clicked)
        self.proxy_ckb.stateChanged.connect(self.proxy_ckb_clicked)
        self.proxy_line.textChanged.connect(self.update_proxy_setting)

    def folder_line_changed(self):
        UserSetting.set('plugin_folder', self.plugin_folder)
        self.versions = PluginManager.get_local_version_list(self.plugin_folder)

    def download_bt_clicked(self):
        self.loading_msg = dy.MToast.loading(tr.downloading.text, parent=self)
        self.disable_dialog(is_disable=True)

        task = DownloadTask(proxies=self.proxies,
                            parent=self)
        task.is_success_sig.connect(self.msg_slot_finished)
        task.start()

    def check_bt_clicked(self):
        current_latest_version = max(self.versions) if self.versions else 'v0.0.0'
        latest_version = PluginManager.get_latest_version()
        if latest_version > current_latest_version:
            if question_box(text=tr.is_download_new_version.text.format(latest_version), parent=self):
                self.download_bt_clicked()
                return
        else:
            show_message(text=tr.already_latest_version.text, parent=self)

    def proxy_ckb_clicked(self):
        self.proxy_line.setEnabled(self.proxy_ckb.isChecked())
        self.update_proxy_setting()

    def update_proxy_setting(self):
        proxy_on = '1' if self.proxy_ckb.isChecked() else ''
        UserSetting.set('proxy_on', proxy_on)
        UserSetting.set('proxy_url', self.proxy_url)

    def translate_ui(self):
        self.setting_title.setText(tr.setting_title_label.text)
        self.plugin_label.setText(tr.plugin_folder_label.text)
        self.version_label.setText(tr.plugin_version_label.text)
        self.download_bt.setText(tr.download_bt.text)
        self.check_bt.setText(tr.check_update_bt.text)
        self.proxy_ckb.setText(tr.proxy_label.text)

    def msg_slot_finished(self, is_success):
        self.disable_dialog(is_disable=False)
        self.loading_msg.close()
        if is_success:
            self.set_data()
            show_message(text=tr.download_success.text,
                         typ='success',
                         pos_center=True,
                         parent=self)
        else:
            show_message(text=tr.download_failed.text,
                         typ='warning',
                         pos_center=True,
                         parent=self)

    def disable_dialog(self, is_disable=True):
        self.download_bt.setEnabled(not is_disable)
        self.check_bt.setEnabled(not is_disable)
        self.folder_line.setEnabled(not is_disable)
        self.version_cb.setEnabled(not is_disable)

    def closeEvent(self, event):
        width = self.size().width()
        height = self.size().height()
        UserSetting.set('setting_window_size', (width, height))

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

    @property
    def proxy_url(self):
        return self.proxy_line.text()

    @proxy_url.setter
    def proxy_url(self, value):
        self.proxy_line.setText(value)

    @property
    def proxies(self):
        if self.proxy_ckb.isChecked():
            return {'http': self.proxy_url, 'https': self.proxy_url}
        else:
            return


class DownloadTask(QtCore.QThread):

    is_success_sig = QtCore.Signal(bool)

    def __init__(self, proxies, parent=None):
        super(DownloadTask, self).__init__(parent=parent)
        self.proxies = proxies

    def run(self):
        if PluginManager.download_plugin(self.proxies):
            self.is_success_sig.emit(True)
        else:
            self.is_success_sig.emit(False)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ui = MainUI()
    ui.show()
    app.exec_()
