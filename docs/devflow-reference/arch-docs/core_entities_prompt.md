version=1
Act as a software architect and analyst. Your task is to identify the common data entities or domain models. 
Based on these files:
1.  List the common data entities or structures central to this project's domain.
2.  Describe their key attributes/fields.
3.  Describe any apparent relationships between these entities (e.g., one-to-many, many-to-many).

**Special Instruction:** ignore any files under ‘arch-docs’ folder.

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