def map_to_response_user(user, parent):
    user = format_user_full_name(user)
   
    if parent is not None:
        parent = format_user_full_name(parent)
        user['manager'] = parent['name']
        
    del user['firstName'], user['lastName'], user['password']

    return user

def format_user_full_name(user):
    first_name = user['firstName']
    last_name = user['lastName']
    user['name'] = f'{first_name} {last_name}'

    return user
