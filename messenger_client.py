from fbchat import *
import fbchat
import config
import urllib.request as url


fb_client: Client
fb_thread: int


def login():
    global fb_client
    fb_client = fbchat.Client(config.FB_EMAIL, config.FB_PASSWORD)


def send_msg(map_url: str, message: str):
    global fb_client
    if fb_client is None:
        login()

    url.urlretrieve(map_url, "map.png")
    fb_client.sendLocalImage("map.png", message, fb_thread, fbchat.ThreadType.GROUP)

