version=2
You are a security auditor performing a comprehensive security assessment. Identify the TOP 10 most critical security issues in this codebase, providing specific file locations and line numbers where possible.

**Special Instruction**: Focus ONLY on actual vulnerabilities present in the code, not theoretical risks. Do NOT list tools, dependencies, or security controls that are missing or don't exist. Only document what IS present in the codebase.

## Security Vulnerability Assessment

Analyze the codebase for the following vulnerability categories and report the TOP 10 most critical issues found:

### 1. Authentication & Session Management
- Weak password policies
- Insecure password storage (plain text, weak hashing)
- Session fixation vulnerabilities
- Missing session timeout
- Insecure token storage
- Broken authentication flows

### 2. Authorization & Access Control
- Missing authorization checks
- Privilege escalation paths
- Insecure direct object references (IDOR)
- Path traversal vulnerabilities
- Broken access control on sensitive functions
- Overly permissive CORS policies

### 3. Injection Vulnerabilities
- SQL injection
- NoSQL injection
- Command injection
- LDAP injection
- XPath injection
- Template injection
- Code injection

### 4. Data Exposure
- Hardcoded secrets (API keys, passwords, tokens)
- Sensitive data in logs
- Unencrypted sensitive data storage
- Sensitive data in URLs
- Information disclosure in error messages
- Exposed debug endpoints

### 5. Cryptographic Issues
- Use of weak algorithms (MD5, SHA1, DES)
- Insecure random number generation
- Hardcoded encryption keys
- Missing encryption for sensitive data
- Improper certificate validation
- Weak TLS/SSL configuration

### 6. Input Validation & Output Encoding
- Missing input validation
- Insufficient sanitization
- XSS vulnerabilities
- XXE vulnerabilities
- Deserialization vulnerabilities
- File upload vulnerabilities

### 7. Security Misconfiguration
- Default credentials
- Unnecessary services enabled
- Verbose error messages
- Missing security headers
- Insecure default settings
- Exposed admin interfaces

### 8. Vulnerable Dependencies
- Known vulnerable packages
- Outdated dependencies with security patches
- Unmaintained libraries
- Dependencies with known CVEs
- Insecure dependency configurations
- **For Python projects**: Check requirements.txt, pyproject.toml, setup.py, setup.cfg, Pipfile, and poetry.lock for vulnerable packages and outdated dependencies

**Note**: When looking for dependencies, package names, or library names, perform case-insensitive matching and consider variations with dashes between words (e.g., "new-relic", "data-dog", "express-rate-limit").

### 9. Business Logic Flaws
- Race conditions
- Time-of-check to time-of-use (TOCTOU)
- Insufficient rate limiting
- Missing anti-automation controls
- Improper transaction handling
- Price manipulation vulnerabilities

### 10. API Security
- Missing API authentication
- Excessive data exposure
- Lack of rate limiting
- Missing API versioning
- Broken object level authorization
- Mass assignment vulnerabilities

## Output Format

For each security issue found, provide:

### Issue #[1-10]: [Vulnerability Type]
**Severity:** CRITICAL | HIGH | MEDIUM | LOW
**Category:** [From categories above]
**Location:** 
- File: `path/to/file.ext`
- Line(s): [specific line numbers]
- Function/Class: [if applicable]

**Description:**
[Clear explanation of the vulnerability]

**Vulnerable Code:**
```[language]
// Show the actual vulnerable code snippet
```

**Impact:**
[What an attacker could do with this vulnerability]

**Fix Required:**
[Specific fix needed]

**Example Secure Implementation:**
```[language]
// Show the corrected code
```

---

## Summary

After listing the top 10 issues, provide:

1. **Overall Security Posture:** Brief assessment
2. **Critical Issues Count:** Number of CRITICAL severity findings
3. **Most Concerning Pattern:** Recurring security anti-pattern observed
4. **Priority Fixes:** Top 3 issues to fix immediately
5. **Implementation Issues:** Patterns in the code that need attention

## Additional Security Issues Found

List any other security concerns found in the codebase that didn't make the top 10:
- Configuration vulnerabilities present
- Architecture security flaws identified  
- Development implementation issues
- Insecure coding patterns found

**Note:** If fewer than 10 security issues are found, list only the actual issues discovered and note that the codebase has fewer security concerns than expected.

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
