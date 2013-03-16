import webapp2

from dashboard.views import DashboardPage, FeedsPage
from dashboard.views import SearchFeedsPage, FeedsDashboardPage


class HomePage(webapp2.RequestHandler):

    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello, LittleFeed World!')


urls = [
    ('/', HomePage),
    ('/dashboard', DashboardPage),
    ('/feeds', FeedsPage),
    ('/feeds/search', SearchFeedsPage),
    ('/dashboard/feeds', FeedsDashboardPage),
]

app = webapp2.WSGIApplication(urls, debug=True)
