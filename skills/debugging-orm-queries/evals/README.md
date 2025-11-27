# Evaluations

Test scenarios for validating skill effectiveness.

## Running Evaluations

Each evaluation in `evaluations.json` contains:
- `id`: Unique identifier
- `skills`: Skills to load (always `["debugging-orm-queries"]`)
- `query`: User request to test
- `files`: Any test files needed (empty for most)
- `expected_behavior`: What Claude should do

## Test Coverage

| ID | Scenario | Tests |
|----|----------|-------|
| eval-001 | Sequelize → SQL | ORM-to-SQL conversion, JOIN handling |
| eval-002 | SQL → GORM | SQL-to-ORM conversion, Go patterns |
| eval-003 | N+1 detection | Anti-pattern identification |
| eval-004 | EXPLAIN analysis | Performance diagnosis |
| eval-005 | Django optimization | Python ORM, eager loading |

## Validation Criteria

Pass if Claude:
1. Reads appropriate reference file
2. Produces correct conversion/analysis
3. References anti-patterns when relevant
4. Suggests scripts for automation
