"""Invocation:  python manage.py verify_quests

Verifies that all of the existing quest lock and unlock condition strings are valid.
Prints out the names of any invalid quest conditions."""

import sys

from django.core import management
from django.contrib.auth.models import User

from apps.widgets.quests.models import Quest
from apps.widgets.quests.quests import process_conditions_string


class Command(management.base.BaseCommand):
    """command"""
    help = "Verifies that all existing quest unlock/completion conditions are valid."

    def handle(self, *args, **options):
        """handle"""
        print "Validating quests ..."
        for quest in Quest.objects.all():
            error_msg = self.validate_conditions(quest.unlock_conditions)
            if error_msg:
                print "Unlock conditions for '%s' did not validate: %s" % (quest.name, error_msg)

            error_msg = self.validate_conditions(quest.completion_conditions)
            if error_msg:
                print "Completion conditions for '%s' did not validate: %s" % (
                quest.name, error_msg)

    def validate_conditions(self, conditions):
        """Validate the conditions string."""
        # Pick a user and see if the conditions result is true or false.
        error_msg = None
        user = User.objects.order_by("?")[0]
        try:
            result = process_conditions_string(conditions, user)
            # Check if the result type is a boolean
            if type(result) != type(True):
                error_msg = "Expected boolean value but got %s" % type(result)
        except AttributeError:
            error_msg = "Received exception: %s" % sys.exc_info()[0]

        return error_msg
