# Spec: Registration

## Overview

Allow a new visitor to create a Spendly account. The user fills in their name, email, and password; the app validates the input, stores a hashed password, opens a session, and redirects to the landing page. This is the first step that introduces Flask sessions and user identity to the app.

---

## Depends on

- Step 1 — Database setup (`users` table, `get_db()`, `init_db()`, `seed_db()` must be complete)

---

## Routes

- `GET /register` — render registration form — public (already exists as stub)
- `POST /register` — handle form submission, create user, set session — public

---

## Database changes

No new tables or columns. The `users` table from Step 1 is used as-is.

New helper functions needed in `database/db.py`:

- `get_user_by_email(email)` — returns a `sqlite3.Row` or `None`
- `create_user(name, email, password)` — hashes password, inserts row, returns new user as `dict`

---

## Templates

- **Modify** `templates/register.html` — already renders `{{ error }}`; no structural changes needed
- No new templates

---

## Files to change

- `app.py` — add `SECRET_KEY`, update imports, convert `GET /register` stub to handle `POST`
- `database/db.py` — add `get_user_by_email()` and `create_user()`

## Files to create

- `tests/conftest.py` — pytest fixture with isolated per-test SQLite DB
- `tests/test_register.py` — registration tests
- `pytest.ini` — set `pythonpath = .` so `import app` resolves

---

## New dependencies

No new dependencies.

---

## Rules for implementation

- No SQLAlchemy or ORMs — use `sqlite3` directly
- Parameterised queries only — never f-strings or `%` formatting in SQL
- Passwords hashed with `werkzeug.security.generate_password_hash` — never stored plaintext
- `SECRET_KEY` read from environment: `os.environ.get("SECRET_KEY", "dev-secret-change-in-prod")`
- Email stored and looked up in lowercase — normalise with `.strip().lower()` on input
- All templates extend `base.html`
- Use CSS variables — never hardcode hex values
- DB helpers open and close their own connection — do not pass connections between functions

---

## Definition of done

- [ ] `GET /register` returns 200 and renders the registration form
- [ ] Valid POST creates a row in `users` with a hashed (not plaintext) password
- [ ] After successful registration, `session["user_id"]` and `session["user_name"]` are set
- [ ] Successful registration redirects to `GET /`
- [ ] Submitting an empty form re-renders the page with "All fields are required."
- [ ] Password shorter than 8 characters re-renders with "Password must be at least 8 characters."
- [ ] Registering with an already-used email re-renders with "An account with that email already exists."
- [ ] Email comparison is case-insensitive (`Alice@Example.COM` matches `alice@example.com`)
- [ ] All 7 tests in `tests/test_register.py` pass with `pytest`
