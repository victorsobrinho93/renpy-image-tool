from configparser import ConfigParser
from pathlib import Path


class Configuration(ConfigParser):
    def __init__(self, controller):
        super().__init__()
        if Path('settings.ini').is_file():
            self.read('settings.ini')
        else:
            self['Files'] = {
                'RpyFile': '',
                'RpyDirectory': '',
                'ImagesDirectory': '',
                'AudioDirectory': '',
                'Script': ''
            }
            self['Timing'] = {
                'DefaultTiming': '0.1',
            }
            with open('settings.ini', mode='w') as configfile:
                self.write(configfile)

    def set_(self, section, key, value):
        self.set(section, key, value)
        with open('settings.ini', 'w') as configfile:
            self.write(configfile)

    def rpy_directory(self):
        return self['Files']['RpyDirectory']

    def rpy_insert(self):
        return str(Path(self['Files']['RpyFile']).stem)

    def timing_insert(self):
        return self['Timing']['DefaultTiming']

    def write_ini(self):
        with open('settings.ini', 'w') as configfile:
            self.write(configfile)
