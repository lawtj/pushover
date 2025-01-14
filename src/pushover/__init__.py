from http.client import HTTPSConnection
from urllib.parse import urlencode
import json
import os

class PushoverError(Exception): pass

class PushoverMessage:
    """
    Used for storing message specific data.
    """

    def __init__(self, message):
        """
        Creates a PushoverMessage object.
        """
        self.vars = {}
        self.vars['message'] = message

    def set(self, key, value):
        """
        Sets the value of a field "key" to the value of "value".
        """
        if value is not None:
            self.vars[key] = value

    def get(self):
        """
        Returns a dictionary with the values for the specified message.
        """
        return self.vars

    def user(self, user_token, user_device=None):
        """
        Sets a single user to be the recipient of this message with token "user_token" and device "user_device".
        """
        self.set('user', user_token)
        self.set('device', user_device)

    def __str__(self):
        return "PushoverMessage: " + str(self.vars)
    

class Pushover:
    """
    Creates a Pushover handler.

    Usage:

        po = Pushover("My App Token")
        po.user("My User Token", "My User Device Name")

        msg = po.msg("Hello, World!")

        po.send(msg)

    """

    PUSHOVER_SERVER = "api.pushover.net:443"
    PUSHOVER_ENDPOINT = "/1/messages.json"
    PUSHOVER_CONTENT_TYPE = { "Content-type": "application/x-www-form-urlencoded"}

    def __init__(self, token: str | None = None, user_token: str | None = None, user_device: str | None = None):
        """
        Creates a Pushover object.
        
        Args:
            token: Optional[str] - The application token. If not provided, 
                                 will look for PUSHOVER_APP_TOKEN in environment variables
            user_token: Optional[str] - The user token. If not provided,
                                      will look for PUSHOVER_USER_TOKEN in environment variables
            user_device: Optional[str] - The specific device to send to (optional)
        
        Raises:
            PushoverError: If no token is supplied and PUSHOVER_APP_TOKEN is not set
        """
        if token is None:
            token = os.getenv('PUSHOVER_APP_TOKEN')
            if token is None:
                raise PushoverError("No token supplied and PUSHOVER_APP_TOKEN environment variable not set.")
        
        self.token = token
        self.user_token = None
        self.user_device = None
        self.messages = []
        
        # Automatically set up user credentials
        self.user(user_token, user_device)

    def msg(self, message):
        """
        Creates a PushoverMessage object. Takes one "message" parameter (the message to be sent).
        Returns with PushoverMessage object (msg).
        """

        message = PushoverMessage(message)
        self.messages.append(message)
        return message

    def send(
        self, 
        message: str | PushoverMessage, 
        title: str | None = None,
        url: str | None = None,
        url_title: str | None = None
    ) -> bool:
        """
        Sends a specified message. Can accept either a PushoverMessage object or a string.
        
        Args:
            message: Union[PushoverMessage, str] - The message to send
            title: Optional[str] - The title of the message (only used when message is a string)
            url: Optional[str] - A supplementary URL to show with the message
            url_title: Optional[str] - A title for the URL (only used when url is provided)
            
        Returns:
            bool: True if message was sent successfully
            
        Raises:
            PushoverError: If the message fails to send
        """
        if isinstance(message, PushoverMessage):
            return self._send(message)
        elif isinstance(message, str):
            temp_message = PushoverMessage(message)
            if title:
                temp_message.set('title', title)
            if url:
                temp_message.set('url', url)
                if url_title:
                    temp_message.set('url_title', url_title)
            if self.user_token:
                temp_message.user(self.user_token, self.user_device)
            return self._send(temp_message)

    def sendall(self):
        """
        Sends all PushoverMessage's owned by the Pushover object.
        """

        response = []
        for message in self.messages:
            response.append(self._send(message))
        return response

    def user(self, user_token: str | None = None, user_device: str | None = None):
        """
        Sets a single user to be the recipient of all messages created with this Pushover object.
        If no user_token is provided, will look for PUSHOVER_USER_TOKEN in environment variables.
        
        Args:
            user_token: Optional[str] - The user token. If not provided, 
                                      will look for PUSHOVER_USER_TOKEN in environment variables
            user_device: Optional[str] - The specific device to send to (optional)
            
        Raises:
            PushoverError: If no user token is supplied and PUSHOVER_USER_TOKEN is not set
        """
        if user_token is None:
            user_token = os.getenv('PUSHOVER_USER_TOKEN')
            if user_token is None:
                raise PushoverError("No user token supplied and PUSHOVER_USER_TOKEN environment variable not set.")
        
        self.user_token = user_token
        self.user_device = user_device

    def _send(self, message):
        """
        Sends the specified PushoverMessage object via the Pushover API.
        """

        kwargs = message.get()
        kwargs['token'] = self.token

        assert 'message' in kwargs
        assert self.token is not None

        if not 'user' in kwargs:
            if self.user is not None:
                kwargs['user'] = self.user_token
                if self.user_device is not None:
                    kwargs['device'] = self.user_device
            else:
                kwargs['user'] = os.environ['PUSHOVER_USER']

        data = urlencode(kwargs)
        conn = HTTPSConnection(Pushover.PUSHOVER_SERVER)
        conn.request("POST", Pushover.PUSHOVER_ENDPOINT, data, Pushover.PUSHOVER_CONTENT_TYPE)
        output = conn.getresponse().read().decode('utf-8')
        data = json.loads(output)

        if data['status'] != 1:
            raise PushoverError(output)
        else:
            return True