from src.data.user_repository import UserRepository

ACCEPTED_KEYWORDS_FOR_SEARCH = ['firstName', 'lastName', 'email', 'position', 'department', 'location']
MINIMUM_NUMBER_OF_CHARACTERS_USED_FOR_SEARCH = 3

def find_the_match(string, query):
    string = string.capitalize()
    query = query.capitalize()
    if string.startswith(query) or string.endswith(query) or string.find(query) != -1:
        return True
    return False

def normalize_user(user):
    response = {}
    response['id'] = user['id']
    value = ''
    for keyword in ACCEPTED_KEYWORDS_FOR_SEARCH:
        value += user[keyword]
        if keyword != ACCEPTED_KEYWORDS_FOR_SEARCH[-1]:
            value += ', '
    response['value'] = value
    return response


def get_required_fields_by_keyword(keyword, query):
    if len(query) < MINIMUM_NUMBER_OF_CHARACTERS_USED_FOR_SEARCH:
        raise Exception('The least number of characters for the search is 3')
    if keyword not in ACCEPTED_KEYWORDS_FOR_SEARCH:
        raise Exception('The keyword provided is not among the accepted ones')
    user = UserRepository()
    all_users = user.get_all()
    matched_users = []
    for user, user_dict_value in all_users.items():
        if find_the_match(str(user_dict_value[keyword]), query):
            normalized_user = normalize_user(user_dict_value)
            matched_users.append(normalized_user)
    return matched_users
