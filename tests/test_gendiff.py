import pytest
import json
from pathlib import Path
from gendiff.gendiff import generate_diff


gendiff_json_output = Path(Path.cwd(), 'result.json')

# Test files fixtures:
path1 = Path(Path.cwd(), 'tests', 'fixtures', 'file0_1.json')       # Empty
path2 = Path(Path.cwd(), 'tests', 'fixtures', 'file0_2.json')       # {}
path3 = Path(Path.cwd(), 'tests', 'fixtures', 'file1.json')         # Flat
path4 = Path(Path.cwd(), 'tests', 'fixtures', 'file2.json')         # Flat
path5 = Path(Path.cwd(), 'tests', 'fixtures', 'file3.json')         # Nested
path6 = Path(Path.cwd(), 'tests', 'fixtures', 'file4.json')         # Nested

path11 = Path(Path.cwd(), 'tests', 'fixtures', 'FILE0.yml')         # Empty
path12 = Path(Path.cwd(), 'tests', 'fixtures', 'FILE1.yaml')        # Flat
path13 = Path(Path.cwd(), 'tests', 'fixtures', 'FILE2.yml')         # Flat
path14 = Path(Path.cwd(), 'tests', 'fixtures', 'FILE3.yaml')        # Nested
path15 = Path(Path.cwd(), 'tests', 'fixtures', 'FILE4.yml')         # Nested

# Result fixtures:
standart1 = Path(Path.cwd(), 'tests', 'fixtures', 'standart1.txt')  # Empty
standart2 = Path(Path.cwd(), 'tests', 'fixtures', 'standart2.txt')  # Empty|Flat
standart3 = Path(Path.cwd(), 'tests', 'fixtures', 'standart3.txt')  # Flat|Flat
standart4 = Path(Path.cwd(), 'tests', 'fixtures', 'standart4.txt')  # Nested

plain2 = Path(Path.cwd(), 'tests', 'fixtures', 'plain2.txt')        # Empty|Flat
plain3 = Path(Path.cwd(), 'tests', 'fixtures', 'plain3.txt')        # Flat|Flat
plain4 = Path(Path.cwd(), 'tests', 'fixtures', 'plain4.txt')        # Nested

json1 = Path(Path.cwd(), 'tests', 'fixtures', 'result.json')        # Nested


@pytest.mark.parametrize("file_1, file_2, correct_result", [
    (path1, path2, standart1),
    (path1, path3, standart2),
    (path3, path4, standart3),
    (path11, path12, standart2),
    (path12, path13, standart3)
])
def test_gendiff_with_flat_files(file_1, file_2, correct_result):
    output_string = generate_diff(file_1, file_2)
    with open(correct_result, 'r') as correct:
        assert output_string == correct.read()


@pytest.mark.parametrize("file_1, file_2, correct_result", [
    (path5, path6, standart4),
    (path14, path15, standart4)
])
def test_gendiff_with_nested_files(file_1, file_2, correct_result):
    output_string = generate_diff(file_1, file_2)
    with open(correct_result, 'r') as correct:
        assert output_string == correct.read()


@pytest.mark.parametrize("file_1, file_2, correct_result", [
    (path1, path2, standart1),
    (path1, path3, plain2),
    (path3, path4, plain3),
    (path5, path6, plain4)
])
def test_gendiff_plain_format(file_1, file_2, correct_result):
    output_string = generate_diff(file_1, file_2, 'plain')
    with open(correct_result, 'r') as correct:
        assert output_string == correct.read()


@pytest.mark.parametrize("file_1, file_2, correct_result", [
    (path5, path6, json1)
])
def test_gendiff_with_json_valid_output(file_1, file_2, correct_result):
    generate_diff(file_1, file_2, 'json')
    with open(gendiff_json_output, 'r') as json_output:
        with open(correct_result, 'r') as json_correct:
            output = json_output.read()
            output_data = json.loads(output)
            correct = json_correct.read()
            correct_data = json.loads(correct)
            assert output_data == correct_data


def test_parsing_wrong_type():
    with pytest.raises(TypeError, match='Get ERROR. Check the file type.'):
        generate_diff(path3, standart1)


def test_wrong_formatter_type():
    with pytest.raises(ValueError,
                       match='Unknown format type, please check the format'):
        generate_diff(path3, path4, 'wrong')
