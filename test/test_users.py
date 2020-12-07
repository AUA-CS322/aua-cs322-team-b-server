import unittest
from src.data.organization_chart import OrganizationChart
from src.data.user_repository import UserRepository
from src.utils.user_mapper import map_to_response_user


class TestUsers(unittest.TestCase):

    repository = UserRepository()
    test_user = {
        "department": "Executive",
        "email": "president@aua.am",
        "id": "94a7335f-2181-4811-9a06-f53ae949a98a",
        "location": "Yerevan, Armenia",
        "firstName": "FName",
        "lastName": "LName",
        "phone": "+37455000000",
        "photoUrl": "https://avataaars.io/?avatarStyle=Transparent&topType=LongHairStraightStrand&accessoriesType=Wayfarers&hairColor=BrownDark&facialHairType=Blank&clotheType=GraphicShirt&clotheColor=Pink&graphicType=Bear&eyeType=Default&eyebrowType=UpDownNatural&mouthType=Twinkle&skinColor=Yellow",
        "position": "President",
        "password": "random"
    }

    test_vp_user = {
        "department": "VP",
        "email": "vicepresident2@aua.am",
        "id": "a9d8c82c-e7c1-40d6-90c2-890587223de5",
        "location": "Yerevan, Armenia",
        "manager": "FName LName",
        "firstName" : "FName2",
        "lastName" : "LName2",
        "name": " LName2",
        "phone": "+37455000002",
        "photoUrl": "https://avataaars.io/?avatarStyle=Transparent&topType=ShortHairShortWaved&accessoriesType=Wayfarers&hairColor=Auburn&facialHairType=MoustacheFancy&facialHairColor=Platinum&clotheType=Hoodie&clotheColor=PastelRed&eyeType=Default&eyebrowType=FlatNatural&mouthType=Smile&skinColor=Tanned",
        "position": "Vice-President 2",
        "password" : "random"
    }

    def test_exists_user(self):
        user = TestUsers.repository.get_by_id("94a7335f-2181-4811-9a06-f53ae949a98a")
        self.compare(user, TestUsers.test_user)

    def test_not_exists_user(self):
        user = TestUsers.repository.get_by_id("94a70000-2181-4811-9a06-f53ae949a98a")
        self.assertEqual(user, None)

    def test_user_no_parent(self):
        user, parent = OrganizationChart().get_user_with_manager("94a7335f-2181-4811-9a06-f53ae949a98a")
        self.compare(user, TestUsers.test_user)
        self.assertEqual(None, parent)

    def test_with_parent(self):
        user, parent = OrganizationChart().get_user_with_manager("a9d8c82c-e7c1-40d6-90c2-890587223de5")
        self.compare(user, TestUsers.test_vp_user)
        self.compare(parent, TestUsers.test_user)

    def test_map_users_with_parent(self):
        result = map_to_response_user(TestUsers.test_vp_user.copy(), TestUsers.test_user.copy())
        self.assertEqual(result["name"], TestUsers.test_vp_user["firstName"] + " " + TestUsers.test_vp_user["lastName"])
        self.assertEqual(result["manager"], TestUsers.test_user["firstName"] + " " + TestUsers.test_user["lastName"])
        self.assertNotIn("fistName", result)
        self.assertNotIn("lastName", result)

    def compare(self, user1, user2):
        self.assertEqual(user1["email"], user2["email"])
        self.assertEqual(user1["department"], user2["department"])
        self.assertEqual(user1["location"], user2["location"])
        self.assertEqual(user1["firstName"], user2["firstName"])
        self.assertEqual(user1["lastName"], user2["lastName"])
        self.assertEqual(user1["phone"], user2["phone"])
        self.assertEqual(user1["photoUrl"], user2["photoUrl"])
        self.assertEqual(user1["position"], user2["position"])


if __name__ == '__main__':
    unittest.main()
