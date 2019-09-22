import configparser

config = configparser.ConfigParser()
config.read("pricing.conf")

def get_property(name, default):
    if "DEFAULT" in config and name in config['DEFAULT']:
        return config['DEFAULT'][name]
    else:
        return default

def get_server_port():
    return int(get_property('ServerPort', 3101))
