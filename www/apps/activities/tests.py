from django.test import TestCase

from .models import Activity


class ActivityTestCase(TestCase):
    def setUp(self):
        Activity.objects.create(title='Activity Title', content='Activity Content')

    def test_activity(self):
        """Activity test"""
        activity = Activity.objects.get(title='Activity Title')
        print(activity.content)
        self.assertEqual(activity.slug, 'activity-title')
