version=1
You are a data privacy and compliance expert tasked with creating a comprehensive data mapping analysis. Analyze how data, especially personal information, flows through this system from collection to storage, processing, and sharing.

**Special Instruction**: Focus on identifying personal data, sensitive information, and compliance-relevant data flows. If no data processing is found, return "no data processing detected". Only document data processing mechanisms that are ACTUALLY implemented in the codebase. Do NOT list data protection tools, compliance frameworks, or privacy technologies that are not present.

## Data Flow Overview

Create a high-level map of data movement through the system:

1. **Data Inputs/Collection Points:**
   - Web forms and user interfaces
   - API endpoints receiving data
   - File uploads and imports
   - Third-party data sources
   - Automated data collection (tracking, analytics)
   - Background jobs fetching data

2. **Internal Processing:**
   - Data transformation and enrichment
   - Validation and cleansing
   - Aggregation and analysis
   - Machine learning/AI processing
   - Caching and temporary storage

3. **Third-Party Processors:**
   - External API calls sending data
   - Cloud service integrations
   - Analytics and monitoring services
   - Payment processors
   - Communication services (email, SMS)
   - CDN and storage providers

4. **Data Outputs/Exports:**
   - API responses
   - Reports and downloads
   - Data synchronization
   - Backups and archives
   - Third-party integrations

## Data Categories

For each data flow identified, document:

### 1. Type of Data/Personal Information

**Personal Identifiers:**
- Names (first, last, full)
- Email addresses
- Phone numbers
- Physical addresses
- IP addresses
- Device identifiers
- User IDs and usernames
- Session identifiers

**Sensitive Categories:**
- Financial data (credit cards, bank accounts, transactions)
- Health information (medical records, conditions, treatments)
- Biometric data (fingerprints, face recognition, voice)
- Government IDs (SSN, passport, driver's license)
- Authentication credentials (passwords, tokens, API keys)
- Location data (GPS, geolocation)
- Children's data (COPPA compliance)

**Business Data:**
- Transaction records
- Customer interactions
- Usage analytics
- Performance metrics
- Audit logs
- Metadata

### 2. Data Activity

For each data processing point, identify:

**Collection Methods:**
- Direct user input
- Automated collection
- Third-party import
- System-generated
- Derived/computed

**Processing Operations:**
- Validation and verification
- Encryption/decryption
- Hashing and tokenization
- Pseudonymization/anonymization
- Aggregation and summarization
- Enrichment and augmentation
- Deduplication
- Format conversion
- Compression

**Data Transformations:**
- Parsing and extraction
- Normalization
- Categorization
- Scoring and ranking
- Machine learning inference

### 3. Purpose of Collection/Processing

Document the business justification for each data activity:

**Primary Purposes:**
- Service delivery (core functionality)
- User authentication and authorization
- Payment processing
- Customer support
- Legal compliance
- Security and fraud prevention
- Performance monitoring

**Secondary Purposes:**
- Analytics and insights
- Marketing and personalization
- Product improvement
- Research and development
- Business intelligence
- Quality assurance

### 4. Data Location & Retention

**Storage Locations:**
- Database systems (specify type and instance)
- File systems (local, network, cloud)
- Cache layers (Redis, Memcached)
- Message queues
- Cloud storage services (S3, Azure Blob, GCS)
- Third-party systems
- Backup locations
- Archive systems

**Retention Policies:**
- Active retention period
- Archive period
- Deletion schedule
- Legal hold requirements
- Regulatory requirements (GDPR, HIPAA, etc.)
- Business requirements
- Technical constraints

## Compliance Considerations

### Privacy Regulations
- **GDPR:** Identify EU personal data processing
- **CCPA/CPRA:** California resident data
- **HIPAA:** Health information handling
- **PCI DSS:** Payment card data
- **COPPA:** Children's data
- **Industry-specific:** Financial (SOX), Education (FERPA)

### Data Subject Rights
- **Access:** How users can view their data
- **Rectification:** Update/correct mechanisms
- **Erasure:** Delete/forget procedures
- **Portability:** Export capabilities
- **Restriction:** Processing limitations
- **Objection:** Opt-out mechanisms

### Cross-Border Transfers
- International data flows
- Data localization requirements
- Transfer mechanisms (SCCs, adequacy decisions)
- Third-party processor locations

## Security Controls

### Data Protection
- Encryption at rest
- Encryption in transit
- Access controls
- Audit logging
- Data masking/redaction
- Secure deletion

### Data Breach Risks
- Vulnerable data exposure points
- Unencrypted transmissions
- Inadequate access controls
- Missing audit trails
- Third-party risks

## Third-Party Data Sharing

### Data Processors
For each third-party processor:
- **Name/Service:** Identity of processor
- **Data Shared:** Types of data sent
- **Purpose:** Why data is shared
- **Location:** Geographic location
- **Security:** Contractual safeguards
- **Retention:** How long they keep data

### Data Controllers
- Joint controller relationships
- Independent controller transfers
- Consent requirements
- Legal basis for sharing

## Data Inventory Summary

Provide a structured inventory:

| Data Type | Collection Point | Processing | Storage | Retention | Sensitivity | Compliance |
|-----------|-----------------|-----------|---------|-----------|-------------|------------|
| [Example] | [Where collected] | [How processed] | [Where stored] | [How long] | [Level] | [Requirements] |

## Risk Assessment

### High-Risk Processing
- Large-scale personal data processing
- Sensitive data categories
- Systematic monitoring
- Automated decision-making
- Children's data
- Cross-border transfers

### Vulnerabilities
- Unencrypted data storage
- Excessive data collection
- Missing consent mechanisms
- Inadequate retention policies
- Third-party dependencies
- Access control gaps

## Current State Analysis

### Critical Issues Found
- Compliance gaps identified in implementation
- Security vulnerabilities discovered
- Documentation issues found
- Consent implementation problems

### Implementation Issues Identified
- Privacy implementation weaknesses
- Data handling problems found
- Security implementation gaps
- Process automation issues
- Documentation problems identified

## Code-Level Findings

For each significant data flow, provide:
- **File Location:** Specific files handling the data
- **Functions/Classes:** Code components involved
- **Data Fields:** Exact field names and types
- **Transformations:** Specific operations performed
- **Validation:** Input validation and sanitization
- **Error Handling:** How failures are managed

Format the output clearly using markdown, creating a comprehensive data map that can be used for compliance, security reviews, and operational understanding.

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
