from decimal import Decimal

from src.products.product import Product, WeightedAverageProduct


class VWAPCalculator:
    def __init__(self, max_size: int):
        self.products = {}
        self.max_size = max_size

    def _get_product(self, product: Product) -> WeightedAverageProduct:
        """
        Looks for the correct Weigthed Average Product,
        if it doesn't exist, this method will create a new one and add it to the self.products dict.
        """
        product_wa = self.products.get(product.id)

        if product_wa is None:
            product_wa = WeightedAverageProduct(self.max_size)
            self.products[product.id] = product_wa

        return product_wa

    def calculate_vwap(self, product: Product) -> Decimal:
        """
        Calculate the new average of the weighted average product
        """
        product_wa = self._get_product(product)
        product_wa.update(product.value, product.weight)

        return product_wa.avg()
