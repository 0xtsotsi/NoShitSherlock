version=1
You are a security architect specializing in authentication. Analyze all authentication mechanisms, identity management, and access control implementations in this codebase.

**Special Instruction**: If no authentication mechanisms are found, return "no authentication mechanisms detected". Only document authentication systems that are ACTUALLY implemented in the codebase. Do NOT list authentication methods, frameworks, or tools that are not present.

## Authentication Methods

1. **Primary Authentication:**
   - Authentication type (JWT, OAuth 2.0, SAML, Basic Auth, API Keys, Session-based)
   - Implementation details
   - Token/session management
   - Multi-factor authentication (MFA/2FA)

2. **Identity Providers:**
   - Local authentication
   - Social login (Google, Facebook, GitHub, Apple)
   - Enterprise SSO (LDAP, Active Directory, Okta)
   - Third-party auth services (Auth0, Firebase Auth, AWS Cognito)

3. **Credentials Management:**
   - Username/password handling
   - Password policies and validation
   - Password hashing algorithms (bcrypt, scrypt, Argon2)
   - Salt generation and storage

## Token Management

1. **Token Generation:**
   - Token creation logic
   - Token signing (algorithms, keys)
   - Token payload structure
   - Token expiration times

2. **Token Storage:**
   - Client-side storage (cookies, localStorage, sessionStorage, keychain)
   - Server-side storage (Redis, database, memory)
   - Secure storage practices
   - Token rotation strategies

3. **Token Validation:**
   - Validation middleware/filters
   - Signature verification
   - Expiration checking
   - Revocation mechanisms

## Session Management

1. **Session Lifecycle:**
   - Session creation
   - Session storage backend
   - Session timeout configuration
   - Session termination

2. **Session Security:**
   - Session ID generation
   - Session fixation prevention
   - Concurrent session handling
   - Session hijacking protection

## Authentication Flow

1. **Login Process:**
   - Login endpoints and handlers
   - Credential validation
   - Success/failure responses
   - Rate limiting and lockout policies

2. **Logout Process:**
   - Logout endpoints
   - Token/session invalidation
   - Cleanup procedures
   - Single sign-out (SSO)

3. **Registration Flow:**
   - User registration endpoints
   - Email/phone verification
   - Account activation
   - Welcome workflows

4. **Password Recovery:**
   - Reset token generation
   - Reset flow implementation
   - Security questions
   - Account recovery options

## Authentication Middleware

1. **Request Authentication:**
   - Authentication filters/guards
   - Header extraction (Authorization, Cookie)
   - Token/session verification
   - Request context enrichment

2. **Route Protection:**
   - Protected route definitions
   - Authentication requirements
   - Redirect logic for unauthenticated users
   - API vs web authentication

## Security Headers & Cookies

1. **Security Headers:**
   - CORS configuration
   - CSP headers
   - X-Frame-Options
   - Strict-Transport-Security

2. **Cookie Security:**
   - HttpOnly flags
   - Secure flags
   - SameSite attributes
   - Cookie encryption

## Biometric & Device Authentication

1. **Biometric Auth:**
   - Fingerprint authentication
   - Face ID/recognition
   - Voice authentication
   - Behavioral biometrics

2. **Device Trust:**
   - Device registration
   - Device fingerprinting
   - Trusted device management
   - Device-based MFA

## API Authentication

1. **API Key Management:**
   - API key generation
   - Key storage and rotation
   - Rate limiting per key
   - Key revocation

2. **Service-to-Service Auth:**
   - mTLS implementation
   - Service accounts
   - Certificate management
   - Inter-service authentication

## OAuth Implementation

1. **OAuth Flows:**
   - Authorization code flow
   - Implicit flow
   - Client credentials flow
   - PKCE implementation

2. **OAuth Configuration:**
   - Client ID/secret management
   - Redirect URI validation
   - Scope definitions
   - Token exchange

## Vulnerabilities & Issues

Identify any authentication vulnerabilities:
- Weak password policies
- Insecure token storage
- Missing rate limiting
- Session fixation risks
- Timing attacks
- Insecure direct object references

For each authentication mechanism found, provide:
- **Location:** Specific files and line numbers
- **Implementation:** How it's implemented
- **Configuration:** Key settings and parameters
- **Security Assessment:** Potential vulnerabilities
- **Issues Identified:** Problems found in current implementation

Format the output clearly using markdown

---

## Repository Structure and Files

Repository: DevFlow_18d08026
============================

  📄 .env.example
  📄 .gitattributes
  📄 .gitignore
  📄 .npmrc
  📄 .prettierignore
  📄 .prettierrc
  📄 AGENTS.md
  📄 BEADS_AUDIT_REPORT.md
  📄 CLAUDE.md
  📄 DISCLAIMER.md
  📄 LICENSE
  📄 PR5_REVIEW_REPORT.md
  📄 QUICK_START_AGENTS.md
  📄 README.md
  📄 SPECIALIZED_AGENTS_SUMMARY.md
  📄 TEST_GENERATION_REPORT.md
  📄 create-pr.sh
  📄 docker-compose.override.yml.example
  📄 docker-compose.yml
  📄 init.mjs
  📄 lint-server-output.txt
  📄 lint-ui-output.txt
  📄 package-lock.json
  📄 package.json
  📄 pr_description.md
  📄 pr_title.txt
  📄 test-network-connectivity.md
  📄 test-output.txt
  📄 test-results.txt
  📄 test-server-results.txt
  📄 typecheck-server-output.txt
  📄 typecheck-ui-output.txt
  📄 vitest.config.ts
  📁 docs/
    📄 HYBRID_ORCHESTRATION_PLAN.md
    📄 checkout-branch-pr.md
    📄 checkpoint-system.md
    📄 clean-code.md
    📄 context-files-pattern.md
    📄 docker-isolation.md
    📄 folder-pattern.md
    📄 llm-shared-packages.md
    📄 migration-plan-nextjs-to-vite.md
    📄 multi-provider-research.md
    📄 pr-comment-fix-agent.md
    📄 pr-comment-fix-prompt.md
    📄 release.md
    📄 terminal.md
    📄 vibe-kanban-mcp-integration.md
    📁 server/
      📄 providers.md
      📄 route-organization.md
      📄 utilities.md
    📁 fixes/
      📄 claude-authentication-cors-fix.md
  📁 .github/
    📄 update-pr-25.sh
    📁 actions/
      📁 setup-project/
        [1 files]
    📁 workflows/
      📄 claude.yml
      📄 e2e-tests.yml
      📄 format-check.yml
      📄 pr-check.yml
      📄 provider-check.yml
      📄 release.yml
      📄 security-audit.yml
      📄 test.yml
    📁 scripts/
      📄 upload-to-r2.js
  📁 test/
    📄 CONFIG_TESTS.md
    📄 README.md
    📄 TEST_SUMMARY.md
    📁 fixtures/
      📁 projectA/
        [1 files]
    📁 config/
      📄 claude-settings.test.ts
      📄 gitignore-validation.test.ts
      📄 readme-validation.test.ts
  📁 .husky/
    📄 pre-commit
  📁 apps/
    📁 server/
      📄 .env.example
      📄 .gitignore
      📄 Dockerfile
      📄 eslint.config.js
      📄 package.json
      📄 pnpm-lock.yaml
      📄 tsconfig.json
      📄 tsconfig.test.json
      📄 vitest.config.ts
      📁 tests/
        📁 fixtures/ [NESTED]
        📁 integration/ [NESTED]
        📁 unit/ [NESTED]
        📁 utils/ [NESTED]
        [1 files]
      📁 src/
        📁 agents/ [NESTED]
        📁 lib/ [NESTED]
        📁 middleware/ [NESTED]
        📁 providers/ [NESTED]
        📁 routes/ [NESTED]
        📁 services/ [NESTED]
        📁 types/ [NESTED]
        [1 files]
    📁 ui/
      📄 .gitignore
      📄 Dockerfile
      📄 components.json
      📄 eslint.config.mjs
      📄 index.html
      📄 nginx.conf
      📄 package.json
      📄 playwright.config.ts
      📄 tsconfig.json
      📄 vite.config.mts
      📁 docs/
        [2 files]
      📁 tests/
        📁 agent/ [NESTED]
        📁 context/ [NESTED]
        📁 features/ [NESTED]
        📁 git/ [NESTED]
        📁 profiles/ [NESTED]
        📁 projects/ [NESTED]
        📁 utils/ [NESTED]
        [1 files]
      📁 public/
        📁 sounds/ [NESTED]
        [10 files]
      📁 scripts/
        [4 files]
      📁 src/
        📁 components/ [NESTED]
        📁 config/ [NESTED]
        📁 contexts/ [NESTED]
        📁 hooks/ [NESTED]
        📁 lib/ [NESTED]
        📁 routes/ [NESTED]
        📁 store/ [NESTED]
        📁 styles/ [NESTED]
        📁 types/ [NESTED]
        📁 utils/ [NESTED]
        [5 files]
    📁 app/
      📁 server-bundle/
        [2 files]
  📁 .claude/
    📄 SETTINGS_GUIDE.md
    📄 settings.json
    📁 plans/
      📄 cheeky-puzzling-dusk.md
    📁 commands/
      📄 commit.md
      📄 fix.md
      📄 update-app.md
  📁 libs/
    📄 tsconfig.base.json
    📁 types/
      📄 README.md
      📄 package.json
      📄 tsconfig.json
      📁 src/
        [15 files]
    📁 dependency-resolver/
      📄 README.md
      📄 package.json
      📄 tsconfig.json
      📄 vitest.config.ts
      📁 tests/
        [1 files]
      📁 src/
        [2 files]
    📁 prompts/
      📄 README.md
      📄 package.json
      📄 tsconfig.json
      📄 vitest.config.ts
      📁 tests/
        [1 files]
      📁 src/
        [2 files]
    📁 model-resolver/
      📄 README.md
      📄 package.json
      📄 tsconfig.json
      📄 vitest.config.ts
      📁 tests/
        [1 files]
      📁 src/
        [2 files]
    📁 utils/
      📄 README.md
      📄 package.json
      📄 tsconfig.json
      📄 vitest.config.ts
      📁 tests/
        [6 files]
      📁 src/
        [9 files]
    📁 platform/
      📄 README.md
      📄 package.json
      📄 tsconfig.json
      📄 vitest.config.ts
      📁 tests/
        [4 files]
      📁 src/
        [6 files]
    📁 git-utils/
      📄 README.md
      📄 package.json
      📄 tsconfig.json
      📄 vitest.config.ts
      📁 tests/
        [1 files]
      📁 src/
        [4 files]
  📁 .beads/
    📄 .gitignore
    📄 .local_version
    📄 README.md
    📄 beads.db
    📄 config.yaml
    📄 daemon.lock
    📄 interactions.jsonl
    📄 issues.jsonl
    📄 metadata.json
    📁 issues/
      📄 claude-auth-cors-fix.md
  📁 scripts/
    📄 check-dependencies.sh
    📄 fix-lockfile-urls.mjs
