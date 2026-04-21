# QuickNotes

A minimal internal notes tool built with Django. Users can write notes and browse them in reverse-chronological order.

---

## Setup

**Prerequisites:** Python 3.10+

```bash
# 1. Clone / navigate to the project root
cd quicknotes

# 2. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Apply database migrations
python manage.py migrate

# 5. (Optional) Create a superuser to access Django Admin
python manage.py createsuperuser
```

---

## Running the app

```bash
source venv/bin/activate
python manage.py runserver
```

Open **http://127.0.0.1:8000/** in your browser.

- `/`: list of all notes (newest first)
- `/new/`: write a new note
- `/admin/`: Django admin (requires superuser)

---

## Running tests

```bash
source venv/bin/activate
python manage.py test notes
```

Run with verbose output:

```bash
python manage.py test notes --verbosity=2
```

The test suite covers 19 cases across model behaviour, view responses, form validation, and ordering.

---


## Design decisions

### Notes have optional titles
A title is not required — a quick, untitled thought is perfectly valid. When no title is given the list view shows the first 60 characters of the content as a preview label. This keeps data entry frictionless while still making the list scannable.

### Notes are read-only after creation
Edit and delete were intentionally omitted. For a first version of an internal tool, immutability is simpler to reason about, easier to audit, and quick to ship. Adding edit/delete later is low-effort (one view + URL each) and the model structure already supports it.

### Newest first ordering
Notes are ordered by `-created_at` (set in `Note.Meta`). For an append-only tool you almost always want to see what you just wrote — not scroll past weeks of history. The ordering lives on the model so every queryset automatically respects it without callers having to remember to sort.

### Django Admin enabled
Registering `Note` in admin costs three lines and gives a fully functional search, filter, and browse interface for free. Useful for any operator who needs to inspect or moderate content without writing extra views.

### Server-rendered HTML, no JavaScript
The app does everything it needs to with a plain HTML form and Django's template engine. No build step, no bundler, no client-side state. For an internal tool where users are on a trusted network this is the right default; JavaScript can be added incrementally if the UX demands it.

### Single app, SQLite
One Django app (`notes`) keeps things cohesive at this scale. SQLite is the default and is perfectly adequate for an internal tool with low concurrent write volume. Switching to Postgres is a one-line settings change.

### Inline CSS in `base.html`
Styles are embedded in the base template rather than served as a static file. This avoids configuring `STATIC_ROOT` and `collectstatic` for development, keeps the project self-contained, and is easy to extract into a separate stylesheet when the project grows.

---

## How you might extend this app

- **Edit / delete notes:** Right now notes are immutable by design, which keeps the first version simple and auditable. Once the tool sees regular use, the ability to correct mistakes or remove stale notes becomes a real need.
- **User accounts:** A shared note list is fine for a single person, but as soon as more than one person uses the tool you need to know who wrote what and limit each user to their own notes.
- **Full-text search:** As the note count grows, scrolling a reverse-chronological list stops being practical. A search bar lets you surface any note instantly by keyword.
- **Tags / categories:** Search finds notes that contain a word, but tags let you group notes by topic or project so you can browse a whole theme at once — useful when a single note may not have consistent wording.
- **Markdown rendering:** Plain text is fine for short thoughts, but longer notes with structure (lists, headings, code) are much easier to read when formatted. Markdown is the lightest way to get that without a rich-text editor.
- **Pagination:** Loading every note on a single page is fine early on, but it gets slow and overwhelming as the list grows. Pagination keeps page load times predictable regardless of how many notes exist.
- **REST API:** A web UI is enough for human users, but a REST API lets other tools and scripts create or read notes programmatically — useful for integrations or building a mobile client later.
- **Production deployment:** The development defaults (debug mode, SQLite, hardcoded secret key) are intentionally insecure and not suitable for a live environment. Hardening the configuration is the necessary step before sharing the tool with anyone outside a local machine.
