## PyEcho

This is a Python API wrapper for the Amazon Echo (undocumented) API. It logs
into the Echo web app at `http://pitangui.amazon.com`.

### Use

Instantiate a PyEcho object using your Amazon credentials. It will automatically
log in to the web service.

```python
import PyEcho

echo = PyEcho.PyEcho("some@email.com", "some_password")
```

Or, if you want, you can use the included `EchoMonitor` script, which is
exactly that: a monitor for the Echo API. It will ask you for your email
and password, login, and then will show you a prompt where you may type
URLs of API endpoints to make authenticated requests against.

#### Dependencies
* Python
* BeautifulSoup 4
* Requests

