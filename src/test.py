from pushover import Pushover
import os

# Method 1: Using environment variables (most simple)
po = Pushover()  # Will automatically use environment variables for both app and user tokens

# Method 2: Explicitly providing all tokens at once
po = Pushover(
    token="your_app_token",
    user_token="your_user_token",
    user_device="optional_device_name"
)

# Method 3: Mix of explicit and environment variables
po = Pushover(token="your_app_token")  # Will use environment variable for user token

# Send messages
po.send("Hello, World!", "Optional Title")