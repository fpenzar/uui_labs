from Parser import Parser
from tree import Tree


if __name__ == "__main__":
    parser = Parser()
    parser.read_stdin()

    graph = parser.parse()
    graph.add_heuristics(parser.get_heuristics_path())

    tree = Tree(graph)
    if parser.check_optimistic:
        tree.check_optimistic()
    elif parser.check_consistency:
        tree.check_consistency()
    else:
        tree.run_algorithm(parser.get_algorithm())
        tree.print()
