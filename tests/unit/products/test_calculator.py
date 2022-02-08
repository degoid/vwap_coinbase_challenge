from decimal import Decimal

from src.products.calculator import VWAPCalculator
from src.products.product import Product


def test_empty_product_list():
    calculator = VWAPCalculator(1)
    product = Product({"product_id": "a", "price": Decimal(10.0), "size": Decimal(2.0)})

    result = calculator._get_product(product)

    assert result.avg() == 0
    assert "a" in calculator.products.keys()

    avg = calculator.calculate_vwap(product)
    assert avg == product.value


def test_empty_product_list_with_size_zero():
    calculator = VWAPCalculator(0)
    product = Product({"product_id": "a", "price": Decimal(10.0), "size": Decimal(2.0)})

    avg = calculator.calculate_vwap(product)
    assert avg == 0


def test_empty_product_list_with_negative_size():
    calculator = VWAPCalculator(-10)
    product = Product({"product_id": "a", "price": Decimal(10.0), "size": Decimal(2.0)})

    avg = calculator.calculate_vwap(product)
    assert avg == 0


