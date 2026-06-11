import requests

class RadioService:
    BASE_URL = "https://de1.api.radio-browser.info/json"

    def search_stations(self, query="", limit=50):
        try:
            response = requests.get(
                f"{self.BASE_URL}/stations/search",
                params={
                    "name": query,
                    "limit": limit,
                    "order": "votes",
                    "reverse": "true",
                    "hidebroken": "true"
                },
                timeout=5
            )
            return response.json()
        except Exception as e:
            print("RADIO SEARCH ERROR:", e)
            return []