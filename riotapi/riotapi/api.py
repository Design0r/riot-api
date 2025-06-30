from __future__ import annotations

import functools
import time
from typing import Any, Callable

import httpx

ROOT_URL = "https://europe.api.riotgames.com"
ACCOUNT_BY_RIOT_ID = (
    f"{ROOT_URL}/riot/account/v1/accounts/by-riot-id/{{gameName}}/{{tagLine}}"
)

ACCOUNT_BY_PUUID = f"{ROOT_URL}/riot/account/v1/accounts/by-puuid/{{puuid}}"
MATCHES_BY_PUUID = f"{ROOT_URL}/lol/match/v5/matches/by-puuid/{{puuid}}/ids?start={{start}}&count={{count}}"
MATCH_BY_MATCHID = f"{ROOT_URL}/lol/match/v5/matches/{{matchId}}"


def create_rate_limiter(timeout_secs: float, verbose: bool = True):
    class RateLimiter(type):
        def __new__(
            mcs: type["RateLimiter"],
            name: str,
            bases: tuple[type, ...],
            namespace: dict[str, Any],
        ) -> RateLimiter:
            timestamp: float = time.time()

            def wrap(func: Callable[..., Any]) -> Callable[..., Any]:
                @functools.wraps(func)
                def wrapped(*args: Any, **kwargs: Any) -> Any:
                    nonlocal timestamp
                    nonlocal timeout_secs

                    now: float = time.time()
                    delta: float = now - timestamp
                    if delta <= timeout_secs:
                        if verbose:
                            print(
                                f"pausing {func.__name__}, "
                                f"sleeping for {timeout_secs - delta:.3f}s"
                            )
                        time.sleep(timeout_secs - delta)

                    timestamp = time.time()
                    return func(*args, **kwargs)

                return wrapped

            new_ns: dict[str, Any] = {}
            for attr, value in namespace.items():
                if isinstance(value, classmethod):
                    new_ns[attr] = classmethod(wrap(value.__func__))  # type: ignore
                elif isinstance(value, staticmethod):
                    new_ns[attr] = staticmethod(wrap(value.__func__))
                elif callable(value):
                    if value.__name__ == "__init__":
                        new_ns[attr] = value
                        continue

                    new_ns[attr] = wrap(value)
                else:
                    new_ns[attr] = value

            return super().__new__(mcs, name, bases, new_ns)

    return RateLimiter


class RiotApi(metaclass=create_rate_limiter(1.4, verbose=False)):
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

    def get_account_by_puuid(self, puuid: str) -> dict[str, Any]:
        res = self.client.get(ACCOUNT_BY_PUUID.format(puuid=puuid))
        res.raise_for_status()
        data = res.json()
        print(f"fetched account for {data['gameName']}#{data['tagLine']}")
        return data
