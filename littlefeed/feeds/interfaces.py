from google.appengine.ext import db

from .models import Feed


class FeedsInterface(object):

    DEFAUL_COLLECTION_NAME = 'default_collection'

    @classmethod
    def _collection_key(cls, collection_name):
        """Constructs a Datastore key for a feed collection."""
        return db.Key.from_path(
            'Feed',
            collection_name or cls.DEFAUL_COLLECTION_NAME
        )

    @classmethod
    def _data(cls, feed):
        return {
            'follower': feed.follower,
            'url': feed.url,
        }

    @classmethod
    def list(cls, collection_name):
        collection_key = cls._collection_key(collection_name)
        # Ancestor Queries, as shown here, are strongly consistent with the
        # High Replication Datastore. Queries that span entity groups are
        # eventually consistent. If we omitted the ancestor from this query
        # there would be a slight chance that greeting that had just been
        # written would not show up in a query.
        feeds = db.GqlQuery(
            """
            SELECT * FROM Feed
              WHERE ANCESTOR IS :1 ORDER BY date_added DESC LIMIT 10
            """,
            collection_key
        )
        return (cls._data(feed) for feed in feeds)

    @classmethod
    def create(cls, collection_name, url, follower=None):
        collection_key = cls._collection_key(collection_name)
        # We set the same parent key on the 'Feed' to ensure each greeting
        # is in the same entity group. Queries across the single entity group
        # will be consistent. However, the write rate to a single entity group
        # should be limited to ~1/second.
        feed = Feed(parent=collection_key)
        feed.url = url
        feed.follower = follower
        feed.put()
