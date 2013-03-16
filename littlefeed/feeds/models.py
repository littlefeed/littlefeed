from google.appengine.ext import db


class Feed(db.Model):
    """
    Models an individual feed url.
    """
    follower = db.StringProperty()
    url = db.LinkProperty()
    date_added = db.DateTimeProperty(auto_now_add=True)
