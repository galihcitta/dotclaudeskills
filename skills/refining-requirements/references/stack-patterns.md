# Stack-Specific Patterns

Adapt output based on detected or specified tech stack.

## Contents
- [Stack Detection](#stack-detection)
- [File Extension Mappings](#file-extension-mappings)
- [Directory Structure by Stack](#directory-structure-by-stack)
- [Migration Patterns by Stack](#migration-patterns-by-stack)
- [Model Definition by Stack](#model-definition-by-stack)
- [API Controller Patterns](#api-controller-patterns)
- [Test Patterns by Stack](#test-patterns-by-stack)
- [Naming Conventions](#naming-conventions)
- [Output Adaptation](#output-adaptation)

## Stack Detection

Detect from file paths, imports, or ask user:

| Indicator | Stack |
|-----------|-------|
| `.js`, `package.json`, `node_modules` | Node.js |
| `.go`, `go.mod`, `go.sum` | Go |
| `.py`, `requirements.txt`, `pyproject.toml` | Python |
| `.java`, `pom.xml`, `build.gradle` | Java/Kotlin |
| `.rb`, `Gemfile` | Ruby |
| `.cs`, `.csproj` | C# / .NET |
| `.rs`, `Cargo.toml` | Rust |
| `.php`, `composer.json` | PHP |

---

## File Extension Mappings

| Component | Node.js | Go | Python | Java |
|-----------|---------|-----|--------|------|
| Controller | `.js` / `.ts` | `.go` | `.py` | `.java` |
| Model | `.js` / `.ts` | `.go` | `.py` | `.java` |
| Route | `.js` / `.ts` | `.go` | `.py` | `.java` |
| Test | `.test.js` / `.spec.ts` | `_test.go` | `test_*.py` | `*Test.java` |
| Config | `.json` / `.env` | `.yaml` / `.env` | `.yaml` / `.env` | `.properties` / `.yaml` |

---

## Directory Structure by Stack

### Node.js (Express/NestJS)
```
app/
├── controllers/
│   └── v2/
│       └── pin/
│           ├── create.js
│           └── login.js
├── models/
│   └── egift.js
├── routes/
│   └── v2.js
├── services/
│   └── verification.js
└── migrations/
    └── 20241127-add-field.js
```

### Go (Standard/Gin/Echo)
```
internal/
├── handler/
│   └── pin/
│       ├── create.go
│       └── login.go
├── model/
│   └── egift.go
├── repository/
│   └── egift_repo.go
├── service/
│   └── verification.go
└── migration/
    └── 20241127_add_field.sql
cmd/
└── api/
    └── main.go
```

### Python (FastAPI/Django)
```
app/
├── api/
│   └── v2/
│       └── pin/
│           ├── create.py
│           └── login.py
├── models/
│   └── egift.py
├── schemas/
│   └── pin.py
├── services/
│   └── verification.py
└── migrations/
    └── versions/
        └── 20241127_add_field.py
```

### Java (Spring Boot)
```
src/main/java/com/example/
├── controller/
│   └── PinController.java
├── model/
│   └── Egift.java
├── repository/
│   └── EgiftRepository.java
├── service/
│   └── VerificationService.java
└── dto/
    └── PinRequest.java
src/main/resources/
└── db/migration/
    └── V1__add_field.sql
```

---

## Migration Patterns by Stack

### Node.js (Sequelize)
```javascript
module.exports = {
  up: async (queryInterface, Sequelize) => {
    await queryInterface.addColumn('Egifts', 'eligiblePhoneNumber', {
      type: Sequelize.STRING(20),
      allowNull: true
    });
  },
  down: async (queryInterface) => {
    await queryInterface.removeColumn('Egifts', 'eligiblePhoneNumber');
  }
};
```

### Go (golang-migrate / SQL)
```sql
-- 20241127_add_eligible_phone.up.sql
ALTER TABLE egifts ADD COLUMN eligible_phone_number VARCHAR(20);

-- 20241127_add_eligible_phone.down.sql
ALTER TABLE egifts DROP COLUMN eligible_phone_number;
```

### Python (Alembic)
```python
def upgrade():
    op.add_column('egifts', sa.Column('eligible_phone_number', sa.String(20), nullable=True))

def downgrade():
    op.drop_column('egifts', 'eligible_phone_number')
```

### Java (Flyway)
```sql
-- V1__add_eligible_phone.sql
ALTER TABLE egifts ADD COLUMN eligible_phone_number VARCHAR(20);
```

---

## Model Definition by Stack

### Node.js (Sequelize)
```javascript
eligiblePhoneNumber: {
  type: DataTypes.STRING(20),
  allowNull: true,
  field: 'eligible_phone_number'
}
```

### Go (GORM)
```go
type Egift struct {
    ID                   uint   `gorm:"primaryKey"`
    EligiblePhoneNumber  string `gorm:"size:20"`
}
```

### Python (SQLAlchemy)
```python
eligible_phone_number = Column(String(20), nullable=True)
```

### Java (JPA/Hibernate)
```java
@Column(name = "eligible_phone_number", length = 20)
private String eligiblePhoneNumber;
```

---

## API Controller Patterns

### Node.js (Express)
```javascript
router.post('/pin/create', async (req, res) => {
  const { memberId, pin } = req.body;
  // ...
  res.json({ success: true });
});
```

### Go (Gin)
```go
func (h *PinHandler) Create(c *gin.Context) {
    var req CreatePinRequest
    if err := c.ShouldBindJSON(&req); err != nil {
        c.JSON(400, gin.H{"error": err.Error()})
        return
    }
    // ...
    c.JSON(200, gin.H{"success": true})
}
```

### Python (FastAPI)
```python
@router.post("/pin/create")
async def create_pin(request: CreatePinRequest):
    # ...
    return {"success": True}
```

### Java (Spring)
```java
@PostMapping("/pin/create")
public ResponseEntity<Map<String, Object>> createPin(@RequestBody CreatePinRequest request) {
    // ...
    return ResponseEntity.ok(Map.of("success", true));
}
```

---

## Test Patterns by Stack

### Node.js (Jest)
```javascript
describe('POST /pin/create', () => {
  it('should create PIN successfully', async () => {
    const res = await request(app)
      .post('/v2/pin/create')
      .send({ memberId: '123', pin: '482916' });
    expect(res.status).toBe(200);
    expect(res.body.success).toBe(true);
  });
});
```

### Go (testing)
```go
func TestCreatePin(t *testing.T) {
    req := CreatePinRequest{MemberID: "123", PIN: "482916"}
    // ...
    assert.Equal(t, 200, resp.Code)
}
```

### Python (pytest)
```python
def test_create_pin(client):
    response = client.post("/v2/pin/create", json={"member_id": "123", "pin": "482916"})
    assert response.status_code == 200
    assert response.json()["success"] == True
```

### Java (JUnit)
```java
@Test
void shouldCreatePin() {
    var request = new CreatePinRequest("123", "482916");
    var response = controller.createPin(request);
    assertEquals(HttpStatus.OK, response.getStatusCode());
}
```

---

## Naming Conventions

| Concept | Node.js | Go | Python | Java |
|---------|---------|-----|--------|------|
| Variable | `camelCase` | `camelCase` | `snake_case` | `camelCase` |
| Function | `camelCase` | `PascalCase` (exported) | `snake_case` | `camelCase` |
| File | `kebab-case.js` | `snake_case.go` | `snake_case.py` | `PascalCase.java` |
| DB Column | `snake_case` | `snake_case` | `snake_case` | `snake_case` |
| Constant | `UPPER_CASE` | `PascalCase` | `UPPER_CASE` | `UPPER_CASE` |

---

## Output Adaptation

When generating refined PRD, adapt examples to match the stack:

**Detected: Go project**
```markdown
## File Mappings
### Create
- `internal/handler/pin/create.go` — PIN creation handler
- `internal/model/egift.go` — Add EligiblePhoneNumber field
- `migration/20241127_add_phone.up.sql` — Schema migration

## Migration
```sql
ALTER TABLE egifts ADD COLUMN eligible_phone_number VARCHAR(20);
```
```

**Detected: Python/FastAPI project**
```markdown
## File Mappings
### Create
- `app/api/v2/pin/create.py` — PIN creation endpoint
- `app/models/egift.py` — Add eligible_phone_number field
- `migrations/versions/20241127_add_phone.py` — Alembic migration

## Migration
```python
op.add_column('egifts', sa.Column('eligible_phone_number', sa.String(20)))
```
```
