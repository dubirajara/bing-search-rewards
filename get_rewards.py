import click
from decouple import config

from bing_rewards_utils import (get_driver_firefox, get_word_list, login,
                                wait_for)

BING_SEARCH_URL = 'http://www.bing.com/search?q='


def callback(ctx, param, value):
    if not value:
        return config('PASS', '')
    return value


@click.command()
@click.option('--mobile', default=False, help='rewards firefox mobile')
@click.option('--email', prompt=True, default=lambda: config('EMAIL', ''), help='microsoft email account')
@click.option('--password', prompt=True, callback=callback, default='', help='microsoft pass account', hide_input=True)
def get_search_rewards(mobile, email, password):
    search_count = 25 if mobile else 35

    driver = get_driver_firefox(mobile)
    login(driver, email, password)

    driver.get(BING_SEARCH_URL)
    wait_for(5)

    for num, word in enumerate(get_word_list(search_count)):
        search_word = BING_SEARCH_URL + word
        print(f'{str(num + 1)}. URL : {search_word}')
        try:
            driver.get(search_word)
            print('\t' + driver.find_element_by_tag_name('h2').text)
        except Exception as e:
            print(e)
        wait_for()
    driver.close()


if __name__ == '__main__':
    get_search_rewards()
