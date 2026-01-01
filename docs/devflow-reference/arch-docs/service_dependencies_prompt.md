version=4
You are an expert software architect and code analyzer. Your task is to analyze a given codebase (which will be provided to you) and identify all its external dependencies.

Definition of an External Dependency: An "external dependency" in this context refers to any service (internal or external), library, or resource that is not part of the codebase itself but is required for the codebase to function correctly during runtime. These dependencies typically reside outside the immediate project's source code and are often managed via package managers, API calls, or configuration.

Clues to Look For:

1. API Calls: Outgoing HTTP/S requests to external services (e.g., fetch, axios, requests library calls to third-party APIs like payment gateways, mapping services, social media APIs).

2. Event Broker Interactions: Publishing to or consuming from external message queues or event streams (e.g., AWS SQS, Azure Event Hubs, Kafka, Ably, RabbitMQ).

3. Database Connections: Connections to databases that are hosted externally or managed as separate services (e.g., AWS RDS, MongoDB Atlas, Redis Cloud).

4. Cloud Service SDKs: Usage of SDKs for cloud providers (e.g., AWS SDK, Azure SDK, Google Cloud SDK) to interact with their services (S3, Blob Storage, Lambda/Functions, etc.).

5. Package Manager Definitions: Entries in configuration files that list required libraries or modules (e.g., package.json for npm/yarn, requirements.txt for pip, pyproject.toml , pom.xml for Maven, build.gradle for Gradle, Gemfile for Bundler, go.mod for Go modules). 

    **For Python projects specifically**: Thoroughly examine requirements.txt, pyproject.toml, setup.py, setup.cfg, Pipfile, poetry.lock, and any other Python dependency files to identify all external Python packages, their versions, and their purposes in the project.

    **Note**: When looking for dependencies, package names, or library names, perform case-insensitive matching and consider variations with dashes between words (e.g., "new-relic", "data-dog", "express-rate-limit").

6. Configuration Files: Environment variables, .env files, or dedicated configuration files that store URLs, API keys, connection strings, or service endpoints pointing to external resources.

7. External File Storage: Interactions with external file storage services (e.g., S3 buckets, Google Cloud Storage, Azure Blob Storage).

8. Authentication/Authorization Services: Integration with external identity providers (e.g., Auth0, Okta, OAuth providers like Google/Facebook login).

9. Monitoring/Logging Tools: Integrations with external monitoring, logging, or analytics platforms (e.g., Datadog, Splunk, Google Analytics).

10. Container Images/Orchestration: References to base images or external services in Dockerfiles, Kubernetes manifests, or similar deployment configurations.

For each external dependency identified, please provide the following information in a clear, structured format:

Dependency Name: A descriptive name for the external dependency (e.g., "Stripe Payment Gateway", "AWS S3", "PostgreSQL Database", "NPM 'lodash' library").

Type of Dependency: Categorize the dependency (e.g., "Third-party API", "Message Broker", "External Service", "Internal Service", "Library/Framework", "Authentication Service", "Monitoring Tool").

Purpose/Role: A concise explanation of why this dependency is used by the codebase and its primary function (e.g., "Processes credit card payments", "Stores static assets", "Manages user data persistence", "Provides utility functions").

Integration Point/Clues: Describe how the codebase integrates with this dependency. Reference specific files, configuration entries, or code patterns that indicate its usage.

Instructions for Analysis:

Thorough Scan: Examine all relevant files, including source code, configuration files, build scripts, and dependency manifests. WHEN READING depdenency files like package.json, DO NOT READ FILE PARTIALLY. ALWAYS READ THEM FULLY.

Distinguish Internal vs. External: Focus strictly on components outside the codebase itself. Internal modules or services within the same repository are not external dependencies for this analysis.

Infer Usage: If explicit documentation is lacking, infer the dependency's purpose and integration points based on code logic and configuration. but MENTION that is is an ASSUMPTION, and requires further investigation.

Clarity and Detail: Provide clear, concise descriptions, but include enough detail to understand the dependency's nature and its interaction with the codebase.

**Special Instruction:** ignore any files under 'arch-docs' folder.

—

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

## Raw Dependencies from requirement.stxt, package.json etc

-----------

{repo_deps}

-----------


