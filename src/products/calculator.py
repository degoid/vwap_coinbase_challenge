from decimal import Decimal

from src.products.product import Product, WeightedAverageProduct


class VWAPCalculator:
    def __init__(self, max_size: int):
        self.products = {}
        self.max_size = max_size

    def _get_product(self, product: Product):
        product_wa = self.products.get(product.id)

        if product_wa is None:
            product_wa = WeightedAverageProduct(self.max_size)
            self.products[product.id] = product_wa

        return product_wa

    def calculate_vwap(self, product: Product) -> Decimal:
        product_wa = self._get_product(product)
        product_wa.update(product.value, product.weight)

        return product_wa.avg()
