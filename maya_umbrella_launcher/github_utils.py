import requests
import urllib3

from maya_umbrella_launcher import constant as const

urllib3.disable_warnings()


def get_latest_tag(owner, repo):
    """
    获取仓库的最新release
    Return:
        返回一个字典，包含键:
            - name 为版本名称
            - zipball_url 为zip包文件的url地址
    """
    url = f'https://api.github.com/repos/{owner}/{repo}/tags'
    response = requests.get(url)
    if response.status_code == 200:
        tags = response.json()
        if tags:
            return tags[0]
    return False


def download_release_files(file_url, file_save_path):
    """
    下载release文件
    """
    try:
        with requests.get(file_url, stream=True) as r:
            r.raise_for_status()
            with open(file_save_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
                return True
    except Exception as e:
        print(e)
        return False


if __name__ == '__main__':
    # for test
    latest_tag = get_latest_tag(owner=const.USER_NAME, repo=const.REPO_NAME)
    download_release_files(file_url=latest_tag['zipball_url'],
                           file_save_path=fr'D:\test\{const.REPO_NAME}_{latest_tag["name"]}.zip')
