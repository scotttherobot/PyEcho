## PyEcho

This is a Python API wrapper for the Amazon Echo (undocumented) API. It logs
into the Echo web app at `http://pitangui.amazon.com`.

### Use

Instantiate a PyEcho object using your Amazon credentials. It will automatically
log in to the web service.

```python
import PyEcho

# Create an echo object
echo = PyEcho.PyEcho("some@email.com", "some_password")

# Listen for events.
# This is naïve, it assumes the above worked.
while True:
   # Fetch our tasks
   tasks = echo.tasks()

   # Process each one
   for task in tasks:
      # Do something depending on the task here.
      print "New task found: " + task['text']

      # Now that we're done with it, delete it.
      # Again, this is naïve. We should error check the response code.
      echo.deleteTask(task)

   # Wait 10 seconds and do it again
   time.sleep(10)
```

Or, if you want, you can use the included `EchoMonitor` script, which is
essentially a monitor prompt for the Echo API. It will ask you for your email
and password, login, and then will show you a prompt where you may type
URLs of API endpoints to make authenticated requests against (GET).

#### Dependencies
* Python
* BeautifulSoup 4
* Requests
* urllib
* cookielib

