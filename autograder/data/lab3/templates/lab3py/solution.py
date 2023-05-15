from Parser import Parser
from id3 import ID3


if __name__ == "__main__":
    parser = Parser()
    parser.read_stdin()
    train_dataset, test_dataset = parser.parse()
    model = ID3(parser.depth)
    model.fit(train_dataset)
    model.predict(test_dataset)
