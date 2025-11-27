# Scaffolding Patterns

Instructions for scaffolding boilerplate files after refining PRD.

## Contents
- [When to Scaffold](#when-to-scaffold)
- [Scaffolding Rules](#scaffolding-rules)
- [Scaffolding Templates by Stack](#scaffolding-templates-by-stack)
- [Directory Creation](#directory-creation)
- [Post-Scaffold Checklist](#post-scaffold-checklist)
- [Conflict Handling](#conflict-handling)

## When to Scaffold

After saving refined PRD, offer scaffolding if:
- Multiple new files need to be created
- Greenfield project
- User explicitly requests it

**Ask:**
> "I've saved the refined PRD to `agent-workflow/requirements/[filename].md`. Would you like me to scaffold the boilerplate files for this feature?"

## Scaffolding Rules

### 1. Read Before Write
Always read existing similar files to match code style:

```bash
# Find similar files to understand patterns
find . -name "*.controller.js" -type f | head -1 | xargs cat | head -50
find . -name "*_handler.go" -type f | head -1 | xargs cat | head -50
```

### 2. Never Overwrite
Check before creating:

```bash
# Safe file creation
if [ -f "path/to/file.js" ]; then
  echo "File exists, creating path/to/file.js.new instead"
  # Create with .new suffix
else
  # Create normally
fi
```

### 3. Match Project Conventions
Read CLAUDE.md first:

```bash
cat CLAUDE.md 2>/dev/null | grep -A 10 "code style\|naming\|conventions"
```

### 4. Add TODO Comments
Mark implementation points:

```javascript
// TODO: Implement validation logic
// TODO: Add error handling
// TODO: Write tests
```

---

## Scaffolding Templates by Stack

### Node.js (Express)

**Controller:**
```javascript
// app/controllers/v2/[feature]/[action].js
const { [Model] } = require('../../../models');

/**
 * [Description from PRD]
 * 
 * @route [METHOD] /v2/[path]
 * @access [Public/Private]
 */
const [actionName] = async (req, res) => {
  try {
    const { /* fields from PRD */ } = req.body;

    // TODO: Implement validation
    // Validation rules from PRD:
    // - [rule 1]
    // - [rule 2]

    // TODO: Implement business logic
    // Business logic from PRD:
    // - [logic 1]
    // - [logic 2]

    return res.status(200).json({
      success: true,
      // TODO: Add response fields from PRD
    });
  } catch (error) {
    console.error('[Feature] Error:', error);
    return res.status(500).json({
      error: 'INTERNAL_ERROR',
      message: 'An error occurred'
    });
  }
};

module.exports = { [actionName] };
```

**Model Field Addition:**
```javascript
// Add to app/models/[model].js
[fieldName]: {
  type: DataTypes.[TYPE],
  allowNull: [true/false],
  defaultValue: [value],
  // From PRD: [description]
},
```

**Migration:**
```javascript
// migrations/YYYYMMDD-[description].js
'use strict';

module.exports = {
  up: async (queryInterface, Sequelize) => {
    // From PRD: [description]
    await queryInterface.addColumn('[TableName]', '[fieldName]', {
      type: Sequelize.[TYPE],
      allowNull: [true/false],
      defaultValue: [value],
    });
  },

  down: async (queryInterface, Sequelize) => {
    await queryInterface.removeColumn('[TableName]', '[fieldName]');
  }
};
```

**Route Registration:**
```javascript
// Add to app/routes/v2/[feature].js
const { [action] } = require('../../controllers/v2/[feature]/[action]');

router.[method]('/[path]', [middlewares], [action]);
```

**Test File:**
```javascript
// tests/[feature]/[action].test.js
const request = require('supertest');
const app = require('../../app');

describe('[METHOD] /v2/[path]', () => {
  describe('Happy Path', () => {
    // TODO: Implement tests from PRD scenarios
    it('should [scenario 1 from PRD]', async () => {
      const res = await request(app)
        .[method]('/v2/[path]')
        .send({ /* input from PRD */ });
      
      expect(res.status).toBe(200);
      // TODO: Add assertions
    });
  });

  describe('Edge Cases', () => {
    // TODO: Implement edge case tests from PRD
  });

  describe('Error Handling', () => {
    // TODO: Implement error tests from PRD
  });
});
```

---

### Go (Gin)

**Handler:**
```go
// internal/handler/[feature]/[action].go
package [feature]

import (
	"net/http"
	"github.com/gin-gonic/gin"
)

// [ActionName]Request represents the request body
// From PRD: [description]
type [ActionName]Request struct {
	// TODO: Add fields from PRD
	FieldName string `json:"fieldName" binding:"required"`
}

// [ActionName]Response represents the response body
type [ActionName]Response struct {
	Success bool   `json:"success"`
	// TODO: Add fields from PRD
}

// [ActionName] handles [description from PRD]
// @Summary [summary]
// @Description [description]
// @Tags [feature]
// @Accept json
// @Produce json
// @Param request body [ActionName]Request true "Request body"
// @Success 200 {object} [ActionName]Response
// @Router /v2/[path] [[method]]
func (h *Handler) [ActionName](c *gin.Context) {
	var req [ActionName]Request
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	// TODO: Implement validation
	// Validation rules from PRD:
	// - [rule 1]
	// - [rule 2]

	// TODO: Implement business logic
	// Business logic from PRD:
	// - [logic 1]
	// - [logic 2]

	c.JSON(http.StatusOK, [ActionName]Response{
		Success: true,
	})
}
```

**Model:**
```go
// internal/model/[entity].go
package model

// Add field to existing struct or create new:
type [Entity] struct {
	ID        uint   `gorm:"primaryKey"`
	// TODO: Add fields from PRD
	FieldName string `gorm:"size:255"` // From PRD: [description]
	CreatedAt time.Time
	UpdatedAt time.Time
}
```

**Migration:**
```sql
-- migrations/YYYYMMDD_[description].up.sql
-- From PRD: [description]
ALTER TABLE [table_name] ADD COLUMN [field_name] VARCHAR(255);

-- migrations/YYYYMMDD_[description].down.sql
ALTER TABLE [table_name] DROP COLUMN [field_name];
```

**Test:**
```go
// internal/handler/[feature]/[action]_test.go
package [feature]

import (
	"testing"
	"net/http/httptest"
	"github.com/stretchr/testify/assert"
)

func TestHandler_[ActionName](t *testing.T) {
	t.Run("Happy Path", func(t *testing.T) {
		// TODO: Implement test from PRD scenarios
	})

	t.Run("Edge Cases", func(t *testing.T) {
		// TODO: Implement edge case tests from PRD
	})
}
```

---

### Python (FastAPI)

**Endpoint:**
```python
# app/api/v2/[feature]/[action].py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

class [ActionName]Request(BaseModel):
    """From PRD: [description]"""
    field_name: str
    # TODO: Add fields from PRD

class [ActionName]Response(BaseModel):
    success: bool
    # TODO: Add fields from PRD

@router.[method]("/[path]")
async def [action_name](request: [ActionName]Request) -> [ActionName]Response:
    """
    [Description from PRD]
    
    Validation rules:
    - [rule 1]
    - [rule 2]
    """
    # TODO: Implement validation
    
    # TODO: Implement business logic
    # Business logic from PRD:
    # - [logic 1]
    # - [logic 2]
    
    return [ActionName]Response(success=True)
```

**Model:**
```python
# app/models/[entity].py
from sqlalchemy import Column, String, Boolean

# Add to existing model or create new:
class [Entity](Base):
    __tablename__ = "[table_name]"
    
    id = Column(Integer, primary_key=True)
    # TODO: Add fields from PRD
    field_name = Column(String(255), nullable=True)  # From PRD: [description]
```

**Migration:**
```python
# migrations/versions/YYYYMMDD_[description].py
"""[Description from PRD]"""

from alembic import op
import sqlalchemy as sa

revision = '[revision_id]'
down_revision = '[previous_revision]'

def upgrade():
    # From PRD: [description]
    op.add_column('[table_name]', sa.Column('[field_name]', sa.String(255), nullable=True))

def downgrade():
    op.drop_column('[table_name]', '[field_name]')
```

**Test:**
```python
# tests/test_[feature]_[action].py
import pytest
from fastapi.testclient import TestClient

class Test[ActionName]:
    """Tests from PRD scenarios"""
    
    def test_happy_path(self, client: TestClient):
        """Should [scenario 1 from PRD]"""
        response = client.[method]("/v2/[path]", json={
            # TODO: Input from PRD
        })
        assert response.status_code == 200
        # TODO: Add assertions
    
    def test_edge_case(self, client: TestClient):
        """Should handle [edge case from PRD]"""
        # TODO: Implement
        pass
```

---

## Directory Creation

Before scaffolding, ensure directories exist:

```bash
# Node.js
mkdir -p app/controllers/v2/[feature]
mkdir -p tests/[feature]

# Go
mkdir -p internal/handler/[feature]
mkdir -p internal/model
mkdir -p migrations

# Python
mkdir -p app/api/v2/[feature]
mkdir -p app/models
mkdir -p migrations/versions
mkdir -p tests
```

---

## Post-Scaffold Checklist

After scaffolding, remind user:

```markdown
## ✅ Files Scaffolded

Created:
- `app/controllers/v2/[feature]/[action].js`
- `migrations/YYYYMMDD-[description].js`
- `tests/[feature]/[action].test.js`

Modified:
- `app/routes/v2/index.js` — Added route registration

## Next Steps
1. [ ] Review generated files for accuracy
2. [ ] Fill in TODO sections
3. [ ] Run migration: `npm run migrate`
4. [ ] Run tests: `npm test`
5. [ ] Implement business logic
```

---

## Conflict Handling

If file exists:

```markdown
## ⚠️ Conflict Detected

The following files already exist:
- `app/controllers/v2/pin/create.js`

Options:
1. **Skip** — Don't create, show diff of changes needed
2. **Create .new** — Create as `create.js.new` for manual merge
3. **Backup & Replace** — Move existing to `.bak` and create new

Which would you prefer?
```
