import pytest
from pathlib import Path
from gendiff.gendiff import generate_diff


gendiff_output = Path(Path.cwd(), 'result.txt')
path1 = Path(Path.cwd(), 'tests', 'fixtures', 'file0_1.json')
path2 = Path(Path.cwd(), 'tests', 'fixtures', 'file0_2.json')
path3 = Path(Path.cwd(), 'tests', 'fixtures', 'file1.json')
path4 = Path(Path.cwd(), 'tests', 'fixtures', 'file2.json')
path5 = Path(Path.cwd(), 'tests', 'fixtures', 'FILE0.yml')
path6 = Path(Path.cwd(), 'tests', 'fixtures', 'FILE1.yaml')
path7 = Path(Path.cwd(), 'tests', 'fixtures', 'FILE2.yml')
standart1 = Path(Path.cwd(), 'tests', 'fixtures', 'standart1.txt')
standart2 = Path(Path.cwd(), 'tests', 'fixtures', 'standart2.txt')
standart3 = Path(Path.cwd(), 'tests', 'fixtures', 'standart3.txt')


@pytest.mark.parametrize("file_1, file_2, correct_result", [
    (path1, path2, standart1),
    (path1, path3, standart2),
    (path3, path4, standart3),
    (path5, path6, standart2),
    (path6, path7, standart3)
])
def test_gendiff_with_flat_json(file_1, file_2, correct_result):
    generate_diff(file_1, file_2)
    with open(gendiff_output, 'r') as output:
        with open(correct_result, 'r') as correct:
            assert output.read() == correct.read()


def test_parsing_wrong_type():
    with pytest.raises(TypeError, match='Get ERROR. Check the file type.'):
        generate_diff(path3, standart1)
