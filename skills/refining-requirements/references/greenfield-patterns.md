# Greenfield Project Patterns

Templates and guidance for new projects built from scratch.

## Contents
- [Detecting Greenfield vs. Feature](#detecting-greenfield-vs-feature)
- [Greenfield Workflow](#greenfield-workflow)
- [Greenfield Template](#greenfield-template)
- [Greenfield Clarifying Questions](#greenfield-clarifying-questions)
- [Quick Scaffolding Commands by Stack](#quick-scaffolding-commands-by-stack)
- [Full Project Scaffolding](#full-project-scaffolding)

## Detecting Greenfield vs. Feature

| Indicator | Type |
|-----------|------|
| "Build a new service/app" | Greenfield |
| "Create from scratch" | Greenfield |
| "New microservice for..." | Greenfield |
| "Add feature to existing..." | Feature (use standard templates) |
| References existing files | Feature |
| No codebase context | Likely Greenfield |

---

## Greenfield Workflow

### Step 1: Gather Requirements
Ask if not clear:
- What does this service do?
- Expected tech stack?
- Deployment target?
- Scale requirements?

### Step 2: Auto-detect or Confirm Stack
```bash
# If in existing repo, detect from files
ls package.json go.mod requirements.txt pom.xml 2>/dev/null
```

### Step 3: Generate Full Specification
Use template below

### Step 4: Save to agent-workflow/requirements/
```bash
mkdir -p agent-workflow/requirements
# Save as: YYYYMMDD-new-[project-name].md
```

### Step 5: Offer Full Project Scaffolding
```
Would you like me to scaffold the entire project structure?
This will create:
- Directory structure
- Configuration files
- Docker setup
- CI/CD templates
- Initial README
```

---

## Greenfield Template

```markdown
---
title: [Project Name]
created: [ISO timestamp]
status: draft
stack: [stack]
type: greenfield
---

# [Project Name]

## Overview
Brief description of what this project/service does.

## Scope
### In Scope
- Core functionality
- Initial endpoints/features
### Out of Scope
- Future enhancements (Phase 2+)
- Nice-to-haves deferred

### Success Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Technical Decisions

### Stack Selection
| Component | Choice | Rationale |
|-----------|--------|-----------|
| Language | Go / Python / Node.js | Why chosen |
| Framework | Gin / FastAPI / Express | Why chosen |
| Database | PostgreSQL / MongoDB | Why chosen |
| Cache | Redis / None | Why chosen |
| Message Queue | NSQ / RabbitMQ / None | Why chosen |

### Architecture Pattern
- [ ] Monolith
- [ ] Microservice
- [ ] Serverless
- [ ] Event-driven

Rationale: ...

## Project Structure
```
project-name/
├── cmd/                    # Entry points (Go) or src/ (Node)
├── internal/               # Private application code
│   ├── handler/            # HTTP handlers / controllers
│   ├── service/            # Business logic
│   ├── repository/         # Data access
│   └── model/              # Domain models
├── pkg/                    # Public libraries (if any)
├── migrations/             # Database migrations
├── config/                 # Configuration files
├── scripts/                # Build/deploy scripts
├── docker/                 # Dockerfiles
├── docs/                   # Documentation
│   └── api/                # API documentation
├── .env.example            # Environment template
├── docker-compose.yml      # Local development
├── Makefile                # Common commands
└── README.md               # Project documentation
```

## Data Model (Initial Schema)

### [Entity 1]
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK | Primary identifier |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW | Creation time |
| updated_at | TIMESTAMP | NOT NULL | Last update |

### Relationships
- [Entity 1] hasMany [Entity 2]

### Indexes
| Table | Columns | Type | Rationale |
|-------|---------|------|-----------|
| entity1 | email | UNIQUE | Lookup by email |
| entity1 | created_at | BTREE | Time-based queries |

## API Design

### Base URL
- Development: `http://localhost:8080/api/v1`
- Staging: `https://api-staging.example.com/v1`
- Production: `https://api.example.com/v1`

### Authentication
- Method: JWT / API Key / OAuth2
- Header: `Authorization: Bearer {token}`

### Endpoints
| Method | Path | Description |
|--------|------|-------------|
| GET | /health | Health check |
| POST | /resource | Create resource |
| GET | /resource/:id | Get resource |

### Error Response Format
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable message",
    "details": {}
  }
}
```

### Error Codes
| Code | HTTP Status | Description |
|------|-------------|-------------|
| VALIDATION_ERROR | 400 | Invalid input |
| UNAUTHORIZED | 401 | Missing/invalid auth |
| NOT_FOUND | 404 | Resource not found |
| INTERNAL_ERROR | 500 | Server error |

## Configuration

### Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| PORT | No | 8080 | Server port |
| DATABASE_URL | Yes | - | PostgreSQL connection |
| REDIS_URL | No | - | Redis connection |
| LOG_LEVEL | No | info | Logging level |
| ENV | No | development | Environment name |

### .env.example
```bash
PORT=8080
DATABASE_URL=postgres://user:pass@localhost:5432/dbname?sslmode=disable
REDIS_URL=redis://localhost:6379
LOG_LEVEL=debug
ENV=development
```

## Infrastructure

### Docker
```dockerfile
# Dockerfile
FROM golang:1.21-alpine AS builder
WORKDIR /app
COPY . .
RUN go build -o main ./cmd/api

FROM alpine:latest
WORKDIR /app
COPY --from=builder /app/main .
EXPOSE 8080
CMD ["./main"]
```

### Docker Compose (Local Dev)
```yaml
version: '3.8'
services:
  api:
    build: .
    ports:
      - "8080:8080"
    environment:
      - DATABASE_URL=postgres://user:pass@db:5432/dbname
    depends_on:
      - db
  db:
    image: postgres:15
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: dbname
    volumes:
      - postgres_data:/var/lib/postgresql/data
volumes:
  postgres_data:
```

### Makefile
```makefile
.PHONY: run build test migrate

run:
	go run ./cmd/api

build:
	go build -o bin/api ./cmd/api

test:
	go test ./...

migrate-up:
	migrate -path migrations -database "$(DATABASE_URL)" up

migrate-down:
	migrate -path migrations -database "$(DATABASE_URL)" down 1
```

## CI/CD Pipeline

### GitHub Actions / GitLab CI
```yaml
stages:
  - test
  - build
  - deploy

test:
  script:
    - make test

build:
  script:
    - docker build -t app:$CI_COMMIT_SHA .
  only:
    - main

deploy-staging:
  script:
    - deploy to staging
  only:
    - main
```

## Observability

### Health Check
```
GET /health
Response: { "status": "ok", "version": "1.0.0" }
```

### Logging
- Format: JSON structured logs
- Fields: timestamp, level, message, request_id, user_id

### Metrics (if applicable)
| Metric | Type | Description |
|--------|------|-------------|
| http_requests_total | Counter | Total requests |
| http_request_duration | Histogram | Request latency |

## Security Checklist (Initial)
- [ ] HTTPS only in production
- [ ] CORS configured
- [ ] Rate limiting
- [ ] Input validation
- [ ] SQL injection prevention (parameterized queries)
- [ ] Secrets in environment variables, not code
- [ ] Dependency vulnerability scanning

## Documentation

### README.md Structure
1. Project description
2. Prerequisites
3. Getting started (local setup)
4. Configuration
5. API documentation link
6. Development workflow
7. Deployment
8. Contributing

### API Documentation
- Tool: Swagger / OpenAPI 3.0
- Location: `/docs/api/openapi.yaml`
- UI: Available at `/swagger` in development

## Execution Checklist

### Phase 1: Setup
1. [ ] Initialize repository
2. [ ] Create project structure
3. [ ] Setup development environment (docker-compose)
4. [ ] Configure linting/formatting
5. [ ] Setup CI pipeline (test stage)

### Phase 2: Core
1. [ ] Implement database models
2. [ ] Create initial migration
3. [ ] Implement core endpoints
4. [ ] Add authentication
5. [ ] Write unit tests

### Phase 3: Production Readiness
1. [ ] Add health check endpoint
2. [ ] Configure logging
3. [ ] Add Dockerfile
4. [ ] Setup staging deployment
5. [ ] Write API documentation
6. [ ] Security review
```

---

## Greenfield Clarifying Questions

Add these for new projects:

| Question | Why It Matters |
|----------|----------------|
| Is this a new project or adding to existing? | Determines template type |
| Preferred tech stack, or need recommendation? | Guides structure and examples |
| Deployment target? (K8s, ECS, serverless, VM) | Affects infra templates |
| Expected scale? (requests/sec, data volume) | Influences architecture |
| Team size and experience? | Adjusts complexity |
| Timeline? (MVP vs production-ready) | Scopes deliverables |
| Any existing services to integrate with? | Identifies dependencies |

---

## Quick Scaffolding Commands by Stack

### Go
```bash
mkdir -p cmd/api internal/{handler,service,repository,model} migrations config
go mod init github.com/org/project
```

### Python (FastAPI)
```bash
mkdir -p app/{api,models,schemas,services} migrations tests
python -m venv venv && source venv/bin/activate
pip install fastapi uvicorn sqlalchemy alembic
```

### Node.js (Express)
```bash
mkdir -p src/{controllers,models,routes,services,middleware} migrations
npm init -y
npm install express sequelize pg dotenv
```

### Java (Spring Boot)
```bash
# Use Spring Initializr or:
mkdir -p src/main/java/com/example/{controller,model,repository,service}
mkdir -p src/main/resources/db/migration
```

---

## Full Project Scaffolding

When user requests full scaffolding for greenfield project:

### Step 1: Create Directory Structure
```bash
# Example for Go project
mkdir -p [project-name]/{cmd/api,internal/{handler,service,repository,model},migrations,config,scripts,docs/api}
cd [project-name]
```

### Step 2: Initialize Project Files
```bash
# Go
go mod init github.com/[org]/[project-name]

# Node.js
npm init -y

# Python
python -m venv venv
pip install fastapi uvicorn sqlalchemy alembic
pip freeze > requirements.txt
```

### Step 3: Create Core Files

**Create these files with TODO placeholders:**
- Main entry point
- Configuration loader
- Database connection
- Health check endpoint
- .env.example
- .gitignore
- README.md
- Dockerfile
- docker-compose.yml
- Makefile

### Step 4: Report Created Files
```markdown
## ✅ Project Scaffolded

Created structure:
```
[project-name]/
├── cmd/api/main.go
├── internal/
│   ├── handler/
│   ├── service/
│   ├── repository/
│   └── model/
├── migrations/
├── config/config.go
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── Makefile
└── README.md
```

## Next Steps
1. [ ] Copy `.env.example` to `.env` and fill values
2. [ ] Run `docker-compose up -d` for local database
3. [ ] Run `make run` to start development server
4. [ ] Begin implementing features from PRD

## PRD Location
`agent-workflow/requirements/[filename].md`
```
