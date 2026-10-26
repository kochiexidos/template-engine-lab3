import json
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined, UndefinedError


# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = BASE_DIR / "Templates"


class TemplateEngine:
    """Render templates using validated input data."""

    def __init__(self, template_dir: Path = TEMPLATE_DIR):
        self.template_dir = Path(template_dir)

        self.environment = Environment(
            loader=FileSystemLoader(str(self.template_dir)),
            undefined=StrictUndefined,
            autoescape=False,
            keep_trailing_newline=True,
        )

    def load_data(self, json_path: Path) -> dict:
        """Load input data from a JSON file."""
        json_path = Path(json_path)

        try:
            with json_path.open("r", encoding="utf-8") as file:
                data = json.load(file)
        except FileNotFoundError as exc:
            raise FileNotFoundError(f"Input JSON file not found: {json_path}") from exc
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON in {json_path}: {exc}") from exc

        if not isinstance(data, dict):
            raise ValueError("Input JSON must contain a JSON object.")

        return data

    def validate_data(self, data: dict) -> None:
        """Validate data values without rejecting missing template variables."""
        if not isinstance(data, dict):
            raise ValueError("Template data must be a dictionary.")

        string_fields = [
            "product_name",
            "plan_reference",
            "currency",
            "billing_frequency",
        ]

        for field in string_fields:
            if field in data and data[field] is not None:
                value = data[field]
                if not isinstance(value, str) or not value.strip():
                    raise ValueError(f"Field '{field}' must be a non-empty string.")

        if "max_users" in data and data["max_users"] is not None:
            max_users = data["max_users"]
            if type(max_users) is not int or max_users <= 0:
                raise ValueError("Field 'max_users' must be a positive integer.")

        for field in ["monthly_price", "annual_price"]:
            if field in data and data[field] is not None:
                value = data[field]
                if isinstance(value, bool) or not isinstance(value, (int, float)):
                    raise ValueError(f"Field '{field}' must be a number.")
                if value <= 0:
                    raise ValueError(f"Field '{field}' must be greater than zero.")

        optional_fields = ["annual_support", "minimum"]
        for field in optional_fields:
            if field in data and data[field] is not None:
                if not isinstance(data[field], (str, int, float)):
                    raise ValueError(f"Field '{field}' has an invalid value.")

    def render(self, template_name: str, data: dict) -> str:
        """Validate data and render the requested template."""
        self.validate_data(data)

        template_name = str(template_name).strip()
        if not template_name:
            raise ValueError("Template name must be a non-empty string.")

        template = self.environment.get_template(template_name)
        return template.render(data)

    def render_from_json(
        self,
        template_name: str,
        json_path: Path,
    ) -> str:
        """Load, validate and render data from a JSON file."""
        data = self.load_data(json_path)
        return self.render(template_name, data)


def main():
    """Generate the example product report."""
    engine = TemplateEngine()

    data_path = BASE_DIR / "Examples" / "example.json"
    template_name = "Project_report.txt"

    try:
        report = engine.render_from_json(template_name, data_path)

        output_path = BASE_DIR / "Examples" / "generated_report.txt"
        output_path.write_text(report, encoding="utf-8")

        print("Template rendered successfully.")
        print(f"Generated report: {output_path}")
        print("\n--- Report Preview ---\n")
        print(report)

    except (FileNotFoundError, ValueError, OSError, UndefinedError) as error:
        print(f"Error: {error}")

    except Exception as error:
        print(f"Template rendering failed: {error}")


if __name__ == "__main__":
    main()

