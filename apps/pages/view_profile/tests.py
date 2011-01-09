from django.test import TestCase
from django.core.urlresolvers import reverse

class ProfileFunctionalTestCase(TestCase):
  def testIndex(self):
    """Check that we can load the index page."""
    response = self.client.get(reverse("profile_index"))
    self.failUnlessEqual(response.status_code, 200)