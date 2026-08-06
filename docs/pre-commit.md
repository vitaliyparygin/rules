### pre commit
1.
```
pytest --cov=src/rules --cov-report=term-missing --cov-fail-under=90
```
2. 
```
ruff check .
black --check .
mypy src
pytest --cov=src/rules --cov-report=term-missing --cov-report=xml
python -m build
```