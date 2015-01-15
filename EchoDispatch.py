# A dispatch script for PyEcho. This script triggers events
# based on commands that are spoken to Alexa.
# By Scott Vanderlind, January 15 2015

import PyEcho, getpass, time

# Create an Echo object
email = raw_input("Email: ")
password = getpass.getpass()
echo = PyEcho.PyEcho(email, password)

# If we successfully logged in, loop and wait for events.
if echo:
   while True:
      # Get a list of tasks...
      tasks = echo.tasks()
      # For every task in the list...
      for task in tasks:
         # Parse the task, do some event.
         # Here is where you might do a regex against the task text to
         # make a decision on what to do.
         command = task['text']
         print "NEW COMMAND: " + command

         # When we're done, delete it.
         res = echo.deleteTask(task)
         if res.status_code == 200:
            print "Task completed and deleted"

      # Sleep a bit before checking for new events.
      time.sleep(5)

