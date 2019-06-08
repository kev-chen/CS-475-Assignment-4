#!/usr/bin/python3

import json

class Config:
    
    settings = json.load(open('settings.json', 'r'))
    
    """
     Returns the value of a setting from the settings file
     @return None if no setting found
    """
    @staticmethod
    def setting(settingName):
        if (settingName in Config.settings):
            return Config.settings[settingName]
        else:
            return None