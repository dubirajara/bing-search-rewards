import os
import shutil
import platform

import httpx

from constants import EDGE_VERSION, FIREFOX_VERSION, GECKODRIVER, GECKODRIVER_URL, MSEDGEDRIVER_VERSION


def check_geckodriver_last_release():
    try:
        tag_version = httpx.get(GECKODRIVER_URL, follow_redirects=True).json()[0]['tag_name']
    except Exception:
        tag_version = 'v0.27.0'
    return tag_version


def save_webdriver(webdriver):
    plataform_system = platform.system().lower()
    platform_version = plataform_system if plataform_system == 'darwin' else plataform_system + platform.architecture()[
        0]
    tag_version = check_geckodriver_last_release() if webdriver == GECKODRIVER else MSEDGEDRIVER_VERSION

    download_url = {
        'msedgedriver': f'https://msedgedriver.azureedge.net/{tag_version}/edgedriver_{EDGE_VERSION[platform_version]}',
        'geckodriver': f'https://github.com/mozilla/geckodriver/releases/download/{tag_version}/geckodriver-'
                       f'{tag_version}-{FIREFOX_VERSION[platform_version]}'
    }

    url = download_url[webdriver]
    file = url.split('/')[-1]
    response = httpx.get(url, follow_redirects=True)
    with open(file, 'wb') as f:
        f.write(response.content)
    shutil.unpack_archive(file, os.path.basename(webdriver))
    print(f'Created {webdriver}!')
    os.remove(file)
