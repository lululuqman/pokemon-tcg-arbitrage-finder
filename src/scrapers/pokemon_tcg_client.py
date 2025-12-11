from pokemontcgsdk import Card, RestClient
import os
import time
from dotenv import load_dotenv

load_dotenv()

class PokemonTCGClient:
    def __init__(self, max_retries=3, retry_delay=1):
        api_key = os.getenv('POKEMON_TCG_API_KEY')
        if api_key:
            RestClient.configure(api_key)
        self.max_retries = max_retries
        self.retry_delay = retry_delay

    def _retry_request(self, func, *args, **kwargs):
        """
        Retry a request with exponential backoff
        """
        for attempt in range(self.max_retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                error_msg = str(e) if not isinstance(e, bytes) else e.decode('utf-8', errors='replace')

                if attempt < self.max_retries - 1:
                    wait_time = self.retry_delay * (2 ** attempt)
                    print(f"Attempt {attempt + 1} failed: {error_msg}. Retrying in {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    print(f"All {self.max_retries} attempts failed: {error_msg}")
                    return None

    def search_card(self, card_name, set_name=None):
        """
        Search for card in Pokemon TCG API with retry logic
        """
        query = f'name:"{card_name}"'
        if set_name:
            query += f' set.name:"{set_name}"'

        def _search():
            cards = Card.where(q=query)
            return cards if cards else []

        result = self._retry_request(_search)
        return result if result is not None else []

    def get_card_by_id(self, pokemon_tcg_id):
        """
        Get card by Pokemon TCG API ID with retry logic
        """
        def _get():
            return Card.find(pokemon_tcg_id)

        return self._retry_request(_get)

    def get_card_image(self, card_name, set_name=None):
        """
        Get card image URL
        """
        cards = self.search_card(card_name, set_name)
        if cards:
            return {
                'small': cards[0].images.small,
                'large': cards[0].images.large
            }
        return None