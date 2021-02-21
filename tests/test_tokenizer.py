from wordsindecks.parser.tokenizer import Tokenizer, TokenKind
import pytest

class TestTokenizer:
    def tokenize_file(self, filename):
        with open('tests/resources/' + filename, 'r') as f:
            produced_tokens = Tokenizer(f.read()).process()
            return [(p.kind, p.content) for p in produced_tokens]

    def test_foo(self):
        expected_tokens = [
            (TokenKind.HEADING_OPEN, '=='),
            (TokenKind.TEXT, 'Heading'),
            (TokenKind.HEADING_CLOSE, '=='),
            (TokenKind.HTML_OPEN, '<b>'),
            (TokenKind.TEXT, 'This is a bold paragraph'),
            (TokenKind.HTML_CLOSE, '</b>'),
            (TokenKind.PBREAK, '\n\n'),
            (TokenKind.TEXT, 'This is another paragraph'),
            (TokenKind.HEADING_OPEN, '=='),
            (TokenKind.TEXT, 'Another heading'),
            (TokenKind.HEADING_CLOSE, '=='),
            (TokenKind.HEADING_OPEN, '==='),
            (TokenKind.TEXT, 'Subsection heading'),
            (TokenKind.HEADING_CLOSE, '==='),
            (TokenKind.HEADING_OPEN, '==='),
            (TokenKind.TEXT, 'Another subsection heading'),
            (TokenKind.HEADING_CLOSE, '==='),
            (TokenKind.TEXT, 'test'),
            (TokenKind.PBREAK, '\n\n'),
            (TokenKind.TEXT, 'test'),
            (TokenKind.LIST_ITEM, '*'),
            (TokenKind.TEXT, ' test'),

        ]

        assert self.tokenize_file('foo.txt') == expected_tokens

    def test_article(self):
        expected_tokens = [
            (TokenKind.HEADING_OPEN, '=='),
            (TokenKind.TEXT, 'English'),
            (TokenKind.HEADING_CLOSE, '=='),
            (TokenKind.TEMPLATE_OPEN, '{{'),
            (TokenKind.TEXT, 'wikipedia'),
            (TokenKind.TEMPLATE_CLOSE, '}}'),
            (TokenKind.HEADING_OPEN, '==='),
            (TokenKind.TEXT, 'Etymology'),
            (TokenKind.HEADING_CLOSE, '==='),
            (TokenKind.TEMPLATE_OPEN, '{{'),
            (TokenKind.TEXT, 'suffix'),
            (TokenKind.TEMPLATE_SPLIT, '|'),
            (TokenKind.TEXT, 'en'),
            (TokenKind.TEMPLATE_SPLIT, '|'),
            (TokenKind.TEXT, 'parse'),
            (TokenKind.TEMPLATE_SPLIT, '|'),
            (TokenKind.TEXT, 'er'),
            (TokenKind.TEMPLATE_CLOSE, '}}'),
            (TokenKind.HEADING_OPEN, '==='),
            (TokenKind.TEXT, 'Pronunciation'),
            (TokenKind.HEADING_CLOSE, '==='),
            (TokenKind.LIST_ITEM, '*'),
            (TokenKind.TEXT, ' '),
            (TokenKind.TEMPLATE_OPEN, '{{'),
            (TokenKind.TEXT, 'a'),
            (TokenKind.TEMPLATE_SPLIT, '|'),
            (TokenKind.TEXT, 'UK'),
            (TokenKind.TEMPLATE_CLOSE, '}}'),
            (TokenKind.TEXT, ' '),
            (TokenKind.TEMPLATE_OPEN, '{{'),
            (TokenKind.TEXT, 'IPA'),
            (TokenKind.TEMPLATE_SPLIT, '|'),
            (TokenKind.TEXT, 'en'),
            (TokenKind.TEMPLATE_SPLIT, '|'),
            (TokenKind.TEXT, '/ˈpɑː(ɹ).zə/'),
            (TokenKind.TEMPLATE_SPLIT, '|'),
            (TokenKind.TEXT, '/ˈpɑː(ɹ).sə/'),
            (TokenKind.TEMPLATE_CLOSE, '}}'),
            (TokenKind.LIST_ITEM, '*'),
            (TokenKind.TEXT, ' '),
            (TokenKind.TEMPLATE_OPEN, '{{'),
            (TokenKind.TEXT, 'rhymes'),
            (TokenKind.TEMPLATE_SPLIT, '|'),
            (TokenKind.TEXT, 'en'),
            (TokenKind.TEMPLATE_SPLIT, '|'),
            (TokenKind.TEXT, 'ɑː(r)zə(r)'),
            (TokenKind.TEMPLATE_SPLIT, '|'),
            (TokenKind.TEXT, 'ɑː(ɹ)sə(ɹ)'),
            (TokenKind.TEMPLATE_CLOSE, '}}'),
            (TokenKind.LIST_ITEM, '*'),
            (TokenKind.TEXT, ' '),
            (TokenKind.TEMPLATE_OPEN, '{{'),
            (TokenKind.TEXT, 'audio'),
            (TokenKind.TEMPLATE_SPLIT, '|'),
            (TokenKind.TEXT, 'en'),
            (TokenKind.TEMPLATE_SPLIT, '|'),
            (TokenKind.TEXT, 'LL-Q1860 (eng)-I learned some phrases-parser.wav'),
            (TokenKind.TEMPLATE_SPLIT, '|'),
            (TokenKind.TEXT, 'Audio (UK)'),
            (TokenKind.TEMPLATE_CLOSE, '}}'),

            (TokenKind.HEADING_OPEN, '==='),
            (TokenKind.TEXT, 'Noun'),
            (TokenKind.HEADING_CLOSE, '==='),
            (TokenKind.TEMPLATE_OPEN, '{{'),
            (TokenKind.TEXT, 'en-noun'),
            (TokenKind.TEMPLATE_CLOSE, '}}'),

            (TokenKind.LIST_ITEM, '#'),
            (TokenKind.TEXT, ' '),
            (TokenKind.TEMPLATE_OPEN, '{{'),
            (TokenKind.TEXT, 'lb'),
            (TokenKind.TEMPLATE_SPLIT, '|'),
            (TokenKind.TEXT, 'en'),
            (TokenKind.TEMPLATE_SPLIT, '|'),
            (TokenKind.TEXT, 'computing'),
            (TokenKind.TEMPLATE_CLOSE, '}}'),
            (TokenKind.TEXT, ' A computer program that parses.'),

            (TokenKind.LIST_ITEM, '#'),
            (TokenKind.TEXT, ' One who '),
            (TokenKind.LINK_OPEN, '[['),
            (TokenKind.TEXT, 'parse'),
            (TokenKind.LINK_CLOSE, ']]'),
            (TokenKind.TEXT, 's.')
        ]
        
        assert self.tokenize_file('parser.txt') == expected_tokens
            
