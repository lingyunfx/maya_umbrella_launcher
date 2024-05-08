from maya_umbrella_launcher.__version__ import __version__


class Trans:
    def __init__(self, cn, en):
        self.__dict = {'cn': cn, 'en': en}

    def __getitem__(self, item):
        return self.__dict[item]


WINDOW_TITLE = f'Maya Umbrella Launcher v{__version__}'
SETTING_FLAG = 'MAYA_UMBRELLA_SETTING_FLAG'

USER_NAME = 'loonghao'
REPO_NAME = 'maya_umbrella'

LAUNCHER_DOC_CN = """
如果不想破坏本地环境，可以选择从启动器启动Maya，
它会为你创建一个临时环境，并自动设置好maya_umbrella防病毒插件。
第一次使用，请先在设置面板指定插件安装目录。
"""

LAUNCHER_DOC_EN = """
If you don't want to damage the local environment, 
you can choose to launch Maya from the launcher. 

It will create a temporary environment for you ,
and automatically set up the maya_umbrella antivirus plugin.
 
For the first use, 
please specify the plugin installation directory in the settings panel.
"""

INSTALLER_DOC_CN = """
如果不想每次都通过启动器启动软件，
可以将maya_umbrella安装到系统环境（通过mod的方式）。
安装后，直接从桌面打开Maya即可加载插件。
第一次使用，请先在设置面板指定插件安装目录。
"""

INSTALLER_DOC_EN = """
If you do not want to launch the software through the launcher every time, 
you can install maya_umbrella into the system environment (via mod). 
After installation, you can directly open Maya from the desktop to load the plugin. 
For the first use, please specify the plugin installation directory in the settings panel first.
"""

# translation
LAUNCH_BUTTON = Trans('   启动Maya', '   Launch Maya')
LAUNCH_TAB = Trans('启动面板', 'launchpad')
INSTALL_TAB = Trans('本地安装', 'Local installation')
VERSION_LABEL = Trans('版本', 'Version')
MOD_LABEL = Trans('Mod目录', 'Mod Folder')
INSTALL_BUTTON = Trans('安装到Maya环境', 'Install to Maya')
REMOVE_BUTTON = Trans('从Maya环境卸载', 'Uninstall from Maya')
LAUNCHER_DESC = Trans(LAUNCHER_DOC_CN, LAUNCHER_DOC_EN)
INSTALL_DESC = Trans(INSTALLER_DOC_CN, INSTALLER_DOC_EN)

DOWNLOAD_BUTTON = Trans('下载', 'Download')
CHECK_UPDATE_BUTTON = Trans('检查更新', 'Check for updates')
SETTING_TITLE_LABEL = Trans('设置面板', 'Settings')
PLUGIN_FOLDER_LABEL = Trans('插件目录', 'Plug-in Folder')
PLUGIN_VERSION_LABEL = Trans('插件版本', 'Plug-in Version')
