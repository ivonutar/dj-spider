from django.test import TestCase
from .models import Target
from .utils import get_links, spider, in_scope
import responses


class TargetTest(TestCase):
    test_url = 'http://test.nonexistent'
    test_scope = '*.test.nonexistent'

    def setUp(self) -> None:
        self.test_target = Target.objects.create(starting_point_url=self.test_url, scope=self.test_scope)

    def test_create_target(self):
        self.assertEqual(self.test_target.starting_point_url, self.test_url)


class TestUtils(TestCase):
    test_url = 'http://test.nonexistent'
    test_url_d1 = 'http://d1.test.nonexistent'
    test_url_d2_of = 'http://d2.test.nonexistent.outofcontext'
    test_url_d2 = 'http://d2.test.nonexistent'
    test_url_d3 = 'http://d3.test.nonexistent'
    test_url_d4 = 'http://d4.test.nonexistent'
    test_url_d5 = 'http://d4.test.nonexistent'
    test_scope = '*.test.nonexistent'
    test_scope_form = 'test.nonexistent'
    test_scope_free = '*'

    @responses.activate
    def test_get_links(self):
        responses.add(responses.GET, self.test_url,
                      body='<a href="test_links"></a>', status=200)
        found_links = get_links(self.test_url)

        self.assertEqual(found_links, {'test_links'})

    def test_in_context(self):
        self.assertTrue(in_scope(self.test_url, self.test_scope))
        self.assertTrue(in_scope(self.test_url, self.test_scope_form))
        self.assertFalse(in_scope(self.test_url_d2_of, self.test_scope))
        self.assertFalse(in_scope(self.test_url_d2_of, self.test_scope_form))

        self.assertTrue(in_scope(self.test_url, self.test_scope_free))
        self.assertTrue(in_scope(self.test_url_d2_of, self.test_scope_free))

    @responses.activate
    def test_spider(self):
        responses.add(responses.GET, self.test_url,
                      body='<a href="{}"></a>'.format(self.test_url_d1), status=200)
        responses.add(responses.GET, self.test_url_d1,
                      body='<a href="{}"></a><a href="{}"></a>'.format(self.test_url_d2, self.test_url_d2_of), status=200)
        responses.add(responses.GET, self.test_url_d2,
                      body='<a href="{}"></a>'.format(self.test_url_d3), status=200)
        responses.add(responses.GET, self.test_url_d3,
                      body='<a href="{}"></a>'.format(self.test_url_d4), status=200)
        responses.add(responses.GET, self.test_url_d4,
                      body='<a href="{}"></a>'.format(self.test_url_d5), status=200)

        self.assertEqual(spider(self.test_url, self.test_scope, depth=0), {self.test_url})
        self.assertEqual(spider(self.test_url, self.test_scope, depth=3), {self.test_url,
                                                                           self.test_url_d1,
                                                                           self.test_url_d2,
                                                                           self.test_url_d3})

        self.assertEqual(spider(self.test_url, self.test_scope, depth=4), {self.test_url,
                                                                           self.test_url_d1,
                                                                           self.test_url_d2,
                                                                           self.test_url_d3,
                                                                           self.test_url_d4})
