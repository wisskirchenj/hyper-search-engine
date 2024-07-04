import unittest
from unittest.mock import patch, MagicMock, call
from parameterized import parameterized

import search.corpus
from search.engine import Engine


class TestEngine(unittest.TestCase):

    def setUp(self):
        search.corpus.PATH = 'corpus'
        self.engine = Engine()

    def test_search_empty(self):
        self.assertEqual([], self.engine.search('testxyz', 1, 0))

    @parameterized.expand([
        1,
        2,
        20
    ])
    def test_search_with_hit_varying_limit(self, limit):
        results = self.engine.search('the', limit, 0)
        self.assertEqual(min(6, limit), len(results))
        self.assertEqual(results[0][0], 'Reader and Writer interfaces.txt')

    @parameterized.expand([
        [0, 'Reader and Writer interfaces.txt'],
        [1, 'Branching.txt'],
        [5, 'Intro to text representation.txt']
    ])
    def test_search_with_hit_varying_offset(self, offset, file):
        results = self.engine.search('the', 1, offset)
        self.assertEqual(1, len(results))
        self.assertEqual(results[0][0], file)

    @patch('builtins.print', wrap=print)
    @patch('search.engine.input', side_effect=['testxyz', 1, 0, 'no'])
    def test_inputs_taken_and_empty_response(self, mock_input: MagicMock, print_spy):
        self.engine.main()
        print_spy.assert_any_call('No results were found for your query and offset')
        mock_input.assert_called_with('Do you want to make another request? (yes/no)\n')
        mock_input.assert_any_call('Enter your query, please:\n')
        mock_input.assert_any_call('Enter limit:\n')
        mock_input.assert_any_call('Enter offset:\n')
        self.assertEqual(4, mock_input.call_count)

    @patch('builtins.print', wrap=print)
    @patch('search.engine.input', side_effect=['testxyz', 1, 0, 'yes', 'testxyz', 1, 0, 'no'])
    def test_main_loop_works(self, mock_input: MagicMock, print_spy: MagicMock):
        self.engine.main()
        self.assertEqual(2, print_spy.call_args_list.count(call('No results were found for your query and offset')))
        self.assertEqual(8, mock_input.call_count)

    @patch('builtins.print', wrap=print)
    @patch('search.engine.input', side_effect=['Hugging Face', 1, 0, 'no'])
    def test_example1_stage5(self, mock_input, print_spy: MagicMock):
        self.engine.main()
        print_spy.assert_any_call('Intro to text representation.txt')
        print_spy.assert_any_call('''...You can download the first on <b>Hugging</b> <b>Face</b>.
Universal Language Mod...''')

    @patch('builtins.print', wrap=print)
    @patch('search.engine.input', side_effect=['functions', 2, 0, 'no'])
    def test_example2_stage5(self, mock_input, print_spy: MagicMock):
        self.engine.main()
        self.assertEqual([call('Invoking a function.txt'),
                          call('...ython interpreter has several <b>functions</b> and types built into it, so ...'),
                          call('Functional decomposition.txt'),
                          call('...posing a problem into several <b>functions</b> or methods. Each method does...'),
                          call('Bye!')], print_spy.call_args_list)

    @patch('builtins.print', wrap=print)
    @patch('search.engine.input', side_effect=['Functional decomposition', 1, 0, 'no'])
    def test_example3_stage5(self, mock_input, print_spy: MagicMock):
        self.engine.main()
        print_spy.assert_any_call('Functional decomposition.txt')
        print_spy.assert_any_call('<b>Functional</b> <b>decomposition</b> is simply a pr...')
