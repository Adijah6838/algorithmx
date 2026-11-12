# Evaluator — Isolated Submission Execution Service

Standalone sandboxed service that compiles and runs untrusted contestant
code (C++, Python, Java) with enforced resource limits, then reports the
verdict back to the backend.

**Purpose:** protects the main application server from untrusted code.

**Security requirements (from spec §4):**
- Runs **outside** the main backend process
- Hard CPU-time limit per submission
- Hard memory limit per submission
- Hard wall-clock timeout per submission
- Read-only filesystem inside the container
- No network access inside the container
- Non-root user inside the container

> **Status:** 🚧 Not yet implemented — built in Step 5 (after backend auth + problems work).