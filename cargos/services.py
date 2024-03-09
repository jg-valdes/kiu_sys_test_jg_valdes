from decimal import Decimal
from typing import Tuple

from cargos.helpers import generate_shipping_list


def get_cargo_invoices_report_for_date(
    shipping_date, total_items=5, use_random_charges=False
) -> Tuple[int, Decimal]:
    """
    Check for shipping date and calculate total invoice and total packages

    :param datetime.date shipping_date: requested shipping date
    :param int total_items: allow to define a total of cargos shipping to process
    :param bool use_random_charges: allow to define if random charges will be used
    """
    # load fixture for shipping
    cargos_shipping_list = generate_shipping_list(
        shipping_date, total_items, use_random_charges
    )

    # filter cargos to get only valid shipping using shipping date
    shipping_list_to_process = [
        shipping
        for shipping in cargos_shipping_list
        if shipping.shipping_date == shipping_date
    ]

    # build metrics for report
    total_packages = 0
    total_invoice = Decimal("0")

    # for each valid shipping we count packages and invoices
    for shipping in shipping_list_to_process:
        shipping_packages, shipping_invoice = shipping.get_report_values_for_sales()
        total_packages += shipping_packages
        total_invoice += shipping_invoice

    return total_packages, total_invoice


def print_cargo_report_for_date(shipping_date, total_items=5, use_random_charges=False):
    """
    Print a report for Airline total packages and shipping, you can optionally define a total of cargos shipping
    to process. Also, if define random cargos you will get random total invoices

    :param datetime.date shipping_date: requested shipping date
    :param int total_items: allow to define a total of cargos shipping to process
    :param bool use_random_charges: allow to define if random charges will be used
    """
    total_packages, total_invoice = get_cargo_invoices_report_for_date(
        shipping_date, total_items, use_random_charges
    )
    print("Company report:")
    print("Total packages shipped:", total_packages)
    print("Total invoice:", total_invoice)
