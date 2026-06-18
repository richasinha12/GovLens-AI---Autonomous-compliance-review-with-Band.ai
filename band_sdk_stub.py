import threading
import time
import queue

class Message:
    def __init__(self, content, agent_id=None):
        self.content = content
        self.agent_id = agent_id

class Room:
    def __init__(self, room_id):
        self.room_id = room_id
        self.handlers = {}
        self.message_queue = queue.Queue()
        self.polling_thread = threading.Thread(target=self._process_messages, daemon=True)
        self.polling_thread.start()

    def on_message(self, agent_id=None):
        def decorator(fn):
            self.handlers[agent_id] = fn
            return fn
        return decorator

    def send_message(self, content, recipient=None):
        print(f"📤 → {recipient}: {content[:60]}...")
        # Simulate message routing to handler
        if recipient in self.handlers:
            self.message_queue.put((recipient, content))

    def _process_messages(self):
        while True:
            try:
                recipient, content = self.message_queue.get(timeout=1)
                if recipient in self.handlers:
                    message = Message(content=content, agent_id=recipient)
                    try:
                        self.handlers[recipient](message)
                    except Exception as e:
                        print(f"❌ Handler error: {e}")
            except queue.Empty:
                pass
            except Exception as e:
                print(f"❌ Error: {e}")

class BandClient:
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.rooms = {}

    def join_room(self, room_id):
        if room_id not in self.rooms:
            self.rooms[room_id] = Room(room_id)
        return self.rooms[room_id]
