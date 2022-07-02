from time import time, gmtime, strftime
from os import path, curdir
import logger.errors as error

def validate_loglevel(loglevel: int) -> bool:
    _available_levels = ['0', '1']
    if not loglevel in _available_levels:
        return False
    return True    

def save_file(path: str, filename: str, data: str) -> None:
    with open(file=f'{path}/{filename}', mode='w') as file:
        file.write(data)
        file.close()

class Logger:
    def __init__(self, consolelog: int) -> None:
        self.cl = consolelog
        self.loglevel = '1'
        self.timeformat = '%d.%m.%y~%H-%M-%S'
        self.log_path = 'logs'
        self.filename = '{time}.log'
        self.data = ""
        self.update_log('info', 'Logger started!')
    
    def get_timestamp(self) -> str:
        return strftime(self.timeformat, gmtime(time()))

    def set_loglevel(self, loglevel: int) -> None:
        if not validate_loglevel(loglevel):
            raise error.UnknowLoggerLevel(f'Unknow log level {loglevel}')
        self.loglevel = loglevel
        self.update_log('info', 'Changed loglevel to ' + loglevel)

    def set_timeformat(self, timeformat: str) -> None:
        self.timeformat = timeformat
        self.update_log('info', 'Changed timeformat to ' + timeformat)

    def set_log_path(self, _path: str) -> None:
        self.log_path = _path
        self.update_log('info', 'Changed log path to ' + _path)

    def set_filename(self, filename: str) -> None:
        self.filename = filename
        self.update_log('info', 'Changed filename to ' + filename)

    def update_log(self, type: str, message: str, name = __name__) -> None:
        data = f'{self.get_timestamp()} ({name}) [{type}] : {message}'
        if self.cl == 1: print(data)
        self.data += data + "\n"
    
    def save_log(self) -> None:
        if self.loglevel == 0: 
            return

        self.update_log('info', 'Logger closing!')

        save_file(self.log_path, self.filename.format(time=self.get_timestamp()), data=self.data)