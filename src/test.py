from pushover import Pushover

# Using environment variables for tokens
po = Pushover()

# Simple message
po.send("Server backup completed successfully")

# Message with title
po.send(
    "CPU usage has exceeded 90%", 
    "High CPU Alert"
)

# Message with URL to logs
po.send(
    "New deployment completed", 
    "Deployment Status",
    url="https://github.com/myorg/myrepo/actions",
    url_title="View deployment logs"
)

# Using the message object for more control
msg = po.msg("Critical error in production")
msg.set('title', 'Production Alert')
msg.set('url', 'https://dashboard.myapp.com/errors/123')
msg.set('url_title', 'View error details')
msg.set('priority', 1)  # Set other parameters as needed
po.send(msg)