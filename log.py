from datetime import datetime

class Logging:
    def __init__(self, LOG_FILE:bool, CONSOLE_LOGGING:bool):
        self.LOG_FILE=LOG_FILE
        self.CONSOLE_LOGGING=CONSOLE_LOGGING
        pass

    def logger(self, value:str, error:bool=False):

        logfile=open(self.LOG_FILE, 'a+')

        now=datetime.now()
        current_time=now.strftime("%H:%M:%S")
        value=f'[{current_time}] {value}'

        if error:
            raise Exception(value)

        if self.CONSOLE_LOGGING:
            print(value)
        
        logfile.write(value+'\n')
        logfile.close()