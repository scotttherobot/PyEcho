# A Python class for connection to the Amazon Echo API
# By Scott Vanderlind, December 31 2014
import requests, json, urllib, cookielib
from bs4 import BeautifulSoup

class PyEcho:

   url = "https://pitangui.amazon.com"
   email = ""
   password = ""
   session = False
    csrf = "-2092727538"

   def __init__(self, email, password):
      self.email = email 
      self.password = password
      self.session = requests.Session()
      self.login()

   def login(self):
      print "logging in..."

      # Get the login page and retrieve our form action.
      loginPage = self.get("")
      loginSoup = BeautifulSoup(loginPage.text)
      
      form = loginSoup.find('form')
      action = form.get('action')

      # Create our parameter payload
      parameters = {}
      # let's not forget our email and password
      parameters['email'] = self.email
      parameters['password'] = self.password
      parameters['create'] = "0"
      # We need to keep the hidden fields around
      hidden = form.find_all(type="hidden")
      for el in hidden:
         parameters[el['name']] = el['value']

      # Set up the headers for the request
      headers = self.getHeaders()
      headers['Referer'] = self.url

      # Now, we can create a new post request to log in
      login = self.session.post(action, data=parameters, headers=headers)

      if login.status_code != 200:
         print "Error logging in! Got status " + str(login.status_code)
      else:
         print "Login success!"
         # print self.session.cookies
         # print BeautifulSoup(login.text).prettify()

         # We need to set a CSRF cookie. CSRF validation works like this:
         # The CSRF cookie has to match the CSRF header. Doesn't matter
         # what the actual value is, they just gotta match.
         csrf = cookielib.Cookie(name="csrf", value=self.csrf,
               domain=".amazon.com", path="/", expires=None,
               secure="false", domain_specified=True,
               domain_initial_dot=True, discard=True,
               rest=None, rfc2109=True,
               comment=None, comment_url=None,
               port=None, port_specified=False,
               version=1, path_specified=True)
         self.session.cookies.set_cookie(csrf)
         print self.session.cookies

   def get(self, url, data=False):
      headers = self.getHeaders()
      return self.session.get(self.url + url, headers=headers, params=data)

   def allTasks(self):
      params = {'type':'TASK', 'size':'10'}
      tasks = self.get('/api/todos', params)
      return json.loads(tasks.text)['values']

   ## TODO: Investigate this.
   ## Okay so we're setting the csrf header and cookie now, so this should
   ## work, but something is still fishy. All PUT requests that I have
   ## tried have been responded to with a "max retries exceeded" error
   ## and a BadStatusLine exception.
   def put(self, url, payload):
      headers = self.getHeaders()
      headers['content-type'] = 'application/json'
      headers['csrf'] = self.csrf
      return self.session.put(self.url + url, data=payload, headers=headers)
   
   ## TODO: This won't work yet. See above TODO.
   def deleteTask(self, task):
      task['deleted'] = True
      return self.put('/api/todos/' + urllib.quote_plus(task['itemId']), task)

   def getHeaders(self):
      headers = {}
      headers['User-Agent'] = 'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.13) Gecko/20101206 Ubuntu/10.10 (maverick) Firefox/3.6.13'
      headers['charset'] = 'utf-8'
      headers['origin'] = 'http://echo.amazon.com'
      headers['referer'] = 'http://echo.amazon.com/spa/index.html'
      return headers
