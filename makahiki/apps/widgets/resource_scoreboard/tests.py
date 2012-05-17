"""Energy scoreboard Test"""
import datetime

from django.test import TransactionTestCase
from django.core.urlresolvers import reverse
from apps.managers.challenge_mgr import challenge_mgr

from apps.test_helpers import test_utils
from apps.widgets.resource_goal.models import EnergyGoal


class EnergyFunctionalTestCase(TransactionTestCase):
    """Energy Test"""

    def setUp(self):
        """Initialize a user and log them in."""
        self.user = test_utils.setup_user(username="user", password="changeme")
        self.team = self.user.get_profile().team

        challenge_mgr.register_page_widget("energy", "resource_scoreboard.energy")
        self.client.login(username="user", password="changeme")

    def testIndex(self):
        """Check that we can load the index page."""
        response = self.client.get(reverse("energy_index"))
        self.failUnlessEqual(response.status_code, 200)

    def testEnergyScoreboard(self):
        """test Energy scoreboard."""
        response = self.client.get(reverse("energy_index"))
        goals = response.context["view_objects"]["resource_scoreboard__energy"]["goals_scoreboard"]
        for goal in goals:
            self.assertEqual(goal["completions"], 0, "No team should have completed a goal.")

        energy_goal = EnergyGoal.objects.create(
            team=self.team,
            date=datetime.date.today(),
            goal_status="Over the goal",
        )

        response = self.client.get(reverse("energy_index"))
        goals = response.context["view_objects"]["resource_scoreboard__energy"]["goals_scoreboard"]
        for goal in goals:
            self.assertEqual(goal["completions"], 0, "No team should have completed a goal.")

        energy_goal.goal_status = "Below the goal",
        energy_goal.save()

        response = self.client.get(reverse("energy_index"))
        goals = response.context["view_objects"]["resource_scoreboard__energy"]["goals_scoreboard"]
        for team in goals:
            if team["team__name"] == self.team.name:
                # print team.teamenergygoal_set.all()
                self.assertEqual(team["completions"], 1,
                    "User's team should have completed 1 goal, but completed %d" % team[
                                                                                    "completions"])
            else:
                self.assertEqual(team["completions"], 0, "No team should have completed a goal.")
