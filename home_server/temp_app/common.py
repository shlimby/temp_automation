import json
from django.conf import settings
import os

DEV_SETTINGS = os.path.join(settings.BASE_DIR, 'settings_dev.json')
DEPLOY_SETTINGS = os.path.join(settings.BASE_DIR, 'settings.json')

# Check if file Exists
if os.path.isfile(DEV_SETTINGS):
    SETTING_File = DEV_SETTINGS
else:
    SETTING_File = DEPLOY_SETTINGS


def get_settings():
    """Read settings file and return decoded object"""
    return json.loads(open(SETTING_File, "r").read())


def set_settings(settings: object):
    """Overwrite settings with given object"""

    # write settings in a nice way
    with open(SETTING_File, 'w', encoding='utf-8') as f:
        json.dump(settings, f, ensure_ascii=False, indent=4)
