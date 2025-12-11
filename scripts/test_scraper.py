import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.scrapers.apify_scraper import ApifyScraper
from src.scrapers.pokemon_tcg_client import PokemonTCGClient
from src.utils.config import PRIORITY_CARDS
import json

def test_apify():
    """Test Apify scraping"""
    scraper = ApifyScraper()

    # Test with top 5 cards
    test_cards = PRIORITY_CARDS[:5]

    print("\n=== Testing TCGPlayer Scraper ===")
    tcg_results = scraper.scrape_tcgplayer(test_cards)
    print(f"Found {len(tcg_results)} results")
    print(json.dumps(tcg_results[0], indent=2) if tcg_results else "No results")

    print("\n=== Testing eBay Scraper ===")
    ebay_results = scraper.scrape_ebay(test_cards)
    print(f"Found {len(ebay_results)} results")
    print(json.dumps(ebay_results[0], indent=2) if ebay_results else "No results")

def test_pokemon_tcg_api():
    """Test Pokemon TCG API"""
    client = PokemonTCGClient()

    print("\n=== Testing Pokemon TCG API ===")
    card_name = "Charizard ex"

    cards = client.search_card(card_name)
    print(f"Found {len(cards)} cards matching '{card_name}'")

    if cards:
        card = cards[0]
        print(f"\nCard: {card.name}")
        print(f"Set: {card.set.name}")
        print(f"Number: {card.number}")
        print(f"Rarity: {card.rarity}")
        print(f"Image: {card.images.small}")

if __name__ == "__main__":
    print("🧪 Testing Scrapers...\n")

    test_pokemon_tcg_api()
    # test_apify()  # Uncomment when Apify actors are configured

    print("\n✅ Tests complete!")