import os
import pytest

# Allow DB access in these tests
pytestmark = pytest.mark.django_db

# Ensure Django settings are loaded before DRF imports
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_backend.settings')

from django.urls import reverse
from rest_framework.test import APIClient
from users.auth import Clerk  # import your Clerk class

@pytest.fixture(autouse=True)
def json_renderer(settings):
    """
    Force JSON-only responses so DRF won't try to render HTML.
    """
    settings.REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = [
        'rest_framework.renderers.JSONRenderer',
    ]

@pytest.fixture
def mock_clerk_jwt(monkeypatch):
    """
    Monkey-patch Clerk.jwt.verify to return a fake payload.
    """
    fake_payload = {
        'sub': 'test-clerk-id-123',
        'email': 'tester@example.com',
    }

    class DummyJWT:
        @staticmethod
        def verify(token):
            return fake_payload

    monkeypatch.setattr(Clerk, 'jwt', DummyJWT, raising=False)
    return fake_payload

def test_who_am_i_populates_request_user(mock_clerk_jwt):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Bearer faketoken')

    url = reverse('who_am_i')
    response = client.get(url)

    assert response.status_code == 200
    data = response.json()
    assert data['id'] == mock_clerk_jwt['sub']
    assert data['email'] == mock_clerk_jwt['email']
