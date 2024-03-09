Test for Kiu Sys
==================

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

This is a simple app to represent a testing scenario for generate invoice reports by date. Follow the instructions to build your app:

Given the following System:
An Airline company is engaged in the business of transporting air cargo between different origins and destinations. The company can only transport packages of Customers.
For each package transported the airline charges $10.00. There must be a method that generates a report with the total packages transported and the total collected for a given day.
You are requested to:
+ Program in Python the classes and responsibilities of the system, create the unit tests that you consider necessary.
+ Do not use any framework or database in the solution (keep it simple).
 
## Dependencies

- Python 3.11.4

## Development setup

```
# Install dependencies for develop only
pip install -r requirements.txt
```

## Run the script for test

Open a python shell in the root and follow the instructions

```
>>> from cargos import services
>>> from datetime import date
>>> shipping_date = date(2024, 3, 9)
>>> services.print_cargo_report_for_date(shipping_date)
Company report:
Total packages shipped: 5
Total invoice: 50
```

- By default the script process 5 Cargos Shipping, you can define more by define total_items param:
```
>>> services.print_cargo_report_for_date(shipping_date, total_items=3)
Company report:
Total packages shipped: 3
Total invoice: 30
```
- Also, it's possible to execute with random cargo charges by adding use_random_charges param:
```
>>> services.print_cargo_report_for_date(shipping_date, total_items=3, use_random_charges=True)
Company report:
Total packages shipped: 3
Total invoice: 28
```

### Testing setup (to run in CI/CD)

```
# Run tests
>>> python -m unittest
Ran 19 tests in (X)s

OK
```

#### Additional information:

- [Unittest documentation](https://docs.python.org/3/library/unittest.html)
- [Black formatting](https://black.readthedocs.io/en/stable/getting_started.html)