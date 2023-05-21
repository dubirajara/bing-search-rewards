import click
from decouple import config

from bing_rewards_utils import (get_driver_firefox, get_word_list, login,
                                wait_for, get_driver_edge)

BING_SEARCH_URL = 'http://www.bing.com/search?q='

DRIVERS = {
    'firefox': get_driver_firefox,
    'edge': get_driver_edge
}


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
def get_search_rewards(mobile, email, password, browser):
    search_count = 25 if mobile else 35

    if browser in DRIVERS.keys():
        driver = DRIVERS[browser](mobile)
        print(f'Start {driver.name} webdriver\n')
        login(driver, email, password)

        driver.get(BING_SEARCH_URL)
        wait_for(5)
        print('starting search keywords to rewards\n')
        for num, word in enumerate(get_word_list(search_count)):
            search_word = BING_SEARCH_URL + word
            print(f'{str(num + 1)}. URL : {search_word}')
            try:
                driver.get(search_word)
                print('\t' + driver.find_element('tag name', 'h2').text)
            except Exception as e:
                print(e)
            wait_for()
        driver.close()
    else:
        print(f'Browser {browser} not supported')


if __name__ == '__main__':
    get_search_rewards()
