import os

from dotenv import load_dotenv
from httpx import Client

load_dotenv()

RIOT_KEY = os.getenv("RIOT_API_KEY")
assert RIOT_KEY, "api key missing"

headers = {"X-Riot-Token": RIOT_KEY}


def main():
    client = Client()
    res = client.get(f"https://euw1.api.riotgames.com/riot?api_key={RIOT_KEY}")
    print(res.json())


if __name__ == "__main__":
    main()
