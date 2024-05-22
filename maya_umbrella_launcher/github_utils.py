import requests
import urllib3

urllib3.disable_warnings()


def get_latest_release(owner, repo):
    """
    获取仓库的最新release
    Return:
        返回一个字典，包含最新发布的json信息，格式如下:
            - tag_name 版本名
            - ['assets'][0]['browser_download_url'] 最新版zip包文件的url地址
    """

    url = f'https://api.github.com/repos/{owner}/{repo}/releases/latest'
    response = requests.get(url)
    if response.status_code == 200:
        tags = response.json()
        if tags:
            return tags
    return False


def download_release_files(file_url, file_save_path, proxies=None):
    """
    下载github release文件
    """
    proxies = proxies if proxies else {}
    try:
        with requests.get(file_url, stream=True, proxies=proxies) as r:
            r.raise_for_status()
            with open(file_save_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
                return True
    except Exception as e:
        print(e)
        return False
