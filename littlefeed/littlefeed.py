import cgi
import urllib
import webapp2

from profiles.interfaces import UserInterface
from feeds.interfaces import FeedsInterface


class HomePage(webapp2.RequestHandler):

    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello, LittleFeed World!')


class DashboardPage(webapp2.RequestHandler):

    def get(self):
        user = UserInterface.get()

        if user:
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.out.write('Hello, {nickname}'.format(**user))
        else:
            self.redirect(UserInterface.login_url(self.request.uri))


class SearchFeedsPage(webapp2.RequestHandler):

    search_template = """
      <html>
        <body>
          <form action="/feeds/search" method="post">
            <div><input type="url" name="feed"></div>
            <div><input type="submit" value="Search"></div>
          </form>
        </body>
      </html>
    """

    results_template = """
      <html>
        <body>
          Searching:<pre>{url}</pre>
        </body>
      </html>
    """

    def get(self):
        self.response.out.write(SearchFeedsPage.search_template)

    def post(self):
        url = cgi.escape(self.request.get('feed'))
        self.response.out.write(
            SearchFeedsPage.results_template.format(url=url)
        )


class FeedsPage(webapp2.RequestHandler):

    header_template = """
      <html>
        <body>
    """

    user_template = """<b>{follower}</b> follows:"""
    anonymous_template = """An anonymous person follows:"""
    feed_template = """<blockquote>{url}</blockquote>"""

    footer_template = """
          <form action="/feeds?{query_string}" method="post">
            <div><input type="url" name="feed"></div>
            <div><input type="submit" value="Search"></div>
          </form>

          <hr>

          <form>
            Collection name:
            <input value="{collection_name}" name="collection_name">

            <input type="submit" value="Go">
          </form>

        </body>
      </html>
    """

    def get(self):
        collection_name = self.request.get('collection_name')

        feeds = FeedsInterface.list(collection_name)

        query_string = urllib.urlencode({'collection_name': collection_name})
        form = {
            'query_string': query_string,
            'collection_name': cgi.escape(collection_name)
        }

        self.response.out.write(FeedsPage.header_template)

        for feed in feeds:

            if feed['follower']:
                self.response.out.write(FeedsPage.user_template.format(**feed))
            else:
                self.response.out.write(FeedsPage.anonymous_template)

            url = cgi.escape(feed['url'])
            self.response.out.write(FeedsPage.feed_template.format(url=url))

        self.response.out.write(FeedsPage.footer_template.format(**form))

    def post(self):
        collection_name = self.request.get('collection_name')
        url = self.request.get('feed')
        user = UserInterface.get()

        follower = user['nickname'] if user else None
        FeedsInterface.create(collection_name, url, follower)

        query_string = urllib.urlencode({'collection_name': collection_name})
        redirect_url = '/feeds?{query_string}'.format(
            query_string=query_string
        )
        self.redirect(redirect_url)


urls = [
    ('/', HomePage),
    ('/dashboard', DashboardPage),
    ('/feeds', FeedsPage),
    ('/feeds/search', SearchFeedsPage),
]

app = webapp2.WSGIApplication(urls, debug=True)
