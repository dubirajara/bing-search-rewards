import os
import shutil
import platform

import requests

VERSION_DISPATCHER = {
    'linux32bit': 'linux32.tar.gz',
    'linux64bit': 'linux64.tar.gz',
    'darwin': 'macos.tar.gz',
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


def save_geckodriver():
    plataform_system = platform.system().lower()
    platform_version = plataform_system if plataform_system == 'darwin' else plataform_system + platform.architecture()[
        0]
    version = VERSION_DISPATCHER[platform_version]
    tag_version = check_geckodriver_last_release()
    url = f'https://github.com/mozilla/geckodriver/releases/download/{tag_version}/geckodriver-{tag_version}-{version}'
    file = url.split('/')[-1]
    response = requests.get(url)
    with open(file, 'wb') as f:
        f.write(response.content)
    shutil.unpack_archive(file, os.path.basename('geckodriver'))
    print('Created firefox geckodriver!')
    os.remove(file)
