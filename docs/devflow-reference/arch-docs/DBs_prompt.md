version=1
You are an expert database architect and code analyzer. Your task is to analyze a given codebase (which will be provided to you) and extract detailed documentation for all databases used, including both SQL and NoSQL types.

**Special Instruction:** If, after a comprehensive scan, you determine that the codebase does not interact with any database (SQL or NoSQL), simply return the text: "no database".

**Special Instruction:** ignore any files under 'arch-docs' folder.

For each database identified, please provide the following information in a clear, structured format:

Database Name/Type: The specific name of the database technology (e.g., PostgreSQL, MySQL, MongoDB, Redis, DynamoDB, Cassandra, SQLite).

Purpose/Role: A concise explanation of what kind of data this database stores and its primary role within the system (e.g., "Stores user profiles and authentication data", "Used for caching frequently accessed data", "Persists event streams for analytics").

Key Technologies/Access Methods: Describe how the code interacts with this database. This could include ORMs (e.g., SQLAlchemy, Hibernate, Mongoose), direct SQL queries, specific SDKs (e.g., AWS SDK for DynamoDB), or client libraries.

Key Files/Configuration: Identify the most important files, directories, or configuration settings within the codebase that relate to this database (e.g., database connection strings, schema definitions, migration scripts, ORM models).

Schema/Table Structure (for SQL) / Collection Structure (for NoSQL):

For SQL databases: Provide a high-level overview of the most important tables, their key columns, and primary/foreign keys. You can use a simplified schema representation or a list of tables with their main attributes.

For NoSQL databases: Describe the structure of key collections/documents, including important fields and nested structures.

Key Entities and Relationships: Identify the main entities stored in this database and describe their relationships (e.g., "One-to-many relationship between Users and Orders", "Products are embedded within Order documents").

Interacting Components: List the main components (as identified in a component analysis) that directly interact with this database (e.g., "User Authentication Service", "Product Catalog Module", "Order Processing Service").

Instructions for Analysis:

Comprehensive Scan: Look for all instances of database connections, queries, ORM definitions, data persistence logic, schema definitions, and migration scripts.

Differentiate Types: Clearly distinguish between relational (SQL) and non-relational (NoSQL) databases and their specific types.

Infer Usage: Based on the code, infer the purpose and role of each database if not explicitly documented.

Schema Extraction: Pay close attention to ORM models (e.g., Django models, SQLAlchemy models, Mongoose schemas), raw SQL CREATE TABLE statements, and data insertion/retrieval patterns to infer schema and entity relationships.

Clarity and Detail: Provide clear, concise descriptions, but include enough detail to understand the database's function, how it's accessed, and its data model.

Example Output Format for a single Database:

---
### Database: PostgreSQL

* **Database Name/Type:** PostgreSQL (SQL)
* **Purpose/Role:** Primary transactional database for the application. Stores core business data such as user accounts, product details, orders, and inventory. Ensures data integrity and supports complex queries.
* **Key Technologies/Access Methods:** Python, SQLAlchemy ORM for model definitions and CRUD operations; raw SQL queries for complex reporting.
* **Key Files/Configuration:**
    * `config/database.py` (connection settings)
    * `src/models/` (SQLAlchemy models for User, Product, Order)
    * `migrations/` (Alembic migration scripts)
* **Schema/Table Structure:**
    * `users` table: `id` (PK), `username`, `email`, `password_hash`, `created_at`
    * `products` table: `id` (PK), `name`, `description`, `price`, `stock_quantity`
    * `orders` table: `id` (PK), `user_id` (FK to `users.id`), `order_date`, `total_amount`, `status`
    * `order_items` table: `id` (PK), `order_id` (FK to `orders.id`), `product_id` (FK to `products.id`), `quantity`, `price_at_purchase`
* **Key Entities and Relationships:**
    * **User:** Represents an application user.
    * **Product:** Represents an item available for sale.
    * **Order:** Represents a customer's purchase.
    * **Order Item:** Represents a specific product within an order.
    * **Relationships:** `User` (1) -- `Orders` (M); `Product` (1) -- `Order Items` (M); `Order` (1) -- `Order Items` (M).
* **Interacting Components:**
    * User Authentication Service
    * Product Catalog Module
    * Order Processing Service
    * Reporting Service

---
### Database: Redis

* **Database Name/Type:** Redis (NoSQL - Key-Value Store)
* **Purpose/Role:** Used as an in-memory data store for caching frequently accessed data (e.g., session tokens, product prices), rate limiting, and managing real-time data like leaderboards.
* **Key Technologies/Access Methods:** Node.js, `ioredis` client library.
* **Key Files/Configuration:**
    * `config/redis.js` (connection settings)
    * `src/cache/` (caching utility functions)
    * `src/sessions/` (session store configuration)
* **Schema/Table Structure (for NoSQL):**
    * `sessions:{sessionId}`: Stores user session data (e.g., `userId`, `lastActivity`, `roles`).
    * `cache:product:{productId}`: Stores cached product details (e.g., `name`, `price`, `description`).
    * `rate_limit:{ipAddress}`: Stores counters for API rate limiting.
* **Key Entities and Relationships:**
    * **Session:** Represents an active user session.
    * **Cached Product:** A temporary representation of product data.
    * **Rate Limit Counter:** Tracks API requests per IP.
    * **Relationships:** Primarily key-value lookups; relationships are managed at the application layer rather than within Redis itself.
* **Interacting Components:**
    * User Authentication Service (for session management)
    * Product Catalog Module (for product caching)
    * API Gateway (for rate limiting)
---

Please provide the database analysis for the provided codebase, following the format above for each database.
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
