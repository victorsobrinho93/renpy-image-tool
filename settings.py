from configparser import ConfigParser
from pathlib import Path


class Parameters(ConfigParser):
    def __init__(self):
        super().__init__()
        if Path('settings.ini').is_file():
            self.read('settings.ini')
        else:
            self['Files'] = {
                'RpyFile': '',
                'RpyDirectory': '',
                'ImagesDirectory': '',
            }
            self['Timing'] = {
                'DefaultTiming': '0.1',
            }
            with open('settings.ini', mode='w') as configfile:
                self.write(configfile)

    def rpy(self, value):
        if value != '':
            self.out()

    def return_rpy(self):
        return str(Path(self['Files']['RpyFile']).stem)

    # I can possibly turn this into a **kwarg
    def update_params(self, value, **key):
        """Function to update the settings.ini file"""
        if key.get('rpy'):
            self.set('Files', 'RpyFile', value)
        elif key.get('rpy_dir'):
            self.set('Files', 'RpyDirectory', value)
        elif key.get('img_dir'):
            self.set('Files', 'ImagesDirectory', value)
        elif key.get('timing'):
            self.set('Timing', 'DefaultTiming', value)
        with open('settings.ini', 'w') as configfile:
            self.write(configfile)

    def update_timing(self, value): #This is due to some refactoring, v4 and beyond.
        if self.if_num(value):
            self.set('Timing', 'DefaultTiming', value)
            self.write_ini()

    def write_ini(self):
        with open('settings.ini', 'w') as configfile:
            self.write(configfile)

    # TODO: ADD CUSTOM CONDITIONS AND SUFFIXES TO .INI SO YOU CAN REPEAT IT. (v4...)
    def custom_params(self, alt, cnd):
        if not self.has_section('Suffixes'):
            self.add_section('Suffixes')
        for obj in alt:
            pass
        if not self.has_section('Conditions'):
            self.add_section('Conditions')
        for obj in cnd:
            pass

    def if_num(self, value):
        try:
            return float(value)
        except ValueError:
            return False
