from typing import Any, Sequence
import sys
import os
from parsing import ConfigError, load_config, write_output
from mazegen import Mazegenerator
from display import display

CONFIG_FILE = "config.txt"


def generate_maze(
    config: dict[str, Any],
) -> tuple[list[list[int]], Sequence[int | str], list[tuple[int, int]], int]:
    """Generate a maze from the config, save it to the output file and
    return (grid, path, fortytwo_cells)."""
    maze = Mazegenerator(
        width=config["WIDTH"],
        height=config["HEIGHT"],
        entry_xy=config["ENTRY"],
        exit_xy=config["EXIT"],
        perfect=config["PERFECT"],
        seed=config["SEED"],
    )

    maze.generate()

    write_output(
        config["OUTPUT_FILE"],
        maze.grid,
        config["ENTRY"],
        config["EXIT"],
        "".join(maze.path),
    )

    return maze.grid, maze.path, maze.fortytwo_cells, maze.seed


def main() -> None:
    """Load the config, generate the maze and show it in the terminal
    menu. Print an error message if the config or output file fails."""
    try:
        config = load_config(CONFIG_FILE)
        if config["WIDTH"] < 2 or config["HEIGHT"] < 2:
            print("Erro: O labirinto é muito pequeno. O tamanho mínimo é 2x2.")
            return
        grid, path, fortytwo, seed = generate_maze(config)

        entry_display = (
            config["ENTRY"][1],
            config["ENTRY"][0],
        )
        ficheiro = sys.argv[1]
        extensao = os.path.splitext(ficheiro)
        if len(sys.argv) > 2 or extensao[1] != ".txt":
            print("\033[91m")
            print("=" * 80)
            print("---> AVISO: Só é possivel passar dois "
                  "argumentos e o segundo deve ser um .txt")
            print("=" * 80 + "\n")
            print("\033[0m")
            return
        if config["WIDTH"] < 9 or config["HEIGHT"] < 7:
            print("\033[91m")
            print("=" * 55)
            print("---> AVISO: LABIRINTO MUITO PEQUENO!")
            print("=" * 55)
            print(" Não é possível visualizar o número 42.")
            print(" Para visualizar, utilize um tamanho mínimo de 9x7.")
            print("=" * 55 + "\n")
            print("\033[0m")
        if sys.argv[1]:
            print("\033[91m")
            print("=" * 55)
            print(f"---> AVISO: ficheiro padrão - {CONFIG_FILE}!")
            print("=" * 55 + "\n")
            print("\033[0m")
        display(
            seed=seed,
            grid=grid,
            path=path,
            entry=entry_display,
            fortytwo=fortytwo,
            regenerate=lambda: generate_maze(config),
        )

    except (ConfigError, ValueError, OSError) as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()
