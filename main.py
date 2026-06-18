import os
import streamlit as st
from dotenv import load_dotenv
from band.client.rest import (
    RestClient,
    ChatMessageRequest,
    ChatMessageRequestMentionsItem,
    DEFAULT_REQUEST_OPTIONS,
)

load_dotenv()

BAND_API_KEY = os.getenv("BAND_API_KEY")
BAND_ROOM_ID = os.getenv("BAND_ROOM_ID", "02627b8c-624b-428a-b5a3-18583e19072d")
TARGET_AGENT_HANDLE = os.getenv("BAND_TARGET_AGENT_HANDLE", "agent-shredder")

st.set_page_config(page_title="GovLens AI", page_icon="🛡️")
st.title("🛡️ GovLens AI — Compliance Swarm Command")
st.write("Submit procurement drafts into an autonomous 4-agent legal war room.")

if not BAND_API_KEY:
    st.error("Missing BAND_API_KEY in environment. Add it to `.env` and restart.")
    st.stop()

client = RestClient(api_key=BAND_API_KEY)


def find_participant(chat_id: str, target_handle: str):
    participants = client.human_api_participants.list_my_chat_participants(
        chat_id=chat_id,
        request_options=DEFAULT_REQUEST_OPTIONS,
    )
    normalized = target_handle.lstrip("@").lower()
    for participant in participants.data:
        if participant.handle and participant.handle.lstrip("@").lower() == normalized:
            return participant
        if participant.name and participant.name.lower() == normalized:
            return participant
    return None


def send_band_message(chat_id: str, recipient_handle: str, content: str):
    recipient = find_participant(chat_id, recipient_handle)
    if recipient is None:
        raise RuntimeError(
            f"Could not find a room participant with handle or name '{recipient_handle}'. "
            "Make sure the agent has been added to the Band room."
        )

    message_request = ChatMessageRequest(
        content=content,
        mentions=[
            ChatMessageRequestMentionsItem(
                id=recipient.id,
                handle=recipient.handle or recipient.name,
                name=recipient.name,
            )
        ],
    )

    client.human_api_messages.send_my_chat_message(
        chat_id=chat_id,
        message=message_request,
        request_options=DEFAULT_REQUEST_OPTIONS,
    )
    return recipient


proposal_draft = st.text_area("Paste Raw RFP/Grant Document Draft Here:", height=150)

if st.button("Deploy Collaborative Swarm"):
    if not proposal_draft:
        st.error("Please insert a draft first.")
    else:
        try:
            recipient = send_band_message(
                chat_id=BAND_ROOM_ID,
                recipient_handle=TARGET_AGENT_HANDLE,
                content=f"@{TARGET_AGENT_HANDLE} START_PROCESS: {proposal_draft}",
            )
            st.success("🔥 Swarm trigger sent to Band!")
            st.info(
                f"Message sent to {recipient.name} ({recipient.handle or recipient.name}) in room {BAND_ROOM_ID}."
            )
            st.write("Watch the Band room or dashboard for agent activity.")
        except Exception as exc:
            st.error(f"Failed to send Band message: {exc}")
