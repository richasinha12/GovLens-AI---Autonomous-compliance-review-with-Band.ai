# Deploying Band Agent Runtime to Render

This guide walks you through deploying `band_sdk_real.py` as a separate Render worker service so your multi-agent swarm is active in production.

---

## Prerequisites

- Existing Render web service running `main.py` (the Streamlit app)
- Band credentials:
  - `BAND_API_KEY`
  - `BAND_AGENT_ID` (the UUID of the agent you created in Band)
  - OpenAI API key (`OPENAI_API_KEY`) or another LLM key if using a different model in `ChatOpenAI`
- Same GitHub repo with the agent runtime files (`band_sdk_real.py`, `requirements-sdk.txt`, `Dockerfile.agent`)

---

## Step 1: Create a Background Worker Service on Render

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **"New +"** → **"Background Worker"**
3. Fill in the form:
   - **Name:** `govlens-ai-agent` (or any name)
   - **Project:** same project as your web service (optional)
   - **Language:** `Docker`
   - **Repository:** `richasinha12/GovLens-AI---Autonomous-compliance-review-with-Band.ai`
   - **Branch:** `main`
   - **Dockerfile Path:** `Dockerfile.agent` ← **Important: specify this path**
   - **Instance Type:** Starter or Standard (depending on your LLM usage)
   - **Region:** same as your web service (e.g., Oregon)

4. Click **"Create Background Worker"**

---

## Step 2: Add Environment Variables

1. Go to the newly created worker service → **Settings** → **Environment**
2. Add these environment variables:
   - `BAND_API_KEY` = your Band API key
   - `BAND_AGENT_ID` = your Band agent UUID (from Band platform)
   - `OPENAI_API_KEY` = your OpenAI API key (if using GPT models)

3. Click **"Save Changes"**
4. The service will restart with the new env vars

---

## Step 3: Deploy the Agent Worker

The worker will auto-deploy once created. Watch the **Logs** tab to confirm it starts without errors.

Expected startup log:
```
Agent is running! Press Ctrl+C to stop.
```

If you see errors, check:
- `BAND_API_KEY` and `BAND_AGENT_ID` are correct (copy-paste from Band)
- `OPENAI_API_KEY` is valid
- The `Dockerfile.agent` path is correct in the Render service settings

---

## How It Works

- The agent worker runs `band_sdk_real.py` continuously in the background.
- It uses `LangGraphAdapter` + `ChatOpenAI` to process incoming Band messages.
- When your Streamlit app sends a message to the Band room with `@agent-shredder START_PROCESS`, the agent runtime (running in this worker) will:
  1. Receive the message via Band SDK
  2. Process it through the LangGraph agent
  3. Send responses back to the Band room
  4. Continue the conversation with other agents in the room

---

## Local Testing (Before Render Deploy)

To test the agent locally before deploying to Render:

```bash
# Install dependencies
pip install -r requirements-sdk.txt

# Set env vars
export BAND_API_KEY="your_band_key"
export BAND_AGENT_ID="your_agent_id"
export OPENAI_API_KEY="your_openai_key"

# Run the agent
python band_sdk_real.py
```

You should see:
```
Agent is running! Press Ctrl+C to stop.
```

Then test by sending a message from the Streamlit app to the Band room. The agent should process it.

---

## Monitoring

- **Logs:** Go to the worker service → **Logs** tab to watch real-time activity
- **Metrics:** Check CPU/memory usage in the service dashboard
- **Cost:** Background workers have lower rates than web services; adjust instance type if needed

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `Agent is running` but no responses in Band | Check BAND_AGENT_ID is correct; ensure agent is added to the Band room |
| Import errors (band, langgraph) | Verify `Dockerfile.agent` uses Python 3.11 and installs `requirements-sdk.txt` |
| `OPENAI_API_KEY` missing | Add to Render service Environment variables |
| Worker keeps crashing | Check logs; ensure Band room exists and agent credentials are valid |

---

## Next Steps

Once the agent worker is running and responding in Band:
- Open the Streamlit app at your web service URL
- Paste a compliance draft and click "Deploy Collaborative Swarm"
- Watch the Band room for the full multi-agent conversation
- Judges will see both the Streamlit UI and the live Band chat activity

---

## Optional: Automate with GitHub Actions

If you want the agent worker to auto-deploy on push to `main`, add a GitHub Actions workflow (similar to the web service workflow in `.github/workflows/deploy_render.yml`). This will trigger a redeploy whenever you push code changes.
