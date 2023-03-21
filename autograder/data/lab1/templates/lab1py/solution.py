from Parser import Parser
from tree import Tree
from node import Node


if __name__ == "__main__":
    parser = Parser()
    parser.read_stdin()

    graph = parser.parse()
    graph.add_heuristics(parser.get_heuristics_path())

    tree = Tree(graph)
    tree.run_algorithm(parser.get_algorithm())
    tree.print()
