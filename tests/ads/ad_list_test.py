import pytest
from ads.models import Ad
from tests.factories import AdFactory
from typing import List


@pytest.mark.django_db
def test_ad_list_1_item(client, category, user):
    ad = Ad.objects.create(
        name="Cool Jacket",
        author_id=user.pk,
        description="",
        category_id=category.pk
    )
    expected_response = {
        "items": [{
            "id": ad.pk,
            "name": "Cool Jacket",
            "author_id": user.pk,
            "author": "Test",
            "price": None,
            "description": "",
            "is_published": False,
            "category_id": category.pk,
            "image": None
        }],
        "total": 1,
        "num_pages": 1
    }

    response = client.get("/ad/")

    assert response.status_code == 200
    assert response.json() == expected_response


@pytest.mark.django_db
def test_ad_list_batch(client):
    ads: List[Ad] = AdFactory.create_batch(2)

    expected_response = {
        "items": [{
            "id": ads[0].pk,
            "name": ads[0].name,
            "author_id": ads[0].author_id,
            "author": "Test",
            "price": None,
            "description": ads[0].description,
            "is_published": False,
            "category_id": ads[0].category_id,
            "image": None
        }, {
            "id": ads[1].pk,
            "name": ads[1].name,
            "author_id": ads[1].author_id,
            "author": "Test",
            "price": None,
            "description": ads[1].description,
            "is_published": False,
            "category_id": ads[1].category_id,
            "image": None
        }
        ],
        "total": 2,
        "num_pages": 1
    }

    response = client.get("/ad/")
    assert response.status_code == 200
    assert response.json() == expected_response
    assert len(response.json()) == 3
