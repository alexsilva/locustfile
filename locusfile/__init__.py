from locust import HttpLocust, TaskSet, task

from .settings import Settings
from .users import User


class UserBehaviour(TaskSet):

    def __init__(self, *args, **kwargs):
        super(UserBehaviour, self).__init__(*args, **kwargs)
        self.settings = self.locust.settings
        self.user = self.locust.user.random()

    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        self.login()

    def on_stop(self):
        """ on_stop is called when the TaskSet is stopping """
        self.logout()

    def login(self):
        auth = {self.settings.login_username_field: self.user['fields']['username'],
                self.settings.login_password_field: self.settings.login_password_default}
        self.client.post(self.settings.login_url, auth)

    def logout(self):
        auth = {self.settings.login_username_field: self.user['fields']['username'],
                self.settings.login_password_field: self.settings.login_password_default}
        self.client.post(self.settings.logout_url, auth)

    @task(1)
    def index(self):
        response = self.client.get("/")
        print "[{0[fields][username]}] {1.url}".format(self.user, response)


class WebsiteUser(HttpLocust):
    task_set = UserBehaviour
    min_wait = 5000
    max_wait = 9000

    def __init__(self, *args, **kwargs):
        super(WebsiteUser, self).__init__(*args, **kwargs)
        self.settings = Settings()
        self.user = User(self.settings.login_users_jsonfile)
