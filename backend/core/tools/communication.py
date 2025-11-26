import smtplib
try:
    import pywhatkit
    PYWHATKIT_AVAILABLE = True
except ImportError:
    PYWHATKIT_AVAILABLE = False
    print("⚠️  PyWhatKit not available (headless server mode)")

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import datetime
import threading

class CommunicationTools:
    def __init__(self):
        self.email_user = os.getenv("EMAIL_USER")
        self.email_pass = os.getenv("EMAIL_PASS")
        
    def execute(self, tool_name: str, params: str) -> str:
        try:
            if tool_name == "send_email":
                # params format: "to_email|subject|body"
                parts = params.split("|")
                if len(parts) < 3:
                    return "Error: Email format must be 'to_email|subject|body'"
                return self.send_email(parts[0], parts[1], "|".join(parts[2:]))
                
            elif tool_name == "send_whatsapp":
                # params format: "phone_number|message"
                parts = params.split("|")
                if len(parts) < 2:
                    return "Error: WhatsApp format must be 'phone_number|message'"
                return self.send_whatsapp(parts[0], parts[1])
                
            else:
                return f"Unknown communication tool: {tool_name}"
        except Exception as e:
            return f"Communication Error: {str(e)}"

    def send_email(self, to_email: str, subject: str, body: str) -> str:
        if not self.email_user or not self.email_pass:
            return "Error: EMAIL_USER and EMAIL_PASS environment variables not set"
            
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email_user
            msg['To'] = to_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.email_user, self.email_pass)
            text = msg.as_string()
            server.sendmail(self.email_user, to_email, text)
            server.quit()
            return f"Email sent to {to_email}"
        except Exception as e:
            return f"Failed to send email: {str(e)}"

    def send_whatsapp(self, phone_no: str, message: str) -> str:
        if not PYWHATKIT_AVAILABLE:
            return "WhatsApp messaging not available on headless server (PyWhatKit requires GUI)"
        
        try:
            # Run in separate thread to not block
            def send():
                try:
                    print(f"Attempting to send WhatsApp to {phone_no} via PyWhatKit (Fast Mode)")
                    # wait_time=10s (faster load), tab_close=True, close_time=3s
                    pywhatkit.sendwhatmsg_instantly(phone_no, message, 10, True, 3)
                    print(f"✅ WhatsApp message sent to {phone_no}")
                except Exception as e:
                    print(f"PyWhatKit Error: {e}")
            
            threading.Thread(target=send).start()
            return f"Queued WhatsApp message to {phone_no} via PyWhatKit. Please wait ~20 seconds for the browser to open and send."
        except Exception as e:
            return f"Failed to initiate WhatsApp: {str(e)}"
