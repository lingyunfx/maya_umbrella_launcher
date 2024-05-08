import os
import tempfile
import zipfile


def extract_zip(zip_path, extract_to=None):
    """
    解压文件
    """
    if extract_to is None:
        extract_to = os.path.dirname(zip_path)

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
        print('Files extracted to: {extract_to}')


def get_maya_module_folder(version_number):
    document_path = os.path.join(os.path.expanduser('~'), 'Documents')
    maya_module_folder = os.path.join(document_path, 'maya', str(version_number), 'modules')
    return maya_module_folder
