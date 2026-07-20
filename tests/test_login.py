def _register(client, name="Alice", email="alice@example.com", password="securepassword"):
    client.post("/register", data={"name": name, "email": email, "password": password})


def _post(client, email="alice@example.com", password="securepassword", **kwargs):
    return client.post("/login", data={"email": email, "password": password}, **kwargs)


def test_get_login_renders_form(client):
    assert client.get("/login").status_code == 200


def test_valid_login_sets_session(client):
    _register(client)
    _post(client)
    with client.session_transaction() as sess:
        assert sess["user_id"] is not None
        assert sess["user_name"] == "Alice"


def test_valid_login_redirects_to_landing(client):
    _register(client)
    resp = _post(client, follow_redirects=True)
    assert resp.status_code == 200
    assert b"Spendly" in resp.data


def test_wrong_password_shows_error(client):
    _register(client)
    client.get("/logout")
    resp = _post(client, password="wrongpassword")
    assert b"Invalid email or password" in resp.data


def test_unknown_email_shows_error(client):
    resp = _post(client, email="nobody@example.com")
    assert b"Invalid email or password" in resp.data


def test_empty_form_shows_error(client):
    resp = _post(client, email="", password="")
    assert b"required" in resp.data


def test_logout_clears_session(client):
    _register(client)
    _post(client)
    client.get("/logout")
    with client.session_transaction() as sess:
        assert "user_id" not in sess


def test_logout_redirects_to_landing(client):
    _register(client)
    _post(client)
    resp = client.get("/logout", follow_redirects=True)
    assert resp.status_code == 200
    assert b"Spendly" in resp.data


def test_logged_in_user_redirected_from_login(client):
    _register(client)
    _post(client)
    resp = client.get("/login")
    assert resp.status_code == 302


def test_logged_in_user_redirected_from_register(client):
    _register(client)
    _post(client)
    resp = client.get("/register")
    assert resp.status_code == 302
