# Plan: Step 1 — Database Setup

## Context

Spendly's `database/db.py` was a comment stub. This step implements the data-layer foundation that every subsequent feature (auth, profile, expenses) depends on. Two files changed: `database/db.py` got three functions, and `app.py` got startup wiring. No new packages, no routes, no templates.

## Status: COMPLETE

---

## Files Modified

- `database/db.py` — implemented `get_db()`, `init_db()`, `seed_db()`
- `app.py` — added import + startup context block

---

## What Was Implemented

### `database/db.py`

**`get_db()`** — opens `spendly.db` at project root (path resolved via `os.path.dirname(__file__)` for portability), sets `row_factory = sqlite3.Row` and `PRAGMA foreign_keys = ON`.

**`init_db()`** — creates `users` and `expenses` tables with `CREATE TABLE IF NOT EXISTS`. Uses `DEFAULT (datetime('now'))` with parentheses (required by SQLite for function calls in defaults).

**`seed_db()`** — guards with `SELECT COUNT(*)` early-exit, inserts Demo User with werkzeug-hashed password, then 8 sample expenses across all 7 categories via `executemany()`. Uses `last_insert_rowid()` to get the new user's id rather than hardcoding 1.

### `app.py`

Added import at top:
```python
from database.db import get_db, init_db, seed_db
```

Added startup block before `app.run()`:
```python
if __name__ == "__main__":
    with app.app_context():
        init_db()
        seed_db()
    app.run(debug=True, port=5001)
```

---

## Verification Results

- `spendly.db` created at project root on first run
- Both tables present with correct schema
- 1 demo user: `Demo User / demo@spendly.com`
- 8 expenses across 7 categories (Food x2, Transport, Bills, Health, Entertainment, Shopping, Other)
- Idempotency confirmed: second run produced no duplicates (1 user, 8 expenses)
- FK enforcement: `PRAGMA foreign_keys` returns `1` on every `get_db()` connection
- App imports cleanly with no errors

---

## Key Implementation Notes

- `DB_PATH` uses `os.path.dirname(__file__)` — portable regardless of launch directory
- `PRAGMA foreign_keys = ON` lives in `get_db()` so it fires on every connection
- `DEFAULT (datetime('now'))` — parentheses required in SQLite for function defaults
- All SQL values use `?` parameterized placeholders — no f-strings in SQL
