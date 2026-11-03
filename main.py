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
    )

    # Gera o labirinto
    maze.generate()

    # Procura o caminho entre ENTRY e EXIT
    maze.solve_maze_bfs()

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

        grid, path, fortytwo = generate_maze(config)

        # O display trabalha com (row, col),
        # mas o config usa (x, y).
        entry_display = (
            config["ENTRY"][1],
            config["ENTRY"][0],
        )

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