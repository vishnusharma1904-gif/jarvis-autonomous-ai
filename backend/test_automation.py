from core.tools.automation import AutomationTools
from core.tools.communication import CommunicationTools
import time

def test_automation():
    print("🤖 Testing Automation Tools...")
    auto = AutomationTools()
    
    # Test 1: Open Notepad
    print("\n1. Testing App Launch (Notepad)...")
    print(auto.execute("open_app", "notepad"))
    time.sleep(2)
    
    # Test 2: Type Text
    print("\n2. Testing Typing...")
    print(auto.execute("type_text", "Hello from Jarvis Automation Test!"))
    
def test_communication():
    print("\n📧 Testing Communication Tools...")
    comm = CommunicationTools()
    
    # Test 3: Email (Mock)
    print("\n3. Testing Email (Mock)...")
    # We expect an error because env vars are not set, which confirms the tool is trying to run
    print(comm.execute("send_email", "test@example.com|Subject|Body"))

if __name__ == "__main__":
    test_automation()
    test_communication()
