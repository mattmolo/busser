# Busser Notification App

Grabs Purdue Citybus times for stops local to me. Adds a notification bell, which when clicked will send notifications when the bus is close.  

Requires `api_key.py` which contains a PushBullet API Key like this:
```py
api_key = '8438d8f8fg8_not_real_key_84338388'
```

## TODO:
- [ ] [Make this better async with twisted](http://tavendo.com/blog/post/going-asynchronous-from-flask-to-twisted-klein/)
- [ ] Kill all threads when it dies
- [ ] Support multiple users/possible auth (Only using this for 2 more months.. so eh)
