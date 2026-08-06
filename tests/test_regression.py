from rules.loader import load_question_templates, load_template


def test_load_question_templates_accepts_single_string_template(tmp_path):
    path = tmp_path / "question_templates.yaml"

    path.write_text(
        """
Vendor Profile:
  - key: Vendor Profile
    query_template: "What is the {field} of the vendor in {filename}?"
    fields:
      - vendor
      - phone
    tags:
      - retrieval
""",
        encoding="utf-8",
    )

    result = load_question_templates(path)

    spec = result["Vendor Profile"][0]

    assert spec.query_template == (
        "What is the {field} of the vendor in {filename}?",
    )

def test_question_template_query_template_is_tuple():
    definition = load_template("erp")

    spec = definition.question_templates["Vendor Profile"][0]

    assert isinstance(spec.query_template, tuple)
    assert spec.query_template == (
        "What is the {field} of the vendor in {filename}?",
    )

def test_question_template_query_templates_are_strings():
    definition = load_template("erp")

    for specs in definition.question_templates.values():
        for spec in specs:
            assert all(
                isinstance(template, str)
                for template in spec.query_template
            )