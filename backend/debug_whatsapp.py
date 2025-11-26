import pywhatkit
import time
import sys

def test_whatsapp():
    print("📱 Testing WhatsApp Automation...")
    phone = "+917711996608" # User's number from logs
    message = "Holaaaa"
    
    print(f"Attempting to send to {phone}...")
    try:
        # wait_time=15s, tab_close=True, close_time=5s
        pywhatkit.sendwhatmsg_instantly(phone, message, 15, True, 5)
        print("✅ pywhatkit function executed successfully")
    except Exception as e:
        print(f"❌ pywhatkit failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_whatsapp()
