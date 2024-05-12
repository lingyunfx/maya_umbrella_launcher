import os
import winreg
import zipfile

from maya_umbrella_launcher.log import logger
from maya_umbrella_launcher import translator as tr


def extract_zip(zip_path, extract_to=None):
    """
    解压文件
    """
    if extract_to is None:
        extract_to = zip_path.replace('.zip', '')

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
        print(f'Files extracted to: {extract_to}')

    return extract_to


def get_document_folder():
    """
    获取文档目录
    """
    return os.path.join(os.path.expanduser('~'), 'Documents')


def get_maya_module_folder(version_number):
    """
    获取maya模块目录
    """
    document_path = get_document_folder()
    maya_module_folder = os.path.join(document_path, 'maya', str(version_number), 'modules')
    return maya_module_folder


def get_maya_app_path(maya_version):
    """
    获取指定maya版本的程序路径
    """
    try:
        key = winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            f'SOFTWARE\\Autodesk\\Maya\\{maya_version}\\Setup\\InstallPath',
        )
        root, _ = winreg.QueryValueEx(key, "MAYA_INSTALL_LOCATION")
        if not os.path.isdir(root):
            print('Failed to locate the appropriate Maya path in the registration list.')
    except OSError:
        return
    app_path = os.path.join(root, 'bin', 'maya.exe')
    return app_path


def get_installed_maya_versions():
    """
    列出所有本地安装的maya版本
    Return:
        由版本号组成的列表
    """
    maya_versions = []
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 'SOFTWARE\\Autodesk\\Maya') as key:
            i = 0
            while True:
                try:
                    version_number = winreg.EnumKey(key, i)
                    if version_number.isdigit():
                        maya_versions.append(version_number)
                except OSError:
                    break
                i += 1
    except Exception as e:
        print(f'Error accessing registry: {e}')

    return maya_versions


def create_folder_if_not_exist(folder_path):
    if not os.path.isdir(folder_path):
        os.makedirs(folder_path)


def validate_folder_exist(folder_path):
    if not os.path.isdir(folder_path):
        logger.warning(tr.path_not_exists.text.format(folder_path))
        return False
    return True
