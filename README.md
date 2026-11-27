# Activity Tracker

A REST API to track time sessions per activity, built with FastAPI and PostgreSQL.
A personal learning project focused on backend development, security and DevSecOps.

## Key rule
Only one open session (no end time) can exist per activity. This is enforced
by the database itself with a partial unique index, not just by application code.

## Tech stack
Python 3.13, FastAPI, SQLAlchemy 2.x, PostgreSQL, Pydantic, uv, pytest, ruff, Docker, Trivy, Semgrep

## Getting started
Prerequisites: Python 3.13, uv, PostgreSQL 16 (or Docker, see below).

1. Install dependencies: `uv sync`
2. Create a dedicated PostgreSQL role without superuser rights, and two databases owned by this role:
   a main one (e.g. `activities_audit`) and a test one (e.g. `activities_test`).
   Use two different databases: the test suite drops all tables when it finishes.

   On Ubuntu, open the PostgreSQL shell as the administrator with `sudo -u postgres psql`, then run:
   If you are not on Ubuntu, run the same commands as a PostgreSQL superuser (for example, on macOS with Homebrew, the `postgres` user or your own administrator role).
   
   ```sql
   CREATE ROLE activity_user WITH LOGIN PASSWORD 'your_password';
   CREATE DATABASE activities_audit OWNER activity_user;
   CREATE DATABASE activities_test OWNER activity_user;
   ```

   Replace `your_password` with a strong password. To avoid storing it in your shell history,
   you can run `CREATE ROLE activity_user WITH LOGIN;` and then `\password activity_user` instead.
   Leave the shell with `\q`.
3. Store the role's password in a file: create `secrets/db_password.txt` containing only the password, on a single line.
   This file is ignored by Git. Never commit it, and never put the password in `.env`.
4. Copy `.env.example` to `.env` and fill in the values:
   - `DATABASE_HOST` (`localhost` for a local PostgreSQL)
   - `DATABASE_USER` (the role created in step 2)
   - `DATABASE_NAME` (the main database)
   - `TEST_DATABASE_NAME` (the test database)
5. Initialize the database tables: `uv run python -m scripts.create_tables`
6. Run the API: `uv run uvicorn app.main:app --reload`, then open `/docs`

## Docker
Docker Compose starts PostgreSQL and the API together. PostgreSQL is not exposed on the host
machine, and the API is published on `http://127.0.0.1:8000` only.

Prerequisites: Docker with Compose, and a `.env` file and `secrets/db_password.txt` as described above.
Compose reads `DATABASE_NAME` and `DATABASE_USER` from your `.env` file, so keep those values filled in.
The PostgreSQL container creates the role and the main database on its first start, using these values
and the password file. You do not need to create them by hand.

1. Build and start the containers: `docker compose up -d --build`
2. Initialize the database tables inside the API container: `docker compose exec api python -m scripts.create_tables`
3. Check that the API responds: `curl http://127.0.0.1:8000/health`

The database password is applied when the data volume is created for the first time. If you change
the password afterwards, the database will refuse the connection. Remove the volume with
`docker compose down -v` (this deletes all data), then start again.

### Running a second copy of the project
Docker Compose names its containers and volumes after the project folder. Two copies in folders with
the same name share the same volume, and the second copy may fail to authenticate.
To run a second copy alongside the first, give it its own project name with the `-p` option, placed
before the subcommand (for example `docker compose -p activity-tracker-clone up -d --build`). Use the
same `-p` value for every later command on that copy, including `down -v`.

## Tests
Tests run against the database named in `TEST_DATABASE_NAME`, on your local PostgreSQL (see Getting started).
They refuse to run if it equals `DATABASE_NAME`, so your main data cannot be dropped by mistake.

Run: `uv run pytest`

## Security

### Secrets
The database password is stored in `secrets/db_password.txt`, which is ignored by Git. It is never
read from `.env` or passed as an environment variable. In Docker, it is mounted as a secret file, so
it does not appear in `docker inspect` or `docker compose config`.

Limitations:
- The password is still stored in plain text on the development machine.
- Docker keeps the password in the data volume after the first start. There is no rotation mechanism yet.
- In Docker, the role from `POSTGRES_USER` is created as a superuser by the official PostgreSQL image.
  The non-superuser recommendation above applies to the local setup.

### Container image (Trivy)

Image `activity-tracker-api` scanned on 2026-11-27 with Trivy 0.76.2 (`trivy image --ignore-unfixed activity-tracker-api`), after a rebuild with `--no-cache --pull`, on a Debian 13.8 base image:

- Base image: 0 fixable vulnerabilities.
- Python dependencies installed in the project virtualenv: 0 findings.
- `uv` binaries: 0 findings.

A full scan without the flag (`trivy image activity-tracker-api`, same day) reports 222 findings in the Debian base image (53 HIGH, 0 CRITICAL). None of them has an upstream fix yet. The Python dependencies still report 0 findings.

The `--ignore-unfixed` flag hides vulnerabilities that have no upstream fix yet, so they are not counted in the first list. The full scan shows them for transparency. These numbers change as the vulnerability database and the Debian packages are updated, so the scan is repeated each time the image is rebuilt.

The image runs as a non-root user, and the Python interpreter's pip has been removed from the final image.

### Static analysis (Semgrep)
Scanned on 2026-11-20 with Semgrep 1.186.0 (`semgrep ci`, Pro engine, free account):
- Code: 0 findings across all 18 git-tracked files (about 145,000 rules, including the community OWASP Top Ten and security-audit packs).
- Dependencies: 0 findings for the 36 packages in `uv.lock`.

Limitation: static analysis does not check business logic. Authorization rules, for example, will need dedicated tests once authentication is added.

## Endpoints
| Method | Path | Success | Errors |
|---|---|---|---|
| GET | /health | 200 | |
| POST | /activities | 201 | 409, 422 |
| GET | /activities | 200 | 422 |
| GET | /activities/{id} | 200 | 404 |
| POST | /activities/{id}/start | 201 | 404, 409 |
| POST | /activities/{id}/stop | 200 | 404 |
| GET | /activities/{id}/entries | 200 | 404, 422 |

- Lists accept `limit` (1-100, default 10) and `offset` (>= 0).
- Activity names (`POST /activities`) must be from **1 to 20 characters** long (leading and trailing whitespace are automatically trimmed).

## Roadmap
- [x] Semgrep (static analysis, dependency check)
- [ ] Authentication and authorization
- [ ] Run Trivy in CI, fail on CRITICAL
- [ ] Run Semgrep in CI, fail on blocking findings