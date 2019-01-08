from environs import Env


class Settings(object):

    def __init__(self, path=None):
        """"""
        self.env = Env()
        self.env.read_env(path=path)

    @property
    def login_users_jsonfile(self):
        return self.env.str("LOGIN_USERS_JSONFILE", "users.json")

    @property
    def login_url(self):
        return self.env.str("LOGIN_URL", "/login")

    @property
    def logout_url(self):
        return self.env.str("LOGOUT_URL", "/logout")

    @property
    def login_username_field(self):
        return self.env.str("LOGIN_USERNAME_FIELD", "username")

    @property
    def login_password_field(self):
        return self.env.str("LOGIN_PASSWORD_FIELD", "password")

    @property
    def login_password_default(self):
        return self.env.str("LOGIN_PASSWORD_DEFAULT", "test")
