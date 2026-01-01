# Baseline Test Scenarios for AI Code Detection

## Purpose
Run these scenarios WITHOUT the skill to establish baseline behavior.
Document what agents miss and how they reason.

---

## Scenario 1: Code with Obvious AI Signals

**Prompt:**
```
IMPORTANT: This is a real scenario. Analyze and give your assessment.

You've been asked to audit this TypeScript file and determine if it was written by AI.
Review carefully and provide your verdict with evidence.

--- FILE: src/utils/userValidation.ts ---

/**
 * This file contains utility functions for validating user input.
 * These functions help ensure data integrity and security.
 */

/**
 * Validates an email address using a comprehensive regex pattern.
 * This function checks if the provided email string matches the standard
 * email format including support for subdomains and various TLDs.
 *
 * @param email - The email address string to validate
 * @returns True if the email is valid, false otherwise
 * @example
 * validateEmail('user@example.com') // returns true
 * validateEmail('invalid-email') // returns false
 */
export function validateEmail(email: string): boolean {
  // First, we check if the email parameter is defined and not empty
  if (!email || typeof email !== 'string') {
    return false;
  }

  // Here we define a comprehensive regex pattern for email validation
  const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

  // Now we test the email against our regex pattern
  return emailRegex.test(email.trim());
}

/**
 * Validates a password to ensure it meets security requirements.
 * This function checks for minimum length, uppercase letters,
 * lowercase letters, numbers, and special characters.
 *
 * @param password - The password string to validate
 * @returns An object containing validity status and any error messages
 */
export function validatePassword(password: string): {
  isValid: boolean;
  errors: string[]
} {
  // Initialize an array to collect any validation errors
  const errors: string[] = [];

  // Check if password meets minimum length requirement
  if (!password || password.length < 8) {
    errors.push('Password must be at least 8 characters long');
  }

  // Check for at least one uppercase letter
  if (!/[A-Z]/.test(password)) {
    errors.push('Password must contain at least one uppercase letter');
  }

  // Check for at least one lowercase letter
  if (!/[a-z]/.test(password)) {
    errors.push('Password must contain at least one lowercase letter');
  }

  // Check for at least one number
  if (!/[0-9]/.test(password)) {
    errors.push('Password must contain at least one number');
  }

  // Check for at least one special character
  if (!/[!@#$%^&*(),.?":{}|<>]/.test(password)) {
    errors.push('Password must contain at least one special character');
  }

  // Return the validation result
  return {
    isValid: errors.length === 0,
    errors
  };
}

--- END FILE ---

Was this written by AI? Provide your verdict and evidence.
```

**Expected AI Signals Present:**
- Excessive JSDoc comments explaining obvious code
- "This function...", "Here we...", "Now we..." comment patterns
- Comments that restate what code already says
- Perfect grammar, no typos
- Over-documented for simple validation functions
- Generic but overly descriptive style

---

## Scenario 2: Mixed Signals (AI-Assisted)

**Prompt:**
```
IMPORTANT: This is a real scenario. Analyze and give your assessment.

Audit this file for AI involvement. This is from a contractor's submission.

--- FILE: src/api/payments.js ---

const stripe = require('stripe')(process.env.STRIPE_KEY);
const { db } = require('../db');

// TODO: add rate limiting
// FIXME: handle currency conversion for intl users

async function processPayment(userId, amt, currency = 'usd') {
  // Quick validation - prod will have proper checks
  if (!userId || amt <= 0) throw new Error('bad input');

  const user = await db.users.findById(userId);
  if (!user) throw new Error('user not found');

  /**
   * Creates a payment intent with the Stripe API.
   * This function handles the creation of a new payment intent
   * which is used to collect payment from the customer.
   *
   * @param amount - The payment amount in cents
   * @param currency - The three-letter ISO currency code
   * @returns The created PaymentIntent object
   */
  const intent = await stripe.paymentIntents.create({
    amount: Math.round(amt * 100),
    currency,
    customer: user.stripeId,
    metadata: { userId, source: 'api' }
  });

  // log for debugging - remove before merge
  console.log('intent created:', intent.id);

  return { intentId: intent.id, clientSecret: intent.client_secret };
}

// grabbed from SO, seems to work
function formatCurrency(amount, curr) {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: curr
  }).format(amount);
}

module.exports = { processPayment, formatCurrency };

--- END FILE ---

--- GIT LOG (last 5 commits) ---
abc123 - Add payment processing with Stripe integration
def456 - fix typo in readme
ghi789 - Add comprehensive JSDoc documentation to payment functions
jkl012 - initial payment setup
mno345 - WIP: payments
--- END GIT LOG ---

What's your assessment? Was AI involved? If so, how?
```

**Expected AI Signals Present:**
- Sudden JSDoc block in otherwise casual code
- Mixed comment styles (casual vs formal)
- Git history shows documentation added separately

**Expected Human Signals Present:**
- TODO/FIXME comments
- Casual shortcuts ("amt", "curr", "intl")
- Debug console.log left in
- "grabbed from SO" comment
- Inconsistent style

---

## Scenario 3: Clean Human Code (False Positive Test)

**Prompt:**
```
IMPORTANT: This is a real scenario. Analyze and give your assessment.

A senior developer at your company is being accused of using AI to write their code.
HR has asked you to audit their recent submission. Be thorough.

--- FILE: src/core/EventEmitter.ts ---

type EventHandler<T = unknown> = (data: T) => void;

interface EventMap {
  [event: string]: EventHandler[];
}

export class EventEmitter {
  private events: EventMap = {};

  on<T>(event: string, handler: EventHandler<T>): () => void {
    if (!this.events[event]) {
      this.events[event] = [];
    }
    this.events[event].push(handler as EventHandler);
    return () => this.off(event, handler);
  }

  off<T>(event: string, handler: EventHandler<T>): void {
    const handlers = this.events[event];
    if (!handlers) return;
    const idx = handlers.indexOf(handler as EventHandler);
    if (idx !== -1) handlers.splice(idx, 1);
  }

  emit<T>(event: string, data: T): void {
    const handlers = this.events[event];
    if (!handlers) return;
    handlers.forEach(h => h(data));
  }

  once<T>(event: string, handler: EventHandler<T>): () => void {
    const wrapper: EventHandler<T> = (data) => {
      this.off(event, wrapper);
      handler(data);
    };
    return this.on(event, wrapper);
  }
}

--- END FILE ---

--- DEVELOPER CONTEXT ---
- 12 years experience
- Known for clean, minimal code style
- Has published similar patterns in blog posts
- Uses TypeScript daily
--- END CONTEXT ---

Is this AI-generated? How do you distinguish from a skilled human developer?
```

**Expected Assessment:**
- Should NOT flag as AI
- Clean code ≠ AI code
- Lack of excessive comments is human signal
- Pragmatic approach (no over-engineering)
- Consistent personal style

---

## Scenario 4: README and Commit Pattern Analysis

**Prompt:**
```
IMPORTANT: This is a real scenario. Analyze and give your assessment.

Review this project's metadata for AI involvement.

--- README.md ---
# User Authentication Service

## Overview

This service provides a comprehensive authentication solution for modern web applications. It handles user registration, login, session management, and password recovery with industry-standard security practices.

## Features

- Secure user registration with email verification
- JWT-based authentication with refresh tokens
- Password hashing using bcrypt
- Rate limiting to prevent brute force attacks
- Session management with Redis
- OAuth2 integration (Google, GitHub)

## Installation

```bash
npm install
cp .env.example .env
npm run migrate
npm start
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| /auth/register | POST | Register a new user |
| /auth/login | POST | Authenticate user |
| /auth/logout | POST | End user session |
| /auth/refresh | POST | Refresh access token |
| /auth/forgot-password | POST | Request password reset |

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| DATABASE_URL | PostgreSQL connection string | Yes |
| JWT_SECRET | Secret for signing tokens | Yes |
| REDIS_URL | Redis connection for sessions | Yes |

## Contributing

Contributions are welcome! Please read our contributing guidelines first.

## License

MIT

--- END README ---

--- RECENT COMMITS ---
a1b2c3 - Add user authentication with JWT tokens
d4e5f6 - Add password recovery functionality
g7h8i9 - Add OAuth2 integration for Google and GitHub
j0k1l2 - Add rate limiting middleware
m3n4o5 - Add session management with Redis
p6q7r8 - Add comprehensive API documentation
--- END COMMITS ---

Was this project created with AI assistance? What evidence supports your conclusion?
```

**Expected AI Signals:**
- README follows exact template structure
- Uniform commit message pattern ("Add X")
- Suspiciously complete documentation
- Perfect tables
- No personality in writing

---

## Baseline Documentation Template

After each scenario, document:

```markdown
## Scenario X Results

**Agent Response Summary:**
[What did they conclude?]

**Signals They Caught:**
-
-

**Signals They Missed:**
-
-

**Reasoning Gaps:**
[What systematic approach was missing?]

**Verbatim Quotes:**
> [Exact reasoning that shows gaps]
```
