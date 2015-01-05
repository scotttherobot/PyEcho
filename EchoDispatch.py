# A test script for PyEcho
# By Scott Vanderlind, January 3 2015

import PyEcho, getpass, time

email = raw_input("Email: ")
password = getpass.getpass()
echo = PyEcho.PyEcho(email, password)

if echo:
   while True:
      tasks = echo.tasks()
      for task in tasks:
         print "NEW TODO: " + task['text']
         res = echo.deleteTask(task)
         if res.status_code == 200:
            print "Task completed and deleted"
      time.sleep(5)

