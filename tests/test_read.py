import pytest


def test_find_activity_returns_200(client, create_activity):
    activity_id = create_activity("test")

    find_activity = client.get(f"/activities/{activity_id}")
    assert find_activity.status_code == 200
    assert find_activity.json()["id"] == activity_id
    assert find_activity.json()["name"] == "test"


def test_find_activity_returns_404(client):
    find_activity = client.get("/activities/99")
    assert find_activity.status_code == 404


def test_list_activities_empty(client):
    empty_list_response = client.get("/activities")
    assert empty_list_response.status_code == 200
    assert len(empty_list_response.json()) == 0


def test_list_activities_ordered_by_id(client, create_activity):
    activity_id1 = create_activity("test1")
    activity_id2 = create_activity("test2")
    activity_id3 = create_activity("test3")

    new_list_response = client.get("/activities")
    assert new_list_response.status_code == 200
    assert len(new_list_response.json()) == 3
    assert new_list_response.json()[0]["id"] == activity_id1
    assert new_list_response.json()[1]["id"] == activity_id2
    assert new_list_response.json()[2]["id"] == activity_id3


def test_list_activities_pagination(client, create_activity):
    create_activity("test1")
    activity_id = create_activity("test2")
    create_activity("test3")

    find_response = client.get("/activities", params={"limit": 1, "offset": 1})
    assert find_response.status_code == 200
    assert len(find_response.json()) == 1
    assert find_response.json()[0]["id"] == activity_id
    assert find_response.json()[0]["name"] == "test2"


@pytest.mark.parametrize(
    "invalid_params",
    [{"limit": 0}, {"limit": 101}, {"offset": -1}],
    ids=["limit_too_low", "limit_too_high", "offset_too_low"],
)
def test_list_activities_returns_422(client, invalid_params):
    find_response = client.get("/activities", params=invalid_params)
    assert find_response.status_code == 422


def test_get_activity_entries_returns_404(client):
    find_activity = client.get("/activities/999/entries")
    assert find_activity.status_code == 404


def test_get_activity_entries_no_session(client, create_activity):
    activity_id = create_activity("test")

    find_response = client.get(f"/activities/{activity_id}/entries")
    assert find_response.status_code == 200
    assert len(find_response.json()) == 0


def test_get_activity_entries_ordered_desc(client, create_activity):
    activity_id = create_activity("test")

    start_response1 = client.post(f"/activities/{activity_id}/start")
    assert start_response1.status_code == 201

    stop_response1 = client.post(f"/activities/{activity_id}/stop")
    assert stop_response1.status_code == 200

    start_response2 = client.post(f"/activities/{activity_id}/start")
    assert start_response2.status_code == 201

    find_response = client.get(f"/activities/{activity_id}/entries")
    assert find_response.status_code == 200
    assert len(find_response.json()) == 2
    assert find_response.json()[0]["id"] == start_response2.json()["id"]
    assert find_response.json()[1]["id"] == start_response1.json()["id"]


def test_get_activity_entries_filter_activity(client, create_activity):
    activity_id1 = create_activity("test1")
    activity_id2 = create_activity("test2")

    start_response1 = client.post(f"/activities/{activity_id1}/start")
    assert start_response1.status_code == 201

    start_response2 = client.post(f"/activities/{activity_id2}/start")
    assert start_response2.status_code == 201

    entry_response1 = client.get(f"/activities/{activity_id1}/entries")
    assert len(entry_response1.json()) == 1
    assert entry_response1.json()[0]["activity_id"] == activity_id1


def test_get_activity_entries_pagination(client, create_activity):
    activity_id = create_activity("test")

    start_response1 = client.post(f"/activities/{activity_id}/start")
    assert start_response1.status_code == 201

    stop_response1 = client.post(f"/activities/{activity_id}/stop")
    assert stop_response1.status_code == 200

    start_response2 = client.post(f"/activities/{activity_id}/start")
    assert start_response2.status_code == 201

    find_response1 = client.get(
        f"/activities/{activity_id}/entries", params={"limit": 1}
    )
    assert find_response1.status_code == 200
    assert len(find_response1.json()) == 1

    find_response2 = client.get(
        f"/activities/{activity_id}/entries", params={"limit": 1, "offset": 1}
    )
    assert find_response2.status_code == 200
    assert len(find_response2.json()) == 1
    assert find_response1.json()[0]["id"] == start_response2.json()["id"]
    assert find_response2.json()[0]["id"] == start_response1.json()["id"]


@pytest.mark.parametrize(
    "invalid_params",
    [{"limit": 0}, {"limit": 101}, {"offset": -1}],
    ids=["limit_too_low", "limit_too_high", "offset_too_low"],
)
def test_get_activity_entries_returns_422(client, invalid_params, create_activity):
    activity_id = create_activity("test")

    find_response = client.get(
        f"/activities/{activity_id}/entries", params=invalid_params
    )
    assert find_response.status_code == 422
