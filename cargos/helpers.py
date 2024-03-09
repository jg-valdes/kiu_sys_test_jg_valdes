import random
from datetime import date, datetime
from decimal import Decimal
from typing import Tuple

from cargos.models import (
    CargoSetting,
    CargoShipping,
    CargoShippingItem,
    City,
)


def _generate_shipping_cities() -> Tuple[City, City]:
    """Generate an origin and destination city"""
    destination_city = City(city_id=2, name="Buenos Aires")
    origin_city = City(city_id=1, name="New York City", destinations=[destination_city])
    return origin_city, destination_city


def _generate_package(use_random_charges=False) -> CargoShippingItem:
    """
    Returns a generic cargo shipping item

    :param bool use_random_charges: allow to define if random charges will be used
    """
    if use_random_charges:
        cargo_charge = CargoSetting(
            cargo_charge=Decimal(random.randint(5, 20))
        ).get_cargo_charge()
    else:
        cargo_charge = CargoSetting.get_shipping_cargo_charge()

    tracking_code = f"{int(datetime.now().timestamp())}"
    return CargoShippingItem(
        tracking_code=tracking_code[-5:], cargo_charge=cargo_charge
    )


def _generate_next_shipping(shipping_date, use_random_charges=False) -> CargoShipping:
    """
    Returns a generic cargo shipping for requested shipping date

    :param date shipping_date: date for shipping
    :param bool use_random_charges: allow to define if random charges will be used
    """
    flight_number = f"{int(datetime.now().timestamp())}"
    origin_city, destination_city = _generate_shipping_cities()
    package = _generate_package(use_random_charges)

    cargo_shipping = CargoShipping(
        flight_number=flight_number,
        shipping_date=shipping_date,
        origin_city=origin_city,
        destination_city=destination_city,
        shipping_items=[package],
    )
    return cargo_shipping


def generate_shipping_list(shipping_date, total_items=5, use_random_charges=False):
    """
    Generate an iterator with cargo shipping using the requested date

    :param date shipping_date:
    :param int total_items: define the total items that will be processed
    :param bool use_random_charges: allow to define if random charges will be used
    :return: CargoShipping iterator
    """
    for _ in range(total_items):
        yield _generate_next_shipping(shipping_date, use_random_charges)
