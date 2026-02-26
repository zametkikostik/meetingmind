# MeetingMind AI API Documentation

## Base URL
```
Development: http://localhost:8000
Production: https://api.meetingmind.ai
```

## Authentication

Most endpoints require authentication using JWT Bearer tokens.

### Login
```http
POST /api/v1/auth/login
Content-Type: application/x-www-form-urlencoded

username=user@example.com
password=yourpassword
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

### Register
```http
POST /api/v1/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "yourpassword",
  "full_name": "John Doe"
}
```

### Refresh Token
```http
POST /api/v1/auth/refresh
Content-Type: application/json

{
  "refresh_token": "eyJhbGciOiJIUzI1NiIs..."
}
```

### Get Current User
```http
GET /api/v1/auth/me
Authorization: Bearer <access_token>
```

---

## Meetings

### List Meetings
```http
GET /api/v1/meetings?skip=0&limit=20&status=completed
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `skip` (int): Number of items to skip (pagination)
- `limit` (int): Number of items to return (max 100)
- `status` (string): Filter by status (scheduled, in_progress, completed, failed)

**Response:**
```json
[
  {
    "id": "uuid",
    "title": "Team Standup",
    "status": "completed",
    "scheduled_at": "2024-01-15T10:00:00Z",
    "duration_seconds": 1800,
    "summary": "Team discussed...",
    "key_topics": ["sprint", "blockers"],
    "created_at": "2024-01-15T09:00:00Z"
  }
]
```

### Create Meeting
```http
POST /api/v1/meetings
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "title": "New Meeting",
  "description": "Optional description",
  "scheduled_at": "2024-01-20T14:00:00Z",
  "platform": "zoom"
}
```

### Get Meeting
```http
GET /api/v1/meetings/{meeting_id}
Authorization: Bearer <access_token>
```

### Update Meeting
```http
PUT /api/v1/meetings/{meeting_id}
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "title": "Updated Title",
  "status": "completed"
}
```

### Delete Meeting
```http
DELETE /api/v1/meetings/{meeting_id}
Authorization: Bearer <access_token>
```

---

## Transcripts

### Get Meeting Transcripts
```http
GET /api/v1/meetings/{meeting_id}/transcripts
Authorization: Bearer <access_token>
```

**Response:**
```json
[
  {
    "id": "uuid",
    "speaker_name": "John Doe",
    "text": "Hello everyone...",
    "start_time": 0.5,
    "end_time": 3.2,
    "confidence": 0.95,
    "is_key_moment": false
  }
]
```

---

## Action Items

### Create Action Item
```http
POST /api/v1/meetings/{meeting_id}/action-items
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "task": "Review PR #123",
  "assignee_name": "John Doe",
  "assignee_email": "john@example.com",
  "priority": "high",
  "due_date": "2024-01-25"
}
```

### Update Action Item
```http
PUT /api/v1/meetings/action-items/{action_id}
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "status": "completed"
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid input data"
}
```

### 401 Unauthorized
```json
{
  "detail": "Could not validate credentials"
}
```

### 403 Forbidden
```json
{
  "detail": "User does not have permission"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

---

## Rate Limits

- Free tier: 100 requests/minute
- Pro tier: 500 requests/minute
- Enterprise: Unlimited

---

## WebSocket (Real-time Transcription)

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/meetings/{meeting_id}/transcribe');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Transcript segment:', data);
};

ws.onerror = (error) => {
  console.error('WebSocket error:', error);
};
```
