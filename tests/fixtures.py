import pytest
from django.contrib.auth.models import User


@pytest.fixture
@pytest.mark.django_db
def jwt_access_token(client, django_user_model: User):
    username = "test_2"
    password = "test_pwd"

    django_user_model.objects.create_user(
        username=username, password=password
    )

    data = {
        "username": username,
        "password": password
    }

    response = client.post(
        "/user/token/",
        data,
        format='json'
    )

    return response.data["access"]
