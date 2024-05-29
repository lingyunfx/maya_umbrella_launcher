from PySide2 import QtCore
import constant as const


def get_language():
    """
    获取语言
    """
    setting = QtCore.QSettings(const.SETTING_FLAG)
    return setting.value('language', 'cn')


def set_language(language):
    """
    设置语言
    """
    setting = QtCore.QSettings(const.SETTING_FLAG)
    setting.setValue('language', language)


class TranslatorText:

    def __init__(self, cn, en):
        self.__dict = {'cn': cn, 'en': en}

    def __str__(self):
        return self.__dict[get_language()]

    @property
    def text(self):
        return self.__dict[get_language()]


# widgets translation
installer_doc_cn = """
如果不想每次都通过启动器启动软件，
可以将maya_umbrella安装到系统环境（通过mod的方式）。
安装后，直接从桌面打开Maya即可加载插件。
(第一次使用，请先在设置面板指定插件安装目录)
"""

installer_doc_en = """
If you do not want to launch the software through the launcher every time, 
you can install maya_umbrella into the system environment (via mod). 
After installation, you can directly open Maya from the desktop to load the plugin. 
For the first use, please specify the plugin installation directory in the settings panel first.
"""

launcher_doc_cn = """
选择从启动器启动Maya，不会破坏本地环境，
启动后，会自动设置好maya_umbrella防病毒插件。

(第一次使用，请先在设置面板指定插件安装目录)
"""

launcher_doc_en = """
If you don't want to damage the local environment, 
you can choose to launch Maya from the launcher. 

It will create a temporary environment for you ,
and automatically set up the maya_umbrella antivirus plugin.

For the first use, 
please specify the plugin installation directory in the settings panel.
"""

launch_bt = TranslatorText('   启动Maya', '   Launch Maya')
launch_tab = TranslatorText('启动面板', 'launchpad')
install_tab = TranslatorText('本地安装', 'Local installation')
version_label = TranslatorText('版本', 'Version')
mod_label = TranslatorText('Mod文件', 'Mod File')
install_bt = TranslatorText('安装到Maya环境', 'Install to Maya')
remove_bt = TranslatorText('从Maya环境卸载', 'Uninstall from Maya')
launcher_desc = TranslatorText(launcher_doc_cn, launcher_doc_en)
install_desc = TranslatorText(installer_doc_cn, installer_doc_en)

download_bt = TranslatorText('下载', 'Download')
check_update_bt = TranslatorText('检查更新', 'Check for updates')
setting_title_label = TranslatorText('设置面板', 'Settings')
plugin_folder_label = TranslatorText('插件目录', 'Plug-in Folder')
plugin_version_label = TranslatorText('插件版本', 'Plug-in Version')


# text translation
no_plugin_folder = TranslatorText('请先指定插件目录', 'Please specify the plugin folder first')
path_not_exists = TranslatorText('路径不存在: {0}', 'Path does not exist: {0}')
path_already_exists = TranslatorText('路径已存在: {0}', 'Path already exists: {0}')
is_download_new_version = TranslatorText('发现新版本{0},\n是否下载新版本？',
                                         'New version {0} found,\nDo you want to download the new version?')
already_latest_version = TranslatorText('已经是最新版本', 'Already the latest version')
downloading = TranslatorText('正在下载...', 'Downloading...')
download_failed = TranslatorText('下载失败', 'Download failed')
download_success = TranslatorText('下载成功', 'Download successful')
unable_found_script = TranslatorText('找不到脚本路径，请设置插件路径，然后下载插件!',
                                     'Cannot find the script path, please set the plugin path first!')
unable_found_maya = TranslatorText('找不到Maya版本: {0}', 'Cannot find Maya version: {0}')
install_success = TranslatorText('安装成功', 'Installation successful')
uninstall_success = TranslatorText('卸载成功', 'Uninstall successful')
install_failed = TranslatorText('安装失败', 'Installation failed')

command_description = TranslatorText('这是一个命令行模式', 'This is a command line mode')
run_download = TranslatorText('执行下载操作', 'Run download operation')
specify_version = TranslatorText('指定一个版本, 比如2018, 2023', 'Specify a version, such as 2018, 2023')
run_install = TranslatorText('执行安装操作', 'Run installation operation')
run_uninstall = TranslatorText('执行卸载操作', 'Run uninstall operation')
already_installed_status = TranslatorText('已安装', 'Already installed')
not_installed_status = TranslatorText('未安装', 'Not installed')
proxy_label = TranslatorText('开启代理', 'Enable proxy')
