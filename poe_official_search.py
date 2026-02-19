import requests
import json

USER_AGENT = "POE2DataTracker/1.0 (Contact: Sfuborisw via GitHub)"
LEAGUE = "Fate of the Vaal" 

def search_and_fetch():
    search_url = f"https://www.pathofexile.com/api/trade2/exchange/{LEAGUE}"
    
    headers = {
        "User-Agent": USER_AGENT,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    # Use Chaos to buy Divine (Most common trade)
    query_payload = {
        "exchange": {
            "status": {"option": "online"},
            "have": ["chaos"],
            "want": ["divine"]
        }
    }

    try:
        print(f"1. Searching for Divine Orbs in '{LEAGUE}'...")
        response = requests.post(search_url, headers=headers, json=query_payload)
        response.raise_for_status()
        search_data = response.json()

        result_data = search_data.get("result", [])
        
        # Official API sometimes returns result as a dictionary of {id: info}
        if isinstance(result_data, dict):
            result_list = list(result_data.keys())
        else:
            result_list = result_data

        if not result_list:
            print("⚠️ No listings found. Try changing the 'have' currency.")
            return

        query_id = search_data.get("id")
        count = min(len(result_list), 5)
        print(f"✅ Found {len(result_list)} listings. Fetching top {count}...")

        top_ids = ",".join(result_list[:count])
        fetch_url = f"https://www.pathofexile.com/api/trade2/fetch/{top_ids}?query={query_id}&exchange"

        fetch_res = requests.get(fetch_url, headers=headers)
        fetch_res.raise_for_status()
        fetch_data = fetch_res.json()

        print("\n" + "="*65)
        print(f"{'SELLER (Account)':<30} | {'CHAOS PER DIVINE':>20}")
        print("-" * 65)

        for item in fetch_data.get("result", []):
            # 防錯檢查：逐層 .get 並提供預設值 {} 或 None
            if item is None: continue
            
            listing = item.get("listing", {})
            offers = listing.get("offers", [])
            
            if offers and len(offers) > 0:
                offer = offers[0]
                item_info = offer.get("item", {})
                exch_info = offer.get("exchange", {})
                
                # 確保數字存在，避免除以零
                want_amt = item_info.get("amount", 1)
                have_amt = exch_info.get("amount", 0)
                
                rate = have_amt / want_amt
                seller = listing.get("account", {}).get("name", "Unknown")
                
                print(f"{seller[:30]:<30} | {rate:>20.2f}")
        
        print("="*65)

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    search_and_fetch()