# bing-search-rewards
Python script to win points in bing search rewards.

Inspired by Medium blog post: https://medium.com/@prateekrm/earn-500-daily-microsoft-rewards-points-automatically-with-a-simple-python-program-38fe648ff2a9

## How to use?

**IMPORTANT**: Requires Python 3.10 or newer. It supports firefox and edge webdrivers, but I advise to use edge webdriver, it gives better results and earns more rewards points.

- Clone the repository:
```sh
git clone https://github.com/dubirajara/bing-search-rewards.git && cd bing-search-rewards
```

- Install the dependencies:
```sh
pip install -r requirements.txt
```

- And run **get_rewards.py**, you can run directly without parameters, in terminal will your microsoft email and password:
```sh
python get_rewards.py
```
- Or you can pass the flags **--browser** **--email** and **--password**
```sh
python get_rewards.py --browser edge --email YOUR-EMAIL@outlook.com --password YOURPASS
```
- Optional you can pass flag **--mobile** to win more points, emulating a mobile browser.
```sh
python get_rewards.py --mobile True --email YOUR-EMAIL@outlook.com --password YOURPASS
```
- If you don't want to always pass the email and password parameters, you can run the **config_utils.py** script, which will save your credentials as environment variables:
```sh
python contrib/config_utils.py
```
