from typing import Any

import httpx

ROOT_URL = "https://europe.api.riotgames.com"
ACCOUNT_BY_RIOT_ID = (
    f"{ROOT_URL}/riot/account/v1/accounts/by-riot-id/{{gameName}}/{{tagLine}}"
)
MATCHES_BY_PUUID = f"{ROOT_URL}/lol/match/v5/matches/by-puuid/{{puuid}}/ids?start={{start}}&count={{count}}"
MATCH_BY_MATCHID = f"{ROOT_URL}/lol/match/v5/matches/{{matchId}}"


class RiotApi:
    def __init__(self, client: httpx.Client, timeout_secs: int = 2) -> None:
        self.client = client
        self.timeout_secs = timeout_secs

    def get_match_by_id(self, match_id: str) -> dict[str, Any]:
        url = MATCH_BY_MATCHID.format(matchId=match_id)
        res = self.client.get(url)
        res.raise_for_status()
        print(f"fetched match {match_id}")
        return res.json()

    def get_matches_by_puuid(self, puuid: str, start: int, count: int) -> list[str]:
        url = MATCHES_BY_PUUID.format(puuid=puuid, start=start, count=count)
        res = self.client.get(url)
        res.raise_for_status()
        print(f"fetched match histroy for {puuid} from {start} to {start + count}")
        return res.json()

    def get_account_by_riot_id(self, game_name: str, tag_line: str) -> dict[str, Any]:
        res = self.client.get(
            ACCOUNT_BY_RIOT_ID.format(gameName=game_name, tagLine=tag_line)
        )
        res.raise_for_status()
        print(f"fetched account for {game_name}#{tag_line}")
        return res.json()
