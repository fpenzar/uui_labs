from Parser import Parser


if __name__ == "__main__":
    parser = Parser()
    parser.read_stdin()
    logic_tree = parser.parse()
    if parser.resolution:
        logic_tree.plResolution(parser.test_state)
        logic_tree.print()
