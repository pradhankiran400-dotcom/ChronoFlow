def test_keyword_and_ai_search(client):
    # Setup topic & article
    t_res = client.post("/topics", json={"name": "Generative AI", "description": "GenAI news"})
    topic_id = t_res.json()["id"]

    client.post("/articles", json={
        "title": "Transformer Architecture Paper",
        "summary": "Attention is All You Need published by Google researchers.",
        "content": "Introduced self-attention mechanisms in deep learning models.",
        "event_date": "2017-06-12",
        "topic_id": topic_id
    })

    # Test Keyword Search
    res_kw = client.get("/search?q=Transformer")
    assert res_kw.status_code == 200
    kw_data = res_kw.json()
    assert "results" in kw_data
    assert len(kw_data["results"]) >= 1
    assert "Transformer" in kw_data["results"][0]["title"]

    # Test AI Vector Search
    res_ai = client.get("/ai/search?q=self-attention neural network")
    assert res_ai.status_code == 200
    ai_data = res_ai.json()
    assert "results" in ai_data
    assert len(ai_data["results"]) >= 1
    assert "similarity_score" in ai_data["results"][0]
