from unittest import TestCase

from datetime import date
from decimal import Decimal

from cargos.models import CargoSetting, CargoShipping, CargoShippingItem, City


class TestCityFunctions(TestCase):
    """Test case for evaluate all functions in the model cargos.models.City"""

    def test_init_default(self):
        # Act
        city = City(1, "Buenos Aires")

        # Asserts
        self.assertEqual(city.id, 1)
        self.assertEqual(city.name, "Buenos Aires")
        self.assertEqual(city.get_destinations(), list())

    def test_init_with_destination(self):
        # Arrange
        destinations = [City(1, "Buenos Aires")]

        # Act
        city2 = City(2, "La Habana", destinations)

        # Asserts
        self.assertEqual(city2.get_destinations(), destinations)

    def test_add_destination(self):
        # Arrange
        city1 = City(1, "Buenos Aires")
        city2 = City(2, "La Habana")

        # Act
        city2.add_destination(city1)

        # Asserts
        self.assertEqual(city2.get_destinations(), [city1])

    def test_add_destination_already_exist(self):
        # Arrange
        city1 = City(1, "Buenos Aires")
        city2 = City(2, "La Habana", [city1])

        # Act
        city2.add_destination(city1)

        # Asserts
        self.assertEqual(city2.get_destinations(), [city1])

    def test_remove_destination(self):
        # Arrange
        city1 = City(1, "Buenos Aires")
        city2 = City(2, "La Habana", [city1])

        # Act
        city2.remove_destination(city1)

        # Asserts
        self.assertEqual(city2.get_destinations(), list())

    def test_remove_destination_doesnt_exists(self):
        # Arrange
        city1 = City(1, "Buenos Aires")
        city2 = City(2, "La Habana", [city1])
        city3 = City(3, "Brasilia")

        # Act
        city2.remove_destination(city3)

        # Asserts
        self.assertEqual(city2.get_destinations(), [city1])

    def test_set_destinations(self):
        # Arrange
        city1 = City(1, "Buenos Aires")
        city2 = City(2, "La Habana", [city1])
        city3 = City(3, "Brasilia")

        # Act
        city2.set_destinations([city1, city3])

        # Asserts
        self.assertEqual(city2.get_destinations(), [city1, city3])


class TestCargoSettingFunctions(TestCase):
    """Test case for evaluate all functions in the model cargos.models.CargoSetting"""

    def test_init_default(self):
        # Act
        cargo_setting = CargoSetting()

        # Asserts
        self.assertEqual(cargo_setting.get_cargo_charge(), Decimal("10.00"))

    def test_init_with_charge(self):
        # Act
        cargo_setting = CargoSetting(Decimal("12.50"))

        # Asserts
        self.assertEqual(cargo_setting.get_cargo_charge(), Decimal("12.50"))


class TestCargoShippingItemFunctions(TestCase):
    """Test case for evaluate all functions in the model cargos.models.CargoShippingItem"""

    def test_init_default(self):
        # Act
        package = CargoShippingItem("abcd", Decimal("10.00"))

        # Asserts
        self.assertEqual(package.tracking_code, "abcd")
        self.assertEqual(package.cargo_charge, Decimal("10.00"))


class TestCargoShippingFunctions(TestCase):
    """Test case for evaluate all functions in the model cargos.models.CargoShipping"""

    def setUp(self) -> None:
        # Arrange common setup
        self.origin_city = City(1, "La Habana")
        self.destination_city = City(2, "Buenos Aires")
        self.package1 = CargoShippingItem("abcd", Decimal("10.00"))
        self.shipping_date = date(2024, 3, 9)

    def test_init_default(self):
        # Act
        cargo_shipping = CargoShipping(
            "FL-12345", self.shipping_date, self.origin_city, self.destination_city
        )

        # Asserts
        self.assertEqual(cargo_shipping.flight_number, "FL-12345")
        self.assertEqual(cargo_shipping.shipping_date, self.shipping_date)
        self.assertEqual(cargo_shipping.origin_city, self.origin_city)
        self.assertEqual(cargo_shipping.destination_city, self.destination_city)
        self.assertEqual(cargo_shipping.get_shipping_items(), list())

    def test_init_with_packages(self):
        # Act
        cargo_shipping = CargoShipping(
            "FL-12345",
            self.shipping_date,
            self.origin_city,
            self.destination_city,
            [self.package1],
        )

        # Asserts
        self.assertEqual(cargo_shipping.flight_number, "FL-12345")
        self.assertEqual(cargo_shipping.shipping_date, self.shipping_date)
        self.assertEqual(cargo_shipping.origin_city, self.origin_city)
        self.assertEqual(cargo_shipping.destination_city, self.destination_city)
        self.assertEqual(cargo_shipping.get_shipping_items(), [self.package1])

    def test_add_package(self):
        # Arrange
        cargo_shipping = CargoShipping(
            "FL-12345",
            self.shipping_date,
            self.origin_city,
            self.destination_city,
        )

        # Act
        cargo_shipping.add_shipping_item(self.package1)

        # Asserts
        self.assertEqual(cargo_shipping.get_shipping_items(), [self.package1])

    def test_add_package_already_exist(self):
        # Arrange
        cargo_shipping = CargoShipping(
            "FL-12345",
            self.shipping_date,
            self.origin_city,
            self.destination_city,
            [self.package1],
        )

        # Act
        cargo_shipping.add_shipping_item(self.package1)

        # Asserts
        self.assertEqual(cargo_shipping.get_shipping_items(), [self.package1])

    def test_remove_package(self):
        # Arrange
        cargo_shipping = CargoShipping(
            "FL-12345",
            self.shipping_date,
            self.origin_city,
            self.destination_city,
            [self.package1],
        )

        # Act
        cargo_shipping.remove_shipping_item(self.package1)

        # Asserts
        self.assertEqual(cargo_shipping.get_shipping_items(), list())

    def test_remove_package_doesnt_exists(self):
        # Arrange
        cargo_shipping = CargoShipping(
            "FL-12345",
            self.shipping_date,
            self.origin_city,
            self.destination_city,
            [self.package1],
        )
        package2 = CargoShippingItem("efgh", Decimal("15.00"))

        # Act
        cargo_shipping.remove_shipping_item(package2)

        # Asserts
        self.assertEqual(cargo_shipping.get_shipping_items(), [self.package1])

    def test_set_shipping_items(self):
        # Arrange
        package2 = CargoShippingItem("efgh", Decimal("15.00"))
        package_items = [self.package1, package2]

        cargo_shipping = CargoShipping(
            "FL-12345", self.shipping_date, self.origin_city, self.destination_city
        )

        # Act
        cargo_shipping.set_shipping_items(package_items)

        # Asserts
        self.assertEqual(cargo_shipping.get_shipping_items(), package_items)

    def test_report_values_for_sales(self):
        # Arrange
        package2 = CargoShippingItem("efgh", Decimal("15.00"))
        package_items = [self.package1, package2]

        cargo_shipping = CargoShipping(
            "FL-12345",
            self.shipping_date,
            self.origin_city,
            self.destination_city,
            package_items,
        )

        # Act
        total_packages, total_invoice = cargo_shipping.get_report_values_for_sales()

        # Asserts
        self.assertEqual(total_packages, 2)
        self.assertEqual(total_invoice, Decimal("25.00"))
