def test_create_and_get_topics(client):
    # 1. Create a topic
    payload = {
        "name": "Artificial Intelligence",
        "description": "Exploration of neural networks and language models."
    }
    response = client.post("/topics", json=payload)
    assert response.status_code == 201
    topic_data = response.json()
    assert topic_data["name"] == payload["name"]
    assert "id" in topic_data

    topic_id = topic_data["id"]

    # 2. Get all topics
    response = client.get("/topics")
    assert response.status_code == 200
    topics = response.json()
    assert len(topics) == 1
    assert topics[0]["id"] == topic_id

    # 3. Get single topic
    response = client.get(f"/topics/{topic_id}")
    assert response.status_code == 200
    assert response.json()["name"] == payload["name"]

    # 4. Delete topic
    response = client.delete(f"/topics/{topic_id}")
    assert response.status_code in [200, 204]

    # 5. Verify deleted
    response = client.get(f"/topics/{topic_id}")
    assert response.status_code == 404
