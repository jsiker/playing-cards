from unittest import TestCase
from ..models import Card, WarGame, Player
from ..tests.factories import WarGameFactory, PlayerFactory


class CardModelCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super(CardModelCase, cls).setUpClass()

    def setUp(self):
        """Test that we get the proper ranking for a card"""
        self.card = Card.objects.create(suit=Card.CLUB, rank="jack")
        self.card_high = Card.objects.create(suit=Card.CLUB, rank='queen')

    def test_get_ranking(self):
        self.assertEqual(self.card.get_ranking(), 11)

    def test_get_war_result(self):
            self.assertEqual(self.card.get_war_result(self.card_high), -1)
            self.assertEqual(self.card_high.get_war_result(self.card), 1)
            self.assertEqual(self.card.get_war_result(self.card), 0)

    def tearDown(self):
        Card.objects.all().delete()


class PlayerModelTest(TestCase):

    def create_war_game(self, user, result=WarGame.LOSS):
        WarGame.objects.create(result=result, player=user)

    def test_get_wins(self):
        user = PlayerFactory.create(email='test@test.com', password='password')
        WarGameFactory.create_batch(2, player=user, result=WarGame.WIN)
        self.assertEqual(user.get_wins(), 2)

    def tearDown(self):
        Player.objects.all().delete()

    def test_get_losses(self):
        user = PlayerFactory(email='test2@test.com', password='password')
        WarGameFactory.create_batch(3, player=user, result=WarGame.LOSS)
        self.assertEqual(user.get_losses(), 3)

    def test_get_ties(self):
        user = PlayerFactory(email='test3@test.com', password='password')
        WarGameFactory.create_batch(2, player=user, result=WarGame.TIE)
        self.assertEqual(user.get_ties(), 2)

    def test_get_record_display(self):
        user = PlayerFactory(email='test4@test.com', password='password')
        WarGameFactory.create_batch(2, player=user, result=WarGame.WIN)
        WarGameFactory.create_batch(3, player=user, result=WarGame.LOSS)
        WarGameFactory.create_batch(4, player=user, result=WarGame.TIE)
        self.assertEqual(user.get_record_display(), "2 wins - 3 losses - 4 ties")
