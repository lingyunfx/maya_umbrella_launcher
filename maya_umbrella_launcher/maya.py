import os
import winreg
import subprocess as sp


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
    bin_root = os.path.join(root, 'bin')
    return {'maya_root': root, 'bin_root': bin_root}


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


def launch_maya(maya_path, envs):
    """
    启动maya
    """
    sp.Popen(maya_path, env=envs, cwd=os.path.dirname(maya_path))


if __name__ == '__main__':
    # for test
    installed_mayas = get_installed_maya_versions()
    for number in installed_mayas:
        print(number)
        print(get_maya_app_path(maya_version=number))
