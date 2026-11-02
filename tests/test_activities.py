def test_create_activity_returns_201(client):
    
    response = client.post("/activities", json={"name" : "Echecs"})
    
    assert response.status_code == 201
    
    assert response.json()["name"] == "Echecs"
    
def test_create_activity_returns_409(client):
    
    response1 = client.post("/activities", json={"name" : "Chess"})
    
    assert response1.status_code == 201
    
    response2 = client.post("/activities", json={"name" : "Chess"})
    
    assert response2.status_code == 409