# GovLens AI - Hackathon Submission Guide

## 📋 Submission Checklist

This guide covers the three mandatory requirements for hackathon submission:

### 1. Public GitHub Repository

**Steps:**

1. **Create a GitHub Repository:**
   - Go to [github.com/new](https://github.com/new)
   - Repository name: `govlens-ai` (or similar)
   - Description: "Autonomous 4-agent compliance review system powered by Band.ai"
   - Make it **Public** (mandatory for judges)
   - Click "Create repository"

2. **Initialize Local Git & Push Code:**

```powershell
cd C:\Users\DELL\OneDrive\Desktop\GovLensAI
git init
git add .
git commit -m "Initial GovLens AI submission with Band.ai integration"
git branch -M main
git remote add origin https://github.com/<your-username>/govlens-ai.git
git push -u origin main
```

3. **GitHub Repository Checklist:**
   - ✅ Public repository
   - ✅ Descriptive README.md (included)
   - ✅ `.gitignore` (included)
   - ✅ Requirements files: `requirements.txt`, `requirements-sdk.txt`
   - ✅ Source code: `main.py`, `app.py`, `band_sdk_real.py`
   - ✅ Docker support: `Dockerfile`, `docker-compose.yml`
   - ✅ Configuration examples: `agent_config.yaml.example`

---

### 2. Demo Platform & Deployment

#### Option A: Streamlit Cloud (Recommended - Easiest)

1. **Sign up at [streamlit.io](https://streamlit.io/cloud)**
2. **Connect your GitHub repository:**
   - Click "New app"
   - Select your GitHub repo
   - Choose branch: `main`
   - Set main file path: `main.py`
   - Click "Deploy"

3. **Add Secrets in Streamlit Cloud:**
   - In app settings, go to **Secrets**
   - Add:
     ```
     BAND_API_KEY = "your_band_api_key_here"
     BAND_ROOM_ID = "02627b8c-624b-428a-b5a3-18583e19072d"
     BAND_TARGET_AGENT_HANDLE = "agent-shredder"
     FEATHERLESS_API_KEY = "your_featherless_api_key_here"
     ```

4. **Your live app URL:** `https://govlens-ai-<random>.streamlit.app`

#### Option B: Replit (Alternate)

1. Sign up at [replit.com](https://replit.com)
2. Create new Repl from GitHub repo
3. Add `.env` secrets via Replit Secrets panel
4. Run `streamlit run main.py`
5. Your URL: `https://govlens-ai.repl.co` (custom domain optional)

#### Option C: Vercel (For custom domain)

1. Deploy via Vercel + serverless functions
2. Requires more configuration; see Vercel Streamlit docs

---

### 3. Application URL for Judges

After deployment, you will have a **Public Application URL** like:

```
https://govlens-ai-abc123.streamlit.app
```

This URL should be:
- ✅ Publicly accessible (no authentication required)
- ✅ Fully functional (all Band.ai API keys configured)
- ✅ Responsive and tested
- ✅ Included in your submission materials

---

## 📝 Submission Materials Template

When submitting to the hackathon, provide:

```
PROJECT NAME: GovLens AI

GITHUB REPOSITORY:
https://github.com/<your-username>/govlens-ai

LIVE APPLICATION URL:
https://govlens-ai-abc123.streamlit.app

PROJECT DESCRIPTION:
An autonomous 4-agent legal compliance review system powered by Band.ai. 
Agents collaborate in real-time to analyze procurement drafts for regulatory 
compliance, financial risk, and governance standards.

TECHNOLOGIES:
- Python 3.11
- Streamlit (UI)
- Band.ai SDK (multi-agent coordination)
- LangGraph (agent orchestration)
- OpenAI GPT-4o (reasoning)
- Featherless AI (secondary LLM)
```

---

## 🔐 Environment Variables Reference

For judges to test locally or deploy:

**Required for live Band integration:**
```
BAND_API_KEY=<band_agent_api_key>
BAND_AGENT_ID=<band_agent_uuid>
BAND_ROOM_ID=<band_room_id>
BAND_TARGET_AGENT_HANDLE=agent-shredder
```

**Optional (for AI model calls):**
```
OPENAI_API_KEY=<openai_api_key>
FEATHERLESS_API_KEY=<featherless_api_key>
```

See `.env.example` or `agent_config.yaml.example` in the repo.

---

## ✅ Final Verification Checklist

Before submitting:

- [ ] GitHub repo is public and all code is committed
- [ ] README.md is clear and includes setup instructions
- [ ] Streamlit Cloud (or Replit/Vercel) deployment is live
- [ ] Live URL is publicly accessible
- [ ] Environment secrets are configured on the hosting platform
- [ ] App works end-to-end (can send a Band message)
- [ ] Docker build works: `docker-compose up --build`
- [ ] All dependencies are in `requirements.txt` and `requirements-sdk.txt`

---

## 📞 Troubleshooting

**Issue: "ModuleNotFoundError: No module named 'band'"**
- Solution: Streamlit Cloud auto-installs `requirements-sdk.txt`. Verify it's in repo.

**Issue: "BAND_API_KEY not found"**
- Solution: Add secret via Streamlit Cloud settings > Secrets panel

**Issue: "Connection timeout to Band API"**
- Solution: Verify BAND_API_KEY is valid and Band account is active

**Issue: Docker build fails**
- Solution: Ensure `Dockerfile` and `docker-compose.yml` are in repo root

---

## 🚀 Quick Deploy Commands

**Streamlit Cloud:**
```bash
# Just push to GitHub; Streamlit Cloud auto-deploys
git push origin main
```

**Local Testing Before Submit:**
```powershell
pip install -r requirements.txt
streamlit run main.py
```

**Docker Testing:**
```powershell
docker-compose up --build
# Visit http://localhost:8501
```

---

Good luck with your submission! 🎉
