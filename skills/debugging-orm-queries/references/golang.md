# Go ORMs Reference

## Table of Contents

1. [GORM](#gorm)
2. [sqlc](#sqlc)
3. [sqlx](#sqlx)
4. [ent](#ent)

---

## GORM

### Enable Logging

```go
import (
    "gorm.io/gorm"
    "gorm.io/gorm/logger"
    "log"
    "os"
    "time"
)

// Global logging configuration
newLogger := logger.New(
    log.New(os.Stdout, "\r\n", log.LstdFlags),
    logger.Config{
        SlowThreshold:             200 * time.Millisecond,
        LogLevel:                  logger.Info,  // Silent, Error, Warn, Info
        IgnoreRecordNotFoundError: true,
        Colorful:                  true,
    },
)

db, err := gorm.Open(postgres.Open(dsn), &gorm.Config{
    Logger: newLogger,
})

// Per-query debugging
db.Debug().Where("name = ?", "john").First(&user)

// Session-level debugging
session := db.Session(&gorm.Session{Logger: newLogger})
```

### ORM to SQL Conversion

```go
// GORM Query
var users []User
db.Select("id", "name", "email").
    Joins("LEFT JOIN posts ON posts.user_id = users.id").
    Where("users.status = ?", "active").
    Where("users.age >= ?", 18).
    Order("users.created_at DESC").
    Limit(10).
    Offset(20).
    Find(&users)

// Generated SQL
SELECT "users"."id", "users"."name", "users"."email"
FROM "users"
LEFT JOIN posts ON posts.user_id = users.id
WHERE users.status = 'active' AND users.age >= 18
ORDER BY users.created_at DESC
LIMIT 10 OFFSET 20;
```

### SQL to ORM Conversion

```sql
-- Raw SQL
SELECT u.id, u.name, COUNT(p.id) as post_count
FROM users u
LEFT JOIN posts p ON u.id = p.user_id
WHERE u.created_at > '2024-01-01'
GROUP BY u.id, u.name
HAVING COUNT(p.id) > 5;
```

```go
// GORM equivalent
type Result struct {
    ID        uint
    Name      string
    PostCount int64
}

var results []Result
db.Model(&User{}).
    Select("users.id, users.name, COUNT(posts.id) as post_count").
    Joins("LEFT JOIN posts ON posts.user_id = users.id").
    Where("users.created_at > ?", "2024-01-01").
    Group("users.id, users.name").
    Having("COUNT(posts.id) > ?", 5).
    Scan(&results)
```

### Execute Raw SQL

```go
// Raw query to struct
type Result struct {
    ID   int
    Name string
}
var results []Result
db.Raw("SELECT id, name FROM users WHERE status = ?", "active").Scan(&results)

// Raw query to map
var result map[string]interface{}
db.Raw("SELECT * FROM users WHERE id = ?", 1).Scan(&result)

// Execute without result (INSERT/UPDATE/DELETE)
db.Exec("UPDATE users SET status = ? WHERE age < ?", "minor", 18)

// Using Rows for iteration
rows, _ := db.Raw("SELECT id, name FROM users").Rows()
defer rows.Close()
for rows.Next() {
    var id int
    var name string
    rows.Scan(&id, &name)
}
```

### Get SQL Without Executing

```go
// Using ToSQL (GORM v2)
sql := db.ToSQL(func(tx *gorm.DB) *gorm.DB {
    return tx.Model(&User{}).Where("id = ?", 1).Find(&User{})
})

// Using DryRun mode
stmt := db.Session(&gorm.Session{DryRun: true}).
    Where("name = ?", "john").
    First(&User{}).Statement

sql := stmt.SQL.String()
vars := stmt.Vars
```

---

## sqlc

sqlc generates Go code from SQL queries - you write SQL, it generates type-safe Go.

### Configuration (sqlc.yaml)

```yaml
version: "2"
sql:
  - engine: "postgresql"
    queries: "query.sql"
    schema: "schema.sql"
    gen:
      go:
        package: "db"
        out: "db"
        sql_package: "pgx/v5"
        emit_json_tags: true
```

### Query Definition (query.sql)

```sql
-- name: GetUser :one
SELECT id, name, email, created_at
FROM users
WHERE id = $1;

-- name: ListUsers :many
SELECT id, name, email
FROM users
WHERE status = $1
ORDER BY created_at DESC
LIMIT $2 OFFSET $3;

-- name: CreateUser :one
INSERT INTO users (name, email, status)
VALUES ($1, $2, $3)
RETURNING id, name, email, created_at;

-- name: UpdateUserStatus :exec
UPDATE users SET status = $1 WHERE id = $2;

-- name: GetUserWithPosts :many
SELECT u.id, u.name, p.id as post_id, p.title
FROM users u
LEFT JOIN posts p ON u.id = p.user_id
WHERE u.id = $1;
```

### Generated Code Usage

```go
// Using generated queries
queries := db.New(conn)

// Single row query
user, err := queries.GetUser(ctx, userID)

// Multiple rows
users, err := queries.ListUsers(ctx, db.ListUsersParams{
    Status: "active",
    Limit:  10,
    Offset: 0,
})

// Insert returning
newUser, err := queries.CreateUser(ctx, db.CreateUserParams{
    Name:   "John",
    Email:  "john@example.com",
    Status: "active",
})

// Update/Delete (no return)
err = queries.UpdateUserStatus(ctx, db.UpdateUserStatusParams{
    Status: "inactive",
    ID:     userID,
})
```

### Enable Logging

sqlc uses the underlying database driver. For pgx:

```go
import (
    "github.com/jackc/pgx/v5/tracelog"
)

config, _ := pgxpool.ParseConfig(connString)
config.ConnConfig.Tracer = &tracelog.TraceLog{
    Logger:   myLogger,
    LogLevel: tracelog.LogLevelDebug,
}
```

---

## sqlx

### Enable Logging

sqlx inherits from database/sql. Use a logging wrapper:

```go
import (
    "database/sql"
    "github.com/jmoiron/sqlx"
    _ "github.com/lib/pq"
)

// Custom logging driver wrapper
type loggingDB struct {
    *sqlx.DB
}

func (l *loggingDB) QueryxContext(ctx context.Context, query string, args ...interface{}) (*sqlx.Rows, error) {
    log.Printf("SQL: %s | Args: %v", query, args)
    start := time.Now()
    rows, err := l.DB.QueryxContext(ctx, query, args...)
    log.Printf("Duration: %v", time.Since(start))
    return rows, err
}
```

### ORM to SQL Conversion

sqlx is a thin wrapper - you write SQL directly:

```go
// Select into struct
type User struct {
    ID        int    `db:"id"`
    Name      string `db:"name"`
    Email     string `db:"email"`
    CreatedAt time.Time `db:"created_at"`
}

var users []User
err := db.Select(&users, `
    SELECT id, name, email, created_at
    FROM users
    WHERE status = $1 AND age >= $2
    ORDER BY created_at DESC
    LIMIT $3 OFFSET $4
`, "active", 18, 10, 20)

// Named queries
query := `SELECT * FROM users WHERE name = :name AND status = :status`
rows, err := db.NamedQuery(query, map[string]interface{}{
    "name":   "john",
    "status": "active",
})
```

### SQL to ORM Conversion

sqlx IS raw SQL - no conversion needed:

```go
// Complex query with joins and aggregation
type UserStats struct {
    ID        int    `db:"id"`
    Name      string `db:"name"`
    PostCount int    `db:"post_count"`
}

var stats []UserStats
err := db.Select(&stats, `
    SELECT u.id, u.name, COUNT(p.id) as post_count
    FROM users u
    LEFT JOIN posts p ON u.id = p.user_id
    WHERE u.created_at > $1
    GROUP BY u.id, u.name
    HAVING COUNT(p.id) > $2
`, "2024-01-01", 5)
```

### Execute Raw SQL

```go
// Query single row
var user User
err := db.Get(&user, "SELECT * FROM users WHERE id = $1", 1)

// Query multiple rows
var users []User
err := db.Select(&users, "SELECT * FROM users WHERE status = $1", "active")

// Execute (INSERT/UPDATE/DELETE)
result, err := db.Exec("UPDATE users SET status = $1 WHERE id = $2", "inactive", 1)
rowsAffected, _ := result.RowsAffected()

// Named exec
result, err := db.NamedExec(`
    INSERT INTO users (name, email) VALUES (:name, :email)
`, map[string]interface{}{"name": "john", "email": "john@example.com"})
```

---

## ent

### Enable Logging

```go
import (
    "entgo.io/ent/dialect"
    "entgo.io/ent/dialect/sql"
)

// Debug mode
client := client.Debug()

// Custom logging driver
drv, _ := sql.Open("postgres", dsn)
client := ent.NewClient(ent.Driver(
    dialect.DebugWithContext(drv, func(ctx context.Context, args ...interface{}) {
        log.Println(args...)
    }),
))
```

### ORM to SQL Conversion

```go
// ent Query
users, err := client.User.
    Query().
    Select(user.FieldID, user.FieldName, user.FieldEmail).
    Where(
        user.StatusEQ("active"),
        user.AgeGTE(18),
    ).
    WithPosts(func(q *ent.PostQuery) {
        q.Where(post.PublishedEQ(true))
    }).
    Order(ent.Desc(user.FieldCreatedAt)).
    Limit(10).
    Offset(20).
    All(ctx)

// Generated SQL
SELECT "users"."id", "users"."name", "users"."email"
FROM "users"
WHERE "users"."status" = $1 AND "users"."age" >= $2
ORDER BY "users"."created_at" DESC
LIMIT 10 OFFSET 20;

-- Separate query for relations
SELECT "posts"."id", "posts"."title", "posts"."user_id"
FROM "posts"
WHERE "posts"."user_id" IN ($1, $2, ...) AND "posts"."published" = true;
```

### SQL to ORM Conversion

```go
// For complex aggregations, use raw SQL modifier
var result []struct {
    ID        int    `json:"id"`
    Name      string `json:"name"`
    PostCount int    `json:"post_count"`
}

err := client.User.
    Query().
    Modify(func(s *sql.Selector) {
        s.Select(
            sql.As(user.FieldID, "id"),
            sql.As(user.FieldName, "name"),
            sql.As(sql.Count("*"), "post_count"),
        ).
        LeftJoin(sql.Table("posts")).
        On(s.C(user.FieldID), sql.Table("posts").C("user_id")).
        GroupBy(user.FieldID, user.FieldName).
        Having(sql.GT(sql.Count("*"), 5))
    }).
    Scan(ctx, &result)
```

### Execute Raw SQL

```go
// Raw SQL query
rows, err := client.QueryContext(ctx,
    "SELECT id, name FROM users WHERE status = $1", "active")
defer rows.Close()

// Using underlying driver
drv := client.Driver()
rows, err := drv.Query(ctx, "SELECT * FROM users WHERE id = $1", 1)
```
