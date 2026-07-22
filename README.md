# Rules

A lightweight Python package containing reusable document classification,
field extraction, synonym dictionaries and question templates for RAG systems.

The project is designed to separate domain knowledge from application logic.

Instead of hardcoding regexes, aliases and document templates inside your
application, they are stored as versioned YAML files and loaded through a
simple Python API.

Badges

Short description

[//]: # (![Tests]&#40;...&#41;)

[//]: # (![Coverage]&#40;...&#41;)

## Features

- YAML-based document classification rules
- YAML-based extraction rules
- YAML-based question templates
- Field synonym dictionaries
- Type-safe Python models
- Simple loader API
- Independent from any specific RAG framework
- Reusable across multiple projects

## Installation

```bash
pip install rules
```



### Quick Start

```python
from rules.loader import (
    load_classification_rules,
    load_extraction_rules,
    load_question_templates,
)

classification = load_classification_rules(...)
extraction = load_extraction_rules(...)
questions = load_question_templates(...)
```


### Project structure
rules/
│
├── yaml/
│   ├── erp/
│   ├── legal/
│   ├── medical/
│   ├── field_rules.yaml
│   └── synonyms.yaml
│
├── loader.py
├── models.py
└── ...

### Supported rule types
## Rule Types

The package currently provides four types of rules.

### Classification Rules

Used to classify documents into document types.

Example:

Invoice:
  filename_patterns:
    - invoice
    - inv

  content_patterns:
    - invoice number
    - total due

---

### Extraction Rules

Used to extract structured fields.

Invoice:

  invoice_number:
    - ...

  amount:
    - ...

---

### Question Templates

Used to generate benchmark questions.

Invoice:

  - key: Invoice

    query_template:
      - What is the {field} on invoice {filename}?

    fields:
      - invoice_number
      - amount

---

### Field Synonyms

Used to normalize field names.

invoice_number:

  aliases:
    - invoice no
    - inv number

Examples

API

## Development

Run tests

python -m pytest

Run coverage

pytest --cov

Run lint

ruff check .

## Roadmap

- More document domains
- Better synonym matching
- Rule validation
- Rule visualizer
- Rule editor
- Community templates

## License
MIT License

## Running tests

```bash
python -m pytest
```

## Coverage

```bash
python -m pytest --cov
```