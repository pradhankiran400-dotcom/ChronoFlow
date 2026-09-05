def test_create_and_get_tags(client):
    # Create tag
    payload = {"name": "LLM"}
    response = client.post("/tags", json=payload)
    assert response.status_code == 201
    tag_data = response.json()
    assert tag_data["name"] == "LLM"
    assert "id" in tag_data

    # Duplicate tag creation returns 400
    response_dup = client.post("/tags", json=payload)
    assert response_dup.status_code == 400

    # Get all tags
    response_list = client.get("/tags")
    assert response_list.status_code == 200
    assert len(response_list.json()) >= 1
