from typing import Any

MANDATORY_KEYS = ("WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT")

class ConfigError(Exception):
    """Classe para erros de configuração"""


def read_config_file(path: str) -> dict[str, str]:
    """Lê um ficheiro par-valor e devolve um dicionario de strings"""
    try:
        with open(path, "r", encoding="utf-8") as file:
            lines = file.readlines()
    except FileNotFoundError:
        raise ConfigError(f"ficheiro '{path}' não encontrado")
    raw : dict[str, str] = {}
    for line in lines:
        line = line.strip()
        if line.startswith("#") or not line:
            continue
        if "=" not in line:
            raise ConfigError(f"linha sem '=': '{line}'")
        key, value = line.split("=", 1)
        raw[key.strip()] = value.strip()
    return raw

def parse_int(key: str, value:str) -> int:
    """Converte o valor de str pra inteiro"""
    try:
        return int(value)
    except ValueError:
        raise ConfigError(f"{key} tem de ser um número inteiro; recebido '{value}'")

def parse_coords(key: str, value:str) -> tuple[int,int]:
    cord = value.split(",")
    if len(cord) != 2:
        raise ConfigError(
            f"Número de coordenadas {key} não esperado! "
            f"Esperam-se 2 coordenadas; recebido '{len(cord)}'"
        )
    elif len(cord) == 2:
        try:
            x = int(cord[0].strip())
            y = int(cord[1].strip())
        except (ValueError):
            raise ConfigError(f"Erro ao tentar converter as coordenadas {value}! Apenas inteiros são aceitos")
    return (x,y)


def parse_bool(key: str, value: str) -> bool:
    if value == "True":
        return True
    elif value == "False":
        return False
    else:
        raise ConfigError(
            f"{key} tem de ser 'True' ou 'False'; recebido '{value}'"
        )

def validate_config(raw: dict[str, str]) -> dict:
    config: dict[str, Any] = {}
    missing = []
    for k in MANDATORY_KEYS:
        if k not in raw:
            missing.append(k)
    if missing:
        raise ConfigError(f"Chaves em falta {(', '.join(missing))}")
    for key, value in raw.items():
        if key == "WIDTH":
            config[key] = parse_int(key,value)
        elif key == "HEIGHT":
            config[key] = parse_int(key,value)
        elif key == "ENTRY":
            config[key] = parse_coords(key,value)
        elif key == "EXIT":
            config[key] = parse_coords(key,value)
        elif key == "PERFECT":
            config[key] = parse_bool(key,value)
        elif key == "OUTPUT_FILE":
            config[key] = value
        else:
            raise ConfigError(f"Chave de configuração desconhecida: '{key}'")

    if config["WIDTH"] < 1 or config["HEIGHT"] < 1:
        raise ConfigError("A altura e a largura prescisam ser >= 1")
    for name in ("ENTRY", "EXIT"):
        x, y = config[name]
        if not (0 <= x < config["WIDTH"] and 0 <= y < config["HEIGHT"]):
            raise ConfigError(
            f"{name} ({x},{y}) está fora do labirinto "
            f"{config['WIDTH']}x{config['HEIGHT']}"
            )
    if config["ENTRY"] == config["EXIT"]:
        raise ConfigError("ENTRY e EXIT têm de ser diferentes")
    return config

def load_config(path: str) -> dict[str, Any]:
    """Lê e valida o ficheiro de configuração."""
    return validate_config(read_config_file(path))

def cell_to_hex(cell: int) -> str:
    """Converte a celula em hexadecimal"""
    if not 0 <= cell <= 15:
        raise ConfigError(f"cell:{cell}, o valor prescisa estar entre >= que 0 e <= que 15")
    return f"{cell:X}"

def write_output(
        path:str,
        grid:list[list[int]],
        entry:tuple[int,int],
        exit_:tuple[int,int],
        solution:str,
                )-> None:
    """Escreve o labirinto no ficheiro de saida"""
    try:
        with open (path, "w", encoding="utf-8") as file:
            for row in grid:
                line = "".join(cell_to_hex(cell) for cell in row)
                file.write(line + "\n")
            file.write("\n")
            file.write(f"{entry[0],entry[1]}\n")
            file.write(f"{exit_[0],exit_[1]}\n")
            file.write(solution + "\n")
    except OSError as err:
        raise(f"Erro no file '{path}', erro:'{err}")

