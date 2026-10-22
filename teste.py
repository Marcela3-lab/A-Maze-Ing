from parsing import read_config_file, ConfigError

try:
    print(read_config_file("config.txt"))
except ConfigError as err:
    print(f"Erro: {err}")