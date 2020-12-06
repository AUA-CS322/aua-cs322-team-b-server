from src.api.controllers.search import (find_the_match, normalize_user, get_required_fields_by_keyword, 
ACCEPTED_KEYWORDS_FOR_SEARCH, MINIMUM_NUMBER_OF_CHARACTERS_USED_FOR_SEARCH)

import unittest
from unittest.mock import MagicMock, patch
from src.data.user_repository import UserRepository

class TestFindMatchMethod(unittest.TestCase):


    def test_find_the_match_beginning(self):
        is_Matched = find_the_match("FirstName", "first")
        self.assertTrue(is_Matched)

    def test_find_the_match_end(self):
        is_Matched = find_the_match("FirstName", "name")
        self.assertTrue(is_Matched)  

    def test_contains_the_match(self):
        is_Matched = find_the_match("Yerevan, Armenia", "Armenia")
        self.assertTrue(is_Matched)

    def test_does_not_contain_the_match(self):
        is_Matched = find_the_match("FirstName", "invalid")
        self.assertFalse(is_Matched)          


class TestNormalizeUser(unittest.TestCase):


    def test_normalize_user_success(self):
        user = {
            "id": "caf54384-0fc3-44a4-a3ec-ca250b10dc40",
            "email": "test@aua.am",
            "username": "test1",
            "password": "$2y$12$sDp8x40HtD78GnQmayDkg.Xepqno3VrZkXI7N5XYw7fx3bnpYP/p2",
            "position": "Test-Test 1",
            "department": "Test",
            "location": "Yerevan, Armenia",
            "firstName": "Test1",
            "lastName": "Test1",
            "phone": "+37455999111",
            "photoUrl": "https://avataaars.io/?avatarStyle=Transparent&topType=ShortHairTheCaesarSidePart&accessoriesType=Wayfarers&hairColor=Platinum&facialHairType=MoustacheMagnum&facialHairColor=BlondeGolden&clotheType=ShirtVNeck&clotheColor=Blue01&graphicType=Cumbia&eyeType=Surprised&eyebrowType=Default&mouthType=Sad&skinColor=Tanned"
        }
        response = normalize_user(user)
        self.assertEquals(user['id'], response['value'])
        self.assertEquals('Test1, Test1, test@aua.am, Test-Test 1, Test, Yerevan, Armenia', response['label'])

    def test_normalize_user_empty_user(self):
        self.assertRaises(KeyError, normalize_user, {})

    def test_normalize_user_missing_key(self):
        user = {
            "email": "test@aua.am",
            "username": "test1",
            "password": "$2y$12$sDp8x40HtD78GnQmayDkg.Xepqno3VrZkXI7N5XYw7fx3bnpYP/p2",
            "position": "Test-Test 1",
            "department": "Test",
            "location": "Yerevan, Armenia",
            "firstName": "Test1",
            "lastName": "Test1",
            "phone": "+37455999111",
            "photoUrl": "https://avataaars.io/?avatarStyle=Transparent&topType=ShortHairTheCaesarSidePart&accessoriesType=Wayfarers&hairColor=Platinum&facialHairType=MoustacheMagnum&facialHairColor=BlondeGolden&clotheType=ShirtVNeck&clotheColor=Blue01&graphicType=Cumbia&eyeType=Surprised&eyebrowType=Default&mouthType=Sad&skinColor=Tanned"
        }
        self.assertRaises(KeyError, normalize_user, user)       

class TestGetRequiredFieldsMethod(unittest.TestCase):


    def test_get_required_fields_min_length_exception(self):
        self.assertRaises(Exception, get_required_fields_by_keyword, 'firstName', 'ab')        
    
    def test_get_required_no_accepted_keyword_exception(self):
        self.assertRaises(Exception, get_required_fields_by_keyword, 'NotAcceptedWord', 'fName1')

    # In case of real data sources UserRepositry should be mocked.
    def test_get_required_accepted_keyword_not_found(self):
        users = get_required_fields_by_keyword("firstName", "notExistingName")
        self.assertFalse(users)
    
    def test_get_required_accepted_keyword_success(self):
        users = get_required_fields_by_keyword("firstName", "FName5")
        self.assertTrue(users)    

if __name__ == '__main__':
    unittest.main()