import pytest


@pytest.mark.django_db
def test_create_selection(client, user, ad, jwt_access_token):
    expected_response = {
        "id": 1,
        "name": "Test selection",
        "items": [ad.pk],
        "owner": user.pk,
    }

    data = {
        "name": "Test selection",
        "owner": user.pk,
        "items": [ad.pk]
    }

    response = client.post(
        "/selection/create/",
        data,
        content_type='application/json',
        HTTP_AUTHORIZATION="Bearer " + jwt_access_token
    )

    assert response.status_code == 201
    assert response.data == expected_response
