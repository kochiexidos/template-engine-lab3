# Template Engine — Lab 3

## 1. Project Overview

This project implements a template engine using Python and Jinja2.

It generates structured product reports from data stored in JSON files. The project uses the Justisys product as an example.

The engine detects missing template variables and handles common file and template errors.

## 2. Project Structure


Template_engine/
├── Examples/
│   ├── example.json
│   └── generated_report.txt
├── src/
│   └── Template_engine.py
├── Templates/
│   └── Project_report.txt
├── Test/
│   └── Test_templates_engine.py
├── README.md
└── Requirement.txt


## 3. Features

* Load product information from JSON files.
* Render text templates using Jinja2.
* Generate structured product reports.
* Detect missing template variables.
* Handle missing JSON files.
* Detect invalid JSON data.
* Handle missing templates.

## 4. Requirements

* Python 3
* Jinja2

## 5. Installation

Install the required dependency using:


python -m pip install -r Requirement.txt


Make sure the `Requirement.txt` file contains:


Jinja2


## 6. Generate a Report

From the project root directory, run:


python src/Template_engine.py


The generated report is saved to:


Examples/generated_report.txt


## 7. Run the Tests

Run the validation tests with:


python Test/Test_templates_engine.py


The tests check:

* Missing template variables.
* Missing JSON files.
* Invalid JSON files.
* Missing templates.

A successful test run displays:


PASS: Missing product_name detected.
PASS: Missing JSON file detected.
PASS: Invalid JSON detected.
PASS: Missing template detected.

All validation tests passed!


## 8. Example Product

The example report uses the following product information:

* Product: Justisys
* Plan reference: JUS-5
* Maximum active members: 5
* Monthly price: 25,000 FCFA
* Annual price: 300,000 FCFA
* Billing frequency: Yearly

## 9. Error Handling

The engine uses explicit error handling to report problems such as missing input files, invalid JSON data, and missing template variables.

## 10. Project Status

The core template rendering functionality and four error-handling tests have been verified.

Further validation should follow the official Lab 3 Gold Validation requirements.
