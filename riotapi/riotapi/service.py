from typing import Optional

from riotapi.api import RiotApi

from .models import Account, Match, MatchHistory


class AccountSvc:
    def __init__(self, riot_api: RiotApi):
        self.riot = riot_api

    def get_by_riot_id(self, game_name: str, tag_line: str) -> Optional[Account]:
        acc = Account.objects.filter(game_name=game_name, tag_line=tag_line).first()
        if acc:
            print(f"found cached account: {acc}")
            return acc

        data = self.riot.get_account_by_riot_id(game_name, tag_line)

        acc = Account.objects.create(
            puuid=data["puuid"], game_name=data["gameName"], tag_line=data["tagLine"]
        )
        print(f"created account {acc}")
        return acc


class MatchSvc:
    def __init__(self, riot_api: RiotApi):
        self.riot = riot_api

    def get_by_id(self, match_id: str) -> Match:
        match, _ = Match.objects.get_or_create(
            id=match_id, defaults={"data": self.riot.get_match_by_id(match_id)}
        )
        return match

    def get_match_history(
        self, user: Account, start_idx: int, count: int
    ) -> Optional[list[MatchHistory]]:
        self._sync_missing_matches(user, start_idx, count)
        end_idx = start_idx + count
        return list(
            MatchHistory.objects.filter(
                match_idx__gte=start_idx, match_idx__lt=end_idx, user=user
            ).all()
        )

    def _sync_missing_matches(self, user: Account, start_idx: int, count: int) -> None:
        end_idx = start_idx + count
        existing = {
            idx: mid
            for idx, mid in MatchHistory.objects.filter(
                user=user, match_idx__gte=start_idx, match_idx__lt=end_idx
            ).values_list("match_idx", "match_id")
        }

        missing = [i for i in range(start_idx, end_idx) if i not in existing]
        if not missing:
            print("match history already synced")
            return

        print(f"found missing match history data for {user}: {missing}")

        ranges: list[tuple[int, int]] = []
        run_start = prev = missing[0]
        for idx in missing[1:]:
            if idx == prev + 1:
                prev = idx
            else:
                ranges.append((run_start, prev - run_start + 1))
                run_start = prev = idx
        ranges.append((run_start, prev - run_start + 1))

        # For each run, fetch match IDs and create histories
        for run_start, run_count in ranges:
            match_ids = self.riot.get_matches_by_puuid(user.puuid, run_start, run_count)
            if not match_ids:
                print(
                    f"found no matches, skippking range, start: {run_start} count: {run_count}"
                )
                continue

            for offset, m_id in enumerate(match_ids):
                idx = run_start + offset
                # Skip if somehow already created in the meantime
                if idx in existing:
                    continue

                # Ensure Match exists
                match = self.get_by_id(m_id)
                mh = MatchHistory.objects.create(match_idx=idx, user=user, match=match)
                print(
                    f"creating match history: {mh} for user: {user} and match: {match}"
                )
