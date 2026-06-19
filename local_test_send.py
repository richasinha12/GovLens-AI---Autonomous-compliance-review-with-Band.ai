import sys
from band_sdk_stub import BandClient

ROOM_ID = "02627b8c-624b-428a-b5a3-18583e19072d"

if len(sys.argv) > 1:
    draft = " ".join(sys.argv[1:])
else:
    draft = input("Paste a short proposal draft to send: ")

client = BandClient(api_key=None)
room = client.join_room(ROOM_ID)

content = f"@agent-shredder START_PROCESS: {draft}"
print(f"Sending to room {ROOM_ID}: {content[:80]}...")
room.send_message(content=content, recipient="Agent-Shredder")
print("Sent.")
