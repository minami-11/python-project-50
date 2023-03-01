import pytest
from pathlib import Path
from gendiff.gendiff import generate_diff


gendiff_output = Path(Path.home(), 'Hexlet_Projects', 'python-project-50',
                      'result.txt')
path1 = Path(Path.home(), 'Hexlet_Projects', 'python-project-50',
             'tests', 'fixtures', 'file0_1.json')
path2 = Path(Path.home(), 'Hexlet_Projects', 'python-project-50',
             'tests', 'fixtures', 'file0_2.json')
path3 = Path(Path.home(), 'Hexlet_Projects', 'python-project-50',
             'tests', 'fixtures', 'file1.json')
path4 = Path(Path.home(), 'Hexlet_Projects', 'python-project-50',
             'tests', 'fixtures', 'file2.json')
standart1 = Path(Path.home(), 'Hexlet_Projects', 'python-project-50',
                 'tests', 'fixtures', 'standart1.txt')
standart2 = Path(Path.home(), 'Hexlet_Projects', 'python-project-50',
                 'tests', 'fixtures', 'standart2.txt')
standart3 = Path(Path.home(), 'Hexlet_Projects', 'python-project-50',
                 'tests', 'fixtures', 'standart3.txt')


@pytest.mark.parametrize("file_1, file_2, correct_result", [
    (path1, path2, standart1),
    (path1, path3, standart2),
    (path3, path4, standart3)
])
def test_gendiff_with_flat_json(file_1, file_2, correct_result):
    generate_diff(file_1, file_2)
    with open(gendiff_output, 'r') as output:
        with open(correct_result, 'r') as correct:
            assert output.read() == correct.read()
