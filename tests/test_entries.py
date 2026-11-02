def test_start_activity_returns_201(client, created_activity):
    
    start_response = client.post(f"/activities/{created_activity}/start")
    
    assert start_response.status_code == 201
    
    assert start_response.json()["activity_id"] == created_activity
    
    assert start_response.json()["ended_at"] is None
    
    
def test_start_two_activities_returns_201(client, created_activity):
    
    start_response1 = client.post(f"/activities/{created_activity}/start")
    
    assert start_response1.status_code == 201
    
    assert start_response1.json()["activity_id"] == created_activity
    
    assert start_response1.json()["ended_at"] is None
    
    create_response2 = client.post("/activities", json={"name": "test2"})
        
    activity_id2 = create_response2.json()["id"]
    
    start_response2 = client.post(f"/activities/{activity_id2}/start")
    
    assert start_response2.status_code == 201
    
    assert start_response2.json()["activity_id"] == activity_id2
    
    assert start_response2.json()["ended_at"] is None


def test_start_activity_returns_404(client):
    
    start_response = client.post("/activities/999/start")
    
    assert start_response.status_code == 404
    
    
def test_start_activity_returns_409(client, created_activity):
    
    first_start_response = client.post(f"/activities/{created_activity}/start")
    
    assert first_start_response.status_code == 201
    
    second_start_response = client.post(f"/activities/{created_activity}/start")
    
    assert second_start_response.status_code == 409
    

def test_stop_activity_returns_200(client, created_activity):
    
    start_response = client.post(f"/activities/{created_activity}/start")
    
    assert start_response.status_code == 201
    
    stop_response = client.post(f"/activities/{created_activity}/stop")
    
    assert stop_response.status_code == 200
    
    assert stop_response.json()["activity_id"] == created_activity
    
    assert stop_response.json()["ended_at"] is not None
    

def test_stop_activity_returns_404_not_found(client):
    
    stop_response = client.post("/activities/999/stop")
    
    assert stop_response.status_code == 404
    

def test_stop_activity_returns_404_no_open_session(client, created_activity):
    
    stop_response = client.post(f"/activities/{created_activity}/stop")
    
    assert stop_response.status_code == 404
    
    
def test_start_stop_start_activity_returns_201(client, created_activity):
    
    first_start_response = client.post(f"/activities/{created_activity}/start")
    
    assert first_start_response.status_code == 201
    
    stop_response = client.post(f"/activities/{created_activity}/stop")
    
    assert stop_response.status_code == 200
    
    second_start_response = client.post(f"/activities/{created_activity}/start")
    
    assert second_start_response.status_code == 201