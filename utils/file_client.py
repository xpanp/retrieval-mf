import requests
from urllib.parse import urljoin


def upload(base_url: str, filename: str, dir: str) -> str:
    '''
        上传文件至文件服务器
        url：url需拼接后缀upload
        filename：本地文件路径
        dir：指定上传至服务器后的目录，便于以数据库区分
    '''
    files = {'file': open(filename, 'rb')}
    data = {'dir': dir}
    url = urljoin(base_url, 'upload')
    print(f'upload url: {url}')
    r = requests.post(url, files=files, data=data, timeout=3)
    return r.json()['url']


def get_download_url(base_url: str, filepath: str) -> str:
    '''
        拼接获取实际的下载地址

        Note: 'download/'中的斜杠必须添加, 否则可能被替换掉
    '''
    url = urljoin(urljoin(base_url, 'download/'), filepath)
    return url
