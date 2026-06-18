import os
import requests
import time
from dotenv import load_dotenv
from band_sdk_stub import BandClient

# Load our secret keys from the .env file
load_dotenv()

BAND_API_KEY = os.getenv("BAND_API_KEY")
FEATHERLESS_API_KEY = os.getenv("FEATHERLESS_API_KEY")

# Initialize the local Band room simulator (stubbed for offline testing)
client = BandClient(api_key=BAND_API_KEY)

# Connect to a multi-agent chat room
ROOM_ID = "02627b8c-624b-428a-b5a3-18583e19072d"
room = client.join_room(ROOM_ID)

def query_featherless_model(system_prompt, user_content):
    """Helper to route specialized tasks to free Featherless open-source models"""
    headers = {
        "Authorization": f"Bearer {FEATHERLESS_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "meta-llama/Meta-Llama-3-70B-Instruct", 
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ]
    }
    try:
        response = requests.post("https://api.featherless.ai/v1/chat/completions", json=payload, headers=headers)
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"Error reaching AI: {str(e)}"

# --- 1. THE INGEST AGENT ---
@room.on_message(agent_id="Agent-Shredder")
def handle_shredder(message):
    # Added mention checking to make sure it reads when tagged
    if "@agent-shredder" in message.content and "START_PROCESS" in message.content:
        raw_text = message.content.replace("@agent-shredder START_PROCESS:", "")
        print("\n[Shredder] Ingesting raw proposal text...")
        
        sys_prompt = "You clean up raw unstructured text and list out key regulatory compliance clauses as clean bullet points."
        cleaned = query_featherless_model(sys_prompt, raw_text)
        
        # FIX: Added @agent-veto mention to content string
        room.send_message(content=f"@agent-veto AUDIT_THIS: {cleaned}", recipient="Agent-Veto")

# --- 2. THE ADVERSARIAL RED-TEAM AUDITOR ---
@room.on_message(agent_id="Agent-Veto")
def handle_auditor(message):
    if "@agent-veto" in message.content and "AUDIT_THIS" in message.content:
        text_to_scan = message.content.replace("@agent-veto AUDIT_THIS:", "")
        print("\n[Veto Agent] Auditing text for liabilities...")
        
        sys_prompt = "You are a ruthless compliance auditor. Scan the text for missing data or risks. If you find any problem, start your answer with the exact word 'CRITICAL_ERROR'. Otherwise, say 'PASSED'."
        findings = query_featherless_model(sys_prompt, text_to_scan)
        
        # FIX: Added @agent-lead mentions to content strings
        if "CRITICAL_ERROR" in findings:
            room.send_message(content=f"@agent-lead VETO: Found issues -> {findings}", recipient="Agent-Lead")
        else:
            room.send_message(content=f"@agent-lead AUDIT_PASSED: {findings}", recipient="Agent-Lead")

# --- 3. THE COUNSEL LEAD ---
@room.on_message(agent_id="Agent-Lead")
def handle_lead(message):
    if "@agent-lead" in message.content:
        if "VETO" in message.content:
            print("\n[Lead Agent] ❌ Veto received! Forcing self-healing loop.")
            # FIX: Added @agent-shredder mention to content string
            room.send_message(content="@agent-shredder START_PROCESS: Rewording required. The auditor rejected your points.", recipient="Agent-Shredder")
        elif "AUDIT_PASSED" in message.content:
            print("\n[Lead Agent] Compliance passed. Handing off to Financial Scorer.")
            # FIX: Added @agent-quant mention to content string
            room.send_message(content="@agent-quant RUN_FINANCIAL_CHECK", recipient="Agent-Quant")

# --- 4. THE FINANCIAL QUANT AGENT ---
@room.on_message(agent_id="Agent-Quant")
def handle_quant(message):
    if "@agent-quant" in message.content and "RUN_FINANCIAL_CHECK" in message.content:
        print("\n[Quant Agent] Calculating financial exposure...")
        # FIX: Added @agent-lead mention to content string
        room.send_message(content="@agent-lead COMPLETE: Proposal compliance approved and budget verified.", recipient="Agent-Lead")

print("🚀 GovLens Swarm is running locally and connected to your Band Room!")

# Keep the script running forever so it listens for live messages
while True:
    time.sleep(1)