import click
from decouple import config

from bing_rewards_utils import (get_driver_firefox, get_word_list, login,
                                wait_for)


@click.command()
@click.option('--mobile', default=False, help='rewards firefox mobile')
@click.option('--email', default=config('EMAIL'), help='microsoft email account')
@click.option('--password', default=config('PASS'), help='microsoft pass account')
def get_search_rewards(mobile, email, password):
    bing_search_url = config('BING_SEARCH_URL')

    search_count = 25 if mobile else 35

    driver = get_driver_firefox(mobile)
    login(driver, email, password)

    driver.get(bing_search_url)
    wait_for(5)

    for num, word in enumerate(get_word_list(search_count)):
        search_word = bing_search_url + word
        print(f'{str(num + 1)}. URL : {search_word}')
        try:
            driver.get(search_word)
            print('\t' + driver.find_element_by_tag_name('h2').text)
        except Exception as e1:
            print(e1)
        wait_for()
    driver.close()


if __name__ == '__main__':
    get_search_rewards()