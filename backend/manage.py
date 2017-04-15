#!/usr/bin/env python
import os
import sys


if __name__ == "__main__":

    # CHANGED manage.py will use development settings by
    # default. Change the DJANGO_SETTINGS_MODULE environment variable
    # for using the environment specific settings file.
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ucaptive.settings")
    os.environ.setdefault('DJANGO_CONFIGURATION', 'Dev')

    from configurations.management import execute_from_command_line

    execute_from_command_line(sys.argv)
    

# Usage eg.    
# manage.py runserver --settings=mounagroup.settings --configuration=Dev
# manage.py shell --settings=mounagroup.settings --configuration=Dev
