def test_article_crud(client):
    # 1. Create topic & tag
    t_res = client.post("/topics", json={"name": "Space Exploration", "description": "Space milestones"})
    topic_id = t_res.json()["id"]

    tag_res = client.post("/tags", json={"name": "Moon"})
    tag_id = tag_res.json()["id"]

    # 2. Create article
    art_payload = {
        "title": "Apollo 11 Moon Landing",
        "summary": "First humans landed on the Moon.",
        "content": "Neil Armstrong and Buzz Aldrin stepped onto the lunar surface in 1969.",
        "event_date": "1969-07-20",
        "source_url": "https://nasa.gov/apollo11",
        "topic_id": topic_id,
        "tag_ids": [tag_id]
    }
    res = client.post("/articles", json=art_payload)
    assert res.status_code == 201
    art_data = res.json()
    assert art_data["title"] == art_payload["title"]
    assert len(art_data["tags"]) == 1
    assert art_data["tags"][0]["name"] == "Moon"

    art_id = art_data["id"]

    # 3. Get article
    res_get = client.get(f"/articles/{art_id}")
    assert res_get.status_code == 200
    assert res_get.json()["event_date"] == "1969-07-20"

    # 4. Update article
    update_payload = {"summary": "Apollo 11 historic lunar landing updated."}
    res_upd = client.put(f"/articles/{art_id}", json=update_payload)
    assert res_upd.status_code == 200
    assert res_upd.json()["summary"] == update_payload["summary"]

    # 5. Delete article
    res_del = client.delete(f"/articles/{art_id}")
    assert res_del.status_code == 200

    # Verify deleted
    res_get_del = client.get(f"/articles/{art_id}")
    assert res_get_del.status_code == 404
