# Spec: Login and Logout

## Overview

Allow registered users to sign in with their email and password, and sign out when done. The login route verifies credentials against the stored password hash, opens a Flask session on success, and redirects to the landing page. The logout route clears the session and redirects back to the landing page. This step also updates the nav bar to reflect the user's authentication state — showing a "Sign out" link when logged in and "Sign in" / "Get started" when logged out.

---

## Depends on

- Step 1 — Database setup (`users` table, `get_db()`, `init_db()`, `seed_db()` must be complete)
- Step 2 — Registration (`get_user_by_email()` and `create_user()` must be in `database/db.py`)

---

## Routes

- `GET /login` — render login form — public (already exists, convert to handle both methods)
- `POST /login` — verify credentials, set session, redirect — public
- `GET /logout` — clear session, redirect to landing — public (currently a stub)

---

## Database changes

No new tables or columns. No new helper functions needed — `get_user_by_email()` from Step 2 is sufficient. Use `werkzeug.security.check_password_hash` directly in the route.

---

## Templates

- **Modify** `templates/base.html` — update `<div class="nav-links">` to conditionally show:
  - When **not** logged in: "Sign in" link + "Get started" link (current behavior)
  - When logged in (`session.user_id` is set): "Sign out" link only (pointing to `/logout`)
- **No changes** to `templates/login.html` — the form already POSTs to `/login` and renders `{{ error }}`

---

## Files to change

- `app.py` — convert `GET /login` stub to a `GET/POST` route; implement `GET /logout`
- `templates/base.html` — conditional nav links based on `session`

## Files to create

- `tests/test_login.py` — login and logout tests

---

## New dependencies

No new dependencies. `check_password_hash` is already available from `werkzeug.security`.

---

## Rules for implementation

- No SQLAlchemy or ORMs — use `sqlite3` directly via `get_db()`
- Parameterised queries only — never f-strings or `%` formatting in SQL
- Passwords verified with `werkzeug.security.check_password_hash` — never compare plaintext
- On failed login, render `login.html` with `error="Invalid email or password."` — same message for both wrong email and wrong password (do not reveal which)
- On successful login, set `session["user_id"]` and `session["user_name"]`, then redirect to `url_for("landing")`
- Logout must call `session.clear()` (not just `session.pop()`), then redirect to `url_for("landing")`
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Use `url_for()` for every internal link — never hardcode URLs
- Import `check_password_hash` from `werkzeug.security` in `app.py`

---

## Definition of done

- [ ] `GET /login` returns 200 and renders the login form
- [ ] Submitting valid credentials sets `session["user_id"]` and `session["user_name"]`
- [ ] Successful login redirects to `GET /` (landing page)
- [ ] Wrong password re-renders login with "Invalid email or password."
- [ ] Unknown email re-renders login with "Invalid email or password."
- [ ] Empty form submission re-renders login with a validation error
- [ ] `GET /logout` clears the session and redirects to `GET /`
- [ ] After logout, `session["user_id"]` is no longer set
- [ ] Nav bar shows "Sign out" link when a user is logged in
- [ ] Nav bar shows "Sign in" and "Get started" when no user is logged in
- [ ] All tests in `tests/test_login.py` pass with `pytest`
