from src.api.controllers.account_controller import SignIn
from src.api import api_messages
import unittest


class TestLogin(unittest.TestCase):

    def test_if_correct(self):
        value = SignIn.validate_user("president", "president")
        self.assertEqual(value[0], None)

    def test_if_correct_email(self):
        value = SignIn.validate_user("president@aua.am", "president")
        self.assertEqual(value[0], None)

    def test_if_incorrect_username(self):
        value = SignIn.validate_user("pasdsfp", "president")
        self.assertEqual((200, api_messages.BAD_USERNAME_OR_PASSWORD), value)

    def test_if_incorrect_password(self):
        value = SignIn.validate_user("president", "president1")
        self.assertEqual((200, api_messages.BAD_USERNAME_OR_PASSWORD), value)

    def test_if_empty_username(self):
        value = SignIn.validate_user("", "president")
        self.assertEqual((400, api_messages.MISSING_USERNAME), value)

    def test_if_empty_password(self):
        value = SignIn.validate_user("president", "")
        self.assertEqual((400, api_messages.MISSING_PASSWORD), value)


if __name__ == '__main__':
    unittest.main()
