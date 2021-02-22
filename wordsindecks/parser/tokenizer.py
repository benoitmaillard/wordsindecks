from enum import Enum, auto
from typing import Iterator
import re

class TokenKind(Enum):
    HEADING_OPEN = auto()
    HEADING_CLOSE = auto()
    TEMPLATE_OPEN = auto()
    TEMPLATE_CLOSE = auto()
    TEMPLATE_SPLIT = auto()
    LINK_OPEN = auto()
    LINK_CLOSE = auto()
    HTML_OPEN = auto()
    HTML_CLOSE = auto()
    LIST_ITEM = auto()
    PBREAK = auto()
    TEXT = auto()
    IGNORE = auto()

TOKENIZE_RULES = [
    (r'(?:\n|^)(=+)', TokenKind.HEADING_OPEN),
    (r'(=+)(?=\n)', TokenKind.HEADING_CLOSE),
    (r'(\{\{)', TokenKind.TEMPLATE_OPEN),
    (r'(\}\})', TokenKind.TEMPLATE_CLOSE),
    (r'(\|)', TokenKind.TEMPLATE_SPLIT),
    (r'(\[\[)', TokenKind.LINK_OPEN),
    (r'(\]\])', TokenKind.LINK_CLOSE),
    (r'(?:\n)([\*\#\:\;]+)', TokenKind.LIST_ITEM),
    (r'(<[A-Za-z]+>)', TokenKind.HTML_OPEN), # TODO add support for attributes
    (r'(</[A-Za-z]+>)', TokenKind.HTML_CLOSE),
    (r'(\n\n(?![=\*\#\:\;]))', TokenKind.PBREAK),
]

IGNORE_REGEX = re.compile(r'\n')

class Token:
    def __init__(self, kind: TokenKind, content: str, position: tuple[int, int]):
        self.kind = kind
        self.content = content
        self.position = position

class Tokenizer:
    def __init__(self, text):
        self.text = text

    def process(self) -> Iterator[Token]:
        compiled_rules = [(re.compile(regex), kind) for (regex, kind) in TOKENIZE_RULES]

        length = len(self.text)
        pos = 0
        orphan_chars = ""

        while (pos < length):
            new_pos = pos
            for (regex, kind) in compiled_rules:
                match = regex.match(self.text, pos)

                if match:
                    new_pos = match.span()[1]
                    
                    if len(orphan_chars) > 0:
                        yield Token(TokenKind.TEXT, orphan_chars, (pos - len(orphan_chars), pos))
                        orphan_chars = ""

                    yield Token(kind, "".join(match.groups()), match.span())
                    break
            
            if new_pos == pos:
                # single new line characters are not taken into account and are
                # removed before producing a plaintext token
                if not IGNORE_REGEX.match(self.text, pos):
                    orphan_chars += self.text[pos]
                pos += 1
            else:
                pos = new_pos

        if len(orphan_chars) > 0:
            yield Token(TokenKind.TEXT, orphan_chars, (pos - len(orphan_chars), pos-1))