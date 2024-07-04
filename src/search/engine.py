import spacy
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from spacy.tokens import Token

from search.corpus import Corpus

nlp = spacy.load('en_core_web_sm')
WS = 30  # window size

class Engine:
    def __init__(self):
        self.corpus = Corpus().read_corpus()
        self.vectorizer = TfidfVectorizer()

    def search(self, query: str, limit: int, offset: int) -> list[tuple[str, float]]:
        X = self.vectorizer.fit_transform(self.corpus.values())
        query_vector = self.vectorizer.transform([query])
        similarities = cosine_similarity(X, query_vector).flatten()
        search_hits = sorted([(doc, sim) for doc, sim in zip(self.corpus.keys(), similarities) if sim > 0], key=lambda x: x[1], reverse=True)
        return search_hits[offset:offset + limit]

    def tokenize_and_show_results(self, file: str, query_words: list[str]):
        print(file)
        result = self.get_first_match(file, query_words)
        txt = self.corpus[file]
        start = result.idx
        end = result.idx + len(result.text)
        prefix = f'...{txt[start - WS:start]}' if start > WS else txt[:start]
        suffix = f'{txt[end:end + WS - 1]}...' if end + WS < len(txt) else txt[end:]
        window = f'{prefix}{result.text}{suffix}'
        for word in query_words:
            window = window.replace(word, f'<b>{word}</b>')
        print(window)

    def get_first_match(self, file, query_words) -> Token:
        doc = nlp(self.corpus[file])
        for token in doc:
            if token.text in query_words:
                return token

    def print_search_results(self, matching_documents, query):
        query_words = re.sub(r'[^ \w]+', '', query).split()
        if not query_words or not matching_documents:
            print('No results were found for your query and offset')
            return
        for doc, _ in matching_documents:
            self.tokenize_and_show_results(doc, query_words)

    def main(self):
        while True:
            query = input('Enter your query, please:\n')
            limit = int(input('Enter limit:\n'))
            offset = int(input('Enter offset:\n'))
            matching_documents = self.search(query, limit, offset)
            self.print_search_results(matching_documents, query)
            if input('Do you want to make another request? (yes/no)\n') == 'no':
                break
        print('Bye!')


if __name__ == '__main__':
    Engine().main()
