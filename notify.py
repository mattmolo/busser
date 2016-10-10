from pushbullet import Pushbullet
from api_key import api_key

pb = Pushbullet(api_key)
def notify(message, url):
    pb.push_link(message, url)
