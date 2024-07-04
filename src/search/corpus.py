import os

PATH = '../../corpus'


class Corpus:

    def __init__(self):
        self.data: dict[str, str] = dict()

    def read_corpus(self) -> dict[str, str]:
        files = os.listdir(PATH)
        for file in files:
            self.store_file_content(file)
        return self.data

    def store_file_content(self, file):
        with open(f'{PATH}/{file}', 'r') as f:
            content = f.read()
        self.data[file] = content

    def main(self):
        corpus = self.read_corpus()
        for key, value in corpus.items():
            print(f'{key}: {len(value)}')


if __name__ == '__main__':
    Corpus().main()
