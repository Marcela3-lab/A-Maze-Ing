from typing import Any

MANDATORY_KEYS = {"WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"}


class ConfigError(Exception):
    """Class for configuration errors"""


def read_config_file(path: str) -> dict[str, str]:
    """Read a key-value file and return a dictionary of strings"""
    try:
        with open(path, "r", encoding="utf-8") as file:
            lines = file.readlines()
    except FileNotFoundError:
        raise ConfigError(f"file '{path}' not found")
    raw: dict[str, str] = {}
    for line in lines:
        line = line.strip()
        if line.startswith("#") or not line:
            continue
        if "=" not in line:
            raise ConfigError(f"line without '=': '{line}'")
        key, value = line.split("=", 1)
        raw[key.strip()] = value.strip()
    return raw


def parse_int(key: str, value: str) -> int:
    """Convert the value from str to int"""
    try:
        return int(value)
    except ValueError:
        raise ConfigError(f"{key} has to be an integer "
                          f"value received: '{value}'")


def parse_coords(key: str, value: str) -> tuple[int, int]:
    """Convert a string such as "x,y" into a tuple of two integers"""
    cord = value.split(",")
    if len(cord) != 2:
        raise ConfigError(
            f"coordenates {key} not expected! "
            f"cordenates must be 2 values (x,y); value received '{len(cord)}'"
        )
    elif len(cord) == 2:
        try:
            x = int(cord[0].strip())
            y = int(cord[1].strip())
        except (ValueError):
            raise ConfigError(f"error: cannot find coordenate"
                              f"{value}! only integers are accepted")
    return (x, y)


def parse_bool(key: str, value: str) -> bool:
    """Convert the strings "True" and "False" into a bool"""
    if value == "True":
        return True
    elif value == "False":
        return False
    else:
        raise ConfigError(
            f"{key} has to be 'True' or 'False'; value received '{value}'"
        )


def validate_config(raw: dict[str, str]) -> dict[str, Any]:
    """Check mandatory keys, convert each value to its proper type and
    validate the dimensions, entry and exit. Return the final config"""
    config: dict[str, Any] = {}
    missing = []
    for k in MANDATORY_KEYS:
        if k not in raw:
            missing.append(k)
    if missing:
        raise ConfigError(f"keys missing {(', '.join(missing))}")
    for key, value in raw.items():
        if key == "WIDTH":
            config[key] = parse_int(key, value)
        elif key == "HEIGHT":
            config[key] = parse_int(key, value)
        elif key == "ENTRY":
            config[key] = parse_coords(key, value)
        elif key == "EXIT":
            config[key] = parse_coords(key, value)
        elif key == "PERFECT":
            config[key] = parse_bool(key, value)
        elif key == "OUTPUT_FILE":
            config[key] = value
        elif key == "SEED":
            config[key] = parse_int(key, value)
        else:
            raise ConfigError(f"Unknown configuration key: '{key}'")
        config.setdefault("SEED", None)
    if config["WIDTH"] < 2 or config["HEIGHT"] < 2:
        raise ConfigError("width and height must be >= 2")
    for name in ("ENTRY", "EXIT"):
        x, y = config[name]
        if not (0 <= x < config["WIDTH"] and 0 <= y < config["HEIGHT"]):
            raise ConfigError(
                f"{name} ({x},{y}) is off the grid "
                f"{config['WIDTH']}x{config['HEIGHT']}"
            )
    if config["ENTRY"] == config["EXIT"]:
        raise ConfigError("ENTRY and EXIT must be different")
    return config


def load_config(path: str) -> dict[str, Any]:
    """Read and validate the configuration file."""
    return validate_config(read_config_file(path))


def cell_to_hex(cell: int) -> str:
    """Convert the cell value to a hexadecimal digit"""
    if not 0 <= cell <= 15:
        raise ConfigError(f"cell:{cell}, value must be "
                          " >= 0 and <= 15")
    return f"{cell:X}"


def write_output(
        path: str,
        grid: list[list[int]],
        entry: tuple[int, int],
        exit_: tuple[int, int],
        solution: str,
                ) -> None:
    """Write the maze to the output file"""
    try:
        with open(path, "w", encoding="utf-8") as file:
            for row in grid:
                line = "".join(cell_to_hex(cell) for cell in row)
                file.write(line + "\n")
            file.write("\n")
            file.write(f"{entry[0]},{entry[1]}\n")
            file.write(f"{exit_[0]},{exit_[1]}\n")
            file.write(solution + "\n")
    except OSError as err:
        raise ConfigError(f"File error '{path}', error:'{err}'")
