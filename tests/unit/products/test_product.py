from decimal import Decimal

from src.products.product import WeightedAverageProduct


def test_empty_product():
    wa_product = WeightedAverageProduct(1)

    assert wa_product.avg() == 0
    assert wa_product.size == 1

    old_v, old_w = wa_product._remove_old_values()
    assert old_v == 0
    assert old_w == 0


def test_add_messages():
    value = Decimal(10.0)
    new_weight = Decimal(2.0)

    wa_product = WeightedAverageProduct(2)
    wa_product.update(value, new_weight)

    assert len(wa_product.weighted_list) == 1 and wa_product.weighted_list[0] == value * new_weight
    assert len(wa_product.weights_list) == 1 and wa_product.weights_list[0] == new_weight
    assert wa_product._sum_values == value * new_weight
    assert wa_product._sum_weight == new_weight
    assert round(wa_product.avg(), 2) == round(value, 2)

    wa_product.update(value, new_weight)

    assert len(wa_product.weighted_list) == 2 and wa_product.weighted_list[1] == value * new_weight
    assert len(wa_product.weights_list) == 2 and wa_product.weights_list[1] == new_weight
    assert wa_product._sum_values == 2 * value * new_weight
    assert wa_product._sum_weight == 2 * new_weight

    assert round(wa_product.avg(), 2) == round(value, 2)


def test_add_messages_when_list_is_full():
    value = Decimal(10.0)
    new_weight = Decimal(2.0)
    size = 1

    wa_product = WeightedAverageProduct(size)
    wa_product.update(Decimal(5.0), Decimal(5.0))
    wa_product.update(value, new_weight)

    assert len(wa_product.weights_list) == size
    assert len(wa_product.weighted_list) == size

    assert wa_product.avg() == value * new_weight / new_weight


def test_max_size_zero():
    wa_product = WeightedAverageProduct(0)
    wa_product.update(Decimal(5.0), Decimal(5.0))
    assert wa_product.avg() == 0


def test_negative_size():
    wa_product = WeightedAverageProduct(-1)
    wa_product.update(Decimal(5.0), Decimal(5.0))
    assert wa_product.avg() == 0
