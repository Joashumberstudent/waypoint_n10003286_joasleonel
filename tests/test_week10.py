import pytest

from django.test import Client


@pytest.mark.django_db
def test_home_page():
    client = Client()

    response = client.get("/")

    assert response.status_code == 200
    assert b"Welcome to Waypoint!" in response.content


@pytest.mark.django_db
def test_report_get():
    client = Client()

    response = client.get("/report/")

    assert response.status_code == 200
    assert b"Report a Trail" in response.content


@pytest.mark.django_db
def test_report_post():
    client = Client()

    response = client.post(
        "/report/",
        {
            "name": "Leonel",
            "email": "leonel@example.com",
            "trail": "Mont Royal",
            "note": "Trail needs an update.",
        },
    )

    assert response.status_code == 200
    assert b"Thank you, Leonel!" in response.content
    assert b"Mont Royal" in response.content


@pytest.mark.django_db
def test_report_post_without_csrf():
    client = Client(enforce_csrf_checks=True)

    response = client.post(
        "/report/",
        {
            "name": "Leonel",
            "email": "leonel@example.com",
            "trail": "Mont Royal",
            "note": "Test",
        },
    )

    assert response.status_code == 403


@pytest.mark.django_db
def test_search_without_query():
    client = Client()

    response = client.get("/search/")

    assert response.status_code == 200


@pytest.mark.django_db
def test_search_with_query():
    client = Client()

    response = client.get(
        "/search/?q=Mont%20Royal"
    )

    assert response.status_code == 200
    assert b"Mont Royal" in response.content