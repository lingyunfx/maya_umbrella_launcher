import os

from PySide2 import QtCore

import maya_umbrella_launcher.translator as tr
import maya_umbrella_launcher.constant as const
from maya_umbrella_launcher.log import logger
from maya_umbrella_launcher.github_utils import get_latest_release, download_release_files
from maya_umbrella_launcher.filesystem import (create_folder_if_not_exist, extract_zip,
                                               validate_folder_exist, MayaSystem)


class UserSetting(object):
    """
    用户设置
    """

    @staticmethod
    def get(key, default=None):
        setting = QtCore.QSettings(const.SETTING_FLAG, default)
        return setting.value(key)

    @staticmethod
    def set(key, value):
        setting = QtCore.QSettings(const.SETTING_FLAG)
        setting.setValue(key, value)


class PluginManager:
    """
    插件管理
    """

    @classmethod
    def get_maya_umbrella_script_folder(cls):
        """
        获取maya_umbrella的script目录
        """
        plugin_folder = UserSetting.get('plugin_folder')
        if not validate_folder_exist(plugin_folder):
            return logger.warning(tr.no_plugin_folder.text)

        versions = cls.get_local_version_list(plugin_folder)
        if not versions:
            return logger.error(tr.unable_found_script.text)

        script_folder = os.path.join(plugin_folder, max(versions), 'maya_umbrella', 'scripts')
        if not validate_folder_exist(script_folder):
            return logger.error(tr.unable_found_script.text)

        return script_folder

    @classmethod
    def get_python_path_env(cls):
        """
        获取Python路径环境变量
        """
        script_folder = cls.get_maya_umbrella_script_folder()
        if not script_folder:
            return False

        envs_copy = os.environ.copy()
        envs_copy['PYTHONPATH'] = envs_copy.get('PYTHONPATH', '') + f';{script_folder}'
        return envs_copy

    @staticmethod
    def get_local_version_list(plugin_folder):
        """
        获取插件的所有版本目录名
        """
        if not validate_folder_exist(plugin_folder):
            return []

        version_list = [ver for ver in os.listdir(plugin_folder)
                        if os.path.isdir(os.path.join(plugin_folder, ver))
                        and ver.startswith('v')]
        return version_list

    @staticmethod
    def download_plugin(proxies=None, overwrite=False):
        """
        下载插件，解压，返回解压后的目录
        """

        # 获取插件目录
        plugin_folder = UserSetting.get('plugin_folder')
        if not validate_folder_exist(plugin_folder):
            return logger.warning(tr.no_plugin_folder.text)

        # 获取最新tag
        latest_tag = get_latest_release(owner=const.USER_NAME,
                                        repo=const.REPO_NAME)

        # 获取插件版本目录
        plugin_version_folder = os.path.join(plugin_folder, str(latest_tag['tag_name']))
        if os.path.isdir(plugin_version_folder) and not overwrite:
            logger.warning(tr.path_already_exists.text.format(plugin_version_folder))
            return False
        create_folder_if_not_exist(plugin_version_folder)
        zip_path = os.path.join(plugin_version_folder, f'{const.REPO_NAME}.zip')

        # 开始下载
        try:
            download_release_files(file_url=latest_tag['assets'][0]['browser_download_url'],
                                   file_save_path=zip_path,
                                   proxies=proxies)
        except Exception as e:
            logger.error(tr.download_failed.text + '\n' + str(e))
            return False

        if not os.path.exists(zip_path):
            return logger.error(tr.download_failed.text)

        un_zip_folder = extract_zip(zip_path=zip_path)
        os.remove(zip_path)

        return un_zip_folder

    @staticmethod
    def get_latest_version():
        """
        获取插件最新版本号
        """
        return get_latest_release(owner=const.USER_NAME, repo=const.REPO_NAME)['tag_name']


class PluginInstaller:
    """
    插件安装器
    """

    @staticmethod
    def install(maya_version):
        module_folder = MayaSystem.get_maya_module_folder(version_number=maya_version)
        if not validate_folder_exist(module_folder):
            return False

        script_folder = PluginManager.get_maya_umbrella_script_folder()
        if not script_folder:
            return False

        script_folder = os.path.dirname(script_folder)
        mod_file = os.path.join(module_folder, 'maya_umbrella.mod')

        if os.path.isfile(mod_file):
            os.remove(mod_file)

        with open(mod_file, 'w') as f:
            f.write(f'+ maya_umbrella any {script_folder}\n')

        return True

    @staticmethod
    def uninstall(maya_version):
        module_folder = MayaSystem.get_maya_module_folder(version_number=maya_version)
        mod_file = os.path.join(module_folder, 'maya_umbrella.mod')
        if os.path.isfile(mod_file):
            os.remove(mod_file)
