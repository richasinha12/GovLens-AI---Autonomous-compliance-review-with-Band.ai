# GovLens AI — Autonomous Compliance Swarm

A hackathon demo app for autonomous compliance review using a multi-agent workflow powered by **Band.ai** orchestration.

**Status:** Submission-ready with real Band.ai integration.

---

## 📋 For Hackathon Submission

See [SUBMISSION.md](./SUBMISSION.md) for:
- **GitHub Repository setup** (public repo required)
- **Deployment instructions** (Streamlit Cloud, Replit, or Vercel)
- **Live application URL** (public demo for judges)
- **Submission checklist & troubleshooting**

---

## Run locally

1. Install dependencies:

```powershell
pip install -r requirements.txt
```

2. Start the Streamlit UI:

```powershell
streamlit run main.py
```

3. Open the browser at the URL shown by Streamlit.

## Real Band.ai SDK integration (optional)

The official Band.ai SDK currently works best on Python 3.10 or 3.11.
If you want real Band integration, install the SDK requirements in a supported environment:

```powershell
python -m pip install -r requirements-sdk.txt
```

Then set these environment variables in `.env`:

```powershell
BAND_API_KEY=your_band_api_key
BAND_AGENT_ID=your_agent_uuid
BAND_ROOM_ID=your_room_id
BAND_TARGET_AGENT_HANDLE=agent-shredder
```

Also create an `agent_config.yaml` file for the agent runtime, or use `BAND_API_KEY` / `BAND_AGENT_ID` directly with `band_sdk_real.py`.

And run the real SDK example:

```powershell
python band_sdk_real.py
```

### Run with Docker (recommended for hackathon)

If installing SDK deps locally is difficult, run the app and agent inside a Python 3.10 container. This provides a reproducible environment for judges.

1. Build and start services:

```powershell
docker-compose up --build
```

2. Open the Streamlit UI at `http://localhost:8501` and the agent will connect inside the container.

3. Provide `BAND_API_KEY`, `BAND_AGENT_ID`, and optional `BAND_ROOM_ID` / `BAND_TARGET_AGENT_HANDLE` to Docker by creating a `.env` file or exporting them in your shell before running `docker-compose`.


## Notes

- `main.py` launches the Streamlit demo interface and sends a real Band chat message via the official Band REST client.
- `band_sdk_real.py` runs a remote Band agent using the `band` SDK and LangGraph adapter.
- `app.py` is a local stubbed room simulator that can be used for offline testing without a Band account.
- Replace `.env` values for `BAND_API_KEY`, `BAND_AGENT_ID`, `BAND_ROOM_ID`, and `FEATHERLESS_API_KEY` if you want real API integration.
