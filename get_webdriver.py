import os
import shutil
import platform

import requests

FIREFOX_VERSION = {
    'linux32bit': 'linux32.tar.gz',
    'linux64bit': 'linux64.tar.gz',
    'darwin': 'macos.tar.gz',
    'windows32bit': 'win32.zip',
    'windows64bit': 'win64.zip'
}

EDGE_VERSION = {
    'linux64bit': 'linux64.zip',
    'darwin': 'mac64.zip',
    'windows32bit': 'win32.zip',
    'windows64bit': 'win64.zip'
}


def check_geckodriver_last_release():
    url = 'https://api.github.com/repos/mozilla/geckodriver/releases'
    try:
        tag_version = requests.get(url).json()[0]['tag_name']
    except Exception:
        tag_version = 'v0.27.0'
    return tag_version


def save_webdriver(webdriver):
    plataform_system = platform.system().lower()
    platform_version = plataform_system if plataform_system == 'darwin' else plataform_system + platform.architecture()[
        0]
    tag_version = check_geckodriver_last_release() if webdriver == 'geckodriver' else '113.0.1774.9'

    download_url = {
        'msedgedriver': f'https://msedgedriver.azureedge.net/{tag_version}/edgedriver_{EDGE_VERSION[platform_version]}',
        'geckodriver': f'https://github.com/mozilla/geckodriver/releases/download/{tag_version}/geckodriver-'
                       f'{tag_version}-{FIREFOX_VERSION[platform_version]}'
    }

    url = download_url[webdriver]
    file = url.split('/')[-1]
    response = requests.get(url)
    with open(file, 'wb') as f:
        f.write(response.content)
    shutil.unpack_archive(file, os.path.basename(webdriver))
    print(f'Created {webdriver}!')
    os.remove(file)
