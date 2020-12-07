from src.api.controllers.search import find_the_match, normalize_user, get_required_fields_by_keyword
import unittest


class TestFindMatchMethod(unittest.TestCase):

    def test_find_the_match_should_match_with_valid_prefix(self):
        is_Matched = find_the_match("FirstName", "first")
        self.assertTrue(is_Matched)

    def test_find_the_match_should_match_with_valid_suffix(self):
        is_Matched = find_the_match("FirstName", "name")
        self.assertTrue(is_Matched)  

    def test_find_the_match_should_match_with_valid_substring(self):
        is_Matched = find_the_match("Yerevan, Armenia", "Armenia")
        self.assertTrue(is_Matched)

    def test_find_the_match_should_not_match_with_invalid_string(self):
        is_Matched = find_the_match("FirstName", "invalid")
        self.assertFalse(is_Matched)          


class TestNormalizeUser(unittest.TestCase):

    def test_normalize_user_returns_formmated_data_with_valid_user(self):
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
        self.assertEqual(user['id'], response['value'])
        self.assertEqual('Test1, Test1, test@aua.am, Test-Test 1, Test, Yerevan, Armenia', response['label'])

    def test_normalize_user_raises_error_with_empty_user(self):
        self.assertRaises(KeyError, normalize_user, {})

    def test_normalize_raises_error_with_missing_user_id(self):
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

    def test_get_required_fields_raises_error_with_invalid_len(self):
        self.assertRaises(Exception, get_required_fields_by_keyword, 'firstName', 'ab')        
    
    def test_get_required_raises_error_on_non_accepted_keyword(self):
        self.assertRaises(Exception, get_required_fields_by_keyword, 'NotAcceptedWord', 'fName1')

    # In case of real data source UserRepositry should be mocked.
    def test_get_required_raises_error_when_query_value_not_found(self):
        users = get_required_fields_by_keyword("firstName", "notExistingName")
        self.assertFalse(users)
    
    def test_get_required_accepted_returns_users_with_valid_keyword_(self):
        users = get_required_fields_by_keyword("firstName", "FName5")
        self.assertTrue(users)    


if __name__ == '__main__':
    unittest.main()
