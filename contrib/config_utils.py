import os
import shutil
import platform

import click
import requests


VERSION_DISPATCHER = {
    'linux32bit': 'linux32.tar.gz',
    'linux64bit': 'linux64.tar.gz',
    'darwin': 'macos.tar.gz',
    'windows32bit': 'win32.zip',
    'windows64bit': 'win64.zip'
}


@click.command()
@click.option('--email', prompt=True, default='')
@click.option('--password', prompt=True, default='', hide_input=True)
def create_config_env(email, password):
    config_env = f"""EMAIL={email}
PASS={password}
"""

    # Writing our configuration file to '.env'
    with open('.env', 'w') as configfile:
        configfile.write(config_env)
        print('Created the .env file successfully!')


def save_geckodriver():
    plataform_system = platform.system().lower()
    platform_version = plataform_system if plataform_system == 'darwin' else plataform_system + platform.architecture()[
        0]
    version = VERSION_DISPATCHER[platform_version]
    url = f'https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-{version}'
    file = url.split('/')[-1]
    response = requests.get(url)
    with open(file, 'wb') as f:
        f.write(response.content)
    shutil.unpack_archive(file, os.path.basename('geckodriver'))
    print('Created firefox geckodriver!')
    os.remove(file)


if __name__ == '__main__':
    create_config_env()
