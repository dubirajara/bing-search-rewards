import click


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


if __name__ == '__main__':
    create_config_env()
