def test_google_gmail_authentication(client):
    payload = {
        "email": "test.developer@gmail.com",
        "name": "Test Developer",
        "picture": "https://lh3.googleusercontent.com/a/test_pic",
        "google_id": "google_test_999"
    }

    # 1. Login / Register
    res = client.post("/auth/google", json=payload)
    assert res.status_code == 200
    user_data = res.json()
    assert user_data["email"] == payload["email"]
    assert user_data["name"] == payload["name"]
    user_id = user_data["id"]

    # 2. Get user profile
    res_me = client.get(f"/auth/me/{user_id}")
    assert res_me.status_code == 200
    assert res_me.json()["email"] == payload["email"]
