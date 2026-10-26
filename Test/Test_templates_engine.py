import sys
import tempfile
from pathlib import Path

from jinja2 import UndefinedError, TemplateNotFound

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR / "src"))

from Template_engine import TemplateEngine

def test_missing_variable():
    """Verify that a missing variable in the template is detected."""
    engine = TemplateEngine()

    incomplete_data = {
        "plan_reference": "JUS-5",
        "max_users": 5,
        "monthly_price": 25000,
        "currency": "FCFA",
        "billing_frequency": "yearly",
        "annual_price": 300000,
        "annual_support": None,
        "minimum": None,
        "alternative_currency": "any currency (typed)",
        "alternative_currency_price": "price typed on the quote",
    }

    try:
        engine.render("Project_report.txt", incomplete_data)

    except ValueError as error:
        assert "product_name" in str(error)
        print("PASS: Missing product_name detected.")
        return

    except UndefinedError as error:
        assert "product_name" in str(error)
        print("PASS: Missing product_name detected.")
        return

    raise AssertionError(
        "FAIL: Missing product_name was not detected."
    )


def test_missing_json_file():
    """Verify that a missing JSON file is detected."""
    engine = TemplateEngine()

    try:
        engine.load_data(
            BASE_DIR / "Examples" / "does_not_exist.json"
        )

    except FileNotFoundError:
        print("PASS: Missing JSON file detected.")
        return

    raise AssertionError(
        "FAIL: Missing JSON file was not detected."
    )


def test_invalid_json():
    """Verify that malformed JSON is detected."""
    engine = TemplateEngine()

    with tempfile.TemporaryDirectory() as temp_dir:
        json_path = Path(temp_dir) / "invalid.json"

        json_path.write_text(
            '{"product_name": "Justisys"',
            encoding="utf-8",
        )

        try:
            engine.load_data(json_path)

        except ValueError as error:
            assert "Invalid JSON" in str(error)
            print("PASS: Invalid JSON detected.")
            return

    raise AssertionError(
        "FAIL: Invalid JSON was not detected."
    )


def test_missing_template():
    """Verify that a missing template is detected."""
    engine = TemplateEngine()

    try:
        engine.render(
            "does_not_exist.txt",
            {"product_name": "Justisys"},
        )

    except TemplateNotFound:
        print("PASS: Missing template detected.")
        return

    raise AssertionError(
        "FAIL: Missing template was not detected."
    )


def test_invalid_max_users():
    """Verify that zero members is rejected."""
    engine = TemplateEngine()

    data = {
        "product_name": "Justisys",
        "plan_reference": "JUS-5",
        "max_users": 0,
        "monthly_price": 25000,
        "currency": "FCFA",
        "billing_frequency": "yearly",
        "annual_price": 300000,
        "annual_support": None,
        "minimum": None,
        "alternative_currency": "any currency (typed)",
        "alternative_currency_price": "price typed on the quote",
    }

    try:
        engine.render("Project_report.txt", data)

    except ValueError as error:
        assert "max_users" in str(error)
        print("PASS: Invalid max_users detected.")
        return

    raise AssertionError(
        "FAIL: Invalid max_users was not detected."
    )


def test_negative_price():
    """Verify that a negative monthly price is rejected."""
    engine = TemplateEngine()

    data = {
        "product_name": "Justisys",
        "plan_reference": "JUS-5",
        "max_users": 5,
        "monthly_price": -1000,
        "currency": "FCFA",
        "billing_frequency": "yearly",
        "annual_price": 300000,
        "annual_support": None,
        "minimum": None,
        "alternative_currency": "any currency (typed)",
        "alternative_currency_price": "price typed on the quote",
    }

    try:
        engine.render("Project_report.txt", data)

    except ValueError as error:
        assert "monthly_price" in str(error)
        print("PASS: Negative price detected.")
        return

    raise AssertionError(
        "FAIL: Negative price was not detected."
    )


def test_valid_data():
    """Verify that valid product data generates a report."""
    engine = TemplateEngine()

    data = {
        "product_name": "Justisys",
        "plan_reference": "JUS-5",
        "max_users": 5,
        "monthly_price": 25000,
        "currency": "FCFA",
        "billing_frequency": "yearly",
        "annual_price": 300000,
        "annual_support": None,
        "minimum": None,
        "alternative_currency": "any currency (typed)",
        "alternative_currency_price": "price typed on the quote",
    }

    report = engine.render("Project_report.txt", data)

    assert "Justisys" in report
    assert "JUS-5" in report
    assert "25,000 FCFA" in report
    assert "300,000 FCFA" in report

    print("PASS: Valid product data rendered.")


def test_json_not_object():
    """Verify that JSON data must be an object."""
    engine = TemplateEngine()

    with tempfile.TemporaryDirectory() as temp_dir:
        json_path = Path(temp_dir) / "list.json"

        json_path.write_text(
            '["Justisys", 5, 25000]',
            encoding="utf-8",
        )

        try:
            engine.load_data(json_path)

        except ValueError as error:
            assert "JSON object" in str(error)
            print("PASS: Non-object JSON detected.")
            return

    raise AssertionError(
        "FAIL: Non-object JSON was not detected."
    )


def test_empty_template_name():
    """Verify that an empty template name is rejected."""
    engine = TemplateEngine()

    try:
        engine.render("   ", {"product_name": "Justisys"})

    except ValueError as error:
        assert "Template name" in str(error)
        print("PASS: Empty template name detected.")
        return

    raise AssertionError(
        "FAIL: Empty template name was not detected."
    )


if __name__ == "__main__":
    test_missing_variable()
    test_missing_json_file()
    test_invalid_json()
    test_missing_template()
    test_invalid_max_users()
    test_negative_price()
    test_valid_data()
    test_json_not_object()
    test_empty_template_name()

    print("\nAll validation tests passed!")