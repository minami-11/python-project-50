automate-build: shell build publish
	pip list

build:
	poetry build



publish:
	poetry publish --dry-run

shell:
	poetry shell


#For installing package from operated system (add "--user" after "install")
package-install:
	python3 -m pip install dist/*.whl

package-uninstall:
	python3 -m pip uninstall hexlet-code
