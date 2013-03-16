from google.appengine.api import users


class UserInterface(object):

    @classmethod
    def get(cls):
        user = users.get_current_user()

        if user:
            return {'nickname': user.nickname()}
        else:
            return None

    @classmethod
    def login_url(cls, redirect_url):
        return users.create_login_url(redirect_url)
