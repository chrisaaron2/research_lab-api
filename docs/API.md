# API Reference

The Research Lab Manager backend serves JSON over HTTP. Locally it runs at `http://localhost:8000`, with interactive OpenAPI docs at `/docs`.

## Conventions

`GET` routes are public. `POST`, `PUT`, and `DELETE` routes require an admin token. Get one from `POST /auth/login` and send it on every write request:

```text
Authorization: Bearer <access_token>
```

Status codes used across the API:

- `200 OK` on a successful read or update.
- `201 Created` when a `POST` creates a new resource (for example, a grant or a publication). A `POST` that modifies an existing resource, such as adding a publication author, returns `200`.
- `400 Bad Request` for a business-rule violation surfaced from the data layer: referencing a project, member, or device that does not exist, adding an author who is already on a publication, or deleting a record that other records still depend on.
- `401 Unauthorized` for any auth failure: a missing, invalid, or expired token, or a valid token that lacks the admin role.
- `404 Not Found` when the requested resource does not exist.
- `422 Unprocessable Entity` when a request body fails schema validation, for example a missing required field or a student created without an `sid`.

## Health

| Method | Path | Auth |
| --- | --- | --- |
| GET | `/health` | Public |

```json
{
  "status": "ok",
  "service": "research-lab-manager"
}
```

## Auth

| Method | Path | Auth |
| --- | --- | --- |
| POST | `/auth/login` | Public |

Request:

```json
{
  "username": "admin",
  "password": "your-password"
}
```

Response:

```json
{
  "access_token": "<jwt>",
  "token_type": "bearer"
}
```

A wrong username or password returns `401`.

## Members

| Method | Path | Auth |
| --- | --- | --- |
| GET | `/members` | Public |
| GET | `/members?type=student` | Public |
| GET | `/members/{mid}` | Public |
| GET | `/grants/{gid}/members` | Public |
| GET | `/projects/{pid}/mentorships` | Public |
| POST | `/members` | Admin |
| PUT | `/members/{mid}` | Admin |
| DELETE | `/members/{mid}` | Admin |

The `type` filter accepts `student`, `faculty`, or `collaborator`. Each member has a type, and the create request must include the fields required by that subtype: `sid` for a student, `department` for faculty, and `affiliation` for a collaborator. Omitting them returns `422`.

Create a student:

```json
{
  "name": "Maria Gonzalez",
  "type": "student",
  "sid": "S7042",
  "level": "MS",
  "major": "Data Science"
}
```

Create a faculty member:

```json
{
  "name": "Dr. Alan Whitfield",
  "type": "faculty",
  "department": "Computer Science"
}
```

Create a collaborator:

```json
{
  "name": "Priya Raman",
  "type": "collaborator",
  "affiliation": "Bell Labs"
}
```

Update (any subset of fields):

```json
{
  "mentor": 3,
  "major": "Computer Science"
}
```

`GET /members/{mid}` response:

```json
{
  "mid": 7,
  "name": "Maria Gonzalez",
  "join_date": "2024-09-01",
  "type": "student",
  "mentor": 3,
  "m_sdate": "2024-09-01",
  "m_edate": null,
  "sid": "S7042",
  "level": "MS",
  "major": "Data Science",
  "affiliation": null,
  "cv": null,
  "department": null
}
```

`GET /members` returns full member records (the same shape as the detail response above). `GET /grants/{gid}/members` returns a lighter summary per member (`mid`, `name`, `type`). `GET /projects/{pid}/mentorships` returns mentor and mentee pairs:

```json
[
  {
    "mentor_mid": 3,
    "mentor_name": "Dr. Alan Whitfield",
    "mentee_mid": 7,
    "mentee_name": "Maria Gonzalez"
  }
]
```

## Projects

| Method | Path | Auth |
| --- | --- | --- |
| GET | `/projects` | Public |
| GET | `/projects?status=active` | Public |
| GET | `/projects/{pid}` | Public |
| GET | `/projects/{pid}/status` | Public |
| POST | `/projects` | Admin |
| PUT | `/projects/{pid}` | Admin |
| DELETE | `/projects/{pid}` | Admin |

The `status` filter accepts `active`, `completed`, or `ongoing`.

Create:

```json
{
  "title": "Edge Inference",
  "s_date": "2025-01-15",
  "e_date": "2026-12-31",
  "e_duration": "24 months",
  "leader": 7
}
```

Update:

```json
{
  "title": "Edge Inference (Phase 2)",
  "leader": 8
}
```

`GET /projects/{pid}` returns the project with derived counts and total funding:

```json
{
  "pid": 1,
  "title": "Edge Inference",
  "s_date": "2025-01-15",
  "e_date": "2026-12-31",
  "e_duration": "24 months",
  "leader": 7,
  "leader_name": "Dr. Alan Whitfield",
  "member_count": 5,
  "grant_count": 2,
  "total_funding": "275000"
}
```

`GET /projects/{pid}/status` returns a computed status and days remaining:

```json
{
  "pid": 1,
  "title": "Edge Inference",
  "s_date": "2025-01-15",
  "e_date": "2026-12-31",
  "status": "active",
  "days_remaining": 191
}
```

## Grants

| Method | Path | Auth |
| --- | --- | --- |
| GET | `/grants` | Public |
| GET | `/grants?pid=1` | Public |
| GET | `/grants?agency=NSF` | Public |
| GET | `/grants/{gid}` | Public |
| POST | `/grants` | Admin |
| PUT | `/grants/{gid}` | Admin |
| DELETE | `/grants/{gid}` | Admin |

Create (`agency` and `pid` are required; a `pid` that does not exist returns `400`):

```json
{
  "p_duration": "12 months",
  "agency": "NSF",
  "budget": "125000",
  "start_date": "2026-04-27",
  "pid": 1
}
```

Update (any subset of fields):

```json
{
  "budget": "150000"
}
```

`GET /grants/{gid}` response:

```json
{
  "gid": 1,
  "p_duration": "12 months",
  "agency": "NSF",
  "budget": "125000",
  "start_date": "2026-04-27",
  "pid": 1,
  "project_title": "Edge Inference"
}
```

## Equipment

| Method | Path | Auth |
| --- | --- | --- |
| GET | `/equipment` | Public |
| GET | `/equipment?e_type=GPU Server` | Public |
| GET | `/equipment?status=active` | Public |
| GET | `/equipment/{eid}` | Public |
| GET | `/equipment/{eid}/active-users` | Public |
| POST | `/equipment` | Admin |
| PUT | `/equipment/{eid}` | Admin |
| DELETE | `/equipment/{eid}` | Admin |

Create:

```json
{
  "e_type": "GPU Server",
  "e_name": "Compute Node A",
  "manual": "https://example.com/manuals/node-a"
}
```

Update:

```json
{
  "manual": "https://example.com/manuals/node-a-v2"
}
```

`GET /equipment/{eid}` returns device counts and a usage count alongside the record:

```json
{
  "eid": 1,
  "e_type": "GPU Server",
  "e_name": "Compute Node A",
  "manual": "https://example.com/manuals/node-a",
  "device_count": 4,
  "active_device_count": 3,
  "usage_count": 12
}
```

`GET /equipment/{eid}/active-users` lists members currently using the equipment, each with their related projects:

```json
[
  {
    "mid": 7,
    "member_name": "Maria Gonzalez",
    "did": 3,
    "purpose": "Model training",
    "active_since": "2026-02-10",
    "projects": [
      { "pid": 2, "title": "Edge Inference", "role": "Researcher" }
    ]
  }
]
```

## Devices

| Method | Path | Auth |
| --- | --- | --- |
| GET | `/devices` | Public |
| GET | `/devices?eid=1` | Public |
| GET | `/devices?status=active` | Public |
| GET | `/devices/{did}` | Public |
| POST | `/devices` | Admin |
| PUT | `/devices/{did}` | Admin |
| DELETE | `/devices/{did}` | Admin |

A device belongs to a piece of equipment through `eid`.

Create:

```json
{
  "eid": 1,
  "status": "active",
  "p_date": "2025-06-01"
}
```

Update:

```json
{
  "status": "maintenance"
}
```

`GET /devices/{did}` response:

```json
{
  "did": 3,
  "eid": 1,
  "equipment_name": "Compute Node A",
  "equipment_type": "GPU Server",
  "status": "active",
  "p_date": "2025-06-01",
  "active_user_count": 2
}
```

## Uses

A usage record links a member, a device, and a piece of equipment, keyed by all three (`mid`, `did`, `eid`).

| Method | Path | Auth |
| --- | --- | --- |
| GET | `/uses` | Public |
| GET | `/uses?active_only=true` | Public |
| GET | `/uses?mid=1` | Public |
| GET | `/uses?did=1` | Public |
| GET | `/uses?eid=1` | Public |
| POST | `/uses` | Admin |
| PUT | `/uses/{mid}/{did}/{eid}` | Admin |
| DELETE | `/uses/{mid}/{did}/{eid}` | Admin |

Create:

```json
{
  "mid": 1,
  "did": 1,
  "eid": 1,
  "s_date": "2026-02-10",
  "purpose": "Model training"
}
```

Update (the key fields stay in the path; only the record's own fields change):

```json
{
  "e_date": "2026-03-15",
  "purpose": "Completed model training"
}
```

`GET /uses` response:

```json
[
  {
    "mid": 1,
    "member_name": "Maria Gonzalez",
    "did": 1,
    "eid": 1,
    "equipment_name": "Compute Node A",
    "s_date": "2026-02-10",
    "e_date": null,
    "purpose": "Model training"
  }
]
```

## Publications

| Method | Path | Auth |
| --- | --- | --- |
| GET | `/publications` | Public |
| GET | `/publications?year=2024` | Public |
| GET | `/publications?venue=VLDB` | Public |
| GET | `/publications?author_mid=1` | Public |
| GET | `/publications/{pubid}` | Public |
| GET | `/publications/{pubid}/authors` | Public |
| POST | `/publications` | Admin |
| PUT | `/publications/{pubid}` | Admin |
| DELETE | `/publications/{pubid}` | Admin |
| POST | `/publications/{pubid}/authors` | Admin |
| DELETE | `/publications/{pubid}/authors/{mid}` | Admin |

Create (returns `201`):

```json
{
  "title": "Reliable Research Data Systems",
  "venue": "VLDB",
  "date": "2026-04-27",
  "doi": "10.1234/rds"
}
```

Update (any subset of fields):

```json
{
  "venue": "SIGMOD"
}
```

Add an author (returns the updated publication; an unknown `mid` returns `404`, an author already on the publication returns `400`):

```json
{
  "mid": 1
}
```

`GET /publications` returns list items with an author count:

```json
[
  {
    "pubid": 1,
    "title": "Reliable Research Data Systems",
    "venue": "VLDB",
    "date": "2026-04-27",
    "doi": "10.1234/rds",
    "author_count": 3
  }
]
```

`GET /publications/{pubid}` includes the full author list:

```json
{
  "pubid": 1,
  "title": "Reliable Research Data Systems",
  "venue": "VLDB",
  "date": "2026-04-27",
  "doi": "10.1234/rds",
  "authors": [
    { "mid": 1, "name": "Maria Gonzalez", "type": "student" }
  ]
}
```

## Reports

All report routes are public reads.

| Method | Path | Auth |
| --- | --- | --- |
| GET | `/reports/top-funded-projects` | Public |
| GET | `/reports/top-mentors-by-publications` | Public |
| GET | `/reports/student-publications-by-major-year` | Public |
| GET | `/reports/projects-ended-before?date=YYYY-MM-DD` | Public |
| GET | `/reports/top-publication-years` | Public |

`projects-ended-before` requires a `date` query parameter in `YYYY-MM-DD` form. It is parsed as a date type, so a missing or malformed value returns `422`.

`GET /reports/top-funded-projects`:

```json
[
  { "pid": 1, "title": "Edge Inference", "total_funding": "275000", "grant_count": 2 }
]
```

`GET /reports/top-mentors-by-publications`:

```json
[
  { "mentor_mid": 3, "mentor_name": "Dr. Alan Whitfield", "mentee_pub_count": 8 }
]
```

`GET /reports/student-publications-by-major-year`:

```json
[
  { "major": "Data Science", "year": 2024, "pub_count": 4 }
]
```

`GET /reports/projects-ended-before?date=2024-01-01`:

```json
[
  { "pid": 5, "title": "Legacy Sensor Net", "e_date": "2023-08-01", "grant_count": 1 }
]
```

`GET /reports/top-publication-years`:

```json
[
  { "year": 2024, "pub_count": 12 }
]
```

## Admin

| Method | Path | Auth |
| --- | --- | --- |
| POST | `/admin/seed` | Admin |

Loads the deterministic seed dataset. On a fresh database:

```json
{
  "message": "seed data inserted",
  "inserted": true
}
```

If the database is already populated, it does not reseed and returns:

```json
{
  "message": "already seeded",
  "inserted": false
}
```
