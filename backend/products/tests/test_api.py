import pytest
from rest_framework.test import APIClient
from users.factories import UserFactory

@pytest.mark.django_db
def test_create_product_authenticated():
    user = UserFactory()
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.post("/api/v1/products/", {"name": "Test", "price": 9.99})
    assert response.status_code == 201
