# A Python class for connection to the Amazon Echo API
# By Scott Vanderlind, December 31 2014
import requests, json, urllib, cookielib
from bs4 import BeautifulSoup

class PyEcho:

   url = "https://pitangui.amazon.com"
   email = ""
   password = ""
   session = False
   loginsuccess = False
   csrf = "-2092727538"

   def __init__(self, email, password):
      self.email = email 
      self.password = password
      self.session = requests.Session()
      self.login()

   ## Log in to the Amazon Echo API
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

      if 'x-amzn-requestid' not in login.headers:
         print "Error logging in! Got status " + str(login.status_code)
         self.loginsuccess = False
      else:
         print "Login success!"
         self.loginsuccess = True

   def tasks(self):
      params = {'type':'TASK', 'size':'10'}
      tasks = self.get('/api/todos', params)
      return json.loads(tasks.text)['values']
    
   def shoppingitems(self):
      params = {'type':'SHOPPING_ITEM', 'size':'10'}
      items = self.get('/api/todos', params)
      return json.loads(items.text)['values']

   def deleteTask(self, task):
      task['deleted'] = True
      return self.put('/api/todos/' + urllib.quote_plus(task['itemId']), task)

   def deleteShoppingItem(self, item):
      item['deleted'] = True
      return self.put('/api/todos/' + urllib.quote_plus(item['itemId']), item)

   def devices(self):
      devices = self.get('/api/devices/device')
      return json.loads(devices.text)['devices']

   def cards(self):
      params = {'limit':'10'}
      cards = self.get('/api/cards', params)
      return json.loads(cards.text)['cards']
   
   def notifications(self):
      notes = self.get('/api/notifications')
      return json.loads(notes.text)['notifications']

   def services(self):
      services = self.get('/api/third-party')
      return json.loads(services.text)['services']

   def preferences(self):
      prefs = self.get('/api/device-preferences')
      return json.loads(prefs.text)['devicePreferences']

   def wakeWords(self):
      words = self.get('/api/wake-word')
      return json.loads(words.text)['wakeWords']

   #####
   ## Helper functions are below
   #####

   ## Make an authenticated GET request
   def get(self, url, data=False):
      headers = self.getHeaders()
      return self.session.get(self.url + url, headers=headers, params=data)

   ## Make an authenticated PUT request
   def put(self, url, payload):
      headers = self.getHeaders()
      headers['Content-type'] = 'application/json'
      headers['csrf'] = self.getCsrfCookie()
      headers['Accept'] = 'application/json, text/javascript, */*; q=0.01'
      return self.session.put(url=self.url + url, data=json.dumps(payload), headers=headers)

   ## Fetch the CSRF token from the cookie jar, set by the server.
   ## CookieLib's documentation is really not great, at least that I could find
   ## so in order to get our csrf token from the cookie, we have to iterate
   ## over the jar and match by name. Fine. Whatever.
   def getCsrfCookie(self):
      for cookie in self.session.cookies:
         if cookie.name == "csrf":
            return cookie.value
   
   ## Prepare common headers that we send with all requests.
   def getHeaders(self):
      headers = {}
      headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A'
      headers['Charset'] = 'utf-8'
      headers['Origin'] = 'http://echo.amazon.com'
      headers['Referer'] = 'http://echo.amazon.com/spa/index.html'
      return headers
