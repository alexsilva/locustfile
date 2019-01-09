import random
import string

from locust import HttpLocust, TaskSequence, seq_task
from pyquery import PyQuery
from six.moves.urllib.parse import urlparse

from .settings import Settings
from .users import User


class UserBehaviour(TaskSequence):

    def __init__(self, *args, **kwargs):
        super(UserBehaviour, self).__init__(*args, **kwargs)
        self.settings = self.locust.settings
        self.user = self.locust.user.random()
        self.links = []

    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        if self.settings.login_enable:
            self.login()

    def on_stop(self):
        """ on_stop is called when the TaskSet is stopping """
        if self.settings.login_enable:
            self.logout()

    def login(self):
        auth = {self.settings.login_username_field: self.user['fields']['username'],
                self.settings.login_password_field: self.settings.login_password_default}
        self.client.post(self.settings.login_url, auth)

    def logout(self):
        auth = {self.settings.login_username_field: self.user['fields']['username'],
                self.settings.login_password_field: self.settings.login_password_default}
        self.client.post(self.settings.logout_url, auth)

    @seq_task(1)
    def index(self):
        response = self.client.get("/")
        print "[{0[fields][username]}] {1.status_code} | {1.url}".format(self.user, response)
        if response.status_code == 200:
            pq = PyQuery(response.content)
            self.links = []
            for a in pq("a:not([href^='http'])"):
                href = pq(a).attr('href')
                if not string.lstrip(href, "/# "):
                    continue
                self.links.append(href)

    @seq_task(2)
    def random_link(self):
        try:
            link = random.choice(self.links)
            print link
            self.client.get(link)
        except IndexError:
            pass


class WebsiteUser(HttpLocust):
    task_set = UserBehaviour
    min_wait = 5000
    max_wait = 9000

    def __init__(self, *args, **kwargs):
        super(WebsiteUser, self).__init__(*args, **kwargs)
        self.settings = Settings()
        self.user = User(self.settings.login_users_jsonfile)
        self.domain = urlparse(self.client.base_url)
