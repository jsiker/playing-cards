from unittest import TestCase
from ..models import Card
from ..utils import create_deck

__author__ = 'danielsiker'


class UtilTest(TestCase):
    def test_create_deck(self):
        self.assertEqual(Card.objects.count(), 0)
        create_deck()
        self.assertEqual(len(Card.objects.all()), 52)

    def tearDown(self):
        Card.objects.all().delete()


class UtilTestCase(TestCase):
    def test_create_deck_count(self):
        """Test that we created 52 cards"""
        create_deck()
        self.assertEqual(Card.objects.count(), 52)

    def tearDown(self):
        Card.objects.all().delete()
