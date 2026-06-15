# Oracle REST API

![Python](https://img.shields.io/badge/python-3.10+-blue?style=flat-square)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-teal?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)
![Part](https://img.shields.io/badge/series-2%20of%205-purple?style=flat-square)

Part 2 of a 5-part series building toward a full URL analytics platform.

This project wraps the Oracle CLI shortener (Part 1) in a FastAPI HTTP service. It shares the same SQLite database at `~/.oracle/db.sqlite3`, so links created via the CLI are immediately visible through the API and vice versa.

Short link codes are random 4-character alphanumeric strings (A-Z, 0-9).

## Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn main:app --reload
```

The API is available at `http://127.0.0.1:8000`. Interactive docs at `http://127.0.0.1:8000/docs`.

---

## Endpoints

### POST /links — Shorten a URL

Creates a new short link. If the URL already exists, returns the existing entry.

```bash
curl -X POST http://localhost:8000/links \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

**Response `201`:**
```json
{ "name": "A3F9", "url": "https://example.com" }
```

---

### GET /links — List all links

Returns all stored short links.

```bash
curl http://localhost:8000/links
```

**Response `200`:**
```json
[
  { "name": "A3F9", "url": "https://example.com", "created_at": "2024-01-01T00:00:00+00:00" }
]
```

---

### GET /links/{code} — Look up a link

Returns the stored URL for a given code.

```bash
curl http://localhost:8000/links/A3F9
```

**Response `200`:**
```json
{ "name": "A3F9", "url": "https://example.com", "created_at": "2024-01-01T00:00:00+00:00" }
```

**Response `404`:**
```json
{ "detail": "No link found for name 'A3F9'" }
```

---

### DELETE /links/{code} — Delete a link

Removes a short link by code.

```bash
curl -X DELETE http://localhost:8000/links/A3F9
```

**Response:** `204 No Content`

**Response `404`:**
```json
{ "detail": "No link found for name 'A3F9'" }
```

---

### GET /{code} — Follow a short link

Redirects to the original URL (HTTP 307). This is the core short-link behavior.

```bash
curl -L http://localhost:8000/A3F9
```

**Response:** `307 Temporary Redirect` to the original URL.

**Response `404`:**
```json
{ "detail": "No link found for name 'A3F9'" }
```

---

## Error Reference

| Status | Meaning |
|--------|---------|
| `404`  | Code not found |
| `409`  | Code collision could not be resolved |
| `422`  | Invalid URL (must start with `http://` or `https://`) |
| `503`  | All codes exhausted — delete some links to free up codes |

All errors return JSON in the format `{ "detail": "message" }`.

---

## Database

Stored at `~/.oracle/db.sqlite3`. Shared with the Part 1 CLI tool — no migration needed.

---

## Series

| Part | Description |
|------|-------------|
| 1    | CLI tool — `oracle` command with SQLite backend |
| **2**    | **REST API — FastAPI wrapper (this project)** |
| 3    | Web Dashboard — Frontend UI for managing and viewing links |
| 4    | Analytics Engine — Track clicks with timestamp, referrer, and device data |
| 5    | Cache & Rate Limiter — Redis caching and rate limiting for scale |
