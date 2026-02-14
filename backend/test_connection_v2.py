import os
import requests
import urllib3
from dotenv import load_dotenv

# Disable SSL warnings for internal servers
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def test_epicor_connection():
    print("========================================")
    print("   Epicor API Connection Tester V2      ")
    print("========================================\n")
    
    # Load Environment Variables
    load_dotenv()
    url = os.getenv("EPICOR_API_URL", "https://199.5.83.159/EpicorERP/api/v1")
    user = os.getenv("EPICOR_USERNAME", "WESTS")
    password = os.getenv("EPICOR_PASSWORD")
    baq_id = os.getenv("EPICOR_BAQ_ID", "PO_Test")

    if not url or not user or not password:
        print("❌ Error: Missing credentials in .env file")
        return

    print(f"Base URL:  {url}")
    print(f"User:      {user}")
    print(f"BAQ ID:    {baq_id}")
    print("----------------------------------------\n")

    # Test different endpoint formats
    endpoints = [
        f"{url}/BaqSvc/{baq_id}",
        f"{url}/BaqSvc/{baq_id}/",
        f"{url}/odata/PO_Test",
        f"{url}/BaqSvc",
    ]

    for endpoint in endpoints:
        print(f"Testing: {endpoint}")
        try:
            response = requests.get(endpoint, auth=(user, password), verify=False, timeout=10)
            print(f"  Status: {response.status_code}")
            
            if response.status_code == 200:
                print(f"  ✅ SUCCESS!")
                print(f"  Response: {response.json()[:200] if response.text else 'Empty'}")
            elif response.status_code in [401, 403]:
                print(f"  ❌ Authentication failed")
            else:
                print(f"  Response: {response.text[:100]}")
        except Exception as e:
            print(f"  ❌ Error: {str(e)}")
        print()

if __name__ == "__main__":
    test_epicor_connection()
