import unittest
from unittest.mock import patch
import search.corpus


class TestCorpusLoad(unittest.TestCase):

    @patch("builtins.print", wrap=print)
    def test_file_stats(self, print_spy):
        search.corpus.PATH = 'corpus'
        search.corpus.Corpus().main()
        print_spy.assert_any_call('Branching.txt: 381')
        print_spy.assert_any_call('Intro to text representation.txt: 725')