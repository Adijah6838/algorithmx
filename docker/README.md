# Docker — Local Development & Deployment

Docker configuration for the full stack.

**Purpose:** this folder holds:
- `Dockerfile.backend` — image for the FastAPI app
- `Dockerfile.frontend` — image for the built React app
- `Dockerfile.evaluator` — hardened, sandboxed image for running submissions
- `docker-compose.yml` — orchestrates PostgreSQL, backend, frontend, evaluator

> **Status:** 🚧 Not yet implemented — added after backend + evaluator are
> functional so real container images can be built and tested.