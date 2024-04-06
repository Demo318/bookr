from django.test import TestCase

class TestSimpleComponent(TestCase):
    def test_basic_some(self):
        assert 1+1 == 2
