from cart import get_implementations

make_cart = get_implementations()


def test_shop():
    cart = make_cart()
    assert not len(cart.get_items())
    cart.add_item({'name': 'car', 'price': 3}, 5)
    cart.add_item({'name': 'house', 'price': 10}, 2)
    assert len(cart.get_items()) == 2
    assert cart.get_cost() == 35
    assert cart.get_items() == [{'good': {'name': 'car', 'price': 3}, 'count': 5},
    {'good': {'name': 'house', 'price': 10}, 'count': 2}]
    assert cart.get_count() == 7
