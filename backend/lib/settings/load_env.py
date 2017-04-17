from __future__ import unicode_literals

from os.path import dirname, join

import dotenv


def load_env():
    """Get the path to the .env file and load it."""
    dotenv.read_dotenv('/home/ceduth/Documents/Devl/Python/Projects/ucaptive.mj/backend/ucaptive/settings/env/l0-ceduth.env')
