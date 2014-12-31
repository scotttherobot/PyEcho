# A test script for PyEcho
# By Scott Vanderlind, December 31 2014

import PyEcho, getpass

email = raw_input("Email: ")
password = getpass.getpass()
echo = PyEcho.PyEcho(email, password)

if echo:
   print "API Monitor. Type an endpoint (starting with /api/) to fetch."
   while True:
      endpoint = raw_input("> ")
      print echo.get(endpoint).text

