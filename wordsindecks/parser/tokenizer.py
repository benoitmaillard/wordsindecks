from enum import Enum, auto
import re

class TokenKind(Enum):
    HEADING_OPEN = 0
    HEADING_CLOSE = 1
    TEMPLATE_OPEN = 2
    TEMPLATE_CLOSE = 3
    LINK_OPEN = 4
    LINK_CLOSE = 5
    HTML_OPEN = 6
    HTML_CLOSE = 7
    LIST_ITEM = 8
    PBREAK = 9
    TEXT = 10
    IGNORE = 11

# TODO enclose all regex in groups in order to have the option to exclude some characters ?
TOKENIZE_RULES = [
    (r'(?:\n|^)==*', TokenKind.HEADING_OPEN),
    (r'==*\n', TokenKind.HEADING_CLOSE),
    (r'\{\{', TokenKind.TEMPLATE_OPEN),
    (r'\}\}', TokenKind.TEMPLATE_CLOSE),
    (r'\[\[', TokenKind.LINK_OPEN),
    (r'\]\]', TokenKind.LINK_CLOSE),
    (r'\n[\*\#\:\;]*', TokenKind.LIST_ITEM),
    (r'<[A-Za-z][A-Za-z]*>', TokenKind.HTML_OPEN), # TODO add support for attributes
    (r'</[A-Za-z][A-Za-z]*>', TokenKind.HTML_CLOSE),
    (r'\n\n(?![=\*\#\:\;])', TokenKind.PBREAK),
    (r'\n', TokenKind.IGNORE),
]

class Token:
    def __init__(self, kind: TokenKind, content: str, position: tuple[int, int]):
        self.kind = kind
        self.content = content
        self.position = position

class Tokenizer:
    def __init__(self, text):
        self.text = text

    def process(self) -> list[Token]:
        compiled_rules = [(re.compile(regex), kind) for (regex, kind) in TOKENIZE_RULES]

        length = len(self.text)
        pos = 0
        orphan_chars = ""
        tokens: list[Token] = []

        while (pos < length):
            new_pos = pos
            for (regex, kind) in compiled_rules:
                match = regex.match(self.text, pos)

                if match:
                    new_pos = match.span()[1]
                    
                    if len(orphan_chars) > 0:
                        tokens.append(Token(TokenKind.TEXT, orphan_chars, (pos - len(orphan_chars), pos)))
                        orphan_chars = ""

                    # TODO should match.group() be replaced by "".join(match.groups()) to exclude
                    # some characters (such as leading \n)?
                    tokens.append(Token(kind, match.group(), match.span()))
                    break

            if new_pos == pos:
                orphan_chars += self.text[pos]
                pos += 1
            else:
                pos = new_pos

        if len(orphan_chars) > 0:
            tokens.append(Token(TokenKind.TEXT, orphan_chars, (pos - len(orphan_chars), pos-1)))

        return tokens