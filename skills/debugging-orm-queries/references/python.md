# Python ORMs Reference

## Table of Contents

1. [SQLAlchemy](#sqlalchemy)
2. [Django ORM](#django-orm)
3. [Peewee](#peewee)

---

## SQLAlchemy

### Enable Logging

```python
from sqlalchemy import create_engine
import logging

# Method 1: echo parameter
engine = create_engine(
    "postgresql://user:pass@localhost/db",
    echo=True,       # Log all SQL
    echo_pool=True   # Log connection pool events
)

# Method 2: Python logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# Method 3: Event listener
from sqlalchemy import event

@event.listens_for(engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    print(f"SQL: {statement}")
    print(f"Parameters: {parameters}")
```

### ORM to SQL Conversion

```python
# SQLAlchemy ORM Query
from sqlalchemy.orm import Session
from sqlalchemy import select, func

stmt = (
    select(User.id, User.name, User.email)
    .join(Post, User.id == Post.user_id)
    .where(User.status == 'active')
    .where(User.age >= 18)
    .order_by(User.created_at.desc())
    .limit(10)
    .offset(20)
)
users = session.execute(stmt).all()

# Generated SQL
SELECT users.id, users.name, users.email
FROM users
JOIN posts ON users.id = posts.user_id
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
HAVING COUNT(p.id) > 5
ORDER BY post_count DESC;
```

```python
# SQLAlchemy equivalent
from sqlalchemy import select, func

stmt = (
    select(
        User.id,
        User.name,
        func.count(Post.id).label('post_count')
    )
    .outerjoin(Post, User.id == Post.user_id)
    .where(User.created_at > '2024-01-01')
    .group_by(User.id, User.name)
    .having(func.count(Post.id) > 5)
    .order_by(func.count(Post.id).desc())
)
results = session.execute(stmt).all()
```

### Execute Raw SQL

```python
from sqlalchemy import text

# Raw query with parameters
result = session.execute(
    text("SELECT * FROM users WHERE status = :status"),
    {"status": "active"}
)
users = result.fetchall()

# Raw query to ORM objects
stmt = text("SELECT * FROM users WHERE id = :id")
user = session.execute(stmt, {"id": 1}).fetchone()

# Execute without result (UPDATE/DELETE)
session.execute(
    text("UPDATE users SET status = :status WHERE id = :id"),
    {"status": "inactive", "id": 1}
)
session.commit()

# Using connection directly
with engine.connect() as conn:
    result = conn.execute(text("SELECT 1"))
```

### Get SQL Without Executing

```python
from sqlalchemy.dialects import postgresql, mysql, sqlite

# Basic stringification
stmt = select(User).where(User.id == 1)
print(str(stmt))  # SELECT users.id, ... WHERE users.id = :id_1

# With literal values (DEBUG ONLY - not safe for production!)
print(stmt.compile(compile_kwargs={"literal_binds": True}))
# SELECT users.id, ... WHERE users.id = 1

# For specific dialect
print(stmt.compile(dialect=postgresql.dialect()))

# Get parameters separately
compiled = stmt.compile()
print(compiled.string)    # SQL with placeholders
print(compiled.params)    # Dictionary of parameters
```

---

## Django ORM

### Enable Logging

```python
# settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}

# Or programmatically
import logging
logging.getLogger('django.db.backends').setLevel(logging.DEBUG)
logging.getLogger('django.db.backends').addHandler(logging.StreamHandler())
```

### ORM to SQL Conversion

```python
# Django ORM Query
from django.db.models import Count, Q

users = (
    User.objects
    .select_related('profile')
    .prefetch_related('posts')
    .filter(status='active', age__gte=18)
    .exclude(email__isnull=True)
    .order_by('-created_at')
    [:10]
)

# Generated SQL
SELECT "users"."id", "users"."name", "users"."email", 
       "profiles"."id", "profiles"."bio"
FROM "users"
LEFT JOIN "profiles" ON "users"."id" = "profiles"."user_id"
WHERE "users"."status" = 'active' 
  AND "users"."age" >= 18
  AND "users"."email" IS NOT NULL
ORDER BY "users"."created_at" DESC
LIMIT 10;
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

```python
# Django ORM equivalent
from django.db.models import Count

users = (
    User.objects
    .filter(created_at__gt='2024-01-01')
    .annotate(post_count=Count('posts'))
    .filter(post_count__gt=5)
    .values('id', 'name', 'post_count')
)
```

### Execute Raw SQL

```python
from django.db import connection

# Raw query with model mapping
users = User.objects.raw(
    'SELECT * FROM users WHERE status = %s',
    ['active']
)

# Raw query without model
with connection.cursor() as cursor:
    cursor.execute(
        "SELECT id, name FROM users WHERE status = %s",
        ['active']
    )
    rows = cursor.fetchall()
    # Or as dictionaries
    columns = [col[0] for col in cursor.description]
    rows = [dict(zip(columns, row)) for row in cursor.fetchall()]

# Execute without result
with connection.cursor() as cursor:
    cursor.execute(
        "UPDATE users SET status = %s WHERE id = %s",
        ['inactive', 1]
    )
```

### Get SQL Without Executing

```python
# Get SQL from QuerySet
queryset = User.objects.filter(status='active')

# Method 1: str(queryset.query)
print(queryset.query)  # Warning: may not show exact SQL for all databases

# Method 2: Using explain (executes EXPLAIN, not the query itself)
print(queryset.explain())

# Method 3: Check connection.queries after execution
from django.db import connection, reset_queries
reset_queries()
list(queryset)  # Execute query
print(connection.queries[-1]['sql'])
```

### Django Query Lookups Reference

| Lookup | SQL Equivalent |
|--------|---------------|
| `exact` | `= value` |
| `iexact` | `ILIKE value` (case-insensitive) |
| `contains` | `LIKE '%value%'` |
| `in` | `IN (...)` |
| `gt` / `gte` | `>` / `>=` |
| `lt` / `lte` | `<` / `<=` |
| `startswith` | `LIKE 'value%'` |
| `range` | `BETWEEN` |
| `isnull` | `IS NULL` / `IS NOT NULL` |

---

## Peewee

### Enable Logging

```python
import logging
from peewee import *

# Method 1: Set up logging
logger = logging.getLogger('peewee')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

# Method 2: Database-level logging
db = PostgresqlDatabase(
    'my_database',
    user='user',
    password='pass'
)

# Custom logger
import sys
db = PostgresqlDatabase('my_db')

class MyRetryDB(PostgresqlDatabase):
    def execute_sql(self, sql, params=None, commit=True):
        print(f"SQL: {sql}")
        print(f"Params: {params}")
        return super().execute_sql(sql, params, commit)
```

### ORM to SQL Conversion

```python
# Peewee Query
query = (
    User
    .select(User.id, User.name, User.email)
    .join(Post, JOIN.LEFT_OUTER)
    .where(User.status == 'active')
    .where(User.age >= 18)
    .order_by(User.created_at.desc())
    .limit(10)
    .offset(20)
)
users = list(query)

# Generated SQL
SELECT "t1"."id", "t1"."name", "t1"."email"
FROM "users" AS "t1"
LEFT OUTER JOIN "posts" AS "t2" ON ("t1"."id" = "t2"."user_id")
WHERE ("t1"."status" = 'active') AND ("t1"."age" >= 18)
ORDER BY "t1"."created_at" DESC
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

```python
# Peewee equivalent
from peewee import fn

query = (
    User
    .select(User.id, User.name, fn.COUNT(Post.id).alias('post_count'))
    .join(Post, JOIN.LEFT_OUTER)
    .where(User.created_at > '2024-01-01')
    .group_by(User.id, User.name)
    .having(fn.COUNT(Post.id) > 5)
)
```

### Execute Raw SQL

```python
# Raw select query
query = User.raw('SELECT * FROM users WHERE status = %s', 'active')
for user in query:
    print(user.name)

# Raw query to tuples
cursor = db.execute_sql(
    'SELECT id, name FROM users WHERE status = %s',
    ('active',)
)
for row in cursor.fetchall():
    print(row)

# Execute without result
db.execute_sql(
    'UPDATE users SET status = %s WHERE id = %s',
    ('inactive', 1)
)
```

### Get SQL Without Executing

```python
# Get SQL from query
query = User.select().where(User.status == 'active')

# Method 1: sql() method returns (sql, params)
sql, params = query.sql()
print(f"SQL: {sql}")
print(f"Params: {params}")

# Method 2: String representation
print(query)  # Shows SQL with placeholders

# For INSERT/UPDATE
insert_query = User.insert(name='John', email='john@example.com')
sql, params = insert_query.sql()
```

### Peewee Operators Reference

```python
# Comparison operators
User.age == 18        # = 18
User.age != 18        # != 18
User.age > 18         # > 18
User.age >= 18        # >= 18
User.age < 18         # < 18
User.age <= 18        # <= 18

# String operators
User.name % 'John%'   # LIKE 'John%'
User.name ** 'john'   # ILIKE 'john' (case-insensitive)
User.name.contains('john')  # LIKE '%john%'
User.name.startswith('J')   # LIKE 'J%'

# IN operator
User.id.in_([1, 2, 3])      # IN (1, 2, 3)
User.id.not_in([1, 2, 3])   # NOT IN (1, 2, 3)

# NULL checks
User.email.is_null()        # IS NULL
User.email.is_null(False)   # IS NOT NULL

# Combining conditions
(User.status == 'active') & (User.age >= 18)  # AND
(User.status == 'active') | (User.status == 'pending')  # OR
~(User.status == 'deleted')  # NOT
```
