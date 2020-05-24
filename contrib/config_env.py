import os
import shutil
from urllib.request import urlretrieve

import click


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
@click.option('--email', prompt=True, default='')
@click.option('--password', prompt=True, default='', hide_input=True)
@click.option('--version', prompt=MSG_CHOICES, type=click.Choice(VERSION_DISPATCHER.keys()), show_choices=False)
def create_config_env(email, password, version):
    save_geckodriver(VERSION_DISPATCHER[str(version)])
    print('Created firefox geckodriver.')
    config_env = f"""EMAIL={email}
PASS={password}
RANDOM_WORDS_URL=https://www.randomlists.com/data/words.json
BING_LOGIN_URL=https://login.live.com/
BING_SEARCH_URL=http://www.bing.com/search?q=
"""

    # Writing our configuration file to '.env'
    with open('.env', 'w') as configfile:
        configfile.write(config_env)
        print('Created the .env file successfully.')


def save_geckodriver(version):
    zip_url = f'https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-{version}'
    zip_file = zip_url.split('/')[-1]
    urlretrieve(zip_url, zip_file)
    shutil.unpack_archive(zip_file, os.path.basename('geckodriver'))
    os.remove(zip_file)


if __name__ == '__main__':
    create_config_env()
