import bcrypt


class AccountManager:

    @staticmethod
    def is_password_correct(password, hashed_password):
        password = password.encode('utf8')
        hashed_password = hashed_password.encode('utf8')
        return bcrypt.checkpw(password=password, hashed_password=hashed_password)
