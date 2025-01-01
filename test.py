from src.pushover import Pushover
import os
from dotenv import load_dotenv

load_dotenv()

# Method 1: Using environment variables (assuming PUSHOVER_APP_TOKEN and PUSHOVER_USER_TOKEN are set)
po = Pushover()
po.send("Hello, World environment variables!")

# Send a message with a title
po.send("Hello, World directly!", "My Custom Title")


# You can still use the PushoverMessage object for more complex messages
msg = po.msg("Hello with custom message object")
msg.set('title', 'Custom Title')
po.send(msg)

# Method 2: Explicitly providing tokens
po = Pushover(os.getenv("PUSHOVER_APP_TOKEN"))
po.user(os.getenv("PUSHOVER_USER_TOKEN"))

# Send messages using either method
po.send("Hello, World directly!")
