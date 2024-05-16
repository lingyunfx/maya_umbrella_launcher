import os
import argparse


import translator as tr
from core import (get_python_path_env, launch_maya, install_to_maya, set_plugin_folder,
                  download_plugin, get_maya_app_path, uninstall_from_maya, get_plugin_folder)


def main():
    parser = argparse.ArgumentParser(description=tr.command_description.text)

    parser.add_argument('-p', '--path', type=str, nargs='?', const='', help=tr.no_plugin_folder.text)
    parser.add_argument('-d', '--download', action='store_true', help=tr.run_download.text)
    parser.add_argument('-s', '--start', type=int, help=tr.specify_version.text)
    parser.add_argument('-i', '--install', type=int, help=tr.run_install.text)
    parser.add_argument('-u', '--uninstall', type=int, help=tr.run_uninstall.text)

    args = parser.parse_args()

    if args.path:
        if os.path.isdir(args.path):
            set_plugin_folder(args.path)
        else:
            print(tr.path_not_exists.text.format(args.path))
            return
    elif args.path == '':
        print(get_plugin_folder())

    if args.download:
        if not download_plugin(overwrite=True):
            return

    if args.start:
        envs = get_python_path_env()
        maya_app_path = get_maya_app_path(maya_version=args.start)
        launch_maya(maya_path=maya_app_path,
                    envs=envs
                    )
        return

    if args.install:
        install_to_maya(maya_version=args.install)
        print(tr.run_install.text)
        return

    if args.uninstall:
        uninstall_from_maya(maya_version=args.uninstall)
        print(tr.run_uninstall.text)
        return


if __name__ == "__main__":
    main()
