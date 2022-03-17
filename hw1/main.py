from utils.console import TTTinTerminal


def main():
    figlet_font = "small"
    delimeter = ","
    board_size = 3
    verbose = True

    TTTinTerminal(board_size, verbose, delimeter, figlet_font)


if __name__ == "__main__":
    main()
