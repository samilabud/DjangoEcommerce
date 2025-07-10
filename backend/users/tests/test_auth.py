import pytest
# pytestmark = pytest.mark.django_db

from django.urls import reverse
from rest_framework.test import APIClient

from users import auth as auth_module

# 1) Fixture supplying the “JWT” we want to see in request.user:
@pytest.fixture
def mock_clerk_jwt():
    return {
        "sub": "test-clerk-id-123",
        "email": "tester@example.com",
    }

# 2) Fixture that monkeypatches Clerk so that authenticate_request and users.list() behave:
@pytest.fixture(autouse=True)
def mock_clerk_sdk(monkeypatch, mock_clerk_jwt):
    # a stand-in for the result of authenticate_request(...)
    class FakeState:
        is_signed_in = True
        reason = None
        payload = mock_clerk_jwt

    # a stand-in for a Clerk user record
    class FakeClerkUser:
        id = mock_clerk_jwt["sub"]
        email_addresses = [type("E", (), {"email_address": mock_clerk_jwt["email"]})()]

    # our fake SDK
    class FakeSDK:
        def __init__(self, bearer_auth):
            pass
        def authenticate_request(self, request, opts):
            return FakeState()
        @property
        def users(self):
            # .list() needs to return an iterable
            return type("U", (), {"list": lambda self: [FakeClerkUser()]})()

    # swap out the real Clerk class
    monkeypatch.setattr(auth_module, "Clerk", FakeSDK)

# 3) The actual test:
@pytest.mark.django_db
def test_who_am_i_populates_request_user(mock_clerk_jwt):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION="Bearer faketoken")
    url = reverse("who_am_i")
    response = client.get(url)

    assert response.status_code == 200, response.content
    data = response.json()
    assert data["id"] == mock_clerk_jwt["sub"]
    assert data["email"] == mock_clerk_jwt["email"]
