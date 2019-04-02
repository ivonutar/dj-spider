from django.test import TestCase
from .models import Target
from .utils import get_links
import responses


class TargetTest(TestCase):

    test_url = 'http://test.nonexistent'

    def setUp(self) -> None:

        self.test_target = Target.objects.create(target_url=self.test_url)

    def test_create_target(self):
        self.assertEqual(self.test_target.target_url, self.test_url)


class TestUtils(TestCase):

    test_url = 'http://test.nonexistent'

    @responses.activate
    def test_get_links(self):
        responses.add(responses.GET, self.test_url,
                      body='<a href="test_links"></a>', status=200)
        found_links = get_links(self.test_url)

        self.assertEqual(found_links, ['test_links'])
