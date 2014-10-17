from django.test import TestCase
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from mock import Mock, patch
from ..models import Player, WarGame
from ..utils import get_random_comic, create_deck


class ViewTestCase(TestCase):

    def setUp(self):
        create_deck()

    def create_war_game(self, user, result=WarGame.LOSS):
        WarGame.objects.create(result=result, player=user)

    # def test_home_page(self):
    #     response = self.client.get(reverse('cards'))
    #     self.assertIn('<p>Suit: spade, Rank: two</p>', response.content)
    #     self.assertEqual(response.context['cards'].count(), 52)

    def test_faq_page(self):
        response = self.client.get(reverse('faq'))
        self.assertIn('<p>Q: Can I win real money on this website?</p>', response.content)

    def test_filters(self):
        response = self.client.get(reverse('filters'))
        self.assertIn('<p>Capitalized Suit: 2<br>Uppercased Rank: TWO</p>', response.content)

    def test_register_page(self):
        username = 'new-user'  # make a new user dict
        data = {
            'username': username,
            'email': 'test@test.com',
            'password1': 'test',
            'password2': 'test'
        }
        response = self.client.post(reverse('register'), data)  # POST request, go to 'register' page

        # Check this user was created in the database
        self.assertTrue(Player.objects.filter(username=username).exists())

        # Check it's a redirect to the profile page
        self.assertIsInstance(response, HttpResponseRedirect)  # set-up redirect
        self.assertTrue(response.get('location').endswith(reverse('profile')))

    def login_test(self):
        pass

    def test_profile_page(self):
        # Create user and log them in
        password = 'passsword'
        user = Player.objects.create_user(username='test-user', email='test@test.com', password=password)
        self.client.login(username=user.username, password=password)

        # Set up some war game entries
        self.create_war_game(user)
        self.create_war_game(user, WarGame.WIN)

        # Make the url call and check the html and games queryset length
        response = self.client.get(reverse('profile'))
        self.assertInHTML('<p>Your email address is {}</p>'.format(user.email), response.content)
        self.assertEqual(len(response.context['games']), 2)

    def test_war_game(self):
        # Create user and log them in
        password = 'passsword'
        user = Player.objects.create_user(username='test-user', email='test@test.com', password=password)
        self.client.login(username=user.username, password=password)

        # Set up some war game entries
        self.create_war_game(user)
        self.create_war_game(user, WarGame.WIN)

        # check war game results, etc ####################################
        # response = self.client.get(reverse('war'))
        # self.assertInHTML('<h2>War!</h2>', response.content)
        # self.assertInHTML('<h2>You won!</h2>', response.content)

    @patch('cards.utils.requests')
    def xkcd_test(self, mock_requests):
        mock_comic = {
        'num': 1433,
        'year': "2014",
        'safe_title': "Lightsaber",
        'alt': "A long time in the future, in a galaxy far, far, away.",
        'transcript': "An unusual gamma-ray burst originating from somewhere across the universe.",
        'img': "http://imgs.xkcd.com/comics/lightsaber.png",
        'title': "Lightsaber",
        }
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_comic
        mock_requests.get.return_value = mock_response
        self.assertEqual(get_random_comic()['num'], 1433)

    def tearDown(self):
        Player.objects.all().delete()
