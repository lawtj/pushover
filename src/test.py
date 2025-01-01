from pushover import Pushover
import os
po = Pushover(os.getenv("APP_TOKEN"))
po.user(os.getenv("USER_TOKEN"))

# Method 1: Using PushoverMessage object (original way)
msg = po.msg("Hello, World!")
po.send(msg)

# Method 2: Directly sending a string
po.send("Hello, World directly!")
