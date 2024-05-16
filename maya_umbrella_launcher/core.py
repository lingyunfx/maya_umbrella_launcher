import os
import subprocess as sp

from PySide2 import QtCore

from maya_umbrella_launcher.log import logger
from maya_umbrella_launcher import translator as tr
from maya_umbrella_launcher import constant as const
from maya_umbrella_launcher.github_utils import get_latest_release, download_release_files
from maya_umbrella_launcher.filesystem import (create_folder_if_not_exist, extract_zip, validate_folder_exist,
                                               get_maya_app_path, get_maya_module_folder)


def get_plugin_latest_version():
    """
    获取插件最新版本号
    """
    return get_latest_release(owner=const.USER_NAME, repo=const.REPO_NAME)['tag_name']


def get_plugin_folder():
    """
    获取插件目录
    """
    setting = QtCore.QSettings(const.SETTING_FLAG)
    return setting.value('plugin_folder')


def set_plugin_folder(path):
    """
    设置插件目录
    """
    setting = QtCore.QSettings(const.SETTING_FLAG)
    setting.setValue('plugin_folder', path)


def download_plugin(overwrite=False):
    """
    下载插件，解压，返回解压后的目录
    """

    # 获取插件目录
    plugin_folder = get_plugin_folder()
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
                               file_save_path=zip_path)
    except Exception as e:
        logger.error(tr.download_failed.text + '\n' + str(e))
        return False

    un_zip_folder = extract_zip(zip_path=zip_path)
    os.remove(zip_path)

    return un_zip_folder


def get_versions(plugin_folder):
    """
    获取插件的所有版本目录名
    """
    if not validate_folder_exist(plugin_folder):
        return []

    versions = [ver for ver in os.listdir(plugin_folder)
                if os.path.isdir(os.path.join(plugin_folder, ver))
                and ver.startswith('v')]
    return versions


def get_script_folder():
    """
    获取脚本目录
    """
    plugin_folder = get_plugin_folder()
    if not validate_folder_exist(plugin_folder):
        return logger.warning(tr.no_plugin_folder.text)

    versions = get_versions(plugin_folder)
    if not versions:
        return logger.error(tr.unable_found_script.text)

    script_folder = os.path.join(plugin_folder, max(versions), 'maya_umbrella', 'scripts')
    if not validate_folder_exist(script_folder):
        return logger.error(tr.unable_found_script.text)

    return script_folder


def get_python_path_env():
    """
    获取Python路径环境变量
    """
    script_path = get_script_folder()
    if not script_path:
        return False

    envs_copy = os.environ.copy()
    envs_copy['PYTHONPATH'] = envs_copy.get('PYTHONPATH', '') + f';{script_path}'
    return envs_copy


def launch_maya(maya_path, envs):
    sp.Popen(maya_path, env=envs, cwd=os.path.dirname(maya_path))


def install_to_maya(maya_version):
    module_folder = get_maya_module_folder(version_number=maya_version)
    if not validate_folder_exist(module_folder):
        return False

    script_folder = get_script_folder()
    if not script_folder:
        return False

    script_folder = os.path.dirname(script_folder)

    mod_file = os.path.join(module_folder, 'maya_umbrella.mod')

    if os.path.isfile(mod_file):
        return logger.warning(tr.path_already_exists.text.format(mod_file))

    with open(mod_file, 'w') as f:
        f.write(f'+ maya_umbrella any {script_folder}\n')


def uninstall_from_maya(maya_version):
    module_folder = get_maya_module_folder(version_number=maya_version)
    mod_file = os.path.join(module_folder, 'maya_umbrella.mod')
    if os.path.isfile(mod_file):
        os.remove(mod_file)


if __name__ == '__main__':
    # 1.设置插件路径
    set_plugin_folder(r'D:\test')

    # 2.下载插件
    download_plugin()

    # 3.获取环境
    envs = get_python_path_env()

    # 4.获取maya软件路径
    maya_app_path = get_maya_app_path(maya_version='2018')

    # 5.启动maya
    launch_maya(maya_path=maya_app_path,
                envs=envs
                )
