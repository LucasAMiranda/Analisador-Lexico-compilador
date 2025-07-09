import argparse
import pathlib
import sys

from sly import Lexer

class MJLexer(Lexer):
    """A lexer for the Minijava language."""
    def __init__(self, error_func=None):
        super().__init__()
        self.error_func = error_func
        self.last_token = None

    def _error(self, msg, token):
        location = self._make_tok_location(token)
        if self.error_func:
            self.error_func(msg, location[0], location[1])
        self.index += 1

    def find_tok_column(self, token):
        last_cr = self.text.rfind("\n", 0, token.index)
        return token.index - last_cr

    def _make_tok_location(self, token):
        return (token.lineno, self.find_tok_column(token))

    # ------------------------------
    # Error handling rule
    # ------------------------------
    def error(self, t):
        msg = f"Illegal character {t.value[0]!r}"
        self._error(msg, t)

    # ------------------------------
    # Utility: print all tokens
    # ------------------------------
    def scan(self, data):
        output = ""
        for token in self.tokenize(data):
            token_str = (
                f"LexToken({token.type},{token.value!r},{token.lineno},{token.index})"
            )
            print(token_str)
            output += token_str + "\n"
        return output

    # --------------------------------------------------------------
    # TOKENS
    # --------------------------------------------------------------
    tokens = {
        # Keywords
        "CLASS", "EXTENDS", "PUBLIC", "STATIC", "VOID", "MAIN", "STRING",
        "BOOLEAN", "CHAR", "INT", "IF", "ELSE", "WHILE", "FOR", "ASSERT",
        "BREAK", "RETURN", "NEW", "THIS", "TRUE", "FALSE", "LENGTH", "PRINT",
        # Literals
        "ID", "INT_LITERAL", "CHAR_LITERAL", "STRING_LITERAL",
        # Operators
        "EQ", "NE", "LE", "GE", "AND", "OR", "ASSIGN", "LT", "GT",
        "PLUS", "MINUS", "TIMES", "DIVIDE", "MOD", "NOT",
        # Punctuation
        "DOT", "SEMI", "COMMA", "LPAREN", "RPAREN", "LBRACKET",
        "RBRACKET", "LBRACE", "RBRACE",
    }

    # --------------------------------------------------------------
    # Keywords map
    # --------------------------------------------------------------
    keywords = {
        "class": "CLASS",
        "extends": "EXTENDS",
        "public": "PUBLIC",
        "static": "STATIC",
        "void": "VOID",
        "main": "MAIN",
        "String": "STRING",
        "boolean": "BOOLEAN",
        "char": "CHAR",
        "int": "INT",
        "if": "IF",
        "else": "ELSE",
        "while": "WHILE",
        "for": "FOR",
        "assert": "ASSERT",
        "break": "BREAK",
        "return": "RETURN",
        "new": "NEW",
        "this": "THIS",
        "true": "TRUE",
        "false": "FALSE",
        "length": "LENGTH",
        "print": "PRINT",
    }

    # --------------------------------------------------------------
    # IGNORE
    # --------------------------------------------------------------
    ignore = " \t"

    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count("\n")

    # --------------------------------------------------------------
    # COMMENTS
    # --------------------------------------------------------------
    @_(r'//.*')
    def ignore_comment(self, t):
        pass

    @_(r'/\*(.|\n)*?\*/')
    def ignore_multiline_comment(self, t):
        self.lineno += t.value.count("\n")

    # --------------------------------------------------------------
    # IDENTIFIERS and KEYWORDS
    # --------------------------------------------------------------
    @_(r'[a-zA-Z_][a-zA-Z_0-9]*')
    def ID(self, t):
        t.type = self.keywords.get(t.value, "ID")
        return t

    # --------------------------------------------------------------
    # LITERALS
    # --------------------------------------------------------------
    @_(r'\d+')
    def INT_LITERAL(self, t):
        t.value = int(t.value)
        return t

    @_(r"'.'")
    def CHAR_LITERAL(self, t):
        t.value = t.value[1]
        return t

    @_(r'"([^"\\]|\\.)*"')
    def STRING_LITERAL(self, t):
        t.value = t.value[1:-1]
        return t

    # --------------------------------------------------------------
    # OPERATORS AND PUNCTUATION
    # (Order matters for longest matches)
    # --------------------------------------------------------------
    EQ = r'=='
    NE = r'!='
    LE = r'<='
    GE = r'>='
    AND = r'&&'
    OR = r'\|\|'
    ASSIGN = r'='
    LT = r'<'
    GT = r'>'
    PLUS = r'\+'
    MINUS = r'-'
    TIMES = r'\*'
    DIVIDE = r'/'
    MOD = r'%'
    NOT = r'!'
    DOT = r'\.'
    SEMI = r';'
    COMMA = r','
    LPAREN = r'\('
    RPAREN = r'\)'
    LBRACKET = r'\['
    RBRACKET = r'\]'
    LBRACE = r'\{'
    RBRACE = r'\}'

# --------------------------------------------------------------
# CLI
# --------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="Path to file to be scanned", type=str)
    args = parser.parse_args()

    input_file = args.input_file
    input_path = pathlib.Path(input_file)

    if not input_path.exists():
        print("Input", input_path, "not found", file=sys.stderr)
        sys.exit(1)

    def print_error(msg, x, y):
        print(f"Lexical error: {msg} at {x}:{y}", file=sys.stdout)

    lexer = MJLexer(print_error)

    with open(input_path) as f:
        lexer.scan(f.read())

if __name__ == "__main__":
    main()
