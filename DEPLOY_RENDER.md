# Deploying to Render (automated via GitHub Actions)

This repository includes a GitHub Actions workflow that triggers a deploy to Render when code is pushed to `main`.

Required GitHub Secrets (set these in the repository Settings → Secrets → Actions):
- `RENDER_API_KEY` — create a Service Account API key in your Render account and paste it here.
- `RENDER_SERVICE_ID` — the Render service ID for your web service.

How it works:
- The workflow ` .github/workflows/deploy_render.yml` sends a POST to Render's deploys endpoint.
- After triggering a deploy, it creates a GitHub Issue notifying maintainers that a deploy was started.

To use:
1. Create a Web Service on Render connected to this GitHub repo (or manual service pointing to repo).
2. In GitHub, add the `RENDER_API_KEY` and `RENDER_SERVICE_ID` secrets.
3. Push to `main` or use the `workflow_dispatch` trigger to start a deploy.

Notes:
- I cannot create Render services or add secrets for you — you must create the service and add the API key in your account.
- Once secrets are present, the workflow runs automatically on push and will create an issue indicating the deploy was triggered.
