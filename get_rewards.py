import click
from decouple import config

from bing_rewards_utils import (get_driver_firefox, get_word_list, login,
                                wait_for, get_driver_edge)
from constants import BING_SEARCH_URL


def callback(ctx, param, value):
    if not value:
        return config('PASS', '')
    return value


@click.command()
@click.option('--mobile', '-m', default=False, help='rewards firefox mobile')
@click.option('--email', '-e', prompt=True if not config('EMAIL', '') else False, default=lambda: config('EMAIL', ''),
              help='microsoft email account')
@click.option('--password', '-p', prompt=True if not config('PASS', '') else False, callback=callback, default='',
              help='microsoft pass account', hide_input=True)
@click.option('--browser', '-b', default='edge', help='webdriver browser')
def get_search_rewards(mobile, email, password, browser, search_count=35):

    drivers = {
        'firefox': get_driver_firefox,
        'edge': get_driver_edge
    }

    if browser in drivers.keys():
        driver = drivers[browser](mobile)
        print(f'Start {driver.name} webdriver\n')
        login(driver, email, password)

        driver.get(BING_SEARCH_URL)
        wait_for(5)
        print('starting search keywords to rewards\n')
        for num, word in enumerate(get_word_list(search_count), start=1):
            search_word = BING_SEARCH_URL + word
            print(f'{num}: {search_word}')
            try:
                driver.get(search_word)
            except Exception as e:
                print(e)
            wait_for()
        driver.close()
    else:
        print(f'Browser {browser} not supported')


if __name__ == '__main__':
    get_search_rewards()
