# Wardrobe AI prototype

A backend prototype for a personal wardrobe, saved outfits, outfit
recommendations, clothing imported from image links, and generated outfit photos.

## Current state

Stages 1.1 through 1.3 are complete: clean project structure, documented record
relationships, and a minimal Flask application with one tested health endpoint.
Database persistence and media-directory creation come in Stage 1.4, which is
next, pending user review.

The agreed foundation is Python 3.11+, Flask, SQLite through Python's built-in
`sqlite3` module, and local image files. AI and image-processing libraries will be
selected with the user when their stages begin.

## Structure

- `src/wardrobe_ai/__init__.py`: application creation, configuration, and health route.
- `tests/test_app.py`: health API test with a temporary data-directory setting.
- `docs/implementation-plan.md`: stages, sub-stages, and completion checks.
- `docs/architecture.md`: agreed architecture and technology decisions.
- `AGENTS.md`: instructions for agents working on the project.

## Development setup

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
```

The existing `.venv` may still contain legacy packages. The new application only
requires the dependencies declared in `pyproject.toml`.

During verification on this Mac, Python skipped the editable install's `.pth`
file because it had the macOS hidden flag. Clearing the flag restored the normal
package import. If the same issue recurs after reinstalling in this environment:

```bash
chflags nohidden .venv/lib/python3.12/site-packages/_editable_impl_wardrobe_ai.pth
```

## Run locally

From the project directory, with the virtual environment activated:

```bash
flask --app wardrobe_ai run --debug
```

Check the endpoint:

```bash
curl http://127.0.0.1:5000/health
```

Expected response: `{"status":"ok"}` with HTTP 200. The root URL `/` has no route.

## Configuration

`WARDROBE_DATA_DIR` sets the future data-directory location. It defaults to
`./data`, resolved relative to the directory from which you start the application.
The value is read when the app is created and stored as `app.config["DATA_DIR"]`.
Stage 1.3 does not create the directory or any database files.

To override it, set the environment variable before starting:

```bash
export WARDROBE_DATA_DIR=./my-data
flask --app wardrobe_ai run --debug
```

`.env.example` documents the setting. It is not loaded automatically; no dotenv
dependency is included.

## Verification

```bash
pytest
ruff check .
ruff format --check .
```

The API test checks the JSON response, environment configuration, and that the
health request creates no data directory.

## Legacy recovery

`work/legacy-scaffold-2026-10-04.tar.gz` contains the old source, tests,
documentation, and project configuration. Each archived file was compared
byte-for-byte with its original before the reset. It excludes virtual environments,
caches, and runtime data.

To inspect or recover it in a separate temporary directory:

```bash
tar -tzf work/legacy-scaffold-2026-10-04.tar.gz
recovery_dir=$(mktemp -d)
tar -xzf work/legacy-scaffold-2026-10-04.tar.gz -C "$recovery_dir"
```

The archive is for recovery, not part of the new application's implementation.
