def test_live_news_sync(client):
    # Setup topic
    t_res = client.post("/topics", json={"name": "Artificial Intelligence", "description": "AI developments"})
    topic_id = t_res.json()["id"]

    # Trigger live sync for query 'GPT-6'
    res = client.post(f"/articles/sync-live?topic_id={topic_id}&query=GPT-6&max_results=3")
    assert res.status_code == 200
    synced_articles = res.json()
    assert isinstance(synced_articles, list)
    assert len(synced_articles) >= 1
    # Check auto-assigned RealTime tag
    first_art = synced_articles[0]
    tag_names = [t["name"] for t in first_art.get("tags", [])]
    assert "RealTime" in tag_names
