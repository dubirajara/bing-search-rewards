# bing-search-rewards
Python script to win points in bing search rewards.

## How to use?

- Clone the repository:
```sh
git clone https://github.com/dubirajara/bing-search-rewards.git && cd bing-search-rewards
```

- Install the dependencies:
```sh
pip install -r requirements.txt
```

- And run **get_rewards.py**, you can run directly without parameters, in terminal will request you to input your microsoft email and password:
```sh
python get_rewards.py
```
or you can pass the flags **--email** and **--password**
```sh
python get_rewards.py --email YOUR-EMAIL@outlook.com --password YOURPASS
```
optional you can pass flag **--mobile** to win more points, emulating a mobile browser.
```sh
python get_rewards.py --mobile True --email YOUR-EMAIL@outlook.com --password YOURPASS
```
If you don't want to always pass the email and password parameters, you can run the **config_utils.py** script, which will save your credentials as environment variables:
```sh
python contrib/config_utils.py
```