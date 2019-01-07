from environs import Env


class Settings(object):

    def __init__(self, path=None):
        """"""
        self.env = Env()
        self.env.read_env(path=path)

    @property
    def login_url(self):
        return self.env.str("LOGIN_URL", "/login")

    @property
    def logout_url(self):
        return self.env.str("LOGOUT_URL", "/logout")

    @property
    def username_field(self):
        return self.env.str("LOGIN_USERNAME_FIELD", "username")

    @property
    def password_field(self):
        return self.env.str("LOGIN_PASSWORD_FIELD", "password")
