import cgi
import webapp2

from google.appengine.api import users


class HomePage(webapp2.RequestHandler):

    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello, LittleFeed World!')


class DashboardPage(webapp2.RequestHandler):

    def get(self):
        user = users.get_current_user()

        if user:
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.out.write('Hello, ' + user.nickname())
        else:
            self.redirect(users.create_login_url(self.request.uri))


class FeedsPage(webapp2.RequestHandler):

    def get(self):
        self.response.out.write("""
          <html>
            <body>
              <form action="/feeds" method="post">
                <div><input type="url" name="feed"></div>
                <div><input type="submit" value="Save this feed"></div>
              </form>
            </body>
          </html>""")

    def post(self):
        self.response.out.write('<html><body>You want to add:<pre>')
        self.response.out.write(cgi.escape(self.request.get('feed')))
        self.response.out.write('</pre></body></html>')


urls = [
    ('/', HomePage),
    ('/dashboard', DashboardPage),
    ('/feeds', FeedsPage),
]

app = webapp2.WSGIApplication(urls, debug=False)
