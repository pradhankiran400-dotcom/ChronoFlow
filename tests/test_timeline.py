def test_timeline_endpoint(client):
    # Setup topic & articles
    t_res = client.post("/topics", json={"name": "Computing", "description": "History of computing"})
    topic_id = t_res.json()["id"]

    client.post("/articles", json={
        "title": "ENIAC Revealed",
        "summary": "First general-purpose electronic computer.",
        "content": "ENIAC was announced to the public in 1946.",
        "event_date": "1946-02-14",
        "topic_id": topic_id
    })

    client.post("/articles", json={
        "title": "IBM Personal Computer",
        "summary": "IBM introduced the 5150 PC.",
        "content": "The IBM PC revolutionized home computing in 1981.",
        "event_date": "1981-08-12",
        "topic_id": topic_id
    })

    # Test GET /timeline
    res = client.get(f"/timeline?topic_id={topic_id}")
    assert res.status_code == 200
    data = res.json()
    assert "events" in data
    assert len(data["events"]) == 2
    # Check chronological ordering
    assert data["events"][0]["event_date"] == "1946-02-14"
    assert data["events"][1]["event_date"] == "1981-08-12"

    # Test date filtering
    res_filtered = client.get(f"/timeline?topic_id={topic_id}&start_date=1980-01-01")
    assert res_filtered.status_code == 200
    assert len(res_filtered.json()["events"]) == 1
    assert res_filtered.json()["events"][0]["title"] == "IBM Personal Computer"
