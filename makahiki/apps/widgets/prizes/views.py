"""Provide the view of the prizes widget."""
import datetime

from django.conf import settings
from apps.widgets.prizes.models import Prize


def supply(request, page_name):
    """Supply view_object content, which is the prizes for this team."""
    _ = page_name
    team = request.user.get_profile().team
    prizes = _get_prizes(team)

    return {
        "prizes": prizes,
        }


def _get_prizes(team):
    """Private method to process the prizes half of the page.
       Takes the user's team and returns a dictionary to be used in the template."""
    rounds = settings.COMPETITION_ROUNDS
    prize_dict = {}
    today = datetime.datetime.today()
    for key in rounds.keys():
        prizes = Prize.objects.filter(round_name=key)
        for prize in prizes:
            if today < rounds[key]["start"]:
                # If the round happens in the future, we don't care who the leader is.
                prize.current_leader = "TBD"
            else:
                # If we are in the middle of the round, display the current leader.
                if today < rounds[key]["end"]:
                    prize.current_leader = prize.leader(team)
                else:
                    prize.winner = prize.leader(team)

        prize_dict[key] = prizes

    return prize_dict
