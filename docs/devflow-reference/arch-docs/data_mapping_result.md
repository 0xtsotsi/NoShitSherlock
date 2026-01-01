Based on my analysis of the repository structure and the nature of the codebase provided, the following data mapping analysis focuses on the internal data flows required to operate this development platform, primarily dealing with local system data, user-defined configurations, and runtime agent processes.

**No Data Processing Detected** for the following common web compliance categories:
*   **No PII Collection:** There are no forms collecting names, emails, or phone numbers.
*   **No Authentication:** The system appears to be a local development tool without centralized user authentication or account management.
*   **No Third-Party Analytics:** No integration with Google Analytics, Segment, or similar trackers.
*   **No Payments:** No financial transaction flows.

**Note:** The system performs extensive file system scanning and process execution. In a local developer tool context, **file paths and project names** serve as the primary "personal" identifiers linking usage to specific user projects.

## Data Flow Overview

### 1. Data Inputs / Collection Points

**A. File System Scanning (Source Code Context)**
*   **Mechanism:** Automated traversal (walking) of local file systems.
*   **Data Types:** File paths, file content (source code), file metadata (permissions, sizes).
*   **Location:** `libs/git-utils/src/`, `apps/server/src/services/context.ts`.

**B. Agent Configuration Inputs**
*   **Mechanism:** User configuration files (e.g., `.claude/settings.json`, `docker-compose.yml`).
*   **Data Types:** API keys (OpenAI, Anthropic), Model preferences, System prompts.
*   **Location:** `apps/server/src/providers/`, `.claude/settings.json`.

**C. Runtime Environment Variables**
*   **Mechanism:** OS-level environment injection.
*   **Data Types:** `PORT`, `NODE_ENV`, API Keys, Database connection strings.
*   **Location:** `.env.example`, `docker-compose.yml`.

**D. User Prompts (Interaction)**
*   **Mechanism:** Command line inputs or API payloads.
*   **Data Types:** Natural language prompts, Code snippets.
*   **Location:** `apps/ui/src/`, `apps/server/src/routes/`.

### 2. Internal Processing

**A. Tokenization & Embedding (Implied by Model Context)**
*   **Processing:** Source code is read, chunked, and prepared for LLM context windows.
*   **Function:** `libs/git-utils` (reading diffs), `apps/server/src/services/context.ts`.
*   **Operation:** Text extraction, diff generation, hashing (for deduplication/caching).

**B. Beads Audit & Logging**
*   **Processing:** The system tracks "interactions" and "issues" within a local database.
*   **Function:** `.beads/interactions.jsonl`, `.beads/issues.jsonl`.
*   **Operation:** JSON serialization, appending to local logs.

**C. Git Operations**
*   **Processing:** Executing git commands to determine repository state.
*   **Function:** `libs/git-utils`.
*   **Operation:** Process spawning (executing `git` binary), parsing stdout/stderr.

**D. Dependency Resolution**
*   **Processing:** Parsing `package.json` and lockfiles.
*   **Function:** `libs/dependency-resolver`.
*   **Operation:** Manifest parsing, tree building.

### 3. Third-Party Processors

**A. LLM Providers (External)**
*   **Services:** OpenAI, Anthropic, other providers defined in `apps/server/src/providers/`.
*   **Data Sent:** User prompts, Source code context (snippets), Configuration data.
*   **Purpose:** Code generation, refactoring, chat responses.
*   **Compliance Risk:** **HIGH**. Source code is sent to external APIs. This constitutes a data leak risk for proprietary codebases.

**B. GitHub Actions (CI/CD)**
*   **Services:** `github/workflows/`.
*   **Data Sent:** Repository status, test results, environment variables configured in secrets.
*   **Purpose:** Automated testing, linting, security auditing.

### 4. Data Outputs / Exports

**A. Code Modifications**
*   **Output:** Modified files on disk.
*   **Mechanism:** Automated patching or writing files via agents.

**B. Local Databases (SQLite/JSONL)**
*   **Output:** `.beads/beads.db`, `.beads/interactions.jsonl`.
*   **Content:** History of agent actions, errors, and state.

**C. Terminal/Standard Output**
*   **Output:** Logs displayed to the user.
*   **Mechanism:** `console.log` streams.

---

## Data Categories

### 1. Personal Identifiers
*   **User Identity:** None detected (No user accounts).
*   **Identifiable Info:** File Paths (e.g., `/Users/[username]/projects/my-app`). These paths reveal usernames and system structure.

### 2. Sensitive Categories
*   **API Keys:** Stored in `.env` or settings. Stored in plaintext unless external secrets management is used (Not detected in code).
*   **Source Code (IP):** Proprietary logic sent to Third-Party LLMs.
*   **System Configuration:** OS versions, Node versions, dependency lists.

### 3. Business Data
*   **Agent Interactions:** Stored in `.beads/interactions.jsonl`.
*   **Issues/Errors:** Stored in `.beads/issues.jsonl`.

---

## Compliance & Security Analysis

### Critical Issues Found

1.  **Source Code Exposure via LLMs (Data Leak Risk)**
    *   **Flow:** `libs/git-utils` -> `Context Manager` -> `LLM Provider API`.
    *   **Issue:** Proprietary source code is sent to external APIs (OpenAI/Anthropic).
    *   **Compliance:** This may violate corporate IP policies. Data retention policies depend on the external provider's terms (e.g., zero-retention APIs must be explicitly configured).
    *   **Mitigation:** Requires configuration check to ensure "zero data retention" settings are active for the provider.

2.  **Insecure Storage of Secrets**
    *   **Flow:** `.env` files / `settings.json`.
    *   **Issue:** API keys are stored in plaintext configuration files.
    *   **Vulnerability:** If this repository is synced to the cloud or shared, secrets are exposed.

3.  **Local Database Exposure (Beads)**
    *   **Flow:** `.beads/beads.db` & `interactions.jsonl`.
    *   **Issue:** Detailed logs of developer activity and potentially snippets of code are stored locally in JSON/DB formats.
    *   **Risk:** If the `.beads/` directory is committed to git (it appears to be `.gitignore`d based on `.beads/.gitignore`), this is a low risk. However, the contents of `interactions.jsonl` should be audited to ensure no sensitive data is logged.

### Privacy Regulations (GDPR/CCPA)
*   **Status:** **N/A (Mostly)**. The system does not collect PII from "Data Subjects" in the traditional sense (Customers/Users).
*   **Employee Monitoring:** If used in a corporate setting, the "Beads" interaction logs and GitHub Actions logs could constitute employee activity monitoring. Consent may be required if this data is reviewed by management.

### Data Subject Rights
*   **Access:** Users can access their data by reading the `.beads/` files and source code.
*   **Erasure:** Users can delete the `.beads/` folder and stop the docker containers to clear local data.
*   **Portability:** Data is stored in JSON/SQLite, which is inherently portable.

---

## Data Inventory Summary

| Data Type | Collection Point | Processing | Storage | Retention | Sensitivity | Compliance |
|-----------|-----------------|-----------|---------|-----------|-------------|------------|
| **Source Code** | File System | Read, Chunk, Embed (implied) | Disk (Git) | Forever (Git History) | **High (IP)** | Data Leak via LLM |
| **API Keys** | `.env` / `settings.json` | Injection to Headers | Plaintext Config | Until Deleted | **Critical (Secret)** | Access Control |
| **User Prompts** | CLI / UI | Text Processing | Logs / LLM Provider | Cached in Logs | Medium (Intent) | IP Leak via LLM |
| **File Paths** | OS / Git Utils | String Manipulation | Logs / DB | Session/Logs | Low (User Info) | Local Privacy |
| **Agent Activity** | Beads Daemon | Serialization | `.beads/beads.db` | Indefinite | Medium | Audit Trail |
| **Git Metadata** | Libs/Git-Utils | Parsing | RAM/Disk | Transient | Low | N/A |

---

## Risk Assessment

### High-Risk Processing
1.  **External LLM Integration:** The core functionality relies on sending local code context to external APIs. This is the highest compliance and security risk.
2.  **Process Execution:** The system spawns child processes (e.g., `git`, `docker`, `npm`). While not a "privacy" risk, it is a security integrity risk (RCE via malicious packages).

### Vulnerabilities
1.  **Log Injection:** If user prompts are logged without sanitization in `interactions.jsonl`, log injection or injection of sensitive secrets into logs is possible.
2.  **Secrets in Git:** `.env.example` provides a template. If a user accidentally commits a real `.env`, secrets are leaked.

---

## Code-Level Findings

### 1. Context Collection & Source Code Exposure
*   **File Location:** `libs/git-utils/src/`, `apps/server/src/services/context.ts` (inferred).
*   **Components:** Git utilities reading diffs and file trees.
*   **Data Fields:** File paths, diff hunks (`+` / `-` lines).
*   **Transformations:** Text is collected into a "context window" or prompt template.
*   **Risk:** This text is sent directly to `https://api.openai.com` (or similar).
*   **Compliance:** Ensure strict filtering of `.env` or `.pem` files before sending to LLM.

### 2. Beads Logging (Local Persistence)
*   **File Location:** `.beads/interactions.jsonl`, `.beads/issues.jsonl`.
*   **Components:** Beads daemon / watcher.
*   **Data Fields:** JSON objects containing timestamps, agent names, and interaction results.
*   **Retention:** Indefinite until manual cleanup.
*   **Security:** The `.beads/.gitignore` is present, which is good. However, ensure these files don't end up in bug reports automatically.

### 3. Dependency Resolution
*   **File Location:** `libs/dependency-resolver/src/`.
*   **Data:** Reads `package.json`.
*   **Processing:** Parses dependencies.
*   **Risk:** Minimal privacy risk, but enumerates software supply chain.

### 4. Environment Configuration
*   **File Location:** `.env`, `docker-compose.yml`.
*   **Data:** Database strings, API Keys.
*   **Issue:** No evidence of HashiCorp Vault or AWS Secrets Manager integration. Secrets management is manual.