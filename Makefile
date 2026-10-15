.PHONY: check serve labs
check:
	ruff check .
	ruff format --check .
	mypy
	PYTHONPATH=src python -m unittest discover -s tests
	python scripts/check_docs.py

serve:
	PYTHONPATH=src python -m solid_workbook.backend

labs:
	PYTHONPATH=src python -m solid_workbook all
	PYTHONPATH=src python -m solid_workbook srp-lab
	PYTHONPATH=src python -m solid_workbook ocp-lab
	PYTHONPATH=src python -m solid_workbook lsp-lab
