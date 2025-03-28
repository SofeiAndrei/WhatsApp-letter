import pywhatkit as kit
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
from datetime import datetime

# Step 1: Connect to Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("whatsapp-newsletter-454320-bdc9c73bc6cc.json", scope)
client = gspread.authorize(creds)

# Step 2: Open the Google Sheet
sheet = client.open("WhatsApp-letter").sheet1
data = sheet.get_all_records()

# Convert to DataFrame
df = pd.DataFrame(data)

# Step 3: Set up message and send via WhatsApp
message = "🚀 Hello! This is our latest WhatsApp newsletter update. Stay tuned for more! 4"

failures = []
for index, row in df.iterrows():
    phone_number = row["Telefon"]
    try:
        print(f"Sending message to {phone_number}...")
        kit.sendwhatmsg_instantly(f"+{phone_number}", message, wait_time=10, tab_close=True)
        time.sleep(5)  # Delay to prevent rate limits
    except Exception as e:
        error_message = str(e)
        timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        failures.append({"phone_number": phone_number, "failure_reason": error_message, "timestamp": timestamp})
        print(f"Error sending message to {phone_number}: {error_message}")

# 🔹 STEP 4: Log failures
if failures:
    print(f"\n⚠️ The following {len(failures)} messages failed:")
    for failure in failures:
        print(f"- {failure['phone_number']} at {failure['timestamp']}: {failure['failure_reason']}")
else:
    print("\n✅ All messages sent successfully! 🎉")
