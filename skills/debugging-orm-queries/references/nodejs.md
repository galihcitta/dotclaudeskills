# Node.js ORMs Reference

## Table of Contents

1. [Sequelize](#sequelize)
2. [Prisma](#prisma)
3. [TypeORM](#typeorm)

---

## Sequelize

### Enable Logging

```javascript
// Global logging
const sequelize = new Sequelize('database', 'user', 'pass', {
  logging: console.log,                    // Default
  logging: (...msg) => console.log(msg),   // All parameters
  logging: (sql) => customLogger(sql),     // Custom logger
  benchmark: true,                          // Include timing
  logQueryParameters: true                  // Show bind values
});

// Per-query logging
User.findAll({
  where: { id: 1 },
  logging: (sql, timing) => {
    console.log('SQL:', sql);
    console.log('Time:', timing, 'ms');
  }
});
```

### ORM to SQL Conversion

```javascript
// Sequelize ORM
User.findAll({
  attributes: ['id', 'name', 'email'],
  where: { 
    status: 'active',
    age: { [Op.gte]: 18 }
  },
  include: [{
    model: Post,
    where: { published: true }
  }],
  order: [['createdAt', 'DESC']],
  limit: 10,
  offset: 20
});

// Generated SQL
SELECT "User"."id", "User"."name", "User"."email", 
       "Posts"."id" AS "Posts.id", "Posts"."title" AS "Posts.title"
FROM "Users" AS "User"
INNER JOIN "Posts" ON "User"."id" = "Posts"."userId" 
  AND "Posts"."published" = true
WHERE "User"."status" = 'active' AND "User"."age" >= 18
ORDER BY "User"."createdAt" DESC
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

```javascript
// Sequelize equivalent
const { fn, col, literal } = require('sequelize');

User.findAll({
  attributes: [
    'id', 
    'name',
    [fn('COUNT', col('Posts.id')), 'post_count']
  ],
  include: [{
    model: Post,
    attributes: []
  }],
  where: {
    createdAt: { [Op.gt]: '2024-01-01' }
  },
  group: ['User.id', 'User.name'],
  having: literal('COUNT("Posts"."id") > 5')
});
```

### Execute Raw SQL

```javascript
// Raw query with model mapping
const users = await sequelize.query(
  'SELECT * FROM users WHERE status = :status',
  {
    replacements: { status: 'active' },
    type: QueryTypes.SELECT,
    model: User,
    mapToModel: true
  }
);

// Raw query without model
const [results, metadata] = await sequelize.query(
  'UPDATE users SET status = ? WHERE id = ?',
  { replacements: ['inactive', 1] }
);
```

### Sequelize Operators Quick Reference

| Operator | SQL Equivalent |
|----------|---------------|
| `Op.eq` | `= value` |
| `Op.ne` | `!= value` |
| `Op.gt` / `Op.gte` | `>` / `>=` |
| `Op.lt` / `Op.lte` | `<` / `<=` |
| `Op.in` | `IN (...)` |
| `Op.like` | `LIKE` |
| `Op.between` | `BETWEEN` |
| `Op.and` / `Op.or` | `AND` / `OR` |

---

## Prisma

### Enable Logging

```javascript
// Configure logging levels
const prisma = new PrismaClient({
  log: ['query', 'info', 'warn', 'error']
});

// Event-based logging with parameters
const prisma = new PrismaClient({
  log: [{ emit: 'event', level: 'query' }]
});

prisma.$on('query', (e) => {
  console.log('Query:', e.query);
  console.log('Params:', e.params);
  console.log('Duration:', e.duration, 'ms');
});
```

### ORM to SQL Conversion

```javascript
// Prisma ORM
const users = await prisma.user.findMany({
  select: { id: true, name: true, email: true },
  where: {
    status: 'active',
    age: { gte: 18 }
  },
  include: {
    posts: {
      where: { published: true }
    }
  },
  orderBy: { createdAt: 'desc' },
  take: 10,
  skip: 20
});

// Generated SQL (PostgreSQL)
SELECT "User"."id", "User"."name", "User"."email"
FROM "User"
WHERE "User"."status" = $1 AND "User"."age" >= $2
ORDER BY "User"."createdAt" DESC
LIMIT $3 OFFSET $4;

-- Separate query for relations
SELECT "Post"."id", "Post"."title", "Post"."userId"
FROM "Post"
WHERE "Post"."userId" IN ($1, $2, ...) AND "Post"."published" = $5;
```

### SQL to ORM Conversion

```sql
-- Raw SQL
SELECT u.*, COUNT(p.id) as post_count
FROM users u
LEFT JOIN posts p ON u.id = p.user_id
WHERE u.role IN ('admin', 'moderator')
GROUP BY u.id;
```

```javascript
// Prisma equivalent (using $queryRaw for aggregation)
const result = await prisma.$queryRaw`
  SELECT u.*, COUNT(p.id) as post_count
  FROM users u
  LEFT JOIN posts p ON u.id = p.user_id
  WHERE u.role IN ('admin', 'moderator')
  GROUP BY u.id
`;

// Or using Prisma's built-in aggregation
const users = await prisma.user.findMany({
  where: { role: { in: ['admin', 'moderator'] } },
  include: {
    _count: { select: { posts: true } }
  }
});
```

### Execute Raw SQL

```javascript
// Type-safe raw query
const users = await prisma.$queryRaw<User[]>`
  SELECT * FROM "User" WHERE status = ${status}
`;

// Unsafe raw query (for dynamic SQL)
const users = await prisma.$queryRawUnsafe(
  `SELECT * FROM "User" WHERE ${column} = $1`,
  value
);

// Execute (INSERT/UPDATE/DELETE)
const count = await prisma.$executeRaw`
  UPDATE "User" SET status = ${status} WHERE id = ${id}
`;
```

---

## TypeORM

### Enable Logging

```javascript
// DataSource configuration
const dataSource = new DataSource({
  type: 'postgres',
  logging: true,                    // All queries
  logging: ['query', 'error'],      // Specific types
  logger: 'advanced-console',       // Pretty output
  maxQueryExecutionTime: 1000       // Log slow queries
});

// Per-query logging not directly supported
// Use query builder with .printSql() for debugging
const sql = userRepository
  .createQueryBuilder('user')
  .where('user.id = :id', { id: 1 })
  .getSql();  // Returns SQL string without executing
```

### ORM to SQL Conversion

```javascript
// TypeORM QueryBuilder
const users = await userRepository
  .createQueryBuilder('user')
  .select(['user.id', 'user.name', 'user.email'])
  .leftJoinAndSelect('user.posts', 'post', 'post.published = :pub', { pub: true })
  .where('user.status = :status', { status: 'active' })
  .andWhere('user.age >= :age', { age: 18 })
  .orderBy('user.createdAt', 'DESC')
  .take(10)
  .skip(20)
  .getMany();

// Generated SQL
SELECT "user"."id", "user"."name", "user"."email",
       "post"."id" AS "post_id", "post"."title" AS "post_title"
FROM "users" "user"
LEFT JOIN "posts" "post" ON "post"."userId" = "user"."id" 
  AND "post"."published" = $1
WHERE "user"."status" = $2 AND "user"."age" >= $3
ORDER BY "user"."createdAt" DESC
LIMIT 10 OFFSET 20;
```

### SQL to ORM Conversion

```sql
-- Raw SQL
SELECT u.id, u.name, 
       COALESCE(SUM(o.total), 0) as total_spent
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.created_at BETWEEN '2024-01-01' AND '2024-12-31'
GROUP BY u.id, u.name
ORDER BY total_spent DESC;
```

```javascript
// TypeORM QueryBuilder equivalent
const result = await userRepository
  .createQueryBuilder('u')
  .select(['u.id', 'u.name'])
  .addSelect('COALESCE(SUM(o.total), 0)', 'total_spent')
  .leftJoin('u.orders', 'o')
  .where('u.createdAt BETWEEN :start AND :end', {
    start: '2024-01-01',
    end: '2024-12-31'
  })
  .groupBy('u.id')
  .addGroupBy('u.name')
  .orderBy('total_spent', 'DESC')
  .getRawMany();
```

### Execute Raw SQL

```javascript
// Raw query with entity mapping
const users = await userRepository.query(
  'SELECT * FROM users WHERE status = $1',
  ['active']
);

// Using QueryRunner for transactions
const queryRunner = dataSource.createQueryRunner();
await queryRunner.connect();
await queryRunner.startTransaction();
try {
  await queryRunner.query('UPDATE users SET status = $1 WHERE id = $2', ['inactive', 1]);
  await queryRunner.commitTransaction();
} catch (err) {
  await queryRunner.rollbackTransaction();
}
```

### Get SQL Without Executing

```javascript
// QueryBuilder - get SQL string
const qb = userRepository
  .createQueryBuilder('user')
  .where('user.id = :id', { id: 1 });

const sql = qb.getSql();           // SQL with parameters as $1, $2
const [query, params] = qb.getQueryAndParameters();  // SQL + params array
```
