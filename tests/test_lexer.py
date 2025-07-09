import sys
from pathlib import Path

import pytest

# Adiciona a pasta raiz do projeto ao sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from mjc.mj_lexer import MJLexer


def resolve_test_files(test_name):
    input_file = test_name + ".in"
    expected_file = test_name + ".out"

    # get current dir
    current_dir = Path(__file__).parent.absolute()

    # get absolute path to inputs folder
    test_folder = current_dir / Path("in-out")

    # get input path and check if exists
    input_path = test_folder / Path(input_file)
    assert input_path.exists()

    # get expected test file real path
    expected_path = test_folder / Path(expected_file)
    assert expected_path.exists()

    return input_path, expected_path


@pytest.mark.parametrize(
    "test_name",
    [
        "t01", "t02", "t03", "t04", "t05",
        "t06", "t07", "t08", "t09", "t10",
        "t11", "t12", "t13", "t14", "t15",
        "t16", "t17", "t18", "t19", "t20",
    ],
)
def test_lexer(test_name, capfd):
    input_path, expected_path = resolve_test_files(test_name)

    def print_error(msg, x, y):
        print("Lexical error: %s at %d:%d" % (msg, x, y), file=sys.stdout)

    lexer = MJLexer(print_error)

    with open(input_path) as f_in, open(expected_path) as f_ex:
        lexer.scan(f_in.read())
        captured = capfd.readouterr()

        # Normaliza as quebras de linha e espaços em branco no final
        actual_lines = [
            line.rstrip() for line in captured.out.replace('\r\n', '\n').split('\n')
        ]
        expected_lines = [
            line.rstrip() for line in f_ex.read().replace('\r\n', '\n').split('\n')
        ]

    # DEBUG: Mostra diferenças se houver falha
    if actual_lines != expected_lines:
        print("\n--- Captured ---\n", actual_lines)
        print("\n--- Expected ---\n", expected_lines)

    assert actual_lines == expected_lines
