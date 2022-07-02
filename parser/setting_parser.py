from logger.log import Logger
import parser.errors as error
from os import path

__SETTING_FILE__ = 'setting'

class Parser:
    def __init__(self) -> None:
        if not path.exists(__SETTING_FILE__):
            raise error.SettingFileNotFound(f'error: Setting file in {__SETTING_FILE__} not found!')
        self.available_settings = ['log_path', 'filename', 'timeformat', 'loglevel', 'token']
    
    def get_settings(self) -> dict[str, str]:
        _parsed_data: list[str]
        with open(__SETTING_FILE__, mode='r') as setting:
            _parsed_data = setting.readlines()
            setting.close()
        
        data = {}
        for line in _parsed_data:
            if line == '\n':
                continue
            if line.startswith('#'):
                continue
            setting, value = line.split('=')
            if not setting in self.available_settings:
                continue
            data[setting] = value.replace('\n', '')
        return data 