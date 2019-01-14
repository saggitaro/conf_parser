from copy import deepcopy
import itertools
import re

class Config:
    def __init__(self, cfg=None):
        if cfg is None:
            self.config = dict()
        elif isinstance(cfg, Config):
            self.config = deepcopy(cfg.config)

    def add_section(self, section, params=None):
        if params is None:
            self.config[section.upper()] = {} 
        elif isinstance(params, dict):
            self.config[section.upper()] = params
        #TODO raise exception when params neither None and dict
        else:
            pass

    def add_param(self, section_name, param):
        if isinstance(param, dict):
            if self.config[section_name.upper()]:
                self.config[section_name.upper()].update(param)
            else:
                self.config[section_name.upper()] = param

    def print_to_file(self, filename):
        with open(filename, 'w') as f:
            for section, params in self.config.items():
                f.write(section + '\n')
                for param_name, param_values in params.items():
                    f.write(param_name + '=' + str(param_values) + '\n')
    
    def read_from_file(self, filename):
        with open(filename, 'r') as f:
            config, delims = list(), list()
            for line in f:
                config.append(line.replace('\n', ''))

        for line in config:
            if re.match('[A-Z]+', line):
                delims.append(line)

        sections = [list(y) for x, y in itertools.groupby(config, lambda z: z in delims) if not x]
        for delim, section in zip(delims, sections):
            dic = {x:y for x, y in (param.split('=') for param in section)}
            self.config[delim] = dic

cfg = Config()
cfg.add_section('DEFAULT', {'username':'mr_sam', 'password':12345})
cfg.add_section('NETWORK', {'address':'localhost', 'port':9090})
cfg.add_section('DISPLAY', {'type':'notebook', 'model':'hp212', 'resolution_width':1366, 'resolution_height':766, 
    'directx_version':11})
cfg.add_section('USER')
cfg.add_param('user', {'sex':'male'})
cfg.add_param('display', {'fullscreen':'yes'})

cfg.print_to_file('test.cfg')
cfg1 = Config()
cfg1.read_from_file('test.cfg')

print(cfg1.config)
