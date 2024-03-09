from unittest import TestCase, mock

from datetime import date
from decimal import Decimal

from cargos.services import (
    get_cargo_invoices_report_for_date,
    print_cargo_report_for_date,
)


@mock.patch("cargos.services.generate_shipping_list")
class TestGetCargoInvoiceReportFunctions(TestCase):
    """Test case for evaluate all paths for get CargoShipping reports for custom shipping dates"""

    def test_get_cargo_invoices_report_for_date__empty_result(
        self, mock_get_shipping_list
    ):
        # Arrange
        mock_shipping = mock.Mock(shipping_date=date(2024, 3, 9))
        mock_shipping.get_report_values_for_sales.return_value = 2, Decimal("20.00")

        mock_get_shipping_list.return_value = [mock_shipping]
        shipping_date = date(2024, 3, 10)

        # Act
        total_packages, total_invoice = get_cargo_invoices_report_for_date(
            shipping_date
        )

        # Asserts
        self.assertEqual(total_packages, 0)
        self.assertEqual(total_invoice, Decimal("0.00"))
        mock_get_shipping_list.assert_called_with(shipping_date, 5, False)
        mock_shipping.get_report_values_for_sales.assert_not_called()

    def test_get_cargo_invoices_report_for_date__valid_results(
        self, mock_get_shipping_list
    ):
        # Arrange
        mock_shipping = mock.Mock(shipping_date=date(2024, 3, 9))
        mock_shipping.get_report_values_for_sales.return_value = 2, Decimal("20.00")

        mock_get_shipping_list.return_value = [mock_shipping]
        shipping_date = date(2024, 3, 9)

        # Act
        total_packages, total_invoice = get_cargo_invoices_report_for_date(
            shipping_date
        )

        # Asserts
        self.assertEqual(total_packages, 2)
        self.assertEqual(total_invoice, Decimal("20.00"))
        mock_get_shipping_list.assert_called_with(shipping_date, 5, False)
        mock_shipping.get_report_values_for_sales.assert_called_once()


@mock.patch("builtins.print")
@mock.patch("cargos.services.get_cargo_invoices_report_for_date")
class TestGetCargoInvoiceReportFunctions(TestCase):
    """Test case for evaluate all paths for get CargoShipping reports print for custom shipping dates"""

    def test_print_cargo_report_for_date__valid_results(
        self, mock_get_invoice_report, mock_print
    ):
        # Arrange
        shipping_date = date(2024, 3, 9)
        mock_get_invoice_report.return_value = 2, Decimal("20.00")

        # Act
        print_cargo_report_for_date(shipping_date)

        # Asserts
        mock_get_invoice_report.assert_called_with(shipping_date, 5, False)
        mock_print.assert_has_calls(
            [
                mock.call("Company report:"),
                mock.call("Total packages shipped:", 2),
                mock.call("Total invoice:", Decimal("20.00")),
            ]
        )
