from apify_client import ApifyClient
import os
from dotenv import load_dotenv
import time

load_dotenv()

class ApifyScraper:
    def __init__(self):
        self.client = ApifyClient(os.getenv('APIFY_API_TOKEN'))

    def scrape_tcgplayer(self, search_queries):
        """
        Scrape TCGPlayer for card prices
        """
        print("🔍 Starting TCGPlayer scrape...")

        # Example actor (replace with actual actor ID)
        actor_id = "YOUR_TCGPLAYER_ACTOR_ID"

        run_input = {
            "queries": search_queries,
            "language": "English",
            "maxItems": 100
        }

        # Run the actor
        run = self.client.actor(actor_id).call(run_input=run_input)

        # Get results
        items = []
        for item in self.client.dataset(run["defaultDatasetId"]).iterate_items():
            items.append(item)

        print(f"✅ Scraped {len(items)} items from TCGPlayer")
        return items

    def scrape_ebay(self, search_queries):
        """
        Scrape eBay for card prices
        """
        print("🔍 Starting eBay scrape...")

        actor_id = "YOUR_EBAY_ACTOR_ID"

        run_input = {
            "queries": [f"{q} Pokemon card English" for q in search_queries],
            "maxItems": 100
        }

        run = self.client.actor(actor_id).call(run_input=run_input)

        items = []
        for item in self.client.dataset(run["defaultDatasetId"]).iterate_items():
            items.append(item)

        print(f"✅ Scraped {len(items)} items from eBay")
        return items