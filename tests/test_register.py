from flask import session


def _post(client, name="Alice", email="alice@example.com", password="securepassword", **kwargs):
    return client.post("/register", data={"name": name, "email": email, "password": password}, **kwargs)


def test_get_register_returns_200(client):
    assert client.get("/register").status_code == 200


def test_valid_post_redirects_to_landing(client):
    resp = _post(client, follow_redirects=True)
    assert resp.status_code == 200


def test_valid_post_sets_session(client):
    _post(client)
    with client.session_transaction() as sess:
        assert sess["user_id"] is not None
        assert sess["user_name"] == "Alice"


def test_duplicate_email_shows_error(client):
    _post(client)
    resp = _post(client)
    assert b"already exists" in resp.data


def test_empty_fields_show_error(client):
    resp = client.post("/register", data={"name": "", "email": "", "password": ""})
    assert b"required" in resp.data


def test_short_password_shows_error(client):
    resp = _post(client, password="short")
    assert b"8 characters" in resp.data


def test_mixed_case_email_is_duplicate(client):
    _post(client, email="alice@example.com")
    resp = _post(client, email="Alice@EXAMPLE.COM")
    assert b"already exists" in resp.data
