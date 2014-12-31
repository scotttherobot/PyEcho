# A Python class for connection to the Amazon Echo API
# By Scott Vanderlind, December 31 2014
import requests
from bs4 import BeautifulSoup

class PyEcho:

   url = "https://pitangui.amazon.com"
   email = ""
   password = ""
   session = False

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
         #print BeautifulSoup(login.text).prettify()

   def get(self, url):
      headers = self.getHeaders()
      return self.session.get(self.url + url, headers=headers)

   def getHeaders(self):
      headers = {}
      headers['User-Agent'] = 'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.13) Gecko/20101206 Ubuntu/10.10 (maverick) Firefox/3.6.13'
      headers['charset'] = 'utf-8'

      return headers
