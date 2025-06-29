import os

import django_prelude  # noqa: F401
from httpx import Client

from riotapi.api import RiotApi
from riotapi.service import AccountSvc, MatchSvc

RIOT_KEY = os.environ.get("RIOT_API_KEY", "")


def main():
    headers = {"X-Riot-Token": RIOT_KEY}
    client = Client(headers=headers)
    riot_api = RiotApi(client, timeout_secs=2)
    acc_svc = AccountSvc(riot_api)
    match_svc = MatchSvc(riot_api)
    acc = acc_svc.get_by_riot_id("souL", "ULU")
    if not acc:
        return
    data = match_svc.get_match_history(acc, 0, 15)
    for d in data:
        print(d, d.match, d.user)


if __name__ == "__main__":
    main()
