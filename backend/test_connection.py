import os
import requests
import urllib3
from dotenv import load_dotenv

# Disable SSL warnings for internal servers
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def test_epicor_connection():
    print("========================================")
    print("   Epicor BAQ Connection Tester         ")
    print("========================================")
    
    # 1. Load Environment Variables
    load_dotenv()
    # Use values from .env, or fallback to your specific server details
    url = os.getenv("EPICOR_API_URL", "https://199.5.83.159/EpicorERP/api/v1")
    user = os.getenv("EPICOR_USERNAME", "WESTS")
    password = os.getenv("EPICOR_PASSWORD")
    company = os.getenv("EPICOR_COMPANY")
    
    # Use BAQ ID from env or default
    baq_id = os.getenv("EPICOR_BAQ_ID", "PO_Test")

    if not url or not user:
        print("❌ Error: Missing credentials in .env file")
        return

    print(f"Target:  {url}")
    print(f"BAQ ID:  {baq_id}")
    print("----------------------------------------")

    # 2. Attempt Connection
    try:
        # Construct standard Epicor REST v1 URL for BAQ
        # Adjust if using v2 (e.g. /api/v2/odata/{company}/...)
        full_url = f"{url}/BaqSvc/{baq_id}/Data"
        
        headers = { "CallSettings": f'{{"Company":"{company}"}}' }
        
        print(f"Full URL: {full_url}")
        print("⏳ Connecting...")
        response = requests.get(full_url, auth=(user, password), headers=headers, verify=False, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            count = len(data.get('value', []))
            print(f"✅ SUCCESS! Found {count} records.")
        else:
            print(f"❌ FAILED. Status Code: {response.status_code}")
            print(f"Response: {response.text[:200]}...")
            
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")

if __name__ == "__main__":
    test_epicor_connection()