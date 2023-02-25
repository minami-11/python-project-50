automate-build: shell lint build publish
	pip list

build:
	poetry build

lint:
	poetry run flake8 gendiff

publish:
	poetry publish --dry-run

shell:
	poetry shell

gendiff:
	poetry run gendiff file1.json file2


#For installing package from operated system (add "--user" after "install")
package-install:
	python3 -m pip install dist/*.whl

package-uninstall:
	python3 -m pip uninstall hexlet-code
