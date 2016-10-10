# Busser Notification App

Grabs Purdue Citybus times for stops local to me. Adds a notification bell, which when clicked will send notifications when the bus is close. Notifications are sent via PushBullet and require an API key.  

Environmental variables must be set for the PushBullet API and the host it's running on.
- `BUSSER_URL_HOST` is the url host in this form `protocal://domain.com:port`. Notice no trailing `/`
- `BUSSER_API_KEY` is the PushBullet API key from your account.

To run:
```bash
export BUSSER_URL_HOST=http://domain.name:4000
export BUSSER_API_KEY=3839292.not.a.real.key.383838
export FLASK_APP=busser.py
python busser.py
```

To run with docker:
```bash
docker build -t -e "BUSSER_URL_HOST=http://domain.name:4000" -e "BUSSER_API_KEY=3839292.not.a.real.key.383838" busser:latest .
docker run -d -p 4000:4000 busser
```

## TODO:
- [ ] [Make this better async with twisted](http://tavendo.com/blog/post/going-asynchronous-from-flask-to-twisted-klein/)
- [ ] Kill all threads when it dies (Solved with being in a docker.. but not a great solution)
- [ ] Support multiple users/possible auth (Only using this for 2 more months.. so eh)
