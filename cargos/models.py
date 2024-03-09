# This file contains all classes for manage Cargos between cities using airline flights

from datetime import date
from decimal import Decimal
from typing import List, Tuple


class City:
    """
    Represents a city that can function as both an origin and a destination, with connections to other cities.

    Each city is uniquely identified by its `id` and has a corresponding `name`. Additionally, a city can have a list of
    destinations, representing other cities it is connected to.

    Usage:
        - Initialize a city with a unique id, name, and optionally a list of destinations.
        - Use methods to manage destinations:
            - :meth:`add_destination`: Add a city as a destination.
            - :meth:`remove_destination`: Remove an existing destination city.
            - :meth:`set_destinations`: Replace the list of destinations with a new list.
            - :meth:`get_destinations`: Retrieve the list of destinations for the current city.

    Attributes:
        id (int): A unique identifier for the city.
        name (str): The name of the city.
        _destinations (list): A list of City objects representing destinations.

    Examples:
        Creating a city::

            >>> city = City(city_id=1, name="New York City")

        Adding a destination::

            >>> destination_city = City(city_id=2, name="Los Angeles")
            >>> city.add_destination(destination_city)

        Retrieving destinations::

            >>> destinations = city.get_destinations()
            >>> print(destinations)
            [City(id=2, name='Los Angeles')]
    """

    def __init__(self, city_id, name, destinations=None):
        """
        Inits the city instance

        :param int city_id: unique id for city
        :param str name: city name
        :param list destinations: list of cities as destinations
        """
        self.id = city_id
        self.name = name
        self._destinations = destinations or list()

    def add_destination(self, city):
        """
        Add a city to destinations references

        :param City city: city to add in destinations list
        """
        if city not in self._destinations:
            self._destinations.append(city)

    def remove_destination(self, city):
        """
        Removes an existing city from destinations references

        :param City city: city to remove from destinations list
        """
        if city in self._destinations:
            self._destinations.remove(city)

    def set_destinations(self, destinations):
        """
        Complete replace of destinations references

        :param List[City] destinations: list of cities to define as destinations
        """
        self._destinations = destinations or list()

    def get_destinations(self):
        """Returns the list of destinations for current city

        :return: List[City]
        """
        return self._destinations


class CargoSetting:
    """
    Define a Singleton setting class to manage general configurations for cargo shipping.

    This class serves as a Singleton, ensuring that only one instance exists throughout the application
    lifecycle to manage cargo-related settings.

    Usage:
        - Initialize the CargoSetting instance with an optional initial cargo charge.
        - Use methods to manage cargo charges:
            - :meth:`update_cargo_charge`: Update the cargo charge for each package.
            - :meth:`get_cargo_charge`: Retrieve the current cargo charge for each package.
            - :meth:`get_shipping_cargo_charge`: Class method for retrieve the current cargo charge for shipping.

    Attributes:
        _cargo_charge (Decimal): The amount for charges in cargo shipping.

    Examples:
        Initializing the cargo setting::

            >>> cargo_setting = CargoSetting(cargo_charge=Decimal("10.00"))

        Updating the cargo charge::

            >>> cargo_setting.update_cargo_charge(Decimal("12.50"))

        Retrieving the cargo charge::

            >>> cargo_charge = cargo_setting.get_cargo_charge()
            >>> print(cargo_charge)
            Decimal('12.50')

        Retrieving the shipping cargo charge::

            >>> shipping_cargo_charge = CargoSetting.get_shipping_cargo_charge()
            >>> print(shipping_cargo_charge)
            Decimal('10.00')
    """

    def __init__(self, cargo_charge=Decimal("10.00")):
        """
        Inits the cargo setting for shipping

        :param Decimal cargo_charge: amount for charges in cargos shipping
        """
        self._cargo_charge = cargo_charge

    def update_cargo_charge(self, cargo_charge: Decimal):
        """Update the current setting for cargo charges"""
        self._cargo_charge = cargo_charge

    def get_cargo_charge(self) -> Decimal:
        """Returns the current cargo charge for each package"""
        return self._cargo_charge

    @classmethod
    def get_shipping_cargo_charge(cls) -> Decimal:
        """Returns the current cargo charge for shipping"""
        return cls().get_cargo_charge()


class CargoShippingItem:
    """
    Represent a package in the shipping

    This class serves as item for record each package into a cargo shipping, allow to track for each package the charge
    used and keep an accurate registry for reports.

    Usage:
        - Initialize the CargoShippingItm instance with a unique tracking code and the applied cargo charge.

    Attributes:
        tracking_code (str): Unique ID for tracking the package.
        cargo_charge (Decimal): The amount for charges in cargo shipping.

    Examples:
        Initializing the cargo shipping item::

            >>> cargo_shipping_item = CargoShippingItem(tracking_code="abcd", cargo_charge=Decimal("10.00"))

    """

    def __init__(self, tracking_code, cargo_charge):
        """
        Inits the shipping item

        :param str tracking_code: unique ID for tracking the package
        :param Decimal cargo_charge: amount for current package charge
        """
        self.tracking_code = tracking_code
        self.cargo_charge = cargo_charge


class CargoShipping:
    """
    Represents a shipping from origin city to destination city and manage all packages.

    Usage:
        - Initialize a flight shipping with a unique flight_number, date, and optionally a list of shipping items.
        - Use methods to manage shipping items:
            - :meth:`add_shipping_item`: Add a CargoShippingItem to the list of packages.
            - :meth:`remove_shipping_item`: Remove an existing shipping item from packages.
            - :meth:`set_shipping_items`: Replace the list of shipping items with a new list.
            - :meth:`get_shipping_items`: Retrieve the list of shipping items for the current cargo shipping.

    Attributes:
        flight_number (str): A unique identifier for the flight number.
        shipping_date (date): The date for the shipping
        origin_city (City): The origin City for load shippping packages.
        destination_city (City): The destination City for deliver the shippping packages.
        _shipping_items (list): The list of shipping packages

    Examples:
        Creating a CargoShipping::

            >>> destination_city = City(city_id=2, name="Buenos Aires")
            >>> origin_city = City(city_id=1, name="New York City", destinations=[destination_city])
            >>> current_cargo_charge = CargoSetting.get_shipping_cargo_charge()
            >>> shipping_item = CargoShippingItem(tracking_code="123456", cargo_charge=current_cargo_charge)
            >>> cargo_shipping = CargoShipping(
                    flight_number="123456",
                    shipping_date=date(2024, 3, 9),
                    origin_city=origin_city,
                    destination_city=destination_city,
                    shipping_items=[shipping_item]
                )

        Adding a package::

            >>> shipping_item2 = CargoShippingItem(tracking_code="123457", cargo_charge=Decimal("12.50"))
            >>> cargo_shipping.add_shipping_item(shipping_item2)

        Retrieving packages::

            >>> packages = cargo_shipping.get_shipping_items()
            >>> print(packages)
            [
                CargoShippingItem(tracking_code="123456", cargo_charge=Decimal("10.00"),
                CargoShippingItem(tracking_code="123457", cargo_charge=Decimal("12.50")
            ]
    """

    def __init__(
        self,
        flight_number,
        shipping_date,
        origin_city,
        destination_city,
        shipping_items=None,
    ):
        """
        Inits the cargo shipping instance

        :param str flight_number: unique id for shipping
        :param date shipping_date: date for current shipping
        :param City origin_city: city for load packages
        :param City destination_city: city for deliver packages
        :param List[CargoShippingItem] shipping_items: list of CargoShippingItem as packages
        """
        self.flight_number = flight_number
        self.shipping_date = shipping_date
        self.origin_city = origin_city
        self.destination_city = destination_city
        self._shipping_items = shipping_items or list()

    def add_shipping_item(self, shipping_item):
        """
        Add a package to shipping items references

        :param CargoShippingItem shipping_item: package to add in shipping items list
        """
        # this evaluation can be using the shipping_item.tracking_code and update item if the cargo_charge is different
        if shipping_item not in self._shipping_items:
            self._shipping_items.append(shipping_item)

    def remove_shipping_item(self, shipping_item):
        """
        Removes an existing package from shipping items references

        :param CargoShippingItem shipping_item: package to remove from shipping items list
        """
        if shipping_item in self._shipping_items:
            self._shipping_items.remove(shipping_item)

    def set_shipping_items(self, shipping_items):
        """
        Complete replace of destinations references

        :param List[CargoShippingItem] shipping_items: list of cities to define as destinations
        """
        self._shipping_items = shipping_items or list()

    def get_shipping_items(self):
        """Returns the list of cargo shipping items for current city

        :return: List[CargoShippingItem]
        """
        return self._shipping_items

    def get_report_values_for_sales(self) -> Tuple[int, Decimal]:
        """Returns the total packages and total invoice for current shipping"""
        shipping_items = self.get_shipping_items()
        return len(shipping_items), sum(
            [package.cargo_charge for package in shipping_items]
        )
