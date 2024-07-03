import os

PATH = '../../corpus'


class FileStats:

    def read_files(self, dir_path: str) -> dict[str, str]:
        corpus = dict()
        files = os.listdir(dir_path)
        for file in files:
            self.store_file_content(corpus, dir_path, file)
        return corpus

    @staticmethod
    def store_file_content(corpus, dir_path, file):
        with open(f'{dir_path}/{file}', 'r') as f:
            content = f.read()
        corpus[file] = content

    def main(self):
        corpus = self.read_files(PATH)
        for key, value in corpus.items():
            print(f'{key}: {len(value)}')


if __name__ == '__main__':
    FileStats().main()