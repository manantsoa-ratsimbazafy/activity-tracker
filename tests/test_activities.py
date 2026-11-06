import pytest


def test_create_activity_returns_201(client):
    response = client.post("/activities", json={"name": "a" * 20})
    assert response.status_code == 201
    assert response.json()["name"] == "a" * 20


def test_create_activity_returns_409(client):
    response1 = client.post("/activities", json={"name": "Chess"})
    assert response1.status_code == 201

    response2 = client.post("/activities", json={"name": "Chess"})
    assert response2.status_code == 409


@pytest.mark.parametrize(
    "payload",
    [{"name": ""}, {"name": "a" * 21}, {"name": " " * 40}, {}, {"name": 422}],
    ids=["empty_name", "too_long", "only_spaces", "missing_name", "wrong_type"],
)
def test_create_activity_returns_422(client, payload):
    response = client.post("/activities", json=payload)
    assert response.status_code == 422
