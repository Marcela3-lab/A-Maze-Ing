from parsing import load_config, write_output
from generator import Mazegenerator
from display import display


CONFIG_FILE = "config.txt"


def generate_maze(config):
    maze = Mazegenerator(
        width=config["WIDTH"],
        height=config["HEIGHT"],
        entry_xy=config["ENTRY"],
        exit_xy=config["EXIT"],
        perfect=config["PERFECT"],
        seed=config["SEED"],
    )

    # Gera o labirinto
    maze.generate()


    # Guarda o labirinto no ficheiro de saída
    write_output(
        config["OUTPUT_FILE"],
        maze.grid,
        config["ENTRY"],
        config["EXIT"],
        "".join(maze.path),
    )

    return maze.grid, maze.path, maze.fortytwo_cells


def main():
    try:
        config = load_config(CONFIG_FILE)
        if config["WIDTH"] < 2 or config["HEIGHT"] < 2:
            print("Erro: O labirinto é muito pequeno. O tamanho mínimo é 2x2.")
            return
        grid, path, fortytwo = generate_maze(config)

        # O display trabalha com (row, col),
        # mas o config usa (x, y).
        entry_display = (
            config["ENTRY"][1],
            config["ENTRY"][0],
        )
        if config["WIDTH"] < 9 or config["HEIGHT"] < 8:
            print("\033[91m")
            print("=" * 55)
            print("---> AVISO: LABIRINTO MUITO PEQUENO!")
            print("=" * 55)
            print(" Não é possível visualizar o número 42.")
            print(" Para visualizar, utilize um tamanho mínimo de 9x8.")
            print("=" * 55 + "\n")
            print("\033[0m")

        display(
            grid,
            path,
            entry=entry_display,
            fortytwo=fortytwo,
            regenerate=lambda: generate_maze(config),
        )

    except (ValueError, OSError) as error:
        print(f"Erro: {error}")


if __name__ == "__main__":
    main()