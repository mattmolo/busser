# Busser Notification App

Grabs Purdue Citybus times for stops local to me. Adds a notification bell, which when clicked will send notifications when the bus is close. Notifications are sent via PushBullet and require an API key.  

Requires `api_key.py` which contains a PushBullet API Key like this:
```py
api_key = '8438d8f8fg8_not_real_key_84338388'
```

To run:
```bash
export FLASK_APP=busser.py
python busser.py
```

To run with docker:
```bash
docker build -t busser:latest .
docker run -d -p 4000:4000 busser
```

## TODO:
- [ ] [Make this better async with twisted](http://tavendo.com/blog/post/going-asynchronous-from-flask-to-twisted-klein/)
- [ ] Kill all threads when it dies (Solved with being in a docker.. but not a great solution)
- [ ] Support multiple users/possible auth (Only using this for 2 more months.. so eh)
