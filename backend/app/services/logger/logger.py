import logging
import logging.config
import os

import yaml

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(ROOT_DIR, 'logger.yml')


def setup_logging(path=CONFIG_PATH, default_level=logging.INFO):

    if os.path.exists(path):
        with open(path, 'rt') as f:
            try:
                config = yaml.safe_load(f.read())
                logging.config.dictConfig(config)
            except Exception as e:
                print(e)
                print('Error in Logging Configuration. Using default configs')
                logging.basicConfig(level=default_level)
    else:
        logging.basicConfig(level=default_level)
        print('Failed to load configuration file. Using default configs')


if __name__ == "__main__":
    setup_logging()
    l = logging.getLogger("ENDPOINT")
    l.log(logging.INFO, "Hello World")
