import pytest


@pytest.mark.django_db
def test_retrieve_ad(client, ad, jwt_access_token):
    expected_response = {
        "id": ad.pk,
        "name": ad.name,
        "author_id": ad.author_id,
        "author": ad.author.first_name,
        "price": None,
        "description": ad.description,
        "is_published": False,
        "category_id": ad.category_id,
    }

    response = client.get(
        f"/ad/{ad.pk}/",
        HTTP_AUTHORIZATION="Bearer " + jwt_access_token
    )
    assert response.status_code == 200
    assert response.json() == expected_response


@pytest.mark.django_db
def test_error_retrieve_ad(client, ad, jwt_access_token):
    expected_response = {"detail": "Authentication credentials were not provided."}

    response = client.get(
        f"/ad/{ad.pk}/",
    )
    assert response.status_code == 401
    assert response.json() == expected_response
