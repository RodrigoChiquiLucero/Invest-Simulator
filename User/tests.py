from django.test import TestCase
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


class AccountTestCase(LiveServerTestCase):

    def setUp(self):
        self.selenium = webdriver.Chrome()
        super(AccountTestCase, self).setUp()

    def tearDown(self):
        self.selenium.quit()
        super(AccountTestCase, self).tearDown()

    def test_register(self):
        selenium = self.selenium
        # Opening the link we want to test
        selenium.get('http://localhost:8000/user/signup/')
        # find the form element
        first_name = selenium.find_element_by_class_name("first_name_div")
        last_name = selenium.find_element_by_class_name("last_name_div")
        username = selenium.find_element_by_class_name("username_div")
        email = selenium.find_element_by_class_name("email1_div")
        email2 = selenium.find_element_by_class_name("email2_div")
        password1 = selenium.find_element_by_class_name("password1_div")
        password2 = selenium.find_element_by_class_name("password2_div")

        submit = selenium.find_element_by_name("signup_submit")

        # Fill the form with data
        element = [avatar, first_name, last_name, username, email, email2,
                   password1,
                   password2]
        data = ['Agustín', 'Gómez', 'ZemoG', 'fagugomez1997@gmail.com',
                'fagugomez1997@gmail.com', 'fedefede', 'fedefede']

        pos = 0
        for e in element:
            e.click()
            d = data[pos]
            pos += 1

            actions = ActionChains(self.selenium)
            actions.send_keys(d)
            actions.perform()

        # submitting the form
        submit.send_keys(Keys.RETURN)

    def test_login(self):
        selenium = self.selenium
        # Opening the link we want to test
        selenium.get('http://localhost:8000/user/login/')
        # find the form element
        username = selenium.find_element_by_name("username")
        password = selenium.find_element_by_name("password")
        submit = selenium.find_element_by_name("signup_submit")
        # Fill the form with data

        username.click()
        actions = ActionChains(self.selenium)
        actions.send_keys("ZemoG")
        actions.perform()

        password.click()
        actions = ActionChains(self.selenium)
        actions.send_keys("fedefede")
        actions.perform()

        submit.send_keys(Keys.RETURN)
