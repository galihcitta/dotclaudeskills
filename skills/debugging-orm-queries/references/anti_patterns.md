# ORM Anti-Patterns Reference

Common performance anti-patterns when using ORMs, how to detect them, and solutions.

## Table of Contents

1. [N+1 Query Problem](#n1-query-problem)
2. [Cartesian Product / Cross Join](#cartesian-product)
3. [Over-fetching (SELECT *)](#over-fetching)
4. [Under-fetching (Missing Eager Loading)](#under-fetching)
5. [Missing Indexes](#missing-indexes)
6. [Implicit Type Casting](#implicit-type-casting)
7. [Unbounded Queries](#unbounded-queries)
8. [Inefficient Pagination](#inefficient-pagination)
9. [Query in Loop](#query-in-loop)
10. [Missing Connection Pooling](#missing-connection-pooling)

---

## N+1 Query Problem

### Description
One query to fetch parent records, then N additional queries to fetch related records for each parent.

### How to Detect

**Query Log Pattern:**
```sql
-- 1 query for users
SELECT * FROM users WHERE active = true;

-- N queries for each user's posts (BAD!)
SELECT * FROM posts WHERE user_id = 1;
SELECT * FROM posts WHERE user_id = 2;
SELECT * FROM posts WHERE user_id = 3;
...
```

**Signs:**
- Query count scales linearly with data size
- Many similar queries with different IDs
- Slow endpoints that worked fine with small data

### Solutions by ORM

**Sequelize:**
```javascript
// BAD
const users = await User.findAll();
for (const user of users) {
  const posts = await user.getPosts(); // N+1!
}

// GOOD - Eager loading
const users = await User.findAll({
  include: [{ model: Post }]
});
```

**Prisma:**
```javascript
// BAD
const users = await prisma.user.findMany();
for (const user of users) {
  const posts = await prisma.post.findMany({ 
    where: { userId: user.id } 
  }); // N+1!
}

// GOOD
const users = await prisma.user.findMany({
  include: { posts: true }
});
```

**GORM:**
```go
// BAD
var users []User
db.Find(&users)
for _, user := range users {
  var posts []Post
  db.Where("user_id = ?", user.ID).Find(&posts) // N+1!
}

// GOOD - Preload
var users []User
db.Preload("Posts").Find(&users)
```

**SQLAlchemy:**
```python
# BAD
users = session.query(User).all()
for user in users:
    posts = user.posts  # Lazy load triggers N+1!

# GOOD - Eager load
from sqlalchemy.orm import joinedload
users = session.query(User).options(joinedload(User.posts)).all()
```

**Django:**
```python
# BAD
users = User.objects.all()
for user in users:
    posts = user.post_set.all()  # N+1!

# GOOD - prefetch_related for many-to-many/reverse FK
users = User.objects.prefetch_related('post_set').all()

# GOOD - select_related for FK/one-to-one
posts = Post.objects.select_related('author').all()
```

---

## Cartesian Product

### Description
Joining tables without proper conditions, resulting in every row matched with every other row.

### How to Detect

**Query Pattern:**
```sql
-- BAD: Missing join condition
SELECT * FROM users, orders;  -- Comma syntax = cross join

-- BAD: Missing ON clause relationship
SELECT * FROM users u
JOIN orders o ON 1=1;  -- Always true = cartesian
```

**Signs:**
- Result set size = table1_rows × table2_rows
- Extremely slow queries on moderate data
- Memory exhaustion errors

### Solutions

**Always use explicit JOIN with ON:**
```sql
-- GOOD
SELECT * FROM users u
INNER JOIN orders o ON u.id = o.user_id;
```

**ORM Example (Sequelize):**
```javascript
// BAD - might generate cartesian if association wrong
User.findAll({
  include: [{ model: Order, required: false }]
});

// GOOD - verify association is properly defined
User.hasMany(Order, { foreignKey: 'userId' });
Order.belongsTo(User, { foreignKey: 'userId' });
```

---

## Over-fetching

### Description
Selecting all columns when only a few are needed.

### How to Detect

**Query Pattern:**
```sql
-- BAD
SELECT * FROM users;  -- Fetches 50 columns when you need 3

-- GOOD
SELECT id, name, email FROM users;
```

**Signs:**
- Large memory usage
- Slow network transfer
- Response includes unused data

### Solutions by ORM

**Sequelize:**
```javascript
User.findAll({
  attributes: ['id', 'name', 'email']
});
```

**Prisma:**
```javascript
prisma.user.findMany({
  select: { id: true, name: true, email: true }
});
```

**GORM:**
```go
db.Select("id", "name", "email").Find(&users)
```

**SQLAlchemy:**
```python
session.query(User.id, User.name, User.email).all()
# or
session.execute(select(User.id, User.name, User.email))
```

**Django:**
```python
User.objects.values('id', 'name', 'email')
# or for model instances with deferred fields
User.objects.only('id', 'name', 'email')
```

---

## Under-fetching

### Description
Not fetching needed related data, leading to additional queries or incomplete data.

### How to Detect

**Signs:**
- Multiple round-trips to render one view
- Missing data in API responses
- Lazy loading errors in detached sessions

### Solutions

Plan data requirements upfront and use appropriate loading:

| ORM | Eager Load Method |
|-----|-------------------|
| Sequelize | `include: [Model]` |
| Prisma | `include: { relation: true }` |
| TypeORM | `relations: ['relation']` or `leftJoinAndSelect` |
| GORM | `Preload("Relation")` |
| SQLAlchemy | `joinedload()`, `selectinload()` |
| Django | `select_related()`, `prefetch_related()` |

---

## Missing Indexes

### Description
Queries filtering or joining on unindexed columns cause full table scans.

### How to Detect

**EXPLAIN Output (PostgreSQL):**
```
Seq Scan on users  (cost=0.00..1000.00 rows=50000)
  Filter: (email = 'test@example.com')
```

**EXPLAIN Output (MySQL):**
```
type: ALL
key: NULL
rows: 50000
```

### Common Columns to Index

- Primary keys (automatic)
- Foreign keys used in JOINs
- Columns in WHERE clauses
- Columns in ORDER BY
- Columns used for uniqueness checks

### Solutions

```sql
-- PostgreSQL
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_orders_user_id ON orders(user_id);

-- Composite index for common query patterns
CREATE INDEX idx_users_status_created 
ON users(status, created_at DESC);
```

**ORM Migration Examples:**

```javascript
// Sequelize
queryInterface.addIndex('users', ['email']);

// Prisma (schema.prisma)
model User {
  email String @unique
  @@index([status, createdAt])
}

// TypeORM
@Index(['status', 'createdAt'])
```

---

## Implicit Type Casting

### Description
Database converts column type to match query parameter, preventing index usage.

### How to Detect

**PostgreSQL:**
```sql
-- BAD: id is integer, passing string
SELECT * FROM users WHERE id = '123';

-- EXPLAIN shows:
-- Seq Scan with Filter (index not used)
```

### Solutions

**Ensure type consistency:**
```javascript
// BAD
const id = req.params.id; // string '123'
User.findByPk(id);

// GOOD
const id = parseInt(req.params.id, 10);
User.findByPk(id);
```

**Database-side:**
```sql
-- Cast explicitly if needed
SELECT * FROM users WHERE id = '123'::integer;
```

---

## Unbounded Queries

### Description
Queries without LIMIT that could return millions of rows.

### How to Detect

**Query Pattern:**
```sql
-- BAD: No limit
SELECT * FROM logs;  -- Could be millions of rows

-- GOOD
SELECT * FROM logs ORDER BY created_at DESC LIMIT 100;
```

### Solutions

**Always add limits:**
```javascript
// Sequelize
User.findAll({ limit: 100 });

// Prisma
prisma.user.findMany({ take: 100 });

// GORM
db.Limit(100).Find(&users)
```

**Application-level defaults:**
```javascript
const DEFAULT_LIMIT = 100;
const MAX_LIMIT = 1000;

function getLimit(requested) {
  if (!requested) return DEFAULT_LIMIT;
  return Math.min(parseInt(requested), MAX_LIMIT);
}
```

---

## Inefficient Pagination

### Description
Using OFFSET for deep pagination causes performance degradation.

### How to Detect

**Query Pattern:**
```sql
-- BAD: Gets slower as offset increases
SELECT * FROM posts ORDER BY id LIMIT 20 OFFSET 10000;
-- Database still scans 10020 rows
```

### Solutions

**Cursor-based pagination:**
```sql
-- GOOD: Consistent performance
SELECT * FROM posts 
WHERE id > :last_seen_id 
ORDER BY id 
LIMIT 20;
```

**ORM Implementation:**
```javascript
// Sequelize cursor pagination
Post.findAll({
  where: { id: { [Op.gt]: lastSeenId } },
  order: [['id', 'ASC']],
  limit: 20
});

// Prisma cursor pagination
prisma.post.findMany({
  take: 20,
  skip: 1,
  cursor: { id: lastSeenId }
});
```

---

## Query in Loop

### Description
Executing database queries inside application loops instead of batching.

### How to Detect

**Code Pattern:**
```javascript
// BAD
for (const id of userIds) {
  const user = await User.findByPk(id);
  results.push(user);
}
```

### Solutions

**Batch queries:**
```javascript
// GOOD - Single query with IN
const users = await User.findAll({
  where: { id: { [Op.in]: userIds } }
});

// Prisma
const users = await prisma.user.findMany({
  where: { id: { in: userIds } }
});

// GORM
db.Where("id IN ?", userIds).Find(&users)
```

**Bulk operations:**
```javascript
// BAD - Multiple inserts
for (const data of items) {
  await Model.create(data);
}

// GOOD - Bulk insert
await Model.bulkCreate(items);
```

---

## Missing Connection Pooling

### Description
Creating new database connections for each query instead of reusing from a pool.

### How to Detect

**Signs:**
- "Too many connections" errors
- High connection establishment overhead
- Slow queries even for simple operations

### Solutions

**Configure connection pool:**
```javascript
// Sequelize
const sequelize = new Sequelize({
  pool: {
    max: 20,
    min: 5,
    acquire: 30000,
    idle: 10000
  }
});

// Prisma (schema.prisma)
datasource db {
  url = env("DATABASE_URL")
  // Add connection_limit to URL:
  // postgresql://user:pass@host/db?connection_limit=20
}
```

```go
// GORM
sqlDB, _ := db.DB()
sqlDB.SetMaxOpenConns(20)
sqlDB.SetMaxIdleConns(5)
sqlDB.SetConnMaxLifetime(time.Hour)
```

```python
# SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    pool_size=5,
    max_overflow=10,
    pool_recycle=3600
)
```

---

## Quick Detection Checklist

| Issue | Detection Method |
|-------|-----------------|
| N+1 | Query count >> expected; repeated similar queries |
| Cartesian | Result size = product of table sizes |
| Over-fetch | SELECT * in logs; large response payloads |
| Missing Index | EXPLAIN shows Seq Scan / type: ALL |
| Unbounded | No LIMIT in SELECT queries |
| Deep Offset | OFFSET > 1000 in queries |
| Loop Queries | Same query pattern with different params |

## Tools for Detection

1. **Query Logging** - Enable in all environments
2. **EXPLAIN ANALYZE** - Check execution plans
3. **APM Tools** - DataDog, New Relic, etc.
4. **Query Analyzer Script** - See `scripts/query_analyzer.py`
5. **pg_stat_statements** (PostgreSQL) - Query statistics
6. **slow_query_log** (MySQL) - Slow query logging
