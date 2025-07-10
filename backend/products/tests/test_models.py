import pytest
from products.factories import ProductFactory

@pytest.mark.django_db
def test_product_str():
    product = ProductFactory()
    assert str(product) == product.name + " (" + str(product.price) + ")"
