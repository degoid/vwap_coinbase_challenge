from decimal import Decimal


class Product:
    def __init__(self, p_dict: dict):
        self.id = p_dict['product_id']
        self.value = Decimal(p_dict['price'])
        self.weight = Decimal(p_dict['size'])


class WeightedAverageProduct:
    def __init__(self, size: int):
        self.size = size
        self.weighted_list = []
        self.weights_list = []

        self._sum_values = Decimal(0)
        self._sum_weight = Decimal(0)

    def _remove_old_values(self) -> (Decimal, Decimal):
        value = Decimal(0)
        weight = Decimal(0)

        if len(self.weighted_list) == self.size:
            value = self.weighted_list[0]
            self.weighted_list = self.weighted_list[1:]

            weight = self.weights_list[0]
            self.weights_list = self.weights_list[1:]

        return value, weight

    def _add_new_weighted_value(self, value: Decimal, weight: Decimal) -> Decimal:
        new_entry = Decimal(value) * Decimal(weight)
        self.weighted_list.append(new_entry)
        self.weights_list.append(weight)

        return new_entry

    def update(self, value: Decimal, new_weight: Decimal):
        old_weighted_value, old_weight = self._remove_old_values()
        new_weighted_value = self._add_new_weighted_value(value, new_weight)

        # Delete old values and add the newest elements to the total [optimization to avoid iteration over all values]
        self._sum_values = self._sum_values - old_weighted_value + new_weighted_value
        self._sum_weight = self._sum_weight - old_weight + new_weight

    def avg(self):
        return self._sum_values / self._sum_weight