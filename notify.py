from pushbullet import Pushbullet
import os

pb = Pushbullet(os.getenv('BUSSER_API_KEY', ''))
def notify(message, url):
    pb.push_link(message, url)
