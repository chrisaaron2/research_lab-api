# API Reference

All public `GET` routes can be called without authentication. Admin write routes
require:

```text
Authorization: Bearer <access_token>
```

## Health

Public:

- `GET /health`

Response:

```json
{
  "status": "ok",
  "service": "research-lab-manager"
}
```

## Auth

Public:

- `POST /auth/login`

Request:

```json
{
  "username": "admin",
  "password": "admin123"
}
```

Response:

```json
{
  "access_token": "<jwt>",
  "token_type": "bearer"
}
```

## Admin

Requires Bearer token:

- `POST /admin/seed`

Response:

```json
{
  "message": "seed data inserted",
  "inserted": true
}
```

## Grants

Public routes:

- `GET /grants`
- `GET /grants?pid=1`
- `GET /grants?agency=NSF`
- `GET /grants/{gid}`

Bearer token required:

- `POST /grants`
- `PUT /grants/{gid}`
- `DELETE /grants/{gid}`

Sample create body:

```json
{
  "p_duration": "12 months",
  "agency": "NSF",
  "budget": "125000",
  "start_date": "2026-04-27",
  "pid": 1
}
```

## Members

Public:

- `GET /members`
- `GET /members?type=student`
- `GET /members/{mid}`
- `GET /grants/{gid}/members`
- `GET /projects/{pid}/mentorships`

Requires Bearer token:

- `POST /members`
- `PUT /members/{mid}`
- `DELETE /members/{mid}`

Create student example:

```json
{
  "name": "Route Test Student",
  "type": "student",
  "sid": "S7777",
  "level": "MS",
  "major": "Data Science"
}
```

Create faculty example:

```json
{
  "name": "Dr. New Faculty",
  "type": "faculty",
  "department": "Computer Science"
}
```

Update example:

```json
{
  "mentor": 7,
  "major": "Computer Science"
}
```

## Projects

Public:

- `GET /projects`
- `GET /projects?status=active`
- `GET /projects?status=completed`
- `GET /projects?status=ongoing`
- `GET /projects/{pid}`
- `GET /projects/{pid}/status`

Requires Bearer token:

- `POST /projects`
- `PUT /projects/{pid}`
- `DELETE /projects/{pid}`

Create example:

```json
{
  "title": "New Research Project",
  "s_date": "2026-04-27",
  "e_date": "2028-04-27",
  "e_duration": "24 months",
  "leader": 7
}
```

Update example:

```json
{
  "title": "Updated Research Project",
  "leader": 8
}
```

## Equipment

Public:

- `GET /equipment`
- `GET /equipment?e_type=GPU Server`
- `GET /equipment?status=active`
- `GET /equipment/{eid}`
- `GET /equipment/{eid}/active-users`

Requires Bearer token:

- `POST /equipment`
- `PUT /equipment/{eid}`
- `DELETE /equipment/{eid}`

Create example:

```json
{
  "e_type": "GPU Server",
  "e_name": "New Compute Node",
  "manual": "https://example.com/manuals/new-node"
}
```

Update example:

```json
{
  "manual": "https://example.com/manuals/updated-node"
}
```

## Devices

Public:

- `GET /devices`
- `GET /devices?eid=1`
- `GET /devices?status=active`
- `GET /devices/{did}`

Requires Bearer token:

- `POST /devices`
- `PUT /devices/{did}`
- `DELETE /devices/{did}`

Create example:

```json
{
  "eid": 1,
  "status": "active",
  "p_date": "2026-04-27"
}
```

Update example:

```json
{
  "status": "maintenance"
}
```

## Uses

Public:

- `GET /uses`
- `GET /uses?active_only=true`
- `GET /uses?mid=1`
- `GET /uses?did=1`
- `GET /uses?eid=1`

Requires Bearer token:

- `POST /uses`
- `PUT /uses/{mid}/{did}/{eid}`
- `DELETE /uses/{mid}/{did}/{eid}`

Create example:

```json
{
  "mid": 1,
  "did": 1,
  "eid": 1,
  "s_date": "2026-04-27",
  "purpose": "Model training"
}
```

Update example:

```json
{
  "e_date": "2026-05-27",
  "purpose": "Completed model training"
}
```

## Reports

Public:

- `GET /reports/top-funded-projects`
- `GET /reports/top-mentors-by-publications`
- `GET /reports/student-publications-by-major-year`
- `GET /reports/projects-ended-before?date=YYYY-MM-DD`
- `GET /reports/top-publication-years`

Report endpoints are read-only and do not require authentication.
