import json
import os

import requests


def download_txt_file(url, local_filename):
    response = requests.get(url)
    path = os.getcwd()
    path_without_filename = path + "/sing-box/"
    if not os.path.exists(path_without_filename):
        os.makedirs(path_without_filename)
    if response.status_code == 200:
        with open(path_without_filename + local_filename, 'wb') as file:
            file.write(response.content)
        print(f'文件已保存到 {local_filename}')
    else:
        print(f'下载失败，状态码：{response.status_code}')


if __name__ == '__main__':
    # 读取当前路径下的 config.json 文件
    with open('config.json', 'r') as file:
        data = json.load(file)

    # 假设 JSON 文件中有一个名为 'settings' 的数组
    configs = data.get('configs', [])

    # 遍历数组中的对象
    for config in configs:
        name = config.get('name')
        url = config.get('url')
        file_name = url.split('/')[-1]
        print(f'Name: {name}, file_name: {file_name}, url: {url}')
        download_txt_file(url, file_name)
