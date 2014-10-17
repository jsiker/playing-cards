from time import sleep
from django.core.urlresolvers import reverse
from django.test import LiveServerTestCase
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.webdriver import WebDriver
from ..models import Player


class SeleniumTests(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver()
        super(SeleniumTests, cls).setUpClass()

    def test_admin_login(self):
        # Create a superuser, give name and passwrd
        Player.objects.create_superuser('superuser', 'superuser@test.com', 'mypassword')

        # let's open the admin login page
        self.selenium.get("{}{}".format(self.live_server_url, reverse('admin:index')))

        # let's fill out the form with our superuser's username and password
        self.selenium.find_element_by_name('username').send_keys('superuser')
        password_input = self.selenium.find_element_by_name('password')
        password_input.send_keys('mypassword')

        # Submit the form
        password_input.send_keys(Keys.RETURN)

        # sleep for half a second to let the page load
        sleep(.5)

        # We check to see if 'Site administration' is now on the page, this means we logged in successfully
        body = self.selenium.find_element_by_tag_name('body')
        self.assertIn('Site administration', body.text)

    def admin_login(self):
        # Create a superuser
        Player.objects.create_superuser('superuser', 'superuser@test.com', 'mypassword')

        # let's open the admin login page
        self.selenium.get("{}{}".format(self.live_server_url, reverse('admin:index')))

        # let's fill out the form with our superuser's username and password
        self.selenium.find_element_by_name('username').send_keys('superuser')
        password_input = self.selenium.find_element_by_name('password')
        password_input.send_keys('mypassword')

        # Submit the form
        password_input.send_keys(Keys.RETURN)

    def test_admin_create_card(self):
        self.admin_login()

        # We can check that our Card model is registered with the admin and we can click on it
        # Get the 2nd one, since the first is the header
        self.selenium.find_elements_by_link_text('Cards')[1].click()

        # Let's click to add a new card
        self.selenium.find_element_by_link_text('Add card').click()

        # Let's fill out the card form
        self.selenium.find_element_by_name('rank').send_keys("ace")
        suit_dropdown = self.selenium.find_element_by_name('suit')
        for option in suit_dropdown.find_elements_by_tag_name('option'):
            if option.text == "heart":
                option.click()

        # Click save to create the new card
        self.selenium.find_element_by_css_selector("input[value='Save']").click()

        sleep(.5)

        # Check to see we get the card was added success message
        body = self.selenium.find_element_by_tag_name('body')
        self.assertIn('The card "ace of hearts" was added successfully', body.text)

    # def test_registration(self):
    #     # create user
    #     Player.objects.create_user(username='username', email='user@user.com', password='password')
    #
    #     # open reg. page
    #     self.selenium.get("{}{}".format(self.live_server_url, reverse('register')))
    #
    #     # fill out form
    #     self.selenium.find_element_by_id('id_username').send_keys('user')
    #     email_input = self.selenium.find_element_by_id('id_email')
    #     email_input.send_keys('user@user.com')
    #     password_input = self.selenium.find_element_by_id('id_password')
    #     password_input.send_keys('password')
    #     password_confirmation = self.selenium.find_element_by_id('id_password2')
    #     password_confirmation.send_keys('password')
    #
    #     # submit form
    #     password_input.send_keys(Keys.RETURN)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(SeleniumTests, cls).tearDownClass()
