import pytest

from cart import Cart

SHARED_CART = Cart()


@pytest.fixture
def cart():
    return SHARED_CART


def test_new_cart_is_empty(cart):
    assert cart.count() == 0


def test_add_items(cart):
    cart.add("A1", 2)
    cart.add("B2")
    assert cart.count() == 3


def test_add_same_sku_twice(cart):
    cart.add("A1")
    cart.add("A1")
    assert cart.items == {"A1": 2}


def test_remove(cart):
    cart.add("A1")
    cart.remove("A1")
    assert cart.count() == 0
