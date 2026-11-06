def test_start_activity_returns_201(client, create_activity):
    activity_id = create_activity("test")

    start_response = client.post(f"/activities/{activity_id}/start")
    assert start_response.status_code == 201
    assert start_response.json()["activity_id"] == activity_id
    assert start_response.json()["ended_at"] is None


def test_start_two_activities_returns_201(client, create_activity):
    activity_id1 = create_activity("test1")

    start_response1 = client.post(f"/activities/{activity_id1}/start")
    assert start_response1.status_code == 201
    assert start_response1.json()["activity_id"] == activity_id1
    assert start_response1.json()["ended_at"] is None

    activity_id2 = create_activity("test2")

    start_response2 = client.post(f"/activities/{activity_id2}/start")
    assert start_response2.status_code == 201
    assert start_response2.json()["activity_id"] == activity_id2
    assert start_response2.json()["ended_at"] is None


def test_start_activity_returns_404(client):
    start_response = client.post("/activities/999/start")
    assert start_response.status_code == 404


def test_start_activity_returns_409(client, create_activity):
    activity_id = create_activity("test")

    first_start_response = client.post(f"/activities/{activity_id}/start")
    assert first_start_response.status_code == 201

    second_start_response = client.post(f"/activities/{activity_id}/start")
    assert second_start_response.status_code == 409


def test_stop_activity_returns_200(client, create_activity):
    activity_id = create_activity("test")

    start_response = client.post(f"/activities/{activity_id}/start")
    assert start_response.status_code == 201

    stop_response = client.post(f"/activities/{activity_id}/stop")
    assert stop_response.status_code == 200
    assert stop_response.json()["activity_id"] == activity_id
    assert stop_response.json()["ended_at"] is not None


def test_stop_activity_returns_404_not_found(client):
    stop_response = client.post("/activities/999/stop")
    assert stop_response.status_code == 404


def test_stop_activity_returns_404_no_open_session(client, create_activity):
    activity_id = create_activity("test")

    stop_response = client.post(f"/activities/{activity_id}/stop")
    assert stop_response.status_code == 404


def test_start_stop_start_activity_returns_201(client, create_activity):
    activity_id = create_activity("test")

    first_start_response = client.post(f"/activities/{activity_id}/start")
    assert first_start_response.status_code == 201

    stop_response = client.post(f"/activities/{activity_id}/stop")
    assert stop_response.status_code == 200

    second_start_response = client.post(f"/activities/{activity_id}/start")
    assert second_start_response.status_code == 201
