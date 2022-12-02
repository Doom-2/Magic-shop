import pytest


@pytest.mark.django_db
def test_create_ad(client, category, user):
    expected_response = {
        "id": 1,
        "name": "Cool Jacket",
        "author_id": user.pk,
        "author": "Test",
        "price": 1,
        "description": "Отдам даром, не подошел",
        "is_published": False,
        "category_id": category.pk,
        "image": None
    }

    data = {
        "name": "Cool Jacket",
        "author_id": user.pk,
        "price": 1,
        "description": "Отдам даром, не подошел",
        "is_published": False,
        "category_id": category.pk
    }

    response = client.post(
        "/ad/create/",
        data,
        content_type='application/json',
    )

    assert response.status_code == 201
    assert response.json() == expected_response


@pytest.mark.django_db
def test_error_create_ad(client, category, user):
    expected_response = {
        "name": ["Ensure this value has at least 10 characters (it has 9)."],
        "price": ["Ensure this value is greater than or equal to 0."]
    }

    data = {
        "name": "Cool Jack",
        "author_id": user.pk,
        "price": -10,
        "category_id": category.pk
    }

    response = client.post(
        "/ad/create/",
        data,
        content_type='application/json',
    )

    assert response.status_code == 422
    assert response.json() == expected_response
