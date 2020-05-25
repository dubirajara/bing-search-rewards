import os
import shutil

import click
import requests


MSG_CHOICES = '''
Enter a firefox geckodriver to your system:\n
Linux32 [1]
Linux64 [2]
MacOs   [3]
Win32   [4]
Win64   [5]
'''''

VERSION_DISPATCHER = {
    '1': 'linux32.tar.gz',
    '2': 'linux64.tar.gz',
    '3': 'macos.tar.gz',
    '4': 'win32.zip',
    '5': 'win64.zip'
}


@click.command()
@click.option('--version', prompt=MSG_CHOICES, type=click.Choice(VERSION_DISPATCHER.keys()), show_choices=False)
@click.option('--email', prompt=True, default='')
@click.option('--password', prompt=True, default='', hide_input=True)
def create_config_env(version, email, password):
    save_geckodriver(VERSION_DISPATCHER[str(version)])
    config_env = f"""EMAIL={email}
PASS={password}
"""

    # Writing our configuration file to '.env'
    with open('.env', 'w') as configfile:
        configfile.write(config_env)
        print('Created the .env file successfully!')


def save_geckodriver(version):
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
