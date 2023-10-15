import pytest
from core.user.models import User 


data_user = {
    "username": "johndoe",
    "email": 'johndoe@mail.com',
    "first_name": "John",
    "last_name": "Doe",
    "password":"test_password"
}


@pytest.fixture
def user(db: None) -> User:
    return User.objects.create_user(**data_user)